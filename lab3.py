def find_numbers(x):
    result = []

    max_k = 0
    while 3 ** max_k <= x:
        max_k += 1
    
    max_l = 0
    while 5 ** max_l <= x:
        max_l += 1
    
    max_m = 0
    while 7 ** max_m <= x:
        max_m += 1
    
    for k in range(max_k):
        for l in range(max_l):
            for m in range(max_m):
                num = (3 ** k) * (5 ** l) * (7 ** m)
                if 1 <= num <= x:
                    result.append(num)
    
    result = sorted(set(result))
    return result

x = int(input("Введите число x: "))
numbers = find_numbers(x)
print(f"Числа от 1 до {x}, удовлетворяющие условию:")
print(numbers)