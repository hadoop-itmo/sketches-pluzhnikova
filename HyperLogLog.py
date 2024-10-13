import mmh3
import math

class HyperLogLog:
    def __init__(self, b):
        self.b = b
        self.m = 1 << b  # Количество регистров
        self.alphaMM = (0.7213 / (1 + 1.079 / self.m))   # Константа для коррекции смещения
        self.registers = [0] * self.m  # Инициализация регистров нулями

    def put(self, item):
        x = mmh3.hash(item,signed=False)
        # Convert the hash to binary and ensure it has enough bits
        x_bin = bin(x)[2:].zfill(32)

        # Use the first b bits for the register index
        j = int(x_bin[:self.b], 2)

        # Use the remaining bits to calculate the rank (rho)
        w = x_bin[self.b:]
        self.registers[j] = max(self.registers[j], self._rho(w))

    def _rho(self, w):
        # Считаем количество ведущих нулей в двоичном представлении
        return len(w) - len(w.lstrip('0')) + 1

    def est_size(self):
        Z = 1.0 / sum([2 ** -reg for reg in self.registers])
        E = self.alphaMM * self.m*self.m * Z

        # Коррекция смещения
        if E <= (5.0 / 2.0) * self.m:
            V = self.registers.count(0)
            if V > 0:
                E = self.m * math.log(self.m / V)

        elif E >  (1 / 30.0) * (1 << 32):
            E = -(2 ** 32) * math.log(1 - E / (2 ** 32))

        return round(E)