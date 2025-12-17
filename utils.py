import tkinter as tk
from tkinter import ttk
from config import WINDOW_BG

def validar_numero(val, tipo=float):
    """Valida y convierte una cadena a número"""
    try:
        return tipo(val)
    except ValueError:
        return None

def mostrar_tabla(datos, cols, titulo="Tabla", parent=None):
    """Muestra datos en una ventana con Treeview"""
    win = tk.Toplevel(parent)
    win.title(titulo)
    win.geometry("700x400")
    win.config(bg=WINDOW_BG)
    
    # Frame para la tabla
    frame = tk.Frame(win, bg=WINDOW_BG)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Scrollbars
    scroll_y = ttk.Scrollbar(frame, orient="vertical")
    scroll_x = ttk.Scrollbar(frame, orient="horizontal")
    
    # Treeview
    tabla = ttk.Treeview(
        frame, 
        columns=cols, 
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )
    
    scroll_y.config(command=tabla.yview)
    scroll_x.config(command=tabla.xview)
    
    # Configurar columnas
    for c in cols:
        tabla.heading(c, text=c.upper())
        tabla.column(c, width=120, anchor="center")
    
    # Insertar datos
    for row in datos:
        tabla.insert("", tk.END, values=[row.get(c, "") for c in cols])
    
    # Empaquetar
    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tabla.pack(fill="both", expand=True)
    
    return win

def configurar_estilo():
    """Configura el estilo global de ttk"""
    style = ttk.Style()
    style.theme_use("clam")
    
    style.configure(
        "TButton", 
        padding=6, 
        relief="flat", 
        background="#4CAF50", 
        foreground="white", 
        font=("Arial", 10, "bold")
    )
    
    style.map("TButton", background=[("active", "#45a049")])
    
    style.configure(
        "TLabel",
        background=WINDOW_BG,
        font=("Arial", 10)
    )
    
    return style