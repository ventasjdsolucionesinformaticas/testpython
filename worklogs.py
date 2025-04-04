import requests

url = "https://api.tempo.io/4/worklogs"
headers = {
    "Authorization": "Bearer 5JuJowZyyiaNR6MvtBjV2cJuNwysyI-eu",
    "Content-Type": "application/json"
}
# Lista de worklogs a registrar
worklogs = [
    {
        "issueId": "31692",
        "timeSpentSeconds": 3600,
        "startDate": "2025-02-12",
        "startTime": "10:00:00",
        "description": "016|Seguimiento a pendiente y/o acciones en los tickets",
        "authorAccountId": "6422fa38b05b4e3e7dab8316"
    },
    {
        "issueId": "31849",
        "timeSpentSeconds": 10800,
        "startDate": "2025-02-12",
        "startTime": "11:00:00",
        "description": "021|Tiempo dedicado a la preparación de componentes y su entrega",
        "authorAccountId": "6422fa38b05b4e3e7dab8316"
    },
    {
        "issueId": "18459",
        "timeSpentSeconds": 7200,
        "startDate": "2025-02-12",
        "startTime": "14:00:00",
        "description": "020|Sesiones internas de laboratorios, aprendizaje, documentación. (L)",
        "authorAccountId": "6422fa38b05b4e3e7dab8316"
    },
    {
        "issueId": "32040",
        "timeSpentSeconds": 3600,
        "startDate": "2025-02-12",
        "startTime": "14:00:00",
        "description": "",
        "authorAccountId": "6422fa38b05b4e3e7dab8316"
    }
]

# Iterar sobre la lista de worklogs y enviarlos
for worklog in worklogs:
    response = requests.post(url, json=worklog, headers=headers)
    print(f"Issue {worklog['issueId']}: {response.status_code} - {response.json()}")