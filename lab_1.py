from math import pi, isclose
from typing import Self, Union

Number = Union[int, float]
AngleLike = Union['Angle', Number]
TWO_PI = 2 * pi
PI_DIVIDED_BY_180 = pi / 180
_180_DIVIDED_BY_PI = 180 / pi


class Angle:
    _rad: float  # no normalized: rad could be not in [0; 2*pi)

    def __init__(self, rad: Number = 0.0) -> None:
        if not isinstance(rad, Number):
            raise TypeError('Value must be Number')
        self._rad: float = rad

    # extra method
    @staticmethod
    def _normalize_rad(rad: Number) -> float:
        return float(rad) % TWO_PI  # rad will be in [0; 2*pi)

    # extra method
    def _normalize_angle(self) -> None:
        self.rad = self.rad % TWO_PI  # angle will be in [0; 2*pi)

    @classmethod
    def from_rad(cls, rad: Number) -> Self:
        if not isinstance(rad, Number):
            raise TypeError('Value must be Number')
        return cls(rad)

    @classmethod
    def from_degrees(cls, degrees: Number) -> Self:
        if not isinstance(degrees, Number):
            raise TypeError('Value must be Number')
        rad: float = degrees * PI_DIVIDED_BY_180
        return cls(rad)

    @property
    def rad(self) -> float:
        return self._rad

    @property
    def normalized_rad(self) -> float:
        return Angle._normalize_rad(self._rad)

    @rad.setter
    def rad(self, value: Number) -> None:
        if not isinstance(value, Number):
            raise TypeError('Value must be Number')
        self._rad = value

    @property
    def degrees(self) -> float:
        return self.normalized_rad * _180_DIVIDED_BY_PI

    @degrees.setter
    def degrees(self, degrees: Number) -> None:
        if not isinstance(degrees, Number):
            raise TypeError('Value must be Number')
        self._rad = degrees * PI_DIVIDED_BY_180

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Angle):
            return False
        self_normalized_rad = Angle._normalize_rad(self.rad)
        other_normalized_rad = Angle._normalize_rad(other.rad)
        return isclose(self_normalized_rad, other_normalized_rad)

    def __ne__(self, other: Self) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Angle):
            return NotImplemented
        self_normalized_rad = Angle._normalize_rad(self.rad)
        other_normalized_rad = Angle._normalize_rad(other.rad)
        return self_normalized_rad < other_normalized_rad

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Angle):
            return NotImplemented
        self_normalized_rad = Angle._normalize_rad(self.rad)
        other_normalized_rad = Angle._normalize_rad(other.rad)
        return self_normalized_rad <= other_normalized_rad

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Angle):
            return NotImplemented
        self_normalized_rad = Angle._normalize_rad(self.rad)
        other_normalized_rad = Angle._normalize_rad(other.rad)
        return self_normalized_rad > other_normalized_rad

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Angle):
            return NotImplemented
        self_normalized_rad = Angle._normalize_rad(self.rad)
        other_normalized_rad = Angle._normalize_rad(other.rad)
        return self_normalized_rad >= other_normalized_rad

    def __float__(self) -> float:
        return self._rad

    def __int__(self) -> int:
        return int(self.degrees)

    # extra method
    @staticmethod
    def _get_other_rad(other: AngleLike) -> float:
        if isinstance(other, Angle):
            return other.rad
        if isinstance(other, Number):
            return other
        raise TypeError(f'Unsupported type: {type(other)}. Only Angle instances are supported')

    def __add__(self, other: AngleLike) -> Self:
        other_rad = Angle._get_other_rad(other)
        return Angle.from_rad(self._rad + other_rad)

    def __radd__(self, other: AngleLike) -> Self:  # 3.14 + Angle.from_degrees(90)
        return self.__add__(other)

    def __iadd__(self, other: AngleLike) -> Self:  # Angle.from_degrees(90) += 3.14
        other_rad = Angle._get_other_rad(other)
        self._rad += other_rad
        return self

    def __sub__(self, other: AngleLike) -> Self:
        other_rad = Angle._get_other_rad(other)
        return Angle.from_rad(self._rad - other_rad)

    def __rsub__(self, other: AngleLike) -> Self:
        other_rad = Angle._get_other_rad(other)
        return Angle.from_rad(other_rad - self._rad)

    def __isub__(self, other: AngleLike) -> Self:
        other_rad = Angle._get_other_rad(other)
        self._rad -= other_rad
        return self

    def __mul__(self, other: Number) -> Self:
        other_rad = Angle._get_other_rad(other)
        return Angle.from_rad(self._rad * other_rad)

    def __rmul__(self, other: Number) -> Self:
        return self.__mul__(other)

    def __imul__(self, other: Number) -> Self:
        other_rad = Angle._get_other_rad(other)
        self._rad *= other_rad
        return self

    def __truediv__(self, other: Number) -> Self:
        if not isinstance(other, Number):
            raise TypeError(f'Value must be float or int')
        if other == 0:
            raise ValueError('Division by zero is not supported')
        return Angle.from_rad(self._rad / other)

    def __rtruediv__(self, other: Number) -> Self:
        return self.__truediv__(other)

    def __str__(self) -> str:
        return f'{self._rad:.6f} rad'

    def __repr__(self) -> str:
        return f'Angle({self._rad})'

    @staticmethod
    def format_angle(a: 'Angle') -> str:
        return f'{a.rad:.4f} rad ≈ {a.degrees:.1f}°'


class AngleRange:
    _start: AngleLike
    _end: AngleLike
    _start_inclusive: bool
    _end_inclusive: bool

    def __init__(self,
                 start: AngleLike = Angle(0.0),
                 end: AngleLike = Angle(0.0),
                 start_inclusive: bool = True,
                 end_inclusive: bool = True) -> None:
        self._start: Angle = self._to_angle(start)
        self._end: Angle = self._to_angle(end)
        self._start_inclusive: bool = start_inclusive
        self._end_inclusive: bool = end_inclusive

    @staticmethod
    def _to_angle(value: AngleLike) -> Angle:
        if isinstance(value, Angle):
            return value
        if isinstance(value, Number):
            return Angle.from_rad(value)
        raise TypeError(f'Value must be Angle, int or float, got {type(value)}')

    @classmethod
    def from_rad(cls,
                 start: AngleLike,
                 end: AngleLike,
                 start_inclusive: bool = True,
                 end_inclusive: bool = True) -> Self:
        return cls(start, end, start_inclusive, end_inclusive)

    @classmethod
    def from_degrees(cls,
                     start: AngleLike,
                     end: AngleLike,
                     start_inclusive: bool = True,
                     end_inclusive: bool = True) -> Self:
        start_angle = Angle.from_degrees(start) if isinstance(start, Number) else start
        end_angle = Angle.from_degrees(end) if isinstance(end, Number) else end
        return cls(start_angle, end_angle, start_inclusive, end_inclusive)

    @property
    def start(self) -> Angle:
        return self._start

    @start.setter
    def start(self, value: AngleLike) -> None:
        self._start = self._to_angle(value)

    @property
    def end(self) -> Angle:
        return self._end

    @end.setter
    def end(self, value: AngleLike) -> None:
        self._end = self._to_angle(value)

    @property
    def start_inclusive(self) -> bool:
        return self._start_inclusive

    @start_inclusive.setter
    def start_inclusive(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f'Value must be boolean, got {type(value)}')
        self._start_inclusive = value

    @property
    def end_inclusive(self) -> bool:
        return self._end_inclusive

    @end_inclusive.setter
    def end_inclusive(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f'Value must be float or int, got {type(value)}')
        self._end_inclusive = value

    @property
    def start_rad(self) -> float:
        return self._start.rad

    @start_rad.setter
    def start_rad(self, rad: Number) -> None:
        if not isinstance(rad, Number):
            raise TypeError(f'Value must be float or int, got {type(rad)}')
        self._start = Angle.from_rad(rad)

    @property
    def end_rad(self) -> float:
        return self._end.rad

    @end_rad.setter
    def end_rad(self, rad: Number) -> None:
        if not isinstance(rad, Number):
            raise TypeError(f'Value must be float or int, got {type(rad)}')
        self._end = Angle.from_rad(rad)

    @property
    def start_degrees(self) -> float:
        return self._start.degrees

    @start_degrees.setter
    def start_degrees(self, degrees: Number) -> None:
        if not isinstance(degrees, Number):
            raise TypeError(f'Value must be float or int, got {type(degrees)}')
        self._start = Angle.from_degrees(degrees)

    @property
    def end_degrees(self) -> float:
        return self._end.degrees

    @end_degrees.setter
    def end_degrees(self, degrees: Number) -> None:
        if not isinstance(degrees, Number):
            raise TypeError(f'Value must be float or int, got {type(degrees)}')
        self._end = Angle.from_degrees(degrees)

    @property
    def wraps_around(self) -> bool:
        return self._start.rad > self._end.rad

    def __abs__(self) -> float:
        if self.wraps_around:
            return (TWO_PI - self._start.rad) + self._end.rad
        return self._end.rad - self._start.rad

    def _raw_segments(self) -> list[tuple[float, float, bool, bool]]:
        s = self.start_rad
        e = self.end_rad
        return [(s, e, self._start_inclusive, self._end_inclusive)]

    @staticmethod
    def _point_in_segment(x: float, seg: tuple[float, float, bool, bool]) -> bool:
        s, e, inc_s, inc_e = seg
        if x < s or x > e:
            return False
        if isclose(x, s) and not inc_s:
            return False
        if isclose(x, e) and not inc_e:
            return False
        return True

    @staticmethod
    def _segment_inside(inner: tuple[float, float, bool, bool],
                        outer: tuple[float, float, bool, bool]) -> bool:
        s1, e1, inc_s1, inc_e1 = inner
        s2, e2, inc_s2, inc_e2 = outer

        if s1 < s2:
            return False
        if isclose(s1, s2) and inc_s1 and not inc_s2:
            return False

        if e1 > e2:
            return False
        if isclose(e1, e2) and inc_e1 and not inc_e2:
            return False

        return True

    def __repr__(self) -> str:
        return (f'AngleRange({self._start}, {self._end}, '
                f'start_inclusive={self._start_inclusive}, '
                f'end_inclusive={self._end_inclusive})')

    def __str__(self) -> str:
        start_bracket = '[' if self._start_inclusive else '('
        end_bracket = ']' if self._end_inclusive else ')'
        return f'{start_bracket}{self._start}, {self._end}{end_bracket}'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AngleRange):
            return NotImplemented
        if (self.wraps_around + other.wraps_around) >= 1:
            return (self._start == other._start and
                    self._end == other._end and
                    self._start_inclusive == other._start_inclusive and
                    self._end_inclusive == other._end_inclusive)
        same_start = isclose(self.start_rad, other.start_rad)
        same_end = isclose(self.end_rad, other.end_rad)
        return (same_start and same_end and
                self._start_inclusive == other._start_inclusive and
                self._end_inclusive == other._end_inclusive)

    def _ordered_pair(self) -> tuple[float, float]:  # tuple[float, float, bool, bool]
        return float(abs(self)), self.start_rad
        # return float(abs(self)), self.start_rad, self.start_inclusive, self.end_inclusive

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, AngleRange):
            return NotImplemented
        return self._ordered_pair() < other._ordered_pair()

    def __le__(self, other: object) -> bool:
        if not isinstance(other, AngleRange):
            return NotImplemented
        return self._ordered_pair() <= other._ordered_pair()

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, AngleRange):
            return NotImplemented
        return self._ordered_pair() > other._ordered_pair()

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, AngleRange):
            return NotImplemented
        return self._ordered_pair() >= other._ordered_pair()

    def __contains__(self, item: object) -> bool:
        if isinstance(item, Angle):
            x = item.normalized_rad
            return any(self._point_in_segment(x, seg) for seg in self._to_segments())

        if isinstance(item, AngleRange):
            if not self.wraps_around and not item.wraps_around:
                outer_segments = self._raw_segments()
                inner_segments = item._raw_segments()
            else:
                outer_segments = self._to_segments()
                inner_segments = item._to_segments()

            return all(
                any(self._segment_inside(inner, outer) for outer in outer_segments)
                for inner in inner_segments
            )

        return NotImplemented

    def _normalized_bounds(self) -> tuple[float, float]:
        return self._start.normalized_rad, self._end.normalized_rad

    def _to_segments(self) -> list[tuple[float, float, bool, bool]]:
        s, e = self._normalized_bounds()
        if s <= e:
            return [(s, e, self._start_inclusive, self._end_inclusive)]
        # wrap-around: [s, 2pi] U [0, e]
        return [(s, TWO_PI, self._start_inclusive, True),
                (0.0, e, True, self._end_inclusive)]

    @staticmethod
    def _segments_to_ranges(
            segments: list[tuple[float, float, bool, bool]]
    ) -> list['AngleRange']:
        return [AngleRange(s, e, inc_s, inc_e)
                for (s, e, inc_s, inc_e) in segments]

    def __add__(self, other: Self) -> list[Self]:
        if not isinstance(other, AngleRange):
            return NotImplemented

        segments = self._to_segments() + other._to_segments()
        segments.sort()

        merged: list[tuple[float, float, bool, bool]] = []
        current_s, current_e, current_inc_s, current_inc_e = segments[0]

        for s, e, inc_s, inc_e in segments[1:]:
            touch_or_overlap = (s < current_e or (isclose(s, current_e) and (current_inc_e or inc_s)))

            if touch_or_overlap:
                if e > current_e:
                    current_e, current_inc_e = e, inc_e
                elif isclose(e, current_e):
                    current_inc_e = current_inc_e or inc_e
            else:
                merged.append((current_s, current_e, current_inc_s, current_inc_e))
                current_s, current_e, current_inc_s, current_inc_e = s, e, inc_s, inc_e

        merged.append((current_s, current_e, current_inc_s, current_inc_e))

        return self._segments_to_ranges(merged)

    @staticmethod
    def _segments_disjoint(a: tuple[float, float, bool, bool],
                           b: tuple[float, float, bool, bool]) -> bool:
        a_start, a_end, inc_a_start, inc_a_end = a
        b_start, b_end, inc_b_start, inc_b_end = b

        if a_end < b_start:
            return True
        if isclose(a_end, b_start) and not (inc_a_end and inc_b_start):
            return True

        if a_start > b_end:
            return True
        if isclose(a_start, b_end) and not (inc_a_start and inc_b_end):
            return True

        return False

    @staticmethod
    def _subtract_one_segment(
            current: tuple[float, float, bool, bool],
            cutter: tuple[float, float, bool, bool]) -> list[tuple[float, float, bool, bool]]:
        if AngleRange._segments_disjoint(current, cutter):
            return [current]

        a_start, a_end, inc_a_start, inc_a_end = current
        b_start, b_end, inc_b_start, inc_b_end = cutter
        pieces: list[tuple[float, float, bool, bool]] = []

        left_exists = (a_start < b_start) or (isclose(a_start, b_start) and inc_a_start and not inc_b_start)
        if left_exists:
            pieces.append((a_start, b_start, inc_a_start, not inc_b_start))

        right_exists = (a_end > b_end) or (isclose(a_end, b_end) and inc_a_end and not inc_b_end)
        if right_exists:
            pieces.append((b_end, a_end, not inc_b_end, inc_a_end))

        return pieces

    def __sub__(self, other: Self) -> list[Self]:
        if not isinstance(other, AngleRange):
            return NotImplemented

        result_segments = self._to_segments()
        cutters = other._to_segments()

        for cutter in cutters:
            new_result: list[tuple[float, float, bool, bool]] = []
            for segment in result_segments:
                new_result.extend(self._subtract_one_segment(segment, cutter))
            result_segments = new_result
            if not result_segments:
                break

        return self._segments_to_ranges(result_segments)

    @staticmethod
    def format_range_deg(r: 'AngleRange') -> str:
        s = '[' if r.start_inclusive else '('
        e = ']' if r.end_inclusive else ')'
        return f'{s}{r.start_degrees:.0f}°, {r.end_degrees:.0f}°{e}'


print('=' * 60)
print('DEMO: класс Angle')
print('=' * 60)

print('\n1. Создание и вывод:')
a_deg = Angle.from_degrees(90)
a_rad = Angle.from_rad(pi / 2)
print('  Angle.from_degrees(90):', Angle.format_angle(a_deg))
print('  Angle.from_rad(pi/2):  ', Angle.format_angle(a_rad))

print('\n2. Нормализация и сравнение (мод 2pi):')
a1 = Angle.from_degrees(0)
a2 = Angle.from_degrees(360)
a3 = Angle.from_degrees(-720)
print('  0°  ->', Angle.format_angle(a1))
print('  360°->', Angle.format_angle(a2))
print('  -720°->', Angle.format_angle(a3))
print('  0° == 360° ?', a1 == a2)
print('  0° == -720°?', a1 == a3)

print('\n  Сравнение по направлению (мод 2pi):')
b1 = Angle.from_degrees(10)
b2 = Angle.from_degrees(350)
print('  10° <', '350° ?', b1 < b2)  # 10° < 350°

print('\n3. Арифметические операции:')
c1 = Angle.from_degrees(30)
c2 = Angle.from_degrees(45)
print('  30° + 45° =', Angle.format_angle(c1 + c2))
print('  30° + 1 рад ≈', Angle.format_angle(c1 + 1.0))
print('  45° - 30° =', Angle.format_angle(c2 - c1))
print('  45° * 2   =', Angle.format_angle(c2 * 2))
print('  45° / 2   =', Angle.format_angle(c2 / 2))

print('\n4. Преобразования типов:')
a_mixed = Angle.from_degrees(150.7)
print('  Угол:', a_mixed)
print('  float(angle):', float(a_mixed), '(радианы)')
print('  int(angle):  ', int(a_mixed), '(целые градусы)')

print('\n' + '=' * 60)
print('DEMO: класс AngleRange')
print('=' * 60)

print('\n5. Создание диапазонов (в градусах для наглядности):')
r_std = AngleRange.from_degrees(0, 90)  # [0°, 90°]
r_std2 = AngleRange.from_degrees(90, 180)  # [90°, 180°]
r_wrap = AngleRange.from_degrees(270, 90)  # [270°, 360°] U [0°, 90°]
print('  Обычный диапазон r_std:   ', AngleRange.format_range_deg(r_std))
print('  Обычный диапазон r_std2:  ', AngleRange.format_range_deg(r_std2))
print('  Wrap-around диапазон r_wrap:', AngleRange.format_range_deg(r_wrap),
      ' (дуга через 360°)')

print('\n6. Длина диапазона (abs):')
print('  |[0°, 90°]| =', abs(r_std), 'рад')
print('  |[270°, 90°]| =', abs(r_wrap), 'рад (ожидаем pi/2 * 2 = pi)')

print('\n7. Вхождение углов (Angle in AngleRange):')
r_all = AngleRange.from_degrees(0, 360)
angle_45 = Angle.from_degrees(45)
angle_315 = Angle.from_degrees(315)
print('  45°  in [0°, 90°]?       ', angle_45 in r_std)
print('  315° in [0°, 90°]?      ', angle_315 in r_std)
print('  315° in wrap [270°, 90°]?', angle_315 in r_wrap)

r_open = AngleRange.from_degrees(0, 90,
                                 start_inclusive=False,
                                 end_inclusive=False)
angle_0 = Angle.from_degrees(0)
angle_90 = Angle.from_degrees(90)
print('  (0°, 90°): 0°  внутри? ', angle_0 in r_open)
print('             45° внутри? ', angle_45 in r_open)
print('             90° внутри? ', angle_90 in r_open)

print('\n8. Вхождение диапазона в диапазон (Range in Range):')

outer_lin = AngleRange.from_degrees(0, 180)
inner_lin_ok = AngleRange.from_degrees(30, 60)
inner_lin_bad = AngleRange.from_degrees(90, 270)
print('  Линейный случай (оба без wrap):')
print('   ', AngleRange.format_range_deg(inner_lin_ok), 'внутри', AngleRange.format_range_deg(outer_lin), '?',
      inner_lin_ok in outer_lin)
print('   ', AngleRange.format_range_deg(inner_lin_bad), 'внутри', AngleRange.format_range_deg(outer_lin), '?',
      inner_lin_bad in outer_lin)

outer_circ = AngleRange.from_degrees(90, -90)  # wrap: [90°, 270°]
inner_circ_ok = AngleRange.from_degrees(90, 270)  # та же дуга
inner_circ_bad = AngleRange.from_degrees(30, 60)  # вне этой дуги
print('\n  Круговой случай (есть wrap-around):')
print('   ', '[90°, 270°]', 'внутри', '[90°, -90°]', '?',
      inner_circ_ok in outer_circ)
print('   ', '[30°, 60°]', 'внутри', '[90°, -90°]', '?',
      inner_circ_bad in outer_circ)
print('   ', '[10°, 20°]', 'внутри', '(10°, 20°]', '?',
      AngleRange.from_degrees(10, 20, True, True) in
      AngleRange.from_degrees(10, 20, False, True))

print('\n9. Сложение диапазонов:')

r_a = AngleRange.from_degrees(120, 200, True, False)
r_b = AngleRange.from_degrees(150, 240, True, False)
sum1 = r_a + r_b
print('  Пересекающиеся дуги:')
print('   ', AngleRange.format_range_deg(r_a), '+', AngleRange.format_range_deg(r_b), '=>',
      [AngleRange.format_range_deg(r) for r in sum1])

r_c = AngleRange.from_degrees(0, 45)
r_d = AngleRange.from_degrees(90, 135)
sum2 = r_c + r_d
print('  Непересекающиеся дуги:')
print('   ', AngleRange.format_range_deg(r_c), '+', AngleRange.format_range_deg(r_d), '=>',
      [AngleRange.format_range_deg(r) for r in sum2])

r_wrap1 = AngleRange.from_degrees(270, 30)  # [270°, 360°] U [0°, 30°]
r_wrap2 = AngleRange.from_degrees(300, 90)  # [300°, 360°] U [0°, 90°]
sum3 = r_wrap1 + r_wrap2
print('  Сложение wrap-around дуг:')
print('   ', AngleRange.format_range_deg(r_wrap1), '+', AngleRange.format_range_deg(r_wrap2), '=>',
      [AngleRange.format_range_deg(r) for r in sum3])

print('\n10. Вычитание диапазонов:')

base = AngleRange.from_degrees(0, 180)
cut_middle = AngleRange.from_degrees(45, 135, False, True)
diff1 = base - cut_middle
print('  Вычитаем середину из [0°, 180°]:')
print('   ', AngleRange.format_range_deg(base), '-', AngleRange.format_range_deg(cut_middle), '=>',
      [AngleRange.format_range_deg(r) for r in diff1])

base_wrap = AngleRange.from_degrees(270, 90)  # wrap
cut_wrap = AngleRange.from_degrees(300, 30)  # wrap
different2 = base_wrap - cut_wrap
print('  Вычитание wrap-around диапазона из wrap-around:')
print('   ', AngleRange.format_range_deg(base_wrap), '-', AngleRange.format_range_deg(cut_wrap), '=>',
      [AngleRange.format_range_deg(r) for r in different2])

base2 = AngleRange.from_degrees(0, 180)
cut_point = AngleRange.from_degrees(90, 90)  # точка
different3 = base2 - cut_point
print('  Вычитаем точку [90°,90°] из [0°,180°]:')
print('   ', AngleRange.format_range_deg(base2), '-', AngleRange.format_range_deg(cut_point), '=>',
      [AngleRange.format_range_deg(r) for r in different3])

print('\nДемонстрация завершена.')

# print(f'{range1:deg} - {range2:deg} = {(range1 - range2):deg}')

print(str(AngleRange.from_degrees(10, 50,True,True)-AngleRange.from_degrees(10, 50,False,False)))