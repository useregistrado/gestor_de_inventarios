from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QAbstractItemView, QHeaderView, QTableWidget, QTabWidget, QWidget, QDialog, QFrame
from PyQt5.QtGui import QFont, QColor
import sys
from management.BdManagement import BdManagement
from management.SalesManagement import SalesManagement
from management.ProductsManagement import ProductsManagement


class Gui(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("gui.ui", self)
        self.title = 'SGIV Oscar Vargas Pedraza @useregistrado'
        self.__init__ui()
        database = BdManagement(database="supermarket")
        self.salesmng = SalesManagement(database)
        self.productsmng = ProductsManagement(database)

    def __init__ui(self):
        self.setWindowTitle(self.title)
        self.btn_add_product.clicked.connect(self.add_product)
        self.btn_end_sale.clicked.connect(self.end_sale)
        self.btn_clear.clicked.connect(self.clear_cart)
        self.btn_create_product.clicked.connect(self.create_product)
        #-------------table----------------------

        self.table.setColumnCount(7)
        self.table.setRowCount(0)

        #Especificar alternacia de colores gris y blanco
        self.table.setAlternatingRowColors(True)

        #deshabilidar comportamiento de arrastrar y soltar
        self.table.setDragDropOverwriteMode(True)

        #deshabilitar edicion de las celdas
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        #seleccionar toda la fila
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        #seleccionar una fila a la vez
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        #Establecer el ajuste de palabras del texto
        self.table.setWordWrap(False)

        #ocultar encabezado vertical (indices de la izquierda)
        self.table.verticalHeader().setVisible(False)

        #Especificar la altura de cada fila
        self.table.verticalHeader().setDefaultSectionSize(20)

        #definimos el encabezado
        columnas_headers = ("id","Nombre","Cantidad","Valor Unitario","Sub Total", "Iva", "Total")

        #Asignamos el encabezado
        self.table.setHorizontalHeaderLabels(columnas_headers)


        for i, w in enumerate((59,170,90,180,200,160,200), start=0):
            self.table.setColumnWidth(i,w)
        self.table.resize(1061,500)
        self.table.move(30,160)
        self.datos_tabla()

        #-------------table----------------------

        #self.table.setVisible(True)

    def add_product(self):
        id_producto = self.id_add_producto.toPlainText()
        cantidad = self.cantidad_add_producto.toPlainText()
        if len(id_producto)>0 and len(cantidad)>0 and int(cantidad)>0:
            try:
                cart=self.salesmng.add_producto(int(id_producto),int(cantidad))
                if cart is not False:
                    self.datos_tabla(cart)
                    self.msg.setText("Se agrego correctamente")
                    self.msg.setStyleSheet("color: #3A3")
                else:
                    print(cart)
                    self.msg.setText("No hay suficientes productos")
                    self.msg.setStyleSheet("color: #d55")
            except NotFoundProduct as e:
                self.msg.setText(f"El  producto con id: {id_producto} no existe")
                self.msg.setStyleSheet("color: #d55")
                print("no se encontro el producto")
        else:
            self.msg.setText("Campos vacios")
            self.msg.setStyleSheet("color: #d55")
            print("campos vacios")

    def end_sale(self):
        result = self.salesmng.complete_sale()
        if result is None:
            self.msg.setText("No hay productos agregados")
            self.msg.setStyleSheet("color: #d55")
        else:
            self.msg.setText("Compra finalizada correctamente")
            self.msg.setStyleSheet("color: #3A3")
            print(result)
            row = result[3]
            self.table.setRowCount(row+1)

            # self.table.setItem(row, 0, QTableWidgetItem(""))
            # self.table.setItem(row, 1, QTableWidgetItem(""))
            # self.table.setItem(row, 2, QTableWidgetItem(""))
            text = QTableWidgetItem("TOTAL")
            subtotal = QTableWidgetItem(str(result[0]))
            iva = QTableWidgetItem(str(result[1]))
            total = QTableWidgetItem(str(result[2]))

            self.table.setItem(row, 3, text)
            self.table.setItem(row, 4, subtotal)
            self.table.setItem(row, 5, iva)
            self.table.setItem(row, 6, total)

            #Cambiaos el color del texto
            color = QColor(0, 0, 100)
            text.setForeground(color)
            subtotal.setForeground(color)
            iva.setForeground(color)

            #Creamos la fuente
            font = QFont("Times", 11, QFont.DemiBold)
            font2 = QFont("Times", 12, QFont.Bold)

            #Asignamos la nueva fuente
            text.setFont(font)
            subtotal.setFont(font)
            iva.setFont(font)
            total.setFont(font2)

            # Asignamos el color de la fuente para que resalte
            total.setBackground(QColor(0, 250, 0, 50))


            self.salesmng.clear_cart()

    def datos_tabla(self, productos = []):

        self.table.clearContents()
        row = 0
        for dato in productos:
            self.table.setRowCount(row+1)

            idDato = QTableWidgetItem(str(dato.id))
            idDato.setTextAlignment(4)

            self.table.setItem(row, 0, idDato)
            self.table.setItem(row, 1, QTableWidgetItem(str(dato.name)))
            self.table.setItem(row, 2, QTableWidgetItem(str(dato.cant)))
            self.table.setItem(row, 3, QTableWidgetItem(str(dato.price)))
            self.table.setItem(row, 4, QTableWidgetItem(str(dato.subtotal)))
            self.table.setItem(row, 5, QTableWidgetItem(str(dato.iva)))
            self.table.setItem(row, 6, QTableWidgetItem(str(dato.total)))

            row += 1

    def clear_cart(self):
        self.salesmng.clear_cart()
        self.table.clearContents()
        self.table.setRowCount(0)

    def create_product(self):

        def end_create(resultado):
            #En resultado se almacenan los productos que se encuantran en la base de datos y se muestran en orden descendente
            if resultado!=False:
                self.msg_create.setText("Creado correctamente")
                self.msg_create.setStyleSheet("color: #3A3")
            else:
                self.msg_create.setText("No se pudo crear el producto")
                self.msg_create.setStyleSheet("color: #D55")

        nombre = self.nombre_create_producto.toPlainText()
        try:
            precio = float(self.precio_create_producto.toPlainText())
        except Exception as e:
            self.msg_create.setText("Campo de precio incorrecto")
            self.msg_create.setStyleSheet("color: #D55")
        else:
            try:
                iva = float(self.iva_create_producto.toPlainText())
            except Exception as e:
                self.msg_create.setText("Campo de iva incorrecto")
                self.msg_create.setStyleSheet("color: #D55")
            else:
                try:
                    cantidad = float(self.cantidad_create_producto.toPlainText())
                    result = self.productsmng.create_product(nombre, precio, iva, cantidad)
                    end_create(result)
                except Exception as e:
                    self.msg_create.setText("Campo de cantidad incorrecto")
                    self.msg_create.setStyleSheet("color: #D55")





if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = Gui()
    gui.show()
    sys.exit(app.exec_())