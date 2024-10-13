import utils
import BloomFilter
import pandas as pd
import BloomFilterK
import HyperLogLog
import CountingBloomFilter
import task_5
import task_6

def checkBloomFilter():
    bloom_size = [8,16,1024,524288,134217728]
    string_size = [5,50,500,5000]
    # uncomment next section to generate data
    # for string in string_size:
    #     utils.gen_uniq_seq("Size_" + str(string), string)
    lst = []
    for i in bloom_size:
        for j in string_size:
            bloom_filter = BloomFilter.BloomFilter(i)
            fp_count = 0
            with open("Size_" + str(j),'r') as file:
                for value in file:
                    a = bloom_filter.get(value)
                    if a:
                        fp_count+= 1
                    bloom_filter.put(value)
            lst.append([i, j,fp_count, bloom_filter.get_size(), ])
    df = pd.DataFrame(lst, columns=['bf_size', 'set_size', 'fp_count', 'ones_count'])
    df.to_csv('Task_1.csv', index=False)
    print(df)

def checkBloomFilterK():
    bloom_size = [8,16,1024,524288,134217728]
    string_size = [5,50,500]
    k_list = [1, 2, 3, 4]
    # uncomment next section to generate data
    # for string in string_size:
    #     utils.gen_uniq_seq("Size_" + str(string), string)
    lst = []
    for k in k_list:
        for i in bloom_size:
            for j in string_size:
                bloom_filter = BloomFilterK.BloomFilterK(k, i)
                fp_count = 0
                with open("Size_" + str(j),'r') as file:
                    for value in file:
                        a = bloom_filter.get(value)
                        if a:
                            fp_count+= 1
                        bloom_filter.put(value)
                lst.append([k, i, j,fp_count, round(bloom_filter.get_size(), 2)])
    df = pd.DataFrame(lst, columns=['k', 'bf_size', 'set_size', 'fp_count', 'ones_count'])
    df.to_csv('Task_2.csv', index=False)
    print(df)

def checkCountingBloomFilter():
    """
         1) Проверяем, что при увеличении cap количество единиц становится ближе к реальному числу строк
         2) Проверяем, что при cap=1 получаем обычный bloom filter
         3) Проверяем нестандартное количество битов на счетчик (не делит 64)
         """
    bloom_size = [8,16,1024,8192,524288]
    string_size = [5,50,5000]
    cap_list = [1, 8, 22]

    # uncomment next section to generate data
    # for string in string_size:
    #     utils.gen_uniq_seq("Size_" + str(string), string)
    lst = []
    for cap in cap_list:
        for i in bloom_size:
            for j in string_size:
                bloom_filter = CountingBloomFilter.CountingBloomFilter(cap, i,2)
                fp_count = 0
                with open("Size_" + str(j),'r') as file:
                    for value in file:
                        a = bloom_filter.get(value)
                        if a:
                            fp_count += 1
                        bloom_filter.put(value)

                lst.append([cap, i, j,fp_count, round(bloom_filter.get_size(), 2)])
    df = pd.DataFrame(lst, columns=['cap', 'bf_size', 'set_size', 'fp_count', 'ones_count'])
    df.to_csv('Task_3.csv', index=False)
    print(df)

def checkHyperLogLog():
    string_size = [500, 5000, 50000]
    b_list = [14, 18]
    # uncomment next section to generate data
    # for string in string_size:
    #     utils.gen_grouped_seq("grouped_" + str(string), pattern = [(string, 1), (20, 10)])
    lst = []
    for b in b_list:
        for j in string_size:
            hyper_log_log = HyperLogLog.HyperLogLog(b)
            with open("grouped_" + str(j),'r') as file:
                for line in file:
                    value = line.strip().split(':')[0]
                    hyper_log_log.put(value)
            estimated_size = hyper_log_log.est_size()
            error_percentage = abs(estimated_size - j) / j
            lst.append([b, j + 20, estimated_size, error_percentage])
    df = pd.DataFrame(lst, columns=['b', 'set_size', 'hyper_log_log_count', 'error_percentage'])
    df.to_csv('Task_4.csv', index=False)
    print(df)

def checkTask5():
    """Сгенерируем файлы так, чтобы первые 10 ключей превышали 60 000 записей (паттерн (10, 65000)).
    Остальные - не превышали: 20 ключей по 20 000 записей (паттерн (20, 20000))"""
    # uncomment next section to generate data
    # pattern = [(10, 65000), (20, 20000)]  # 10 keys with 65,000 records each, 20 keys with 20,000 records
    # utils.gen_grouped_seq("file1.csv", pattern, to_shuffle=True)

    file1_path = 'file1.csv'
    file2_path = 'file1.csv'
    problematic_keys = task_5.find_problematic_keys(file1_path, file2_path)
    print(f"Число проблемных ключей: {len(problematic_keys)}") # 10
    print(f"Ключи: {problematic_keys}")

def checkTask6():
    # uncomment next section to generate data
    # pattern = [(10000, 1), (2000, 2)]
    # utils.gen_grouped_seq("file2.csv", pattern, to_shuffle=True)
    file1_path = 'file2.csv'
    file2_path = 'file2.csv'
    task_6.estimate_join(file1_path, file2_path)

    # pattern = [(1, 100)]
    # utils.gen_grouped_seq("file3.csv", pattern, to_shuffle=True)
    # utils.gen_grouped_seq("file4.csv", pattern, to_shuffle=True)
    file1_path = 'file3.csv'
    file2_path = 'file4.csv'
    task_6.estimate_join(file1_path, file2_path)

if __name__ == '__main__':
    checkBloomFilter()
    checkBloomFilterK()
    checkCountingBloomFilter()
    checkHyperLogLog()
    checkTask5()
    checkTask6()