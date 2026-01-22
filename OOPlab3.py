from abc import ABC, abstractmethod # для работы в абстрактными классами 
from enum import Enum # импортируем класс Enum для создания перечислений цветов
from datetime import datetime # библиотека для работы со временем
import re # для регулярных выражений в ReLogFilter

#создаем класс(перечисление) для отслеживания уровня логирования
class LogLevel(Enum):
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


class LogFilterProtocol(ABC): #абстрактный класс
    @abstractmethod # помечаем что данный метод абстрактный
    # теперь любой класс наследующий от LogFilterProtocol обязан иметь метод match
    def match(self, log_level: LogLevel, text: str) -> bool:
        ... # можно заменить на pass

# LevelFilter помогает отфильтровать какие логи мы хотим видеть. Например если мы хотим найти ошибки то ставми фильтр Error и info и warn не показываются 
class LevelFilter(LogFilterProtocol): # наследование от абстрк класса
    def __init__(self, allowed_level: LogLevel): #allowed_level - какой уровень разрешен и указываем что должен быть объектом класса LogLevel
        self.allowed_level = allowed_level # создание атрибута

    def match(self, log_level: LogLevel, text: str) -> bool: # в данном фильтре text не используется,но другие фильтры могут использовать текст, а интерфейс должен быть един
        return log_level == self.allowed_level # сравниваем уровень проверяемого сообщения с уровнем разрешенного

# текстовый фильтр, Пример: db_filter = SimpleLogFilter("database"); db_filter.match(LogLevel.WARN, "Slow database query") -> True,т.к. есть database
class SimpleLogFilter(LogFilterProtocol):
    def __init__(self, pattern: str):
        self.pattern = pattern

    def match(self, log_level: LogLevel, text: str) -> bool: # log_level не используется
        return self.pattern in text # поиск слова/фразы в тексте

# фильтр на регулярные выражения
# регулярные выржения - формула/шаблон для поиска текста. Пример: найди мне слово в которой есть буква К и оно из трех букв
class ReLogFilter(LogFilterProtocol):
    def __init__(self, pattern: str):
        try:
            self.pattern = re.compile(pattern) # компилируем регулярное выражение для повышения производительности при повторном использовании
        except re.error: # сключение при невалидном регулярном выражении
            self.pattern = None 

    def match(self, log_level: LogLevel, text: str) -> bool:
        if self.pattern is None or not isinstance(text, str):
            return False
        return bool(self.pattern.search(text)) # ищем совпадение регулярки в тексте

#нужен для - все обработчики логов должны иметь метод handle() для обработки лог-сообщений
class LogHandlerProtocol(ABC):
    @abstractmethod
    def handle(self, log_level: LogLevel, text: str) -> None:
        ...
#выводит лог-сообщение в консоль
class ConsoleHandler(LogHandlerProtocol):
    def handle(self, log_level: LogLevel, text: str) -> None:
        print(text)

#сохраняет логи в файл, чтобы даже при выключении программы логи не терялись
class FileHandler(LogHandlerProtocol):
    def __init__(self, filename: str):
        self.filename = filename

    def handle(self, log_level: LogLevel, text: str) -> None:
        try:
            with open(self.filename, "a", encoding="utf-8") as file: # a - (append) добавление в конец файла
                file.write(text + "\n")
        except (PermissionError, FileNotFoundError, OSError): 
            pass
        # PermissionError - нет прав на запись
        # FileNotFoundError - путь не существует
        # OSError - диск полный/поврежден

#отправляет лог-сообщения по сети через сокеты. (Заглушка)
class SocketHandler(LogHandlerProtocol):
    def handle(self, log_level: LogLevel, text: str) -> None:
        print(f"[SOCKET] Отправка сообщения: {text}")

#обработчик для отправки логов в системный лог. (Заглушка)
class SyslogHandler(LogHandlerProtocol):
    def handle(self, log_level: LogLevel, text: str) -> None:
        print(f"[SYSLOG] {text}")

#обработчик для записи логов на FTP сервер. (Заглушка)
class FtpHandler(LogHandlerProtocol):
    def handle(self, log_level: LogLevel, text: str) -> None:
        print(f"[FTP] Запись лога: {text}")

#все форматтеры должны иметь метод format() для преобразования лог-сообщений
class LogFormatterProtocol(ABC):
    @abstractmethod
    def format(self, log_level: LogLevel, text: str) -> str:
        ...

#форматтер который добавляет к тексту Artyom
class ArtyomLogFormatter(LogFormatterProtocol):
    def format(self, log_level: LogLevel, text: str) -> str:
        return f"(Artyom) {text}"

#основной форматтер
class DefaultLogFormatter(LogFormatterProtocol):
    def __init__(self, time_format: str = "%Y.%m.%d %H:%M:%S"):
        self.time_format = time_format

    def format(self, log_level: LogLevel, text: str) -> str:
        current_time = datetime.now().strftime(self.time_format) # datetime.now() - возвращает текущую дату и время;.strftime(self.time_format)-преобразует дату/время в строку по указанному формату
        return f"[{log_level.value}] [{current_time}] {text}"

# класс который принимает все фильтры форматтеры и обработчики
class Logger:
    def __init__(
        self,
        log_filters: list[LogFilterProtocol],
        log_formatters: list[LogFormatterProtocol],
        log_handlers: list[LogHandlerProtocol]
    ):
        self.filters = log_filters
        self.formatters = log_formatters
        self.handlers = log_handlers

    def log(self, log_level: LogLevel, text: str) -> None:
        # проходим все фильтры если любой фильтр вернет False -> сообщение отбрасывается
        for log_filter in self.filters:
            if not log_filter.match(log_level, text):
                return
        # применяем все форматеры последовательно
        for formatter in self.formatters:
            text = formatter.format(log_level, text)
        # применяем все обработчики последовательно 
        for handler in self.handlers:
            handler.handle(log_level, text)

    def log_info(self, text: str) -> None:
        self.log(LogLevel.INFO, text)

    def log_warn(self, text: str) -> None:
        self.log(LogLevel.WARN, text)

    def log_error(self, text: str) -> None:
        self.log(LogLevel.ERROR, text)

filters = [
    LevelFilter(LogLevel.WARN),
    SimpleLogFilter("error"),
    # ReLogFilter("adgasdgsa['///asdsak/\\")
]

formatters = [
    DefaultLogFormatter("%d.%m.%Y %H:%M:%S"),
    ArtyomLogFormatter()
]

handlers = [
    ConsoleHandler(),
    FileHandler("result.log"),
    SyslogHandler(),
    FtpHandler()
]

logger = Logger(filters, formatters, handlers)

logger.log_info("this is info message")
logger.log_warn("warning without error")
logger.log_error("critical error happened")
