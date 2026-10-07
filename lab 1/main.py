import logging
import sys
import os
from triangle import classify_triangle

os.makedirs("logs", exist_ok=True)

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/file_txt.log", encoding="utf-8")
    ]
)


def run_test(label: str, a: str, b: str, c: str) -> None:
    logging.info(f"{label}")
    logging.debug(f"Параметры: side_a='{a}', side_b='{b}', side_c='{c}'")

    try:
        tri_type, coords = classify_triangle(a, b, c)

        logging.info(
            f"Параметры: a='{a}', b='{b}', c='{c}'. Результат: тип='{tri_type}', вершины={coords}")

        print(f"\n {label}")
        print(f"Тип: {tri_type} | Вершины: {coords}")

    except Exception as e:

        logging.error(f"Неуспешный запрос. Параметры: a='{a}', b='{b}', c='{c}'")

        print(f"\n ошибка {label}: {e}")


if __name__ == "__main__":

    run_test("Равносторонний треугольник", "5", "5", "5")
    run_test("Разносторонний треугольник", "3", "4", "5")

    run_test("Нарушено неравенство треугольника", "1", "2", "10")
    run_test("Отрицательная сторона", "-3", "4", "5")

    run_test("Нечисловые данные", "abc", "4", "5")
    run_test("", "0.1", "0.2", "0.3")