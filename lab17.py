class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def parse_tree_string(tree_str):
    
    def parse_subtree(s, index):
        if index >= len(s) or s[index] == ',' or s[index] == ')':
            return None, index
        
        # Пропускаем пробелы
        while index < len(s) and s[index] == ' ':
            index += 1
            
        # Извлекаем значение узла
        value_str = ''
        while index < len(s) and s[index].isdigit():
            value_str += s[index]
            index += 1
        
        if not value_str:
            return None, index
        
        node = TreeNode(int(value_str))
        
        # Пропускаем пробелы
        while index < len(s) and s[index] == ' ':
            index += 1
            
        # Если следующий символ '(', значит есть дети
        if index < len(s) and s[index] == '(':
            node.left, index = parse_subtree(s, index + 1)
            
            # Пропускаем пробелы перед запятой
            while index < len(s) and s[index] == ' ':
                index += 1
                
            if index < len(s) and s[index] == ',':
                index += 1
                
            node.right, index = parse_subtree(s, index)
            
            # Пропускаем пробелы перед закрывающей скобкой
            while index < len(s) and s[index] == ' ':
                index += 1
                
            if index < len(s) and s[index] == ')':
                index += 1
        
        return node, index
    
    root, _ = parse_subtree(tree_str, 0)
    return root

def search_node(root, value):
    """Поиск узла в бинарном дереве поиска"""
    current = root
    while current is not None:
        if value == current.value:
            return True
        elif value < current.value:
            current = current.left
        else:
            current = current.right
    return False

def insert_node(root, value):
    """Добавление узла в бинарное дерево поиска"""
    new_node = TreeNode(value)
    
    if root is None:
        return new_node
    
    current = root
    parent = None
    
    while current is not None:
        parent = current
        if value < current.value:
            current = current.left
        elif value > current.value:
            current = current.right
        else:
            # Значение уже существует в дереве
            print(f"Значение {value} уже существует в дереве!")
            return root
    
    # Определяем, куда вставить новый узел
    if value < parent.value:
        parent.left = new_node
    else:
        parent.right = new_node
    
    print(f"Значение {value} успешно добавлено в дерево!")
    return root

def delete_node(root, value):
    """Удаление узла из бинарного дерева поиска"""
    if root is None:
        print(f"Значение {value} не найдено в дереве!")
        return root
    
    current = root
    parent = None
    
    # Поиск удаляемого узла и его родителя
    while current is not None and current.value != value:
        parent = current
        if value < current.value:
            current = current.left
        else:
            current = current.right
    
    # Узел не найден
    if current is None:
        print(f"Значение {value} не найдено в дереве!")
        return root
    
    # Случай 1: У удаляемого узла нет потомков
    if current.left is None and current.right is None:
        if current == root:
            root = None
        elif parent.left == current:
            parent.left = None
        else:
            parent.right = None
    
    # Случай 2: У удаляемого узла один потомок
    elif current.left is None:
        if current == root:
            root = current.right
        elif parent.left == current:
            parent.left = current.right
        else:
            parent.right = current.right
    
    elif current.right is None:
        if current == root:
            root = current.left
        elif parent.left == current:
            parent.left = current.left
        else:
            parent.right = current.left
    
    # Случай 3: У удаляемого узла два потомка
    else:
        # Находим наименьший узел в правом поддереве (преемник)
        successor_parent = current
        successor = current.right
        
        while successor.left is not None:
            successor_parent = successor
            successor = successor.left
        
        # Заменяем значение удаляемого узла значением преемника
        current.value = successor.value
        
        # Удаляем преемника
        if successor_parent.left == successor:
            successor_parent.left = successor.right
        else:
            successor_parent.right = successor.right
    
    print(f"Значение {value} успешно удалено из дерева!")
    return root

def tree_to_string(root):
    """Преобразует дерево обратно в линейно-скобочную запись"""
    if root is None:
        return ""
    
    result = str(root.value)
    
    if root.left is not None or root.right is not None:
        result += "(" + tree_to_string(root.left) + ", " + tree_to_string(root.right) + ")"
    
    return result

def print_tree_structure(node, level=0, prefix="Root: "):
    """Вспомогательная функция для визуализации структуры дерева"""
    if node is not None:
        print(" " * (level * 4) + prefix + str(node.value))
        if node.left is not None or node.right is not None:
            print_tree_structure(node.left, level + 1, "L--- ")
            print_tree_structure(node.right, level + 1, "R--- ")

def display_menu():
    """Отображает меню операций"""
    print("\n" + "="*50)
    print("          ОПЕРАЦИИ НАД БИНАРНЫМ ДЕРЕВОМ ПОИСКА")
    print("="*50)
    print("1. Поиск вершины")
    print("2. Добавление вершины") 
    print("3. Удаление вершины")
    print("4. Показать структуру дерева")
    print("5. Выход")
    print("="*50)

def main():
    # Ввод дерева
    print("Введите бинарное дерево в линейно-скобочной записи:")
    print("Пример: 8 (3 (1, 6 (4,7)), 10 (, 14(13,)))")
    
    tree_input = input("Ввод: ").strip()
    
    # Парсим строку и строим дерево
    root = parse_tree_string(tree_input)
    
    print("\nДерево успешно построено!")
    print("Структура дерева:")
    print_tree_structure(root)
    
    # Основной цикл меню
    while True:
        display_menu()
        choice = input("Выберите операцию (1-5): ").strip()
        
        if choice == '1':
            # Поиск вершины
            try:
                value = int(input("Введите значение для поиска: "))
                if search_node(root, value):
                    print(f"✓ Значение {value} найдено в дереве!")
                else:
                    print(f"✗ Значение {value} не найдено в дереве!")
            except ValueError:
                print("Ошибка: введите целое число!")
                
        elif choice == '2':
            # Добавление вершины
            try:
                value = int(input("Введите значение для добавления: "))
                root = insert_node(root, value)
            except ValueError:
                print("Ошибка: введите целое число!")
                
        elif choice == '3':
            # Удаление вершины
            try:
                value = int(input("Введите значение для удаления: "))
                root = delete_node(root, value)
            except ValueError:
                print("Ошибка: введите целое число!")
                
        elif choice == '4':
            # Показать структуру дерева
            print("\nТекущая структура дерева:")
            print_tree_structure(root)
            
        elif choice == '5':
            # Выход
            break
            
        else:
            print("Неверный выбор! Пожалуйста, выберите операцию от 1 до 5.")
    
    # Вывод итогового дерева перед завершением
    print("\n" + "="*50)
    print("ИТОГОВОЕ ДЕРЕВО:")
    print("="*50)
    print("Линейно-скобочная запись:")
    final_tree_str = tree_to_string(root)
    print(final_tree_str)
    
    print("\nГрафическое представление:")
    print_tree_structure(root)
    
    print("\nПрограмма завершена. До свидания!")

if __name__ == "__main__":
    main()