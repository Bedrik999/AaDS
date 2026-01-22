import json # импортируем модуль для работы с json форматом
from enum import Enum # импортируем класс Enum для создания перечислений цветов

# испольщзуем enum как некий простой список
#используем ansi коды для задания цвета
class Color(Enum):
    RESET = "\033[0m" # reset-сброс. Позволяет указывать что дальше использование этого цвета не нужно
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m" # пурпурный
    CYAN = "\033[36m" # голубой

class Printer:
    @staticmethod # испльзуем декораток - "этот метод не нуждается в объекте класса"
    def load_font(path: str) -> dict: # объявляем метод, path - путь к файлу тип строка, ->dict - метод будет возвращать словарь
        # котекстный менеджер with, гарантирует что файл будет закрыт
        with open(path, "r", encoding="utf8") as f:
            return json.load(f) # читаем json из файла f. Вернет словарь    

    @staticmethod
    #рисует текст большими сиволами в консоли
    #нижним подчеркиванием говорим что метод приватный
    def _render_text(text: str, x: int, y: int, symbol: str, font: dict) -> None:
        #text - что печатаем; x,y - координаты; symbol - каким символом будем печатать; font - словарь со шрифтом.
        print("\n" * (y - 1), end="") #вертикальное позиционирование нашего текста 
        height = len(next(iter(font.values()))) # font.values() — все значения словаря шрифта; iter(font.values()) — создает итератор объект для последовательного доступа
        # next(...) — берет первый элемент; len(...) — длина списка = высота символа
        # позволяет нам узнать высоту любого шрифта (5, 7, 10 строк) без знания его структуры
        for row in range(height): #для font5 итераций будет 5
            print(" " * (x - 1), end="") # горизонтальное позиционирование
            for ch in text:#цикл по символам текста
                if ch in font:
                    line = font[ch][row].replace("*", symbol)
                    #font[ch] — список строк для символа ch; font[ch][row] — конкретная строка row; .replace("*", symbol) — заменяет '*' на нужный символ
                    print(line, end=" ") #печататем строку, end добавит пробел меж букв
            print() # переход на новую строку

    @classmethod
    #метод для вывода текста в консоль
    def print(cls, text: str, color: Color, position: tuple[int, int],
              symbol: str, font: dict) -> None:
        x, y = position #распаковка нашего котежа
        print(color.value, end="") #установка цвета
        cls._render_text(text, x, y, symbol, font) #т.к. это классовый метод, испольщуем cls
        print(Color.RESET.value, end="") #сбрасывает текст к стандартному иначе весь текст будет цветным

    def __init__(self, color: Color, position: tuple[int, int], 
                 symbol: str, font: dict): # конструктор
        self.color = color
        self.position = position
        self.symbol = symbol
        self.font = font

    def __enter__(self): # метод для автоматической настройки при работе с блоком with
        print(self.color.value, end="")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # сбрасываем цвет чтобы гарантировать, что после блока with консоль вернется в нормальное состояние, даже если внутри была ошибка
        print(Color.RESET.value, end="")

    def print_(self, text: str) -> None:
        x, y = self.position
        self._render_text(text, x, y, self.symbol, self.font)


font5 = Printer.load_font("font5.json")
font7 = Printer.load_font("font7.json")
#cтатический метод
Printer.print(text="HELLO", color=Color.MAGENTA, position=(2, 2), symbol="#", font=font5)
#метод экземляра 
with Printer(color=Color.CYAN, position=(10, 2), symbol="?", font=font7) as pr:
    pr.print_("NIGGA")
