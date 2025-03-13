# 📂 src/create_ticket.py - Creación automática de tickets en Jira y Azure Boards
import requests

def create_jira_ticket(summary, description, assignee, project_key, jira_url, auth):
    """Crea un ticket en Jira."""
    url = f"{jira_url}/rest/api/2/issue"
    headers = {"Content-Type": "application/json"}
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "assignee": {"name": assignee},
            "issuetype": {"name": "Task"}
        }
    }
    response = requests.post(url, json=payload, headers=headers, auth=auth)
    return response.json()