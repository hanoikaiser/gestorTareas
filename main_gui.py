import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import funciones

tareas_filtradas = []

# --- Funciones de la interfaz ---
def agregar():
    nombre = entry_nombre.get().strip()
    desc = entry_desc.get().strip()
    fecha = entry_fecha.get_date().strftime("%Y-%m-%d")  # Guardar formato YYYY-MM-DD
    if nombre:
        funciones.agregar_tarea(nombre, desc, fecha)
        actualizar_lista()
        entry_nombre.delete(0, tk.END)
        entry_desc.delete(0, tk.END)
    else:
        messagebox.showwarning("⚠️ Atención", "El nombre de la tarea no puede estar vacío.")

def actualizar_lista(busqueda=""):
    listbox.delete(0, tk.END)
    tareas = funciones.cargar_tareas()
    tareas.sort(key=lambda t: (t["completada"], t.get("vencimiento", "")))

    global tareas_filtradas
    if busqueda:
        tareas_filtradas = [t for t in tareas if busqueda.lower() in t["nombre"].lower()]
    else:
        tareas_filtradas = tareas

    for i, tarea in enumerate(tareas_filtradas, start=1):
        estado = "✅" if tarea["completada"] else "❌"
        venc = f" | Vence: {tarea['vencimiento']}" if tarea.get("vencimiento") else ""
        texto = f"{i}. {tarea['nombre']} - {tarea['descripcion']}{venc} [{estado}]"
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

def buscar():
    busqueda = entry_busqueda.get().strip()
    actualizar_lista(busqueda)

# --- Ventana principal ---
ventana = tk.Tk()
ventana.title("Gestor de Tareas")
ventana.geometry("600x500")
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

tk.Label(frame_inputs, text="Fecha de vencimiento:", bg="#f0f0f0").grid(row=2, column=0, padx=5, sticky="w")
entry_fecha = DateEntry(frame_inputs, width=27, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
entry_fecha.grid(row=2, column=1, padx=5)

# --- Botones principales ---
frame_botones = tk.Frame(ventana, bg="#f0f0f0")
frame_botones.pack(pady=10)

btn_agregar = tk.Button(frame_botones, text="➕ Agregar", bg="#4CAF50", fg="white", command=agregar, width=12)
btn_agregar.grid(row=0, column=0, padx=5)

btn_completar = tk.Button(frame_botones, text="✅ Completar", bg="#2196F3", fg="white", command=completar, width=12)
btn_completar.grid(row=0, column=1, padx=5)

btn_eliminar = tk.Button(frame_botones, text="🗑️ Eliminar", bg="#f44336", fg="white", command=eliminar, width=12)
btn_eliminar.grid(row=0, column=2, padx=5)

# --- Campo de búsqueda ---
frame_busqueda = tk.Frame(ventana, bg="#f0f0f0")
frame_busqueda.pack(pady=5)

tk.Label(frame_busqueda, text="🔍 Buscar:", bg="#f0f0f0").grid(row=0, column=0, padx=5)
entry_busqueda = tk.Entry(frame_busqueda, width=25)
entry_busqueda.grid(row=0, column=1, padx=5)
btn_buscar = tk.Button(frame_busqueda, text="Buscar", command=buscar)
btn_buscar.grid(row=0, column=2, padx=5)

# --- Lista de tareas ---
frame_lista = tk.Frame(ventana, bg="#f0f0f0")
frame_lista.pack(pady=10, fill="both", expand=True)

scroll = tk.Scrollbar(frame_lista)
scroll.pack(side="right", fill="y")

listbox = tk.Listbox(frame_lista, width=80, height=15, yscrollcommand=scroll.set, selectbackground="#d1e7dd")
listbox.pack(side="left", fill="both", expand=True)
scroll.config(command=listbox.yview)

# Inicializar lista
actualizar_lista()

ventana.mainloop()
