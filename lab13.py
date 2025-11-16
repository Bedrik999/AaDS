#Когда происходит коллизия (два ключа имеют одинаковый хеш), мы ищем другую свободную ячейку в том же массиве.
class HashTable:
    def __init__(self, size=1000):
        
        self.size = size # size: размер хеш-таблицы (количество buckets)
        self.table = [[] for _ in range(size)]  # Создаем пустые цепочки
        self.collisions = 0  # Счетчик коллизий
    
    def hash_function(self, key):

        if not key:
            return 0
        
        # Простая хеш-функция: сумма ASCII кодов символов
        hash_value = 0
        for char in key:
            # ord - получает код символа в ascii.
            # слово cat: ord('c') = 99 => hash_value = (0 * 31 + 99) % 10 = (0 + 99) % 10 = 99 % 10 = 9
            # ord('a') = 97 => hash_value = (9 * 31 + 97) % 10 = (279 + 97) % 10 = 376 % 10 = 6
            # ord('t') = 116 => hash_value = (6 * 31 + 116) % 10 = (186 + 116) % 10 = 302 % 10 = 2
            hash_value = (hash_value * 31 + ord(char)) % self.size
        return hash_value
    
    def insert(self, key, value):
       
        # key: ключ (слово)
        # value: значение (частота или другая информация)
        
        index = self.hash_function(key)
        bucket = self.table[index] # Получает ссылку на цепочку (список) по вычисленному индексу.
        # Проверяем, есть ли уже такой ключ в цепочке
        for i, (k, v) in enumerate(bucket):
            # i - индекс элемента в цепочке (0, 1, 2, ...)
            # (k, v) - распаковываем кортеж (ключ, значение)
            # enumerate(bucket) - дает пары (индекс, элемент)
            if k == key: # Проверяем, совпадает ли ключ из цепочки с вставляемым ключом.
                # Если ключ уже существует, обновляем значение
                bucket[i] = (key, value)
                # Было: bucket = [("apple", 1)]
                # Вставляем: ("apple", 5)
                return
            # Если bucket = [("banana", 2), ("orange", 1)]
            # Первая итерация: i=0, k="banana", v=2
            # Вторая итерация: i=1, k="orange", v=1    
                
        # Если ключа нет, добавляем в цепочку (возможна коллизия)
        if bucket:  # Если bucket не пустой - это коллизия
            # пустой список [] считается False, непустой - True
            self.collisions += 1 # Увеличивает счетчик коллизий на 1.
        bucket.append((key, value))
    
    def get(self, key):
        """
        Поиск элемента в хеш-таблице
        
        Args:
            key: ключ для поиска
        
        Returns:
            значение или None если не найдено
        """
        index = self.hash_function(key)
        bucket = self.table[index] # Получает ссылку на цепочку (список) по вычисленному индексу.
        
        for k, v in bucket:
            if k == key:
                return v
        return None
    
    def save_to_file(self, filename):

        # Сохранение хеш-таблицы в файл
        # filename: имя файла для сохранения
       
        with open(filename, 'w', encoding='utf-8') as f: # имя файла для сохранения
            f.write("Хеш-таблица (метод цепочек)\n") # Записывает заголовок в файл.
            f.write("=" * 50 + "\n") # Создает разделительную линию из 50 символов =
            # ==================================================
            f.write(f"Размер таблицы: {self.size}\n") # Записывает размер хеш-таблицы.
            f.write(f"Коллизии: {self.collisions}\n") # Записывает количество коллизий.
            f.write("=" * 50 + "\n\n") # Записывает вторую разделительную линию и две пустые строки.
            
            for i, bucket in enumerate(self.table): # Перебирает все buckets таблицы с их индексами.
                if bucket:  # Записываем только непустые buckets
                    f.write(f"Bucket {i}:\n")
                    for key, value in bucket:
                        f.write(f"  '{key}' -> {value}\n") # Записывает каждый элемент с отступом.Cтрелка для наглядности
                    f.write("\n")
'''
Хеш-таблица (метод цепочек)
==================================================
Размер таблицы: 1000
Коллизии: 15
==================================================

Bucket 1:
  'apple' -> 3
  'banana' -> 5

Bucket 3:
  'cat' -> 2
'''

def read_text_file(filename):
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        # Читает ВЕСЬ текст файла в одну строку
        
        # Очистка текста и разбиение на слова
        words = [] # Создает пустой список для хранения найденных слов.
        current_word = [] # Создает временный список для накопления символов текущего слова.
        
        for char in text:
            if char.isalpha():  # Проверяет, является ли символ буквой.
                current_word.append(char.lower()) # Добавляет символ в текущее слово, преобразованный в нижний регистр.
            elif current_word:  # Не буква, но у нас есть накопленное слово
                words.append(''.join(current_word)) # Объединяет символы в строку и добавляет в список слов.
                current_word = [] # Очищает текущее слово для сбора следующего слова.
        
        # Добавляем последнее слово, если есть
        if current_word:
            words.append(''.join(current_word))
        
        return words
    
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден!")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


def process_text(filename, hash_table_size=1000):
    
    print("Чтение текстового файла...")
    words = read_text_file(filename)
    
    if not words:
        print("Не удалось прочитать файл или файл пуст.")
        return
    
    print(f"Прочитано {len(words)} слов")
    print(f"Уникальных слов: {len(set(words))}")
    
    # Создаем хеш-таблицу
    print("\nСоздание хеш-таблицы...")
    hash_table = HashTable(hash_table_size)
    
    # Подсчет частоты слов
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    
    # Вставляем слова в хеш-таблицу
    for word, count in word_count.items():
        hash_table.insert(word, count)
    
    print(f"Хеш-таблица создана!")
    print(f"Размер таблицы: {hash_table_size}")
    print(f"Коллизии: {hash_table.collisions}")
    print(f"Коэффициент заполнения: {len(word_count) / hash_table_size:.3f}")
    
    # Сохраняем хеш-таблицу в файл
    output_file = "hash_table_result.txt"
    hash_table.save_to_file(output_file)
    print(f"\nРезультат сохранен в файл: {output_file}")
    
    # Демонстрация поиска
    demo_search(hash_table, words)
    
    return hash_table


def demo_search(hash_table, words):
    """
    Демонстрация поиска в хеш-таблице
    """
    print("\nДемонстрация поиска:")
    print("-" * 30)
    
    # Берем несколько случайных слов для демонстрации
    demo_words = words[:5] + words[-5:]  # Первые и последние 5 слов
    demo_words = list(set(demo_words))[:5]  # Уникальные, не более 5
    
    for word in demo_words:
        frequency = hash_table.get(word)
        print(f"Слово '{word}': частота = {frequency}")


# Создание тестового файла с текстом
def create_sample_text_file():
    """
    Создает тестовый файл с текстом на русском и английском
    """
    sample_text = """
    В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!
    The quick brown fox jumps over the lazy dog.
    
    Съешь же ещё этих мягких французских булок, да выпей чаю.
    Pack my box with five dozen liquor jugs.
    
    Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.
    How vexingly quick daft zebras jump!
    
    Широкая электрификация южных губерний даст мощный толчок 
    развитию сельскохозяйственного производства.
    """
    
    with open("sample_text.txt", "w", encoding="utf-8") as f:
        f.write(sample_text)
    
    print("Создан тестовый файл: sample_text.txt")


# Основная программа
if __name__ == "__main__":
    # Создаем тестовый файл, если его нет
    create_sample_text_file()
    
    print("Лабораторная работа №13: Хеш-таблица с методом цепочек")
    print("=" * 60)
    
    # Обрабатываем текст
    filename = "sample_text.txt"  # Можно заменить на любой другой файл
    hash_table = process_text(filename, hash_table_size=50)  # Маленький размер для демонстрации коллизий
    
    # Дополнительная демонстрация
    if hash_table:
        print("\n" + "=" * 60)
        print("Дополнительная информация:")
        print(f"Коэффициент коллизий: {hash_table.collisions / len([b for b in hash_table.table if b]) if any(hash_table.table) else 0:.2f}")