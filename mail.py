import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox

def correo(email_destino, contactos):
    sender = '19aidan99@gmail.com'
    password = 'ypkc amhe njxh otyt'
    server = 'smtp.gmail.com'
    port = 465
    to = email_destino

    message = MIMEMultipart("alternative")
    message["Subject"] = "Contactos"
    message["From"] = sender
    message["To"] = to

    body = "Listado de contactos"

    for contacto in contactos:
        body += f"Nombre: {contacto['nombre']}\nApellido: {contacto['apellido']}\nTeléfono: {contacto['numero']}\nCorreo electrónico: {contacto['correo']}\nFavorito: {'Si' if contacto['favorito'] else 'No'}\n\n"

    part = MIMEText(body, "plain")
    message.attach(part)

    try:
        smtp_server = smtplib.SMTP_SSL(server, port)
        smtp_server.ehlo()
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, to, message.as_string())
        smtp_server.close()
        messagebox.showinfo("Hecho", "Mensaje enviado con éxito")
    except TypeError:
        pass
    except Exception as e:
        messagebox.showerror("Error", "Correo no válido")