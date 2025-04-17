
class Tienda:
    def __init__(self):
        self.productos = {}
        self.historial = []

    def cargar_productos_iniciales(self):
        self.productos = {
            "P01": {"nombre": "Manzana", "precio": 700, "stock": 300},
            "P02": {"nombre": "Banano", "precio": 200, "stock": 300},
            "P03": {"nombre": "Fresa", "precio": 300, "stock": 100},
            "po4": {"nombre":"Naranja","precio":200,"stock": 500},
        }

    def agregar_producto(self, idp, nombre, precio, stock):
        if idp not in self.productos:
            self.productos[idp] = {"nombre": nombre, "precio": precio, "stock": stock}
            self.historial.append(f"Agregado: {idp} - {nombre}")
            return True
        return False

    def eliminar_producto(self, idp):
        if idp in self.productos:
            del self.productos[idp]
            self.historial.append(f"Eliminado: {idp}")
            return True
        return False

    def modificar_producto(self, idp, nombre, precio, stock):
        if idp in self.productos:
            self.productos[idp] = {"nombre": nombre, "precio": precio, "stock": stock}
            self.historial.append(f"Modificado: {idp} - {nombre}")
            return True
        return False