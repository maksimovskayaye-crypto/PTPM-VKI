class TriangleController:

    def __init__(self, calculator, database, user_interaction, external_service):
        self.calculator = calculator
        self.db = database
        self.ui = user_interaction
        self.ext = external_service

    def process(self) -> str:
        a_str, b_str, c_str = self.ui.get_triangle_sides()

        try:
            a_f, b_f, c_f = float(a_str), float(b_str), float(c_str)
        except (ValueError, TypeError):
            # Нечисловые данные — не сохраняем в БД, сразу вычисляем и отправляем
            tri_type, coords = self.calculator.classify(a_str, b_str, c_str)
            result = f"Тип: {tri_type}, вершины: {coords}"
            self.ext.send_result(result)
            return result

        record = self.db.get(a_f, b_f, c_f)
        if record:
            tri_type, error_msg = record
            result = f"Тип: {tri_type}" + (f" (ошибка: {error_msg})" if error_msg else "")
        else:
            tri_type, coords = self.calculator.classify(a_str, b_str, c_str)
            error_msg = "некорректные данные" if tri_type in ("", "не треугольник") else ""
            self.db.add(a_f, b_f, c_f, tri_type, error_msg)
            result = f"Тип: {tri_type}, вершины: {coords}"

        self.ext.send_result(result)
        return result