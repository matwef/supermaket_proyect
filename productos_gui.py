import tkinter as tk
from tkinter import ttk, messagebox

from database import Database
from utils import validar_numero, mostrar_tabla
from config import WINDOW_BG

# instancia global de base de datos
db = Database()

def productos_menu(parent):
    """Ventana de gestión de productos"""
    win = tk.Toplevel(parent)
    win.title("Gestión de Productos")
    win.geometry("450x400")
    win.config(bg=WINDOW_BG)

    # Título
    tk.Label(
        win,
        text="PRODUCTOS",
        font=("Arial", 16, "bold"),
        bg=WINDOW_BG
    ).pack(pady=10)

    # Frame de formulario
    form_frame = tk.Frame(win, bg=WINDOW_BG)
    form_frame.pack(pady=10, padx=20, fill="x")

    # Campos
    tk.Label(form_frame, text="Nombre:", bg=WINDOW_BG).grid(row=0, column=0, sticky="w", pady=5)
    nombre = tk.Entry(form_frame, width=30)
    nombre.grid(row=0, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="Precio:", bg=WINDOW_BG).grid(row=1, column=0, sticky="w", pady=5)
    precio = tk.Entry(form_frame, width=30)
    precio.grid(row=1, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="Stock:", bg=WINDOW_BG).grid(row=2, column=0, sticky="w", pady=5)
    stock = tk.Entry(form_frame, width=30)
    stock.grid(row=2, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="ID (actualizar/eliminar):", bg=WINDOW_BG).grid(row=3, column=0, sticky="w", pady=5)
    prod_id = tk.Entry(form_frame, width=30)
    prod_id.grid(row=3, column=1, pady=5, padx=10)

    # ---------- FUNCIONES ----------

    def agregar():
        p = nombre.get().strip()
        pre = validar_numero(precio.get())
        s = validar_numero(stock.get(), int)

        if not p or pre is None or s is None:
            messagebox.showwarning("Aviso", "Todos los campos son obligatorios y válidos")
            return

        try:
            db.crear_producto(p, pre, s)
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar: {e}")

    def actualizar():
        pid = validar_numero(prod_id.get(), int)
        if pid is None:
            messagebox.showwarning("Aviso", "ID inválido")
            return

        data = {}

        if nombre.get().strip():
            data["nombre"] = nombre.get().strip()

        pre = validar_numero(precio.get())
        if pre is not None:
            data["precio"] = pre

        s = validar_numero(stock.get(), int)
        if s is not None:
            data["stock"] = s

        if not data:
            messagebox.showwarning("Aviso", "Ingrese al menos un campo para actualizar")
            return

        try:
            db.supabase.table("products").update(data).eq("id", pid).execute()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {e}")

    def eliminar():
        pid = validar_numero(prod_id.get(), int)
        if pid is None:
            messagebox.showwarning("Aviso", "ID inválido")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
            try:
                db.supabase.table("products").delete().eq("id", pid).execute()
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {e}")

    def buscar():
        p = nombre.get().strip()
        if not p:
            messagebox.showwarning("Aviso", "Ingrese un nombre para buscar")
            return

        try:
            res = db.supabase.table("products") \
                .select("*") \
                .ilike("nombre", f"%{p}%") \
                .execute()

            if res.data:
                mostrar_tabla(res.data, ["id", "nombre", "precio", "stock"], "Resultados", win)
            else:
                messagebox.showinfo("Sin resultados", "No se encontraron productos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar: {e}")

    def ver_todos():
        try:
            productos = db.listar_productos()  # ← lista

            if productos:
                mostrar_tabla(
                    productos,
                    ["id", "nombre", "precio", "stock"],
                    "Productos",
                    win
                )
            else:
                messagebox.showinfo("Sin datos", "No hay productos registrados")

        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener productos: {e}")

    def limpiar_campos():
        nombre.delete(0, tk.END)
        precio.delete(0, tk.END)
        stock.delete(0, tk.END)
        prod_id.delete(0, tk.END)

    # Frame de botones
    btn_frame = tk.Frame(win, bg=WINDOW_BG)
    btn_frame.pack(pady=10, padx=20, fill="x")

    ttk.Button(btn_frame, text="➕ Agregar", command=agregar).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="✏️ Actualizar", command=actualizar).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="🗑️ Eliminar", command=eliminar).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="🔍 Buscar", command=buscar).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="📋 Ver Todos", command=ver_todos).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="🧹 Limpiar", command=limpiar_campos).pack(pady=3, fill="x")
