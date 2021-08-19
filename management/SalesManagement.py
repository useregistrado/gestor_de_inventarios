from management.Product import Product
class SalesManagement:

    def __init__(self, database):

        self.__bd_mngt = database
        self.__cart_products = []

    # Recibimos el id y la cantidad del producto que queremos agregar a la lista de compras
    # Consultamos los detalles del producto en la base de datos como el precio, iva y nombre
    # Creamos el nuevo producto y lo agregamos al carrito
    def add_producto(self, id, cant):
        p = self.search_product(id)
        if p is None:
            query = f"SELECT * FROM products WHERE id = {id}"
            products = self.__bd_mngt.select(query, "id", "name", "price", "iva", "cantidad")
            if len(products) == 0:
                raise NotFoundProduct(f"No se encuentra el producto con id: {id}")
            product = products[0]

            if product["cantidad"]>=cant:
                self.__cart_products.append(Product(product["id"], product["name"], product["price"], cant, product["iva"]))
                return self.__cart_products
            return False
        else:
            query = f"SELECT cantidad FROM products WHERE id = {id}"
            disponibilidad = self.__bd_mngt.select(query,"cantidad")[0]["cantidad"]
            cant = p.cantidad + cant
            if cant <= disponibilidad:
                p.cantidad = cant
                return self.__cart_products
            return False

    #Busca un objeto en el carrito de compras y lo retorna si lo encuentra, si no lo encuentra retorna None
    def search_product(self, id):
        for p in self.__cart_products:
            if p.id == id:
                return p
        return None

    def calculate_subtotal(self):
        return sum([p.subtotal for p in self.__cart_products])

    def calculate_iva(self):
        return sum([p.iva for p in self.__cart_products ])

    def calculate_total(self, subtotal=None, iva=None):
        if subtotal == None and iva == None:
            return self.calculate_iva() + self.calculate_subtotal()
        return iva + subtotal

    def complete_sale(self):

        #verificamos que haya mas de un producto en el carrito

        if len(self.__cart_products) == 0:
            return None

        subtotal, iva = self.calculate_subtotal(), self.calculate_iva()
        total = self.calculate_total(subtotal=subtotal,iva=iva)

        # A continuación se agregan los detalles de la venta a la base de datos y se actualizan las existencias en inventario
        query1 = "INSERT INTO factura (fecha, subtotal, iva, total) VALUES(now(), %s, %s, %s)"
        self.__bd_mngt.insert(query1, (subtotal, iva, total))

        # obtenemos el id de la ultima factua agregada para poder asignarle los detalles
        query2 = "SELECT max(id) FROM factura"
        id_voice = self.__bd_mngt.select(query2,"id")[0]["id"]

        for p in self.__cart_products:
            query_detalle = "INSERT INTO detalle (id_product, id_factura, cant) VALUES(%s, %s, %s)"
            self.__bd_mngt.insert(query_detalle, (p.id, id_voice, p.cantidad))

            query_update_cant = "UPDATE products SET cantidad = ((select cantidad from products where id = %s) - %s) WHERE id = %s"
            self.__bd_mngt.update(query_update_cant, (p.id, p.cantidad, p.id))

        # Vaciamos el carrito de compras y retornamos la suma de todos los subtotal, iva y total
        tam = len(self.__cart_products)
        return subtotal, iva, total, tam

    def clear_cart(self):
        del self.__cart_products[:]


class NotFoundProduct(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
