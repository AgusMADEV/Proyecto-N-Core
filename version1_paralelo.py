"""
VERSIÓN 2 - PROCESAMIENTO PARALELO (MULTINÚCLEO)
=================================================
Este programa procesa una lista de números de forma PARALELA,
distribuyendo el trabajo entre TODOS los núcleos disponibles del procesador.

Tarea: Calcular si un número es primo y encontrar sus divisores
Ahora usando multiprocessing para aprovechar el multinúcleo.
"""

import time
import multiprocessing
from datetime import datetime


def es_primo(n):
    """
    Verifica si un número es primo.
    Usa un algoritmo simple pero costoso para simular trabajo intensivo.
    
    Args:
        n: Número a verificar
    
    Returns:
        True si es primo, False si no lo es
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Verificamos divisores impares hasta la raíz cuadrada
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def encontrar_divisores(n):
    """
    Encuentra todos los divisores de un número.
    
    Args:
        n: Número a procesar
    
    Returns:
        Lista de divisores
    """
    divisores = []
    for i in range(1, n + 1):
        if n % i == 0:
            divisores.append(i)
    return divisores


def procesar_numero(n):
    """
    Procesa un número: verifica si es primo y encuentra sus divisores.
    Esta función será ejecutada en PARALELO por diferentes procesos.
    
    Args:
        n: Número a procesar
    
    Returns:
        Diccionario con los resultados del procesamiento
    """
    inicio = time.time()
    proceso_id = multiprocessing.current_process().name
    
    print(f"  🔄 [{proceso_id}] Procesando: {n}")
    
    primo = es_primo(n)
    divisores = encontrar_divisores(n)
    
    tiempo = time.time() - inicio
    
    # Mostrar resultado inmediatamente
    estado = "✅ PRIMO" if primo else "❌ No primo"
    print(f"  ✓ [{proceso_id}] {n}: {estado} | {len(divisores)} divisores | {tiempo:.3f}s")
    
    return {
        'numero': n,
        'es_primo': primo,
        'cantidad_divisores': len(divisores),
        'divisores': divisores[:10],  # Solo mostramos los primeros 10
        'tiempo_proceso': tiempo,
        'proceso': proceso_id
    }


def procesar_lista_paralelo(numeros):
    """
    Procesa una lista de números de forma PARALELA.
    Distribuye los números entre todos los núcleos disponibles.
    
    Args:
        numeros: Lista de números a procesar
    
    Returns:
        Tupla (resultados, tiempo_total)
    """
    num_nucleos = multiprocessing.cpu_count()
    
    print("\n" + "="*60)
    print("🚀 INICIANDO PROCESAMIENTO PARALELO (MULTINÚCLEO)")
    print("="*60)
    print(f"📊 Números a procesar: {len(numeros)}")
    print(f"🖥️  Núcleos disponibles: {num_nucleos}")
    print(f"⚡ Modo: PROCESAMIENTO PARALELO")
    print("="*60 + "\n")
    
    tiempo_inicio = time.time()
    
    # Crear pool de procesos (uno por cada núcleo)
    with multiprocessing.Pool(processes=num_nucleos) as pool:
        # map() distribuye automáticamente el trabajo entre los procesos
        # Cada número será procesado por un proceso diferente en paralelo
        resultados = pool.map(procesar_numero, numeros)
    
    tiempo_total = time.time() - tiempo_inicio
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN DEL PROCESAMIENTO PARALELO")
    print("="*60)
    print(f"⏱️  Tiempo total: {tiempo_total:.2f} segundos")
    print(f"📈 Promedio por número: {tiempo_total/len(numeros):.3f} segundos")
    print(f"🔢 Números procesados: {len(resultados)}")
    primos = sum(1 for r in resultados if r['es_primo'])
    print(f"✨ Números primos encontrados: {primos}")
    print(f"🖥️  Núcleos utilizados: {num_nucleos}")
    print("="*60 + "\n")
    
    return resultados, tiempo_total


def main():
    """
    Función principal del programa
    """
    # Lista de números a procesar (números grandes para hacer el proceso más lento)
    numeros = [
        15485863,  # Primo
        15485867,  # No primo
        15485917,  # No primo
        15485923,  # Primo
        15485933,  # Primo
        15485941,  # No primo
        15485951,  # No primo
        15485959,  # Primo
    ]
    
    print("\n" + "🎯"*30)
    print("  PROYECTO: PROCESAMIENTO MULTINÚCLEO - VERSIÓN PARALELA")
    print("🎯"*30)
    print(f"\n📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Procesar en paralelo
    resultados, tiempo = procesar_lista_paralelo(numeros)
    
    print("✅ Programa finalizado correctamente")
    print(f"💡 TIP: Ejecuta version1_secuencial.py para comparar el rendimiento\n")


if __name__ == "__main__":
    # Necesario en Windows para multiprocessing
    multiprocessing.freeze_support()
    main()
