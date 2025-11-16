class HashTableOpenAddressing:
    """
    Лабораторная работа №13: Хеш-таблица с наложением (метод открытой адресации)
    """
    
    def __init__(self, size=1000):
        """
        Инициализация хеш-таблицы
        
        Args:
            size: размер хеш-таблицы
        """
        self.size = size
        self.table = [None] * size  # Один массив, каждая ячейка содержит None или (key, value)
        self.collisions = 0  # Счетчик коллизий
        self.deleted = object()  # Специальный маркер для удаленных элементов
    
    def hash_function(self, key):
        
        if not key:
            return 0
        
        hash_value = 0
        for char in key:
            hash_value = (hash_value * 31 + ord(char)) % self.size
        return hash_value
    
    def linear_probe(self, index, attempt):
        """
        Линейное пробирование: ищем следующую ячейку
        
        Args:
            index: исходный индекс
            attempt: номер попытки
            
        Returns:
            новый индекс для проверки
        """
        return (index + attempt) % self.size
    
    def insert(self, key, value):
        """
        Вставка элемента в хеш-таблицу с наложением
        
        Args:
            key: ключ (слово)
            value: значение (частота)
        """
        original_index = self.hash_function(key)
        
        for attempt in range(self.size):
            current_index = self.linear_probe(original_index, attempt)
            current_cell = self.table[current_index]
            
            # Если ячейка пустая или помечена как удаленная
            if current_cell is None or current_cell == self.deleted:
                self.table[current_index] = (key, value)
                if attempt > 0:  # Если потребовалось больше 1 попытки - это коллизия
                    self.collisions += 1
                return
            
            # Если ключ уже существует - обновляем значение
            if current_cell[0] == key:
                self.table[current_index] = (key, value)
                return
        
        # Если дошли сюда - таблица переполнена
        raise Exception("Хеш-таблица переполнена!")
    
    def search(self, key):
        """
        Поиск элемента в хеш-таблице
        
        Args:
            key: ключ для поиска
            
        Returns:
            значение или None если не найдено
        """
        original_index = self.hash_function(key)
        
        for attempt in range(self.size):
            current_index = self.linear_probe(original_index, attempt)
            current_cell = self.table[current_index]
            
            # Если нашли пустую ячейку - элемента нет
            if current_cell is None:
                return None
            
            # Если нашли наш ключ (и ячейка не удалена)
            if current_cell != self.deleted and current_cell[0] == key:
                return current_cell[1]
        
        return None
    
    def delete(self, key):
        """
        Удаление элемента из хеш-таблицы
        
        Args:
            key: ключ для удаления
            
        Returns:
            True если удалено, False если не найден
        """
        original_index = self.hash_function(key)
        
        for attempt in range(self.size):
            current_index = self.linear_probe(original_index, attempt)
            current_cell = self.table[current_index]
            
            if current_cell is None:
                return False  # Элемент не найден
            
            if current_cell != self.deleted and current_cell[0] == key:
                self.table[current_index] = self.deleted  # Помечаем как удаленный
                return True
        
        return False
    
    def get_statistics(self):
        """
        Сбор статистики по хеш-таблице
        
        Returns:
            словарь со статистикой
        """
        occupied_count = sum(1 for cell in self.table if cell is not None and cell != self.deleted)
        deleted_count = sum(1 for cell in self.table if cell == self.deleted)
        
        return {
            'size': self.size,
            'occupied': occupied_count,
            'deleted': deleted_count,
            'empty': self.size - occupied_count - deleted_count,
            'collisions': self.collisions,
            'load_factor': occupied_count / self.size
        }
    
    def save_to_file(self, filename):
        """
        Сохранение хеш-таблицы в файл
        
        Args:
            filename: имя файла для сохранения
        """
        stats = self.get_statistics()
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Заголовок и общая информация
            f.write("Лабораторная работа №13: Хеш-таблица с наложением\n")
            f.write("=" * 60 + "\n")
            f.write(f"Размер таблицы: {stats['size']}\n")
            f.write(f"Занято ячеек: {stats['occupied']}\n")
            f.write(f"Удаленные ячейки: {stats['deleted']}\n")
            f.write(f"Пустые ячейки: {stats['empty']}\n")
            f.write(f"Коллизии: {stats['collisions']}\n")
            f.write(f"Коэффициент заполнения: {stats['load_factor']:.3f}\n")
            f.write("=" * 60 + "\n\n")
            
            # Детальная информация по ячейкам
            f.write("ДЕТАЛЬНАЯ СТРУКТУРА ТАБЛИЦЫ:\n")
            f.write("-" * 50 + "\n\n")
            
            for i, cell in enumerate(self.table):
                if cell is None:
                    status = "ПУСТО"
                elif cell == self.deleted:
                    status = "УДАЛЕНО"
                else:
                    key, value = cell
                    status = f"'{key}' -> {value}"
                
                f.write(f"Ячейка [{i:4d}]: {status}\n")


def read_text_file(filename):
    """
    Чтение текстового файла и разбиение на слова
    
    Args:
        filename: имя файла для чтения
    
    Returns:
        список слов
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read().lower()
        
        # Разбиваем текст на слова, игнорируя знаки препинания
        words = []
        current_word = []
        
        for char in text:
            if char.isalpha():  # Буква
                current_word.append(char)
            elif current_word:  # Не буква, но есть накопленное слово
                word = ''.join(current_word)
                if len(word) > 1:  # Игнорируем слова из одной буквы
                    words.append(word)
                current_word = []
        
        # Добавляем последнее слово, если есть
        if current_word:
            word = ''.join(current_word)
            if len(word) > 1:
                words.append(word)
        
        return words
    
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден!")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


def create_sample_text_file():
    """
    Создает тестовый файл с текстом
    """
    sample_text = """
    В лесу родилась елочка, в лесу она росла.
    The quick brown fox jumps over the lazy dog.
    
    Съешь же ещё этих мягких французских булок, да выпей чаю.
    Pack my box with five dozen liquor jugs.
    
    Зимой и летом стройная, зеленая была.
    How vexingly quick daft zebras jump!
    
    Метод наложения позволяет хранить все элементы в одном массиве.
    Open addressing stores all elements in a single array.
    """
    
    with open("sample_text.txt", "w", encoding="utf-8") as f:
        f.write(sample_text)
    
    print("Создан тестовый файл: sample_text.txt")
    return "sample_text.txt"


def demonstrate_collisions(hash_table, words):
    """
    Демонстрация работы метода наложения при коллизиях
    """
    print("\nДЕМОНСТРАЦИЯ КОЛЛИЗИЙ:")
    print("-" * 50)
    
    # Найдем несколько слов с коллизиями
    collision_examples = []
    
    for word in words[:10]:  # Проверим первые 10 слов
        original_index = hash_table.hash_function(word)
        actual_index = None
        
        # Найдем, где фактически хранится слово
        for attempt in range(hash_table.size):
            current_index = hash_table.linear_probe(original_index, attempt)
            cell = hash_table.table[current_index]
            if cell is not None and cell != hash_table.deleted and cell[0] == word:
                actual_index = current_index
                break
        
        if actual_index != original_index:
            collision_examples.append((word, original_index, actual_index))
        
        if len(collision_examples) >= 3:
            break
    
    for word, original_idx, actual_idx in collision_examples:
        print(f"Слово '{word}':")
        print(f"  Исходный хеш: {original_idx}")
        print(f"  Фактическое положение: {actual_idx}")
        print(f"  Сдвиг: {actual_idx - original_idx}")


def main():
    """
    Главная функция программы
    """
    print("Лабораторная работа №13: Хеш-таблица с наложением")
    print("=" * 60)
    
    # Создаем тестовый файл
    input_file = create_sample_text_file()
    
    # Читаем текст
    print("\nЧтение текстового файла...")
    words = read_text_file(input_file)
    
    if not words:
        print("Не удалось прочитать файл или файл пуст.")
        return
    
    print(f"Прочитано слов: {len(words)}")
    print(f"Уникальных слов: {len(set(words))}")
    
    # Создаем хеш-таблицу с небольшим размером для демонстрации коллизий
    hash_table_size = 30
    print(f"\nСоздание хеш-таблицы (размер: {hash_table_size})...")
    hash_table = HashTableOpenAddressing(hash_table_size)
    
    # Подсчитываем частоту слов и вставляем в таблицу
    from collections import Counter
    word_freq = Counter(words)
    
    print("Вставка слов в хеш-таблицу...")
    for word, count in word_freq.items():
        try:
            hash_table.insert(word, count)
        except Exception as e:
            print(f"Ошибка при вставке '{word}': {e}")
            break
    
    # Выводим статистику
    stats = hash_table.get_statistics()
    print("\nСТАТИСТИКА ХЕШ-ТАБЛИЦЫ:")
    print(f"  Размер таблицы: {stats['size']}")
    print(f"  Занято ячеек: {stats['occupied']}")
    print(f"  Удаленные ячейки: {stats['deleted']}")
    print(f"  Пустые ячейки: {stats['empty']}")
    print(f"  Коллизии: {stats['collisions']}")
    print(f"  Коэффициент заполнения: {stats['load_factor']:.3f}")
    
    # Демонстрируем коллизии
    demonstrate_collisions(hash_table, list(word_freq.keys()))
    
    # Сохраняем результат
    output_file = "hash_table_open_addressing.txt"
    hash_table.save_to_file(output_file)
    print(f"\nРезультат сохранен в файл: {output_file}")
    
    # Демонстрация поиска
    print("\nДЕМОНСТРАЦИЯ ПОИСКА:")
    print("-" * 30)
    test_words = list(word_freq.keys())[:5]
    for word in test_words:
        frequency = hash_table.search(word)
        print(f"Слово: '{word:15}' → частота: {frequency}")


if __name__ == "__main__":
    main()