import os
import csv
from src.sent_collector import SentCollector
from src.bounce_analyzer import BounceAnalyzer
from dotenv import load_dotenv

# Cargar configuración del .env original
DOTENV_PATH = r"C:\Users\Esteban Selvaggi\Desktop\Diseño web\e-mail_marketing\.env"
load_dotenv(dotenv_path=DOTENV_PATH)

def main():
    accounts_str = os.getenv("SMTP_ACCOUNTS", "")
    accounts = [acc.split('|') for acc in accounts_str.split(',') if '|' in acc]
    
    if not accounts:
        print("[-] No se cargaron cuentas.")
        return

    all_sent_records = []
    global_bounces = {"rebotado": set(), "no_encontrado": set()}

    print("\n" + "="*50)
    print("INICIANDO PROCESAMIENTO GLOBAL DE CAMPAÑAS")
    print("="*50)

    for email_addr, password in accounts:
        # 1. Extraer Enviados
        collector = SentCollector(email_addr, password)
        try:
            collector.connect()
            all_sent_records.extend(collector.fetch_records())
        except Exception as e:
            print(f"    [-] Error en enviados de {email_addr}: {e}")

        # 2. Analizar Rebotes
        analyzer = BounceAnalyzer(email_addr, password)
        try:
            bounce_res = analyzer.analyze()
            global_bounces["rebotado"].update(bounce_res["rebotado"])
            global_bounces["no_encontrado"].update(bounce_res["no_encontrado"])
        except Exception as e:
            print(f"    [-] Error en rebotes de {email_addr}: {e}")

    # 3. Cruzar y Enriquecer Datos
    print("\n[*] Cruzando envíos con rebotes...")
    final_data = []
    for rec in all_sent_records:
        dest = rec["Destinatario"]
        rec["Estado"] = "Entregado"
        rec["Detalle"] = ""
        
        if dest in global_bounces["no_encontrado"]:
            rec["Estado"] = "Rebotado"
            rec["Detalle"] = "No Encontrado (Inexistente)"
        elif dest in global_bounces["rebotado"]:
            rec["Estado"] = "Rebotado"
            rec["Detalle"] = "Falla de Entrega (General)"
            
        final_data.append(rec)

    # 4. Guardar Reporte Final
    output_path = r"C:\Users\Esteban Selvaggi\Desktop\Diseño web\e-mail_marketing_reports\reports\final_enriched_report.csv"
    headers = ["Remitente", "Destinatario", "Asunto", "Fecha", "Estado", "Detalle", "Snippet"]
    
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(final_data)

    print("\n" + "="*50)
    print("REPORTE FINAL COMPLETADO")
    print("="*50)
    print(f"Total Registros: {len(final_data)}")
    print(f"Archivo: {output_path}")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
