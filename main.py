import funciones

def menu():
    while True:
        print("\n=== GESTOR DE TAREAS ===")
        print("1. Agregar tarea")
        print("2. Ver tareas")
        print("3. Completar tarea")
        print("4. Eliminar tarea")
        print("5. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre de la tarea: ")
            descripcion = input("Descripción: ")
            funciones.agregar_tarea(nombre, descripcion)
            print("✅ Tarea agregada con éxito.")
        elif opcion == "2":
            funciones.listar_tareas()
        elif opcion == "3":
            funciones.listar_tareas()
            indice = int(input("Número de tarea a completar: ")) - 1
            funciones.completar_tarea(indice)
            print("✅ Tarea marcada como completada.")
        elif opcion == "4":
            funciones.listar_tareas()
            indice = int(input("Número de tarea a eliminar: ")) - 1
            funciones.eliminar_tarea(indice)
            print("🗑️ Tarea eliminada.")
        elif opcion == "5":
            print("👋 Saliendo...")
            break
        else:
            print("⚠️ Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    menu()
