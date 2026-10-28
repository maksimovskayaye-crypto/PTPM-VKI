# tests/test_delivery.py
import unittest
import sys
import os
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from scr.Delivery import calculate_delivery_cost

class TestDeliveryService(unittest.TestCase):

    def test_standard_delivery_basic_calculation(self):
        """Базовая доставка: обычный груз, без экспресса, малый вес"""
        cost, date = calculate_delivery_cost(2.0, 100, "обычный")
        self.assertEqual(cost, 700)
        self.assertEqual(date, "2026-09-04")

    def test_weight_coefficient_medium(self):
        """Проверка множителя 1.2 для веса от 5.1 до 19.9"""
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный")
        self.assertEqual(cost, int(700 * 1.2))

    def test_weight_coefficient_heavy(self):
        """Проверка множителя 1.5 для веса >= 20"""
        cost, _ = calculate_delivery_cost(25.0, 100, "обычный")
        self.assertEqual(cost, int(700 * 1.5))

    def test_fragile_package_surcharge(self):
        """Проверка наценки 300 руб для хрупкого груза"""
        cost, _ = calculate_delivery_cost(2.0, 100, "хрупкий")
        self.assertEqual(cost, 700 + 300)

    def test_hazardous_package_surcharge(self):
        """Проверка наценки 1000 руб для опасного груза"""
        cost, _ = calculate_delivery_cost(2.0, 100, "опасный")
        self.assertEqual(cost, 700 + 1000)

    def test_long_distance_days_calculation(self):
        """Проверка расчета дней для большого расстояния"""
        _, date = calculate_delivery_cost(2.0, 1500, "обычный")
        self.assertEqual(date, "2026-09-06")


    def test_invalid_weight_too_low(self):
        """Вес меньше минимального (0.1)"""
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_invalid_weight_too_high(self):
        """Вес больше максимального (50.0)"""
        cost, date = calculate_delivery_cost(55.0, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_invalid_distance_zero_or_negative(self):
        """Дистанция 0 или меньше"""
        cost, date = calculate_delivery_cost(2.0, 0, "обычный")
        self.assertEqual(cost, -1)

    def test_invalid_distance_too_high(self):
        """Дистанция больше 5000"""
        cost, date = calculate_delivery_cost(2.0, 6000, "обычный")
        self.assertEqual(cost, -1)

    def test_invalid_package_type(self):
        """Несуществующий тип посылки"""
        cost, date = calculate_delivery_cost(2.0, 100, "стекло")
        self.assertEqual(cost, -1)

    # --- FAIL ---

    def test_express_delivery_must_be_more_expensive(self):
        """[ОЖИДАЕМЫЙ FAIL] Экспресс-доставка должна быть ДОРОЖЕ обычной, а не дешевле"""
        cost_normal, _ = calculate_delivery_cost(2.0, 100, "обычный", is_express=False)
        cost_express, _ = calculate_delivery_cost(2.0, 100, "обычный", is_express=True)
        self.assertGreater(cost_express, cost_normal, "Экспресс не может стоить дешевле обычного!")

    def test_express_delivery_minimum_one_day(self):
        """[ОЖИДАЕМЫЙ FAIL] Экспресс-доставка не может занимать 0 дней (даже на короткое расстояние)"""
        _, date_str = calculate_delivery_cost(2.0, 400, "обычный", is_express=True)
        delivery_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        current_date = datetime.date(2026, 9, 3)
        days_diff = (delivery_date - current_date).days
        self.assertGreaterEqual(days_diff, 1, "Доставка не может занять 0 дней!")

if __name__ == '__main__':
    unittest.main()