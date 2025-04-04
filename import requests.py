import requests

url = "https://api.tempo.io/4/worklogs"
headers = {
    "Authorization": "Bearer 5JuJowZyyiaNR6MvtBjV2cJuNwysyI-eu",
    "Content-Type": "application/json"
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    try:
        data = response.json()
        print(data)
    except requests.exceptions.JSONDecodeError:
        print("La respuesta no contiene JSON válido.")
else:
    print(f"Error {response.status_code}: {response.text}")  # Muestra el cuerpo de la respuesta