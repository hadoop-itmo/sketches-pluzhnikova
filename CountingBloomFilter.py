import numpy as np
import mmh3

class CountingBloomFilter:
    def __init__(self, cap, n, k):
        self.cap = cap  # Количество бит на счетчик
        self.size = n   # Общее количество счетчиков
        self.k = k      # Количество хеш-функций
        self.bits_per_counter = 64 // cap  # Количество счетчиков в одном 64-битном числе
        self.array_size = (self.size + self.bits_per_counter - 1) // self.bits_per_counter  # Размер массива
        self.count_array = np.zeros(self.array_size, dtype=np.uint64)  # Массив для хранения счетчиков

    def _hash(self, s, seed):
        """Возвращает индекс для заданной строки"""
        hash_value = mmh3.hash(s, seed)
        return hash_value % self.size

    def put(self, s):
        """Добавляет элемент в Counting Bloom-фильтр"""
        for i in range(self.k):  # Используем k хеш-функций
            index = self._hash(s, i)
            counter_index = index // self.bits_per_counter
            bit_position = (index % self.bits_per_counter) * self.cap
            # Увеличиваем счетчик
            current_value = (self.count_array[counter_index] >> np.uint64(bit_position)) & np.uint64(((1 << self.cap) - 1))
            if current_value < np.uint64((1 << self.cap) - 1):  # Проверяем, не превышает ли он максимальное значение
                current_value += 1
                self.count_array[counter_index] |= (np.uint64(current_value) << np.uint64(bit_position))


    def get(self, s):
        """Проверяет наличие элемента в Counting Bloom-фильтре"""
        for i in range(self.k):  # Используем k хеш-функций
            index = self._hash(s, i)
            counter_index = index // self.bits_per_counter
            bit_position = (index % self.bits_per_counter) * self.cap
            if ((self.count_array[counter_index] >> np.uint64(bit_position)) & np.uint64(((1 << self.cap) - 1))) == 0:
                return False
        return True

    def get_size(self):
        """Возвращает количество установленных битов (единиц), делённое на k"""
        return sum(bin(counter).count('1') for counter in self.count_array) / self.k