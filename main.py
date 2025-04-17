# main.py
import tkinter as tk
from tkinter import ttk


from operaciones import InterfazTienda

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazTienda(root)
    root.mainloop()