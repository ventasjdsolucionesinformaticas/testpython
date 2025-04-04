import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Configurar los detalles del servidor SMTP de Gmail
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Puerto seguro TLS

# Configurar tus credenciales de Gmail
email_address = 'scdepediatriacaldas@gmail.com'
password = 'vfpg rfch urmj bvhr'  # Considera usar métodos más seguros para almacenar contraseñas

# Diccionario que mapea destinatarios a archivos adjuntos
recipients_with_attachments = {
    'ventasjdsolucionesinformaticas@gmail.com': 'C:/Users/NESHORE_/OneDrive - Latinia Interactive Business, S.A/Escritorio/Adjuntos/jaime.txt'
}

# Ruta del archivo de log
log_file = 'C:/Users/NESHORE_/OneDrive - Latinia Interactive Business, S.A/Escritorio/Adjuntos/resultados.log'

# Función para adjuntar archivo
def attach_file(msg, filepath):
    if os.path.exists(filepath):
        with open(filepath, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filepath)}')
            msg.attach(part)
    else:
        print(f'El archivo {filepath} no existe.')

# Función para registrar mensajes en resultados.log
def log_message(message):
        with open(log_file, 'a') as log:
            log.write(message + '\n')

# Crear el mensaje MIME para cada destinatario y adjuntar su archivo correspondiente
for recipient, attachment_path in recipients_with_attachments.items():
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = recipient
    msg['Subject'] = 'Certificado Asistencia XVIII Jornadas de Pediatría CALDAS'

    # Contenido del mensaje
    body = '<p>Manizales, 25 de septiembre de 2024</p><p>Cordial saludo:</p><p>De manera grata me permito compartir certificado de asistencia a la XVIII Jornada de pediatría Sociedad colombiana de Pediatría – Regional Caldas.</p><p>Feliz noche.</p>'
    msg.attach(MIMEText(body, 'html'))

    # Adjuntar el archivo específico para el destinatario
    attach_file(msg, attachment_path)

    # Establecer la conexión SMTP y enviar el correo
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_address, password)
        server.send_message(msg)

     # Registrar en resultados.log
    log_message(f'Correo enviado a {recipient} con el archivo adjunto {attachment_path}')