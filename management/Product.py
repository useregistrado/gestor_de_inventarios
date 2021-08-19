class Product:

    __subtotal = 0
    __total = 0
    __iva = 0

    def __init__(self,id, name, price, cant, iva_percentage):
        self.__id = id
        self.__name = name
        self.__price = price
        self.__cant = cant
        self.__iva_percentage = iva_percentage
        self.calculate_iva()
        self.calculate_subtotal()
        self.calculate_total()

    def calculate_iva(self):
        self.__iva = float("{:.2f}".format(self.__cant*self.__price*self.__iva_percentage))
        return self.__iva

    def calculate_subtotal(self):
        self.__subtotal = float("{:.2f}".format(self.__price*self.__cant))
        return  self.__subtotal

    def calculate_total(self):
        self.__total = float("{:.2f}".format(self.__subtotal + self.__iva))
        return self.__total

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def cant(self):
        return self.__cant

    @property
    def iva(self):
        return self.__iva

    @property
    def subtotal(self):
        return  self.__subtotal

    @property
    def total(self):
        return self.__total

    @property
    def cantidad(self):
        return self.__cant

    @property
    def subtotal(self):
        return self.__subtotal

    @property
    def total(self):
        return self.__total

    @cantidad.setter
    def cantidad(self, value):
        self.__cant =  value
        self.calculate_iva()
        self.calculate_subtotal()
        self.calculate_total()

    def __str__(self):
        return str(self.__cant)