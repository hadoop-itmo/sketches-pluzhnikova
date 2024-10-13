import mmh3

class BloomFilter:
    def __init__(self, n):
        self.size = n
        self.bit_array = 0  # Используем целое число для хранения битов
        self.hash_function = self._hash

    def _hash(self, s):
        """Хеш-функция, которая возвращает индекс бита"""
        hash_value = mmh3.hash(s)
        return hash_value % self.size

    def put(self, s):
        """Добавляет элемент в Bloom-фильтр"""
        index = self.hash_function(s)
        self.bit_array |= (1 << index)  # Устанавливаем бит в 1

    def get(self, s):
        """Проверяет наличие элемента в Bloom-фильтре"""
        index = self.hash_function(s)
        return (self.bit_array & (1 << index)) != 0  # Проверяем бит

    def get_size(self):
        """Возвращает количество установленных битов (единиц)"""
        return bin(self.bit_array).count('1')
