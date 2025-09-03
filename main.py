import tkinter as tk
from tkinter import messagebox
import funciones

# --- Variables globales ---
tareas_filtradas = []  # Para manejar la búsqueda


# --- Funciones de la interfaz ---
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


def actualizar_lista(busqueda=""):
    listbox.delete(0, tk.END)
    tareas = funciones.cargar_tareas()

    # --- Ordenar: primero pendientes, luego completadas ---
    tareas.sort(key=lambda t: t["completada"])

    # --- Filtro por búsqueda ---
    global tareas_filtradas
    if busqueda:
        tareas_filtradas = [t for t in tareas if busqueda.lower() in t["nombre"].lower()]
    else:
        tareas_filtradas = tareas

    # --- Mostrar ---
    for i, tarea in enumerate(tareas_filtradas, start=1):
        estado = "✅" if tarea["completada"] else "❌"
        texto = f"{i}. {tarea['nombre']} - {tarea['descripcion']} [{estado}]"
        listbox.insert(tk.END, texto)


def completar():
    seleccion = listbox.curselection()
    if seleccion:
        idx = seleccion[0]
        tarea_original = tareas_filtradas[idx]
        todas = funciones.cargar_tareas()
        pos_real = todas.index(tarea_original)
        funciones.completar_tarea(pos_real)
        actualizar_lista(entry_busqueda.get().strip())
    else:
        messagebox.showinfo("ℹ️ Info", "Selecciona una tarea para completar.")


def eliminar():
    seleccion = listbox.curselection()
    if seleccion:
        idx = seleccion[0]
        tarea_original = tareas_filtradas[idx]
        todas = funciones.cargar_tareas()
        pos_real = todas.index(tarea_original)
        funciones.eliminar_tarea(pos_real)
        actualizar_lista(entry_busqueda.get().strip())
    else:
        messagebox.showinfo("ℹ️ Info", "Selecciona una tarea para eliminar.")


def editar():
    seleccion = listbox.curselection()
    if not seleccion:
        messagebox.showinfo("ℹ️ Info", "Selecciona una tarea para editar.")
        return

    idx = seleccion[0]
    tarea_original = tareas_filtradas[idx]
    todas = funciones.cargar_tareas()
    pos_real = todas.index(tarea_original)

    # --- Ventana emergente para edición ---
    edit_win = tk.Toplevel(ventana)
    edit_win.title("Editar tarea")
    edit_win.geometry("350x200")

    tk.Label(edit_win, text="Nuevo nombre:").pack(pady=5)
    entry_edit_nombre = tk.Entry(edit_win, width=30)
    entry_edit_nombre.insert(0, tarea_original["nombre"])
    entry_edit_nombre.pack()

    tk.Label(edit_win, text="Nueva descripción:").pack(pady=5)
    entry_edit_desc = tk.Entry(edit_win, width=30)
    entry_edit_desc.insert(0, tarea_original["descripcion"])
    entry_edit_desc.pack()

    def guardar_cambios():
        nuevo_nombre = entry_edit_nombre.get().strip()
        nueva_desc = entry_edit_desc.get().strip()
        if nuevo_nombre:
            todas[pos_real]["nombre"] = nuevo_nombre
            todas[pos_real]["descripcion"] = nueva_desc
            funciones.guardar_tareas(todas)
            actualizar_lista(entry_busqueda.get().strip())
            edit_win.destroy()
        else:
            messagebox.showwarning("⚠️ Atención", "El nombre no puede estar vacío.")

    tk.Button(edit_win, text="💾 Guardar cambios", command=guardar_cambios).pack(pady=10)


def buscar():
    busqueda = entry_busqueda.get().strip()
    actualizar_lista(busqueda)


# --- Ventana principal ---
ventana = tk.Tk()
ventana.title("Gestor de Tareas")
ventana.geometry("550x450")
ventana.config(bg="#f0f0f0")

# --- Frame de entrada ---
frame_inputs = tk.Frame(ventana, bg="#f0f0f0")
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Nombre:", bg="#f0f0f0").grid(row=0, column=0, padx=5, sticky="w")
entry_nombre = tk.Entry(frame_inputs, width=30)
entry_nombre.grid(row=0, column=1, padx=5)

tk.Label(frame_inputs, text="Descripción:", bg="#f0f0f0").grid(row=1, column=0, padx=5, sticky="w")
entry_desc = tk.Entry(frame_inputs, width=30)
entry_desc.grid(row=1, column=1, padx=5)

# --- Botones principales ---
frame_botones = tk.Frame(ventana, bg="#f0f0f0")
frame_botones.pack(pady=10)

btn_agregar = tk.Button(frame_botones, text="➕ Agregar", bg="#4CAF50", fg="white", command=agregar, width=12)
btn_agregar.grid(row=0, column=0, padx=5)

btn_completar = tk.Button(frame_botones, text="✅ Completar", bg="#2196F3", fg="white", command=completar, width=12)
btn_completar.grid(row=0, column=1, padx=5)

btn_eliminar = tk.Button(frame_botones, text="🗑️ Eliminar", bg="#f44336", fg="white", command=eliminar, width=12)
btn_eliminar.grid(row=0, column=2, padx=5)

btn_editar = tk.Button(frame_botones, text="✏️ Editar", bg="#FF9800", fg="white", command=editar, width=12)
btn_editar.grid(row=0, column=3, padx=5)

# --- Campo de búsqueda ---
frame_busqueda = tk.Frame(ventana, bg="#f0f0f0")
frame_busqueda.pack(pady=5)

tk.Label(frame_busqueda, text="🔍 Buscar:", bg="#f0f0f0").grid(row=0, column=0, padx=5)
entry_busqueda = tk.Entry(frame_busqueda, width=25)
entry_busqueda.grid(row=0, column=1, padx=5)
btn_buscar = tk.Button(frame_busqueda, text="Buscar", command=buscar)
btn_buscar.grid(row=0, column=2, padx=5)

# --- Lista de tareas con scroll ---
frame_lista = tk.Frame(ventana, bg="#f0f0f0")
frame_lista.pack(pady=10, fill="both", expand=True)

scroll = tk.Scrollbar(frame_lista)
scroll.pack(side="right", fill="y")

listbox = tk.Listbox(frame_lista, width=70, height=12, yscrollcommand=scroll.set, selectbackground="#d1e7dd")
listbox.pack(side="left", fill="both", expand=True)
scroll.config(command=listbox.yview)

# Inicializar lista
actualizar_lista()

ventana.mainloop()
