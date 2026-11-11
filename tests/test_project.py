import unittest
import sys
import os
from src.triangle import TriangleCalculator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))



class TestTriangleCalculatorUnit(unittest.TestCase):

    def setUp(self):
        self.calc = TriangleCalculator()

    def test_isosceles_with_two_equal_sides_at_end(self):
        """Равнобедренный треугольник: две равные стороны — B и C."""
        tri_type, coords = self.calc.classify("3", "5", "5")
        self.assertEqual(tri_type, "равнобедренный")
        self.assertEqual(len(coords), 3)

    def test_coords_are_within_canvas_bounds(self):
        """Проверка, что координаты всегда в пределах 0..99 для поля 100x100."""
        _, coords = self.calc.classify("7.5", "8.2", "9.1")
        for x, y in coords:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 99)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 99)


if __name__ == '__main__':
    unittest.main()