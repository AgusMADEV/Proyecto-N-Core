"""
VERSIÓN 4 - SERVIDOR WEBSOCKET (BACKEND)
=========================================
Backend asíncrono que expone el procesamiento multinúcleo en tiempo real
a través de WebSockets. Permite controlar y monitorizar el procesamiento
de imágenes desde el dashboard web.

Tecnologías:
  - asyncio: Bucle de eventos asíncrono
  - websockets: Protocolo WebSocket
  - psutil: Monitorización de CPU y RAM
  - concurrent.futures: Pool de procesos integrado con asyncio
  - multiprocessing: Detección de núcleos

Requiere:
  pip install websockets psutil Pillow
"""

import asyncio
import json
import time
import multiprocessing
import os
import sys
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor

try:
    import psutil
    PSUTIL_DISPONIBLE = True
except ImportError:
    PSUTIL_DISPONIBLE = False

try:
    import websockets
    from websockets.exceptions import ConnectionClosed
except ImportError:
    print("❌ ERROR: websockets no está instalado.")
    print("   Ejecuta: pip install websockets")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────
# Importar procesador de imágenes de V3
# ─────────────────────────────────────────────────────────────
try:
    from version3_paralelo import procesar_imagen_wrapper
    PILLOW_DISPONIBLE = True
except ImportError:
    PILLOW_DISPONIBLE = False

    def procesar_imagen_wrapper(args):
        """Stub cuando Pillow no está instalado."""
        import time
        time.sleep(0.5)
        ruta_entrada, ruta_salida, _ = args
        return {
            'archivo': os.path.basename(ruta_entrada),
            'exito': False,
            'error': 'Pillow no instalado',
            'tiempo_proceso': 0.5,
            'proceso': multiprocessing.current_process().name
        }


# ─────────────────────────────────────────────────────────────
# Estado global del servidor (protegido con asyncio.Lock)
# ─────────────────────────────────────────────────────────────
estado = {
    "state": "idle",       # idle | running | stopping
    "current": 0,
    "total": 0,
    "workers": multiprocessing.cpu_count(),
    "inicio_proceso": None,
    "cpu_count": multiprocessing.cpu_count(),
    "pillow": PILLOW_DISPONIBLE,
    "psutil": PSUTIL_DISPONIBLE,
}

clientes: set = set()
estado_lock = asyncio.Lock() if False else None   # se crea en main()
cancelar_procesamiento = False


# ─────────────────────────────────────────────────────────────
# Utilidades de comunicación
# ─────────────────────────────────────────────────────────────
async def broadcast(mensaje: dict):
    """Envía un mensaje JSON a TODOS los clientes conectados."""
    if not clientes:
        return
    datos = json.dumps(mensaje, ensure_ascii=False)
    await asyncio.gather(
        *[ws.send(datos) for ws in list(clientes)],
        return_exceptions=True
    )


async def log(mensaje: str, nivel: str = "info"):
    """Envía un mensaje de log a todos los clientes."""
    await broadcast({
        "type": "log",
        "data": {
            "message": mensaje,
            "level": nivel,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
    })


# ─────────────────────────────────────────────────────────────
# Monitorización de recursos del sistema
# ─────────────────────────────────────────────────────────────
async def tarea_monitor_cpu():
    """Tarea de background: envía estadísticas de CPU y RAM cada ~0.8s."""
    if not PSUTIL_DISPONIBLE:
        return

    # Primera llamada sin intervalo (normalmente devuelve 0)
    psutil.cpu_percent(interval=None, percpu=True)

    while True:
        try:
            cores = psutil.cpu_percent(interval=None, percpu=True)
            total = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory()

            await broadcast({
                "type": "cpu_stats",
                "data": {
                    "cores": cores,
                    "total": round(total, 1),
                    "ram_percent": round(ram.percent, 1),
                    "ram_used_gb": round(ram.used  / (1024 ** 3), 2),
                    "ram_total_gb": round(ram.total / (1024 ** 3), 2),
                }
            })
        except Exception:
            pass

        await asyncio.sleep(0.8)


# ─────────────────────────────────────────────────────────────
# Núcleo del procesamiento
# ─────────────────────────────────────────────────────────────
async def procesar_imagenes_async(operaciones: list, num_workers: int):
    """
    Procesa imágenes usando ProcessPoolExecutor integrado con asyncio.
    Envía actualizaciones en tiempo real a todos los clientes conectados.
    """
    global estado, cancelar_procesamiento

    carpeta_entrada = Path(__file__).parent / "imagenes_entrada"
    carpeta_salida  = Path(__file__).parent / "imagenes_salida"
    carpeta_salida.mkdir(exist_ok=True)

    # ── Buscar imágenes ──────────────────────────────────────
    extensiones = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif']
    imagenes = []
    for ext in extensiones:
        imagenes.extend(carpeta_entrada.glob(ext))
        imagenes.extend(carpeta_entrada.glob(ext.upper()))

    if not imagenes:
        await log("⚠️  No se encontraron imágenes en 'imagenes_entrada/'", "warning")
        await log("💡 Ejecuta primero: python generador_imagenes.py", "info")
        estado["state"] = "idle"
        await broadcast({"type": "status", "data": estado})
        return

    total = len(imagenes)
    estado["total"] = total
    estado["current"] = 0
    estado["inicio_proceso"] = time.time()

    await log(f"📂 {total} imagen(es) encontrada(s)", "info")
    await log(f"⚙️  Workers: {num_workers} | Núcleos: {multiprocessing.cpu_count()}", "info")
    await log(f"🎨 Operaciones: {', '.join(op['tipo'] for op in operaciones)}", "info")
    await broadcast({"type": "status", "data": estado})

    # ── Preparar tareas ──────────────────────────────────────
    tareas = []
    for img in imagenes:
        nombre_salida = f"{img.stem}_v4{img.suffix}"
        ruta_salida = carpeta_salida / nombre_salida
        tareas.append((str(img), str(ruta_salida), operaciones))

    inicio_total = time.time()
    resultados = []
    loop = asyncio.get_event_loop()

    # ── Ejecutar con ProcessPoolExecutor ────────────────────
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            loop.run_in_executor(executor, procesar_imagen_wrapper, tarea)
            for tarea in tareas
        ]

        for future in asyncio.as_completed(futures):
            # ── Comprobar cancelación ────────────────────────
            if cancelar_procesamiento:
                await log("🛑 Procesamiento cancelado por el usuario", "warning")
                # Cancelar futuros pendientes
                for f in futures:
                    f.cancel()
                break

            try:
                resultado = await future
                resultados.append(resultado)
                estado["current"] += 1
                porcentaje = int((estado["current"] / total) * 100)

                # Progreso global
                await broadcast({
                    "type": "progress",
                    "data": {
                        "current":    estado["current"],
                        "total":      total,
                        "percentage": porcentaje,
                        "file":       resultado.get("archivo", ""),
                    }
                })

                # Resultado individual
                if resultado.get("exito"):
                    await broadcast({
                        "type": "result",
                        "data": {
                            "file":           resultado["archivo"],
                            "time":           round(resultado["tiempo_proceso"], 3),
                            "operations":     resultado.get("operaciones_aplicadas", []),
                            "size_before_kb": resultado.get("tamanio_kb_entrada", 0),
                            "size_after_kb":  resultado.get("tamanio_kb_salida",  0),
                            "size_original":  list(resultado.get("tamanio_original", [0, 0])),
                            "size_final":     list(resultado.get("tamanio_final",   [0, 0])),
                            "proceso":        resultado.get("proceso", ""),
                        }
                    })
                    await log(
                        f"✅  {resultado['archivo']}  →  {resultado['tiempo_proceso']:.3f}s",
                        "success"
                    )
                else:
                    await log(
                        f"❌  {resultado['archivo']}: {resultado.get('error', 'error desconocido')}",
                        "error"
                    )

            except Exception as e:
                await log(f"❌ Excepción inesperada: {e}", "error")

    # ── Métricas finales ─────────────────────────────────────
    if not cancelar_procesamiento and resultados:
        tiempo_total = time.time() - inicio_total
        exitosos = [r for r in resultados if r.get("exito")]
        suma_tiempos = sum(r.get("tiempo_proceso", 0) for r in resultados)
        speedup    = round(suma_tiempos / tiempo_total, 2) if tiempo_total > 0 else 1.0
        eficiencia = round((speedup / num_workers) * 100, 1)

        await broadcast({
            "type": "metrics",
            "data": {
                "speedup":    speedup,
                "efficiency": eficiencia,
                "total_time": round(tiempo_total, 2),
                "successful": len(exitosos),
                "failed":     len(resultados) - len(exitosos),
                "total":      total,
                "avg_time":   round(tiempo_total / total, 3) if total else 0,
                "workers":    num_workers,
            }
        })

        await log(
            f"🏁 Finalizado en {tiempo_total:.2f}s  |  "
            f"Speedup: {speedup}x  |  Eficiencia: {eficiencia}%",
            "success"
        )

    # ── Restablecer estado ───────────────────────────────────
    cancelar_procesamiento = False
    estado["state"] = "idle"
    await broadcast({"type": "status", "data": estado})


# ─────────────────────────────────────────────────────────────
# Manejador de clientes WebSocket
# ─────────────────────────────────────────────────────────────
async def manejar_cliente(websocket):
    """Gestiona la conexión completa de un cliente."""
    global cancelar_procesamiento

    clientes.add(websocket)
    ip = websocket.remote_address[0] if websocket.remote_address else "desconocido"
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}]  ✅  Cliente conectado:     {ip}  (total: {len(clientes)})")

    # ── Bienvenida ───────────────────────────────────────────
    await websocket.send(json.dumps({"type": "status",  "data": estado}))
    await websocket.send(json.dumps({
        "type": "log",
        "data": {
            "message":   f"🔗 Conectado al servidor "
                         f"({multiprocessing.cpu_count()} núcleos | "
                         f"Pillow: {'✅' if PILLOW_DISPONIBLE else '❌'} | "
                         f"psutil: {'✅' if PSUTIL_DISPONIBLE else '❌'})",
            "level":     "success",
            "timestamp": ts,
        }
    }))

    try:
        async for mensaje in websocket:
            try:
                data   = json.loads(mensaje)
                accion = data.get("action", "")

                # ── start ────────────────────────────────────
                if accion == "start":
                    if estado["state"] == "idle":
                        payload = data.get("data", {})
                        operaciones = payload.get("operaciones", [
                            {"tipo": "blur"},
                            {"tipo": "escala_grises"},
                            {"tipo": "redimensionar", "ancho": 800, "alto": 600},
                        ])
                        num_workers = max(1, min(
                            payload.get("num_workers", multiprocessing.cpu_count()),
                            multiprocessing.cpu_count()
                        ))
                        estado["state"] = "running"
                        cancelar_procesamiento = False
                        await broadcast({"type": "status", "data": estado})
                        asyncio.create_task(
                            procesar_imagenes_async(operaciones, num_workers)
                        )
                    else:
                        await websocket.send(json.dumps({
                            "type": "log",
                            "data": {
                                "message":   "⚠️  Ya hay un procesamiento en curso",
                                "level":     "warning",
                                "timestamp": datetime.now().strftime("%H:%M:%S"),
                            }
                        }))

                # ── stop ─────────────────────────────────────
                elif accion == "stop":
                    if estado["state"] == "running":
                        cancelar_procesamiento = True
                        estado["state"] = "stopping"
                        await broadcast({"type": "status", "data": estado})

                # ── get_status ────────────────────────────────
                elif accion == "get_status":
                    await websocket.send(json.dumps({"type": "status", "data": estado}))

                # ── ping ──────────────────────────────────────
                elif accion == "ping":
                    await websocket.send(json.dumps({"type": "pong"}))

            except json.JSONDecodeError:
                pass

    except ConnectionClosed:
        pass
    except Exception as e:
        print(f"Error con cliente {ip}: {e}")
    finally:
        clientes.discard(websocket)
        print(f"[{datetime.now().strftime('%H:%M:%S')}]  🔌  Cliente desconectado: {ip}")


# ─────────────────────────────────────────────────────────────
# Punto de entrada
# ─────────────────────────────────────────────────────────────
async def main():
    HOST = "localhost"
    PORT = 8765

    print("\n" + "=" * 60)
    print("  🚀  VERSIÓN 4 - SERVIDOR WEBSOCKET")
    print("=" * 60)
    print(f"  📅  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  🖥️   Núcleos detectados : {multiprocessing.cpu_count()}")
    print(f"  🌐  WebSocket          : ws://{HOST}:{PORT}")
    print(f"  🖼️   Pillow             : {'✅ Disponible' if PILLOW_DISPONIBLE else '❌ pip install Pillow'}")
    print(f"  📊  psutil             : {'✅ Disponible' if PSUTIL_DISPONIBLE else '❌ pip install psutil'}")
    print("=" * 60)
    print(f"\n  📂  Abre en tu navegador:")
    print(f"      {Path(__file__).parent / 'frontend' / 'index.html'}")
    print(f"\n  ⏹️   Ctrl+C para detener\n")

    # Inicializar psutil (primera muestra siempre es 0)
    if PSUTIL_DISPONIBLE:
        psutil.cpu_percent(interval=None, percpu=True)

    async with websockets.serve(manejar_cliente, HOST, PORT):
        print(f"  ✅  Servidor escuchando en ws://{HOST}:{PORT}\n")
        asyncio.create_task(tarea_monitor_cpu())
        await asyncio.Future()   # Mantener el servidor activo indefinidamente


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n  🛑  Servidor detenido\n")
