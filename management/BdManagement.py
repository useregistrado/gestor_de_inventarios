import mysql.connector as mysql

class BdManagement:

    def __init__(self, host="localhost", database=None, user="root", port="3306", password=""):
        self.__db = mysql.connect(host=host, user=user, database=database, port=port, password=password)
        self.__cursor = self.__db.cursor()

    # Hace una consulta a la base de datos y devuelve una listo con un diccionario por cada fila
    # en los *args se especifican las columnas que se estan consultando para poder convertir las
    # tuplas en diccionarios ya que la consulta solo devuelve las filas en forma de tupla y para
    # acceder se hace por medio de posiciones, por este motivo se convierte a diccionario para que
    # sea mas practico acceder a las columnas de las filas consultadas.
    def select(self, query, *args):
        self.__cursor.execute(query)
        rows = self.__cursor.fetchall()
        rows_dict = []
        if len(args) == 0:
            return rows
        for row in rows:
            rows_dict.append(dict(zip(args,row)))
        return  rows_dict

    # funcion que inserta una fila nueva a una tabla, recibe la query y los valores a insertar en una tupla
    # sql_str: "INSERT INTO products ( name, price, iva) VALUES(%s, %s, %s)"
    # values: ("Azúcar morena 1kg", 3400, 0.19)
    def insert(self, sql_str, values):
        self.__cursor.execute(sql_str, values)
        self.__db.commit()

    # recibe una query como "DELETE FROM products WHERE id = %s" y una tupla que contiene el id (4,) posteriormente
    # retorna el numero de filas afectadas

    def delete(self, sql_str, id):
        self.__cursor.execute(sql_str, id)
        self.__db.commit()
        return self.__cursor.rowcount

    # Actualiza filas, recibe la sql_str y los valores y retorna la cantidad de filas afectadas
    # Ejemplo sql_str: "UPDATE products SET iva = %s where iva = %s" values: (0.14, 0.19)
    def update(self, sql_str, values):
        self.__cursor.execute(sql_str, values)
        self.__db.commit()
        return self.__cursor.rowcount
