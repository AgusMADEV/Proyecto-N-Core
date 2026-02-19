"""
VERSIÓN 2 - PROCESAMIENTO SECUENCIAL DE ARCHIVOS
=================================================
Este programa lee múltiples archivos de texto de forma SECUENCIAL
y realiza análisis estadístico del contenido.

Tarea: Leer archivos y calcular estadísticas de texto
Procesa un archivo tras otro en un solo núcleo del procesador.
"""

import time
import os
from datetime import datetime
from pathlib import Path
import re


def contar_palabras(texto):
    """
    Cuenta las palabras en un texto.
    
    Args:
        texto: String con el contenido del texto
    
    Returns:
        Número de palabras
    """
    palabras = texto.split()
    return len(palabras)


def contar_lineas(texto):
    """
    Cuenta las líneas en un texto.
    
    Args:
        texto: String con el contenido del texto
    
    Returns:
        Número de líneas
    """
    return len(texto.splitlines())


def contar_caracteres(texto):
    """
    Cuenta los caracteres en un texto.
    
    Args:
        texto: String con el contenido del texto
    
    Returns:
        Diccionario con conteos de caracteres
    """
    return {
        'total': len(texto),
        'sin_espacios': len(texto.replace(' ', '').replace('\n', '').replace('\t', '')),
        'espacios': texto.count(' '),
        'saltos_linea': texto.count('\n')
    }


def encontrar_palabras_frecuentes(texto, top_n=10):
    """
    Encuentra las palabras más frecuentes en el texto.
    
    Args:
        texto: String con el contenido del texto
        top_n: Número de palabras más frecuentes a retornar
    
    Returns:
        Lista de tuplas (palabra, frecuencia)
    """
    # Convertir a minúsculas y extraer palabras
    palabras = re.findall(r'\b\w+\b', texto.lower())
    
    # Contar frecuencias
    frecuencias = {}
    for palabra in palabras:
        if len(palabra) > 2:  # Ignorar palabras muy cortas
            frecuencias[palabra] = frecuencias.get(palabra, 0) + 1
    
    # Ordenar por frecuencia
    palabras_ordenadas = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)
    
    return palabras_ordenadas[:top_n]


def calcular_promedio_longitud_palabra(texto):
    """
    Calcula la longitud promedio de las palabras.
    
    Args:
        texto: String con el contenido del texto
    
    Returns:
        Promedio de longitud de palabras
    """
    palabras = re.findall(r'\b\w+\b', texto)
    if not palabras:
        return 0
    
    total_caracteres = sum(len(palabra) for palabra in palabras)
    return total_caracteres / len(palabras)


def analizar_archivo(ruta_archivo):
    """
    Lee y analiza un archivo de texto.
    
    Args:
        ruta_archivo: Ruta del archivo a procesar
    
    Returns:
        Diccionario con las estadísticas del archivo
    """
    inicio = time.time()
    
    try:
        # Leer el archivo
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Calcular estadísticas
        num_palabras = contar_palabras(contenido)
        num_lineas = contar_lineas(contenido)
        stats_caracteres = contar_caracteres(contenido)
        palabras_frecuentes = encontrar_palabras_frecuentes(contenido)
        promedio_longitud = calcular_promedio_longitud_palabra(contenido)
        
        tiempo = time.time() - inicio
        
        # Obtener tamaño del archivo
        tamanio_bytes = os.path.getsize(ruta_archivo)
        tamanio_kb = tamanio_bytes / 1024
        
        return {
            'archivo': os.path.basename(ruta_archivo),
            'ruta': ruta_archivo,
            'exito': True,
            'tamanio_kb': round(tamanio_kb, 2),
            'num_lineas': num_lineas,
            'num_palabras': num_palabras,
            'num_caracteres': stats_caracteres['total'],
            'num_caracteres_sin_espacios': stats_caracteres['sin_espacios'],
            'promedio_longitud_palabra': round(promedio_longitud, 2),
            'palabras_frecuentes': palabras_frecuentes[:5],  # Top 5
            'tiempo_proceso': tiempo
        }
    
    except FileNotFoundError:
        return {
            'archivo': os.path.basename(ruta_archivo),
            'ruta': ruta_archivo,
            'exito': False,
            'error': 'Archivo no encontrado',
            'tiempo_proceso': time.time() - inicio
        }
    
    except Exception as e:
        return {
            'archivo': os.path.basename(ruta_archivo),
            'ruta': ruta_archivo,
            'exito': False,
            'error': str(e),
            'tiempo_proceso': time.time() - inicio
        }


def procesar_archivos_secuencial(lista_archivos):
    """
    Procesa una lista de archivos de forma SECUENCIAL.
    Cada archivo se procesa uno después del otro.
    
    Args:
        lista_archivos: Lista de rutas de archivos a procesar
    
    Returns:
        Lista con los resultados de cada archivo
    """
    print("\n" + "="*70)
    print("📄 INICIANDO PROCESAMIENTO SECUENCIAL DE ARCHIVOS")
    print("="*70)
    print(f"📊 Archivos a procesar: {len(lista_archivos)}")
    print(f"🖥️  Modo: UN SOLO NÚCLEO (secuencial)")
    print("="*70 + "\n")
    
    inicio_total = time.time()
    resultados = []
    
    # Procesar cada archivo secuencialmente
    for i, archivo in enumerate(lista_archivos, 1):
        print(f"🔄 Procesando archivo {i}/{len(lista_archivos)}: {os.path.basename(archivo)}")
        resultado = analizar_archivo(archivo)
        resultados.append(resultado)
        
        if resultado['exito']:
            print(f"  ✅ {resultado['num_palabras']} palabras | "
                  f"{resultado['num_lineas']} líneas | "
                  f"{resultado['tamanio_kb']} KB | "
                  f"{resultado['tiempo_proceso']:.3f}s\n")
        else:
            print(f"  ❌ Error: {resultado['error']}\n")
    
    tiempo_total = time.time() - inicio_total
    
    # Mostrar resumen
    print("="*70)
    print("📈 RESUMEN DEL PROCESAMIENTO SECUENCIAL")
    print("="*70)
    
    archivos_exitosos = [r for r in resultados if r['exito']]
    
    if archivos_exitosos:
        total_palabras = sum(r['num_palabras'] for r in archivos_exitosos)
        total_lineas = sum(r['num_lineas'] for r in archivos_exitosos)
        total_caracteres = sum(r['num_caracteres'] for r in archivos_exitosos)
        
        print(f"✅ Archivos procesados exitosamente: {len(archivos_exitosos)}/{len(lista_archivos)}")
        print(f"📝 Total de palabras: {total_palabras:,}")
        print(f"📄 Total de líneas: {total_lineas:,}")
        print(f"🔤 Total de caracteres: {total_caracteres:,}")
    
    print(f"⏱️  Tiempo total: {tiempo_total:.2f} segundos")
    print(f"⚡ Promedio por archivo: {tiempo_total/len(lista_archivos):.2f} segundos")
    print("="*70 + "\n")
    
    return resultados, tiempo_total


def main():
    """
    Función principal del programa.
    """
    print("\n" + "="*70)
    print("🚀 VERSIÓN 2 - PROCESAMIENTO SECUENCIAL DE ARCHIVOS")
    print("="*70)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Buscar archivos .txt en la carpeta actual
    carpeta_datos = Path(__file__).parent / "datos_ejemplo"
    
    if not carpeta_datos.exists():
        print(f"\n⚠️  La carpeta 'datos_ejemplo' no existe.")
        print(f"📁 Creando carpeta: {carpeta_datos}")
        carpeta_datos.mkdir(exist_ok=True)
        print("ℹ️  Por favor, coloca archivos .txt en la carpeta 'datos_ejemplo' y ejecuta nuevamente.")
        return
    
    # Buscar archivos .txt
    archivos_txt = list(carpeta_datos.glob("*.txt"))
    
    if not archivos_txt:
        print(f"\n⚠️  No se encontraron archivos .txt en '{carpeta_datos}'")
        print("ℹ️  Por favor, coloca archivos .txt en la carpeta y ejecuta nuevamente.")
        return
    
    archivos_txt = [str(archivo) for archivo in archivos_txt]
    
    print(f"\n📂 Archivos encontrados: {len(archivos_txt)}")
    for archivo in archivos_txt:
        print(f"   - {os.path.basename(archivo)}")
    
    # Procesar archivos
    resultados, tiempo_total = procesar_archivos_secuencial(archivos_txt)
    
    # Mostrar detalles de cada archivo procesado
    print("\n" + "="*70)
    print("📊 DETALLES POR ARCHIVO")
    print("="*70)
    
    for resultado in resultados:
        if resultado['exito']:
            print(f"\n📄 {resultado['archivo']}")
            print(f"   - Tamaño: {resultado['tamanio_kb']} KB")
            print(f"   - Líneas: {resultado['num_lineas']:,}")
            print(f"   - Palabras: {resultado['num_palabras']:,}")
            print(f"   - Caracteres: {resultado['num_caracteres']:,}")
            print(f"   - Promedio longitud palabra: {resultado['promedio_longitud_palabra']} caracteres")
            print(f"   - Top 5 palabras frecuentes:")
            for palabra, frecuencia in resultado['palabras_frecuentes']:
                print(f"      • {palabra}: {frecuencia} veces")
            print(f"   - Tiempo: {resultado['tiempo_proceso']:.3f}s")
    
    print("\n" + "="*70)
    print("✅ PROCESAMIENTO COMPLETADO")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
