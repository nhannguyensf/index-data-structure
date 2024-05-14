import sys
from datetime import datetime
from b_plus_tree import BPlusTree

def parse_input(input_str):
    parts = input_str.strip().split(' ')
    command = parts[0].upper()
    args = parts[1:]
    return command, args

def main():
    try:
        order = int(input("Enter the order of the B+ Tree: "))
        if order < 3:
            print("Order should be at least 3")
            return
    except ValueError:
        print("Invalid input. Order should be an integer.")
        return

    tree = BPlusTree(order)
    print("B+ Tree initialized with order", order)

    while True:
        user_input = input("Enter command (INSERT, UPDATE, DELETE, SHOW, EXIT): ")
        command, args = parse_input(user_input)

        if command == 'INSERT':
            if len(args) != 2:
                print("INSERT command requires exactly 2 arguments: key and value.")
                continue
            key, value = args
            try:
                key = int(key)
            except ValueError:
                try:
                    key = float(key)
                except ValueError:
                    try:
                        key = datetime.strptime(key, '%Y-%m-%d')
                    except ValueError:
                        pass
            tree.insert(key, value)
            print(f"After INSERT[{key}]:")
            tree.show()

        elif command == 'UPDATE':
            if len(args) != 3:
                print("UPDATE command requires exactly 3 arguments: old_key, new_key, new_value.")
                continue
            old_key, new_key, new_value = args
            try:
                old_key = int(old_key)
            except ValueError:
                try:
                    old_key = float(old_key)
                except ValueError:
                    try:
                        old_key = datetime.strptime(old_key, '%Y-%m-%d')
                    except ValueError:
                        pass
            try:
                new_key = int(new_key)
            except ValueError:
                try:
                    new_key = float(new_key)
                except ValueError:
                    try:
                        new_key = datetime.strptime(new_key, '%Y-%m-%d')
                    except ValueError:
                        pass
            tree.update(old_key, new_key, new_value)
            print(f"After UPDATE[{old_key} -> {new_key}]:")
            tree.show()

        elif command == 'DELETE':
            if len(args) != 1:
                print("DELETE command requires exactly 1 argument: key.")
                continue
            key = args[0]
            try:
                key = int(key)
            except ValueError:
                try:
                    key = float(key)
                except ValueError:
                    try:
                        key = datetime.strptime(key, '%Y-%m-%d')
                    except ValueError:
                        pass
            tree.delete(key)
            print(f"After DELETE[{key}]:")
            tree.show()

        elif command == 'SHOW':
            print("Current Tree:")
            tree.show()

        elif command == 'EXIT':
            print("Exiting...")
            break

        else:
            print("Invalid command. Available commands: INSERT, UPDATE, DELETE, SHOW, EXIT.")

if __name__ == '__main__':
    main()
