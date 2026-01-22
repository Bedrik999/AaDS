from dataclasses import dataclass, field
from typing import Optional, Protocol, TypeVar, Sequence, List, Generic
#Optional - либо T, либо None.TypeVar/Generic - может хранить любой тип данных.
import pickle # сохранить объект в файл/восстановить его обратно
import os #для работы с файловой системой

#класс для хранения информации о пользователе
@dataclass(order=True)#order=True - автоматически создаются методы <,>,<=,=>
class User:
    name: str # по имени пользователя мы разрешаем сравнение по остальным объектам запрещено
    id: int = field(compare=False)
    login: str = field(compare=False)
    password: str = field(repr=False, compare=False) #repr - запрещаем строковое представление пароля. То есть при вызове принта покажется None. Нужно это для безопастности данных пользователя
    email: Optional[str] = field(default=None, compare=False) #default-None. Если значение не передали то по умолчанию будет None
    address: Optional[str] = field(default=None, compare=False)


T = TypeVar("T") #переменная которая может стать любым типом данныха
#CRUD-Create, read, update, delete  
#создаем интерфейс
class DataRepositoryProtocol(Protocol[T]):#protocol - любой класс, который реализует эти методы считается репозиторием
    def get_all(self) -> Sequence[T]: #возвращает все элементы хранилища. Sequence-общий тип(список,кортеж,и т.д.)
        ...
    def get_by_id(self, id: int) -> T | None: #ищет по id
        ...
    def add(self, item: T) -> None: #добавляет объект в хранилище
        ...
    def update(self, item: T) -> None: #обновляет существующий объект
        ...
    def delete(self, item: T) -> None: #удаляет объект из хранилища
        ...

#интерфес репозитория который знает что такое User
class UserRepositoryProtocol(DataRepositoryProtocol[User], Protocol):#наследуем от DataRepositoryProtocol - обычный репозитория плюс умеет работать с пользователем
    #[User] - T ->User (фиксируем T)
    def get_by_login(self, login: str) -> User | None: #поиск пользователя по логину
        ...

#универсальное хранилище данных,работает с любым типом данных
class DataRepository(Generic[T], DataRepositoryProtocol[T]): #Genetic-работает с обобщ типом данных.DataRepositoryProtocol-обязуется реализовать все методы CRUD
    def __init__(self, filename: str):
        self.filename = filename
        self._data: List[T] = self._load() #self_data-список элементов Т например User
        #self_load - инициализируем _data знач которые возвращ _load

    def _load(self) -> List[T]:#загруж данные из файла
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "rb") as f: #rb - бинарный режим чтения
            return pickle.load(f) #pickle читает байты из файла и восстанавливает python объекты

    def _save(self) -> None:    
        with open(self.filename, "wb") as f: #wb - бинарная запись
            pickle.dump(self._data, f)

    def get_all(self) -> List[T]:
        return list(self._data) #создаем копию дата,защищая дата из вне

    def get_by_id(self, id: int) -> T | None: #поиск по id
        for item in self._data:
            if getattr(item, "id", None) == id:
                return item
        return None

    def add(self, item: T) -> None:
        self._data.append(item)#добав в дату
        self._save()#сразу сохраняем в файл

    def update(self, item: T) -> None:#ищем равные айди и обнавляем данные
        for i, existing in enumerate(self._data):
            if getattr(existing, "id", None) == getattr(item, "id", None):
                self._data[i] = item
                self._save()
                return

    def delete(self, item: T) -> None:
        self._data = [x for x in self._data if x != item] #ищет объкт по равенству а не по id
        self._save()

#поиск юзера по логину
class UserRepository(DataRepository[User], UserRepositoryProtocol):
    def get_by_login(self, login: str) -> User | None: 
        for user in self._data:
            if user.login == login:
                return user
        return None



class AuthServiceProtocol(Protocol):
    def sign_in(self, user: User) -> None: #регистрация
        ...
    def sign_out(self) -> None: #выход из системы
        ...
    def is_authorized(self) -> bool: #проверка если пользователь уже авторизован
        ...
    def current_user(self) -> User | None: #возвращ тек польз
        ...



class AuthService(AuthServiceProtocol):
    def __init__(self, auth_file: str, user_repo: UserRepositoryProtocol):
        self.auth_file = auth_file #путь к файлу
        self.user_repo = user_repo #репозиторий пользователя
        self._current_user: User | None = None # текущий авторизованный пользователь
        self._auto_login() #автоматически авторизовывает пользователя при запуске программы

    def _auto_login(self): 
        if os.path.exists(self.auth_file):
            with open(self.auth_file, "rb") as f:
                user_id = pickle.load(f) #считываем ID пользователя, который был авторизован ранее
                self._current_user = self.user_repo.get_by_id(user_id) #ищем объект User по этому ID в репозитории

    def sign_in(self, user: User) -> None:
        self._current_user = user #сохраняем пользователя
        with open(self.auth_file, "wb") as f:
            pickle.dump(user.id, f) #сохраянем только ID пользоавтеля

    def sign_out(self) -> None:
        self._current_user = None 
        if os.path.exists(self.auth_file):
            os.remove(self.auth_file) #если файл существует удаляем его

    def is_authorized(self) -> bool: 
        return self._current_user is not None

    def current_user(self) -> User | None:
        return self._current_user


# =========================================================
# 8. Демонстрация работы системы
# =========================================================

def main():
    users_repo = UserRepository("users.db")
    auth_service = AuthService("auth.db", users_repo)

    # Добавление пользователей
    if not users_repo.get_all():
        print("Добавляем пользователей...")
        users_repo.add(User(1, "Иван", "ivan", "123", "ivan@mail.com"))
        users_repo.add(User(2, "Анна", "anna", "qwerty"))

    # Просмотр пользователей
    print("\nВсе пользователи (сортировка по имени):")
    for user in sorted(users_repo.get_all()):
        print(user)

    # Авторизация
    print("\nАвторизация пользователя ivan")
    user = users_repo.get_by_login("ivan")
    auth_service.sign_in(user)
    print("Текущий пользователь:", auth_service.current_user())

    # Смена пользователя
    print("\nСмена пользователя на anna")
    auth_service.sign_out()
    auth_service.sign_in(users_repo.get_by_login("anna"))
    print("Текущий пользователь:", auth_service.current_user())

    # Автоматическая авторизация
    print("\nИмитируем повторный запуск программы")
    auth_service2 = AuthService("auth.db", users_repo)
    print("Автоматически авторизован:", auth_service2.current_user())


if __name__ == "__main__":
    main()
