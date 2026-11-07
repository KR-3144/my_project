from datetime import datetime
from pathlib import Path
import math

HISTORY_FILE = Path(__file__).with_name("history.txt")


def get_number(prompt):
    """Запрашивает число, заменяет запятую на точку, повторяет при ошибке."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("Ввод не должен быть пустым. Попробуйте ещё раз.")
            continue
        value = raw.replace(",", ".")
        try:
            number = float(value)
        except ValueError:
            print("Некорректное число. Попробуйте ещё раз.")
            continue
        if not math.isfinite(number):
            print("Слишком большое число. Попробуйте ещё раз.")
            continue
        return number


def format_number(number):
    """Показывает целые числа без лишней десятичной части."""
    if number == int(number):
        return str(int(number))
    return str(number)


def save_to_history(operation, result):
    """Дописывает операцию с датой и временем в history.txt."""
    try:
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        line = f"{timestamp} | {operation} = {format_number(result)}"
        with HISTORY_FILE.open("a", encoding="utf-8") as file:
            file.write(line + "\n")
    except OSError:
        print("Не удалось записать историю вычислений.")


def read_history():
    """Читает историю; если файла нет, возвращает пустой список."""
    try:
        with HISTORY_FILE.open("r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []
    except OSError:
        print("Не удалось прочитать историю вычислений.")
        return []


def main():
    """Меню, словарь операций и главный цикл программы."""
    print("=== Консольный калькулятор ===")
    operations = {
        "1": ("Сложение", "+", lambda a, b: a + b),
        "2": ("Вычитание", "-", lambda a, b: a - b),
        "3": ("Умножение", "*", lambda a, b: a * b),
        "4": ("Деление", "/", lambda a, b: a / b),
    }
    while True:
        print()
        print("1 - сложение")
        print("2 - вычитание")
        print("3 - умножение")
        print("4 - деление")
        print("5 - история вычислений")
        print("0 - выход")
        choice = input("Выберите действие: ").strip()

        if choice == "0":
            print("Работа калькулятора завершена.")
            break
        if choice == "5":
            history = read_history()
            if not history:
                print("История пока пуста.")
            else:
                print("--- История вычислений ---")
                for record in history:
                    print(record)
            continue
        if choice not in operations:
            print("Такого пункта меню нет. Выберите действие ещё раз.")
            continue

        name, symbol, action = operations[choice]
        a = get_number("Введите первое число: ")
        b = get_number("Введите второе число: ")
        if choice == "4" and b == 0:
            print("На ноль делить нельзя. Выберите действие ещё раз.")
            continue
        result = action(a, b)
        expression = f"{format_number(a)} {symbol} {format_number(b)}"
        print(f"Результат: {expression} = {format_number(result)}")
        save_to_history(expression, result)


if __name__ == "__main__":
    main()
