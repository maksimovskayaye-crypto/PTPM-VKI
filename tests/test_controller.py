import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from src.triangle import TriangleCalculator
from src.database import TriangleDatabase
from src.user_interaction import ConsoleUserInteraction
from src.external_service import EmailService
from src.controller import TriangleController
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))



class TestControllerIntegration(unittest.TestCase):

    def setUp(self):
        self.calc = TriangleCalculator()
        self.db = TriangleDatabase(":memory:")
        self.ui = ConsoleUserInteraction()
        self.ext = EmailService()
        self.controller = TriangleController(self.calc, self.db, self.ui, self.ext)

    def tearDown(self):
        self.db.close()

    # Проверка на сквозной сценарий: новый треугольник -> вычисление -> сохранение в БД -> отправка
    @patch.object(EmailService, 'send_result', return_value=True)
    @patch.object(ConsoleUserInteraction, 'get_triangle_sides', return_value=("3", "4", "5"))
    def test_new_triangle_computed_saved_and_sent(self, mock_ui, mock_ext):
        result = self.controller.process()

        self.assertIn("разносторонний", result)

        record = self.db.get(3.0, 4.0, 5.0)
        self.assertIsNotNone(record)
        self.assertEqual(record[0], "разносторонний")

        mock_ext.assert_called_once()

    # Проверка, что при повторном запросе результат берётся из БД, а не вычисляется заново
    @patch.object(EmailService, 'send_result', return_value=True)
    @patch.object(ConsoleUserInteraction, 'get_triangle_sides', return_value=("5", "5", "5"))
    def test_existing_triangle_taken_from_db(self, mock_ui, mock_ext):
        self.db.add(5.0, 5.0, 5.0, "равносторонний", "")

        result = self.controller.process()

        self.assertIn("равносторонний", result)

        mock_ext.assert_called_once()

    # Проверка на обработку нечисловых данных: БД не задействуется, но внешний сервис вызывается
    @patch.object(EmailService, 'send_result', return_value=True)
    @patch.object(ConsoleUserInteraction, 'get_triangle_sides', return_value=("abc", "4", "5"))
    def test_non_numeric_data_bypasses_db(self, mock_ui, mock_ext):
        result = self.controller.process()

        self.assertIn("вершины", result)

        mock_ext.assert_called_once()


if __name__ == '__main__':
    unittest.main()