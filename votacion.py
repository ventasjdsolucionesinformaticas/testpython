n = int(input())

candidatos = {}

for i in range(n): names = input() 
if names in candidatos: candidatos[names] += 1 
else: candidatos[names] = 1

valor_max = max(candidatos.values()) 
votos = tuple(candidatos.values()) 
dato = votos.count(valor_max) 
nombres = tuple(candidatos.keys())

if dato > 2: print('EMPATE')

else: posicion = votos.index(valor_max) 
resultado = nombres[posicion] 
print(resultado)5
