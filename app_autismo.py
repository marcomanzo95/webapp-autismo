Skip to content
marcomanzo95
webapp-autismo
Repository navigation
Code
Issues
Pull requests
Agents
Actions
Projects
Wiki
Security
Insights
Settings
Files
Go to file
t
README.md
app_autismo.py
calcolatore_test_autismo.py
requirements.txt
webapp-autismo
/
app_autismo.py
in
main

Edit

Preview
Indent mode

Spaces
Indent size

4
Line wrap mode

No wrap
Editing app_autismo.py file contents


  1
  2
  3
  4
  5
  6
  7
  8
  9
 10
 11
 12
 13
 14
 15
 16
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
from flask import Flask, render_template, request, jsonify, session
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

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configurazione email (da impostare con variabili d'ambiente o file di configurazione)
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
            # ... (aggiungere tutte le 80 domande RAADS-R)
            # Per brevità, qui metto solo 3 esempi
        ]
    },
    'aq': {
        'nome': 'AQ (Autism-Spectrum Quotient)',
        'item_count': 50,
        'domande': [
            "1. Capisco con facilità se qualcuno vuole partecipare ad una conversazione.",
            "2. Trovo difficile spiegare agli altri concetti che io comprendo facilmente.",
            "3. Prendermi cura degli altri è qualcosa che mi fa veramente piacere.",
            # ... (aggiungere tutte le 50 domande AQ)
        ]
    },
    'eq': {
        'nome': 'EQ (Empathy Quotient)',
        'item_count': 40,
        'domande': [
            "1. Capisco con facilità se qualcuno vuole partecipare ad una conversazione.",
            "2. Trovo difficile spiegare agli altri concetti che io comprendo facilmente, quando loro non capiscono alla prima spiegazione.",
            "3. Prendermi cura degli altri è qualcosa che mi fa veramente piacere.",
            # ... (aggiungere tutte le 40 domande EQ)
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
Use Control + Shift + m to toggle the tab key moving focus. Alternatively, use esc then tab to move to the next interactive element on the page.





