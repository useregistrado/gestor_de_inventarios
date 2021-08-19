

class ProductsManagement:

    def __init__(self, bd_management):
        self.__bd_management = bd_management

    def create_product(self, nombre, precio, iva, cantidad):
        product = self.__bd_management.select(f"SELECT id FROM products WHERE name = '{nombre}'")
        if len(product)==0:
            query = "INSERT INTO products (name, price, iva, cantidad) VALUES (%s, %s, %s, %s)"
            result = self.__bd_management.insert(query, (nombre, precio, iva, cantidad))
            products = self.find_products()
            return products
        else:
            print("El producto ya existe")
            return False

    def update_product(self, id, sets):
        query1 = f"SELECT id FROM products WHERE id = {id}"
        p = self.__bd_management.select(query1)
        if len(p) == 0:
            raise NotFoundProduct(f"El producto con id: {id} no existe en la base de datos")

        set = ""
        for k, v in sets.items():
            set += f" {k} = %s"
            set += ","
        set = set[0:-1]
        query = f"UPDATE products SET {set} WHERE id = %s"

    def find_products(self):
        query = "SELECT * FROM products ORDER BY id DESC"
        return self.__bd_management.select(query, "id", "nombre", "precio", "iva", "cantidad")

if __name__ == "__main__":
    p = ProductsManangement(55)