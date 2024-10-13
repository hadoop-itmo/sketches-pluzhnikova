import mmh3

class BloomFilterK:
    def __init__(self, k, n):
        self.k = k
        self.size = n
        self.bit_array = 0  # Используем целое число для хранения битов
        self.hash_functions = [i for i in range(k)]

    def _hash(self, s,l):
        """Хеш-функция, которая возвращает индекс бита"""
        hash_value = mmh3.hash(s,l)
        return hash_value % self.size

    def put(self, s):
        """Добавляет элемент в Bloom-фильтр"""
        for hash_i in self.hash_functions:
            index = self._hash(s,hash_i)
            self.bit_array |= (1 << index)  # Устанавливаем бит в 1

    def get(self, s):
        """Проверяет наличие элемента в Bloom-фильтре"""
        return all((self.bit_array & (1 << self._hash(s,hash_i))) != 0 for hash_i in self.hash_functions)

    def get_size(self):
        """Возвращает количество установленных битов (единиц), делённое на k"""
        return bin(self.bit_array).count('1') / self.k
