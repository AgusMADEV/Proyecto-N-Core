"""
VERSIÓN 1 - PROCESAMIENTO SECUENCIAL
=====================================
Este programa procesa una lista de números de forma SECUENCIAL,
es decir, uno tras otro en un solo núcleo del procesador.

Tarea: Calcular si un número es primo y encontrar sus divisores
Esta operación es intensiva en CPU, ideal para demostrar el beneficio del multinúcleo.
"""

import time
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
    
    Args:
        n: Número a procesar
    
    Returns:
        Diccionario con los resultados del procesamiento
    """
    inicio = time.time()
    
    primo = es_primo(n)
    divisores = encontrar_divisores(n)
    
    tiempo = time.time() - inicio
    
    return {
        'numero': n,
        'es_primo': primo,
        'cantidad_divisores': len(divisores),
        'divisores': divisores[:10],  # Solo mostramos los primeros 10
        'tiempo_proceso': tiempo
    }


def procesar_lista_secuencial(numeros):
    """
    Procesa una lista de números de forma SECUENCIAL.
    Cada número se procesa uno después del otro.
    
    Args:
        numeros: Lista de números a procesar
    
    Returns:
        Lista con los resultados de cada número
    """
    print("\n" + "="*60)
    print("🐌 INICIANDO PROCESAMIENTO SECUENCIAL")
    print("="*60)
    print(f"📊 Números a procesar: {len(numeros)}")
    print(f"🖥️  Modo: UN SOLO NÚCLEO (secuencial)")
    print("="*60 + "\n")
    
    resultados = []
    tiempo_inicio = time.time()
    
    for i, numero in enumerate(numeros, 1):
        print(f"⏳ Procesando {i}/{len(numeros)}: {numero}...", end=" ")
        resultado = procesar_numero(numero)
        resultados.append(resultado)
        
        # Mostrar resultado
        estado = "✅ PRIMO" if resultado['es_primo'] else "❌ No primo"
        print(f"{estado} | {len(resultado['divisores'])} divisores | {resultado['tiempo_proceso']:.3f}s")
    
    tiempo_total = time.time() - tiempo_inicio
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN DEL PROCESAMIENTO")
    print("="*60)
    print(f"⏱️  Tiempo total: {tiempo_total:.2f} segundos")
    print(f"📈 Promedio por número: {tiempo_total/len(numeros):.3f} segundos")
    print(f"🔢 Números procesados: {len(resultados)}")
    primos = sum(1 for r in resultados if r['es_primo'])
    print(f"✨ Números primos encontrados: {primos}")
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
    print("  PROYECTO: PROCESAMIENTO MULTINÚCLEO - VERSIÓN SECUENCIAL")
    print("🎯"*30)
    print(f"\n📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Procesar de forma secuencial
    resultados, tiempo = procesar_lista_secuencial(numeros)
    
    print("✅ Programa finalizado correctamente\n")


if __name__ == "__main__":
    main()
