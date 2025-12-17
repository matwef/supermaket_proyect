import tkinter as tk
from tkinter import ttk, messagebox

from database import Database
from utils import validar_numero, mostrar_tabla
from config import WINDOW_BG

# instancia global de base de datos
db = Database()


def empleados_menu(parent):
    """Ventana de gestión de empleados"""
    win = tk.Toplevel(parent)
    win.title("Gestión de Empleados")
    win.geometry("450x350")
    win.config(bg=WINDOW_BG)

    # Título
    tk.Label(
        win,
        text="EMPLEADOS",
        font=("Arial", 16, "bold"),
        bg=WINDOW_BG
    ).pack(pady=10)

    # Frame de formulario
    form_frame = tk.Frame(win, bg=WINDOW_BG)
    form_frame.pack(pady=10, padx=20, fill="x")

    # Campos
    tk.Label(form_frame, text="Nombre:", bg=WINDOW_BG)\
        .grid(row=0, column=0, sticky="w", pady=5)
    nombre = tk.Entry(form_frame, width=30)
    nombre.grid(row=0, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="Cargo:", bg=WINDOW_BG)\
        .grid(row=1, column=0, sticky="w", pady=5)
    cargo = tk.Entry(form_frame, width=30)
    cargo.grid(row=1, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="ID (actualizar/eliminar):", bg=WINDOW_BG)\
        .grid(row=2, column=0, sticky="w", pady=5)
    emp_id = tk.Entry(form_frame, width=30)
    emp_id.grid(row=2, column=1, pady=5, padx=10)

    # ---------- FUNCIONES ----------

    def agregar():
        n = nombre.get().strip()
        c = cargo.get().strip()

        if not n or not c:
            messagebox.showwarning("Aviso", "Todos los campos son obligatorios")
            return

        try:
            db.crear_empleado(n, c, 0)
            messagebox.showinfo("Éxito", "Empleado agregado correctamente")
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar: {e}")

    def actualizar():
        eid = validar_numero(emp_id.get(), int)
        if eid is None:
            messagebox.showwarning("Aviso", "ID inválido")
            return

        data = {}
        if nombre.get().strip():
            data["nombre"] = nombre.get().strip()
        if cargo.get().strip():
            data["cargo"] = cargo.get().strip()

        if not data:
            messagebox.showwarning(
                "Aviso", "Ingrese al menos un campo para actualizar"
            )
            return

        try:
            db.supabase.table("employees") \
                .update(data) \
                .eq("id", eid) \
                .execute()

            messagebox.showinfo("Éxito", "Empleado actualizado correctamente")
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {e}")

    def eliminar():
        eid = validar_numero(emp_id.get(), int)
        if eid is None:
            messagebox.showwarning("Aviso", "ID inválido")
            return

        if messagebox.askyesno(
            "Confirmar", "¿Está seguro de eliminar este empleado?"
        ):
            try:
                db.supabase.table("employees") \
                    .delete() \
                    .eq("id", eid) \
                    .execute()

                messagebox.showinfo("Éxito", "Empleado eliminado correctamente")
                limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {e}")

    def buscar():
        n = nombre.get().strip()
        if not n:
            messagebox.showwarning(
                "Aviso", "Ingrese un nombre para buscar"
            )
            return

        try:
            res = db.supabase.table("employees") \
                .select("*") \
                .ilike("nombre", f"%{n}%") \
                .execute()

            if res.data:
                mostrar_tabla(
                    res.data,
                    ["id", "nombre", "cargo"],
                    "Resultados",
                    win
                )
            else:
                messagebox.showinfo(
                    "Sin resultados", "No se encontraron empleados"
                )
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar: {e}")

    def ver_todos():
        try:
            empleados = db.listar_empleados()  # ← ES UNA LISTA

            if empleados:
                mostrar_tabla(
                    empleados,
                    ["id", "nombre", "cargo"],
                    "Empleados",
                    win
                )
            else:
                messagebox.showinfo(
                    "Sin datos", "No hay empleados registrados"
                )
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al obtener empleados: {e}"
            )

    def limpiar_campos():
        nombre.delete(0, tk.END)
        cargo.delete(0, tk.END)
        emp_id.delete(0, tk.END)

    # Frame de botones
    btn_frame = tk.Frame(win, bg=WINDOW_BG)
    btn_frame.pack(pady=10, padx=20, fill="x")

    ttk.Button(btn_frame, text="➕ Agregar", command=agregar)\
        .pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="✏️ Actualizar", command=actualizar)\
        .pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="🗑️ Eliminar", command=eliminar)\
        .pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="🔍 Buscar", command=buscar)\
        .pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="📋 Ver Todos", command=ver_todos)\
        .pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="🧹 Limpiar", command=limpiar_campos)\
        .pack(pady=3, fill="x")
