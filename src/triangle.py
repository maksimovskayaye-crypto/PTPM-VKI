import math


class TriangleCalculator:

    def classify(self, side_a_str: str, side_b_str: str, side_c_str: str) -> tuple:

        ERR_COORDS = [(-1, -1), (-1, -1), (-1, -1)]
        INV_COORDS = [(-2, -2), (-2, -2), (-2, -2)]

        try:
            a = float(side_a_str)
            b = float(side_b_str)
            c = float(side_c_str)
        except (ValueError, TypeError):
            return "", INV_COORDS

        if a <= 0 or b <= 0 or c <= 0:
            return "не треугольник", ERR_COORDS

        epsilon = 1e-9
        if (a + b <= c + epsilon) or (a + c <= b + epsilon) or (b + c <= a + epsilon):
            return "не треугольник", ERR_COORDS

        if math.isclose(a, b, rel_tol=1e-9) and math.isclose(b, c, rel_tol=1e-9):
            tri_type = "равносторонний"
        elif math.isclose(a, b, rel_tol=1e-9) or math.isclose(b, c, rel_tol=1e-9) or math.isclose(a, c, rel_tol=1e-9):
            tri_type = "равнобедренный"
        else:
            tri_type = "разносторонний"

        x3 = (b ** 2 + c ** 2 - a ** 2) / (2 * c)
        y3 = math.sqrt(max(0.0, b ** 2 - x3 ** 2))
        raw_points = [(0.0, 0.0), (c, 0.0), (x3, y3)]
        coords = self._scale_to_canvas(raw_points)

        return tri_type, coords

    def _scale_to_canvas(self, points, canvas_size=100, padding=5):
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        width = max_x - min_x
        height = max_y - min_y
        usable = canvas_size - 2 * padding
        if max(width, height) == 0:
            center = canvas_size // 2
            return [(center, center)] * 3
        scale = usable / max(width, height)
        result = []
        for x, y in points:
            nx = int(round(padding + (x - min_x) * scale))
            ny = int(round(padding + (y - min_y) * scale))
            result.append((max(0, min(canvas_size - 1, nx)),
                           max(0, min(canvas_size - 1, ny))))
        return result