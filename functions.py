from connection import columna
from tkinter import *
from tkinter import simpledialog, messagebox
from insert import insertar
from utils import *

import os
import csv
import pyperclip
import json



def actualizar_tabla_y_base():
    borrar()
    cargar()



def insertar_datos():
    numero_registros = simpledialog.askinteger("Registros", "Introduce el numero de registros que deseas agregar")
    insertar(numero_registros)
    messagebox.showinfo("Hecho", "Datos cargados con éxito")
    actualizar_tabla_y_base()



def vaciar():
    try:
        validar = simpledialog.askstring("Auntenticación", "Introduzca la contraseña para eliminar", show="*")
        if validar == 'admin99':
            opcion = messagebox.askquestion("Advertencia", "¿Seguro que desea vaciar la base de datos? Esta opción no se podra deshacer")
            if opcion == 'yes':
                columna.drop()
                messagebox.showinfo("Hecho", "Base de datos vaciada con éxito")
                actualizar_tabla_y_base()
            else:
                pass
        else:
            pass
    except ValueError:
        messagebox.showerror("Error", "Carácter no válido")
    except Exception as e:
        messagebox.showerror("Error", f"{e}")



def buscar(tabla):
    try:
        numero = simpledialog.askinteger("Buscar un contacto", "Introduzca el numero que desea buscar")
        pipeline = [{"$match": {"numero": numero}}]
        res = columna.aggregate(pipeline)
        contador = columna.count_documents({"numero": numero})
        if contador > 0:
            borrar()
            for registro in res:
                tabla.insert("", "end", values=(registro['nombre'], registro['apellido'], registro['numero'], registro['correo']))
        else:
            messagebox.showinfo("Sin registros", "No existo un contacto con ese número")
    except ValueError:
        messagebox.showerror("Error", "Carácter no cálido")
    except Exception as e:
        messagebox.showerror("Error", f"{e}")



def enviar_contacto(nombre_entrada, apellido_entrada, numero_entrada, email_entrada):
    try:
        nombre = nombre_entrada.get().capitalize()
        apellido = apellido_entrada.get().capitalize()
        numero = int(numero_entrada.get())
        email = email_entrada.get().lower()
        if nombre and apellido and numero and email:
            contacto = {"nombre": nombre, "apellido": apellido, "numero": numero, "correo": email, "favorito": False}
            columna.insert_one(contacto)
            messagebox.showinfo("Hecho", "Contacto añadido con éxito")
            for entrada in [nombre_entrada, apellido_entrada, numero_entrada, email_entrada]:
                entrada.delete(0, END)
            actualizar_tabla_y_base()
        else:
            messagebox.showerror("Error", "No pueden haber campos vacios")
    except ValueError:
        messagebox.showerror("Error", "Carácter no válido")
    except Exception as e:
        messagebox.showerror("Error", f"{e}")



def seleccion_contacto(nombre_entrada, apellido_entrada, numero_entrada, email_entrada, tabla, boton_editar, boton_borrar, boton_enviar):
    tabla_seleccion = tabla.selection()
    for entradas in [nombre_entrada, apellido_entrada, numero_entrada, email_entrada]:
        entradas.delete(0, END)
    if tabla_seleccion:
        tabla_registro = (tabla.item(tabla_seleccion, "values"))
        nombre_entrada.insert(0, tabla_registro[0])
        apellido_entrada.insert(0, tabla_registro[1])
        numero_entrada.insert(0, tabla_registro[2])
        email_entrada.insert(0, tabla_registro[3])
        boton_borrar.config(state="active")
        boton_editar.config(state="active")
        boton_enviar.config(state="disabled")



def borrar_contacto(nombre_entrada, apellido_entrada, numero_entrada, email_entrada, boton_editar, boton_borrar, boton_enviar):
    nombre = nombre_entrada.get().capitalize()
    apellido = apellido_entrada.get().capitalize()
    numero = numero_entrada.get()
    email = email_entrada.get().lower()
    if nombre and apellido and numero and email:
        contacto = {"nombre": nombre, "apellido": apellido, "numero": int(numero), "correo": email}
        alerta = messagebox.askquestion("", "Seguro que desea eliminar este campo")
        if alerta == 'yes':
            columna.delete_one(contacto)
            messagebox.showinfo("Hecho", "Contacto eliminado con éxito")
            for entradas in [nombre_entrada, apellido_entrada, numero_entrada, email_entrada]:
                entradas.delete(0, END)
            boton_editar.config(state="disabled")
            boton_borrar.config(state="disabled")
            boton_enviar.config(state="active")
            actualizar_tabla_y_base()



def editar_contacto(nombre_entrada, apellido_entrada, numero_entrada, email_entrada, boton_editar, boton_borrar, boton_enviar, tabla):
    seleccion = tabla.selection()
    tabla_registro = list((tabla.item(seleccion, "values")))
    numero_buscar = tabla_registro[2]

    nombre_actual = nombre_entrada.get()
    apellido_actual = apellido_entrada.get()
    numero_actual = numero_entrada.get()
    email_actual = email_entrada.get()

    filtro = {"numero": int(numero_buscar)}
    datos_actuales = {"$set": {"nombre": nombre_actual, "apellido": apellido_actual, "numero": int(numero_actual), "correo": email_actual}}

    columna.update_one(filtro, datos_actuales)

    messagebox.showinfo("Editado", "Contacto editado con éxito")

    for entradas in [nombre_entrada, apellido_entrada, numero_entrada, email_entrada]:
        entradas.delete(0, END)

    boton_editar.config(state="disabled")
    boton_borrar.config(state="disabled")
    boton_enviar.config(state="active")
    actualizar_tabla_y_base()



def exportar(tabla, exportar_csv, exportar_txt, exportar_json):
    ruta = os.path.dirname(__file__)
    if exportar_txt:
        with open(f"{ruta}/archivos/contactos.txt", "w") as archivo:
            for datos in tabla.get_children():
                dato = tabla.item(datos, "values")
                archivo.write(f"Nombre: {dato[0]}\nApellido: {dato[1]}\nTeléfono: {dato[2]}\nCorreo: {dato[3]}\n\n")
        abrir = messagebox.askquestion("Hecho", "Contactos exportados a txt con éxito, ¿Quieres abrir el archivo?")
        if abrir:
            os.startfile(f"{ruta}/archivos/contactos.txt")
    if exportar_csv:
        with open(f"{ruta}/archivos/contactos.csv", "w", newline="") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(["Nombre", "Apellido", "Teléfono", "Correo"])
            for datos in tabla.get_children():
                dato = tabla.item(datos, "values")
                writer.writerow(dato)
        abrir = messagebox.askquestion("Hecho", "Contactos exportados a csv con éxito, ¿Quieres abrir el archivo?")
        if abrir:
            os.startfile(f"{ruta}/archivos/contactos.csv")
    if exportar_json:
        datos_exportar = columna.find({})
        datos = []
        for dato in datos_exportar:
            datos.append({"nombre": dato['nombre'], "apellido": dato['apellido'], "numero": dato['numero'], "correo": dato['correo'], "favorito": dato['favorito']})
        with open(f"{ruta}/archivos/contactos.json", "w") as archivo:
            json.dump(datos, archivo, indent=4)
        abrir = messagebox.askquestion("Hecho", "Contactos exportados a json con éxito, ¿Quieres abrir el archivo?")
        if abrir:
            os.startfile(f"{ruta}/archivos/contactos.json")



def popup(event, tabla, root):
    row_id = tabla.identify_row(event.y)
    if row_id:
        tabla.selection_set(row_id)
        item = list(tabla.item(row_id, "values"))
        dato = {"nombre": item[0], "apellido": item[1], "numero": int(item[2]), "correo": item[3]}
        registro = columna.find_one(dato)
        popup = Menu(root, tearoff=0)
        popup.add_command(label="Copiar", command=lambda: copiar_dato(item))
        popup.add_command(label="Eliminar", command=lambda: eliminar_desde_popup(item))
        if not registro['favorito']:
            popup.add_command(label="Agregar favorito", command=lambda: favoritos(item, agregar=True, quitar=False))
        else:
            popup.add_command(label="Quitar favorito", command=lambda: favoritos(item, agregar=False, quitar=True))
        popup.tk_popup(event.x_root, event.y_root, None)



def copiar_dato(item):
    dato = " ".join(item)
    pyperclip.copy(dato)
    messagebox.showinfo("Hecho", "Registro copiado")



def eliminar_desde_popup(item):
    datos = {"nombre": item[0], "apellido": item[1], "numero": int(item[2]), "correo": item[3]}
    eliminar = messagebox.askquestion("Atención", "¿Desea eliminar este contacto? No se podrá deshacer")
    if eliminar:
        columna.delete_one(datos)
        messagebox.showinfo("Hecho", "Contacto eliminado con éxito")
        actualizar_tabla_y_base()
    else:
        pass



def favoritos(item, agregar, quitar):
    datos = {"nombre": item[0], "apellido": item[1], "numero": int(item[2]), "correo": item[3]}
    if agregar:
        datos_nuevos = {"$set": {"nombre": item[0], "apellido": item[1], "numero": int(item[2]), "correo": item[3], "favorito": True}}
        columna.update_one(datos, datos_nuevos)
        actualizar_tabla_y_base()
    if quitar:
        datos_nuevos = {"$set": {"nombre": item[0], "apellido": item[1], "numero": int(item[2]), "correo": item[3], "favorito": False}}
        columna.update_one(datos, datos_nuevos)
        actualizar_tabla_y_base()



def ver_favoritos(tabla):
    borrar()
    consulta = [{"$match": {"favorito": True}}]
    favoritos = columna.aggregate(consulta)
    for favorito in favoritos:
        tabla.insert("", "end", values=(favorito['nombre'], favorito['apellido'], favorito['numero'], favorito['correo']))



def importar():
    try:
        ruta = os.path.dirname(__file__)
        with open(f"{ruta}/archivos/contactos.json", "r") as archivo:
            columna.insert_many(json.load(archivo))
        messagebox.showinfo("Hecho", "Contactos importados con éxito")
        actualizar_tabla_y_base()
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo no encontrado")


