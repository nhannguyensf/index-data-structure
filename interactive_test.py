import unittest
from datetime import datetime

from b_plus_tree import BPlusTree

class TestBPlusTreeInteractive(unittest.TestCase):

    @staticmethod
    def simulate_operations(tree, operations):
        for operation in operations:
            op_type = operation[0]
            if op_type == 'INSERT':
                key, value = operation[1], operation[2]
                tree.insert(key, value)
                print(f"After INSERT[{key}]:")
                tree.show()

            elif op_type == 'DELETE':
                key = operation[1]
                tree.delete(key)
                print(f"After DELETE[{key}]:")
                tree.show()

            elif op_type == 'UPDATE':
                old_key, new_key, new_value = operation[1], operation[2], operation[3]
                tree.update(old_key, new_key, new_value)
                print(f"After UPDATE[{old_key} -> {new_key}]:")
                tree.show()

            elif op_type == 'SHOW':
                print("Current Tree:")
                tree.show()

    def test_interactive_simulation_default_order(self):
        tree = BPlusTree(order=4)
        operations = [
            ('INSERT', 10, 'Record10'),
            ('INSERT', 20, 'Record20'),
            ('UPDATE', 10, 15, 'Record15'),
            ('DELETE', 20),
            ('SHOW',)
        ]
        self.simulate_operations(tree, operations)

    def test_interactive_simulation_higher_order(self):
        tree = BPlusTree(order=6)
        operations = [
            ('INSERT', 10, 'Record10'),
            ('INSERT', 20, 'Record20'),
            ('INSERT', 30, 'Record30'),
            ('DELETE', 20),
            ('UPDATE', 10, 15, 'NewRecord15'),
            ('SHOW',)
        ]
        self.simulate_operations(tree, operations)

    def test_interactive_simulation_with_strings(self):
        tree = BPlusTree(order=3)
        operations = [
            ('INSERT', 'apple', 'Fruit'),
            ('INSERT', 'banana', 'Yellow Fruit'),
            ('UPDATE', 'apple', 'green apple', 'Green Fruit'),
            ('DELETE', 'banana'),
            ('SHOW',)
        ]
        self.simulate_operations(tree, operations)

    def test_interactive_simulation_with_floats(self):
        tree = BPlusTree(order=5)
        operations = [
            ('INSERT', 3.14159, 'Pi'),
            ('INSERT', 2.71828, 'Euler Number'),
            ('UPDATE', 3.14159, 3.14, 'Pi Approx'),
            ('DELETE', 2.71828),
            ('SHOW',)
        ]
        self.simulate_operations(tree, operations)

if __name__ == '__main__':
    unittest.main()
