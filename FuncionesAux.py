import math

def distancia_km(p1, p2):
    lat1, lon1 = p1
    lat2, lon2 = p2

    R = 6371  # radio de la Tierra en km

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def latlon_a_km(lat, lon, lat_ref=19.43):
    x = lon * 111 * math.cos(math.radians(lat_ref))
    y = lat * 111
    return (x, y)

def distancia_euclidiana(p1, p2):
    return math.sqrt(sum((p1[i] - p2[i])**2 for i in range(len(p1))))