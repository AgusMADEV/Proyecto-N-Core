"""
GENERADOR DE IMÁGENES DE EJEMPLO
=================================
Este script genera imágenes de ejemplo para probar el procesamiento
paralelo de imágenes de la Versión 3.0.

Genera imágenes con diferentes patrones, colores y tamaños.

Requiere: pip install Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path
import random


def verificar_pillow():
    """Verifica que Pillow esté instalado."""
    try:
        import PIL
        return True
    except ImportError:
        print("\n❌ ERROR: La biblioteca Pillow no está instalada.")
        print("\n📦 Para instalar Pillow, ejecuta:")
        print("   pip install Pillow")
        return False


def generar_imagen_colores(ancho, alto, nombre_archivo):
    """
    Genera una imagen con bloques de colores.
    
    Args:
        ancho: Ancho de la imagen
        alto: Alto de la imagen
        nombre_archivo: Ruta donde guardar la imagen
    """
    imagen = Image.new('RGB', (ancho, alto))
    draw = ImageDraw.Draw(imagen)
    
    # Dividir en cuadrantes de colores
    colores = [
        (255, 0, 0),    # Rojo
        (0, 255, 0),    # Verde
        (0, 0, 255),    # Azul
        (255, 255, 0),  # Amarillo
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
    ]
    
    cuadrantes_x = 3
    cuadrantes_y = 2
    ancho_cuadrante = ancho // cuadrantes_x
    alto_cuadrante = alto // cuadrantes_y
    
    idx_color = 0
    for i in range(cuadrantes_y):
        for j in range(cuadrantes_x):
            x1 = j * ancho_cuadrante
            y1 = i * alto_cuadrante
            x2 = x1 + ancho_cuadrante
            y2 = y1 + alto_cuadrante
            
            draw.rectangle([x1, y1, x2, y2], fill=colores[idx_color % len(colores)])
            idx_color += 1
    
    imagen.save(nombre_archivo, 'JPEG', quality=95)
    print(f"✅ Generada: {os.path.basename(nombre_archivo)}")


def generar_imagen_gradiente(ancho, alto, nombre_archivo):
    """
    Genera una imagen con gradiente de colores.
    
    Args:
        ancho: Ancho de la imagen
        alto: Alto de la imagen
        nombre_archivo: Ruta donde guardar la imagen
    """
    imagen = Image.new('RGB', (ancho, alto))
    draw = ImageDraw.Draw(imagen)
    
    for y in range(alto):
        # Gradiente de rojo a azul
        r = int(255 * (1 - y / alto))
        b = int(255 * (y / alto))
        g = 100
        
        draw.line([(0, y), (ancho, y)], fill=(r, g, b))
    
    imagen.save(nombre_archivo, 'JPEG', quality=95)
    print(f"✅ Generada: {os.path.basename(nombre_archivo)}")


def generar_imagen_patron(ancho, alto, nombre_archivo):
    """
    Genera una imagen con patrón geométrico.
    
    Args:
        ancho: Ancho de la imagen
        alto: Alto de la imagen
        nombre_archivo: Ruta donde guardar la imagen
    """
    imagen = Image.new('RGB', (ancho, alto), color=(255, 255, 255))
    draw = ImageDraw.Draw(imagen)
    
    # Dibujar círculos en patrón
    radio = 30
    espaciado = 60
    
    for y in range(0, alto, espaciado):
        for x in range(0, ancho, espaciado):
            color = (
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255)
            )
            draw.ellipse([x-radio, y-radio, x+radio, y+radio], fill=color, outline=(0, 0, 0))
    
    imagen.save(nombre_archivo, 'JPEG', quality=95)
    print(f"✅ Generada: {os.path.basename(nombre_archivo)}")


def generar_imagen_rayas(ancho, alto, nombre_archivo):
    """
    Genera una imagen con rayas horizontales.
    
    Args:
        ancho: Ancho de la imagen
        alto: Alto de la imagen
        nombre_archivo: Ruta donde guardar la imagen
    """
    imagen = Image.new('RGB', (ancho, alto))
    draw = ImageDraw.Draw(imagen)
    
    altura_raya = 40
    colores = [
        (255, 100, 100),
        (100, 255, 100),
        (100, 100, 255),
        (255, 255, 100),
        (255, 100, 255),
        (100, 255, 255),
    ]
    
    y = 0
    idx = 0
    while y < alto:
        draw.rectangle([0, y, ancho, y + altura_raya], fill=colores[idx % len(colores)])
        y += altura_raya
        idx += 1
    
    imagen.save(nombre_archivo, 'JPEG', quality=95)
    print(f"✅ Generada: {os.path.basename(nombre_archivo)}")


def generar_imagen_texto(ancho, alto, nombre_archivo, texto):
    """
    Genera una imagen con texto.
    
    Args:
        ancho: Ancho de la imagen
        alto: Alto de la imagen
        nombre_archivo: Ruta donde guardar la imagen
        texto: Texto a dibujar
    """
    imagen = Image.new('RGB', (ancho, alto), color=(240, 240, 240))
    draw = ImageDraw.Draw(imagen)
    
    # Fondo con gradiente
    for y in range(alto):
        color_val = int(240 - (y / alto) * 80)
        draw.line([(0, y), (ancho, y)], fill=(color_val, color_val, 255))
    
    # Intentar usar una fuente, si no está disponible usar la por defecto
    try:
        # Tamaño de fuente basado en el tamaño de la imagen
        font_size = ancho // 15
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Dibujar texto centrado
    bbox = draw.textbbox((0, 0), texto, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (ancho - text_width) // 2
    y = (alto - text_height) // 2
    
    # Sombra del texto
    draw.text((x+3, y+3), texto, fill=(100, 100, 100), font=font)
    # Texto principal
    draw.text((x, y), texto, fill=(255, 255, 255), font=font)
    
    imagen.save(nombre_archivo, 'JPEG', quality=95)
    print(f"✅ Generada: {os.path.basename(nombre_archivo)}")


def generar_imagen_compleja(ancho, alto, nombre_archivo):
    """
    Genera una imagen compleja con múltiples elementos.
    
    Args:
        ancho: Ancho de la imagen
        alto: Alto de la imagen
        nombre_archivo: Ruta donde guardar la imagen
    """
    imagen = Image.new('RGB', (ancho, alto), color=(20, 20, 40))
    draw = ImageDraw.Draw(imagen)
    
    # Fondo con estrellas
    for _ in range(200):
        x = random.randint(0, ancho)
        y = random.randint(0, alto)
        brillo = random.randint(150, 255)
        draw.point((x, y), fill=(brillo, brillo, brillo))
    
    # Círculos de colores
    for _ in range(50):
        x = random.randint(0, ancho)
        y = random.randint(0, alto)
        radio = random.randint(10, 50)
        color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        draw.ellipse([x-radio, y-radio, x+radio, y+radio], fill=color)
    
    imagen.save(nombre_archivo, 'PNG')
    print(f"✅ Generada: {os.path.basename(nombre_archivo)}")


def main():
    """
    Función principal del generador.
    """
    print("\n" + "="*70)
    print("🎨 GENERADOR DE IMÁGENES DE EJEMPLO")
    print("="*70)
    
    if not verificar_pillow():
        return
    
    # Crear carpeta de imágenes
    carpeta = Path(__file__).parent / "imagenes_entrada"
    carpeta.mkdir(exist_ok=True)
    
    print(f"\n📁 Carpeta de destino: {carpeta}")
    print("\n🎨 Generando imágenes de ejemplo...\n")
    
    # Generar diferentes tipos de imágenes
    generar_imagen_colores(1200, 800, str(carpeta / "imagen1_colores.jpg"))
    generar_imagen_gradiente(1600, 1200, str(carpeta / "imagen2_gradiente.jpg"))
    generar_imagen_patron(1400, 1000, str(carpeta / "imagen3_patron.jpg"))
    generar_imagen_rayas(1800, 1200, str(carpeta / "imagen4_rayas.jpg"))
    generar_imagen_texto(1600, 900, str(carpeta / "imagen5_texto.jpg"), "PYTHON")
    generar_imagen_texto(1400, 1000, str(carpeta / "imagen6_multicore.jpg"), "MULTICORE")
    generar_imagen_compleja(2000, 1500, str(carpeta / "imagen7_compleja.png"))
    
    print("\n" + "="*70)
    print("✅ GENERACIÓN COMPLETADA")
    print("="*70)
    print(f"\n📊 Total de imágenes generadas: 7")
    print(f"📁 Ubicación: {carpeta}")
    print("\n💡 Ahora puedes ejecutar:")
    print("   python version3_secuencial.py")
    print("   python version3_paralelo.py")
    print("   python comparador_v3.py")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
