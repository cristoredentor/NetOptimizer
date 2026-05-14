import time
import random
import math
from KD_tree import kd_tree, nodoKd

def generar_puntos(cantidad, dimensiones, rango=100):
    """Genera puntos aleatorios en un espacio de dimensiones"""
    puntos = []
    for _ in range(cantidad):
        punto = tuple(random.randint(0, rango) for _ in range(dimensiones))
        puntos.append(punto)
    return puntos

def busqueda_lineal(puntos, punto_busqueda, dimensiones):
    """Búsqueda lineal bruta para comparación"""
    mejorp = None
    mejord = float('inf')
    
    for p in puntos:
        d = sum((p[i] - punto_busqueda[i])**2 for i in range(dimensiones))
        if d < mejord:
            mejord = d
            mejorp = p
    
    return mejorp, mejord

def distancia_euclidiana(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos"""
    return math.sqrt(sum((p1[i] - p2[i])**2 for i in range(len(p1))))

def experimento_basico():
    """Experimento básico: búsqueda de vecino más cercano"""
    print("=" * 60)
    print("EXPERIMENTO 1: Búsqueda Básica de Vecino Más Cercano")
    print("=" * 60)
    
    # Crear puntos en 2D
    dimensiones = 2
    cantidad_puntos = 20
    puntos = generar_puntos(cantidad_puntos, dimensiones, rango=100)
    
    print(f"\nPuntos generados ({cantidad_puntos} puntos en {dimensiones}D):")
    for i, p in enumerate(puntos[:10]):
        print(f"  P{i}: {p}")
    if len(puntos) > 10:
        print(f"  ... y {len(puntos) - 10} puntos más")
    
    # Construir k-d tree
    arbol = kd_tree(dimensiones)
    arbol.creaArbol(puntos)
    print(f"\nÁrbol KD-tree creado con {arbol.elementos} elementos")
    
    # Realizar búsquedas
    punto_busqueda = (50, 50)
    print(f"\nBuscando vecino más cercano a: {punto_busqueda}")
    
    mejorp, mejord = arbol.busca(arbol.raiz, punto_busqueda, 0, None, 0)
    distancia = distancia_euclidiana(mejorp, punto_busqueda)
    
    print(f"Punto más cercano encontrado: {mejorp}")
    print(f"Distancia al cuadrado: {mejord:.2f}")
    print(f"Distancia euclidiana: {distancia:.2f}")

def experimento_comparativo():
    """Experimento: comparación de rendimiento KD-tree vs búsqueda lineal"""
    print("\n" + "=" * 60)
    print("EXPERIMENTO 2: Comparación de Rendimiento")
    print("=" * 60)
    
    dimensiones = 3
    tamaños = [100, 500, 1000, 5000]
    
    print(f"\nDimensión: {dimensiones}D")
    print(f"{'Cantidad':<10} {'KD-tree (ms)':<15} {'Búsqueda Lineal (ms)':<20} {'Mejora':<10}")
    print("-" * 60)
    
    for cantidad in tamaños:
        puntos = generar_puntos(cantidad, dimensiones, rango=1000)
        punto_busqueda = tuple(random.randint(0, 1000) for _ in range(dimensiones))
        
        # Medir KD-tree
        arbol = kd_tree(dimensiones)
        arbol.creaArbol(puntos)
        
        inicio = time.time()
        for _ in range(100):  # 100 búsquedas
            arbol.busca(arbol.raiz, punto_busqueda, 0, None, 0)
        tiempo_kd = (time.time() - inicio) * 1000
        
        # Medir búsqueda lineal
        inicio = time.time()
        for _ in range(100):  # 100 búsquedas
            busqueda_lineal(puntos, punto_busqueda, dimensiones)
        tiempo_lineal = (time.time() - inicio) * 1000
        
        mejora = tiempo_lineal / tiempo_kd
        
        print(f"{cantidad:<10} {tiempo_kd:<15.4f} {tiempo_lineal:<20.4f} {mejora:.2f}x")

def experimento_multiples_busquedas():
    """Experimento: múltiples búsquedas en el mismo árbol"""
    print("\n" + "=" * 60)
    print("EXPERIMENTO 3: Múltiples Búsquedas")
    print("=" * 60)
    
    dimensiones = 2
    cantidad_puntos = 50
    cantidad_busquedas = 10
    
    puntos = generar_puntos(cantidad_puntos, dimensiones, rango=100)
    arbol = kd_tree(dimensiones)
    arbol.creaArbol(puntos)
    
    print(f"\nÁrbol con {cantidad_puntos} puntos en {dimensiones}D")
    print(f"Realizando {cantidad_busquedas} búsquedas aleatorias:\n")
    
    print(f"{'Búsqueda':<10} {'Punto Buscado':<20} {'Vecino Más Cercano':<20} {'Distancia':<10}")
    print("-" * 60)
    
    for i in range(cantidad_busquedas):
        punto_busqueda = tuple(random.randint(0, 100) for _ in range(dimensiones))
        mejorp, mejord = arbol.busca(arbol.raiz, punto_busqueda, 0, None, 0)
        distancia = distancia_euclidiana(mejorp, punto_busqueda)
        
        print(f"{i+1:<10} {str(punto_busqueda):<20} {str(mejorp):<20} {distancia:<10.2f}")

def experimento_dimensiones():
    """Experimento: cómo varía el rendimiento con dimensiones"""
    print("\n" + "=" * 60)
    print("EXPERIMENTO 4: Impacto de Dimensiones")
    print("=" * 60)
    
    cantidad_puntos = 1000
    dimensiones_list = [2, 3, 4, 5, 10]
    
    print(f"\nCantidad de puntos: {cantidad_puntos}")
    print(f"{'Dimensiones':<15} {'Tiempo KD (ms)':<15} {'Tiempo Lineal (ms)':<20}")
    print("-" * 50)
    
    for dim in dimensiones_list:
        puntos = generar_puntos(cantidad_puntos, dim, rango=1000)
        punto_busqueda = tuple(random.randint(0, 1000) for _ in range(dim))
        
        # KD-tree
        arbol = kd_tree(dim)
        arbol.creaArbol(puntos)
        
        inicio = time.time()
        for _ in range(100):
            arbol.busca(arbol.raiz, punto_busqueda, 0, None, 0)
        tiempo_kd = (time.time() - inicio) * 1000
        
        # Lineal
        inicio = time.time()
        for _ in range(100):
            busqueda_lineal(puntos, punto_busqueda, dim)
        tiempo_lineal = (time.time() - inicio) * 1000
        
        print(f"{dim:<15} {tiempo_kd:<15.4f} {tiempo_lineal:<20.4f}")

def main():
    """Ejecuta todos los experimentos"""
    random.seed(42)  # Para reproducibilidad
    
    experimento_basico()
    experimento_comparativo()
    experimento_multiples_busquedas()
    experimento_dimensiones()
    
    print("\n" + "=" * 60)
    print("EXPERIMENTOS COMPLETADOS")
    print("=" * 60)

if __name__ == "__main__":
    main()
