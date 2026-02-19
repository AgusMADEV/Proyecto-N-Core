"""
VERSIÓN 3 - PROCESAMIENTO SECUENCIAL DE IMÁGENES
=================================================
Este programa procesa múltiples imágenes de forma SECUENCIAL
aplicando filtros y transformaciones.

Tarea: Aplicar filtros (blur, escala de grises) y redimensionamiento
Procesa una imagen tras otra en un solo núcleo del procesador.

Requiere: pip install Pillow
"""

import time
import os
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageFilter
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
        print("\nO si usas conda:")
        print("   conda install pillow")
        return False


def aplicar_blur(imagen):
    """
    Aplica filtro de desenfoque a una imagen.
    
    Args:
        imagen: Objeto PIL Image
    
    Returns:
        Imagen con filtro blur aplicado
    """
    return imagen.filter(ImageFilter.GaussianBlur(radius=5))


def aplicar_escala_grises(imagen):
    """
    Convierte una imagen a escala de grises.
    
    Args:
        imagen: Objeto PIL Image
    
    Returns:
        Imagen en escala de grises
    """
    return imagen.convert('L')


def aplicar_blur_intenso(imagen):
    """
    Aplica filtro de desenfoque intenso.
    
    Args:
        imagen: Objeto PIL Image
    
    Returns:
        Imagen con blur intenso
    """
    return imagen.filter(ImageFilter.GaussianBlur(radius=10))


def aplicar_sharpen(imagen):
    """
    Aplica filtro de nitidez a una imagen.
    
    Args:
        imagen: Objeto PIL Image
    
    Returns:
        Imagen con filtro sharpen aplicado
    """
    return imagen.filter(ImageFilter.SHARPEN)


def aplicar_contorno(imagen):
    """
    Aplica filtro de detección de contornos.
    
    Args:
        imagen: Objeto PIL Image
    
    Returns:
        Imagen con contornos detectados
    """
    return imagen.filter(ImageFilter.FIND_EDGES)


def redimensionar(imagen, ancho, alto):
    """
    Redimensiona una imagen.
    
    Args:
        imagen: Objeto PIL Image
        ancho: Nuevo ancho
        alto: Nuevo alto
    
    Returns:
        Imagen redimensionada
    """
    return imagen.resize((ancho, alto), Image.Resampling.LANCZOS)


def procesar_imagen(ruta_entrada, ruta_salida, operaciones):
    """
    Procesa una imagen aplicando las operaciones especificadas.
    
    Args:
        ruta_entrada: Ruta de la imagen original
        ruta_salida: Ruta donde guardar la imagen procesada
        operaciones: Lista de operaciones a aplicar
    
    Returns:
        Diccionario con información del procesamiento
    """
    inicio = time.time()
    nombre_archivo = os.path.basename(ruta_entrada)
    
    try:
        # Cargar imagen
        imagen = Image.open(ruta_entrada)
        tamanio_original = imagen.size
        formato_original = imagen.format
        modo_original = imagen.mode
        
        # Aplicar operaciones
        ops_aplicadas = []
        for operacion in operaciones:
            if operacion['tipo'] == 'blur':
                imagen = aplicar_blur(imagen)
                ops_aplicadas.append('Blur')
            
            elif operacion['tipo'] == 'blur_intenso':
                imagen = aplicar_blur_intenso(imagen)
                ops_aplicadas.append('Blur Intenso')
            
            elif operacion['tipo'] == 'escala_grises':
                imagen = aplicar_escala_grises(imagen)
                ops_aplicadas.append('Escala de Grises')
            
            elif operacion['tipo'] == 'sharpen':
                imagen = aplicar_sharpen(imagen)
                ops_aplicadas.append('Sharpen')
            
            elif operacion['tipo'] == 'contorno':
                imagen = aplicar_contorno(imagen)
                ops_aplicadas.append('Detección de Contornos')
            
            elif operacion['tipo'] == 'redimensionar':
                ancho = operacion.get('ancho', 800)
                alto = operacion.get('alto', 600)
                imagen = redimensionar(imagen, ancho, alto)
                ops_aplicadas.append(f'Redimensionar {ancho}x{alto}')
        
        # Guardar imagen procesada
        imagen.save(ruta_salida, quality=95)
        
        tiempo = time.time() - inicio
        tamanio_final = imagen.size
        
        # Obtener tamaños de archivo
        tamanio_archivo_entrada = os.path.getsize(ruta_entrada) / 1024
        tamanio_archivo_salida = os.path.getsize(ruta_salida) / 1024
        
        return {
            'archivo': nombre_archivo,
            'ruta_entrada': ruta_entrada,
            'ruta_salida': ruta_salida,
            'exito': True,
            'tamanio_original': tamanio_original,
            'tamanio_final': tamanio_final,
            'formato': formato_original,
            'modo_original': modo_original,
            'operaciones_aplicadas': ops_aplicadas,
            'num_operaciones': len(ops_aplicadas),
            'tamanio_kb_entrada': round(tamanio_archivo_entrada, 2),
            'tamanio_kb_salida': round(tamanio_archivo_salida, 2),
            'tiempo_proceso': tiempo
        }
    
    except FileNotFoundError:
        return {
            'archivo': nombre_archivo,
            'ruta_entrada': ruta_entrada,
            'exito': False,
            'error': 'Archivo no encontrado',
            'tiempo_proceso': time.time() - inicio
        }
    
    except Exception as e:
        return {
            'archivo': nombre_archivo,
            'ruta_entrada': ruta_entrada,
            'exito': False,
            'error': str(e),
            'tiempo_proceso': time.time() - inicio
        }


def procesar_imagenes_secuencial(lista_imagenes, carpeta_salida, operaciones):
    """
    Procesa una lista de imágenes de forma SECUENCIAL.
    Cada imagen se procesa una después de la otra.
    
    Args:
        lista_imagenes: Lista de rutas de imágenes a procesar
        carpeta_salida: Carpeta donde guardar las imágenes procesadas
        operaciones: Lista de operaciones a aplicar a cada imagen
    
    Returns:
        Tupla (lista de resultados, tiempo total)
    """
    print("\n" + "="*70)
    print("🖼️  INICIANDO PROCESAMIENTO SECUENCIAL DE IMÁGENES")
    print("="*70)
    print(f"📊 Imágenes a procesar: {len(lista_imagenes)}")
    print(f"🖥️  Modo: UN SOLO NÚCLEO (secuencial)")
    print(f"🎨 Operaciones: {', '.join([op['tipo'] for op in operaciones])}")
    print("="*70 + "\n")
    
    inicio_total = time.time()
    resultados = []
    
    # Procesar cada imagen secuencialmente
    for i, ruta_imagen in enumerate(lista_imagenes, 1):
        nombre_archivo = os.path.basename(ruta_imagen)
        print(f"🔄 Procesando imagen {i}/{len(lista_imagenes)}: {nombre_archivo}")
        
        # Generar ruta de salida
        nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
        extension = os.path.splitext(nombre_archivo)[1]
        nombre_salida = f"{nombre_sin_ext}_procesado{extension}"
        ruta_salida = os.path.join(carpeta_salida, nombre_salida)
        
        # Procesar imagen
        resultado = procesar_imagen(ruta_imagen, ruta_salida, operaciones)
        resultados.append(resultado)
        
        if resultado['exito']:
            print(f"  ✅ {resultado['tamanio_original']} → {resultado['tamanio_final']} | "
                  f"{resultado['tamanio_kb_entrada']} KB → {resultado['tamanio_kb_salida']} KB | "
                  f"{resultado['tiempo_proceso']:.3f}s\n")
        else:
            print(f"  ❌ Error: {resultado['error']}\n")
    
    tiempo_total = time.time() - inicio_total
    
    # Mostrar resumen
    print("="*70)
    print("📈 RESUMEN DEL PROCESAMIENTO SECUENCIAL")
    print("="*70)
    
    imagenes_exitosas = [r for r in resultados if r['exito']]
    
    if imagenes_exitosas:
        print(f"✅ Imágenes procesadas exitosamente: {len(imagenes_exitosas)}/{len(lista_imagenes)}")
        total_ops = sum(r['num_operaciones'] for r in imagenes_exitosas)
        print(f"🎨 Total de operaciones aplicadas: {total_ops}")
        
        tamanio_total_entrada = sum(r['tamanio_kb_entrada'] for r in imagenes_exitosas)
        tamanio_total_salida = sum(r['tamanio_kb_salida'] for r in imagenes_exitosas)
        print(f"💾 Tamaño total entrada: {tamanio_total_entrada:.2f} KB")
        print(f"💾 Tamaño total salida: {tamanio_total_salida:.2f} KB")
    
    print(f"⏱️  Tiempo total: {tiempo_total:.2f} segundos")
    print(f"⚡ Promedio por imagen: {tiempo_total/len(lista_imagenes):.2f} segundos")
    print("="*70 + "\n")
    
    return resultados, tiempo_total


def main():
    """
    Función principal del programa.
    """
    print("\n" + "="*70)
    print("🚀 VERSIÓN 3 - PROCESAMIENTO SECUENCIAL DE IMÁGENES")
    print("="*70)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Verificar que Pillow esté instalado
    if not verificar_pillow():
        return
    
    # Definir carpetas
    carpeta_entrada = Path(__file__).parent / "imagenes_entrada"
    carpeta_salida = Path(__file__).parent / "imagenes_salida"
    
    # Crear carpetas si no existen
    if not carpeta_entrada.exists():
        print(f"\n⚠️  La carpeta 'imagenes_entrada' no existe.")
        print(f"📁 Creando carpeta: {carpeta_entrada}")
        carpeta_entrada.mkdir(exist_ok=True)
        print("ℹ️  Por favor, coloca archivos de imagen en la carpeta 'imagenes_entrada' y ejecuta nuevamente.")
        print("📸 Formatos soportados: .jpg, .jpeg, .png, .bmp, .gif")
        return
    
    carpeta_salida.mkdir(exist_ok=True)
    
    # Buscar imágenes
    extensiones = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif']
    imagenes = []
    for ext in extensiones:
        imagenes.extend(list(carpeta_entrada.glob(ext)))
        imagenes.extend(list(carpeta_entrada.glob(ext.upper())))
    
    if not imagenes:
        print(f"\n⚠️  No se encontraron imágenes en '{carpeta_entrada}'")
        print("ℹ️  Por favor, coloca archivos de imagen en la carpeta y ejecuta nuevamente.")
        print("📸 Formatos soportados: .jpg, .jpeg, .png, .bmp, .gif")
        return
    
    imagenes = [str(img) for img in imagenes]
    
    print(f"\n📂 Imágenes encontradas: {len(imagenes)}")
    for imagen in imagenes:
        tamanio_kb = os.path.getsize(imagen) / 1024
        print(f"   - {os.path.basename(imagen)} ({tamanio_kb:.2f} KB)")
    
    # Definir operaciones a aplicar
    print(f"\n🎨 Selecciona las operaciones a aplicar:")
    print("   1. Blur (desenfoque)")
    print("   2. Escala de grises")
    print("   3. Redimensionar a 800x600")
    print("   4. Sharpen (nitidez)")
    print("   5. Detección de contornos")
    print("   6. Combo: Blur + Escala de grises + Redimensionar")
    print("   7. Todas las operaciones")
    
    try:
        opcion = input("\nIngresa el número de opción (default: 6): ").strip()
        if not opcion:
            opcion = "6"
        opcion = int(opcion)
    except:
        opcion = 6
    
    # Configurar operaciones según la opción
    if opcion == 1:
        operaciones = [{'tipo': 'blur'}]
    elif opcion == 2:
        operaciones = [{'tipo': 'escala_grises'}]
    elif opcion == 3:
        operaciones = [{'tipo': 'redimensionar', 'ancho': 800, 'alto': 600}]
    elif opcion == 4:
        operaciones = [{'tipo': 'sharpen'}]
    elif opcion == 5:
        operaciones = [{'tipo': 'contorno'}]
    elif opcion == 6:
        operaciones = [
            {'tipo': 'blur'},
            {'tipo': 'escala_grises'},
            {'tipo': 'redimensionar', 'ancho': 800, 'alto': 600}
        ]
    else:  # opcion 7
        operaciones = [
            {'tipo': 'blur'},
            {'tipo': 'escala_grises'},
            {'tipo': 'sharpen'},
            {'tipo': 'redimensionar', 'ancho': 800, 'alto': 600}
        ]
    
    # Procesar imágenes
    resultados, tiempo_total = procesar_imagenes_secuencial(imagenes, str(carpeta_salida), operaciones)
    
    # Mostrar detalles
    print("\n" + "="*70)
    print("📊 DETALLES POR IMAGEN")
    print("="*70)
    
    for resultado in resultados:
        if resultado['exito']:
            print(f"\n🖼️  {resultado['archivo']}")
            print(f"   - Tamaño original: {resultado['tamanio_original']}")
            print(f"   - Tamaño final: {resultado['tamanio_final']}")
            print(f"   - Formato: {resultado['formato']}")
            print(f"   - Operaciones aplicadas: {', '.join(resultado['operaciones_aplicadas'])}")
            print(f"   - Archivo entrada: {resultado['tamanio_kb_entrada']} KB")
            print(f"   - Archivo salida: {resultado['tamanio_kb_salida']} KB")
            print(f"   - Tiempo: {resultado['tiempo_proceso']:.3f}s")
            print(f"   - Guardado en: {os.path.basename(resultado['ruta_salida'])}")
    
    print(f"\n📁 Imágenes procesadas guardadas en: {carpeta_salida}")
    print("\n" + "="*70)
    print("✅ PROCESAMIENTO COMPLETADO")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
