import requests
import json
import os

# Configurar API
url = "https://api.tempo.io/4/worklogs"
headers = {
    "Authorization": "Bearer Hutjs9YiIf2nvet2uj0uCP0fMD66iL-eu",
    "Content-Type": "application/json"
}

# Leer y enviar los datos línea por línea
os.chdir("c:/DiscoD/Curso python Unacional/python") #Coloca aqui la ruta donde se encuentra el archivo worklogs.json.
print(os.getcwd()) #Verifica el cambio.
with open("worklogs.json", mode="r", encoding="utf-8") as file:
    for line in file:
        worklog = json.loads(line.strip())  # Convertir la línea en un diccionario
        response = requests.post(url, json=worklog, headers=headers)

        # Imprimir el resultado de cada solicitud
        print(f"Issue {worklog['issueId']}: {response.status_code} - {response.json()}")