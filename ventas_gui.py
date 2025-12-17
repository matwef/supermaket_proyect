import tkinter as tk
from tkinter import ttk, messagebox

from database import Database
from utils import mostrar_tabla
from config import WINDOW_BG

db = Database()

def ventas_menu(parent):
    """Ventana de gestión de ventas"""
    win = tk.Toplevel(parent)
    win.title("Gestión de Ventas")
    win.geometry("500x420")
    win.config(bg=WINDOW_BG)

    # Título
    tk.Label(
        win,
        text="VENTAS",
        font=("Arial", 16, "bold"),
        bg=WINDOW_BG
    ).pack(pady=10)

    form_frame = tk.Frame(win, bg=WINDOW_BG)
    form_frame.pack(pady=10, padx=20, fill="x")

    # Campos
    tk.Label(form_frame, text="Cliente ID (UUID):", bg=WINDOW_BG)\
        .grid(row=0, column=0, sticky="w", pady=5)
    client_id = tk.Entry(form_frame, width=36)
    client_id.grid(row=0, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="Empleado ID (UUID):", bg=WINDOW_BG)\
        .grid(row=1, column=0, sticky="w", pady=5)
    employee_id = tk.Entry(form_frame, width=36)
    employee_id.grid(row=1, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="Total:", bg=WINDOW_BG)\
        .grid(row=2, column=0, sticky="w", pady=5)
    total = tk.Entry(form_frame, width=36)
    total.grid(row=2, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="ID venta (UUID):", bg=WINDOW_BG)\
        .grid(row=3, column=0, sticky="w", pady=5)
    sale_id = tk.Entry(form_frame, width=36)
    sale_id.grid(row=3, column=1, pady=5, padx=10)

    # ---------- FUNCIONES ----------

    def agregar():
        if not client_id.get().strip() or not employee_id.get().strip() or not total.get().strip():
            messagebox.showwarning("Aviso", "Todos los campos son obligatorios")
            return

        try:
            total_val = float(total.get())
        except ValueError:
            messagebox.showwarning("Aviso", "El total debe ser numérico")
            return

        try:
            db.crear_venta(
                client_id.get().strip(),
                employee_id.get().strip(),
                total_val
            )
            messagebox.showinfo("Éxito", "Venta registrada correctamente")
            limpiar()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar venta: {e}")

    def eliminar():
        if not sale_id.get().strip():
            messagebox.showwarning("Aviso", "Ingrese el ID de la venta")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar esta venta?"):
            try:
                db.supabase.table("sales") \
                    .delete() \
                    .eq("id", sale_id.get().strip()) \
                    .execute()

                messagebox.showinfo("Éxito", "Venta eliminada")
                limpiar()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {e}")

    def ver_todas():
        try:
            ventas = db.listar_ventas()
            if ventas:
                mostrar_tabla(
                    ventas,
                    ["id", "client_id", "employee_id", "total", "fecha"],
                    "Ventas",
                    win
                )
            else:
                messagebox.showinfo("Sin datos", "No hay ventas registradas")
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener ventas: {e}")

    def limpiar():
        client_id.delete(0, tk.END)
        employee_id.delete(0, tk.END)
        total.delete(0, tk.END)
        sale_id.delete(0, tk.END)

    # Botones
    btn_frame = tk.Frame(win, bg=WINDOW_BG)
    btn_frame.pack(pady=10, padx=20, fill="x")

    ttk.Button(btn_frame, text="➕ Registrar venta", command=agregar).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="🗑️ Eliminar venta", command=eliminar).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="📋 Ver ventas", command=ver_todas).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="🧹 Limpiar", command=limpiar).pack(pady=3, fill="x")
