def compare_keys(key1, key2):
    """ Compare keys of possibly different types: numeric, string, or datetime. """
    if type(key1) == type(key2):
        return (key1 > key2) - (key1 < key2)
    elif isinstance(key1, (int, float)) and isinstance(key2, (int, float)):
        return (key1 > key2) - (key1 < key2)
    else:
        key1_str = str(key1)
        key2_str = str(key2)
        return (key1_str > key2_str) - (key1_str < key2_str)

class BPlusTreeNode:
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.children = []
        self.leaf = True
        self.values = []

    def split(self):
        mid_point = len(self.keys) // 2
        new_node = BPlusTreeNode(self.order)
        new_node.keys = self.keys[mid_point:]
        new_node.values = self.values[mid_point:]
        new_node.leaf = self.leaf
        if not self.leaf:
            new_node.children = self.children[mid_point:]
        self.keys = self.keys[:mid_point]
        self.values = self.values[:mid_point]
        if not self.leaf:
            self.children = self.children[:mid_point]
        return new_node, self.keys[-1]

class BPlusTree:
    def __init__(self, order):
        self.root = BPlusTreeNode(order)
        self.order = order

    def insert(self, key, value):
        result = self._insert(self.root, key, value)
        if result:
            new_node, new_key = result  # Properly handle the returned tuple
            new_root = BPlusTreeNode(self.order)
            new_root.keys = [new_key]
            new_root.children = [self.root, new_node]
            new_root.leaf = False
            self.root = new_root

    def _insert(self, node, key, value):
        # If leaf node, handle insertion here
        if node.leaf:
            index = 0
            while index < len(node.keys) and compare_keys(node.keys[index], key) < 0:
                index += 1
            node.keys.insert(index, key)
            node.values.insert(index, value)
            if len(node.keys) > self.order:
                return node.split()  # Split and return new node and median key
            return None
        else:
            # Not a leaf node, so find the correct child to recurse on
            index = 0
            while index < len(node.keys) and compare_keys(node.keys[index], key) < 0:
                index += 1
            if index == len(node.children):
                index -= 1  # To handle edge case where key is greater than all existing keys

            result = self._insert(node.children[index], key, value)
            if result:
                new_node, median = result
                node.keys.insert(index, median)
                node.children.insert(index + 1, new_node)
                if len(node.keys) > self.order:
                    return node.split()
            return None

    def delete(self, key):
        self._delete(self.root, key)
        if len(self.root.keys) == 0 and not self.root.leaf:  # Shrink tree height if necessary
            self.root = self.root.children[0]

    def _delete(self, node, key):
        # Step 1: Find the key in the tree
        index = 0
        while index < len(node.keys) and node.keys[index] < key:
            index += 1

        if node.leaf:
            # Directly remove the key if it is in a leaf node
            if key in node.keys:
                pos = node.keys.index(key)
                node.keys.pop(pos)
                node.values.pop(pos)
            return
        else:
            # The key is in an internal node
            if index < len(node.keys) and node.keys[index] == key:
                left_child = node.children[index]
                node.keys[index] = left_child.keys[-1]
                node.values[index] = left_child.values[-1]
                self._delete(left_child, left_child.keys[-1])
            else:
                self._delete(node.children[index], key)

        # Step 2: Handle underflow
        if len(node.children[index].keys) < (self.order + 1) // 2:
            self._rebalance(node, index)

    def _rebalance(self, parent, index):
        child = parent.children[index]
        # Try to borrow from the left sibling
        if index > 0:
            left_sibling = parent.children[index - 1]
            if len(left_sibling.keys) > (self.order + 1) // 2:
                # Borrow the last element from the left sibling
                child.keys.insert(0, parent.keys[index - 1])
                child.values.insert(0, left_sibling.values.pop())
                parent.keys[index - 1] = left_sibling.keys.pop()
                return

        # Try to borrow from the right sibling
        if index < len(parent.children) - 1:
            right_sibling = parent.children[index + 1]
            if len(right_sibling.keys) > (self.order + 1) // 2:
                # Borrow the first element from the right sibling
                child.keys.append(parent.keys[index])
                child.values.append(right_sibling.values.pop(0))
                parent.keys[index] = right_sibling.keys.pop(0)
                return

        # Merge with a sibling if borrowing is not possible
        if index > 0:
            # Merge with the left sibling
            left_sibling = parent.children[index - 1]
            left_sibling.keys.extend(child.keys)
            left_sibling.values.extend(child.values)
            parent.keys.pop(index - 1)
            parent.children.pop(index)
        else:
            # Merge with the right sibling
            right_sibling = parent.children[index + 1]
            child.keys.extend(right_sibling.keys)
            child.values.extend(right_sibling.values)
            parent.keys.pop(index)
            parent.children.pop(index + 1)

    def update(self, old_key, new_key, new_value):
        # This simplified update function assumes keys must be unique
        self.delete(old_key)
        self.insert(new_key, new_value)

    def find(self, key):
        return self._find(self.root, key)

    def _find(self, node, key):
        if node.leaf:
            if key in node.keys:
                return node.values[node.keys.index(key)]
            return None
        else:
            index = 0
            while index < len(node.keys) and compare_keys(node.keys[index], key) < 0:
                index += 1
            return self._find(node.children[index], key)

    def show(self):
        self._show(self.root, 0)

    def _show(self, node, depth):
        if node:
            print('Level', depth, 'Keys:', node.keys)
            if node.leaf:
                print('Level', depth, 'Values:', node.values)
            else:
                for child in node.children:
                    self._show(child, depth + 1)
