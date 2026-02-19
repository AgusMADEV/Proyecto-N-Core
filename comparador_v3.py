"""
COMPARADOR VERSIÓN 3 - PROCESAMIENTO DE IMÁGENES
=================================================
Este script compara el rendimiento entre el procesamiento SECUENCIAL
y PARALELO de imágenes con filtros y transformaciones.

Permite visualizar claramente las ventajas del multinúcleo en procesamiento de imágenes.
"""

import time
import multiprocessing
from datetime import datetime
from pathlib import Path
import os
import sys


def verificar_pillow():
    """
    Verifica que Pillow esté instalado.
    """
    try:
        import PIL
        return True
    except ImportError:
        print("\n❌ ERROR: La biblioteca Pillow no está instalada.")
        print("\n📦 Para instalar Pillow, ejecuta:")
        print("   pip install Pillow")
        return False


# Importar funciones de ambas versiones
try:
    from version3_secuencial import procesar_imagen as procesar_secuencial
    from version3_paralelo import procesar_imagen_wrapper, procesar_imagen as procesar_paralelo
except ImportError as e:
    print(f"\n❌ Error al importar módulos: {e}")
    print("Asegúrate de que version3_secuencial.py y version3_paralelo.py estén en la misma carpeta.")
    sys.exit(1)


def ejecutar_prueba_secuencial(imagenes, carpeta_salida_sec, operaciones):
    """
    Ejecuta el procesamiento secuencial de imágenes.
    
    Args:
        imagenes: Lista de rutas de imágenes
        carpeta_salida_sec: Carpeta donde guardar resultados secuenciales
        operaciones: Lista de operaciones a aplicar
    
    Returns:
        Tupla (resultados, tiempo_total)
    """
    print("\n" + "="*70)
    print("🐌 EJECUTANDO VERSIÓN SECUENCIAL")
    print("="*70)
    print(f"📊 Imágenes: {len(imagenes)}")
    print(f"🖥️  Modo: UN SOLO NÚCLEO")
    print(f"🎨 Operaciones: {', '.join([op['tipo'] for op in operaciones])}")
    print("="*70 + "\n")
    
    inicio = time.time()
    resultados = []
    
    for i, ruta_imagen in enumerate(imagenes, 1):
        nombre_archivo = os.path.basename(ruta_imagen)
        print(f"🔄 Procesando {i}/{len(imagenes)}: {nombre_archivo}")
        
        # Generar ruta de salida
        nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
        extension = os.path.splitext(nombre_archivo)[1]
        nombre_salida = f"{nombre_sin_ext}_sec{extension}"
        ruta_salida = os.path.join(carpeta_salida_sec, nombre_salida)
        
        resultado = procesar_secuencial(ruta_imagen, ruta_salida, operaciones)
        resultados.append(resultado)
        
        if resultado['exito']:
            print(f"  ✅ {resultado['tamanio_original']} → {resultado['tamanio_final']} | "
                  f"{resultado['tiempo_proceso']:.3f}s\n")
    
    tiempo_total = time.time() - inicio
    
    return resultados, tiempo_total


def ejecutar_prueba_paralelo(imagenes, carpeta_salida_par, operaciones, num_procesos=None):
    """
    Ejecuta el procesamiento paralelo de imágenes.
    
    Args:
        imagenes: Lista de rutas de imágenes
        carpeta_salida_par: Carpeta donde guardar resultados paralelos
        operaciones: Lista de operaciones a aplicar
        num_procesos: Número de procesos (None = todos los núcleos)
    
    Returns:
        Tupla (resultados, tiempo_total)
    """
    if num_procesos is None:
        num_procesos = multiprocessing.cpu_count()
    
    print("\n" + "="*70)
    print("🚀 EJECUTANDO VERSIÓN PARALELA")
    print("="*70)
    print(f"📊 Imágenes: {len(imagenes)}")
    print(f"🖥️  Núcleos disponibles: {multiprocessing.cpu_count()}")
    print(f"⚙️  Procesos a usar: {num_procesos}")
    print(f"🎨 Operaciones: {', '.join([op['tipo'] for op in operaciones])}")
    print("="*70 + "\n")
    
    inicio = time.time()
    
    # Preparar argumentos
    tareas = []
    for ruta_imagen in imagenes:
        nombre_archivo = os.path.basename(ruta_imagen)
        nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
        extension = os.path.splitext(nombre_archivo)[1]
        nombre_salida = f"{nombre_sin_ext}_par{extension}"
        ruta_salida = os.path.join(carpeta_salida_par, nombre_salida)
        
        tareas.append((ruta_imagen, ruta_salida, operaciones))
    
    # Procesar en paralelo
    with multiprocessing.Pool(processes=num_procesos) as pool:
        resultados = pool.map(procesar_imagen_wrapper, tareas)
    
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


def mostrar_comparacion(tiempo_sec, tiempo_par, metricas, imagenes_sec, imagenes_par):
    """
    Muestra una comparación visual de los resultados.
    """
    print("\n" + "="*70)
    print("📊 COMPARACIÓN DE RENDIMIENTO")
    print("="*70)
    
    # Información de imágenes procesadas
    exitos_sec = sum(1 for r in imagenes_sec if r['exito'])
    exitos_par = sum(1 for r in imagenes_par if r['exito'])
    
    print(f"\n✅ Imágenes procesadas correctamente:")
    print(f"   Secuencial: {exitos_sec}/{len(imagenes_sec)}")
    print(f"   Paralelo:   {exitos_par}/{len(imagenes_par)}")
    
    # Estadísticas totales
    if exitos_sec > 0:
        total_ops_sec = sum(r['num_operaciones'] for r in imagenes_sec if r['exito'])
        total_kb_entrada = sum(r['tamanio_kb_entrada'] for r in imagenes_sec if r['exito'])
        total_kb_salida_sec = sum(r['tamanio_kb_salida'] for r in imagenes_sec if r['exito'])
        
        print(f"\n🎨 Total de operaciones realizadas: {total_ops_sec}")
        print(f"💾 Total de datos procesados: {total_kb_entrada:.2f} KB")
        print(f"💾 Total de datos generados: {total_kb_salida_sec:.2f} KB")
    
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
    max_tiempo = max(tiempo_sec, tiempo_par)
    escala = 40 / max_tiempo  # 40 caracteres máximo
    
    barra_sec = "█" * int(tiempo_sec * escala)
    barra_par = "█" * int(tiempo_par * escala)
    
    print(f"   Secuencial: {barra_sec} {tiempo_sec:.2f}s")
    print(f"   Paralelo:   {barra_par} {tiempo_par:.2f}s")
    
    # Interpretación
    print(f"\n💡 INTERPRETACIÓN:")
    if metricas['speedup'] >= 4:
        print(f"   ✨ ¡Excelente mejora de rendimiento! El procesamiento paralelo brilla.")
    elif metricas['speedup'] >= 2.5:
        print(f"   👍 Muy buena mejora de rendimiento")
    elif metricas['speedup'] >= 1.5:
        print(f"   ✓ Mejora moderada de rendimiento")
    else:
        print(f"   ⚠️  Mejora limitada (posible overhead o imágenes muy pequeñas)")
    
    print(f"\n📝 NOTA:")
    print(f"   El procesamiento de imágenes es CPU-intensivo, por lo que")
    print(f"   el paralelismo suele ofrecer ganancias significativas.")
    print("="*70 + "\n")


def main():
    """
    Función principal del comparador.
    """
    print("\n" + "="*70)
    print("🔬 COMPARADOR DE RENDIMIENTO - PROCESAMIENTO DE IMÁGENES")
    print("="*70)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🖥️  Sistema: {multiprocessing.cpu_count()} núcleos detectados")
    print("="*70)
    
    # Verificar Pillow
    if not verificar_pillow():
        return
    
    # Buscar imágenes
    carpeta_entrada = Path(__file__).parent / "imagenes_entrada"
    
    if not carpeta_entrada.exists():
        print(f"\n❌ Error: La carpeta 'imagenes_entrada' no existe.")
        print("Por favor, ejecuta primero version3_secuencial.py o version3_paralelo.py")
        return
    
    # Buscar imágenes
    extensiones = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif']
    imagenes = []
    for ext in extensiones:
        imagenes.extend(list(carpeta_entrada.glob(ext)))
        imagenes.extend(list(carpeta_entrada.glob(ext.upper())))
    
    if not imagenes:
        print(f"\n❌ Error: No se encontraron imágenes en '{carpeta_entrada}'")
        print("📸 Formatos soportados: .jpg, .jpeg, .png, .bmp, .gif")
        return
    
    imagenes = [str(img) for img in imagenes]
    
    print(f"\n📂 Imágenes encontradas: {len(imagenes)}")
    for imagen in imagenes:
        tamanio_kb = os.path.getsize(imagen) / 1024
        print(f"   - {os.path.basename(imagen)} ({tamanio_kb:.2f} KB)")
    
    # Crear carpetas de salida para comparación
    carpeta_salida_sec = Path(__file__).parent / "imagenes_salida_comparacion" / "secuencial"
    carpeta_salida_par = Path(__file__).parent / "imagenes_salida_comparacion" / "paralelo"
    
    carpeta_salida_sec.mkdir(parents=True, exist_ok=True)
    carpeta_salida_par.mkdir(parents=True, exist_ok=True)
    
    # Definir operaciones (combo estándar)
    operaciones = [
        {'tipo': 'blur'},
        {'tipo': 'escala_grises'},
        {'tipo': 'redimensionar', 'ancho': 800, 'alto': 600}
    ]
    
    print(f"\n🎨 Operaciones a aplicar: {', '.join([op['tipo'] for op in operaciones])}")
    
    # Ejecutar pruebas
    print("\n" + "="*70)
    print("🏃 INICIANDO PRUEBAS COMPARATIVAS")
    print("="*70)
    
    # Prueba secuencial
    resultados_sec, tiempo_sec = ejecutar_prueba_secuencial(
        imagenes, str(carpeta_salida_sec), operaciones
    )
    
    # Pequeña pausa entre pruebas
    time.sleep(1)
    
    # Prueba paralela
    num_procesos = multiprocessing.cpu_count()
    resultados_par, tiempo_par = ejecutar_prueba_paralelo(
        imagenes, str(carpeta_salida_par), operaciones, num_procesos
    )
    
    # Calcular métricas
    metricas = calcular_metricas(tiempo_sec, tiempo_par, num_procesos)
    
    # Mostrar comparación
    mostrar_comparacion(tiempo_sec, tiempo_par, metricas, resultados_sec, resultados_par)
    
    # Información de salida
    print(f"📁 Resultados guardados en:")
    print(f"   Secuencial: {carpeta_salida_sec}")
    print(f"   Paralelo:   {carpeta_salida_par}")
    
    print("\n" + "="*70)
    print("✅ COMPARACIÓN COMPLETADA")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
