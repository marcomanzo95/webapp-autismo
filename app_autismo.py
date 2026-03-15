import os
import secrets
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, jsonify, render_template, request

# Importa le funzioni dal tuo file calcolatore
from calcolatore_test_autismo import (
    calcola_aq, calcola_asi, calcola_asq, calcola_eq, calcola_gsrs,
    calcola_isi, calcola_ocir, calcola_raads_r, calcola_stai_y1,
    calcola_stai_y2, calcola_tas20
)

# Configurazione App
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = secrets.token_hex(16)

# Configurazione Email (da impostare nelle variabili d'ambiente di PythonAnywhere)
EMAIL_MITTENTE = os.environ.get('EMAIL_MITTENTE', 'your_email@gmail.com')
PASSWORD_APP = os.environ.get('PASSWORD_APP', 'your_app_password')
EMAIL_DESTINATARIO = os.environ.get('EMAIL_DESTINATARIO', 'your_email@gmail.com')

# Dati dei questionari
QUESTIONARI = {
    'raads_r': {
        'nome': 'RAADS-R',
        'item_count': 80,
        'descrizione': 'Ritvo Autism Asperger Diagnostic Scale-Revised'
    },
    'aq': {'nome': 'AQ', 'item_count': 50, 'descrizione': 'Autism-Spectrum Quotient'},
    'eq': {'nome': 'EQ', 'item_count': 40, 'descrizione': 'Empathy Quotient'},
    'tas20': {'nome': 'TAS-20', 'item_count': 20, 'descrizione': 'Toronto Alexithymia Scale'},
    'stai_y1': {'nome': 'STAI-Y1', 'item_count': 20, 'descrizione': 'Ansia di Stato'},
    'stai_y2': {'nome': 'STAI-Y2', 'item_count': 20, 'descrizione': 'Ansia di Tratto'},
    'gsrs': {'nome': 'GSRS', 'item_count': 15, 'descrizione': 'Gastrointestinal Symptom Rating Scale'},
    'isi': {'nome': 'ISI', 'item_count': 7, 'descrizione': 'Insomnia Severity Index'},
    'asi': {'nome': 'ASI', 'item_count': 29, 'descrizione': 'Aberrant Salience Inventory'},
    'ocir': {'nome': 'OCI-R', 'item_count': 18, 'descrizione': 'Obsessive Compulsive Inventory-Revised'},
    'asq': {'nome': 'ASQ', 'item_count': 40, 'descrizione': 'Attachment Style Questionnaire'}
}

@app.route('/')
def index():
    return render_template('index.html', questionari=QUESTIONARI)

@app.route('/questionario/<nome_test>')
def questionario(nome_test):
    if nome_test not in QUESTIONARI:
        return "Test non trovato", 404
    test_data = QUESTIONARI[nome_test]
    return render_template('questionario.html', test_name=nome_test, test_data=test_data)

@app.route('/api/invia_risultati', methods=['POST'])
def invia_risultati():
    try:
        test_name = request.form.get('test_name')
        codice_paziente = request.form.get('codice_paziente')
        
        # Estrai risposte
        risposte = []
        for i in range(1, QUESTIONARI[test_name]['item_count'] + 1):
            val = request.form.get(f'item_{i}', '0')
            risposte.append(int(val))
            
        # Calcola risultato (esempio semplificato per brevità, aggiungi gli altri elif)
        if test_name == 'raads_r':
            risultato = calcola_raads_r(risposte)
        elif test_name == 'aq':
            risultato = calcola_aq(risposte)
        else:
            # Fallback per gli altri test
            risultato = {'punteggio_totale': sum(risposte), 'interpretazione': 'Calcolo completato'}

        return jsonify({'success': True, 'risultato': risultato})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
