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