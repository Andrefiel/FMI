import smtplib
from email.message import EmailMessage
import os

def send_email_report(smtp_settings, recipient, subject, body, attachment_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = smtp_settings['user']
    msg['To'] = recipient
    msg.set_content(body)

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    try:
        if smtp_settings['use_ssl']:
            server = smtplib.SMTP_SSL(smtp_settings['server'], smtp_settings['port'])
        else:
            server = smtplib.SMTP(smtp_settings['server'], smtp_settings['port'])
            server.starttls()
        server.login(smtp_settings['user'], smtp_settings['password'])
        server.send_message(msg)
        server.quit()
        return True, "Relatório enviado com sucesso!"
    except Exception as e:
        return False, f"Erro ao enviar e-mail: {e}"
