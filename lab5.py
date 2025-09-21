def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]      
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

    return arr

data = [5, 3, 4, 1, 2]
print("Исходный массив:", data)
sorted_data = insertion_sort(data)
print("Отсортированный массив:", sorted_data)