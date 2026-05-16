import Grafo
import pandas as pd


grafo = Grafo.Grafo()

df_e = pd.read_csv("datos/enlaces.csv")
df_n = pd.read_csv("datos/nodos.csv")

def insertaNodos():

    nodos = []
    for _, fila_n in df_n.iterrows():
        for _, fila_e  in df_e.iterrows():

            tipo = str(fila_n["tipo"])
            latitud = float(fila_n["latitud"])
            longitud = float(fila_n["longitud"])
            id = int(fila_n["id"])
            if(id == int(fila_e["origen"])):
                latencia = (int(fila_e["destino"]), fila_e["latencia_ms"])
                

            nodos.append(
                (tipo, latitud, longitud, id, latencia)
            )

    return nodos
    

def insertaElementos(grafo):
    for _, fila in df_e.iterrows():
        origen = int(fila["origen"])
        destino = int(fila["destino"])
        peso = {
            "latencia": int(fila["latencia_ms"]),
            "ancho_banda": int(fila["ancho_banda_gbps"]),
            "costo": int(fila["costo_km"])
        }
        # Grafo.inserta_no_dirigido ya agrega ambas direcciones,
        # por lo que solo necesitamos llamarlo una vez.
        grafo.inserta_no_dirigido(origen, destino, peso)
    return grafo

## Comparaciones
def comparaciones(elemento_a_comparar, grafo):
    total = 0
    for vecinos in grafo.getOrigen().values():
        for peso in vecinos.values():
            total = total + peso[elemento_a_comparar]

    print(f"sin prim la suma total de {elemento_a_comparar} es de {total}")
        
    _, llave = grafo.prim_latencia(1)
    suma = 0
    for valores in llave.values():
        suma = suma + valores

    print(f"con prim la suma total de {elemento_a_comparar} es de {suma}")


def conexiones(grafo):
    """Devuelve una lista de conexiones (tuplas de ids) sin duplicados.
    Si el grafo es no dirigido, evita repetir (a,b) y (b,a) usando sorted.
    """
    conexiones = set()
    for origen, vecinos in grafo.getOrigen().items():
        for destino in vecinos:
            conexion = tuple(sorted((origen, destino)))
            conexiones.add(conexion)

    return list(conexiones)

def conexiones_con_pos(posiciones):
    #  diccionario índice -> coordenadas
    # Mapear por el id real del nodo (columna 'id' en el CSV)
    coordenadas = {}
    for _, fila in df_n.iterrows():
        try:
            node_id = int(fila["id"])
        except Exception:
            # Si la columna ya está indexada o tiene otro formato,
            # usar el índice de la fila como respaldo
            node_id = int(_)
        coordenadas[node_id] = (float(fila["latitud"]), float(fila["longitud"]))

    # Construir las direcciones usando ids de nodos
    direcciones = []
    for idx_origen, idx_destino in posiciones:
        o = int(idx_origen)
        d = int(idx_destino)
        if o in coordenadas and d in coordenadas:
            direcciones.append((coordenadas[o], coordenadas[d]))

    return direcciones

def referencias_despues_prim(grafo):
    """Devuelve conexiones (padre, hijo) excluyendo la raíz"""
    padre, _ = grafo.prim_latencia(1)
    nuevas_referencias = []
    for hijo, padre_nodo in padre.items():
        if padre_nodo is not None:  
            nuevas_referencias.append((padre_nodo, hijo))
    return nuevas_referencias



insertaElementos(grafo)
padre, llave = grafo.prim_latencia(1)
print(padre)