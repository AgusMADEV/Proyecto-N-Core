/**
 * VERSIÓN 4 — DASHBOARD MULTINÚCLEO
 * Lógica del cliente WebSocket en tiempo real
 *
 * Flujo:
 *  1. Intenta conectar al servidor ws://localhost:8765
 *  2. Recibe mensajes JSON y actualiza la UI
 *  3. Envía comandos (start / stop) al servidor
 */

"use strict";

/* ══════════════════════════════════════════════════════════
   CONFIGURACIÓN
══════════════════════════════════════════════════════════ */
const WS_URL        = "ws://localhost:8765";
const RECONECT_DELAY = 3000;   // ms entre intentos de reconexión

/* ══════════════════════════════════════════════════════════
   REFERENCIAS AL DOM
══════════════════════════════════════════════════════════ */
const $ = id => document.getElementById(id);

const DOM = {
  connDot:          $("connDot"),
  connLabel:        $("connLabel"),
  stateBadge:       $("stateBadge"),

  // Sistema info
  sysCores:         $("sysCores"),
  sysPillow:        $("sysPillow"),
  sysPsutil:        $("sysPsutil"),
  cpuTotal:         $("cpuTotal"),
  cpuTotalBar:      $("cpuTotalBar"),
  ramInfo:          $("ramInfo"),
  ramBar:           $("ramBar"),
  cpuGrid:          $("cpuGrid"),

  // Métricas
  mSpeedup:         $("mSpeedup"),
  mEfficiency:      $("mEfficiency"),
  mTime:            $("mTime"),
  mImages:          $("mImages"),

  // Progreso
  progressBar:      $("progressBar"),
  progressLabel:    $("progressLabel"),
  progressCounter:  $("progressCounter"),
  progressFile:     $("progressFile"),

  // Resultados
  resultsBody:      $("resultsBody"),

  // Log
  logBody:          $("logBody"),

  // Controles
  btnStart:         $("btnStart"),
  btnStop:          $("btnStop"),
  workerSlider:     $("workerSlider"),
  workerVal:        $("workerVal"),
  resizeSelect:     $("resizeSelect"),
  opBlur:           $("opBlur"),
  opGrises:         $("opGrises"),
  opResize:         $("opResize"),
  opSharpen:        $("opSharpen"),
  opContorno:       $("opContorno"),
  btnClearLog:      $("btnClearLog"),
};

/* ══════════════════════════════════════════════════════════
   ESTADO DE LA APLICACIÓN
══════════════════════════════════════════════════════════ */
let ws            = null;
let reconectTimer = null;
let coresCount    = 0;
let coresDOMReady = false;
let resultCount   = 0;
let serverState   = "idle";   // idle | running | stopping

/* ══════════════════════════════════════════════════════════
   WEBSOCKET
══════════════════════════════════════════════════════════ */
function conectar() {
  addLog("🔌 Conectando a " + WS_URL + "...", "info");
  setConnected(false);

  ws = new WebSocket(WS_URL);

  ws.onopen = () => {
    clearTimeout(reconectTimer);
    setConnected(true);
    ws.send(JSON.stringify({ action: "get_status" }));
  };

  ws.onmessage = e => {
    let msg;
    try   { msg = JSON.parse(e.data); }
    catch { return; }
    handleMessage(msg);
  };

  ws.onclose = () => {
    setConnected(false);
    addLog("⚠️  Conexión cerrada. Reconectando en 3s...", "warning");
    reconectTimer = setTimeout(conectar, RECONECT_DELAY);
  };

  ws.onerror = () => {
    addLog("❌ Error de conexión — ¿está el servidor activo?", "error");
  };
}

function send(obj) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(obj));
  }
}

/* ══════════════════════════════════════════════════════════
   MANEJADOR CENTRAL DE MENSAJES
══════════════════════════════════════════════════════════ */
function handleMessage(msg) {
  switch (msg.type) {

    case "cpu_stats":
      updateCPU(msg.data);
      break;

    case "log":
      addLog(msg.data.message, msg.data.level, msg.data.timestamp);
      break;

    case "progress":
      updateProgress(msg.data);
      break;

    case "result":
      addResult(msg.data);
      break;

    case "status":
      updateStatus(msg.data);
      break;

    case "metrics":
      updateMetrics(msg.data);
      break;

    case "pong":
      // Keep-alive
      break;
  }
}

/* ══════════════════════════════════════════════════════════
   ACTUALIZAR UI
══════════════════════════════════════════════════════════ */

// ── Conexión ─────────────────────────────────────────────
function setConnected(ok) {
  DOM.connDot.className   = "conn-dot" + (ok ? " connected" : "");
  DOM.connLabel.textContent = ok ? "Conectado" : "Desconectado";
  DOM.btnStart.disabled   = !ok || serverState === "running";
}

// ── Status del servidor ───────────────────────────────────
function updateStatus(data) {
  serverState = data.state || "idle";

  // Badge de estado
  const labels = { idle: "● Inactivo", running: "⟳ Procesando", stopping: "■ Deteniendo" };
  DOM.stateBadge.textContent  = labels[serverState] || serverState;
  DOM.stateBadge.className    = "state-badge " + serverState;

  // Botones
  DOM.btnStart.disabled = serverState !== "idle";
  DOM.btnStop.disabled  = serverState !== "running";
  DOM.btnStart.className = serverState === "running"
    ? "btn btn-start running"
    : "btn btn-start";

  // Info del sistema (solo primera vez)
  if (data.cpu_count && !coresDOMReady) {
    DOM.sysCores.textContent = data.cpu_count + " núcleos";
    DOM.workerSlider.max     = data.cpu_count;
    DOM.workerSlider.value   = data.cpu_count;
    DOM.workerVal.textContent = data.cpu_count;
    buildCoreCards(data.cpu_count);
  }

  if (data.pillow !== undefined) {
    DOM.sysPillow.textContent = data.pillow ? "✅ OK" : "❌ No";
    DOM.sysPillow.style.color = data.pillow ? "var(--green)" : "var(--red)";
  }

  if (data.psutil !== undefined) {
    DOM.sysPsutil.textContent = data.psutil  ? "✅ OK" : "❌ No";
    DOM.sysPsutil.style.color = data.psutil  ? "var(--green)" : "var(--red)";
  }
}

// ── CPU por núcleo ────────────────────────────────────────
function buildCoreCards(n) {
  coresCount   = n;
  coresDOMReady = true;
  DOM.cpuGrid.innerHTML = "";

  for (let i = 0; i < n; i++) {
    const card = document.createElement("div");
    card.className = "core-card";
    card.innerHTML = `
      <span class="core-label">Core ${i}</span>
      <div class="core-usage-bar">
        <div class="core-bar-fill low" id="coreBar${i}" style="height:0%"></div>
      </div>
      <span class="core-pct" id="corePct${i}">0%</span>
    `;
    DOM.cpuGrid.appendChild(card);
  }
}

function updateCPU(data) {
  const cores = data.cores || [];

  // Reconstruir grid si cambia el número de núcleos
  if (cores.length !== coresCount) {
    buildCoreCards(cores.length);
  }

  cores.forEach((pct, i) => {
    const bar  = $(`coreBar${i}`);
    const lbl  = $(`corePct${i}`);
    if (!bar || !lbl) return;

    bar.style.height = pct + "%";
    lbl.textContent  = pct + "%";

    // Color según carga
    bar.className = "core-bar-fill " + (
      pct <  30 ? "low"    :
      pct <  60 ? "medium" :
      pct <  85 ? "high"   : "max"
    );
  });

  // CPU total
  const total = data.total || 0;
  DOM.cpuTotal.textContent = total + "%";
  DOM.cpuTotalBar.style.width = total + "%";

  // RAM
  if (data.ram_percent !== undefined) {
    DOM.ramInfo.textContent = `${data.ram_used_gb} / ${data.ram_total_gb} GB (${data.ram_percent}%)`;
    DOM.ramBar.style.width  = data.ram_percent + "%";

    // Color según uso de RAM
    const rp = data.ram_percent;
    DOM.ramBar.style.background =
      rp < 60 ? "var(--purple)" :
      rp < 80 ? "var(--orange)" : "var(--red)";
  }
}

// ── Progreso ──────────────────────────────────────────────
function updateProgress(data) {
  const pct     = data.percentage || 0;
  const current = data.current    || 0;
  const total   = data.total      || 0;

  DOM.progressBar.style.width    = pct + "%";
  DOM.progressLabel.textContent  = pct === 100
    ? "✅ Completado"
    : `Procesando... ${pct}%`;
  DOM.progressCounter.textContent = `${current} / ${total}`;
  DOM.progressFile.textContent    = data.file
    ? "📄 " + data.file
    : "Esperando...";

  DOM.mImages.textContent = `${current} / ${total}`;
}

// ── Resultado individual ──────────────────────────────────
function addResult(data) {
  // Quitar fila de "Sin resultados" la primera vez
  if (resultCount === 0) {
    DOM.resultsBody.innerHTML = "";
  }
  resultCount++;

  // Construir tags HTML de operaciones
  const opTagMap = {
    "Blur":               "blur",
    "Blur Intenso":       "blur",
    "Escala de Grises":   "grises",
    "Sharpen":            "sharpen",
    "Detección de Contornos": "contorno",
  };
  const tagsHTML = (data.operations || []).map(op => {
    const key = op.startsWith("Redimensionar") ? "resize" : (opTagMap[op] || "");
    const label = op.startsWith("Redimensionar") ? op : op;
    return `<span class="tag ${key}">${label}</span>`;
  }).join("");

  const workerNum = data.proceso
    ? data.proceso.replace("ForkPoolWorker-", "W").replace("SpawnPoolWorker-", "W")
    : "—";

  const tr = document.createElement("tr");
  tr.innerHTML = `
    <td title="${data.file}">${data.file}</td>
    <td>${tagsHTML}</td>
    <td>${data.size_before_kb} KB</td>
    <td>${data.size_after_kb} KB</td>
    <td style="font-family:var(--font-mono); color:var(--green)">${data.time}s</td>
    <td style="font-family:var(--font-mono); color:var(--blue)">${workerNum}</td>
  `;
  DOM.resultsBody.prepend(tr);   // más reciente arriba
}

// ── Métricas finales ──────────────────────────────────────
function updateMetrics(data) {
  DOM.mSpeedup.textContent    = data.speedup    + "×";
  DOM.mEfficiency.textContent = data.efficiency + "%";
  DOM.mTime.textContent       = data.total_time + "s";
  DOM.mImages.textContent     = `${data.successful} / ${data.total}`;
}

/* ══════════════════════════════════════════════════════════
   LOG CONSOLE
══════════════════════════════════════════════════════════ */
function addLog(message, level = "info", ts = null) {
  const timestamp = ts || new Date().toLocaleTimeString("es-ES", { hour12: false });
  const entry = document.createElement("div");
  entry.className = `log-entry ${level}`;
  entry.innerHTML = `
    <span class="log-ts">${timestamp}</span>
    <span class="log-msg">${escapeHTML(message)}</span>
  `;
  DOM.logBody.appendChild(entry);
  DOM.logBody.scrollTop = DOM.logBody.scrollHeight;

  // Limitar a 200 entradas para no saturar el DOM
  while (DOM.logBody.children.length > 200) {
    DOM.logBody.removeChild(DOM.logBody.firstChild);
  }
}

function escapeHTML(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

/* ══════════════════════════════════════════════════════════
   CONSTRUIR PAYLOAD DE OPERACIONES
══════════════════════════════════════════════════════════ */
function buildOperaciones() {
  const ops = [];

  if (DOM.opBlur.checked)     ops.push({ tipo: "blur" });
  if (DOM.opGrises.checked)   ops.push({ tipo: "escala_grises" });
  if (DOM.opSharpen.checked)  ops.push({ tipo: "sharpen" });
  if (DOM.opContorno.checked) ops.push({ tipo: "contorno" });

  if (DOM.opResize.checked) {
    const [w, h] = DOM.resizeSelect.value.split("x").map(Number);
    ops.push({ tipo: "redimensionar", ancho: w, alto: h });
  }

  // Al menos una operación
  if (ops.length === 0) ops.push({ tipo: "blur" });
  return ops;
}

/* ══════════════════════════════════════════════════════════
   EVENTOS DE CONTROLES
══════════════════════════════════════════════════════════ */

// Slider de workers
DOM.workerSlider.addEventListener("input", () => {
  DOM.workerVal.textContent = DOM.workerSlider.value;
});

// Botón INICIAR
DOM.btnStart.addEventListener("click", () => {
  if (serverState !== "idle") return;

  // Resetear UI de resultados y progreso
  resultCount = 0;
  DOM.resultsBody.innerHTML = `
    <tr>
      <td colspan="6" style="color:var(--text-muted); text-align:center; padding:14px">
        Procesando imágenes...
      </td>
    </tr>`;
  DOM.progressBar.style.width    = "0%";
  DOM.progressLabel.textContent  = "Iniciando...";
  DOM.progressCounter.textContent = "0 / 0";
  DOM.progressFile.textContent   = "";
  DOM.mSpeedup.textContent    = "—";
  DOM.mEfficiency.textContent = "—";
  DOM.mTime.textContent       = "—";
  DOM.mImages.textContent     = "0 / 0";

  send({
    action: "start",
    data: {
      operaciones: buildOperaciones(),
      num_workers: parseInt(DOM.workerSlider.value),
    }
  });
});

// Botón DETENER
DOM.btnStop.addEventListener("click", () => {
  if (serverState !== "running") return;
  send({ action: "stop" });
  addLog("🛑 Solicitando detención...", "warning");
});

// Limpiar log
DOM.btnClearLog.addEventListener("click", () => {
  DOM.logBody.innerHTML = "";
});

/* ══════════════════════════════════════════════════════════
   INICIO
══════════════════════════════════════════════════════════ */
conectar();
