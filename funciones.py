import json
import os

archivo = "tareas.json"

def cargar_tareas():
    if os.path.exists(archivo):
        with open(archivo, "r") as f:
            return json.load(f)
    return []

def guardar_tareas(tareas):
    with open(archivo, "w") as f:
        json.dump(tareas, f, indent=4)

def agregar_tarea(nombre, descripcion="", vencimiento=""):
    tareas = cargar_tareas()
    tareas.append({
        "nombre": nombre,
        "descripcion": descripcion,
        "vencimiento": vencimiento,
        "completada": False
    })
    guardar_tareas(tareas)

def completar_tarea(indice):
    tareas = cargar_tareas()
    if 0 <= indice < len(tareas):
        tareas[indice]["completada"] = True
        guardar_tareas(tareas)

def eliminar_tarea(indice):
    tareas = cargar_tareas()
    if 0 <= indice < len(tareas):
        tareas.pop(indice)
        guardar_tareas(tareas)
