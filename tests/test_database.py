import unittest
import sys
import os
from src.database import TriangleDatabase
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))



class TestTriangleDatabase(unittest.TestCase):

    def setUp(self):
        self.db = TriangleDatabase(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_and_get_record(self):
        """Добавление и получение записи"""
        self.db.add(3.0, 4.0, 5.0, "разносторонний", "")
        record = self.db.get(3.0, 4.0, 5.0)
        self.assertIsNotNone(record)
        self.assertEqual(record[0], "разносторонний")
        self.assertEqual(record[1], "")

    def test_delete_record(self):
        """Удаление записи """
        self.db.add(5.0, 5.0, 5.0, "равносторонний", "")
        self.db.delete(5.0, 5.0, 5.0)
        record = self.db.get(5.0, 5.0, 5.0)
        self.assertIsNone(record)


if __name__ == '__main__':
    unittest.main()