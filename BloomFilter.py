import hashlib


class BloomFilter:

    def __init__(self, tamaño=10000, num_hashes=4):

        self.tamaño = tamaño
        self.num_hashes = num_hashes

        # Arreglo de bits
        self.bits = [0] * tamaño

    def _hashes(self, elemento):

        hashes = []

        elemento = str(elemento)

        for i in range(self.num_hashes):

            texto = elemento + str(i)

            h = hashlib.md5(texto.encode()).hexdigest()

            indice = int(h, 16) % self.tamaño

            hashes.append(indice)

        return hashes

    def agregar(self, elemento):

        for indice in self._hashes(elemento):

            self.bits[indice] = 1

    def contiene(self, elemento):

        for indice in self._hashes(elemento):

            if self.bits[indice] == 0:
                return False

        return True