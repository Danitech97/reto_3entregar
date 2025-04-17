import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
from excepciones import mostrar_info,mostrar_error,mostrar_advertencia
from productos import Tienda
class InterfazTienda:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal - Tienda")
        self.root.geometry("800x700")
        self.fondo_img = ImageTk.PhotoImage(Image.open("python-supermarket.jpg").resize((800, 700)))
        self.canvas = None
        self.tienda = Tienda()
        self.tienda.cargar_productos_iniciales()
        self.usuario_es_admin = False
        self.carrito = []
        self.menu_inicio()

    
    def limpiar_ventana(self, mostrar_fondo=True):
       for widget in self.root.winfo_children():
         widget.destroy()
       self.canvas = tk.Canvas(self.root, width=650, height=700)
       self.canvas.pack(fill="both", expand=True)
       if mostrar_fondo:
          self.fondo_id = self.canvas.create_image(0, 0, image=self.fondo_img, anchor="nw")  

    def menu_inicio(self):
        self.limpiar_ventana()
        btn_client = tk.Button(self.root, text="🧑‍💻🍍 FrutaStack – Alimenta tu RAM con Vitaminas 🍇⚙️", width=50,)
        btn_cliente = tk.Button(self.root, text="Cliente", width=20, command=self.ventana_cliente)
        btn_admin = tk.Button(self.root, text="Administrador", width=20, command=self.ventana_admin_login)
        self.canvas.create_window(325, 600, window=btn_cliente)
        
        self.canvas.create_window(325, 560, window=btn_admin)
        self.canvas.create_window(325, 100, window=btn_client)
        

    def ventana_cliente(self):
        if hasattr(self, "fondo_id"):
         self.canvas.delete(self.fondo_id)

        
        self.usuario_es_admin = False
        self.carrito = []
        self.ventana_cliente_compra()

    def ventana_cliente_compra(self):
        self.limpiar_ventana(mostrar_fondo=False)
        
    # 👉 Frame que contiene la imagen + texto
        titulo_frame = tk.Frame(self.root, bg="white")
        self.canvas.create_window(325, 30, window=titulo_frame)

    # 👉 Cargar la imagen
        img = Image.open("supermarket.jpg").resize((200, 120))
        img_tk = ImageTk.PhotoImage(img)
        self.icono_producto = img_tk  # guardar referencia

        img_label = tk.Label(titulo_frame, image=img_tk, bg="white")
        img_label.pack(side="left", padx=(0, 10))

    # 👉 Texto al lado derecho
        texto_label = tk.Label(titulo_frame, text="Productos disponibles", font=("Arial", 14, "bold"), bg="white")
        texto_label.pack(side="left")

    # 👉 Frame para los productos debajo
        frame = tk.Frame(self.root)
        self.canvas.create_window(325, 180, window=frame)
    
        self.canvas.create_text(325, 30, text="Productos disponibles", font=("Arial", 14, "bold"), fill="black")
        
        frame = tk.Frame(self.root)
        self.canvas.create_window(325, 180, window=frame)

        columnas = ("ID", "Nombre", "Precio unidad ", "Stock")
        self.tree_productos = ttk.Treeview(frame, columns=columnas, show="headings", height=7)
        for col in columnas:
            self.tree_productos.heading(col, text=col)
            self.tree_productos.column(col, anchor="center")
        self.tree_productos.pack()
        self.actualizar_tabla_productos()

        btn_agregar = tk.Button(self.root, text="Agregar al carrito", command=self.agregar_al_carrito)
        self.canvas.create_window(325, 340, window=btn_agregar)

        self.canvas.create_text(325, 370, text="🧺 Carrito de Compras", font=("Arial", 12, "bold"), fill="black")

        frame_carrito = tk.Frame(self.root)
        self.canvas.create_window(325, 470, window=frame_carrito)

        carrito_cols = ("Nombre", "Precio", "Cantidad", "Subtotal")
        self.tree_carrito = ttk.Treeview(frame_carrito, columns=carrito_cols, show="headings", height=5)
        for col in carrito_cols:
            self.tree_carrito.heading(col, text=col)
            self.tree_carrito.column(col, anchor="center")
        self.tree_carrito.pack()

        self.label_total = tk.Label(self.root, text="Total: $0.00", font=("Arial", 12, "bold"), bg="lightgray")
        self.canvas.create_window(325, 540, window=self.label_total)

        btn_factura = tk.Button(self.root, text="Ver factura", command=self.mostrar_factura)
        btn_volver = tk.Button(self.root, text="Regresar al menú principal", command=self.menu_inicio)
        self.canvas.create_window(325, 580, window=btn_factura)
        self.canvas.create_window(325, 620, window=btn_volver)

    def actualizar_tabla_productos(self):
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        for pid, datos in self.tienda.productos.items():
            self.tree_productos.insert("", tk.END, values=(pid, datos['nombre'], f"${datos['precio']}", datos['stock']))

    def actualizar_tabla_carrito(self):
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)
        total = 0
        for item in self.carrito:
            subtotal = item['cantidad'] * item['precio']
            self.tree_carrito.insert("", tk.END, values=(item['producto'], f"${item['precio']:.2f}", item['cantidad'], f"${subtotal:.2f}"))
            total += subtotal
        self.label_total.config(text=f"Total: ${total:.2f}")

    def agregar_al_carrito(self):
        try:
            seleccion = self.tree_productos.selection()
            if not seleccion:
                mostrar_advertencia("Selecciona un producto")
                return
            valores = self.tree_productos.item(seleccion[0], "values")
            idp = valores[0]
            producto = self.tienda.productos.get(idp)
            cantidad = simpledialog.askinteger("Cantidad", f"Ingrese la cantidad de {producto['nombre']}:")
            if cantidad and cantidad > 0:
                if cantidad <= producto["stock"]:
                    self.carrito.append({"producto": producto["nombre"], "precio": producto["precio"], "cantidad": cantidad})
                    producto["stock"] -= cantidad
                    mostrar_info(f"Agregado {producto['nombre']} al carrito")
                    self.actualizar_tabla_productos()
                    self.actualizar_tabla_carrito()
                else:
                    mostrar_error("Stock insuficiente")
            else:
                mostrar_advertencia("Cantidad inválida")
        except Exception as e:
            mostrar_error(f"Error al agregar al carrito: {e}")

    def mostrar_factura(self):
        if not self.carrito:
            mostrar_advertencia("El carrito está vacío")
            return
        factura_ventana = tk.Toplevel(self.root)
        factura_ventana.title("Factura")
        factura_ventana.geometry("400x400")
        tk.Label(factura_ventana, text="Factura de Compra", font=("Courier", 14, "bold")).pack(pady=10)
        frame = tk.Frame(factura_ventana)
        frame.pack(pady=10)
        total = 0
        for item in self.carrito:
            linea = f"{item['cantidad']} x {item['producto']:<12} ${item['precio']:.2f} = ${item['cantidad'] * item['precio']:.2f}"
            tk.Label(frame, text=linea, font=("Courier", 10)).pack(anchor="w")
            total += item['cantidad'] * item['precio']
        tk.Label(factura_ventana, text=f"\nTotal a pagar: ${total:.2f}", font=("Courier", 12, "bold")).pack()
        tk.Button(factura_ventana, text="Volver al menú principal", command=lambda: [factura_ventana.destroy(), self.menu_inicio()]).pack(pady=20)

    def ventana_admin_login(self):
        self.limpiar_ventana(mostrar_fondo=False)
        
        self.canvas.create_text(325, 100, text="Inicio de Sesión", font=("Arial", 14, "bold"), fill="black")
        self.user_entry = tk.Entry(self.root)
        self.pass_entry = tk.Entry(self.root, show="*")
        self.canvas.create_window(325, 160, window=self.user_entry)
        self.canvas.create_window(325, 200, window=self.pass_entry)
        self.canvas.create_text(325, 145, text="Usuario:", fill="black")
        self.canvas.create_text(325, 185, text="Contraseña:", fill="black")
        login_btn = tk.Button(self.root, text="Ingresar", command=self.verificar_login_admin)
        self.canvas.create_window(325, 240, window=login_btn)

    def verificar_login_admin(self):
        usuario = self.user_entry.get()
        password = self.pass_entry.get()
        if usuario == "admin" and password == "1234":
            self.usuario_es_admin = True
            self.ventana_admin()
        else:
            mostrar_error("Credenciales incorrectas")

    def ventana_admin(self):
        self.limpiar_ventana()
        self.canvas.create_text(325, 30, text="Gestión de Productos", font=("Arial", 14, "bold"), fill="white")
        frame = tk.Frame(self.root)
        self.canvas.create_window(325, 240, window=frame)

        columnas = ("ID", "Nombre", "Precio", "Stock")
        self.tree = ttk.Treeview(frame, columns=columnas, show="headings", height=7)
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack()
        self.actualizar_tabla_productos_admin()

        botones = [
            ("Agregar", self.agregar_producto),
            ("Modificar", self.modificar_producto),
            ("Eliminar", self.eliminar_producto),
            ("Ver Historial", self.ver_historial),
            ("Volver", self.menu_inicio)
        ]
        for i, (texto, comando) in enumerate(botones):
            btn = tk.Button(self.root, text=texto, command=comando)
            self.canvas.create_window(325, 420 + i*40, window=btn)

    def actualizar_tabla_productos_admin(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for pid, datos in self.tienda.productos.items():
            self.tree.insert("", tk.END, values=(pid, datos['nombre'], f"${datos['precio']}", datos['stock']))

    def agregar_producto(self):
        try:
            idp = simpledialog.askstring("Agregar", "ID:")
            nombre = simpledialog.askstring("Agregar", "Nombre:")
            precio = float(simpledialog.askstring("Agregar", "Precio:"))
            stock = int(simpledialog.askstring("Agregar", "Stock:"))
            if self.tienda.agregar_producto(idp, nombre, precio, stock):
                self.actualizar_tabla_productos_admin()
                mostrar_info("Producto agregado")
            else:
                mostrar_error("ID ya registrado")
        except Exception:
            mostrar_error("Datos inválidos")

    def eliminar_producto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        valores = self.tree.item(seleccion[0], "values")
        idp = valores[0]
        if self.tienda.eliminar_producto(idp):
            self.actualizar_tabla_productos_admin()
            mostrar_info(f"Producto {idp} eliminado")

    def modificar_producto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        valores = self.tree.item(seleccion[0], "values")
        idp = valores[0]
        try:
            nombre = simpledialog.askstring("Modificar", "Nuevo nombre:")
            precio = float(simpledialog.askstring("Modificar", "Nuevo precio:"))
            stock = int(simpledialog.askstring("Modificar", "Nuevo stock:"))
            if self.tienda.modificar_producto(idp, nombre, precio, stock):
                self.actualizar_tabla_productos_admin()
                mostrar_info("Producto modificado")
        except Exception:
            mostrar_error("Datos inválidos")

    def ver_historial(self):
        historial = "\n".join(self.tienda.historial)
        messagebox.showinfo("Historial de acciones", historial)