
📘 README.md para GitHub
Este es el archivo README.md que acompañará el repositorio del portafolio:

markdown
Copiar
Editar
# 🎟 Automatización de Creación de Tickets en Jira & Azure Boards

## 📌 Descripción del Proyecto

Este proyecto permite la creación automatizada de tickets en **Jira** y **Azure Boards** mediante la integración de correos electrónicos y bots en Telegram/WhatsApp. Se desarrolla para optimizar la gestión de tareas y mejorar la asignación de incidentes.

## 🛠 Tecnologías Utilizadas
- **Visual Basic (VBA)**: Automatización en Outlook para extraer correos y programar eventos sin necesidad de APIs.
- **Python**: Procesamiento de correos, integración con APIs de Jira/Azure DevOps.
- **Jira API / Azure DevOps API**: Creación y asignación de tickets.
- **Telegram & WhatsApp Bots**: Automatización de respuestas y generación de solicitudes a través de formularios interactivos.

## ⚡ Flujo de Trabajo

1. **Automatización de Correos (Outlook + VBA)**
   - Extrae correos sin utilizar la API de Outlook por restricciones de seguridad.
   - Guarda correos relevantes y los programa para su procesamiento automático.

2. **Procesamiento de Correos & Creación de Tickets**
   - Python procesa los correos almacenados.
   - Se genera un **ticket en Jira/Azure Boards** con asignaciones personalizadas.
   - Se vincula el informador del ticket al remitente del correo.

3. **Bots de Telegram & WhatsApp**
   - Creación de tickets mediante **comandos en Telegram**.
   - Respuestas automáticas a consultas frecuentes.
   - Formularios interactivos para captura de incidentes.

4. **Automatización para DBA y Equipos Técnicos**
   - Generación de tickets en Jira cuando los DBA completan tareas específicas.
   - Configuración de reglas personalizadas para asignación y etiquetado.

## 📂 Estructura del Proyecto
📁 Ticket_Automation 
│── 📂 src/ 
│ │── process_email.py # Extracción y procesamiento de correos 
│ │── create_ticket.py # Creación de tickets en Jira/Azure Boards 
│ │── telegram_bot.py # Bot para generación de tickets 
│ │── whatsapp_bot.py # Integración con WhatsApp 
│── 📂 vba/ │ │── outlook_macro.vba # Macro para extraer correos sin API 
│── 📂 docs/ │ 
│── README.md # Documentación del proyecto 
│── 📂 images/ │ │── workflow.png # Diagrama del proceso

bash
Copiar
Editar

## 🚀 Instalación y Ejecución

1. Clona este repositorio:
   ```sh
   git clone https://github.com/emmacm20-lab/Ticket_Automation.git
Instala los paquetes necesarios:
sh
Copiar
Editar
pip install -r requirements.txt
Configura los archivos de credenciales (config.json) para Jira, Azure DevOps y Telegram.
Ejecuta la automatización:
sh
Copiar
Editar
python src/main.py
📈 Resultados Esperados
Reducción del tiempo de creación de tickets en Jira/Azure Boards.
Automatización segura sin depender de la API de Outlook.
Interacción eficiente con bots de mensajería.
Optimización de la carga de trabajo para equipos de DBA y TI.
📬 Contacto
Si tienes preguntas o sugerencias, contáctame en emmanuel.cmora20@gmail.com.