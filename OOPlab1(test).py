import math
from math import pi

class Angle:

    def __init__(self, value=0, is_degrees=False):
        if is_degrees:
            self._radians = math.radians(value)
        else:   
            self._radians = self._normalize(value)
    
    def _normalize(self, angle):
        two_pi = 2 * math.pi
        normalized = angle % two_pi
        if normalized < 0:
            normalized += two_pi
        return normalized
    
    @property 
    def radians(self):
        return self._radians
    
    @radians.setter 
    def radians(self, value):
        self._radians = self._normalize(value)
    
    @property
    def degrees(self):
        return math.degrees(self._radians)
    
    @degrees.setter
    def degrees(self, value):
        self._radians = self._normalize(math.radians(value))
    
    def __float__(self):
        return float(self._radians)
    
    def __int__(self):
        return int(self._radians)
    
    def __str__(self):
        return f"{self.degrees:.2f}° ({self._radians:.4f} rad)"
    
    def __repr__(self):
        return f"Angle({self._radians})"
    
    def __eq__(self, other):
        if isinstance(other, Angle):
            return math.isclose(self._radians, other._radians, abs_tol=1e-10)
        elif isinstance(other, (int, float)):
            return math.isclose(self._radians, self._normalize(other), abs_tol=1e-10)
        return False
    
    def __lt__(self, other): 
        if isinstance(other, Angle):
            return self._radians < other._radians
        elif isinstance(other, (int, float)): 
            return self._radians < self._normalize(other) 
        return NotImplemented 
    
    def __le__(self, other): 
        if isinstance(other, Angle):
            return self._radians <= other._radians
        elif isinstance(other, (int, float)):
            return self._radians <= self._normalize(other)
        return NotImplemented
    
    def __add__(self, other):
        if isinstance(other, Angle):
            return Angle(self._radians + other._radians)
        elif isinstance(other, (int, float)):
            return Angle(self._radians + other)
        return NotImplemented
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, Angle):
            return Angle(self._radians - other._radians)
        elif isinstance(other, (int, float)):
            return Angle(self._radians - other)
        return NotImplemented
    
    def __rsub__(self, other): 
        if isinstance(other, (int, float)):
            return Angle(other - self._radians)
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Angle(self._radians * other)
        return NotImplemented
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Деление угла на ноль")
            return Angle(self._radians / other)
        return NotImplemented


class AngleRange:
    
    def __init__(self, start, end, start_inclusive=True, end_inclusive=True):
        if isinstance(start, (int, float)):
            self.start = Angle(start)

        elif isinstance(start, Angle):
            self.start = start
        else:
            raise TypeError("Начальная точка должна быть числом или Angle")
        
        if isinstance(end, (int, float)):
            self.end = Angle(end)
        elif isinstance(end, Angle):
            self.end = end
        else:
            raise TypeError("Конечная точка должна быть числом или Angle")
        
        self.start_inclusive = start_inclusive
        self.end_inclusive = end_inclusive
    
    def __str__(self): 
        start_bracket = "[" if self.start_inclusive else "("
        end_bracket = "]" if self.end_inclusive else ")"
        return f"{start_bracket}{self.start} - {self.end}{end_bracket}"
    
    def __repr__(self):
        return f"AngleRange({self.start._radians}, {self.end._radians}, {self.start_inclusive}, {self.end_inclusive})"
    
    def __eq__(self, other):
        if not isinstance(other, AngleRange):
            return False
        return (self.start == other.start and 
                self.end == other.end and 
                self.start_inclusive == other.start_inclusive and 
                self.end_inclusive == other.end_inclusive)
    
    def __abs__(self): 
        start_rad = self.start.radians
        end_rad = self.end.radians
        
        if end_rad >= start_rad:
            return end_rad - start_rad
        else:
            return 2 * math.pi - start_rad + end_rad
    
    def __contains__(self, item):
        if isinstance(item, (Angle, int, float)):
            if isinstance(item, (int, float)): 
                angle = Angle(item)
            else:
                angle = item
            
            angle_rad = angle.radians
            start_rad = self.start.radians
            end_rad = self.end.radians
            
            if start_rad <= end_rad:
                if start_rad < angle_rad < end_rad:
                    return True
                elif angle_rad == start_rad:
                    return self.start_inclusive 
                elif angle_rad == end_rad:
                    return self.end_inclusive
            else:
                if angle_rad >= start_rad or angle_rad <= end_rad:
                    if angle_rad > start_rad or angle_rad < end_rad: 
                        return True
                    elif angle_rad == start_rad:
                        return self.start_inclusive
                    elif angle_rad == end_rad:
                        return self.end_inclusive
            return False
        
        elif isinstance(item, AngleRange):
            return (item.start in self and item.end in self)
        
        return False
    
    def __add__(self, other):
        if not isinstance(other, AngleRange):
            return NotImplemented
        
        s1 = self.start.radians
        e1 = self.end.radians
        s2 = other.start.radians
        e2 = other.end.radians
        
        def are_connected_or_overlapping():
            if s1 <= e1 and s2 <= e2:
                if s2 <= e1 and e2 >= s1: 
                    return True
                if math.isclose(e1, s2, abs_tol=1e-10) or math.isclose(e2, s1, abs_tol=1e-10):  
                    return True
            else:
                intervals1 = []
                intervals2 = []
                
                if s1 <= e1:
                    intervals1.append((s1, e1))
                else:
                    intervals1.append((s1, 2 * math.pi))
                    intervals1.append((0, e1))
                
                if s2 <= e2:
                    intervals2.append((s2, e2))
                else:
                    intervals2.append((s2, 2 * math.pi))
                    intervals2.append((0, e2))
                
                for int1 in intervals1:
                    for int2 in intervals2:
                        if int2[0] <= int1[1] and int2[1] >= int1[0]:
                            return True
                        if math.isclose(int1[1], int2[0], abs_tol=1e-10) or math.isclose(int2[1], int1[0], abs_tol=1e-10):
                            return True
            return False
        
        if not are_connected_or_overlapping():
            return [self, other]
        
        points = []
        
        for start, end, start_inc, end_inc in [(s1, e1, self.start_inclusive, self.end_inclusive),
                                                (s2, e2, other.start_inclusive, other.end_inclusive)]:
            if start <= end:
                points.append((start, start_inc, 'start'))
                points.append((end, end_inc, 'end'))
            else:
                points.append((start, start_inc, 'start'))
                points.append((2 * math.pi, end_inc, 'end'))
                points.append((0, start_inc, 'start'))
                points.append((end, end_inc, 'end'))
        
        points.sort(key=lambda x: (x[0], 0 if x[2] == 'start' else 1))
        
        result_starts = []
        result_ends = []
        result_start_inclusive = []
        result_end_inclusive = []
        
        i = 0
        while i < len(points):
            current_start = points[i][0]
            current_start_inc = points[i][1]
            i += 1
         
            max_end = current_start
            max_end_inc = False
            count = 1
            
            while i < len(points) and count > 0:
                if points[i][2] == 'start':
                    count += 1
                else:
                    count -= 1
                    if count == 0:
                        max_end = points[i][0]
                        max_end_inc = points[i][1]
                i += 1
            
            result_starts.append(current_start)
            result_ends.append(max_end)
            result_start_inclusive.append(current_start_inc)
            result_end_inclusive.append(max_end_inc)
        
        if len(result_starts) == 1:
            return AngleRange(result_starts[0], result_ends[0], 
                            result_start_inclusive[0], result_end_inclusive[0])
        else:
            ranges = []
            for j in range(len(result_starts)):
                ranges.append(AngleRange(result_starts[j], result_ends[j],
                                        result_start_inclusive[j], result_end_inclusive[j]))
            return ranges
    
    def __sub__(self, other):
        """Вычитание диапазона углов из другого"""
        if not isinstance(other, AngleRange):
            return NotImplemented
        
        s1 = self.start.radians
        e1 = self.end.radians
        s2 = other.start.radians
        e2 = other.end.radians
        
        result_ranges = []
        
        self_intervals = []
        if s1 <= e1:
            self_intervals.append((s1, e1, self.start_inclusive, self.end_inclusive))
        else:
            self_intervals.append((s1, 2 * math.pi, self.start_inclusive, True))
            self_intervals.append((0, e1, True, self.end_inclusive))
        
        other_intervals = []
        if s2 <= e2:
            other_intervals.append((s2, e2, other.start_inclusive, other.end_inclusive))
        else:
            other_intervals.append((s2, 2 * math.pi, other.start_inclusive, True))
            other_intervals.append((0, e2, True, other.end_inclusive))
        
        for s_start, s_end, s_start_inc, s_end_inc in self_intervals:
            current_intervals = [(s_start, s_end, s_start_inc, s_end_inc)]
            
            for o_start, o_end, o_start_inc, o_end_inc in other_intervals:
                new_intervals = []
                
                for c_start, c_end, c_start_inc, c_end_inc in current_intervals:
                    if c_end < o_start - 1e-10 or c_start > o_end + 1e-10:
                        new_intervals.append((c_start, c_end, c_start_inc, c_end_inc))
                    else:
                        if c_start < o_start - 1e-10:
                            left_inc = c_start_inc
                            left_end = o_start
                            left_end_inc = not o_start_inc
                            new_intervals.append((c_start, left_end, left_inc, left_end_inc))
                        elif math.isclose(c_start, o_start, abs_tol=1e-10):
                            if c_start_inc and not o_start_inc:
                                new_intervals.append((c_start, c_start, True, True))
                        
                        if c_end > o_end + 1e-10:
                            right_start = o_end
                            right_start_inc = not o_end_inc
                            right_end = c_end
                            right_end_inc = c_end_inc
                            new_intervals.append((right_start, right_end, right_start_inc, right_end_inc))
                        elif math.isclose(c_end, o_end, abs_tol=1e-10):
                            if c_end_inc and not o_end_inc:
                                new_intervals.append((c_end, c_end, True, True))
                
                current_intervals = new_intervals
            
            for start, end, start_inc, end_inc in current_intervals:
                result_ranges.append(AngleRange(start, end, start_inc, end_inc))
        
        result_ranges = [r for r in result_ranges if r.start.radians <= r.end.radians + 1e-10]
        
        result_ranges.sort(key=lambda x: x.start.radians)
        
        merged_ranges = []
        for r in result_ranges:
            if not merged_ranges:
                merged_ranges.append(r)
            else:
                last = merged_ranges[-1]
                last_end = last.end.radians
                curr_start = r.start.radians
                
                if (math.isclose(last_end, curr_start, abs_tol=1e-10) and 
                    (last.end_inclusive or r.start_inclusive)):
                    new_range = AngleRange(
                        last.start.radians,
                        r.end.radians,
                        last.start_inclusive,
                        r.end_inclusive
                    )
                    merged_ranges[-1] = new_range
                else:
                    merged_ranges.append(r)
        
        if len(merged_ranges) == 0:
            return None
        elif len(merged_ranges) == 1:
            return merged_ranges[0]
        else:
            return merged_ranges

print('=' * 60)
print('DEMO: класс Angle')
print('=' * 60)

print('\n1. Создание и вывод:')
a_deg = Angle(90, is_degrees=True)
a_rad = Angle(pi / 2)
print('  Angle(90, is_degrees=True):', str(a_deg))
print('  Angle(pi/2):               ', str(a_rad))

print('\n2. Нормализация и сравнение (мод 2pi):')
a1 = Angle(0)
a2 = Angle(2 * pi)
a3 = Angle(-4 * pi)
print('0°  ->', str(a1))
print('360°->', str(a2))
print('-720°->', str(a3))
print('0° == 360° ?', a1 == a2)
print('0° == -720°?', a1 == a3)

print('\n  Сравнение по направлению (мод 2pi):')
b1 = Angle(10, is_degrees=True)
b2 = Angle(350, is_degrees=True)
print('  10° < 350° ?', b1 < b2)

print('\n3. Арифметические операции:')
c1 = Angle(30, is_degrees=True)
c2 = Angle(45, is_degrees=True)
print('30° + 45° =', str(c1 + c2))
print('30° + 1 рад ≈', str(c1 + 1.0))
print('45° - 30° =', str(c2 - c1))
print('45° * 2   =', str(c2 * 2))
print('45° / 2   =', str(c2 / 2))

print('\n4. Преобразования типов:')
a_mixed = Angle(150.7, is_degrees=True)
print('Угол:', a_mixed)
print('float(angle):', float(a_mixed), '(радианы)')
print('int(angle):  ', int(a_mixed), '(целая часть радиан)')

print('\n' + '=' * 60)
print('DEMO: класс AngleRange')
print('=' * 60)

# Вспомогательные функции для удобства тестирования
def make_range_deg(start_deg, end_deg, start_inclusive=True, end_inclusive=True):
    """Создание AngleRange из градусов"""
    return AngleRange(
        Angle(start_deg, is_degrees=True),
        Angle(end_deg, is_degrees=True),
        start_inclusive, end_inclusive
    )

def format_range_deg(range_obj):
    """Форматирование диапазона в градусах"""
    if range_obj is None:
        return "None"
    if isinstance(range_obj, list):
        return [format_range_deg(r) for r in range_obj]
    
    start_bracket = "[" if range_obj.start_inclusive else "("
    end_bracket = "]" if range_obj.end_inclusive else ")"
    start_deg = range_obj.start.degrees
    end_deg = range_obj.end.degrees
    
    if start_deg <= end_deg:
        return f"{start_bracket}{start_deg:.1f}°, {end_deg:.1f}°{end_bracket}"
    else:
        return f"{start_bracket}{start_deg:.1f}°, 360°) ∪ [0°, {end_deg:.1f}°{end_bracket}"

print('\n5. Создание диапазонов (в градусах для наглядности):')
r_std = make_range_deg(0, 90)
r_std2 = make_range_deg(90, 180)
r_wrap = make_range_deg(270, 90)
print('Обычный диапазон r_std:   ', format_range_deg(r_std))
print('Обычный диапазон r_std2:  ', format_range_deg(r_std2))
print('Wrap-around диапазон r_wrap:', format_range_deg(r_wrap))

print('\n6. Длина диапазона (abs):')
print('  |[0°, 90°]| =', abs(r_std), 'рад')
print('  |[270°, 90°]| =', abs(r_wrap), 'рад (ожидаем pi)')

print('\n7. Вхождение углов (Angle in AngleRange):')
r_all = make_range_deg(0, 360)
angle_45 = Angle(45, is_degrees=True)
angle_315 = Angle(315, is_degrees=True)
print('45°  in [0°, 90°]? ', angle_45 in r_std)
print('15° in [0°, 90°]? ', angle_315 in r_std)
print('315° in wrap [270°, 90°]?', angle_315 in r_wrap)

r_open = make_range_deg(0, 90, start_inclusive=False, end_inclusive=False)
angle_0 = Angle(0, is_degrees=True)
angle_90 = Angle(90, is_degrees=True)
print('(0°, 90°): 0°  внутри? ', angle_0 in r_open)
print('45° внутри? ', angle_45 in r_open)
print('90° внутри? ', angle_90 in r_open)

print('\n8. Вхождение диапазона в диапазон (Range in Range):')

outer_lin = make_range_deg(0, 180)
inner_lin_ok = make_range_deg(30, 60)
inner_lin_bad = make_range_deg(90, 270)
print('Линейный случай (оба без wrap):')
print('   ', format_range_deg(inner_lin_ok), 'внутри', format_range_deg(outer_lin), '?',
      inner_lin_ok in outer_lin)
print('   ', format_range_deg(inner_lin_bad), 'внутри', format_range_deg(outer_lin), '?',
      inner_lin_bad in outer_lin)

outer_circ = make_range_deg(90, -90)
inner_circ_ok = make_range_deg(90, 270)
inner_circ_bad = make_range_deg(30, 60)
print('\n  Круговой случай (есть wrap-around):')
print('   ', '[90°, 270°]', 'внутри', '[90°, -90°]', '?',
      inner_circ_ok in outer_circ)
print('   ', '[30°, 60°]', 'внутри', '[90°, -90°]', '?',
      inner_circ_bad in outer_circ)
print('   ', '[10°, 20°]', 'внутри', '(10°, 20°]', '?',
      make_range_deg(10, 20, True, True) in
      make_range_deg(10, 20, False, True))

print('\n9. Сложение диапазонов:')

r_a = make_range_deg(120, 200, True, False)
r_b = make_range_deg(150, 240, True, False)
sum1 = r_a + r_b
print('Пересекающиеся дуги:')
print('   ', format_range_deg(r_a), '+', format_range_deg(r_b), '=>',
      format_range_deg(sum1))

r_c = make_range_deg(0, 45)
r_d = make_range_deg(90, 135)
sum2 = r_c + r_d
print('Непересекающиеся дуги:')
print('   ', format_range_deg(r_c), '+', format_range_deg(r_d), '=>',
      format_range_deg(sum2))

r_wrap1 = make_range_deg(270, 30)
r_wrap2 = make_range_deg(300, 90)
sum3 = r_wrap1 + r_wrap2
print('Сложение wrap-around дуг:')
print('   ', format_range_deg(r_wrap1), '+', format_range_deg(r_wrap2), '=>',
      format_range_deg(sum3))

print('\n10. Вычитание диапазонов:')

base = make_range_deg(0, 180)
cut_middle = make_range_deg(45, 135, False, True)
diff1 = base - cut_middle
print('Вычитаем середину из [0°, 180°]:')
print('   ', format_range_deg(base), '-', format_range_deg(cut_middle), '=>',
      format_range_deg(diff1))

base_wrap = make_range_deg(270, 90)
cut_wrap = make_range_deg(300, 30)
diff2 = base_wrap - cut_wrap
print('Вычитание wrap-around диапазона из wrap-around:')
print('   ', format_range_deg(base_wrap), '-', format_range_deg(cut_wrap), '=>',
      format_range_deg(diff2))

base2 = make_range_deg(0, 180)
cut_point = make_range_deg(90, 90)
diff3 = base2 - cut_point
print('Вычитаем точку [90°,90°] из [0°,180°]:')
print('   ', format_range_deg(base2), '-', format_range_deg(cut_point), '=>',
      format_range_deg(diff3))

print('\nДополнительный тест:')
result = make_range_deg(10, 50, True, True) - make_range_deg(10, 50, False, False)
print('[10°,50°] - (10°,50°) =', format_range_deg(result))
