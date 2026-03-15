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
    'isi': {
        'nome': 'ISI (Insomnia Severity Index)',
        'item_count': 7,
        'scale_type': 'numeric_0_4',
        'scale_labels': ['No', 'Lieve', 'Media', 'Grave', 'Molto grave'],
        'domande': [
            "Difficoltà ad addormentarsi (nelle ultime 2 settimane)",
            "Difficoltà a restare addormentato (nelle ultime 2 settimane)",
            "Risveglio troppo precoce (nelle ultime 2 settimane)",
            "Quanto si sente soddisfatto/insoddisfatto del suo attuale sonno? (Molto soddisfatto=0, Soddisfatto=1, Neutro=2, Non molto soddisfatto=3, Molto insoddisfatto=4)",
            "In quale misura ritiene che il problema di sonno interferisca con la sua efficienza diurna? (affaticamento diurno, capacità di svolgere lavoro/faccende di casa, concentrazione, memoria, umore, ecc.)",
            "Quanto pensa che il suo problema di sonno sia evidente agli altri, in termini di peggioramento di qualità della sua vita?",
            "Quanto si sente preoccupato/a – stressato/a a causa del suo attuale problema di sonno?"
        ]
    },
    'tas20': {'nome': 'TAS-20', 'item_count': 20, 'domande': ["Domanda 1", "Domanda 2"]},
    'stai_y1': {'nome': 'STAI-Y-1', 'item_count': 20, 'domande': ["Domanda 1", "Domanda 2"]},
    'stai_y2': {'nome': 'STAI-Y-2', 'item_count': 20, 'domande': ["Domanda 1", "Domanda 2"]},
    'gsrs': {
        'nome': 'GSRS (Gastrointestinal Symptom Rating Scale)',
        'item_count': 15,
        'domande': [
            "Hai avuto DOLORE O DISAGIO nella parte superiore dell'addome o alla bocca dello stomaco nell'ultima settimana?",
            "Hai avuto BRUCIORE DI STOMACO nell'ultima settimana?",
            "Hai avuto REFLUSSO ACIDO nell'ultima settimana?",
            "Hai avuto CRAMPI DA FAME allo stomaco nell'ultima settimana?",
            "Hai avuto NAUSEA nell'ultima settimana?",
            "Hai avuto RUMORI allo stomaco nell'ultima settimana?",
            "Hai avuto una SENSAZIONE DI GONFIORE allo stomaco nell'ultima settimana?",
            "Hai avuto ERUTTAZIONI nell'ultima settimana?",
            "Hai avuto GAS o FLATULENZA nell'ultima settimana?",
            "Hai avuto STITICHEZZA nell'ultima settimana?",
            "Hai avuto DIARREA nell'ultima settimana?",
            "Hai avuto FECI MOLLI nell'ultima settimana?",
            "Hai avuto FECI DURE nell'ultima settimana?",
            "Hai avuto un BISOGNO URGENTE di andare in bagno per un movimento intestinale nell'ultima settimana?",
            "Quando sei andato in bagno nell'ultima settimana, hai avuto la SENSAZIONE DI NON SVUOTARE COMPLETAMENTE l'intestino?"
        ],
        'scale': ['Nessun disagio', 'Disagio minimo', 'Disagio lieve', 'Disagio moderato', 'Disagio medio-grave', 'Disagio grave', 'Disagio molto grave']
    },
    'asi': {
        'nome': 'ASI (Aberrant Salience Inventory)',
        'item_count': 29,
        'scale_type': 'binary',
        'scale_labels': ['No', 'Si'],
        'domande': [
            "Le è mai capitato di alcune cose di poco conto lo siano apparse improvvisamente importanti o significative?",
            "Le succede, talvolta, di sentirsi come alla soglia di qualcosa di veramente grande, ma non è sicuro di che cosa sia?",
            "Le capita, qualche volta, che le sue capacità sensoriali le sembrino acute?",
            "Si è mai sentito come se stesse rapidamente per raggiungere il massimo delle sue capacità intellettuali?",
            "Le capita, qualche volta, di prestare attenzione a certi dettagli non notati in precedenza che vengono ad assumere una certa rilevanza per lei?",
            "Le succede di sentirsi come se ci fosse qualcosa di importante (per lei) da capire, ma non è sicuro di che cosa sia?",
            "Ha mai passato periodi in cui si è sentito particolarmente religioso o contemplativo?",
            "Ha mai avuto difficoltà a distinguere se si sente eccitato, spaventato, sconcertato o ansioso?",
            "Ha mai attraversato dei periodi di maggiore consapevolezza sulle cose?",
            "Ha mai sentito il bisogno di dare un senso a situazioni o avvenimenti apparentemente casuali?",
            "Qualche volta le capita di sentirsi come stesse trovando il pezzo mancante di un puzzle?",
            "A volte si sente come se potesse udire le cose con maggior chiarezza?",
            "A volte si sente come se fosse una persona particolarmente evoluta dal punto di vista spirituale?",
            "Osservazioni di norma insignificanti, a volte assumono per lei un significato inusuale?",
            "Attraversa dei periodi in cui le canzoni talvolta assumono significati rilevanti per la sua vita?",
            "Qualche volta le capita di sentirsi sul punto di comprendere qualcosa di veramente grande o importante, ma non sa con certezza cosa sia?",
            "Il suo senso del gusto le è mai sembrato più fine?",
            "Ha mai avuto la sensazione che i misteri dell'universo fossero sul punto di rivelarsi a lei?",
            "Le capita di passare periodi in cui si sente eccessivamente stimolato da oggetti o esperienze che normalmente sono poco spiacevoli?",
            "Rimane spesso affascinato dalle piccole cose che la circondano?",
            "I suoi sensi le sembrino mai estremamente spiccioli o chiari?",
            "Si sente mai come se un intero mondo le si stesse rivelando?",
            "Si è mai sentito come se i confini fra le sue sensazioni interne ed esterne fossero stali tolto?",
            "Qualche volta le succede di avere la sensazione che il mondo stia cambiando e che lei debba trovare una spiegazione?",
            "Ha mai percepito un significato travolgente in cose che normalmente per lei non sono significative?",
            "Ha mai sperimentato una sensazione inesprimibile di urgenza in cui non era sicuro sulla farsi?",
            "Le è mai capitato di sviluppare in particolare interesse per persone, eventi, luoghi o idee che normalmente non attirebbero in quel modo la sua attenzione?",
            "Le capita mai che i suoi pensieri e le sue percezioni diventino troppo rapidi per essere ben assimilati?",
            "A volte nota cose a cui non aveva prestato attenzione in precedenza e che invece vengono ora ad assumere un significato speciale?"
        ]
    }
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
        
        print(f"DEBUG: Dati ricevuti: {dati}")  # DEBUG
        
        codice_paziente = dati.get('codice_paziente', '')
        if not codice_paziente:
            return jsonify({'success': False, 'message': 'Codice paziente mancante'}), 400
        
        genere = dati.get('genere', 'Non specificato')
        istruzione = dati.get('istruzione', 'Non specificata')
        telefono = dati.get('telefono', 'Non specificato')
        indirizzo = dati.get('indirizzo', 'Non specificato')
        
        risultati = {}
        # Raccogli le risposte dal form (item_1, item_2, ecc.)
        risposte_dict = {}
        for key, value in dati.items():
            if key.startswith('item_'):
                # Estrai il numero dalla chiave (item_1 -> 1)
                item_num = int(key.split('_')[1])
                risposte_dict[item_num] = int(value)
        
        print(f"DEBUG: Risposte raccolte (dict): {risposte_dict}")  # DEBUG
        
        # Determina quale test è stato compilato dal nome del test
        nome_test = dati.get('test_name', '')
        test_info = QUESTIONARI.get(nome_test, {})
        item_count = test_info.get('item_count', 0)
        
        # Converti il dizionario in una lista ordinata
        risposte = [risposte_dict.get(i, 0) for i in range(1, item_count + 1)]
        
        print(f"DEBUG: Risposte come lista: {risposte}")  # DEBUG
        
        if nome_test == 'raads_r' and risposte:
            risultati['raads_r'] = calcola_raads_r(risposte)
        elif nome_test == 'aq' and risposte:
            risultati['aq'] = calcola_aq(risposte)
        elif nome_test == 'eq' and risposte:
            risultati['eq'] = calcola_eq(risposte)
        elif nome_test == 'isi' and risposte:
            risultati['isi'] = calcola_isi(risposte)
        elif nome_test == 'tas20' and risposte:
            risultati['tas20'] = calcola_tas20(risposte)
        elif nome_test == 'stai_y1' and risposte:
            risultati['stai_y1'] = calcola_stai_y1(risposte)
        elif nome_test == 'stai_y2' and risposte:
            risultati['stai_y2'] = calcola_stai_y2(risposte)
        elif nome_test == 'gsrs' and risposte:
            risultati['gsrs'] = calcola_gsrs(risposte)
        elif nome_test == 'asi' and risposte:
            risultati['asi'] = calcola_asi(risposte)
        elif nome_test == 'ocir' and risposte:
            risultati['ocir'] = calcola_ocir(risposte)
        elif nome_test == 'asq' and risposte:
            risultati['asq'] = calcola_asq(risposte)
        
        email_body = genera_email_risultati(codice_paziente, genere, istruzione, telefono, indirizzo, risultati)
        invia_email(EMAIL_MITTENTE, EMAIL_DESTINATARIO, email_body, codice_paziente)
        
        return jsonify({'success': True, 'message': 'Risultati inviati con successo.', 'codice_paziente': codice_paziente})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Errore: {str(e)}'}), 500

def genera_email_risultati(codice, genere, istruzione, telefono, indirizzo, risultati):
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h1>Valutazione ADHD/Autismo</h1>
        <hr>
        
        <h2>Dati Paziente</h2>
        <p><strong>Codice Paziente:</strong> {codice}</p>
        <p><strong>Genere:</strong> {genere}</p>
        <p><strong>Istruzione:</strong> {istruzione}</p>
        <p><strong>Telefono:</strong> {telefono}</p>
        <p><strong>Indirizzo:</strong> {indirizzo}</p>
        
        <h2>Risultati Test</h2>
    """
    
    if risultati:
        for test_name, risultato in risultati.items():
            html += f"<h3>{test_name.upper()}</h3>"
            html += f"<p><strong>Punteggio:</strong> {risultato.get('punteggio_totale', 'N/A')}</p>"
            html += f"<p><strong>Interpretazione:</strong> {risultato.get('interpretazione', 'N/A')}</p>"
            if 'sottoscale' in risultato:
                html += "<p><strong>Sottoscale:</strong></p><ul>"
                for subscale, valore in risultato['sottoscale'].items():
                    html += f"<li>{subscale}: {valore}</li>"
                html += "</ul>"
    else:
        html += "<p>Nessun risultato disponibile</p>"
    
    html += """
        <hr>
        <p style="color: #666; font-size: 12px;">Questo è un messaggio automatico. Non rispondere a questa email.</p>
    </body>
    </html>
    """
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
