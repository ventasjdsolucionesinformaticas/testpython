##CRIBA SU CÓDIGO A PARTIR DE AQUÍ ### (~ 11 líneas de código)

# Entrada del programa (~ 1 línea).
cadena = input ("ingrese una cadena de texto cidini:")           # Reemplace 'None' por el código necesario. 

# Operaciones en cadenas de texto (~ 9 líneas)
resultado = cadena.replace('a','i').replace('e','i').replace('o','i').replace('Á','Í').replace('á','Í').replace('É','Í').replace('é','Í').replace('Ó','Í').replace('ó','Í').lower()

# Salida del programa (~ 1 línea).
print(resultado)
