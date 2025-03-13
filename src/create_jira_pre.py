import os
import pandas as pd
from extract_msg import Message
from bs4 import BeautifulSoup
import pyodbc
import requests
from fuzzywuzzy import fuzz
import logging

# Configuración de la conexión a SQL Server
server = '10.136.2.76,58523'
database = 'TEST_DB'

# Configuración de Jira Cloud
jira_url = 'https://emc-latam.atlassian.net'
username = 'emmanuel.mora@emc-latam..com'
api_token = 'ATATTD6BqmZ8nVLAc47XPTw'

# Ruta de red en formato crudo (raw string)
ruta_red = r'\\10.136.00.00\BackUps\Mensajes_Correos\\'

# Número de resultados por página
results_per_page = 50  # Puedes ajustar esto según tus necesidades
# Inicializa la variable start_at en 0
start_at = 0

# Crear un DataFrame para almacenar los datos de usuarios Jira
df_users = pd.DataFrame(columns=['DisplayName', 'AccountId'])

while True:
    get_users_url = f'{jira_url}/rest/api/3/users/search?startAt={start_at}&maxResults={results_per_page}'
    auth = (username, api_token)

    response = requests.get(get_users_url, auth=auth)

    if response.status_code == 200:
        users = response.json()
        if not users:
            # No hay más usuarios, sal del bucle
            break

        for user in users:
            user_display_name = user['displayName']
            user_account_id = user['accountId']
            print(f'Nombre de usuario: {user_display_name}, ID de cuenta de usuario: {user_account_id}')

            # Agregar los datos al DataFrame
            df_users = df_users.append({'DisplayName': user_display_name, 'AccountId': user_account_id}, ignore_index=True)

        # Incrementa el valor de start_at para obtener la siguiente página de resultados
        start_at += results_per_page
    else:
        print(f'Error al obtener la lista de usuarios. Código de respuesta: {response.status_code}')
        print(response.text)

# Mostrar el DataFrame de usuarios Jira
print(df_users)

# Configuración de logging
logging.basicConfig(filename='jira_import.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Función para encontrar el ID del usuario por similitud de cadenas
def encontrar_id_usuario(nombre_remitente, df_usuarios):
    # Extraer el nombre del remitente sin la dirección de correo electrónico
    remitente_nombre = nombre_remitente.split('<')[0].strip()

    # Calcular las mejores coincidencias con los nombres en el DataFrame
    mejores_coincidencias = df_usuarios['DisplayName'].apply(lambda x: fuzz.ratio(remitente_nombre.lower(), x.lower()))

    # Obtener el índice de la mejor coincidencia
    indice_mejor_coincidencia = mejores_coincidencias.idxmax()

    # Puedes establecer un umbral de similitud para considerar la coincidencia
    umbral_similitud = 80

    print(f'Remitente: {nombre_remitente}')
    print(f'Mejores coincidencias: {mejores_coincidencias}')

    if mejores_coincidencias[indice_mejor_coincidencia] >= umbral_similitud:
        account_id = df_usuarios.loc[indice_mejor_coincidencia, 'AccountId']
        print(f'Coincidencia encontrada. AccountId: {account_id}')
        return account_id
    else:
        print('No se encontró una coincidencia suficientemente buena.')
        return 'informador_por_defecto'

# Función para borrar archivos .msg en la ruta especificada
def borrar_archivos_msg(ruta):
    archivos_msg = [archivo for archivo in os.listdir(ruta) if archivo.endswith('.msg')]
    for archivo in archivos_msg:
        archivo_path = os.path.join(ruta, archivo)
        os.remove(archivo_path)
        print(f"Archivo {archivo} eliminado.")

# Llamar a la función para listar y extraer información de archivos .msg
def listar_y_extraer_msg(ruta, df_usuarios):
    data = {
        'ID': [],
        'Asunto': [],
        'Remitente': [],
        'Destinatarios': [],
        'Fecha de envío': [],
        'Cuerpo del mensaje': [],
        'AccountId': []
    }

    try:
        archivos_msg = [archivo for archivo in os.listdir(ruta) if archivo.endswith('.msg')]

        if not archivos_msg:
            print("No se encontraron archivos .msg en la ruta proporcionada.")
        else:
            print("Archivos .msg en la ruta proporcionada:")
            for archivo in archivos_msg:
                archivo_path = os.path.join(ruta, archivo)
                print(archivo)

                with open(archivo_path, 'rb') as f:
                    msg = Message(f)
                    data['ID'].append(archivo)  # Agregar el campo ID con el nombre del archivo .msg
                    data['Asunto'].append(msg.subject)
                    data['Remitente'].append(msg.sender)
                    data['Destinatarios'].append(msg.to)
                    data['Fecha de envío'].append(msg.date)

                    # Procesar el cuerpo del mensaje HTML
                    soup = BeautifulSoup(msg.body, 'html.parser')
                    body_text = soup.get_text()

                    # Obtener el AccountId correspondiente al remitente
                    account_id = encontrar_id_usuario(msg.sender, df_users)

                    # Agregar el remitente al inicio del cuerpo del mensaje en la descripción de Jira
                    body_with_sender = f'Remitente: {msg.sender}\n\n{body_text[:5000]}'

                    # Agregar los datos al DataFrame
                    data['Cuerpo del mensaje'].append(body_with_sender)
                    data['AccountId'].append(account_id)

                print("------")

    except FileNotFoundError:
        print(f"La ruta {ruta} no existe.")
    except PermissionError:
        print(f"No tienes permisos para acceder a la ruta {ruta}.")
    except Exception as e:
        error_message = f"Ocurrió un error: {e}"
        print(error_message)
        logging.error(error_message)

    df = pd.DataFrame(data)
    return df

# Llamar a la función para listar y extraer información de archivos .msg
df = listar_y_extraer_msg(ruta_red, df_users)

# Mostrar el DataFrame de mensajes
print(df)

# Configuración de la conexión a SQL Server con autenticación de Windows
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
conn = pyodbc.connect(connection_string)

def create_jira_issue_and_assign_user(project_key, issue_type, summary, description, attachment_path=None):
    auth = (username, api_token)
    headers = {
        'Content-Type': 'application/json',
    }

    # Verificar si el campo "summary" tiene un valor válido
    if not summary or not isinstance(summary, str):
        summary = 'Asunto no proporcionado'

    # Crear datos para la solicitud de creación de incidencia
    data = {
        'fields': {
            'project': {'key': project_key},
            'issuetype': {'id': issue_type},
            'summary': summary,
            'description': {'type': 'doc', 'version': 1, 'content': [{'type': 'paragraph', 'content': [{'text': description, 'type': 'text'}]}]},
        }
    }

    response = requests.post(f'{jira_url}/rest/api/3/issue/', json=data, auth=auth, headers=headers)

    if response.status_code == 201:
        response_data = response.json()
        issue_key = response_data['key']
        print(f'Incidencia creada exitosamente en Jira. Número de incidencia: {issue_key}')

        # Adjuntar archivo si se proporciona la ruta
        if attachment_path:
            attach_file_url = f'{jira_url}/rest/api/3/issue/{issue_key}/attachments'
            attach_headers = {'X-Atlassian-Token': 'no-check'}  # Necesario para evitar el token anti-CSRF

            # Cargar el archivo .msg
            files = {'file': open(attachment_path, 'rb')}

            # Enviar la solicitud de carga de archivo adjunto
            attach_response = requests.post(attach_file_url, auth=auth, headers=attach_headers, files=files)

            if attach_response.status_code == 200:
                print(f'Archivo adjuntado con éxito a la incidencia {issue_key}')
            else:
                error_message = f'Error al adjuntar el archivo. Código de respuesta: {attach_response.status_code}'
                print(error_message)
                logging.error(error_message)

        return issue_key
    else:
        error_message = f'Error al crear la incidencia en Jira. Código de respuesta: {response.status_code}'
        print(error_message)
        logging.error(error_message)
        print(response.text)
        return None

# Función para actualizar el informador de una incidencia en Jira
def update_issue_reporter(issue_key, user_account_id):
    update_issue_url = f'{jira_url}/rest/api/3/issue/{issue_key}'
    auth = (username, api_token)
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        'fields': {
            'reporter': {
                'id': user_account_id
            }
        }
    }

    response = requests.put(update_issue_url, json=data, auth=auth, headers=headers)

    if response.status_code == 204:
        print(f"Informador '{user_account_id}' asignado con éxito a la incidencia {issue_key}")
    else:
        error_message = f"Error al asignar el informador. Código de respuesta: {response.status_code}"
        print(error_message)
        logging.error(error_message)
        print(response.text)

try:
    cursor = conn.cursor()

    # Leer los datos del DataFrame y crear incidencias en Jira
    for index, row in df.iterrows():
        asunto = row['Asunto']
        cuerpo = row['Cuerpo del mensaje']
        msg_id = row['ID']  # Nuevo campo para almacenar el ID del archivo .msg

        # Crear una incidencia en Jira para cada fila del DataFrame
        issue_key = create_jira_issue_and_assign_user('IDP', '10001', asunto, cuerpo, attachment_path=os.path.join(ruta_red, msg_id))

        # Actualizar el informador de la incidencia recién creada
        if issue_key:
            account_id = row['AccountId']
            update_issue_reporter(issue_key, account_id)

            # Borrar archivo .msg después de procesarlo
            archivo_path = os.path.join(ruta_red, msg_id)
            os.remove(archivo_path)
            print(f'Archivo {msg_id} eliminado.')

except Exception as e:
    error_message = f"Error: {str(e)}"
    print(error_message)
    logging.error(error_message)
finally:
    conn.close()