# 📂 docs/README.md - Documentación del Proyecto
"""
# 🎟 Automatización de Creación de Tickets en Jira & Azure Boards

## 📌 Descripción del Proyecto

Este proyecto automatiza la generación de tickets en **Jira** y **Azure Boards** mediante la integración de correos electrónicos y bots en Telegram. Se optimiza la gestión de solicitudes y asignaciones automáticas en sistemas de IT.

## 📂 Estructura del Proyecto
```
📁 Ticket_Automation
│── 📂 src/
│   │── process_email.py   # Extracción y procesamiento de correos
│   │── create_ticket.py   # Creación de tickets en Jira/Azure Boards
│   │── telegram_bot.py    # Bot para generación de tickets
│── 📂 tests/
│   │── test_process_email.py  # Pruebas de procesamiento de correos
│   │── test_create_ticket.py  # Pruebas para creación de tickets
│   │── test_telegram_bot.py   # Pruebas del bot de Telegram
│── 📂 docs/
│   │── README.md          # Documentación del proyecto
```

## 🚀 Instalación y Ejecución

1. **Clona este repositorio:**
   ```sh
   git clone https://github.com/emmacm20-lab/Ticket_Automation.git
   ```
2. **Instala las dependencias necesarias:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Configura credenciales en `config.json`** (Ejemplo para Jira):
   ```json
   {
       "jira_url": "https://jira.example.com",
       "auth": ["usuario", "contraseña"],
       "telegram_token": "TU_TELEGRAM_BOT_TOKEN"
   }
   ```
4. **Ejecuta los scripts de automatización:**
   ```sh
   python src/process_email.py  # Extrae y procesa correos
   python src/create_ticket.py  # Crea tickets en Jira/Azure
   python src/telegram_bot.py   # Ejecuta el bot de Telegram
   ```

## 📩 Flujo de Trabajo
1. **Automatización de Correos**: Se extraen correos mediante IMAP y se programan para su procesamiento automático.
2. **Generación de Tickets**: Se analizan los correos y se generan tickets personalizados en Jira/Azure Boards.
3. **Bots de Mensajería**: Telegram permite gestionar tickets y recibir notificaciones sobre solicitudes.

## 🛠 Tecnologías Utilizadas
- **Python**: Procesamiento de correos, integración con APIs.
- **Jira API & Azure DevOps API**: Creación y gestión de tickets.
- **Telegram Bot API**: Automatización y gestión de solicitudes.
- **IMAP (Email Processing)**: Extracción de correos sin necesidad de acceso directo a Outlook.

## 📈 Resultados Esperados
- 📌 **Automatización del proceso de generación de tickets.**
- 📌 **Reducción del tiempo de respuesta en gestión de solicitudes IT.**
- 📌 **Mejor integración con herramientas de comunicación y gestión de proyectos.**

## 📬 Contacto
Para consultas o sugerencias, contáctame en [emmanuel.cmora20@gmail.com](mailto:emmanuel.cmora20@gmail.com).
"""
