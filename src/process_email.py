# 📂 src/process_email.py - Procesa correos electrónicos para extraer información relevante
import imaplib
import email
from email.header import decode_header

def fetch_emails(username, password, imap_server, folder="INBOX"):
    """Extrae correos electrónicos de una cuenta IMAP."""
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(username, password)
        mail.select(folder)
        
        status, messages = mail.search(None, 'UNSEEN')  # Obtiene correos no leídos
        email_ids = messages[0].split()
        
        emails = []
        for e_id in email_ids:
            _, msg_data = mail.fetch(e_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else 'utf-8')
                    emails.append(subject)
        
        mail.logout()
        return emails
    except Exception as e:
        print(f"Error obteniendo correos: {e}")
        return []

if __name__ == "__main__":
    emails = fetch_emails("usuario@example.com", "password", "imap.outlook.com")
    print("Correos extraídos:", emails)
