from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, List #mодуль для аннотаций типов 
from dataclasses import dataclass # для автоматического создания классов данных

# Протокол EventHandler
TEventArgs = TypeVar('TEventArgs') # создание generic-параметра

#абстрактный класс. Generic[TEventArgs] - класс будет работать с любым типом аргументов события
class EventHandler(ABC, Generic[TEventArgs]):
    @abstractmethod
    def handle(self, sender: Any, args: TEventArgs) -> None: #sender -  кто вызвал событие; args - аргументы события
        pass

# это менеджер событий, который:
# хранит список подписчиков
# позволяет подписываться/отписываться через += и -=
# оповещает всех подписчиков при возникновении события
class Event(Generic[TEventArgs]):# generic - позволяет сделать класс обобщённым. Работает с каким то типом данных, тип будет указан позже
    def __init__(self):
        # привытный атрибут
        self._handlers: List[EventHandler[TEventArgs]] = [] #список объектов типа EventHandler[TEventArgs]
        #_handler - список подписчиков события 
    #магический метод, вызывается при +=. Отвечаает за подписки
    def __iadd__(self, handler: EventHandler[TEventArgs]) -> 'Event[TEventArgs]':
        if handler not in self._handlers: # предотвращает дублирование
            self._handlers.append(handler) # добавляем обработчик в список self._handlers
        # обязательно возвращаем self иначе при event += handler сломается ссылка на event
        return self
    
    def __isub__(self, handler: EventHandler[TEventArgs]) -> 'Event[TEventArgs]':
        if handler in self._handlers:
            self._handlers.remove(handler)
        return self
    
    #оповещение всех подписчиков
    def invoke(self, sender: Any, args: TEventArgs) -> None: #sender - кто вызвал событие; args - аргументы события
        for handler in self._handlers: # перебираем всех подписчиков в списке
            handler.handle(sender, args) 
    
    #делаем метод invoke callable.То есть -> self.property_changing.invoke(self, changing_args) => self.property_changing(self, changing_args)
    def __call__(self, sender: Any, args: TEventArgs) -> None:
        self.invoke(sender, args)

# роль маркера и базового типа
# объединяет все аргументы событий
# позволяет писать общий код
# делает иерархию логичной
class EventArgs:
    pass

#описывает информацию о событии. Отвечает на: какое именно свойство изменилось
@dataclass # датакласс автоматически создает __init__
class PropertyChangedEventArgs(EventArgs):
    property_name: str #объявление поля класса

# хранит всю информацию, необходимую для проверки изменения свойства до его выполнения
@dataclass
class PropertyChangingEventArgs(EventArgs):
    property_name: str
    old_value: Any
    new_value: Any
    can_change: bool = True #разрешено или запрещено изменение

# 
class PropertyChangingValidator(EventHandler[PropertyChangingEventArgs]):
    def handle(self, sender: Any, args: PropertyChangingEventArgs) -> None:
        #валидатор: проверяет и может отменить изменение
        print(f"[VALIDATOR] Проверка изменения свойства '{args.property_name}'")
        print(f"  Старое значение: {args.old_value}")
        print(f"  Новое значение: {args.new_value}")
        
        # примеры правил валидации
        if args.property_name == "age" and isinstance(args.new_value, int):
            if args.new_value < 0:
                print(" [ОТМЕНА] Возраст не может быть отрицательным!")  
                args.can_change = False
            elif args.new_value > 150:
                print(" [ОТМЕНА] Возраст не может быть больше 150!")     
                args.can_change = False
        
        elif args.property_name == "email" and isinstance(args.new_value, str):
            if "@" not in args.new_value:
                print(" [ОТМЕНА] Email должен содержать @!")             
                args.can_change = False
        
        elif args.property_name == "balance" and isinstance(args.new_value, (int, float)):
            if args.new_value < 0:
                print(" [ОТМЕНА] Баланс не может быть отрицательным!")   
                args.can_change = False
        
        if args.can_change:
            print(f"  [РАЗРЕШЕНО] Изменение свойства '{args.property_name}'")  

# подписывается на событие после изменения свойства и выводит информацию об успешном изменении в консоль
class PropertyChangedLogger(EventHandler[PropertyChangedEventArgs]):
    def handle(self, sender: Any, args: PropertyChangedEventArgs) -> None:
        #логгер: выводит информацию об изменении свойства
        print(f"[LOGGER] Свойство '{args.property_name}' объекта {type(sender).__name__} изменено") # args.property_name - имя изменённого свойства. type(sender).__name__ - имя класса объекта
        if hasattr(sender, args.property_name):  #hasattr - проверяет, есть ли у объекта такое свойство
            print(f"  Новое значение: {getattr(sender, args.property_name)}") #getattr - получает значение атрибута по имени строки

# добавляет объектам возможность реагировать на изменение своих свойств
class ObservableObject:
    def __init__(self):
        self.property_changing = Event[PropertyChangingEventArgs]() #ДО изменения свойства
        self.property_changed = Event[PropertyChangedEventArgs]() #ПОСЛЕ изменения свойства
    
    def _set_property(self, property_name: str, value: Any) -> None:
        #общий метод для установки свойств с событиями
        old_value = getattr(self, f"_{property_name}", None)
        
        # Событие ДО изменения (с валидацией)
        changing_args = PropertyChangingEventArgs(
            property_name=property_name,
            old_value=old_value,
            new_value=value
        )
        self.property_changing(self, changing_args)
        
        # если валидатор разрешил изменение
        if changing_args.can_change:
            # устанавливаем новое значение
            setattr(self, f"_{property_name}", value)
            
            # событие ПОСЛЕ изменения
            changed_args = PropertyChangedEventArgs(property_name=property_name)
            self.property_changed(self, changed_args)
        else:
            print(f"[INFO] Изменение свойства '{property_name}' отменено")

# первый класс с тремя полями: User
class User(ObservableObject):
    def __init__(self, name: str = "", email: str = "", age: int = 0):
        super().__init__()
        self._name = name
        self._email = email
        self._age = age
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        self._set_property("name", value)
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        self._set_property("email", value)
    
    @property
    def age(self) -> int:
        return self._age
    
    @age.setter
    def age(self, value: int) -> None:
        self._set_property("age", value)
    
    def __str__(self) -> str:
        return f"User(name='{self.name}', email='{self.email}', age={self.age})"

# второй класс с тремя полями: BankAccount
class BankAccount(ObservableObject):
    def __init__(self, account_number: str = "", owner: str = "", balance: float = 0.0):
        super().__init__()
        self._account_number = account_number
        self._owner = owner
        self._balance = balance
    
    @property
    def account_number(self) -> str:
        return self._account_number
    
    @account_number.setter
    def account_number(self, value: str) -> None:
        self._set_property("account_number", value)
    
    @property
    def owner(self) -> str:
        return self._owner
    
    @owner.setter
    def owner(self, value: str) -> None:
        self._set_property("owner", value)
    
    @property
    def balance(self) -> float:
        return self._balance
    
    @balance.setter
    def balance(self, value: float) -> None:
        self._set_property("balance", value)
    
    def __str__(self) -> str:
        return f"BankAccount(account='{self.account_number}', owner='{self.owner}', balance={self.balance:.2f})"

# демонстрация работы
def main():
    print("=== Демонстрация системы событий и валидации ===\n")
    
    # Создаем обработчики событий
    validator = PropertyChangingValidator()
    logger = PropertyChangedLogger()
    
    # 1. Демонстрация с User
    print("1. Тестирование класса User:")
    print("-" * 40)
    
    user = User("Иван", "ivan@mail.com", 25)
    
    # Подписываемся на события
    user.property_changing += validator
    user.property_changed += logger
    
    print(f"Создан: {user}")
    print()
    
    # Пытаемся изменить свойства
    print("Попытка изменить возраст на 30:")
    user.age = 30
    print()
    
    print("Попытка изменить возраст на -5 (невалидное значение):")
    user.age = -5
    print()
    
    print("Попытка изменить email без @:")
    user.email = "invalid-email"
    print()
    
    print("Попытка изменить email корректно:")
    user.email = "ivan.new@company.com"
    print()
    
    print(f"Итоговое состояние: {user}")
    print()
    
    # Отписываемся от событий
    user.property_changing -= validator
    user.property_changed -= logger
    
    # 2. Демонстрация с BankAccount
    print("\n2. Тестирование класса BankAccount:")
    print("-" * 40)
    
    account = BankAccount("1234567890", "Иван Иванов", 1000.0)
    
    # Подписываемся на события
    account.property_changing += validator
    account.property_changed += logger
    
    print(f"Создан: {account}")
    print()
    
    # Пытаемся изменить свойства
    print("Попытка изменить баланс на 1500:")
    account.balance = 1500.0
    print()
    
    print("Попытка установить отрицательный баланс:")
    account.balance = -100.0
    print()
    
    print("Попытка изменить владельца:")
    account.owner = "Петр Петров"
    print()
    
    print(f"Итоговое состояние: {account}")
    
    # 3. Демонстрация отписки
    print("\n3. Демонстрация отписки от событий:")
    print("-" * 40)
    
    account.property_changing -= validator
    account.property_changed -= logger
    
    print("После отписки (изменения не будут логироваться и валидироваться):")
    account.balance = 2000.0
    print(f"Баланс изменен на: {account.balance}")
    
    # 4. Демонстрация нескольких подписчиков
    print("\n4. Демонстрация нескольких подписчиков:")
    print("-" * 40)
    
    # Создаем второй логгер
    logger2 = PropertyChangedLogger()
    
    user.property_changed += logger
    user.property_changed += logger2
    
    print("Два логгера подписаны на одно событие:")
    user.name = "Новое Имя"
    print()
    
    print(f"Итоговый пользователь: {user}")

if __name__ == "__main__":
    main()