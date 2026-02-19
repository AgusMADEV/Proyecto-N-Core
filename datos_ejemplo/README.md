# 📁 Datos de Ejemplo

Esta carpeta contiene archivos de texto de ejemplo para probar el procesamiento paralelo de archivos de la **Versión 2.0**.

## 📄 Archivos Incluidos

Los archivos de ejemplo incluyen artículos informativos sobre diferentes temas relacionados con programación y procesamiento paralelo:

1. **articulo1_procesamiento_paralelo.txt** - Introducción al procesamiento paralelo en Python
2. **articulo2_multicore.txt** - Programación multinúcleo y sus conceptos
3. **articulo3_python.txt** - El lenguaje Python y sus características
4. **articulo4_analisis_texto.txt** - Análisis de texto con Python
5. **articulo5_optimizacion.txt** - Optimización de código Python

## 🎯 Propósito

Estos archivos permiten:
- ✅ Probar el procesamiento secuencial y paralelo
- ✅ Ver las diferencias de rendimiento
- ✅ Analizar estadísticas de texto reales
- ✅ Comparar resultados entre ambos métodos

## 🚀 Uso

Los scripts `version2_secuencial.py` y `version2_paralelo.py` buscan automáticamente archivos `.txt` en esta carpeta.

Simplemente ejecuta:
```powershell
python version2_secuencial.py
# o
python version2_paralelo.py
```

## ➕ Agregar Más Archivos

Puedes agregar tus propios archivos `.txt` a esta carpeta para procesarlos. Los scripts detectarán automáticamente todos los archivos `.txt` disponibles.

**Recomendaciones:**
- Usa codificación UTF-8 para los archivos
- Los archivos más grandes mostrarán mejores diferencias de rendimiento
- Prueba con diferentes cantidades de archivos para ver el impacto del paralelismo
