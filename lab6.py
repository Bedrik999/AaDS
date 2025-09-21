def selection_sort(arr):
    n = len(arr)
    
    for i in range(n - 1):
        min_index = i
        
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j

        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

data = [5, 3, 4, 1, 2]
print("Исходный массив:", data)
sorted_data = selection_sort(data)
print("Отсортированный массив:", sorted_data)