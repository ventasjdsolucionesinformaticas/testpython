import base64

# Reemplaza estos valores con tus credenciales
CLIENT_ID = "5ega5niaf771dfejgcbg42rf64"
CLIENT_SECRET = "459hgha3hqqaoca7mlh41mjhcq4kva06djd451apdqp97repa6r"
#apyy: kwPodOPY1O2DFRtBSfU6u91DBORteGnrS9S1Gjud
#Basic NWVnYTVuaWFmNzcxZGZlamdjYmc0MnJmNjQ6NDU5aGdoYTNocXFhb2NhN21saDQxbWpoY3E0a3ZhMDZkamQ0NTFhcGRxcDk3cmVwYTZy

# Codifica las credenciales en Base64
credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

# Imprime el valor del encabezado Authorization
print(f"Authorization: Basic {encoded_credentials}")