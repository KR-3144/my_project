# -*- coding: utf-8 -*-
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(SCRIPT_DIR, "history.txt")


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Деление на ноль невозможно!")
    return a / b


def get_number(prompt):
    while True:
        raw = input(prompt).strip().replace(",", ".")
        if raw == "":
            print("Ошибка: введена пустая строка. Повторите ввод.")
            continue
        try:
            return float(raw)
        except ValueError:
            print("Ошибка: это не число. Введите число, например 5 или 3.14")


def get_operation_choice():
    while True:
        raw = input("Выберите операцию: ").strip()
        if raw in ("0", "1", "2", "3", "4", "5", "6"):
            return raw
        print("Ошибка: нет такой команды. Введите число из списка меню.")


def format_number(value):
    if value == int(value):
        return str(int(value))
    return str(round(value, 10))


def save_to_history(expression, result):
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {expression} = {result}\n")


def read_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f if line.strip()]


def show_history():
    records = read_history()
    print()
    print("=" * 50)
    if not records:
        print("История пуста: вы ещё не выполнили ни одной операции.")
    else:
        print(f"ИСТОРИЯ ОПЕРАЦИЙ (всего записей: {len(records)})")
        print("-" * 50)
        for line in records:
            print(line)
    print("=" * 50)


def clear_history():
    confirm = input("Вы уверены, что хотите удалить всю историю? (да/нет): ").strip().lower()
    if confirm in ("да", "д", "y", "yes"):
        open(HISTORY_FILE, "w", encoding="utf-8").close()
        print("История очищена.")
    else:
        print("Отмена: история сохранена.")


def perform_operation(choice):
    num1 = get_number("Введите первое число: ")
    num2 = get_number("Введите второе число: ")

    operations = {
        "1": (add, "+"),
        "2": (subtract, "-"),
        "3": (multiply, "*"),
        "4": (divide, "/"),
    }

    func, sign = operations[choice]
    result = func(num1, num2)
    expression = f"{format_number(num1)} {sign} {format_number(num2)}"
    record = f"{expression} = {format_number(result)}"
    print(f"Результат: {record}")
    return record


def run():
    print("=" * 50)
    print("      КОНСОЛЬНЫЙ КАЛЬКУЛЯТОР С ИСТОРИЕЙ")
    print("=" * 50)
    print("Доступные операции:")
    print("  1 - Сложение")
    print("  2 - Вычитание")
    print("  3 - Умножение")
    print("  4 - Деление")
    print("  5 - Показать историю операций")
    print("  6 - Очистить историю")
    print("  0 - Выход")
    print("=" * 50)

    while True:
        print()
        choice = get_operation_choice()

        try:
            if choice == "0":
                print("Работа завершена. Спасибо за использование калькулятора!")
                break
            elif choice in ("1", "2", "3", "4"):
                record = perform_operation(choice)
                parts = record.split(" = ")
                save_to_history(parts[0], parts[1])
                print("Операция сохранена в историю.")
            elif choice == "5":
                show_history()
            elif choice == "6":
                clear_history()
        except ZeroDivisionError as error:
            print("Ошибка:", error)
            print("Попробуйте другое число.")
        except KeyboardInterrupt:
            print("\nРабота прервана пользователем.")
            break


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nРабота прервана пользователем.")
