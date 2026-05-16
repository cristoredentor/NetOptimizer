import Grafo
import pandas as pd


grafo = Grafo.Grafo()

df = pd.read_csv("datos/enlaces.csv")

for _, fila in df.iterrows():
    origen = int(fila["origen"])
    destino = int(fila["destino"])
    peso = {
        "latencia": int(fila["latencia_ms"]),
        "ancho_banda": int(fila["ancho_banda_gbps"]),
        "costo": int(fila["costo_km"])
    }
    grafo.inserta(origen, destino, peso)
    grafo.inserta(destino, origen, peso)

padre, llave = grafo.prim_latencia(1)
print(padre)
