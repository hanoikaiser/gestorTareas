import json

ARCHIVO = "tareas.json"

def cargar_tareas():
    try:
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_tareas(tareas):
    with open(ARCHIVO, "w") as f:
        json.dump(tareas, f, indent=4)

def agregar_tarea(nombre, descripcion):
    tareas = cargar_tareas()
    tareas.append({"nombre": nombre, "descripcion": descripcion, "completada": False})
    guardar_tareas(tareas)

def listar_tareas():
    tareas = cargar_tareas()
    if not tareas:
        print("No hay tareas registradas.")
    for i, tarea in enumerate(tareas, start=1):
        estado = "✅" if tarea["completada"] else "❌"
        print(f"{i}. {tarea['nombre']} - {tarea['descripcion']} [{estado}]")

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
