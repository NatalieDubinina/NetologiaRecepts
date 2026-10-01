import pprint


# =====================================================================
# ЗАДАЧА №1: Функция для чтения кулинарной книги
# =====================================================================
def read_cook_book(file_path: str) -> dict:
    """
    Читает файл с рецептами и возвращает словарь cook_book.
    """
    cook_book = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                dish_name = line.strip()
                if not dish_name:
                    continue

                try:
                    ingredients_count = int(file.readline().strip())
                except ValueError:
                    continue

                ingredients_list = []

                for _ in range(ingredients_count):
                    ingredient_line = file.readline().strip()
                    name, quantity, measure = ingredient_line.split(' | ')

                    ingredients_list.append({
                        'ingredient_name': name.strip(),
                        'quantity': int(quantity.strip()),
                        'measure': measure.strip()
                    })

                cook_book[dish_name] = ingredients_list
                file.readline()  # Пропускаем пустую строку-разделитель

    except FileNotFoundError:
        print(f"Ошибка: Не удалось найти файл '{file_path}' в папке проекта.")

    return cook_book


# =====================================================================
# ЗАДАЧА №2: Функция для подсчета ингредиентов на количество персон
# =====================================================================
def get_shop_list_by_dishes(dishes: list, person_count: int, cook_book: dict) -> dict:
    """
    Формирует словарь с необходимыми ингредиентами и их количеством на число персон.
    """
    shop_list = {}

    for dish in dishes:
        if dish in cook_book:
            for ingredient in cook_book[dish]:
                name = ingredient['ingredient_name']
                total_quantity = ingredient['quantity'] * person_count

                # Суммируем ингредиенты, если они повторяются
                if name in shop_list:
                    shop_list[name]['quantity'] += total_quantity
                else:
                    shop_list[name] = {
                        'measure': ingredient['measure'],
                        'quantity': total_quantity
                    }
        else:
            print(f"Предупреждение: Блюда '{dish}' нет в кулинарной книге.")

    return shop_list


# =====================================================================
# ЗАДАЧА №3: Функция для сортировки и слияния файлов
# =====================================================================
def merge_files(file_names: list, result_file_name: str):
    """
    Считывает файлы из списка, сортирует их по количеству строк
    и объединяет в один результирующий файл со служебной информацией.
    """
    files_data = []

    # Шаг 1: Читаем каждый файл и считаем количество строк
    for name in file_names:
        try:
            with open(name, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                files_data.append({
                    'filename': name,
                    'lines_count': len(lines),
                    'content': lines
                })
        except FileNotFoundError:
            print(f"Предупреждение: Файл '{name}' не найден, пропускаем его.")

    # Шаг 2: Сортируем файлы по количеству строк (от меньшего к большему)
    files_data.sort(key=lambda x: x['lines_count'])

    # Шаг 3: Записываем всё в итоговый файл
    with open(result_file_name, 'w', encoding='utf-8') as result_file:
        for file_info in files_data:
            # Записываем служебные строки
            result_file.write(f"{file_info['filename']}\n")
            result_file.write(f"{file_info['lines_count']}\n")

            # Записываем содержимое
            for line in file_info['content']:
                result_file.write(line)

            # Проверяем перенос строки в конце файла
            if file_info['content'] and not file_info['content'][-1].endswith('\n'):
                result_file.write('\n')

    print(f"Успех! Файлы успешно объединены в '{result_file_name}'.")


# =====================================================================
# ГЛАВНАЯ УПРАВЛЯЮЩАЯ ФУНКЦИЯ
# =====================================================================
def main():
    # --- Тест Задачи №1 ---
    file_name = 'recipe.txt'
    my_cook_book = read_cook_book(file_name)

    if my_cook_book:
        print("=== ЗАДАЧА №1: КУЛИНАРНАЯ КНИГА ===")
        pprint.pprint(my_cook_book, sort_dicts=False, width=100)
        print("\n" + "="*50 + "\n")

        # --- Тест Задачи №2 ---
        test_dishes = ['Запеченный картофель', 'Омлет']
        shopping_list = get_shop_list_by_dishes(test_dishes, 2, my_cook_book)
        print("=== ЗАДАЧА №2: СПИСОК ПОКУПОК ===")
        pprint.pprint(shopping_list, sort_dicts=False, width=100)
        print("\n" + "="*50 + "\n")

    # --- Тест Задачи №3 ---
    print("=== ЗАДАЧА №3: ОБЪЕДИНЕНИЕ ФАЙЛОВ ===")
    files_to_merge = ['1.txt', '2.txt', '3.txt']
    output_file = 'result.txt'
    merge_files(files_to_merge, output_file)


if __name__ == '__main__':
    main()
