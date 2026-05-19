def referencias_despues_Dijkstra(grafo, nodo):
    """Devuelve conexiones (padre, hijo) excluyendo la raíz"""
    padre, _ = grafo.Dijkstra(nodo)
    nuevas_referencias = []
    for hijo, padre_nodo in padre.items():
        if padre_nodo is not None:  
            nuevas_referencias.append((padre_nodo, hijo))
    return nuevas_referencias

