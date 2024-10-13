import csv
import BloomFilterK

def estimate_join(file1, file2):
    # Параметры для Bloom Filter
    k = 5  # Количество хеш-функций
    n = 1_000_000  # Размер битового массива

    # Создаем два экземпляра Bloom Filter
    bloom1 = BloomFilterK.BloomFilterK(k, n)
    bloom2 = BloomFilterK.BloomFilterK(k, n)

    # Проход по первому файлу
    with open(file1, 'r') as f1:
        reader = csv.reader(f1)
        for row in reader:
            bloom1.put(row[0])

    # Проход по второму файлу
    with open(file2, 'r') as f2:
        reader = csv.reader(f2)
        for row in reader:
            bloom2.put(row[0])

    # Оценка количества уникальных ключей
    unique_count_1 = bloom1.get_size()
    unique_count_2 = bloom2.get_size()

    # Если оба файла содержат менее 1 миллиона уникальных ключей, делаем точный подсчет
    if unique_count_1 < 1_000_000 and unique_count_2 < 1_000_000:
        set1 = set()
        with open(file1, 'r') as f1:
            reader = csv.reader(f1)
            for row in reader:
                set1.add(row[0])

        set2 = set()
        with open(file2, 'r') as f2:
            reader = csv.reader(f2)
            for row in reader:
                set2.add(row[0])

        intersection_count = len(set1.intersection(set2))
        print(f"Estimated JOIN size: {intersection_count}")
        return

    # Оценка вероятного размера JOIN с использованием Bloom Filter
    estimated_join_size = 0
    with open(file2, 'r') as f2:
        reader = csv.reader(f2)
        for row in reader:
            if bloom1.get(row[0]):
                estimated_join_size += 1

    if estimated_join_size == 0:
        print("Estimated JOIN size: 0")
        return

    if estimated_join_size > 10_000_000:
        print("JOIN exceeds 10 million")
        return

    print(f"Estimated JOIN size: {estimated_join_size}")


