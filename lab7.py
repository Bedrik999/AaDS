def shell_sort(arr):
    n = len(arr)
    gap = n // 2 

    while gap > 0:
        for i in range(gap, n):
            key = arr[i]
            j = i
            while j >= gap and arr[j - gap] > key:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = key

        gap //= 2
    return arr

data = [8, 4, 5, 2, 9, 1, 3, 7, 6]
print("Исходный массив:", data)
sorted_data = shell_sort(data)
print("Отсортированный массив:", sorted_data)