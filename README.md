# 📊 E-mail Marketing Reports

Herramienta profesional para la auditoría exhaustiva de campañas de e-mail marketing. Este proyecto permite extraer todos los mensajes enviados, analizar los rebotes directamente desde las bandejas de entrada de Gmail y generar reportes enriquecidos con el estado final de entrega.

## 🚀 Funcionalidades

- **Extracción de Enviados**: Recupera automáticamente cada registro de la carpeta de *Sent Mail* de múltiples cuentas.
- **Análisis de Mailer-Daemon**: Detecta rebotes, bloqueos y cuentas inexistentes mediante IMAP.
- **Cruce de Datos Inteligente**: Mapea los fallos de entrega con los envíos originales para identificar exactamente qué destinatarios fallaron.
- **Reportes Enriquecidos**: Genera archivos CSV profesionales listos para Excel o Google Sheets.

## 🛠️ Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/selvaggiesteban/e-mail_marketing_reports.git
   cd e-mail_marketing_reports
   ```

2. Instala las dependencias:
   ```bash
   pip install python-dotenv
   ```

## ⚙️ Configuración

Crea un archivo `.env` en la raíz (puedes usar el del proyecto de marketing principal) con tus credenciales:

```env
SMTP_ACCOUNTS=cuenta1@gmail.com|pass_app_1,cuenta2@gmail.com|pass_app_2
```

## 📈 Uso

Simplemente ejecuta el orquestador principal:

```bash
python main.py
```

El reporte final se generará en la carpeta `reports/final_enriched_report.csv`.

## 📜 Licencia
MIT
