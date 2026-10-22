import unittest

from date_utils import generate_nearby_dates


class DateRangeTests(unittest.TestCase):
    def test_neighbors(self):
        self.assertEqual(
            generate_nearby_dates("2026-12-15", 2),
            ["2026-12-13", "2026-12-14", "2026-12-15",
             "2026-12-16", "2026-12-17"],
        )

    def test_leap_day(self):
        self.assertEqual(
            generate_nearby_dates("2028-02-29", 1),
            ["2028-02-28", "2028-02-29", "2028-03-01"],
        )

    def test_invalid_range_and_date(self):
        with self.assertRaises(ValueError):
            generate_nearby_dates("2026-12-15", -1)
        with self.assertRaises(ValueError):
            generate_nearby_dates("12/15/2026", 1)


if __name__ == "__main__":
    unittest.main()
