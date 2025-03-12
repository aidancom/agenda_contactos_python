from connection import columna, columna_2


tabla_global = None

def set_tabla(tabla):
    global tabla_global
    tabla_global = tabla



def cargar_tabla():
    datos = columna.find({})
    [tabla_global.insert("", "end", values=(dato['nombre'], dato['apellido'], dato['numero'], dato['correo'])) for dato in datos if not dato['privado']]



def cargar_estilos(root, nombre, apellido, numero, email, marco_izquierdo, marco_campos, marco_botones, nombre_entrada, apellido_entrada, numero_entrada, email_entrada, boton_editar, boton_borrar, boton_enviar):

    colores = columna_2.find({})

    for color in colores:
        if color['colorBackground']:
            [cambio.config(bg=color['colorBackground']) for cambio in [root, marco_campos, marco_botones, marco_izquierdo, nombre, apellido, numero, email]]

        if color['colorText']:
            [cambio.config(fg=color['colorText']) for cambio in [nombre, apellido, numero, email]]

        if color['colorButton']:
            [cambio.config(bg=color['colorButton']) for cambio in [boton_editar, boton_borrar, boton_enviar]]

        if color['colorButtonText']:
            [cambio.config(fg=color['colorButtonText']) for cambio in [boton_editar, boton_borrar, boton_enviar]]



def borrar_tabla():
    [tabla_global.delete(fila) for fila in tabla_global.get_children()]