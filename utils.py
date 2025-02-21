from connection import columna

tabla_global = None

def set_tabla(tabla):
    global tabla_global
    tabla_global = tabla

def cargar():
    datos = columna.find({})
    for dato in datos:
        tabla_global.insert("", "end", values=(dato['nombre'], dato['apellido'], dato['numero'], dato['correo']))

def borrar():
    for fila in tabla_global.get_children():
        tabla_global.delete(fila)