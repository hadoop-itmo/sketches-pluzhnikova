import csv
from collections import defaultdict


def count_keys(file_path):
    key_count = defaultdict(int)
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            key = row[0]  # Предполагаем, что ключ находится в первой колонке
            key_count[key] += 1
    return key_count


def find_problematic_keys(file1_path, file2_path, threshold=60000):
    # Считаем ключи для первого файла
    key_count_1 = count_keys(file1_path)

    # Считаем ключи для второго файла и проверяем на пересечения
    problematic_keys = set()

    with open(file2_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            key = row[0]  # Предполагаем, что ключ находится в первой колонке
            if key in key_count_1:
                total_count = key_count_1[key] + 1  # Учитываем текущее вхождение из второго файла
                if total_count >= threshold:
                    problematic_keys.add(key)

    return problematic_keys