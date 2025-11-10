import math

class Angle:
    #если is_degrees передаем радианы, иначе градусы
    #внутри храним все в радинах для единства и удобства(все стандартные функции в python работают в радинах)
    def __init__(self, value=0, is_degrees=False):
        # Инициализация угла: по умолчанию в радианах, можно задать в градусах
        if is_degrees:
            # Преобразование градусов в радианы
            #создаем поле класаа _radians, _ значит что это внутренняя пременная и не предназначена для внешнего использования
            self._radians = math.radians(value)
        else:   
            # Нормализация угла в диапазон [0, 2π)
            self._radians = self._normalize(value)
    
    def _normalize(self, angle):
        # 2pi = 360 градусов
        two_pi = 2 * math.pi
        # Приведение угла к диапазону [0, 2π) делением на 360 град
        normalized = angle % two_pi
        # Обеспечение неотрицательности
        if normalized < 0:
            normalized += two_pi
        return normalized
    
    @property #превращаем метод в свойство 
    #позволяет использовать геттер без скобок как атрибут класса
    def radians(self):
        #Геттер для получения угла в радианах
        return self._radians
    
    @radians.setter 
    def radians(self, value):
        #Сеттер для установки угла в радианах
        self._radians = self._normalize(value)
    
    @property
    def degrees(self):
        #Геттер для получения угла в градусах
        return math.degrees(self._radians)
    
    @degrees.setter
    def degrees(self, value):
        #Сеттер для установки угла в градусах
        self._radians = self._normalize(math.radians(value))
    
    def __float__(self): #магический метод
        #Преобразование к float (в радианах)
        return float(self._radians)
    
    def __int__(self):
        #Преобразование к int (в радианах)
        return int(self._radians)
    
    def __str__(self):
        #Строковое представление для пользователя, так нужен для print
        return f"{self.degrees:.2f}° ({self._radians:.4f} rad)"
        #:.2f оставляет две цифры после запятой, а :.4f - 4 цифры
    
    def __repr__(self):
        #Строковое представление для разработчика(отладки)
        return f"Angle({self._radians})"
    
    def __eq__(self, other): #магический метод который вызывается при ==
        #Проверка равенства углов с учетом периодичности
        if isinstance(other, Angle): #Проверяем, является ли other объектом класса Angle
            # Сравнение двух углов
            return math.isclose(self._radians, other._radians, abs_tol=1e-10)#abs_tol=1e-10 - допустимая погрешность (0.0000000001 радиан)
        elif isinstance(other, (int, float)):
            # Сравнение с числом (представляем число в радианах)
            return math.isclose(self._radians, self._normalize(other), abs_tol=1e-10)
        return False
    
    def __lt__(self, other):
        """Проверка меньше ли текущий угол"""
        if isinstance(other, Angle):
            return self._radians < other._radians
        elif isinstance(other, (int, float)):
            return self._radians < self._normalize(other)
        return NotImplemented
    
    def __le__(self, other):
        """Проверка меньше или равен текущий угол"""
        if isinstance(other, Angle):
            return self._radians <= other._radians
        elif isinstance(other, (int, float)):
            return self._radians <= self._normalize(other)
        return NotImplemented
    
    def __add__(self, other):
        """Сложение углов или с числом (в радианах)"""
        if isinstance(other, Angle):
            # Сложение двух углов
            return Angle(self._radians + other._radians)
        elif isinstance(other, (int, float)):
            # Сложение с числом (в радианах)
            return Angle(self._radians + other)
        return NotImplemented
    
    def __radd__(self, other):
        """Правое сложение"""
        return self.__add__(other)
    
    def __sub__(self, other):
        """Вычитание углов или числа (в радианах)"""
        if isinstance(other, Angle):
            # Вычитание двух углов
            return Angle(self._radians - other._radians)
        elif isinstance(other, (int, float)):
            # Вычитание числа (в радианах)
            return Angle(self._radians - other)
        return NotImplemented
    
    def __rsub__(self, other):
        """Правое вычитание"""
        if isinstance(other, (int, float)):
            return Angle(other - self._radians)
        return NotImplemented
    
    def __mul__(self, other):
        """Умножение угла на число"""
        if isinstance(other, (int, float)):
            return Angle(self._radians * other)
        return NotImplemented
    
    def __rmul__(self, other):
        """Правое умножение"""
        return self.__mul__(other)
    
    def __truediv__(self, other):
        """Деление угла на число"""
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Деление угла на ноль")
            return Angle(self._radians / other)
        return NotImplemented


class AngleRange:
    """Класс для представления промежутков углов"""
    
    def __init__(self, start, end, start_inclusive=True, end_inclusive=True):
        # Преобразование начальной точки в Angle если необходимо
        if isinstance(start, (int, float)):
            self.start = Angle(start)
        elif isinstance(start, Angle):
            self.start = start
        else:
            raise TypeError("Начальная точка должна быть числом или Angle")
        
        # Преобразование конечной точки в Angle если необходимо
        if isinstance(end, (int, float)):
            self.end = Angle(end)
        elif isinstance(end, Angle):
            self.end = end
        else:
            raise TypeError("Конечная точка должна быть числом или Angle")
        
        # Флаги включения границ
        self.start_inclusive = start_inclusive
        self.end_inclusive = end_inclusive
    
    def __str__(self):
        """Строковое представление для пользователя"""
        start_bracket = "[" if self.start_inclusive else "("
        end_bracket = "]" if self.end_inclusive else ")"
        return f"{start_bracket}{self.start} - {self.end}{end_bracket}"
    
    def __repr__(self):
        """Строковое представление для разработчика"""
        return f"AngleRange({self.start._radians}, {self.end._radians}, {self.start_inclusive}, {self.end_inclusive})"
    
    def __eq__(self, other):
        """Проверка эквивалентности промежутков"""
        if not isinstance(other, AngleRange):
            return False
        return (self.start == other.start and 
                self.end == other.end and 
                self.start_inclusive == other.start_inclusive and 
                self.end_inclusive == other.end_inclusive)
    
    def __abs__(self):
        """Длина промежутка в радианах"""
        start_rad = self.start.radians
        end_rad = self.end.radians
        
        if end_rad >= start_rad:
            return end_rad - start_rad
        else:
            # Учет перехода через 2π
            return 2 * math.pi - start_rad + end_rad
    
    def __contains__(self, item):
        """Проверка вхождения угла или промежутка"""
        if isinstance(item, (Angle, int, float)):
            # Проверка вхождения угла
            if isinstance(item, (int, float)):
                angle = Angle(item)
            else:
                angle = item
            
            angle_rad = angle.radians
            start_rad = self.start.radians
            end_rad = self.end.radians
            
            if start_rad <= end_rad:
                # Обычный случай без перехода через 2π
                if start_rad < angle_rad < end_rad:
                    return True
                elif angle_rad == start_rad:
                    return self.start_inclusive
                elif angle_rad == end_rad:
                    return self.end_inclusive
            else:
                # Случай с переходом через 2π
                if angle_rad >= start_rad or angle_rad <= end_rad:
                    if angle_rad > start_rad or angle_rad < end_rad:
                        return True
                    elif angle_rad == start_rad:
                        return self.start_inclusive
                    elif angle_rad == end_rad:
                        return self.end_inclusive
            return False
        
        elif isinstance(item, AngleRange):
            # Проверка вхождения промежутка в промежуток
            # Упрощенная реализация - проверяем границы
            return (item.start in self and item.end in self)
        
        return False
    
    def __add__(self, other):
        """Сложение промежутков (объединение)"""
        if not isinstance(other, AngleRange):
            return NotImplemented
        
        # Упрощенная реализация - возвращаем список промежутков
        return [self, other]
    
    def __sub__(self, other):
        """Вычитание промежутков (разность)"""
        if not isinstance(other, AngleRange):
            return NotImplemented
        
        # Упрощенная реализация - возвращаем список промежутков
        return [self]


# Демонстрация работоспособности
if __name__ == "__main__":
    print("=== Демонстрация класса Angle ===")
    
    # Создание углов разными способами
    angle1 = Angle(math.pi)  # 180 градусов в радианах
    angle2 = Angle(90, is_degrees=True)  # 90 градусов
    angle3 = Angle(3 * math.pi)  # 540 градусов, нормализуется до 180
    
    print(f"angle1: {angle1}")
    print(f"angle2: {angle2}")
    print(f"angle3: {angle3}")
    
    # Проверка сравнения
    print(f"\nangle1 == angle3: {angle1 == angle3}")  # Должно быть True
    print(f"angle1 == 3.14159: {angle1 == 3.14159}")  # Должно быть True
    
    # Арифметические операции
    angle_sum = angle1 + angle2
    angle_diff = angle1 - angle2
    angle_mult = angle2 * 2
    angle_div = angle1 / 2
    
    print(f"\nangle1 + angle2: {angle_sum}")
    print(f"angle1 - angle2: {angle_diff}")
    print(f"angle2 * 2: {angle_mult}")
    print(f"angle1 / 2: {angle_div}")
    
    # Преобразования
    print(f"\nfloat(angle2): {float(angle2):.4f}")
    print(f"int(angle2): {int(angle2)}")
    print(f"str(angle2): {str(angle2)}")
    print(f"repr(angle2): {repr(angle2)}")
    
    print("\n=== Демонстрация класса AngleRange ===")
    
    # Создание промежутков
    range1 = AngleRange(0, math.pi)  # [0, π]
    range2 = AngleRange(Angle(math.pi/2), Angle(3*math.pi/2))  # [π/2, 3π/2]
    range3 = AngleRange(Angle(300, is_degrees=True), Angle(60, is_degrees=True), 
                       start_inclusive=True, end_inclusive=False)
    
    print(f"range1: {range1}")
    print(f"range2: {range2}")
    print(f"range3: {range3}")
    
    # Длины промежутков
    print(f"\nДлина range1: {abs(range1):.4f} радиан")
    print(f"Длина range2: {abs(range2):.4f} радиан")
    print(f"Длина range3: {abs(range3):.4f} радиан")
    
    # Проверка вхождения
    test_angle = Angle(45, is_degrees=True)
    print(f"\n{test_angle} в range1: {test_angle in range1}")
    print(f"{test_angle} в range2: {test_angle in range2}")
    
    # Сравнение промежутков
    range4 = AngleRange(0, math.pi)
    print(f"\nrange1 == range4: {range1 == range4}")
    print(f"range1 == range2: {range1 == range2}")
    
    # Операции с промежутками
    print(f"\nrange1 + range2: {range1 + range2}")
    print(f"range1 - range2: {range1 - range2}")
    
    print("\n=== Дополнительные тесты ===")
    
    # Тест нормализации
    big_angle = Angle(5 * math.pi)  # 900 градусов
    print(f"Angle(5π) нормализован: {big_angle}")
    
    # Тест отрицательного угла
    neg_angle = Angle(-math.pi/2)  # -90 градусов
    print(f"Angle(-π/2) нормализован: {neg_angle}")
    
    # Тест граничных случаев
    zero_angle = Angle(0)
    full_circle = Angle(2 * math.pi)
    print(f"Angle(0): {zero_angle}")
    print(f"Angle(2π): {full_circle}")
    print(f"0 == 2π: {zero_angle == full_circle}")
