import os
import secrets
from flask import Flask, render_template, request, jsonify

# Configurazione App
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = secrets.token_hex(16)

# Definizione dati (usiamo un nome univoco per forzare il refresh)
DATI_QUESTIONARI = {
    'raads_r': {'nome': 'RAADS-R', 'item_count': 80, 'descrizione': 'Ritvo Autism Asperger Diagnostic Scale-Revised'},
    'aq': {'nome': 'AQ', 'item_count': 50, 'descrizione': 'Autism-Spectrum Quotient'},
    'eq': {'nome': 'EQ', 'item_count': 40, 'descrizione': 'Empathy Quotient'}
}

@app.route('/')
def index():
    # Passiamo esplicitamente la variabile richiesta dal template
    return render_template('index.html', questionari=DATI_QUESTIONARI)

@app.route('/questionario/<nome_test>')
def questionario(nome_test):
    if nome_test not in DATI_QUESTIONARI:
        return "Test non trovato", 404
    return render_template('questionario.html', test_name=nome_test, test_data=DATI_QUESTIONARI[nome_test])

# Blocco per evitare esecuzioni errate
if __name__ == '__main__':
    app.run()
