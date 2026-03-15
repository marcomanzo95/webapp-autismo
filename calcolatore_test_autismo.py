import os
import secrets
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, jsonify, render_template, request

# --- FUNZIONI DEL CALCOLATORE (Incluse direttamente qui per evitare errori di import) ---
def calcola_raads_r(risposte):
    item_reverse = [0, 5, 10, 17, 22, 25, 32, 36, 42, 46, 47, 52, 57, 67, 71, 76]
    p = 0
    for i, r in enumerate(risposte):
        p += (3 - r) if i in item_reverse else r
    return {'punteggio_totale': p, 'interpretazione': "Test completato", 'range_massimo': 240}

def calcola_aq(risposte): return {'punteggio_totale': sum(risposte), 'interpretazione': "Completato", 'range_massimo': 50}
def calcola_eq(risposte): return {'punteggio_totale': sum(risposte), 'interpretazione': "Completato", 'range_massimo': 80}
def calcola_isi(risposte): return {'punteggio_totale': sum(risposte), 'interpretazione': "Completato", 'range_massimo': 28}
def calcola_tas20(risposte): return {'punteggio_totale': sum(risposte), 'interpretazione': "Completato", 'range_massimo': 100}
def calcola_stai_y1(risposte): return {'punteggio_totale': sum(risposte), 'interpretazione': "Completato", 'range_massimo': 80}
def calcola_stai_y2(risposte): return {'punteggio_totale': sum(risposte), 'interpretazione': "Completato", 'range_massimo': 80}
def calcola_gsrs(risposte): return {'punteggio_totale': sum(risposte), 'interpretazione': "Completato", 'range_massimo': 105}
def calcola_asi(risposte): return {'punteggio_totale': sum(risposte), 'interpretazione': "Completato", 'range_massimo': 29}
def calcola_ocir(risposte): return {'punteggio_totale': sum(risposte), 'interpretazione': "Completato", 'range_massimo': 72}
def calcola_asq(risposte, genere=None): return {'punteggio_totale': sum(risposte), 'interpretazione': "Completato", 'range_massimo': 240}

# --- CONFIGURAZIONE APP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = secrets.token_hex(16)

QUESTIONARI = {
    'raads_r': {'nome': 'RAADS-R', 'item_count': 80, 'descrizione': 'Ritvo Autism Asperger Diagnostic Scale-Revised'},
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
    if nome_test not in QUESTIONARI: return "Test non trovato", 404
    return render_template('questionario.html', test_name=nome_test, test_data=QUESTIONARI[nome_test])

@app.route('/api/invia_risultati', methods=['POST'])
def invia_risultati():
    try:
        test_name = request.form.get('test_name')
        risposte = [int(request.form.get(f'item_{i}', '0')) for i in range(1, QUESTIONARI[test_name]['item_count'] + 1)]
        
        if test_name == 'raads_r': risultato = calcola_raads_r(risposte)
        elif test_name == 'aq': risultato = calcola_aq(risposte)
        else: risultato = {'punteggio_totale': sum(risposte), 'interpretazione': 'Calcolo completato'}

        return jsonify({'success': True, 'risultato': risultato})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
