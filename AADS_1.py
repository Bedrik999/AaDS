
def main():
    n = int(input())
    dots = []
    
    for _ in range(n):
        x, y = map(int, input().split())
        dots.append((x, y))
    
    jarvis_algorithm(dots)


def calculate_orientation(point_a, point_b, point_c):
    return (point_b[0] - point_a[0]) * (point_c[1] - point_a[1]) - \
           (point_b[1] - point_a[1]) * (point_c[0] - point_a[0])


def calculate_distance_squared(point_a, point_b):
    return (point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2


def jarvis_algorithm(dots):
    n = len(dots)
    
    if n < 3:
        print("No")
        return
    
    if len(dots) == 3 and calculate_orientation(dots[0], dots[1], dots[2]) == 0:
        print("No")
        return
   
    leftmost_point_index = min(range(n), key=lambda i: (dots[i][0], dots[i][1]))
    hull = []
    current_point = leftmost_point_index
    
    while True:
        hull.append(dots[current_point])
        next_point = (current_point + 1) % n
        
        for i in range(n):
            orientation = calculate_orientation(dots[current_point], dots[i], dots[next_point])
            
            if orientation > 0 or (orientation == 0 and 
                                   calculate_distance_squared(dots[current_point], dots[i]) > 
                                   calculate_distance_squared(dots[current_point], dots[next_point])):
                next_point = i
        
        current_point = next_point
        
        if current_point == leftmost_point_index:
            break
    print(hull)


if __name__ == "__main__":
    main()