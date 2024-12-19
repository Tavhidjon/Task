import json

class ProductManager:
    def __init__(self, filename):
        self.filename = filename
        self.products = self.load_products()

    def load_products(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return [line.strip().split(' — ') for line in file.readlines()]
        except FileNotFoundError:
            return []

    def save_products(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            for name, price in self.products:
                file.write(f"{name} — {price}\n")

    def add_product(self, name, price):
        self.products.append((name, price))
        self.save_products()

    def update_product(self, name, new_price):
        for i, (product_name, _) in enumerate(self.products):
            if product_name == name:
                self.products[i] = (name, new_price)
                self.save_products()
                return True
        return False

    def delete_product(self, name):
        self.products = [product for product in self.products if product[0] != name]
        self.save_products()

    def total_price(self):
        return sum(int(price) for _, price in self.products)

    def execute_command(self, action, name=None, price=None):
        if action == "add":
            self.add_product(name, price)
        elif action == "update":
            return self.update_product(name, price)
        elif action == "delete":
            self.delete_product(name)
        elif action == "total":
            return self.total_price()
        else:
            raise ValueError("Unknown action")

# Example usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python alif.py <filename> <action> [<name> <price>]")
        sys.exit(1)

    filename = sys.argv[1]
    action = sys.argv[2]
    name = sys.argv[3] if len(sys.argv) > 3 else None
    price = sys.argv[4] if len(sys.argv) > 4 else None

    manager = ProductManager(filename)
    if action in ["add", "update", "delete"]:
        if price is not None:
            price = int(price)
        manager.execute_command(action, name, price)
    elif action == "total":
        print(f"Total price: {manager.execute_command(action)}")