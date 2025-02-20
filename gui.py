from connection import columna
from tkinter import *
from tkinter.ttk import Treeview



##### CREAR WIDGETS Y EL ROOT #####

root = Tk()
root.title("Agenda de contactos")

marco_derecho = Frame(root)
marco_izquierdo = Frame(root)

marco_campos = Frame(marco_izquierdo)
marco_botones = Frame(marco_izquierdo)

nombre = Label(marco_campos, text="Nombre")
apellido = Label(marco_campos, text="Apellido")
numero = Label(marco_campos, text="Télefono")
email = Label(marco_campos, text="Correo Electronico")

nombre_entrada = Entry(marco_campos)
apellido_entrada = Entry(marco_campos)
numero_entrada = Entry(marco_campos)
email_entrada = Entry(marco_campos)

boton_enviar = Button(marco_botones, text="Enviar")
boton_borrar = Button(marco_botones, text="Borrar")
boton_editar = Button(marco_botones, text="Editar")

cabecera = ("Nombre", "Apellido", "Número", "Correo")
tabla = Treeview(marco_derecho, columns=cabecera, show="headings")
for insert in cabecera:
    tabla.column(column=insert, width=100)
    tabla.heading(insert, text=insert)

menu = Menu(root, tearoff=0)
submenu_1 = Menu(menu, tearoff=0)
submenu_1.add_command(label="Buscar")
menu.add_cascade(label="Opciones", menu=submenu_1)


##### CARGAR WIDGETS EN ROOT #####


for boton in [boton_enviar, boton_borrar, boton_editar]:
    boton.pack(side=LEFT, padx=(0, 10))

tabla.pack(fill="both", expand=1)

nombre.grid(row=0, column=0, sticky="w")
apellido.grid(row=0, column=1, sticky="w", padx=(10, 0))
numero.grid(row=2, column=0, sticky="w")
email.grid(row=2, column=1, sticky="w", padx=(10, 0))

nombre_entrada.grid(row=1, column=0)
apellido_entrada.grid(row=1, column=1, padx=(10, 0))
numero_entrada.grid(row=3, column=0)
email_entrada.grid(row=3, column=1, padx=(10, 0))

marco_izquierdo.pack(side=LEFT, padx=10)
marco_derecho.pack(fill="both", expand=1, side=LEFT)

marco_campos.pack(fill="x", expand=1)
marco_botones.pack(fill="x", expand=1, side=BOTTOM, anchor="w", pady=(10, 0))

root.config(menu=menu)
root.mainloop()

