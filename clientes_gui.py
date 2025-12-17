import tkinter as tk
from tkinter import ttk, messagebox

from database import Database
from utils import validar_numero, mostrar_tabla
from config import WINDOW_BG

# instancia global de la base de datos
db = Database()

def clientes_menu(parent):
    """Ventana de gestión de clientes"""
    win = tk.Toplevel(parent)
    win.title("Gestión de Clientes")
    win.geometry("450x400")
    win.config(bg=WINDOW_BG)

    # Título
    tk.Label(
        win,
        text="CLIENTES",
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

    tk.Label(form_frame, text="Teléfono:", bg=WINDOW_BG).grid(row=1, column=0, sticky="w", pady=5)
    telefono = tk.Entry(form_frame, width=30)
    telefono.grid(row=1, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="Email:", bg=WINDOW_BG).grid(row=2, column=0, sticky="w", pady=5)
    email = tk.Entry(form_frame, width=30)
    email.grid(row=2, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="ID (actualizar/eliminar):", bg=WINDOW_BG).grid(row=3, column=0, sticky="w", pady=5)
    cliente_id = tk.Entry(form_frame, width=30)
    cliente_id.grid(row=3, column=1, pady=5, padx=10)

    # ---------- FUNCIONES ----------

    def agregar():
        n = nombre.get().strip()
        t = telefono.get().strip()
        e = email.get().strip()

        if not n or not t or not e:
            messagebox.showwarning("Aviso", "Todos los campos son obligatorios")
            return

        try:
            db.supabase.table("clients").insert({
                "nombre": n,
                "telefono": t,
                "email": e
            }).execute()

            messagebox.showinfo("Éxito", "Cliente agregado correctamente")
            limpiar_campos()

        except Exception as ex:
            messagebox.showerror("Error", f"Error al agregar: {ex}")

    def actualizar():
        cid = validar_numero(cliente_id.get(), int)
        if cid is None:
            messagebox.showwarning("Aviso", "ID inválido")
            return

        data = {}
        if nombre.get().strip():
            data["nombre"] = nombre.get().strip()
        if telefono.get().strip():
            data["telefono"] = telefono.get().strip()
        if email.get().strip():
            data["email"] = email.get().strip()

        if not data:
            messagebox.showwarning("Aviso", "Ingrese al menos un campo para actualizar")
            return

        try:
            db.supabase.table("clients").update(data).eq("id", cid).execute()
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            limpiar_campos()

        except Exception as ex:
            messagebox.showerror("Error", f"Error al actualizar: {ex}")

    def eliminar():
        cid = validar_numero(cliente_id.get(), int)
        if cid is None:
            messagebox.showwarning("Aviso", "ID inválido")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
            try:
                db.supabase.table("clients").delete().eq("id", cid).execute()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                limpiar_campos()

            except Exception as ex:
                messagebox.showerror("Error", f"Error al eliminar: {ex}")

    def buscar():
        n = nombre.get().strip()
        if not n:
            messagebox.showwarning("Aviso", "Ingrese un nombre para buscar")
            return

        try:
            res = db.supabase.table("clients").select("*").ilike("nombre", f"%{n}%").execute()
            datos = res.data

            if datos:
                mostrar_tabla(datos, ["id", "nombre", "telefono", "email"], "Resultados de búsqueda", win)
            else:
                messagebox.showinfo("Sin resultados", "No se encontraron clientes con ese nombre")

        except Exception as ex:
            messagebox.showerror("Error", f"Error al buscar: {ex}")

    def ver_todos():
        try:
            res = db.supabase.table("clients").select("*").execute()
            datos = res.data

            if datos:
                mostrar_tabla(datos, ["id", "nombre", "telefono", "email"], "Todos los clientes", win)
            else:
                messagebox.showinfo("Sin datos", "No hay clientes registrados")

        except Exception as ex:
            messagebox.showerror("Error", f"Error al obtener clientes: {ex}")

    def limpiar_campos():
        nombre.delete(0, tk.END)
        telefono.delete(0, tk.END)
        email.delete(0, tk.END)
        cliente_id.delete(0, tk.END)

    # Botones
    btn_frame = tk.Frame(win, bg=WINDOW_BG)
    btn_frame.pack(pady=10, padx=20, fill="x")

    ttk.Button(btn_frame, text="➕ Agregar", command=agregar).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="✏️ Actualizar", command=actualizar).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="🗑️ Eliminar", command=eliminar).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="🔍 Buscar", command=buscar).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="📋 Ver Todos", command=ver_todos).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="🧹 Limpiar", command=limpiar_campos).pack(pady=3, fill="x")
