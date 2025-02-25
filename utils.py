from connection import columna, columna_2



tabla_global = None

def set_tabla(tabla):
    global tabla_global
    tabla_global = tabla


def cargar_tabla():
    datos = columna.find({})
    for dato in datos:
        tabla_global.insert("", "end", values=(dato['nombre'], dato['apellido'], dato['numero'], dato['correo']))

def cargar_estilos(root, nombre, apellido, numero, email, marco_izquierdo, marco_campos, marco_botones, nombre_entrada, apellido_entrada, numero_entrada, email_entrada, boton_editar, boton_borrar, boton_enviar):

    colores = columna_2.find({})

    for color in colores:
        if color['colorBackground']:
            for cambio in [root, marco_campos, marco_botones, marco_izquierdo, nombre, apellido, numero, email]:
                cambio.config(bg=color['colorBackground'])

        if color['colorText']:
            for cambio in [nombre, apellido, numero, email]:
                cambio.config(fg=color['colorText'])

        if color['colorButton']:
            for cambio in [boton_editar, boton_borrar, boton_enviar]:
                cambio.config(bg=color['colorButton'])

        if color['colorButtonText']:
            for cambio in [boton_editar, boton_borrar, boton_enviar]:
                cambio.config(fg=color['colorButtonText'])



def borrar_tabla():
    for fila in tabla_global.get_children():
        tabla_global.delete(fila)