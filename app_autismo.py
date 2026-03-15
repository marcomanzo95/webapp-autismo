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
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configurazione email
EMAIL_MITTENTE = os.environ.get('EMAIL_MITTENTE', 'your_email@gmail.com')
PASSWORD_APP = os.environ.get('PASSWORD_APP', 'your_app_password')
EMAIL_DESTINATARIO = os.environ.get('EMAIL_DESTINATARIO', 'your_email@gmail.com')


# Dati dei questionari
QUESTIONARI = {
    'raads_r': {
        'nome': 'RAADS-R (Ritvo Autism Asperger\'s Diagnostic Scale-Revised)',
        'item_count': 80,
        'domande': [
            "1. Preferisco le attività solitarie a quelle di gruppo.",
            "2. Sono stato/a un bambino/a molto attivo/a.",
            "3. Quando ero bambino/a, preferivo giocare da solo/a.",
        ]
    },
    'aq': {
        'nome': 'AQ (Autism-Spectrum Quotient)',
        'item_count': 50,
        'domande': [
            "1. Capisco con facilità se qualcuno vuole partecipare ad una conversazione.",
            "2. Trovo difficile spiegare agli altri concetti che io comprendo facilmente.",
            "3. Prendermi cura degli altri è qualcosa che mi fa veramente piacere.",
        ]
    },
    'eq': {
        'nome': 'EQ (Empathy Quotient)',
        'item_count': 40,
        'domande': [
            "1. Capisco con facilità se qualcuno vuole partecipare ad una conversazione.",
            "2. Trovo difficile spiegare agli altri concetti che io comprendo facilmente.",
            "3. Prendermi cura degli altri è qualcosa che mi fa veramente piacere.",
        ]
    },
    'isi': {
        'nome': 'ISI (Insomnia Severity Index)',
        'item_count': 7,
        'domande': [
            "1a. Difficoltà ad addormentarsi",
            "1b. Difficoltà a restare addormentato",
            "1c. Risveglio troppo precoce",
            "2. Quanto si sente soddisfatto/insoddisfatto del suo attuale sonno?",
            "3. In quale misura ritiene che il problema di sonno interferisca con la sua efficienza diurna?",
            "4. Quanto pensa che il suo problema di sonno sia evidente agli altri?",
            "5. Quanto si sente preoccupato/a - stressato/a a causa del suo attuale problema di sonno?"
        ]
    },
    'tas20': {
        'nome': 'TAS-20 (Toronto Alexithymia Scale)',
        'item_count': 20,
        'domande': [
            "1. Sono spesso confuso/a circa le emozioni che provo",
            "2. Mi è difficile trovare le parole giuste per esprimere i miei sentimenti",
        ]
    },
    'stai_y1': {
        'nome': 'STAI-Y-1 (State-Trait Anxiety Inventory - Ansia di Stato)',
        'item_count': 20,
        'domande': [
            "1. Mi sento calmo",
            "2. Mi sento sicuro",
        ]
    },
    'stai_y2': {
        'nome': 'STAI-Y-2 (State-Trait Anxiety Inventory - Ansia di Tratto)',
        'item_count': 20,
        'domande': [
            "1. Mi sento bene",
            "2. Mi sento teso ed irrequieto",
        ]
    },
    'gsrs': {
        'nome': 'GSRS (General Sleep Disturbance Scale)',
        'item_count': 15,
        'domande': [
            "1. Dolore addominale",
            "2. Reflusso acido",
        ]
    },
    'asi': {
        'nome': 'ASI (Anxiety Sensitivity Index)',
        'item_count': 29,
        'domande': [
            "1. Ho la paura di avere un attacco di panico.",
            "2. È difficile per me stare fermo/a.",
        ]
    },
    'ocir': {
        'nome': 'OCI-R (Obsessive-Compulsive Inventory - Revised)',
        'item_count': 18,
        'domande': [
            "1. Ho conservato talmente tante cose che ora sono intralciato da esse.",
            "2. Ho la tendenza a controllare e ricontrollare le cose molto più spesso del necessario.",
        ]
    },
    'asq': {
        'nome': 'ASQ (Attachment Style Questionnaire)',
        'item_count': 40,
        'domande': [
            "1. Capisco con facilità se qualcuno vuole partecipare ad una conversazione.",
            "2. Trovo difficile spiegare agli altri concetti che io comprendo facilmente.",
        ]
    }
}

@app.route('/')
def index():
    """Pagina principale con informazioni sull'app"""
    return render_template('index.html')

@app.route('/questionario/<nome_test>')
def questionario(nome_test):
    """Mostra il questionario richiesto"""
    if nome_test not in QUESTIONARI:
        return "Test non trovato", 404
    test_data = QUESTIONARI[nome_test]
    return render_template('questionario.html', test_name=nome_test, test_data=test_data)

@app.route('/api/invia_risultati', methods=['POST'])
def invia_risultati():
    """Riceve i risultati e li invia via email"""
    try:
        # Gestisci sia JSON che form-urlencoded
        if request.is_json:
            dati = request.json
        else:
            dati = request.form.to_dict()
        
        # Estrai il codice paziente
        codice_paziente = dati.get('codice_paziente', '')
        if not codice_paziente:
            return jsonify({
                'success': False,
                'message': 'Codice paziente mancante'
            }), 400
        
        # Estrai gli altri dati (opzionali)
        genere = dati.get('genere', 'Non specificato')
        istruzione = dati.get('istruzione', 'Non specificata')
        telefono = dati.get('telefono', 'Non specificato')
        indirizzo = dati.get('indirizzo', 'Non specificato')
        
        # Calcola i risultati dei test
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
        
        # Crea l'email con i risultati
        email_body = genera_email_risultati(
            codice_paziente, genere, istruzione, telefono, indirizzo, risultati
        )
        
        # Invia l'email
        invia_email(EMAIL_MITTENTE, EMAIL_DESTINATARIO, email_body, codice_paziente)
        
        return jsonify({
            'success': True,
            'message': 'Risultati inviati con successo. Grazie per aver compilato i questionari.',
            'codice_paziente': codice_paziente
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Errore durante l\'invio: {str(e)}'
        }), 500

def genera_email_risultati(codice, genere, istruzione, telefono, indirizzo, risultati):
    """Genera il corpo dell'email con i risultati"""
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; margin-top: 20px; }}
            table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
            th, td {{ border: 1px solid #bdc3c7; padding: 10px; text-align: left; }}
            th {{ background-color: #ecf0f1; }}
        </style>
    </head>
    <body>
        <h1>Valutazione ADHD - Test Autosomministrati</h1>
        <p><strong>Data e ora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        <p><strong>Codice Paziente (Anonimo):</strong> {codice}</p>
        
        <h2>Dati Aggiuntivi</h2>
        <table>
            <tr><th>Campo</th><th>Valore</th></tr>
            <tr><td>Genere</td><td>{genere}</td></tr>
            <tr><td>Livello di Istruzione</td><td>{istruzione}</td></tr>
            <tr><td>Telefono</td><td>{telefono}</td></tr>
            <tr><td>Indirizzo</td><td>{indirizzo}</td></tr>
        </table>
        
        <h2>Risultati dei Test</h2>
    """
    
    for test_name, risultato in risultati.items():
        html += f"<h3>{test_name.upper()}</h3>"
        html += f"<p><strong>Punteggio:</strong> {risultato.get('punteggio_totale', 'N/A')}</p>"
        html += f"<p><strong>Interpretazione:</strong> {risultato.get('interpretazione', 'N/A')}</p>"
        if 'sottoscale' in risultato:
            html += "<p><strong>Sottoscale:</strong></p><ul>"
            for subscale, valore in risultato['sottoscale'].items():
                html += f"<li>{subscale}: {valore}</li>"
            html += "</ul>"
    
    html += """
    </body>
    </html>
    """
    return html

def invia_email(mittente, destinatario, corpo_html, codice_paziente):
    """Invia l'email con i risultati"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'Risultati Valutazione Autismo - Codice Paziente: {codice_paziente}'
        msg['From'] = mittente
        msg['To'] = destinatario
        
        parte_html = MIMEText(corpo_html, 'html')
        msg.attach(parte_html)
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(mittente, PASSWORD_APP)
        server.sendmail(mittente, destinatario, msg.as_string())
        server.quit()
    
    except Exception as e:
        raise Exception(f"Errore nell'invio dell'email: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
