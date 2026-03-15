import os
from flask import Flask, render_template, request, jsonify

# Usa il percorso assoluto completo di PythonAnywhere
BASE_DIR = "/home/marcomanzo/webapp-autismo"
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = os.urandom(24)


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
