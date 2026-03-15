from flask import Flask, render_template, request, jsonify
from calcolatore_test_autismo import (
    calcola_raads_r, calcola_aq, calcola_eq, calcola_isi, calcola_tas20,
    calcola_stai_y1, calcola_stai_y2, calcola_gsrs, calcola_asi, calcola_ocir, calcola_asq
)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import secrets
#from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
#load_dotenv()

# Leggi il file .env manualmente
def load_env_file():
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env_file()


# Definisci il percorso assoluto della cartella templates
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = secrets.token_hex(16)

# Configurazione email
EMAIL_MITTENTE = os.environ.get('EMAIL_MITTENTE', 'your_email@gmail.com')
PASSWORD_APP = os.environ.get('PASSWORD_APP', 'your_app_password')
EMAIL_DESTINATARIO = os.environ.get('EMAIL_DESTINATARIO', 'your_email@gmail.com')


# Dati dei questionari (placeholder)
QUESTIONARI = {
    'raads_r': {'nome': 'RAADS-R', 'item_count': 80, 'domande': ["Domanda 1", "Domanda 2"]},
    'aq': {'nome': 'AQ', 'item_count': 50, 'domande': ["Domanda 1", "Domanda 2"]},
    'eq': {'nome': 'EQ', 'item_count': 40, 'domande': ["Domanda 1", "Domanda 2"]},
    'isi': {'nome': 'ISI', 'item_count': 7, 'domande': ["Domanda 1", "Domanda 2"]},
    'tas20': {'nome': 'TAS-20', 'item_count': 20, 'domande': ["Domanda 1", "Domanda 2"]},
    'stai_y1': {'nome': 'STAI-Y-1', 'item_count': 20, 'domande': ["Domanda 1", "Domanda 2"]},
    'stai_y2': {'nome': 'STAI-Y-2', 'item_count': 20, 'domande': ["Domanda 1", "Domanda 2"]},
    'gsrs': {'nome': 'GSRS', 'item_count': 15, 'domande': ["Domanda 1", "Domanda 2"]},
    'asi': {'nome': 'ASI', 'item_count': 29, 'domande': ["Domanda 1", "Domanda 2"]},
    'ocir': {'nome': 'OCI-R', 'item_count': 18, 'domande': ["Domanda 1", "Domanda 2"]},
    'asq': {'nome': 'ASQ', 'item_count': 40, 'domande': ["Domanda 1", "Domanda 2"]}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questionario/<nome_test>')
def questionario(nome_test):
    if nome_test not in QUESTIONARI:
        return "Test non trovato", 404
    test_data = QUESTIONARI[nome_test]
    return render_template('questionario.html', test_name=nome_test, test_data=test_data)

@app.route('/api/invia_risultati', methods=['POST'])
def invia_risultati():
    try:
        if request.is_json:
            dati = request.json
        else:
            dati = request.form.to_dict()
        
        codice_paziente = dati.get('codice_paziente', '')
        if not codice_paziente:
            return jsonify({'success': False, 'message': 'Codice paziente mancante'}), 400
        
        genere = dati.get('genere', 'Non specificato')
        istruzione = dati.get('istruzione', 'Non specificata')
        telefono = dati.get('telefono', 'Non specificato')
        indirizzo = dati.get('indirizzo', 'Non specificato')
        
        risultati = {}
        
        if 'raads_r' in dati:
            risultati['raads_r'] = calcola_raads_r(dati['raads_r'])
        if 'aq' in dati:
            risultati['aq'] = calcola_aq(dati['aq'])
        if 'eq' in dati:
            risultati['eq'] = calcola_eq(dati['eq'])
        if 'isi' in dati:
            risultati['isi'] = calcola_isi(dati['isi'])
        if 'tas20' in dati:
            risultati['tas20'] = calcola_tas20(dati['tas20'])
        if 'stai_y1' in dati:
            risultati['stai_y1'] = calcola_stai_y1(dati['stai_y1'])
        if 'stai_y2' in dati:
            risultati['stai_y2'] = calcola_stai_y2(dati['stai_y2'])
        if 'gsrs' in dati:
            risultati['gsrs'] = calcola_gsrs(dati['gsrs'])
        if 'asi' in dati:
            risultati['asi'] = calcola_asi(dati['asi'])
        if 'ocir' in dati:
            risultati['ocir'] = calcola_ocir(dati['ocir'])
        if 'asq' in dati:
            risultati['asq'] = calcola_asq(dati['asq'])
        
        email_body = genera_email_risultati(codice_paziente, genere, istruzione, telefono, indirizzo, risultati)
        invia_email(EMAIL_MITTENTE, EMAIL_DESTINATARIO, email_body, codice_paziente)
        
        return jsonify({'success': True, 'message': 'Risultati inviati con successo.', 'codice_paziente': codice_paziente})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Errore: {str(e)}'}), 500

def genera_email_risultati(codice, genere, istruzione, telefono, indirizzo, risultati):
    html = f"<html><body><h1>Valutazione ADHD</h1><p>Codice: {codice}</p></body></html>"
    return html

def invia_email(mittente, destinatario, corpo_html, codice_paziente):
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Crea il messaggio
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'Risultati - {codice_paziente}'
        msg['From'] = mittente
        msg['To'] = destinatario
        msg.attach(MIMEText(corpo_html, 'html'))
        
        # Usa Gmail SMTP
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(mittente, PASSWORD_APP)
        server.sendmail(mittente, destinatario, msg.as_string())
        server.quit()
    except Exception as e:
        raise Exception(f"Errore email: {str(e)}")






if __name__ == '__main__':
    app.run(debug=True)
