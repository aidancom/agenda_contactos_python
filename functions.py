from connection import columna
from tkinter import *
from tkinter import simpledialog, messagebox
from insert import insertar
from utils import *



def insertar_datos():
    numero_registros = simpledialog.askinteger("Registros", "Introduce el numero de registros que deseas agregar")
    insertar(numero_registros)
    messagebox.showinfo("Hecho", "Datos cargados con éxito")
    borrar()
    cargar()



def vaciar():
    try:
        validar = simpledialog.askstring("Auntenticación", "Introduzca la contraseña para eliminar", show="*")
        if validar == 'admin99':
            opcion = messagebox.askquestion("Advertencia", "¿Seguro que desea vaciar la base de datos? Esta opción no se podra deshacer")
            if opcion == 'yes':
                columna.drop()
                messagebox.showinfo("Hecho", "Base de datos vaciada con éxito")
                borrar()
                cargar()
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
            contacto = {"nombre": nombre, "apellido": apellido, "numero": numero, "email": email, "favorito": False}
            columna.insert_one(contacto)
            messagebox.showinfo("Hecho", "Contacto añadido con éxito")
            borrar()
            cargar()
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

    borrar()
    cargar()