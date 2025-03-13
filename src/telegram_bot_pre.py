## Este codigo:

import requests
import time
import pandas as pd
from telegram import ReplyKeyboardMarkup, KeyboardButton

# Configuración de Telegram
TOKEN = '6820EDQXIl71R4'
chat_id = 2088032855

# Configuración de Jira Cloud
jira_url = 'https://emmac2.atlassian.net'
username = 'emmanuel.c2@gmail.com'
api_token = 'ATATT3xFfG05EUU5AQ5MzNIzk=69788AF4'  # Reemplaza con tu API token

# Inicialización del DataFrame con las preguntas como columnas
columns = ["Tipo de Incidencia", "Asunto del incidente", "Descripción del Incidente", "Responsable de la tarea", "Hora de Envío", "Hora de Recepción"]
df = pd.DataFrame(columns=columns)

# Función para enviar mensaje a Telegram
def enviar_mensaje(chat_id, mensaje, teclado=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    if teclado:
        data = {"chat_id": chat_id, "text": mensaje, "reply_markup": teclado.to_json()}
    else:
        data = {"chat_id": chat_id, "text": mensaje}
    response = requests.post(url, json=data)
    return response.json()

# Función para esperar respuesta de Telegram
def esperar_respuesta(chat_id, marca_tiempo_pregunta):
    while True:
        time.sleep(0.2)
        url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
        params = {"chat_id": chat_id}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['result']:
                for mensaje in data['result']:
                    fecha_hora_mensaje = mensaje['message']['date']
                    if fecha_hora_mensaje >= marca_tiempo_pregunta:
                        return mensaje['message']['text']

# Función para mapear el tipo de incidencia a su ID en Jira
def mapear_tipo_incidencia_a_id(tipo_incidencia):
    tipos_incidencia_jira = {
        "Epic": "10000",
        "Tarea": "10002",
        "Historia": "10001",
        "Error": "10004",
        "Subtarea": "10003"
    }
    return tipos_incidencia_jira.get(tipo_incidencia, "10001")  # Default a 'Historia' si no se encuentra

# ...

# Función para crear una incidencia en Jira
def crear_incidencia_en_jira(datos_incidencia):
    auth = (username, api_token)
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    # Asegúrate de que la descripción está en formato UTF-8
    descripcion_texto = datos_incidencia['Descripción del Incidente'].encode('utf-8').decode('utf-8')

    descripcion_formateada = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "text": descripcion_texto,
                        "type": "text"
                    }
                ]
            }
        ]
    }

    data = {
        "fields": {
            "project": {"key": "JMF"},
            "summary": datos_incidencia['Asunto del incidente'],
            "description": descripcion_formateada,
            "issuetype": {"id": mapear_tipo_incidencia_a_id(datos_incidencia['Tipo de Incidencia'])}
        }
    }

    response = requests.post(f'{jira_url}/rest/api/3/issue/', json=data, auth=auth, headers=headers)

    if response.status_code == 201:
        issue_key = response.json()['key']
        mensaje_exito = f'Su incidencia: {issue_key} ha sido creada correctamente.'
        enviar_mensaje(chat_id, mensaje_exito)
        print(f'Incidencia creada exitosamente. Número de incidencia: {issue_key}')
    else:
        print(f'Error al crear la incidencia. Código de respuesta: {response.status_code}')
        print(response.text)

# ...


# Inicio del script principal
if __name__ == '__main__':
    preguntas = [
        "Ingrese el tipo de Incidencia que desea crear:",
        "Asunto del incidente:",
        "Descripción del Incidente:",
        "¿Quién es el responsable de la tarea?"
    ]s

    # Teclados personalizados
    opciones_tipo_incidencia = ["Epic", "Tarea", "Historia", "Error", "Subtarea"]
    teclado_incidencia = ReplyKeyboardMarkup([[KeyboardButton(opcion)] for opcion in opciones_tipo_incidencia], one_time_keyboard=True)

    opciones_responsable = ["Emmanuel", "Miriam", "Yorleny", "Abigail"]
    teclado_responsable = ReplyKeyboardMarkup([[KeyboardButton(opcion)] for opcion in opciones_responsable], one_time_keyboard=True)

    # Diccionario para almacenar las respuestas
    respuestas = {}

    for i, pregunta in enumerate(preguntas):
        teclado_actual = teclado_incidencia if i == 0 else teclado_responsable if i == 3 else None
        enviar_mensaje(chat_id, pregunta, teclado_actual)
        marca_tiempo_pregunta = time.time()
        respuesta = esperar_respuesta(chat_id, marca_tiempo_pregunta)
        respuestas[columns[i]] = respuesta
        respuestas["Hora de Recepción"] = time.ctime(marca_tiempo_pregunta)
        if i == 0:
            respuestas["Hora de Envío"] = respuestas["Hora de Recepción"]

    # Crear la incidencia en Jira con los datos recogidos
    crear_incidencia_en_jira(respuestas)