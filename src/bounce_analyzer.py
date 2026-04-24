import imaplib
import email
import re

class BounceAnalyzer:
    """Analiza la bandeja de entrada buscando reportes de rebote (Mailer-Daemon)."""
    def __init__(self, email_addr, password):
        self.email_addr = email_addr
        self.password = password
        self.mail = None
        self.patterns = {
            "not_found": ["no se ha encontrado", "address couldn't be found", "does not exist", "user unknown"],
            "blocked": ["bloqueado", "message blocked", "message rejected"],
            "recipient": [r"wasn't delivered to\s+([^\s]+)", r"Tu mensaje no se ha entregado a\s+([^\s]+)", r"Your message to\s+([^\s]+)"]
        }

    def analyze(self):
        print(f"[*] Analizando rebotes en: {self.email_addr}...")
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
        self.mail.login(self.email_addr, self.password)
        self.mail.select("inbox")
        
        status, messages = self.mail.search(None, '(FROM "mailer-daemon")')
        msg_ids = messages[0].split()
        
        results = {"no_encontrado": set(), "rebotado": set()}
        
        for m_id in msg_ids:
            status, data = self.mail.fetch(m_id, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body += part.get_payload(decode=True).decode(errors='ignore')
            else: body = msg.get_payload(decode=True).decode(errors='ignore')

            body_lower = body.lower()
            bounced_email = None
            for p in self.patterns["recipient"]:
                match = re.search(p, body, re.I)
                if match: 
                    bounced_email = match.group(1).strip('<>.,').lower()
                    break
            
            if bounced_email:
                results["rebotado"].add(bounced_email)
                if any(s in body_lower for s in self.patterns["not_found"]):
                    results["no_encontrado"].add(bounced_email)

        self.mail.logout()
        return results
