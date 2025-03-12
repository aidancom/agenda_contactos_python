import os, csv, pyperclip, json, tkinter.colorchooser, re

from connection import columna, columna_2, columna_3
from tkinter import *
from tkinter import simpledialog, messagebox
from insert import insertar
from utils import *
from mail import correo


color_fondo, color_texto, color_texto_boton, color_botones, color_borde_normal, color_borde_resaltado, grosor_borde, tipo_borde = "", "", "", "", "", "", "", ""
validar_correo = r"[a-zA-Z0-9]+@[a-zA-Z0-9.-]+\.[a-z]{2,5}"


def actualizar_tabla_y_base():
    borrar_tabla(), cargar_tabla()

def insertar_datos():
    numero_registros = simpledialog.askinteger("Registros", "Introduce el numero de registros que deseas agregar")
    insertar(numero_registros)
    messagebox.showinfo("Hecho", "¡Datos cargados con éxito!")
    actualizar_tabla_y_base()



def vaciar():
    try:
        validar = simpledialog.askstring("Auntenticación", "Introduzca la contraseña para eliminar", show="*")
        if validar == 'admin99':
            opcion = messagebox.askquestion("Advertencia", "¿Seguro que desea vaciar la base de datos? Esta opción no se podra deshacer")
            if opcion == 'yes':
                columna.drop()
                messagebox.showinfo("Hecho", "¡Base de datos vaciada con éxito!")
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
        res = columna.aggregate([{"$match": {"numero": numero}}])
        contador = columna.count_documents({"numero": numero})
        if contador > 0:
            borrar_tabla()
            [tabla.insert("", "end", values=(registro['nombre'], registro['apellido'], registro['numero'], registro['correo'])) for registro in res]
        else:
            messagebox.showinfo("Sin registros", "No existe un contacto con ese número")
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
            if re.match(validar_correo, email) is not None:
                contacto = {"nombre": nombre, "apellido": apellido, "numero": numero, "correo": email, "favorito": False, "privado": False}
                columna.insert_one(contacto)
                messagebox.showinfo("Hecho", "Contacto añadido con éxito")
                [entrada.delete(0, END) for entrada in [nombre_entrada, apellido_entrada, numero_entrada, email_entrada]]
                actualizar_tabla_y_base()
            else:
                messagebox.showerror("Error", "Correo no válido")
        else:
            messagebox.showerror("Error", "No pueden haber campos vacíos")
    except ValueError:
        messagebox.showerror("Error", "Carácter no válido")
    except Exception as e:
        messagebox.showerror("Error", f"{e}")



def seleccion_contacto(nombre_entrada, apellido_entrada, numero_entrada, email_entrada, tabla):
    tabla_seleccion = tabla.selection()
    [entrada.delete(0, END) for entrada in [nombre_entrada, apellido_entrada, numero_entrada, email_entrada]]
    if tabla_seleccion:
        tabla_registro = (tabla.item(tabla_seleccion, "values"))
        nombre_entrada.insert(0, tabla_registro[0])
        apellido_entrada.insert(0, tabla_registro[1])
        numero_entrada.insert(0, tabla_registro[2])
        email_entrada.insert(0, tabla_registro[3])



def borrar_contacto(nombre_entrada, apellido_entrada, numero_entrada, email_entrada):
    if nombre_entrada.get() and apellido_entrada.get() and numero_entrada.get() and email_entrada.get():
        nombre = nombre_entrada.get().capitalize()
        apellido = apellido_entrada.get().capitalize()
        numero = numero_entrada.get()
        email = email_entrada.get().lower()
        if nombre and apellido and numero and email:
            contacto = {"nombre": nombre, "apellido": apellido, "numero": int(numero), "correo": email}
            alerta = messagebox.askquestion("Alerta", "¿Seguro que desea eliminar este campo?")
            if alerta == 'yes':
                columna.delete_one(contacto)
                columna_3.insert_one(contacto)
                messagebox.showinfo("Hecho", "¡Contacto eliminado con éxito!")
                [entrada.delete(0, END) for entrada in [nombre_entrada, apellido_entrada, numero_entrada, email_entrada]]
                actualizar_tabla_y_base()



def editar_contacto(nombre_entrada, apellido_entrada, numero_entrada, email_entrada, tabla):
    if nombre_entrada.get() and apellido_entrada.get() and numero_entrada.get() and email_entrada.get():
        seleccion = tabla.selection()
        tabla_registro = list((tabla.item(seleccion, "values")))
        numero_buscar = tabla_registro[2]

        nombre_actual = nombre_entrada.get().capitalize()
        apellido_actual = apellido_entrada.get().capitalize()
        numero_actual = numero_entrada.get()
        email_actual = email_entrada.get().capitalize()

        filtro = {"numero": int(numero_buscar)}
        datos_actuales = {"$set": {"nombre": nombre_actual, "apellido": apellido_actual, "numero": int(numero_actual), "correo": email_actual}}

        columna.update_one(filtro, datos_actuales)

        messagebox.showinfo("Hecho", "¡Contacto editado con éxito!")

        [entrada.delete(0, END) for entrada in [nombre_entrada, apellido_entrada, numero_entrada, email_entrada]]

        actualizar_tabla_y_base()



def exportar(tabla, exportar_csv, exportar_txt, exportar_json):
    ruta = os.getcwd()
    ruta_directorio = os.path.join(ruta, "archivos")

    if not os.path.exists(ruta_directorio):
        os.mkdir(ruta_directorio)

    if exportar_txt:
        with open(os.path.join(ruta_directorio, "contactos.txt"), "w") as archivo:
            for datos in tabla.get_children():
                dato = tabla.item(datos, "values")
                archivo.write(f"Nombre: {dato[0]}\nApellido: {dato[1]}\nTeléfono: {dato[2]}\nCorreo: {dato[3]}\n\n")
        abrir = messagebox.askquestion("Hecho", "¡Contactos exportados a txt con éxito!, ¿Quieres abrir el archivo?")
        if abrir:
            os.startfile(os.path.join(ruta_directorio, "contactos.txt"))
    if exportar_csv:
        with open(os.path.join(ruta_directorio, "contactos.csv"), "w", newline="") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(["Nombre", "Apellido", "Teléfono", "Correo"])
            for datos in tabla.get_children():
                dato = tabla.item(datos, "values")
                writer.writerow(dato)
        abrir = messagebox.askquestion("Hecho", "¡Contactos exportados a csv con éxito!, ¿Quieres abrir el archivo?")
        if abrir:
            os.startfile(os.path.join(ruta_directorio, "contactos.csv"))
    if exportar_json:
        datos_exportar = columna.find({})
        datos = []
        [datos.append({"nombre": dato['nombre'], "apellido": dato['apellido'], "numero": dato['numero'], "correo": dato['correo'], "favorito": dato['favorito'], "privado": dato['privado']}) for dato in datos_exportar]
        with open(os.path.join(ruta_directorio, "contactos.json"), "w") as archivo:
            json.dump(datos, archivo, indent=4)
        abrir = messagebox.askquestion("Hecho", "¡Contactos exportados a json con éxito!, ¿Quieres abrir el archivo?")
        if abrir:
            os.startfile(os.path.join(ruta_directorio, "contactos.json"))



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
        if not registro['privado']:
            popup.add_command(label="Hacer privado", command=lambda: privado(item, privado=True, publico=False))
        else:
            popup.add_command(label="Hacer público", command=lambda: privado(item, privado=False, publico=True))
        popup.tk_popup(event.x_root, event.y_root, None)



def privado(item, privado, publico):
    datos = {"nombre": item[0], "apellido": item[1], "numero": int(item[2]), "correo": item[3]}
    if privado:
        datos_nuevos = {"$set": {"privado": True}}
        columna.update_one(datos, datos_nuevos)
        actualizar_tabla_y_base()
    if publico:
        datos_nuevos = {"$set": {"privado": False}}
        columna.update_one(datos, datos_nuevos)
        actualizar_tabla_y_base()



def copiar_dato(item):
    dato = " ".join(item)
    pyperclip.copy(dato)
    messagebox.showinfo("Hecho", "Registro copiado")



def eliminar_desde_popup(item):
    datos = {"nombre": item[0], "apellido": item[1], "numero": int(item[2]), "correo": item[3]}
    eliminar = messagebox.askquestion("Atención", "¿Desea eliminar este contacto?")
    if eliminar == 'yes':
        columna.delete_one(datos)
        columna_3.insert_one(datos)
        messagebox.showinfo("Hecho", "¡Contacto eliminado con éxito!")
        actualizar_tabla_y_base()
    else:
        pass



def favoritos(item, agregar, quitar):
    datos = {"nombre": item[0], "apellido": item[1], "numero": int(item[2]), "correo": item[3]}
    if agregar:
        datos_nuevos = {"$set": {"favorito": True}}
        columna.update_one(datos, datos_nuevos)
        actualizar_tabla_y_base()
    if quitar:
        datos_nuevos = {"$set": {"favorito": False}}
        columna.update_one(datos, datos_nuevos)
        actualizar_tabla_y_base()



def ver_favoritos(tabla):
    consulta = [{"$match": {"favorito": True}}]
    favoritos = columna.aggregate(consulta)
    if columna.count_documents({"favorito": True}) == 0:
        messagebox.showinfo("Atención", "No hay contactos favoritos")
    else:
        borrar_tabla()
        for favorito in favoritos:
            tabla.insert("", "end", values=(favorito['nombre'], favorito['apellido'], favorito['numero'], favorito['correo']))



def acceso(tabla, root):

    root.attributes("-disabled", True)

    creedenciales = Toplevel(root)
    creedenciales.title("Acceso")
    creedenciales.resizable(False, False)

    marco_creedenciales = Frame(creedenciales, pady=10, padx=10)

    Label(marco_creedenciales, text="Acceso", font=("Arial", 15)).pack(pady=(0, 5))
    Label(marco_creedenciales, text="Usuario").pack(anchor='w')
    user = Entry(marco_creedenciales)
    user.pack(pady=(0, 10))
    Label(marco_creedenciales, text="Contraseña").pack(anchor='w')
    password = Entry(marco_creedenciales, show="*")
    password.pack(pady=(0, 10))
    Button(marco_creedenciales, text="Aceptar", command=lambda: ver_privados(root, tabla, user, password, creedenciales)).pack(anchor='e')

    marco_creedenciales.pack(fill="both", expand=1)

    creedenciales.protocol("WM_DELETE_WINDOW", lambda: cerrar(root, creedenciales))




def ver_privados(root, tabla, user, password, creedenciales):
    consulta = [{"$match": {"privado": True}}]
    privados = columna.aggregate(consulta)
    if columna.count_documents({"privado": True}) > 0:
        if user.get() == 'admin' and password.get() == 'admin':
            borrar_tabla()

            for privado in privados:
                tabla.insert("", "end",
                             values=(privado['nombre'], privado['apellido'], privado['numero'], privado['correo']))
            creedenciales.destroy()
            cerrar(root, creedenciales)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    else:
        messagebox.showinfo("Atención", "No hay contactos privados")
        creedenciales.destroy()
        cerrar(root, creedenciales)



def importar():
    try:
        ruta = os.getcwd()
        ruta_directorio = os.path.join(ruta, "archivos")
        with open(os.path.join(ruta_directorio, "contactos.json"), "r") as archivo:
            columna.insert_many(json.load(archivo))
        messagebox.showinfo("Hecho", "¡Contactos importados con éxito!")
        actualizar_tabla_y_base()
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo no encontrado")



def enviar_correo():
    email_destino = simpledialog.askstring("Información", "Escribe el correo al que quieras enviar los contactos")
    contactos = columna.find({})
    correo(email_destino, contactos)



def cerrar(root, ventana):
    root.attributes("-disabled", False)
    ventana.destroy()



def editor(root, nombre, apellido, numero, email, marco_izquierdo, marco_campos, marco_botones, nombre_entrada, apellido_entrada, numero_entrada, email_entrada, boton_editar, boton_borrar, boton_enviar):

    root.attributes("-disabled", True)

    ventana = Toplevel(root)
    ventana.title("Editor del programa")
    ventana.resizable(False, False)

    Label(ventana, text="Colores", font=("Arial", 20, "bold")).pack(pady=(10, 10), padx=(10, 10), anchor='w')

    marco_primero = Frame(ventana)
    marco_1 = Frame(marco_primero)
    marco_2 = Frame(marco_primero)

    Label(marco_1, text="Textos", font=5).pack(anchor='w', pady=(0, 10))
    Button(marco_1, text="Texto label", width=20, command=lambda: color(fondo=False, textos=True, botones=False, texto_botones=False)).pack(pady=(0, 10))
    Button(marco_1, text="Texto boton", width=20, command=lambda: color(fondo=False, textos=False, botones=False, texto_botones=True)).pack(pady=(0, 0))

    Label(marco_2, text="Fondos", font=5).pack(anchor='w', pady=(0, 10))
    Button(marco_2, text="Fondo boton", width=20, command=lambda: color(fondo=False, textos=False, botones=True, texto_botones=False)).pack(pady=(0, 10))
    Button(marco_2, text="Fondo programa", width=20, command=lambda: color(fondo=True, textos=False, botones=False, texto_botones=False)).pack(pady=(0, 0))

    marco_primero.pack()
    marco_1.pack(fill='x', anchor='w', pady=(0, 10), padx=(10, 10), side=LEFT)
    marco_2.pack(fill='x', anchor='w', pady=(0, 10), padx=(10, 10), side=LEFT)
    Button(ventana, text="Aceptar", command=lambda: editor_ventana(ventana, root, nombre, apellido, numero, email, marco_izquierdo, marco_campos, marco_botones, boton_editar, boton_borrar, boton_enviar)).pack(padx=(5, 10), pady=(0, 10), anchor='e')

    ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar(root, ventana))



def backup(root):
    datos = columna.find({})
    backup = []
    ruta = os.getcwd()
    ruta_directorio = os.path.join(ruta, "backup")
    if not os.path.exists(ruta_directorio):
        os.mkdir(ruta_directorio)
    [backup.append({"nombre": dato['nombre'], "apellido": dato['apellido'], "numero": dato['numero'], "correo": dato['correo'], "favorito": dato['favorito'], "privado": dato['privado']}) for dato in datos]

    with open(os.path.join(ruta_directorio, "backup.json"), "w", encoding="utf-8") as archivo:
        json.dump(backup, archivo, indent=4)

    root.destroy()



def color(fondo, textos, botones, texto_botones):
    global color_fondo, color_texto, color_botones, color_texto_boton
    if fondo:
        colors = tkinter.colorchooser.askcolor()
        color_fondo = colors[1]
    if textos:
        colors = tkinter.colorchooser.askcolor()
        color_texto = colors[1]
    if botones:
        colors = tkinter.colorchooser.askcolor()
        color_botones = colors[1]
    if texto_botones:
        colors = tkinter.colorchooser.askcolor()
        color_texto_boton = colors[1]



def editor_ventana(ventana, root, nombre, apellido, numero, email, marco_izquierdo, marco_campos, marco_botones, boton_editar, boton_borrar, boton_enviar):
    global color_fondo, color_texto, color_botones, texto_botones
    if color_fondo:
        [cambio.config(bg=color_fondo) for cambio in [root, marco_campos, marco_botones, marco_izquierdo, nombre, apellido, numero, email]]

    if color_texto:
        [cambio.config(fg=color_texto) for cambio in [nombre, apellido, numero, email]]

    if color_botones:
        [cambio.config(bg=color_botones) for cambio in [boton_editar, boton_borrar, boton_enviar]]

    if color_texto_boton:
        [cambio.config(fg=color_texto_boton) for cambio in [boton_editar, boton_borrar, boton_enviar]]


    colores = {'colorBackground': color_fondo, 'colorText': color_texto, 'colorButtonText': color_texto_boton, 'colorButton': color_botones}
    columna_2.drop()
    columna_2.insert_one(colores)
    cerrar(root, ventana)



def modo(root, nombre, apellido, numero, email, marco_izquierdo, marco_campos, marco_botones, boton_editar, boton_borrar, boton_enviar, claro, oscuro):
    if oscuro:
        [cambio.config(bg="#000000") for cambio in [root, marco_campos, marco_botones, marco_izquierdo, nombre, apellido, numero, email, boton_editar, boton_borrar, boton_enviar]]
        [cambio.config(bg="#FFFFFF") for cambio in [nombre, apellido, numero, email, boton_editar, boton_borrar, boton_enviar]]
        colores = {'colorBackground': "#000000", 'colorText': "#FFFFFF", 'colorButtonText': "#FFFFFF", 'colorButton': "#000000"}
        columna_2.drop()
        columna_2.insert_one(colores)
    if claro:
        [cambio.config(bg="#FFFFFF") for cambio in [root, marco_campos, marco_botones, marco_izquierdo, nombre, apellido, numero, email, boton_editar, boton_borrar, boton_enviar]]
        [cambio.config(bg="#000000") for cambio in [nombre, apellido, numero, email, boton_editar, boton_borrar, boton_enviar]]
        colores = {'colorBackground': "#FFFFFF", 'colorText': "#000000", 'colorButtonText': "#000000", 'colorButton': "#FFFFFF"}
        columna_2.drop()
        columna_2.insert_one(colores)



def eliminados(root):
    contactos_eliminados = columna_3.find({})
    datos = []
    root.attributes("-disabled", True)
    [datos.append({"nombre": eliminado['nombre'], "apellido": eliminado['apellido'], "numero": eliminado['numero'], "correo": eliminado['correo'], "favorito": False, "privado": False}) for eliminado in contactos_eliminados]

    ventana = Toplevel(root)
    ventana.resizable(False, False)
    marco_texto = Frame(ventana, pady=5)
    marco_boton = Frame(ventana, pady=10)

    caja = Text(marco_texto, padx=10, pady=10, width=60, height=10)
    [caja.insert(END, f"{dato['nombre']} - {dato['apellido']} - {dato['numero']} - {dato['correo']}\n") for dato in datos]

    Button(marco_boton, text="Reestablecer contactos", command=lambda: reestablecer(datos, caja, ventana, root)).pack()

    marco_texto.pack()
    marco_boton.pack()
    caja.pack()
    ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar(root, ventana))
    ventana.mainloop()



def reestablecer(datos, caja, ventana, root):

    if len(datos) == 0:
        messagebox.showinfo("Atención", "No hay contactos eliminados")
    else:
        columna.insert_many(datos)
        columna_3.drop()
        messagebox.showinfo("Hecho", "¡Contactos recuperados con éxito!")
        caja.delete("1.0", END)
        actualizar_tabla_y_base()
        ventana.destroy()
    cerrar(root, ventana)

