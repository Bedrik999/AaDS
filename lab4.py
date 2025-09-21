def comb_sort(arr):
    n = len(arr)
    gap = n
    shrink = 1.3  
    swapped = True

    while gap > 1 or swapped:
        gap = int(gap // shrink)
        if gap < 1:
            gap = 1

        swapped = False

        for i in range(0, n - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True

    return arr

data = [8, 4, 5, 2, 9]
print("Исходный массив:", data)
sorted_data = comb_sort(data)
print("Отсортированный массив:", sorted_data)