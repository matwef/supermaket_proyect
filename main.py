import tkinter as tk
from tkinter import ttk
from config import WINDOW_BG, MENU_BG
from utils import configurar_estilo
from productos_gui import productos_menu
from empleados_gui import empleados_menu
from clientes_gui import clientes_menu
from usuarios_gui import usuarios_menu
from ventas_gui import ventas_menu

def main():
    """Función principal de la aplicación"""
    root = tk.Tk()
    root.title("Sistema de Gestión - Supermercado La Doble Via")
    root.geometry("800x500")
    root.config(bg=WINDOW_BG)
    
    configurar_estilo()
    
    header_frame = tk.Frame(root, bg=WINDOW_BG)
    header_frame.pack(fill="x", pady=20)
    
    tk.Label(
        header_frame,
        text="🏪 Supermercado La Doble Via",
        font=("Arial", 24, "bold"),
        bg=WINDOW_BG,
        fg="#2c3e50"
    ).pack()
    
    tk.Label(
        header_frame,
        text="Sistema de Gestión Integral",
        font=("Arial", 12),
        bg=WINDOW_BG,
        fg="#7f8c8d"
    ).pack()
    
    menu_container = tk.Frame(root, bg=WINDOW_BG)
    menu_container.pack(expand=True, fill="both", padx=40, pady=20)
    
    buttons_frame = tk.Frame(menu_container, bg=WINDOW_BG)
    buttons_frame.pack(expand=True)
    
    btn_config = {"width": 20, "padding": 15}
    
    ttk.Button(
        buttons_frame, 
        text="📦 PRODUCTOS", 
        command=lambda: productos_menu(root),
        **btn_config
    ).grid(row=0, column=0, padx=10, pady=10)
    
    ttk.Button(
        buttons_frame, 
        text="👥 EMPLEADOS", 
        command=lambda: empleados_menu(root),
        **btn_config
    ).grid(row=0, column=1, padx=10, pady=10)
    
    ttk.Button(
        buttons_frame, 
        text="🤝 CLIENTES", 
        command=lambda: clientes_menu(root),
        **btn_config
    ).grid(row=0, column=2, padx=10, pady=10)
    
    ttk.Button(
        buttons_frame, 
        text="🔐 USUARIOS", 
        command=lambda: usuarios_menu(root),
        **btn_config
    ).grid(row=1, column=0, padx=10, pady=10)
    
    ttk.Button(
        buttons_frame, 
        text="💰 VENTAS", 
        command=lambda: ventas_menu(root),
        **btn_config
    ).grid(row=1, column=1, padx=10, pady=10)
    
    exit_btn = ttk.Button(
        buttons_frame, 
        text="🚪 SALIR", 
        command=root.destroy,
        **btn_config
    )
    exit_btn.grid(row=2, column=1, padx=10, pady=20)
    
    footer_frame = tk.Frame(root, bg=MENU_BG, height=40)
    footer_frame.pack(side="bottom", fill="x")
    
    tk.Label(
        footer_frame,
        text="Sistema desarrollado con Python + Tkinter + Supabase",
        font=("Arial", 9),
        bg=MENU_BG,
        fg="#555"
    ).pack(pady=10)
    
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()