from num2words import num2words
numero = input("Ingrese el numero a convertir: ")
texto = num2words(numero, lang='es')
print(texto + " pesos mcte")