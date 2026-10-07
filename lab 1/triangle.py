import math
import logging

def scale_to_canvas(points: list, canvas_size: int = 100, padding: int = 5) -> list:

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = max_x - min_x
    height = max_y - min_y
    usable = canvas_size - 2 * padding

    if max(width, height) == 0:
        center = canvas_size // 2
        return [(center, center)]

    scale = usable / max(width, height)

    result = []
    for x, y in points:
        nx = int(round(padding + (x - min_x) * scale))
        ny = int(round(padding + (y - min_y) * scale))
        nx = max(0, min(canvas_size - 1, nx))
        ny = max(0, min(canvas_size - 1, ny))
        result.append((nx, ny))
    return result

def classify_triangle(side_a_str: str, side_b_str: str, side_c_str:str) -> tuple:

    ERR_COORDS = [(-1, -1), (-1, -1), (-1, -1)]
    INV_COORDS = [(-2, -2), (-2, -2), (-2, -2)]

    try:
        a = float(side_a_str)
        b = float(side_b_str)
        c = float(side_c_str)
    except (ValueError, TypeError) as e:
        logging.warning(f"Неуспешный запрос. Параметры: a='{side_a_str}', b='{side_b_str}', c='{side_c_str}'. Нечисловые данные ({e}).")
        return "", INV_COORDS

    logging.debug(f"числа a={a}, b={b}, c={c}")

    if a <= 0 or b <= 0 or c <= 0:
        logging.warning((f"Неуспешный запрос. Параметры: a={a}, b={b}, c={c}. Стороны должны быть > 0."))
        return "не треугольник", ERR_COORDS

    epsilon = 1e-9
    if (a + b <= c + epsilon) or (a + c <= b + epsilon) or (b + c <= a + epsilon):
        logging.warning(
            f"Неуспешный запрос. Параметры: a={a}, b={b}, c={c}. Ошибка: нарушено неравенство треугольника.")
        return "не треугольник", ERR_COORDS

    if math.isclose(a, b, rel_tol=1e-9) or math.isclose(b, c, rel_tol=1e-9):
        tri_type = "равносторонний"
    elif math.isclose(a, b, rel_tol=1e-9) or math.isclose(b, c, rel_tol=1e-9) or math.isclose(a, c, rel_tol=1e-9):
        tri_type = "равнобедренный"
    else:
        tri_type = "разносторонний"

    x3 = (b ** 2 + c ** 2 - a ** 2) / (2 * c)
    y3_sq = b ** 2 - x3 ** 2
    y3 = math.sqrt(max(0.0, y3_sq))

    raw_points = [(0.0, 0.0), (c, 0.0), (x3, y3)]
    coords = scale_to_canvas(raw_points)

    logging.debug(f"{raw_points}, {coords}")

    return tri_type, coords