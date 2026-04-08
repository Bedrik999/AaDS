import math
from itertools import combinations

def dist(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1]  - b[1]) ** 2)

def lines_cross(a, b, c, d):
    if a[0] - b[0] == 0:
        if c[0] - d[0] == 0 and a[0] == b[0]:
            return "Colinear"
        if c[0] - d[0] == 0 and a[0] != b[0]:
            return None
        
        k2 = (c[1] - d[1]) / (c[0] - d[0])
        b2 = c[1] - k2 * c[0]
        
        x = a[0]
        y = k2 * x + b2

        return (x, y)

    if c[0] - d[0] == 0:
        if a[0] - b[0] == 0 and c[0] == d[0]:
            return "Colinear"
        if a[0] - b[0] == 0 and c[0] != d[0]:
            return None
        
        k1 = (a[1] - b[1]) / (a[0] - b[0])
        b1 = a[1] - k1 * a[0]

        
        x = c[0]
        y = k1 * x + b1

        return (x, y)

    k1 = (a[1] - b[1]) / (a[0] - b[0])
    b1 = a[1] - k1 * a[0]

    k2 = (c[1] - d[1]) / (c[0] - d[0])
    b2 = c[1] - k2 * c[0]

    if k1 == k2 and  b1 == b2:
        return "Colinear"
    
    if k1 == k2 and  b1 != b2:
        return None
    
    x = (b1 - b2) / (k2 - k1)
    y = k1 * x + b1

    return (x, y)

def segments_cross(a, b, c, d):
    dot = lines_cross(a, b, c, d)

    if dot is None:
        return None
    
    if dot == "Colinear":
        if a[0] == b[0] == c[0] == d[0]:
            y1 = min(a[1], b[1])
            y2 = max(a[1], b[1])
            y3 = min(c[1], d[1])
            y4 = max(c[1], d[1])

            if y2 < y3 or y4 < y1:
                return None
            elif y2 == y3:
                return (a[0], y2)
            elif y4 == y1:
                return (a[0], y1)
            else:
                return "Colinear"
            
        a1 = min(a[0], b[0])
        b1 = max(a[0], b[0])   

        c1 = min(c[0], d[0])
        d1 = max(c[0], d[0])  

        if b1 < c1 or d1 < a1:
            return None
        elif b1 == c1:
            return max(a, b, key=lambda a: a[0])
        elif d1 == a1:
            return max(c, d, key=lambda a: a[0])
        else:
            return "Colinear"
        
    x, y = dot 

    if min(a[0], b[0]) <= x <= max(a[0], b[0]) and \
        min(c[0], d[0]) <= x <= max(c[0], d[0]) and \
        min(a[1], b[1]) <= y <= max(a[1], b[1]) and \
        min(c[1], d[1]) <= y <= max(c[1], d[1]):
        return (x, y)
    
    return None

def segment_and_line_cross(a, b, c, d):
    dot = lines_cross(a, b, c, d)

    if dot is None:
        return None
    
    if dot == "Colinear":
        return "Colinear"

    x, y = dot 

    if min(c[0], d[0]) <= x <= max(c[0], d[0]) and min(c[1], d[1]) <= y <= max(c[1], d[1]):
        return (x, y)
    
    return None

def line_and_circle_cross(a, b, o, r):
    if a[0] - b[0] == 0:
        x = a[0]
        a1 = 1
        b1 = -2 * o[1]
        c1 = o[1] ** 2 - r ** 2 + (x - o[0])** 2

        d = b1 ** 2 - 4 * a1 * c1

        if d < 0:
            return None
        elif d == 0:
            y = -b1 / (2 * a1)
            return[(x, y)]
        else:
            y1 = (- b1 + math.sqrt(d)) / (2 * a1)
            y2 = (- b1 - math.sqrt(d)) / (2 * a1)

            return [(x, y1), (x, y2)]

    k = (a[1] - b[1]) / (a[0] - b[0])
    b = a[1] - k * a[0]

    a1 = 1 + k ** 2
    b1 = - 2 * o[0] - 2 * o[1] * k + 2 * k * b
    c1 = o[0] ** 2 + b ** 2 + o[1] ** 2 - 2 * b * o[1] - r ** 2

    d = b1 ** 2 - 4 * a1 * c1

    if d < 0:
        return None
    elif d == 0:
        x = -b1 / (2 * a1)
        y = k * x + b
        return [(x, y)]
    else:
        x1 = (- b1 + math.sqrt(d)) / (2 * a1)
        y1 = k * x1 + b

        x2 = (- b1 - math.sqrt(d)) / (2 * a1)
        y2 = k * x2 + b

        return [(x1, y1), (x2, y2)]

    
def segment_and_circle_cross(a, b, o, r):
    dot = line_and_circle_cross(a, b, o, r)

    if dot is None:
        return None
    
    res = []
    for el in dot:
        x, y = el

        if min(a[0], b[0]) <= x <= max(a[0], b[0]) and min(a[1], b[1]) <= y <= max(a[1], b[1]):
            res.append((x, y))

    if res == []: 
        return None

    return res

def circles_cross(o1, r1, o2, r2):
    if dist(o1, o2) > r1 + r2:
        return None
    
    if o1 == o2 and r1 == r2:
        return "Same"
    
    if o1 == o2 and r1 != r2:
        return None
    
    if o1[0] - o2[0] != 0:
        x1 = (r2 ** 2 - r1 ** 2 + o1[1] ** 2 - o2[1] ** 2 + o1[0] ** 2 - o2[0] ** 2 - 1 * (2 * (o1[1] - o2[1]))) / (2 * (o1[0] - o2[0]))
        x2 = (r2 ** 2 - r1 ** 2 + o1[1] ** 2 - o2[1] ** 2 + o1[0] ** 2 - o2[0] ** 2 - 2 * (2 * (o1[1] - o2[1]))) / (2 * (o1[0] - o2[0]))

        d1 = (x1, 1)
        d2 = (x2, 2)
    else:
        y1  = (r2 ** 2 - r1 ** 2 + o1[1] ** 2 - o2[1] ** 2 + o1[0] ** 2 - o2[0] ** 2 - 1 * (2 * (o1[0] - o2[0]))) / (2 * (o1[1] - o2[1]))
        y2 = (r2 ** 2 - r1 ** 2 + o1[1] ** 2 - o2[1] ** 2 + o1[0] ** 2 - o2[0] ** 2 - 2 * (2 * (o1[0] - o2[0]))) / (2 * (o1[1] - o2[1]))

        d1 = (1, y1)
        d2 = (2, y2)

    return line_and_circle_cross(d1, d2, o1, r1)

n = int(input())
dots = list()

for _ in range(n):
    x, y = map(int, input().split())
    dots.append((x,y))


def geron(a, b, c):
    ab = dist(a, b)
    bc = dist(b, c)
    ac = dist(a, c)

    p = (ab + bc + ac) / 2

    return math.sqrt(p * (p - ab) * (p - bc) * (p - ac))

def tringle_in_triangle(dots):
    triangles = list(combinations(dots, 3))
    for a, b, c in triangles:
        for d in dots:
            if d in[a, b, c]:
                continue

            if math.isclose(geron(a, b, c), geron(a, b, d) + geron(a, d, c) + geron(d, b, c)):
                return True
            
    return False

print(tringle_in_triangle(dots))