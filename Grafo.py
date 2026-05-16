import numpy as np
# Método alternativo: instalar e importar en una celda
from collections import deque


class NodoHeap:

    def __init__(self, nodo, costo):
        self.nodo = nodo
        self.costo = costo

    def __lt__(self, otro):
        return self.costo < otro.costo

class MinHeap:

    def __init__(self): #Método constructor 
        self.elementos = []

    def isEmpty(self):  #Método para ver si está vacio
        return len(self.elementos) == 0

    def insertaElem(self, dato):

        self.elementos.append(dato) 
        indiceActual = len(self.elementos) - 1 #guardamos los elementos en el índice final

        # Heapify up
        while indiceActual > 0:

            indicePadre = (indiceActual - 1) // 2  #su padre es la funcion piso de la mitad

            if self.elementos[indicePadre] < self.elementos[indiceActual]:
                break

            # Intercambio
            self.elementos[indicePadre], self.elementos[indiceActual] = \
                self.elementos[indiceActual], self.elementos[indicePadre]

            indiceActual = indicePadre

    def eliminaMin(self):
        if self.isEmpty():
            return None

        minimo = self.elementos[0]

        ultimo = self.elementos.pop()

        if not self.isEmpty():

            self.elementos[0] = ultimo

            self.__heapifyDown(0)

        return minimo

    def __heapifyDown(self, indice):

        n = len(self.elementos)

        while True:

            menor = indice

            izq = 2 * indice + 1
            der = 2 * indice + 2

            if izq < n and self.elementos[izq] < self.elementos[menor]:
                menor = izq

            if der < n and self.elementos[der] < self.elementos[menor]:
                menor = der

            if menor == indice:
                break

            self.elementos[indice], self.elementos[menor] = \
                self.elementos[menor], self.elementos[indice]

            indice = menor


class Grafo:

    def __init__(self):
        self.origen = {}
        
    def getOrigen(self):
        return self.origen

    def inserta_no_dirigido(self, v1, v2, peso):

        if v1 not in self.origen:
            self.origen[v1] = {}

        if v2 not in self.origen:
            self.origen[v2] = {}

        self.origen[v1][v2] = peso # peso es un arreglo cuyo primer elemento va a ser latencia, el segundo ancho de banda y el tercero costo
        self.origen[v2][v1] = peso

    def prim_latencia(self, v0):

        padre = {} #Diccionario con los padres de cada nodo
        llave = {} #Diccionario que guarda el valor de un nodo con respecto a otro
        visitado = {} #Nos dice que nodos hemos visitado

        for nodo in self.origen:

            padre[nodo] = None
            llave[nodo] = np.inf
            visitado[nodo] = False

        llave[v0] = 0

        if v0 not in self.origen:
            raise KeyError(f"El nodo inicial {v0} no existe en el grafo")

        heap = MinHeap()

        heap.insertaElem(NodoHeap(v0, 0))

        while not heap.isEmpty():

            actual = heap.eliminaMin()

            u = actual.nodo
            
            if visitado[u]: 
                continue


            visitado[u] = True

            for vecino, peso in self.origen[u].items():

                if not visitado[vecino] and peso["latencia"] < llave[vecino]:

                    llave[vecino] = peso["latencia"]
                    padre[vecino] = u

                    heap.insertaElem(
                        NodoHeap(vecino, peso["latencia"])
                    )

        return padre, llave
    
    def DFS(self):
        
        "Método que regresa los elementos de un grafo con el método de Depth First Search"
        
        visitados = {}
        for v in self.origen:
            visitados[v] = False
        lista = []

        for v in self.origen:
            if not visitados[v]:
                self.__DFS(v, lista, visitados)

        return lista
  
    def __DFS(self, actual, lista, visitados):
        
        visitados[actual] = True
        lista.append(actual)

        for hijo in self.origen[actual]:

            if not visitados[hijo]:
                self.__DFS(hijo, lista, visitados)
                
    def BFS(self):
        "Método que regresa los elementos de un grafo con el método de Breath First Search"
        visitados = {}

        for v in self.origen:
            visitados[v] = False

        lista = []

        for v in self.origen:

            if not visitados[v]:
                self.__BFS(v, lista, visitados)

        return lista
    
    def __BFS(self, actual, lista, visitados):

        cola = deque()

        cola.append(actual)
        visitados[actual] = True

        while len(cola) > 0:

            actual = cola.popleft()

            lista.append(actual)

            for hijo in self.origen[actual]:

                if not visitados[hijo]:

                    visitados[hijo] = True
                    cola.append(hijo)
                    
    def Dijkstra(self, v0):
        padre = {}
        llave = {}
        visitado = {}

        for nodo in self.origen:

            padre[nodo] = None
            llave[nodo] = np.inf
            visitado[nodo] = False

        llave[v0] = 0

        heap = MinHeap()

        heap.insertaElem(
            NodoHeap(v0, 0)
        )

        while not heap.isEmpty():

            actual = heap.eliminaMin()

            u = actual.nodo

            if visitado[u]:
                continue

            visitado[u] = True

            for vecino, peso in self.origen[u].items():

                if (
                    not visitado[vecino]
                    and
                    llave[u] + peso < llave[vecino]
                ):

                    llave[vecino] = llave[u] + peso

                    padre[vecino] = u

                    heap.insertaElem(
                        NodoHeap(vecino, llave[vecino])
                    )

        return padre, llave