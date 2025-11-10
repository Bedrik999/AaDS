def quick_sort(arr):

    # Базовый случай: массивы длиной 0 или 1 уже отсортированы
    if len(arr) <= 1:
        return arr
    
    # Выбор опорного элемента
    pivot = arr[len(arr) // 2]
    
    # Разделение на три части
    left = [x for x in arr if x < pivot]      # Элементы меньше опорного
    middle = [x for x in arr if x == pivot]   # Элементы равные опорному
    right = [x for x in arr if x > pivot]     # Элементы больше опорного

    '''
    Пример для [38, 27, 43, 3, 9, 82, 10] c pivot = 43:

    left = [38, 27, 3, 9, 10]

    middle = [43]

    right = [82]
    '''
    
    # Рекурсивная сортировка и объединение
    return quick_sort(left) + middle + quick_sort(right)


def partition(arr, low, high):
    
    # Выбираем опорный элемент (здесь - последний элемент)
    pivot = arr[high]
    
    # Индекс элемента, который меньше опорного
    i = low - 1
    
    for j in range(low, high):
        # Если текущий элемент меньше или равен опорному
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Меняем местами
    
    # Помещаем опорный элемент на правильную позицию
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# Пример использования
data = [329, 457, 657, 839, 436, 720, 355]
print("Исходный массив:", data)

simple_sorted = quick_sort(data.copy())
print("Отсортированный массив:", simple_sorted)
