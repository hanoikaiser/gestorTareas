import tkinter as tk
from tkinter import messagebox
import funciones

# --- Funciones para manejar la interfaz ---
def agregar():
    nombre = entry_nombre.get().strip()
    desc = entry_desc.get().strip()
    if nombre:
        funciones.agregar_tarea(nombre, desc)
        actualizar_lista()
        entry_nombre.delete(0, tk.END)
        entry_desc.delete(0, tk.END)
    else:
        messagebox.showwarning("⚠️ Atención", "El nombre de la tarea no puede estar vacío.")

def actualizar_lista():
    listbox.delete(0, tk.END)
    tareas = funciones.cargar_tareas()
    for i, tarea in enumerate(tareas, start=1):
        estado = "✅" if tarea["completada"] else "❌"
        texto = f"{i}. {tarea['nombre']} - {tarea['descripcion']} [{estado}]"
        listbox.insert(tk.END, texto)

def completar():
    seleccion = listbox.curselection()
    if seleccion:
        funciones.completar_tarea(seleccion[0])
        actualizar_lista()
    else:
        messagebox.showinfo("ℹ️ Info", "Selecciona una tarea para completar.")

def eliminar():
    seleccion = listbox.curselection()
    if seleccion:
        funciones.eliminar_tarea(seleccion[0])
        actualizar_lista()
    else:
        messagebox.showinfo("ℹ️ Info", "Selecciona una tarea para eliminar.")

# --- Ventana principal ---
ventana = tk.Tk()
ventana.title("Gestor de Tareas")
ventana.geometry("500x400")
ventana.config(bg="#f0f0f0")

# --- Etiquetas y campos de entrada ---
frame_inputs = tk.Frame(ventana, bg="#f0f0f0")
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Nombre:", bg="#f0f0f0").grid(row=0, column=0, padx=5, sticky="w")
entry_nombre = tk.Entry(frame_inputs, width=30)
entry_nombre.grid(row=0, column=1, padx=5)

tk.Label(frame_inputs, text="Descripción:", bg="#f0f0f0").grid(row=1, column=0, padx=5, sticky="w")
entry_desc = tk.Entry(frame_inputs, width=30)
entry_desc.grid(row=1, column=1, padx=5)

# --- Botones ---
frame_botones = tk.Frame(ventana, bg="#f0f0f0")
frame_botones.pack(pady=10)

btn_agregar = tk.Button(frame_botones, text="➕ Agregar", bg="#4CAF50", fg="white", command=agregar, width=12)
btn_agregar.grid(row=0, column=0, padx=5)

btn_completar = tk.Button(frame_botones, text="✅ Completar", bg="#2196F3", fg="white", command=completar, width=12)
btn_completar.grid(row=0, column=1, padx=5)

btn_eliminar = tk.Button(frame_botones, text="🗑️ Eliminar", bg="#f44336", fg="white", command=eliminar, width=12)
btn_eliminar.grid(row=0, column=2, padx=5)

# --- Lista de tareas ---
frame_lista = tk.Frame(ventana, bg="#f0f0f0")
frame_lista.pack(pady=10, fill="both", expand=True)

scroll = tk.Scrollbar(frame_lista)
scroll.pack(side="right", fill="y")

listbox = tk.Listbox(frame_lista, width=60, height=12, yscrollcommand=scroll.set, selectbackground="#d1e7dd")
listbox.pack(side="left", fill="both", expand=True)
scroll.config(command=listbox.yview)

# Inicializar lista
actualizar_lista()

ventana.mainloop()
