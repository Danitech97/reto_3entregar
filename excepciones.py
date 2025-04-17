import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
def mostrar_error(mensaje):
    messagebox.showerror("Error", mensaje)

def mostrar_info(mensaje):
    messagebox.showinfo("Información", mensaje)

def mostrar_advertencia(mensaje):
    messagebox.showwarning("Advertencia", mensaje)
