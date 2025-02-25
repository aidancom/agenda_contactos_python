import random
from connection import columna

def insertar(numero_registros):
    nombre = ['Antonio', 'Alfredo', 'Alicia', 'Raúl', 'Aidan', 'Liam', 'Manuel', 'Jose', 'Carlos', 'Luis', 'María', 'Marta', 'Carol', 'Kathe', 'Valeria', 'Valentina', 'Rocío', 'Inma']
    apellido = ['García', 'Vázquez', 'Verdejo', 'Rodríguez', 'Heredia', 'López', 'Piera', 'Guillem', 'Maynero', 'Saéz', 'Cuenca']
    correo = ['gmail.com', 'yahoo.es', 'outlook.com', 'hotmail.com', 'zoho.com', 'tutanota.com', 'live.com', 'mail.com', 'gmail.es']

    contador = 0

    while True:
        nombre_registro = random.choice(nombre)
        apellido_registro = random.choice(apellido)
        numero_registro = random.randint(900000000, 999999999)
        correo_registro = f"{random.randint(000, 999)}{nombre_registro.lower()}{random.randint(000, 999)}{random.choice(correo)}"

        dato = {
            "nombre": nombre_registro,
            "apellido": apellido_registro,
            "numero": int(numero_registro),
            "correo": correo_registro,
            "favorito": False,
            "privado": False
        }

        columna.insert_one(dato)

        contador += 1

        if contador == numero_registros:
            break
        else:
            continue