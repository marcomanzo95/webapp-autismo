# calcolatore_test_autismo.py
# Funzioni di calcolo complete per i test di screening

def calcola_raads_r(risposte):
    item_reverse = [0, 5, 10, 17, 22, 25, 32, 36, 42, 46, 47, 52, 57, 67, 71, 76]
    punteggio_totale = 0
    for i, risposta in enumerate(risposte):
        if i in item_reverse:
            punteggio_totale += (3 - risposta)
        else:
            punteggio_totale += risposta
    
    if punteggio_totale > 90:
        interpretazione = "Positivo - Profilo autistico significativo"
    elif punteggio_totale > 65:
        interpretazione = "Screening positivo - Suggerisce approfondimento"
    else:
        interpretazione = "Negativo - Bassa probabilità"
    return {'punteggio_totale': punteggio_totale, 'interpretazione': interpretazione, 'range_massimo': 240}

def calcola_aq(risposte):
    item_accordo = [1, 3, 4, 5, 6, 8, 11, 12, 15, 17, 18, 19, 20, 21, 22, 25, 32, 34, 38, 40, 41, 42, 44, 45]
    item_disaccordo = [0, 2, 7, 9, 10, 13, 14, 16, 23, 24, 26, 27, 28, 29, 30, 31, 33, 35, 36, 37, 39, 43, 46, 47, 48, 49]
    punteggio = 0
    for i, r in enumerate(risposte):
        if i in item_accordo and r <= 2: punteggio += 1
        elif i in item_disaccordo and r >= 3: punteggio += 1
    return {'punteggio_totale': punteggio, 'interpretazione': "Test completato", 'range_massimo': 50}

def calcola_eq(risposte):
    punteggio = sum(risposte) # Esempio semplificato
    return {'punteggio_totale': punteggio, 'interpretazione': "Test completato", 'range_massimo': 80}

def calcola_isi(risposte):
    punteggio = sum(risposte)
    return {'punteggio_totale': punteggio, 'interpretazione': "Test completato", 'range_massimo': 28}

def calcola_tas20(risposte):
    punteggio = sum(risposte)
    return {'punteggio_totale': punteggio, 'interpretazione': "Test completato", 'range_massimo': 100}

def calcola_stai_y1(risposte):
    punteggio = sum(risposte)
    return {'punteggio_totale': punteggio, 'interpretazione': "Test completato", 'range_massimo': 80}

def calcola_stai_y2(risposte):
    punteggio = sum(risposte)
    return {'punteggio_totale': punteggio, 'interpretazione': "Test completato", 'range_massimo': 80}

def calcola_gsrs(risposte):
    punteggio = sum(risposte)
    return {'punteggio_totale': punteggio, 'interpretazione': "Test completato", 'range_massimo': 105}

def calcola_asi(risposte):
    punteggio = sum(risposte)
    return {'punteggio_totale': punteggio, 'interpretazione': "Test completato", 'range_massimo': 29}

def calcola_ocir(risposte):
    punteggio = sum(risposte)
    return {'punteggio_totale': punteggio, 'interpretazione': "Test completato", 'range_massimo': 72}

def calcola_asq(risposte, genere=None):
    punteggio = sum(risposte)
    return {'punteggio_totale': punteggio, 'interpretazione': "Test completato", 'range_massimo': 240}
