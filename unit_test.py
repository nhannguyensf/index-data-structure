import unittest
from datetime import datetime

from main import BPlusTree

class TestBPlusTree(unittest.TestCase):
    def setUp(self):
        self.tree = BPlusTree(order=4)

    def test_insert_and_find_int(self):
        self.tree.insert(10, "Integer Record")
        result = self.tree.find(10)
        self.assertEqual(result, "Integer Record")

    def test_insert_and_find_string(self):
        self.tree.insert("key20", "String Record")
        result = self.tree.find("key20")
        self.assertEqual(result, "String Record")

    def test_insert_and_find_float(self):
        self.tree.insert(30.5, "Float Record")
        result = self.tree.find(30.5)
        self.assertEqual(result, "Float Record")

    def test_insert_and_find_date_string(self):
        date_key = "2021-05-10"
        self.tree.insert(date_key, "Date Record")
        result = self.tree.find(date_key)
        self.assertEqual(result, "Date Record")

    def test_structural_integrity(self):
        inputs = [(15, "val1"), ("10", "val2"), (20.0, "val3"), ("2020-01-01", "val4"), ("30", "val5"), (25.5, "val6")]
        for key, value in inputs:
            self.tree.insert(key, value)

        for key, expected_value in inputs:
            result = self.tree.find(key)
            self.assertEqual(result, expected_value)

    def test_ordering(self):
        # Insert keys in random order and check if they can be retrieved correctly
        inputs = [(5, "value5"), (1, "value1"), (3, "value3"), (4, "value4"), (2, "value2")]
        for key, value in sorted(inputs):
            self.tree.insert(key, value)

        for key, expected_value in sorted(inputs):
            result = self.tree.find(key)
            self.assertEqual(result, expected_value)

    def test_show_tree(self):
        # This method is for visualization, generally not used in automated tests but useful for debugging
        keys = [5, "key10", 15.2, "2019-12-25", "key40", 35.1]
        for key in keys:
            self.tree.insert(key, f"Record for {key}")
        self.tree.show()

if __name__ == '__main__':
    unittest.main()
