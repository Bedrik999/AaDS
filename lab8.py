def counting_sort_for_radix(arr, exp):
    """
    Сортировка подсчётом по текущему разряду.
    exp — это 1 (единицы), 10 (десятки), 100 (сотни) и т.д.
    """
    n = len(arr)
    output = [0] * n  # временный массив
    count = [0] * 10  # массив для цифр 0-9

    # считаем количество вхождений каждой цифры
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1

    # преобразуем count в позиции
    for i in range(1, 10):
        count[i] += count[i - 1]

    # строим отсортированный массив (в обратном порядке для устойчивости)
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    # копируем результат в исходный массив
    for i in range(n):
        arr[i] = output[i]


def radix_sort(arr):
    # находим максимальный элемент, чтобы узнать количество разрядов
    max_num = max(arr)

    exp = 1
    while max_num // exp > 0:
        counting_sort_for_radix(arr, exp)
        exp *= 10

    return arr


# Пример использования
data = [329, 457, 657, 839, 436, 720, 355]
print("Исходный массив:", data)
sorted_data = radix_sort(data)
print("Отсортированный массив:", sorted_data)