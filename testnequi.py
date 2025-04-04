import requests

# Reemplaza con la URL correcta de tu API
API_URL = "https://api.nequi.com.co/tu_endpoint"
access_token = "eyJraWQiOiJuZVhiaFBIVkREV3IxXC9sZTl2YVdVQ0laNHlrSHZsUkF0bjFGajBRSVU3WT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI1ZWdhNW5pYWY3NzFkZmVqZ2NiZzQycmY2NCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXBpXC90aGlyZHBhcnR5YXBwcyBhcGlcL2FnZW50cyBhcGlcL25vdGlmaWNhdGlvbnMgYXBpXC9wYXJ0bmVycyBhcGlcL21vbmV5bWFuYWdlbWVudCBhcGlcL3BheW1lbnRzIGFwaVwvc3Vic2NyaXB0aW9ucyBhcGlcL3JlcG9ydHMgYXBpXC9kaXNwZXJzaW9ucyBhcGlcL2V4dGVybmFscGF5bWVudHMgYXBpXC90cmFuc3BvcnQgYXBpXC9naWZ0Y29kZXMiLCJhdXRoX3RpbWUiOjE3MTg5NzkwNjcsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX202b21PQnFDWSIsImV4cCI6MTcxODk4MjY2NywiaWF0IjoxNzE4OTc5MDY3LCJ2ZXJzaW9uIjoyLCJqdGkiOiI3ZWE2MGYyMi1jZjI0LTRlZTgtYmFmNi1lZWI1YmY1ZjZkZjciLCJjbGllbnRfaWQiOiI1ZWdhNW5pYWY3NzFkZmVqZ2NiZzQycmY2NCJ9.oMURYH14LsAft6JuJduKlDKQi5FoApwwvysUVJZTTy1M1Npq-qx_Ea5u5bELfP8jITQ53mNdqdwCzd99gJwghSgayy8RX_cYzYLssWYazU7v6Ilq3W1bOhTmpX3424NAe0BNyfMvXAbeevivSmmkFuiwhoCXTwTfpWpcYMCSRQZbcIGJ5QP5DJfPFuMMzabooJYKOHzi-RszHODuTDRqBXZjF9HIxcAGo3W5WFCrtZtmqnxjeGN2UWE-UdmkpfIImVysrJgZobvJ6E0IGCda7MJtd7QKwbbvs3jPOoEAYU56AWBXdbWTNHRI8ImsBI_1F_2kHyai4HWEvEnU1cTY3A"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

try:
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP 4xx/5xx
    print("Request successful:", response.json())
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
except requests.exceptions.Timeout as timeout_err:
    print(f"Timeout error occurred: {timeout_err}")
except requests.exceptions.RequestException as req_err:
    print(f"An error occurred: {req_err}")