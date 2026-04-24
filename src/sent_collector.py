import os
import imaplib
import email
import csv
import re
from datetime import datetime
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()

class SentCollector:
    """Extrae todos los mensajes enviados de las cuentas de Gmail configuradas."""
    def __init__(self, email_addr, password):
        self.email_addr = email_addr
        self.password = password
        self.mail = None

    def connect(self):
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
        self.mail.login(self.email_addr, self.password)

    def get_sent_folder(self):
        status, folders = self.mail.list()
        for f in folders:
            f_str = f.decode()
            if '\\Sent' in f_str:
                return f_str.split(' "/" ')[-1]
        return '"[Gmail]/Sent Mail"'

    def clean_header(self, header_val):
        if not header_val: return "(Sin Asunto)"
        try:
            decoded = decode_header(header_val)
            parts = []
            for content, charset in decoded:
                if isinstance(content, bytes):
                    parts.append(content.decode(charset or 'utf-8', errors='ignore'))
                else: parts.append(str(content))
            return "".join(parts)
        except: return str(header_val)

    def fetch_records(self):
        print(f"[*] Accediendo a 'Enviados' de: {self.email_addr}...")
        sent_folder = self.get_sent_folder()
        self.mail.select(sent_folder, readonly=True)
        status, messages = self.mail.search(None, "ALL")
        msg_ids = messages[0].split()
        
        records = []
        # Procesar en bloques para estabilidad
        for i in range(0, len(msg_ids), 100):
            chunk = msg_ids[i:i+100]
            chunk_str = ",".join(m.decode() for m in chunk)
            status, data = self.mail.fetch(chunk_str, "(RFC822)")
            
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = self.clean_header(msg.get('Subject'))
                    recipient = self.clean_header(msg.get('To', '(Desconocido)'))
                    
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                payload = part.get_payload(decode=True)
                                if payload: body = payload.decode(errors='ignore')
                                break
                    else:
                        payload = msg.get_payload(decode=True)
                        if payload: body = payload.decode(errors='ignore')

                    records.append({
                        "Remitente": self.email_addr,
                        "Destinatario": recipient.lower().strip('<> '),
                        "Asunto": subject,
                        "Fecha": str(msg.get('Date')),
                        "Snippet": " ".join(body.split())[:200]
                    })
        self.mail.logout()
        return records
