# 🚀 Proyecto: Procesamiento Multinúcleo en Python

## 📋 Descripción
Este proyecto demuestra el uso de **procesamiento multinúcleo** en Python para mejorar el rendimiento de aplicaciones que requieren cálculos intensivos.

## 🎯 Objetivo
Demostrar cómo un proceso puede dividirse en procesos paralelos que se ejecutan simultáneamente en múltiples núcleos, reduciendo significativamente el tiempo de procesamiento.

## 📂 Estructura del Proyecto

### Versión 1: Procesamiento de Números
- `version1_secuencial.py` - Procesamiento secuencial de números (sin paralelismo)
- `version1_paralelo.py` - Procesamiento de números con multiprocessing
- `comparador.py` - Compara el rendimiento de ambos enfoques

### Versión 2: Procesamiento de Archivos
- `version2_secuencial.py` - Lectura y análisis de archivos secuencial
- `version2_paralelo.py` - Lectura y análisis de archivos en paralelo
- `comparador_v2.py` - Compara rendimiento de procesamiento de archivos
- `datos_ejemplo/` - Carpeta con archivos de texto de ejemplo para procesar

### Versión 3: Procesamiento de Imágenes (ACTUAL) ✨
- `version3_secuencial.py` - Procesamiento secuencial de imágenes con filtros
- `version3_paralelo.py` - Procesamiento paralelo de imágenes
- `comparador_v3.py` - Compara rendimiento de procesamiento de imágenes
- `generador_imagenes.py` - Genera imágenes de ejemplo para pruebas
- `imagenes_entrada/` - Carpeta con imágenes para procesar
- `imagenes_salida/` - Carpeta con imágenes procesadas

### Versión 4: Interfaz Gráfica Web (ACTUAL) ✨
- `servidor.py` - Backend WebSocket asíncrono (asyncio)
- `frontend/index.html` - Dashboard web en tiempo real
- `frontend/app.js` - Lógica del cliente WebSocket
- `frontend/styles.css` - Tema oscuro del dashboard

### Versiones Futuras
- Versión 5: Optimizaciones avanzadas (caché, colas con prioridad)

## 🔧 Requisitos
- Python 3.8 o superior
- Biblioteca estándar (no requiere instalaciones adicionales para V1 y V2)
- **Pillow** (requerido para Versiones 3 y 4):
  ```powershell
  pip install Pillow
  ```
- **websockets + psutil** (requerido para Versión 4):
  ```powershell
  pip install websockets psutil
  ```

## 🚀 Uso

### Versión 1: Procesamiento de Números

#### Ejecutar procesamiento secuencial
```powershell
python version1_secuencial.py
```

#### Ejecutar procesamiento paralelo
```powershell
python version1_paralelo.py
```

#### Comparar rendimiento
```powershell
python comparador.py
```

### Versión 2: Procesamiento de Archivos ✨

#### Ejecutar análisis secuencial de archivos
```powershell
python version2_secuencial.py
```

#### Ejecutar análisis paralelo de archivos
```powershell
python version2_paralelo.py
```

#### Comparar rendimiento de versión 2
```powershell
python comparador_v2.py
```

**Nota:** Los scripts buscan archivos `.txt` en la carpeta `datos_ejemplo/`. La carpeta ya incluye 5 archivos de ejemplo para probar.

### Versión 3: Procesamiento de Imágenes ✨

#### Generar imágenes de ejemplo
```powershell
python generador_imagenes.py
```

#### Ejecutar procesamiento secuencial de imágenes
```powershell
python version3_secuencial.py
```

#### Ejecutar procesamiento paralelo de imágenes
```powershell
python version3_paralelo.py
```

#### Comparar rendimiento de versión 3
```powershell
python comparador_v3.py
```

**Nota:** Puedes generar imágenes de prueba con `generador_imagenes.py` o usar tus propias imágenes en la carpeta `imagenes_entrada/`.

### Versión 4: Interfaz Gráfica Web ✨

#### Paso 1 — Instalar dependencias
```powershell
pip install websockets psutil Pillow
```

#### Paso 2 — Iniciar el servidor
```powershell
python servidor.py
```

#### Paso 3 — Abrir el dashboard
Abre el archivo `frontend/index.html` en tu navegador.

**Características del dashboard:**
- 📊 Monitorización en tiempo real de CPU por núcleo
- 📈 Métricas: Speedup, Eficiencia, Tiempo total
- ▶ Control de procesamiento (Iniciar / Detener)
- ⚙️ Configuración de workers y operaciones
- 📋 Consola de logs en vivo
- 🖼️ Resultados por imagen con tiempos

## 📊 Conceptos Aplicados

### Versión 1
- ✅ Procesos paralelos
- ✅ Uso de módulo `multiprocessing`
- ✅ Distribución de carga entre núcleos
- ✅ Medición de rendimiento
- ✅ Sincronización de resultados

### Versión 2
- ✅ Lectura de múltiples archivos en paralelo
- ✅ Análisis de texto y estadísticas
- ✅ Conteo de palabras, líneas y caracteres
- ✅ Identificación de palabras frecuentes
- ✅ Expresiones regulares para procesamiento de texto
- ✅ Manejo eficiente de archivos grandes
- ✅ Pool de procesos para I/O intensivo

### Versión 3
- ✅ Procesamiento paralelo de imágenes
- ✅ Aplicación de filtros (blur, escala de grises, sharpen)
- ✅ Redimensionamiento en batch
- ✅ Uso de Pillow (PIL) para manipulación de imágenes
- ✅ Procesamiento CPU-intensivo optimizado
- ✅ Múltiples formatos de imagen soportados
- ✅ Generación automática de imágenes de prueba

### Versión 4
- ✅ Servidor WebSocket asíncrono con `asyncio`
- ✅ Dashboard web en tiempo real
- ✅ Monitorización de CPU por núcleo con `psutil`
- ✅ Control interactivo (start / stop)
- ✅ Logs en vivo en consola web
- ✅ Métricas en tiempo real (speedup, eficiencia)
- ✅ Integración `ProcessPoolExecutor` + `asyncio`
- ✅ Broadcasting a múltiples clientes conectados

## 🎓 Basado en
- Apuntes de Programación Multiproceso
- Ejercicios de clase de procesamiento paralelo
- Proyecto de referencia: Sistema de Procesamiento de Imágenes

---
**Autor:** AgusMAdev