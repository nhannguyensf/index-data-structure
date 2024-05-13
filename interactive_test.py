import unittest

from main import BPlusTree

class TestBPlusTreeInteractive(unittest.TestCase):
    def setUp(self):
        self.tree = BPlusTree(order=4)  # Choose an appropriate order

    def simulate_operations(self, operations):
        for operation in operations:
            op_type = operation[0]
            if op_type == 'INSERT':
                key, value = operation[1], operation[2]
                self.tree.insert(key, value)
                print(f"After INSERT[{key}]:")
                self.tree.show()

            elif op_type == 'DELETE':
                key = operation[1]
                self.tree.delete(key)
                print(f"After DELETE[{key}]:")
                self.tree.show()

            elif op_type == 'UPDATE':
                old_key, new_key, new_value = operation[1], operation[2], operation[3]
                self.tree.update(old_key, new_key, new_value)
                print(f"After UPDATE[{old_key} -> {new_key}]:")
                self.tree.show()

            elif op_type == 'SHOW':
                print("Current Tree:")
                self.tree.show()

    def test_interactive_simulation(self):
        operations = [
            ('INSERT', 10, 'Record10'),
            ('INSERT', 20, 'Record20'),
            ('UPDATE', 10, 15, 'Record15'),
            ('DELETE', 20),
            ('SHOW',)
        ]
        self.simulate_operations(operations)

if __name__ == '__main__':
    unittest.main()
