import requests

# Configuración de WooCommerce API
#Se debe activar claves de aPi en woocomerce/avanzada
woocommerce_url = 'https://ginecologadianaalvarez.com/wp-json'
woocommerce_key = 'ck_2427f3ac596e18ef4096fec1728b96296ee1b8d6'  # Tu Consumer Key de WooCommerce
woocommerce_secret = 'cs_b7aca615c09d1b84a8c1c2149c191fe76c6bb726'  # Tu Consumer Secret de WooCommerce

# Endpoint de la API de WooCommerce para obtener los pedidos
endpoint_pedidos = '/wc/v3/orders'
url_api_woocommerce = woocommerce_url + endpoint_pedidos

# Parámetros de paginación inicial
pagina_actual = 1
por_pagina = 100  # Número máximo de pedidos por página (ajústalo según tus necesidades)

# Lista para almacenar todos los pedidos
todos_los_pedidos = []

while True:
    # Realizar la solicitud GET a la API de WooCommerce con autenticación OAuth 1.0a y parámetros de paginación
    response = requests.get(url_api_woocommerce, params={'page': pagina_actual, 'per_page': por_pagina},
                            auth=(woocommerce_key, woocommerce_secret))

    # Verificar si la solicitud fue exitosa (código de estado HTTP 200)
    if response.status_code == 200:
        # Convertir la respuesta JSON a una lista de diccionarios de Python
        pedidos = response.json()

        # Agregar los pedidos obtenidos a la lista todos_los_pedidos
        todos_los_pedidos.extend(pedidos)

        # Verificar si hay más páginas de resultados
        if len(pedidos) < por_pagina:
            # Ya no hay más páginas, salir del bucle
            break
        else:
            # Incrementar el número de página para la siguiente solicitud
            pagina_actual += 1
    else:
        print(f'Error al obtener los pedidos en la página {pagina_actual}. Código de estado: {response.status_code}')
        break

# Imprimir la cantidad total de pedidos obtenidos
cantidad_pedidos = len(todos_los_pedidos)
print(f'Cantidad total de pedidos: {cantidad_pedidos}')

# Escribir los detalles de los pedidos en un archivo de texto
nombre_archivo = 'pedidos_woocommerce.txt'

with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
    for pedido in todos_los_pedidos:
        archivo.write(f'ID del pedido: {pedido["id"]}\n')
        archivo.write(f'Fecha del pedido: {pedido["date_created"]}\n')
        archivo.write(f'Estado del pedido: {pedido["status"]}\n')
        archivo.write(f'Total del pedido: {pedido["total"]}\n')
        archivo.write(
            f'Cliente: {pedido["billing"]["first_name"]} {pedido["billing"]["last_name"]} ({pedido["billing"]["email"]})\n')
        archivo.write('--------------------------------------\n')
    archivo.write(f'Cantidad total de pedidos: {cantidad_pedidos}\n')

print(f'Los pedidos han sido guardados en {nombre_archivo}')
