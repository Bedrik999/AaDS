import math
from math import pi


class Angle:
    def __init__(self, value=0, is_degrees=False):
        self._original_value = value
        self._is_degrees = is_degrees
        if is_degrees:
            self._radians = math.radians(value)
        else:   
            self._radians = value
    
    def _normalize(self, value=None):
        if value is None:
            value = self._radians
        two_pi = 2 * math.pi
        normalized = value % two_pi
        if normalized < 0:
            normalized += two_pi
        return normalized
    
    @property 
    def radians(self):
        return self._radians
    
    @radians.setter 
    def radians(self, value):
        self._radians = value
        self._original_value = value
        self._is_degrees = False
    
    @property
    def degrees(self):
        return math.degrees(self._radians)
    
    @degrees.setter
    def degrees(self, value):
        self._radians = math.radians(value)
        self._original_value = value
        self._is_degrees = True
    
    @property
    def normalized_radians(self):
        return self._normalize()
    
    @property
    def normalized_degrees(self):
        return math.degrees(self._normalize())
    
    def __float__(self):
        return float(self._radians)
    
    def __int__(self):
        return int(self._radians)
    
    def __str__(self):
        if self._is_degrees:
            return f"{self._original_value:.2f}° ({self._radians:.4f} rad)"
        else:
            return f"{math.degrees(self._radians):.2f}° ({self._radians:.4f} rad)"
        
    def __repr__(self):
        return f"Angle({self._radians})"
    
    def __eq__(self, other):
        if isinstance(other, Angle):
            return math.isclose(self._normalize(), other._normalize(), abs_tol=1e-10)
        elif isinstance(other, (int, float)):
            return math.isclose(self._normalize(), self._normalize(other), abs_tol=1e-10)
        return False
    
    def __lt__(self, other): 
        if isinstance(other, Angle):
            return self._normalize() < other._normalize()
        elif isinstance(other, (int, float)): 
            return self._normalize() < self._normalize(other) 
        return NotImplemented 
    
    def __le__(self, other): 
        if isinstance(other, Angle):
            return self._normalize() <= other._normalize()
        elif isinstance(other, (int, float)):
            return self._normalize() <= self._normalize(other)
        return NotImplemented
    
    def __add__(self, other):
        if isinstance(other, Angle):
            return Angle(self._normalize() + other._normalize())
        elif isinstance(other, (int, float)):
            return Angle(self._normalize() + other)
        return NotImplemented
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, Angle):
            return Angle(self._normalize() - other._normalize())
        elif isinstance(other, (int, float)):
            return Angle(self._normalize() - other)
        return NotImplemented
    
    def __rsub__(self, other): 
        if isinstance(other, (int, float)):
            return Angle(other - self._normalize())
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Angle(self._normalize() * other)
        return NotImplemented
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("деление угла на ноль")
            return Angle(self._normalize() / other)
        return NotImplemented



class AngleRange:
    eps = 1e-10

    def __init__(self, start, end,
                 start_inclusive=True,
                 end_inclusive=True):

        self.start = start if isinstance(start, Angle) else Angle(start)
        self.end = end if isinstance(end, Angle) else Angle(end)

        self.start_inclusive = start_inclusive
        self.end_inclusive = end_inclusive

    def _s(self):
        return self.start.normalized_radians

    def _e(self):
        return self.end.normalized_radians

    def _wraps(self):
        return self._s() > self._e()

    def _contains_point_rad(self, x):
        s = self._s()
        e = self._e()

        if not self._wraps():
            if s < x < e:
                return True
            if abs(x - s) <= self.eps:
                return self.start_inclusive
            if abs(x - e) <= self.eps:
                return self.end_inclusive
            return False
        else:
            if x > s or x < e:
                return True
            if abs(x - s) <= self.eps:
                return self.start_inclusive
            if abs(x - e) <= self.eps:
                return self.end_inclusive
            return False

    def __contains__(self, item):
        if isinstance(item, (int, float)):
            item = Angle(item)
        if isinstance(item, Angle):
            return self._contains_point_rad(item.normalized_radians)
        if isinstance(item, AngleRange):
            return (item.start in self) and (item.end in self)
        return False

    def _is_overlapping(self, other):
        if other.start in self:
            return True
        if other.end in self:
            return True
        if self.start in other:
            return True
        if self.end in other:
            return True
        return False

    def __add__(self, other):
        if isinstance(other, (int, float, Angle)):
            return [AngleRange(self.start + other,self.end + other,self.start_inclusive,self.end_inclusive)]
        if not isinstance(other, AngleRange):
            return NotImplemented
        if not self._is_overlapping(other):
            return [self, other]

        points = [
            (self._s(), self.start_inclusive),
            (self._e(), self.end_inclusive),
            (other._s(), other.start_inclusive),
            (other._e(), other.end_inclusive)
        ]
        points.sort(key=lambda x: x[0])
        new_start = Angle(points[0][0])
        new_end = Angle(points[-1][0])

        return [AngleRange(new_start,new_end,True,True)]

    def __sub__(self, other):
        if isinstance(other, (int, float, Angle)):
            return [AngleRange(self.start - other,
                               self.end - other,
                               self.start_inclusive,
                               self.end_inclusive)]

        if not isinstance(other, AngleRange):
            return NotImplemented

        if not self._is_overlapping(other):
            return [self]

        result = []

        s1 = self._s()
        e1 = self._e()
        s2 = other._s()
        e2 = other._e()

        if other.start in self and other.end in self:
            if abs(s1 - s2) <= self.eps and self.start_inclusive and not other.start_inclusive:
                result.append(AngleRange(self.start, self.start, True, True))
            if abs(e1 - e2) <= self.eps and self.end_inclusive and not other.end_inclusive:
                result.append(AngleRange(self.end, self.end, True, True))
            return result
        
        if other.start in self:
            result.append(AngleRange(self.start,other.start,self.start_inclusive,not other.start_inclusive))

        if other.end in self:
            result.append(AngleRange(other.end,self.end,not other.end_inclusive,self.end_inclusive))
        return result

    def __str__(self):
        left = "[" if self.start_inclusive else "("
        right = "]" if self.end_inclusive else ")"
        return f"{left}{self.start} - {self.end}{right}"

    def __repr__(self):
        return f"AngleRange({self.start}, {self.end}, {self.start_inclusive}, {self.end_inclusive})"


print('\n1. Создание и вывод:')
a_deg = Angle(90, is_degrees=True)
a_rad = Angle(pi / 2)
print(str(a_deg))
print(str(a_rad))

print('\n2.Cравнение:')
a1 = Angle(0)
a2 = Angle(2 * pi)
a3 = Angle(-4 * pi)
print('0° == 360° ?', a1 == a2)
print('0° == -720°?', a1 == a3)

print('\n3. Арифметические операции:')
c1 = Angle(30, is_degrees=True)
c2 = Angle(45, is_degrees=True)
print('30° + 45° =', str(c1 + c2))
print('30° + 1 рад ≈', str(c1 + 1.0))
print('45° - 30° =', str(c2 - c1))

print('\n4. Проверка вхождения диапазона в диапазон с исходными значениями:')
first_range = AngleRange(Angle(math.pi / 3, False), Angle(math.pi * 5, False), True, True)
second_range = AngleRange(Angle(math.pi / 6, False), Angle(math.pi * 6, False), True, True)
print(first_range, second_range)
print(first_range in second_range)
print(second_range in first_range)

print('\n5. Тест вычитания с разными границами:')
range1 = AngleRange(Angle(10, is_degrees=True), Angle(50, is_degrees=True), start_inclusive=True, end_inclusive=True)
range2 = AngleRange(Angle(10, is_degrees=True), Angle(50, is_degrees=True), start_inclusive=False, end_inclusive=False)

result = range1 - range2
print(f"[10°,50°] - (10°,50°) = {result}")
