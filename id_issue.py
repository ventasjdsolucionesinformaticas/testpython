import base64
import requests

# Credenciales
EMAIL = "jdiaz@latinia.com"
API_TOKEN = "5JuJowZyyiaNR6MvtBjV2cJuNwysyI-eu"
JIRA_URL = "https://latinia.atlassian.net"
TEMPO_URL = "https://api.tempo.io/core/3/worklogs"

# Datos de la tarea
ISSUE_KEY = "LATSUP-4756"  # Reemplaza con el Issue Key correcto
AUTHOR_ACCOUNT_ID = "6422fa38b05b4e3e7dab8316"  # Tu ID de usuario en Jira/Tempo

# 1️⃣ Obtener el issueId desde el issueKey
auth_header = base64.b64encode(f"{EMAIL}:{API_TOKEN}".encode()).decode()
HEADERS_JIRA = {
    "Authorization": f"Basic {auth_header}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

response = requests.get(f"{JIRA_URL}/rest/api/3/issue/{ISSUE_KEY}", headers=HEADERS_JIRA)

if response.status_code == 200:
    issue_data = response.json()
    issue_id = issue_data.get("id")
    print(f"🔹 Issue ID obtenido: {issue_id}")
else:
    print(f"❌ Error al obtener issueId: {response.status_code} - {response.text}")
    exit()

# 2️⃣ Enviar request a la API de Tempo para registrar el tiempo
HEADERS_TEMPO = {
    "Authorization": f"Basic {auth_header}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

payload = {
    "attributes": [{"key": "_COLOR_", "value": "green"}],
    "authorAccountId": AUTHOR_ACCOUNT_ID,
    "billableSeconds": 3600,  # 1 hora facturable
    "bypassPeriodClosuresAndApprovals": True,
    "description": "Investigación sobre la base de datos externa",
    "issueId": issue_id,  # Usamos el ID obtenido
    "remainingEstimateSeconds": 120,
    "startDate": "2024-02-11",  # Fecha actualizada
    "startTime": "10:00:00",  # Hora de inicio
    "timeSpentSeconds": 3600  # Tiempo trabajado (1 hora)
}

response = requests.post(TEMPO_URL, json=payload, headers=HEADERS_TEMPO)

if response.status_code == 200 or response.status_code == 201:
    print("✅ Tiempo registrado correctamente en Tempo")
else:
    print(f"❌ Error al registrar tiempo: {response.status_code} - {response.text}")
