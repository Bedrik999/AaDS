#Проблема: У нас есть огромный файл (10 ГБ), но оперативная память всего 8 ГБ
#Решение: Внешняя сортировка - обрабатываем данные частями
import heapq
import os

def external_polyphase_sort(input_file, output_file, chunk_size=1000):
    """
    Args:
        input_file: огромный файл, который не помещается в память
        output_file: куда записать отсортированный результат
        chunk_size: сколько чисел можем обработать за раз в памяти
    """
    
    # ФАЗА 1: Разбиваем большой файл на отсортированные чанки
    print("=== ФАЗА 1: Разбиение на отсортированные чанки ===")
    chunk_files = _create_sorted_chunks(input_file, chunk_size) #Делим огромный файл на маленькие отсортированные кусочки
    
    # ФАЗА 2: Многофазное слияние чанков
    print("\n=== ФАЗА 2: Многофазное слияние ===")
    _polyphase_merge(chunk_files, output_file) #Объединяем маленькие отсортированные кусочки в один большой отсортированный файл
    
    # Очистка временных файлов
    for chunk_file in chunk_files:
        os.remove(chunk_file)
    
    print(f"\nСортировка завершена! Результат в {output_file}")


def _create_sorted_chunks(input_file, chunk_size):
    """
    Фаза 1: Читаем большой файл кусками, сортируем в памяти, 
    записываем в временные файлы-чанки
    """
    chunk_files = [] # Список для хранения имен файлов-чанков
    chunk_number = 0 # Номер текущего чанка
    
    with open(input_file, 'r') as f: # читаем наш огромный файл
        while True:
            # Читаем chunk_size чисел в оперативную память
            chunk = []
            for _ in range(chunk_size):
                line = f.readline()
                if not line:  # Если строка пустая - конец файла
                    break
                chunk.append(int(line.strip())) # Добавляем число в чанк
            
            if not chunk:  # Если ничего не прочитали - выходим
                break
            # Если chunk_size = 1000, мы читаем 1000 чисел в список chunk
            
            # Сортируем чанк в оперативной памяти
            chunk.sort()
            
            # Сохраняем отсортированный чанк во временный файл
            chunk_filename = f"chunk_{chunk_number}.txt"
            with open(chunk_filename, 'w') as chunk_file: # Записываем отсортированные 1000 чисел в файл chunk_0.txt
                for number in chunk:
                    chunk_file.write(f"{number}\n")
            
            print(f"Создан чанк {chunk_number} с {len(chunk)} числами")
            chunk_files.append(chunk_filename)
            chunk_number += 1
            # Если было 5000 чисел и chunk_size = 1000, получим 5 файлов: chunk_0.txt, chunk_1.txt, ... chunk_4.txt
    return chunk_files


def _polyphase_merge(chunk_files, output_file):
    """
    Фаза 2: Многофазное слияние отсортированных чанков
    """
    # Открываем все 5(условно) файлов-чанков для одновременного чтения
    chunk_readers = []
    for chunk_file in chunk_files:
        chunk_readers.append(open(chunk_file, 'r'))
    
    try:
        # Создаем кучу (min-heap) для слияния
        heap = []
        
        # Инициализация: берем по первому числу из каждого чанка
        # Из каждого чанка берем первое (наименьшее) число и кладем в кучу.
        # chunk_0.txt: [1, 5, 9, ...] → берем 1
        # chunk_1.txt: [2, 6, 8, ...] → берем 2
        # chunk_2.txt: [3, 4, 7, ...] → берем 3
        for i, reader in enumerate(chunk_readers):
            line = reader.readline()
            if line:
                number = int(line.strip())
                # Сохраняем (число, индекс_чанка, reader)
                heapq.heappush(heap, (number, i, reader))
        #Куча: [(1,0), (2,1), (3,2)]    

        # Процесс слияния
        # Достаем из кучи наименьшее число (1)
        # Записываем его в итоговый файл
        with open(output_file, 'w') as out_f:
            while heap:
                # Берем наименьшее число из кучи
                smallest_num, chunk_idx, reader = heapq.heappop(heap)
                
                # Записываем его в выходной файл
                out_f.write(f"{smallest_num}\n")
                
                # Берем следующее число из того же чанка
                # Из чанка, откуда взяли число 1, читаем следующее число (5)
                # Кладем его в кучу
                next_line = reader.readline()
                if next_line:
                    next_num = int(next_line.strip())
                    heapq.heappush(heap, (next_num, chunk_idx, reader))
                # Теперь куча: [(2,1), (3,2), (5,0)]
        
        print(f"Слияние завершено. Слито {len(chunk_files)} чанков")
        
    finally:
        # Закрываем все файлы
        for reader in chunk_readers:
            reader.close()


# Создание тестовых данных
def generate_test_data(filename, num_elements=10000):
    """Генерирует большой файл со случайными числами"""
    import random
    with open(filename, 'w') as f:
        for i in range(num_elements):
            f.write(f"{random.randint(1, 100000)}\n")
    print(f"Сгенерирован файл {filename} с {num_elements} числами")


# Демонстрация
if __name__ == "__main__":
    # Создаем тестовые данные
    input_file = "big_data.txt"
    output_file = "sorted_data.txt"
    
    generate_test_data(input_file, 5000)  # 5000 случайных чисел
    
    # Запускаем сортировку
    external_polyphase_sort(input_file, output_file, chunk_size=1000)
    
    # Проверяем результат
    with open(output_file, 'r') as f:
        numbers = [int(line.strip()) for line in f]
        is_sorted = all(numbers[i] <= numbers[i+1] for i in range(len(numbers)-1))
        print(f"\nПроверка сортировки: {'УСПЕХ' if is_sorted else 'ОШИБКА'}")
        print(f"Отсортировано {len(numbers)} элементов")

'''
Визуализация процесса слияния

Исходные чанки:

Чанк 0: [1, 5, 9]
Чанк 1: [2, 6, 8] 
Чанк 2: [3, 4, 7]

Процесс слияния:

    Инициализация кучи: [(1,0), (2,1), (3,2)]

    Извлекаем 1 → записываем 1, берем 5 из чанка 0 → куча: [(2,1), (3,2), (5,0)]

    Извлекаем 2 → записываем 2, берем 6 из чанка 1 → куча: [(3,2), (5,0), (6,1)]

    Извлекаем 3 → записываем 3, берем 4 из чанка 2 → куча: [(4,2), (5,0), (6,1)]

    Извлекаем 4 → записываем 4, берем 7 из чанка 2 → куча: [(5,0), (6,1), (7,2)]

    И так далее...

Результат: [1, 2, 3, 4, 5, 6, 7, 8, 9]
'''