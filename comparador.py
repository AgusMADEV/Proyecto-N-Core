"""
COMPARADOR VERSIÓN 2 - PROCESAMIENTO DE ARCHIVOS
================================================
Este script compara el rendimiento entre el procesamiento SECUENCIAL
y PARALELO de archivos de texto.

Permite visualizar claramente las ventajas del multinúcleo.
"""

import time
import multiprocessing
from datetime import datetime
from pathlib import Path
import os


# Importar funciones de ambas versiones
from secuencial import analizar_archivo as analizar_secuencial
from paralelo import analizar_archivo as analizar_paralelo


def ejecutar_prueba_secuencial(archivos):
    """
    Ejecuta el procesamiento secuencial de archivos.
    
    Args:
        archivos: Lista de rutas de archivos
    
    Returns:
        Tupla (resultados, tiempo_total)
    """
    print("\n" + "="*70)
    print("🐌 EJECUTANDO VERSIÓN SECUENCIAL")
    print("="*70)
    print(f"📊 Archivos: {len(archivos)}")
    print(f"🖥️  Modo: UN SOLO NÚCLEO")
    print("="*70 + "\n")
    
    inicio = time.time()
    resultados = []
    
    for i, archivo in enumerate(archivos, 1):
        print(f"🔄 Procesando {i}/{len(archivos)}: {os.path.basename(archivo)}")
        resultado = analizar_secuencial(archivo)
        resultados.append(resultado)
        
        if resultado['exito']:
            print(f"  ✅ {resultado['num_palabras']} palabras | "
                  f"{resultado['num_lineas']} líneas | {resultado['tiempo_proceso']:.3f}s\n")
    
    tiempo_total = time.time() - inicio
    
    return resultados, tiempo_total


def ejecutar_prueba_paralelo(archivos, num_procesos=None):
    """
    Ejecuta el procesamiento paralelo de archivos.
    
    Args:
        archivos: Lista de rutas de archivos
        num_procesos: Número de procesos (None = todos los núcleos)
    
    Returns:
        Tupla (resultados, tiempo_total)
    """
    if num_procesos is None:
        num_procesos = multiprocessing.cpu_count()
    
    print("\n" + "="*70)
    print("🚀 EJECUTANDO VERSIÓN PARALELA")
    print("="*70)
    print(f"📊 Archivos: {len(archivos)}")
    print(f"🖥️  Núcleos disponibles: {multiprocessing.cpu_count()}")
    print(f"⚙️  Procesos a usar: {num_procesos}")
    print("="*70 + "\n")
    
    inicio = time.time()
    
    with multiprocessing.Pool(processes=num_procesos) as pool:
        resultados = pool.map(analizar_paralelo, archivos)
    
    tiempo_total = time.time() - inicio
    
    return resultados, tiempo_total


def calcular_metricas(tiempo_secuencial, tiempo_paralelo, num_procesos):
    """
    Calcula métricas de rendimiento comparativo.
    
    Args:
        tiempo_secuencial: Tiempo de ejecución secuencial
        tiempo_paralelo: Tiempo de ejecución paralela
        num_procesos: Número de procesos utilizados
    
    Returns:
        Diccionario con las métricas
    """
    speedup = tiempo_secuencial / tiempo_paralelo
    eficiencia = (speedup / num_procesos) * 100
    reduccion_tiempo = ((tiempo_secuencial - tiempo_paralelo) / tiempo_secuencial) * 100
    
    return {
        'speedup': speedup,
        'eficiencia': eficiencia,
        'reduccion_tiempo': reduccion_tiempo
    }


def mostrar_comparacion(tiempo_sec, tiempo_par, metricas, archivos_sec, archivos_par):
    """
    Muestra una comparación visual de los resultados.
    """
    print("\n" + "="*70)
    print("📊 COMPARACIÓN DE RENDIMIENTO")
    print("="*70)
    
    # Información de archivos procesados
    exitos_sec = sum(1 for r in archivos_sec if r['exito'])
    exitos_par = sum(1 for r in archivos_par if r['exito'])
    
    print(f"\n✅ Archivos procesados correctamente:")
    print(f"   Secuencial: {exitos_sec}/{len(archivos_sec)}")
    print(f"   Paralelo:   {exitos_par}/{len(archivos_par)}")
    
    # Estadísticas totales
    if exitos_sec > 0:
        total_palabras_sec = sum(r['num_palabras'] for r in archivos_sec if r['exito'])
        total_lineas_sec = sum(r['num_lineas'] for r in archivos_sec if r['exito'])
        
        print(f"\n📝 Total de palabras procesadas: {total_palabras_sec:,}")
        print(f"📄 Total de líneas procesadas: {total_lineas_sec:,}")
    
    # Tiempos
    print(f"\n⏱️  TIEMPOS DE EJECUCIÓN:")
    print(f"   Secuencial:  {tiempo_sec:.2f} segundos")
    print(f"   Paralelo:    {tiempo_par:.2f} segundos")
    
    # Métricas
    print(f"\n🚀 MÉTRICAS DE RENDIMIENTO:")
    print(f"   Speedup:     {metricas['speedup']:.2f}x más rápido")
    print(f"   Eficiencia:  {metricas['eficiencia']:.1f}%")
    print(f"   Reducción:   {metricas['reduccion_tiempo']:.1f}% menos tiempo")
    
    # Visualización
    print(f"\n📈 VISUALIZACIÓN:")
    barra_sec = "█" * int(tiempo_sec * 2)
    barra_par = "█" * int(tiempo_par * 2)
    
    print(f"   Secuencial: {barra_sec} {tiempo_sec:.2f}s")
    print(f"   Paralelo:   {barra_par} {tiempo_par:.2f}s")
    
    # Interpretación
    print(f"\n💡 INTERPRETACIÓN:")
    if metricas['speedup'] >= 3:
        print(f"   ✨ Excelente mejora de rendimiento!")
    elif metricas['speedup'] >= 2:
        print(f"   👍 Buena mejora de rendimiento")
    elif metricas['speedup'] >= 1.5:
        print(f"   ✓ Mejora moderada de rendimiento")
    else:
        print(f"   ⚠️  Mejora limitada (posible overhead o archivos pequeños)")
    
    print("="*70 + "\n")


def main():
    """
    Función principal del comparador.
    """
    print("\n" + "="*70)
    print("🔬 COMPARADOR DE RENDIMIENTO - PROCESAMIENTO DE ARCHIVOS")
    print("="*70)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🖥️  Sistema: {multiprocessing.cpu_count()} núcleos detectados")
    print("="*70)
    
    # Buscar archivos
    carpeta_datos = Path(__file__).parent / "datos_ejemplo"
    
    if not carpeta_datos.exists():
        print(f"\n❌ Error: La carpeta 'datos_ejemplo' no existe.")
        print("Por favor, ejecuta primero secuencial.py o paralelo.py")
        return
    
    archivos_txt = list(carpeta_datos.glob("*.txt"))
    
    if not archivos_txt:
        print(f"\n❌ Error: No se encontraron archivos .txt en '{carpeta_datos}'")
        return
    
    archivos_txt = [str(archivo) for archivo in archivos_txt]
    
    print(f"\n📂 Archivos encontrados: {len(archivos_txt)}")
    for archivo in archivos_txt:
        tamanio_kb = os.path.getsize(archivo) / 1024
        print(f"   - {os.path.basename(archivo)} ({tamanio_kb:.2f} KB)")
    
    # Ejecutar pruebas
    print("\n" + "="*70)
    print("🏃 INICIANDO PRUEBAS COMPARATIVAS")
    print("="*70)
    
    # Prueba secuencial
    resultados_sec, tiempo_sec = ejecutar_prueba_secuencial(archivos_txt)
    
    # Pequeña pausa entre pruebas
    time.sleep(1)
    
    # Prueba paralela
    num_procesos = multiprocessing.cpu_count()
    resultados_par, tiempo_par = ejecutar_prueba_paralelo(archivos_txt, num_procesos)
    
    # Calcular métricas
    metricas = calcular_metricas(tiempo_sec, tiempo_par, num_procesos)
    
    # Mostrar comparación
    mostrar_comparacion(tiempo_sec, tiempo_par, metricas, resultados_sec, resultados_par)
    
    # Guardar resultados
    print("💾 Los resultados se han mostrado en consola")
    print("\n" + "="*70)
    print("✅ COMPARACIÓN COMPLETADA")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
