from twilio.rest import Client
def enviar_mensaje_whatsapp(mensaje, numero_telefono):
    # Crea una instancia del cliente de Twilio
    account_sid = 'TU_ACCOUNT_SID'
    auth_token = 'TU_AUTH_TOKEN'
    client = Client(account_sid, auth_token)

    # Envía el mensaje de WhatsApp
    message = client.messages.create(
        body=mensaje,
        from_='whatsapp:+NUMERO_DE_ORIGEN',
        to=f'whatsapp:{numero_telefono}'
    )

    print(f'Mensaje enviado a {numero_telefono}: {message.sid}')

    def procesar_seleccion(seleccion):
        # Define la lista de productos con sus precios
        productos = {
            1: {'nombre': 'Producto 1', 'precio': 10},
            2: {'nombre': 'Producto 2', 'precio': 15},
            3: {'nombre': 'Producto 3', 'precio': 20},
            # Agrega más productos si es necesario
        }

        # Separa los números seleccionados
        numeros_seleccionados = [int(num) for num in seleccion.split(',')]

        # Calcula el total de los productos seleccionados
        total = sum(productos[numero]['precio'] for numero in numeros_seleccionados)

        # Genera el mensaje con los productos seleccionados y el total
        mensaje = 'Productos seleccionados:\n'
        for numero in numeros_seleccionados:
            producto = productos[numero]
            mensaje += f'{producto["nombre"]}: ${producto["precio"]}\n'
        mensaje += f'Total: ${total}'

        return mensaje

    seleccion = input('Ingrese los números de los productos seleccionados separados por comas: ')
    mensaje = procesar_seleccion(seleccion)
    numero_telefono = 'NUMERO_DESTINO'  # Reemplaza con el número de teléfono al que deseas enviar el mensaje
    enviar_mensaje_whatsapp(mensaje, numero_telefono)