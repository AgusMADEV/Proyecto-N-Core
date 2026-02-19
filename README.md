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

### Versión 2: Procesamiento de Archivos (ACTUAL) ✨
- `version2_secuencial.py` - Lectura y análisis de archivos secuencial
- `version2_paralelo.py` - Lectura y análisis de archivos en paralelo
- `comparador_v2.py` - Compara rendimiento de procesamiento de archivos
- `datos_ejemplo/` - Carpeta con archivos de texto de ejemplo para procesar

### Versiones Futuras
- Versión 3: Procesamiento de imágenes
- Versión 4: Interfaz gráfica con monitorización

## 🔧 Requisitos
- Python 3.8 o superior
- Biblioteca estándar (no requiere instalaciones adicionales)

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

## 🎓 Basado en
- Apuntes de Programación Multiproceso
- Ejercicios de clase de procesamiento paralelo
- Proyecto de referencia: Sistema de Procesamiento de Imágenes

---
**Autor:** AgusMAdev