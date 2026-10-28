import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from scr.triangle import classify_triangle

class TestTriangleClassifier(unittest.TestCase):

    def test_equilateral_triangle_with_integer_sides(self):
        """Проверка равностороннего треугольника с целыми сторонами"""
        tri_type, coords = classify_triangle("5", "5", "5")
        self.assertEqual(tri_type, "равносторонний")
        self.assertEqual(len(coords), 3)

    def test_isosceles_triangle_with_float_sides(self):
        """Проверка равнобедренного треугольника с вещественными сторонами"""
        tri_type, coords = classify_triangle("5.5", "5.5", "3.0")
        self.assertEqual(tri_type, "равнобедренный")

    def test_scalene_triangle_right_angled(self):
        """Проверка разностороннего (прямоугольного) треугольника 3-4-5"""
        tri_type, coords = classify_triangle("3", "4", "5")
        self.assertEqual(tri_type, "разносторонний")

    def test_degenerate_triangle_float_precision_bug(self):
        """ПРОВЕРКА ИСПРАВЛЕНИЯ БАГА: вырожденный треугольник с погрешностью float (0.1 + 0.2 = 0.3)"""
        tri_type, coords = classify_triangle("0.1", "0.2", "0.3")
        self.assertEqual(tri_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_triangle_inequality_violation_large_side(self):
        """Проверка нарушения неравенства треугольника (одна сторона слишком большая)"""
        tri_type, coords = classify_triangle("1", "2", "10")
        self.assertEqual(tri_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_negative_side_length(self):
        """Проверка обработки отрицательной длины стороны"""
        tri_type, coords = classify_triangle("-3", "4", "5")
        self.assertEqual(tri_type, "не треугольник")

    def test_zero_side_length(self):
        """Проверка обработки нулевой длины стороны"""
        tri_type, coords = classify_triangle("0", "4", "5")
        self.assertEqual(tri_type, "не треугольник")

    def test_non_numeric_string_input(self):
        """Проверка обработки нечисловых строковых данных"""
        tri_type, coords = classify_triangle("abc", "4", "5")
        self.assertEqual(tri_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_empty_string_input(self):
        """Проверка обработки пустой строки на входе"""
        tri_type, coords = classify_triangle("", "4", "5")
        self.assertEqual(tri_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_none_type_input_handling(self):
        """Проверка обработки типа None (имитация сбоя передачи данных)"""
        tri_type, coords = classify_triangle(None, "4", "5")
        self.assertEqual(tri_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_very_large_sides_scaling(self):
        """Проверка масштабирования координат для очень больших сторон (вписывание в 100x100)"""
        tri_type, coords = classify_triangle("1000", "1000", "1000")
        self.assertEqual(tri_type, "равносторонний")
        for x, y in coords:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 99)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 99)

    def test_mixed_valid_and_invalid_inputs(self):
        """Проверка смешанных валидных и невалидных данных"""
        tri_type, coords = classify_triangle("5", "null", "5")
        self.assertEqual(tri_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

if __name__ == '__main__':
    unittest.main()