class nodoKd:
    def __init__(self, valor = None):
        self.distancia = 0     
        self.hijoizq = None
        self.hijoder = None
        self.value = valor
    
    #setters
    def setHijoIzq(self,hijo):
        self.hijoizq = hijo
    
    def setHijoDer(self, hijo):
        self.hijoder = hijo
        
    def setValue(self,valor):
        self.value = valor
    
    def setDistancia(self, distancia):
        self.distancia = distancia
    
    #getters 
    def getValor(self):
        return self.value
    
    def getHijoIzq(self):
        return self.hijoizq
    
    def getHijoDer(self):
        return self.hijoder
    
    def getHijoValor(self):
        return self.value
    
    def getDistancia(self):
        return self.distancia

class kd_tree:
    def __init__(self, k):
        self.raiz = None
        self.elementos = 0
        self.dimensiones = k
    
    def creaArbol(self, puntos):
        self.elementos = len(puntos)
        self.raiz = self.__insertaPuntos(puntos, 0)
        
    
    def __insertaPuntos(self, puntos, nivel):
        if(len(puntos) == 0):
            return None
        puntos = sorted(puntos, key = lambda x: x[nivel % self.dimensiones])
        med = len(puntos) //2
        actual = nodoKd(puntos[med])
        actual.setHijoIzq(self.__insertaPuntos(puntos[0:med], nivel+1))
        actual.setHijoDer(self.__insertaPuntos(puntos[med+1:], nivel+1))
        
        return actual

    
    def busca(self, actual, punto, nivel, mejorp, mejord):
        if actual is None: 
            return (mejorp, mejord)
        
        if mejorp is None or self.distancia(actual.getValor(), punto) < mejord:
            mejorp = actual.getValor()
            mejord = self.distancia(actual.getValor(), punto)
            
        c = nivel % self.dimensiones
        ramaIzq =True
        
        if punto[c] <= actual.getValor()[c]:
            mejorp, mejord =  self.busca(actual.getHijoIzq(), punto, nivel+1, mejorp, mejord)
        else:
            mejorp, mejord = self.busca(actual.getHijoDer(), punto, nivel+1, mejorp, mejord)
            ramaIzq = False
            
        if mejord > (actual.getValor()[c] - punto[c]) **2:
            if ramaIzq is True:
                mejorp, mejord = self.busca(actual.getHijoDer(), punto, nivel+1, mejorp, mejord)
            else:
                mejorp, mejord = self.busca(actual.getHijoIzq(), punto, nivel+1, mejorp, mejord)
            
        return (mejorp, mejord)
                
        
    def distancia(self, nodo1, nodo2):
        d= 0
        for i in range(self.dimensiones):
            d+=  (nodo1[i] - nodo2[i]) **2
        
        return d