bodega = (input('Ingrese el numero de la bodega: '))
categoria = (input('Ingrese el numero de la categoria: '))
ceros = str ('000')
primercodigo= str (1)
consecutivo = bodega + ceros + categoria + primercodigo        
archivo = "codigos.txt"
salida = "result.txt"
lineas_escribir = []
with open(archivo, "r") as archivo_lectura:
    numero_linea = 0
    for linea in archivo_lectura:
        numero_linea += 1
        linea = linea.rstrip()
        separado = linea.split(" ")
        if consecutivo in separado:
            print(f"El codigo {consecutivo} ya existe ")
            break
    else:
        with open(salida, "a") as archivo_salida:
            archivo_salida.write(consecutivo + "\n")
            print("Se agegó con exito el codigo " + consecutivo)
