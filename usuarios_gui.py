import tkinter as tk
from tkinter import ttk, messagebox

from database import Database
from utils import mostrar_tabla
from config import WINDOW_BG

# instancia de la base de datos
db = Database()

def usuarios_menu(parent):
    """Ventana de gestión de usuarios"""
    win = tk.Toplevel(parent)
    win.title("Gestión de Usuarios")
    win.geometry("450x350")
    win.config(bg=WINDOW_BG)

    # Título
    tk.Label(
        win,
        text="USUARIOS",
        font=("Arial", 16, "bold"),
        bg=WINDOW_BG
    ).pack(pady=10)

    # Frame formulario
    form_frame = tk.Frame(win, bg=WINDOW_BG)
    form_frame.pack(pady=10, padx=20, fill="x")

    tk.Label(form_frame, text="Usuario:", bg=WINDOW_BG).grid(row=0, column=0, sticky="w", pady=5)
    username = tk.Entry(form_frame, width=30)
    username.grid(row=0, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="Rol:", bg=WINDOW_BG).grid(row=1, column=0, sticky="w", pady=5)
    rol = tk.Entry(form_frame, width=30)
    rol.grid(row=1, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="ID (actualizar/eliminar):", bg=WINDOW_BG).grid(row=2, column=0, sticky="w", pady=5)
    user_id = tk.Entry(form_frame, width=30)
    user_id.grid(row=2, column=1, pady=5, padx=10)

    # ---------- FUNCIONES ----------

    def agregar():
        u = username.get().strip()
        r = rol.get().strip()

        if not u or not r:
            messagebox.showwarning("Aviso", "Todos los campos son obligatorios")
            return

        try:
            db.supabase.table("usuarios").insert({
                "username": u,
                "rol": r
            }).execute()

            messagebox.showinfo("Éxito", "Usuario agregado correctamente")
            limpiar()

        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar: {e}")

    def actualizar():
        uid = user_id.get().strip()
        if not uid.isdigit():
            messagebox.showwarning("Aviso", "ID inválido")
            return

        data = {}
        if username.get().strip():
            data["username"] = username.get().strip()
        if rol.get().strip():
            data["rol"] = rol.get().strip()

        if not data:
            messagebox.showwarning("Aviso", "Ingrese datos para actualizar")
            return

        try:
            db.supabase.table("usuarios").update(data).eq("id", int(uid)).execute()
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
            limpiar()

        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {e}")

    def eliminar():
        uid = user_id.get().strip()
        if not uid.isdigit():
            messagebox.showwarning("Aviso", "ID inválido")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar este usuario?"):
            try:
                db.supabase.table("usuarios").delete().eq("id", int(uid)).execute()
                messagebox.showinfo("Éxito", "Usuario eliminado")
                limpiar()

            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {e}")

    def ver_todos():
        try:
            res = db.supabase.table("usuarios").select("*").execute()
            datos = res.data

            if datos:
                mostrar_tabla(datos, ["id", "username", "rol"], "Usuarios", win)
            else:
                messagebox.showinfo("Sin datos", "No hay usuarios registrados")

        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener usuarios: {e}")

    def limpiar():
        username.delete(0, tk.END)
        rol.delete(0, tk.END)
        user_id.delete(0, tk.END)

    # Botones
    btn_frame = tk.Frame(win, bg=WINDOW_BG)
    btn_frame.pack(pady=10, padx=20, fill="x")

    ttk.Button(btn_frame, text="➕ Agregar", command=agregar).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="✏️ Actualizar", command=actualizar).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="🗑️ Eliminar", command=eliminar).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="📋 Ver Todos", command=ver_todos).pack(pady=3, fill="x")
    ttk.Button(btn_frame, text="🧹 Limpiar", command=limpiar).pack(pady=3, fill="x")
