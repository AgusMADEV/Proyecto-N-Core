"""
COMPARADOR DE RENDIMIENTO
=========================
Este script ejecuta ambas versiones (secuencial y paralela) 
y compara los resultados para mostrar claramente la mejora de rendimiento.
"""

import time
import multiprocessing
from datetime import datetime


# ==================== FUNCIONES COMPARTIDAS ====================

def es_primo(n):
    """Verifica si un número es primo"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def encontrar_divisores(n):
    """Encuentra todos los divisores de un número"""
    divisores = []
    for i in range(1, n + 1):
        if n % i == 0:
            divisores.append(i)
    return divisores


def procesar_numero_simple(n):
    """Versión simplificada para procesamiento (sin prints)"""
    primo = es_primo(n)
    divisores = encontrar_divisores(n)
    return {
        'numero': n,
        'es_primo': primo,
        'cantidad_divisores': len(divisores)
    }


# ==================== VERSIÓN SECUENCIAL ====================

def procesar_secuencial(numeros):
    """Procesa números de forma secuencial"""
    resultados = []
    for numero in numeros:
        resultado = procesar_numero_simple(numero)
        resultados.append(resultado)
    return resultados


# ==================== VERSIÓN PARALELA ====================

def procesar_paralelo(numeros):
    """Procesa números en paralelo usando multiprocessing"""
    num_nucleos = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=num_nucleos) as pool:
        resultados = pool.map(procesar_numero_simple, numeros)
    return resultados


# ==================== COMPARACIÓN ====================

def comparar_rendimiento(numeros):
    """
    Ejecuta ambas versiones y compara los resultados
    
    Args:
        numeros: Lista de números a procesar
    """
    num_nucleos = multiprocessing.cpu_count()
    
    print("\n" + "🎯"*30)
    print("     COMPARADOR DE RENDIMIENTO - MULTINÚCLEO vs SECUENCIAL")
    print("🎯"*30)
    print(f"\n📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🖥️  Núcleos disponibles en tu procesador: {num_nucleos}")
    print(f"📊 Números a procesar: {len(numeros)}")
    print(f"🔢 Números: {numeros}")
    
    # ==================== PRUEBA 1: SECUENCIAL ====================
    print("\n" + "="*60)
    print("🐌 PRUEBA 1: PROCESAMIENTO SECUENCIAL")
    print("="*60)
    print("⏳ Procesando...")
    
    tiempo_inicio_sec = time.time()
    resultados_sec = procesar_secuencial(numeros)
    tiempo_sec = time.time() - tiempo_inicio_sec
    
    print(f"✅ Completado en {tiempo_sec:.2f} segundos")
    primos_sec = sum(1 for r in resultados_sec if r['es_primo'])
    print(f"✨ Números primos encontrados: {primos_sec}")
    
    # ==================== PRUEBA 2: PARALELO ====================
    print("\n" + "="*60)
    print("🚀 PRUEBA 2: PROCESAMIENTO PARALELO (MULTINÚCLEO)")
    print("="*60)
    print("⏳ Procesando...")
    
    tiempo_inicio_par = time.time()
    resultados_par = procesar_paralelo(numeros)
    tiempo_par = time.time() - tiempo_inicio_par
    
    print(f"✅ Completado en {tiempo_par:.2f} segundos")
    primos_par = sum(1 for r in resultados_par if r['es_primo'])
    print(f"✨ Números primos encontrados: {primos_par}")
    
    # ==================== COMPARACIÓN Y ANÁLISIS ====================
    print("\n" + "="*60)
    print("📊 ANÁLISIS COMPARATIVO")
    print("="*60)
    
    print(f"\n⏱️  TIEMPOS DE EJECUCIÓN:")
    print(f"   • Secuencial:  {tiempo_sec:.2f} segundos")
    print(f"   • Paralelo:    {tiempo_par:.2f} segundos")
    
    if tiempo_sec > tiempo_par:
        mejora = ((tiempo_sec - tiempo_par) / tiempo_sec) * 100
        aceleracion = tiempo_sec / tiempo_par
        print(f"\n🎉 MEJORA DE RENDIMIENTO:")
        print(f"   • Reducción de tiempo: {mejora:.1f}%")
        print(f"   • Aceleración: {aceleracion:.2f}x más rápido")
        print(f"   • Tiempo ahorrado: {tiempo_sec - tiempo_par:.2f} segundos")
    else:
        print(f"\n⚠️  El procesamiento paralelo fue más lento")
        print(f"   Esto puede ocurrir con pocas tareas o números pequeños")
        print(f"   El overhead de crear procesos supera el beneficio")
    
    print(f"\n🖥️  USO DEL PROCESADOR:")
    print(f"   • Núcleos disponibles: {num_nucleos}")
    print(f"   • Núcleos usados (secuencial): 1")
    print(f"   • Núcleos usados (paralelo): {num_nucleos}")
    print(f"   • Aprovechamiento: {num_nucleos}x más CPU")
    
    print(f"\n📈 EFICIENCIA:")
    eficiencia = (aceleracion / num_nucleos) * 100 if tiempo_sec > tiempo_par else 0
    print(f"   • Eficiencia teórica máxima: {num_nucleos}x")
    print(f"   • Eficiencia real: {aceleracion:.2f}x")
    print(f"   • Porcentaje de eficiencia: {eficiencia:.1f}%")
    print(f"   • Overhead del paralelismo: {100 - eficiencia:.1f}%")
    
    print("\n" + "="*60)
    print("💡 CONCLUSIONES")
    print("="*60)
    if mejora > 30:
        print("✅ El procesamiento paralelo es SIGNIFICATIVAMENTE más rápido")
        print("✅ Ideal para procesar grandes cantidades de datos")
        print("✅ Aprovecha eficientemente los múltiples núcleos")
    elif mejora > 10:
        print("✔️  El procesamiento paralelo es más rápido")
        print("✔️  Hay margen de mejora en la eficiencia")
    else:
        print("⚠️  El beneficio del paralelismo es limitado")
        print("💡 Considera aumentar el tamaño del problema")
        print("💡 El overhead de crear procesos afecta el rendimiento")
    
    print("\n" + "="*60 + "\n")


def main():
    """Función principal"""
    
    # Lista de números a procesar
    # Números grandes para que el procesamiento sea más intensivo
    numeros = [
        15485863,  # Primo grande
        15485867,  # No primo
        15485917,  # No primo
        15485923,  # Primo
        15485933,  # Primo
        15485941,  # No primo
        15485951,  # No primo
        15485959,  # Primo
    ]
    
    comparar_rendimiento(numeros)
    
    print("✅ Comparación finalizada\n")
    print("💡 TIPS:")
    print("   • Añade más números para ver mayor diferencia de rendimiento")
    print("   • Usa números más grandes para procesos más intensivos")
    print("   • La mejora es proporcional al número de núcleos disponibles")
    print()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
