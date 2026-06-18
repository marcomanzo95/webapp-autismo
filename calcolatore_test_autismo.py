# calcolatore_test_autismo.py
# Funzioni di calcolo per tutti i test di screening dell'autismo

def calcola_raads_r(risposte):
    """
    Calcola il punteggio del RAADS-R (Ritvo Autism Asperger's Diagnostic Scale-Revised)
    
    Parametri:
    risposte: lista di 80 valori (0-3)
    
    Item reverse: 1, 6, 11, 18, 23, 26, 33, 37, 43, 47, 48, 53, 58, 68, 72, 77
    """
    item_reverse = [0, 5, 10, 17, 22, 25, 32, 36, 42, 46, 47, 52, 57, 67, 71, 76]  # 0-indexed
    
    punteggio_totale = 0
    
    for i, risposta in enumerate(risposte):
        if i in item_reverse:
            # Inverti il punteggio: 0->3, 1->2, 2->1, 3->0
            punteggio_invertito = 3 - risposta
            punteggio_totale += punteggio_invertito
        else:
            punteggio_totale += risposta
    
    # Calcolo delle sottoscale
    # Interazione Sociale: item specifici
    # Interessi Circoscritti: item specifici
    # Pragmatica: item specifici
    # Senso Motorio: item specifici
    
    if punteggio_totale > 90:
        interpretazione = "Positivo - Profilo autistico significativo (punteggio > 90)"
    elif punteggio_totale > 65:
        interpretazione = "Screening positivo - Suggerisce approfondimento diagnostico (punteggio > 65)"
    else:
        interpretazione = "Negativo - Bassa probabilità di autismo (punteggio ≤ 65)"
    
    return {
        'punteggio_totale': punteggio_totale,
        'interpretazione': interpretazione,
        'range_massimo': 240
    }


def calcola_aq(risposte):
    """
    Calcola il punteggio dell'AQ (Autism-Spectrum Quotient)
    
    Parametri:
    risposte: lista di 50 valori (1-4, dove 1=Assolutamente d'accordo, 4=Assolutamente in disaccordo)
    
    Sistema di scoring asimmetrico:
    - Item 2, 4, 5, 6, 7, 9, 12, 13, 16, 18, 19, 20, 21, 22, 23, 26, 33, 35, 39, 41, 42, 43, 45, 46:
      "Assolutamente d'accordo" O "Parzialmente d'accordo" = 1 punto
    - Item 1, 3, 8, 10, 11, 14, 15, 17, 24, 25, 27, 28, 29, 30, 31, 32, 34, 36, 37, 38, 40, 44, 47, 48, 49, 50:
      "Assolutamente in disaccordo" O "Parzialmente in disaccordo" = 1 punto
    """
    # Item che danno 1 punto per accordo (1 o 2)
    item_accordo = [1, 3, 4, 5, 6, 8, 11, 12, 15, 17, 18, 19, 20, 21, 22, 25, 32, 34, 38, 40, 41, 42, 44, 45]  # 1-indexed
    
    # Item che danno 1 punto per disaccordo (3 o 4)
    item_disaccordo = [0, 2, 7, 9, 10, 13, 14, 16, 23, 24, 26, 27, 28, 29, 30, 31, 33, 35, 36, 37, 39, 43, 46, 47, 48, 49]  # 0-indexed
    
    punteggio_totale = 0
    
    for i, risposta in enumerate(risposte):
        if i in item_accordo:
            # Accordo: 1 o 2 = 1 punto
            if risposta <= 2:
                punteggio_totale += 1
        elif i in item_disaccordo:
            # Disaccordo: 3 o 4 = 1 punto
            if risposta >= 3:
                punteggio_totale += 1
    
    if punteggio_totale >= 32:
        interpretazione = "Positivo - Tratti autistici significativi (punteggio ≥ 32)"
    elif punteggio_totale >= 21:
        interpretazione = "Moderato - Livello moderato di tratti autistici (punteggio 21-31)"
    else:
        interpretazione = "Negativo - Basso livello di tratti autistici (punteggio < 21)"
    
    return {
        'punteggio_totale': punteggio_totale,
        'interpretazione': interpretazione,
        'range_massimo': 50
    }
def calcola_eq(risposte):
    """
    Calcola il punteggio dell'EQ (Empathy Quotient)
    
    Parametri:
    risposte: lista di 40 valori (1-4, dove 1=Assolutamente d'accordo, 4=Assolutamente in disaccordo)
    
    Item che indicano ALTA EMPATIA (accordo = punto):
    1, 2, 3, 4, 8, 11, 13, 14, 15, 17, 21, 22, 23, 24, 26, 27, 28, 29, 34, 35, 36, 39, 40
    
    Item che indicano BASSA EMPATIA (disaccordo = punto):
    5, 6, 7, 9, 10, 12, 16, 18, 19, 20, 25, 30, 31, 32, 33, 37, 38
    """
    # Item che indicano ALTA EMPATIA (0-indexed)
    item_alta_empatia = [0, 1, 2, 3, 7, 10, 12, 13, 14, 16, 20, 21, 22, 23, 25, 26, 27, 28, 33, 34, 35, 38, 39]
    
    # Item che indicano BASSA EMPATIA (0-indexed)
    item_bassa_empatia = [4, 5, 6, 8, 9, 11, 15, 17, 18, 19, 24, 29, 30, 31, 32, 36, 37]
    
    punteggio_totale = 0
    
    for i, risposta in enumerate(risposte):
        if i in item_alta_empatia:
            # Alta empatia: accordo (1 o 2) = punti
            if risposta == 1:
                punteggio_totale += 2
            elif risposta == 2:
                punteggio_totale += 1
        elif i in item_bassa_empatia:
            # Bassa empatia: disaccordo (3 o 4) = punti
            if risposta == 3:
                punteggio_totale += 1
            elif risposta == 4:
                punteggio_totale += 2
    
    if punteggio_totale >= 61:
        interpretazione = "Alta empatia (punteggio 61-80)"
    elif punteggio_totale >= 41:
        interpretazione = "Empatia buona (punteggio 41-60)"
    elif punteggio_totale >= 21:
        interpretazione = "Empatia moderata (punteggio 21-40)"
    else:
        interpretazione = "Bassa empatia (punteggio 0-20)"
    
    return {
        'punteggio_totale': punteggio_totale,
        'interpretazione': interpretazione,
        'range_massimo': 80
    }

def calcola_tas20(risposte):
    """
    Calcola il punteggio della TAS-20 (Toronto Alexithymia Scale)
    
    Parametri:
    risposte: lista di 20 valori (1-5)
    
    Item reverse: 4, 5, 10, 18, 19 (0-indexed: 3, 4, 9, 17, 18)
    """
    item_reverse = [3, 4, 9, 17, 18]
    
    punteggio_totale = 0
    
    for i, risposta in enumerate(risposte):
        if i in item_reverse:
            # Inverti il punteggio: 1->5, 2->4, 3->3, 4->2, 5->1
            punteggio_invertito = 6 - risposta
            punteggio_totale += punteggio_invertito
        else:
            punteggio_totale += risposta
    
    if punteggio_totale >= 61:
        interpretazione = "Alessitimia clinicamente significativa (punteggio ≥ 61)"
    elif punteggio_totale >= 52:
        interpretazione = "Possibile alessitimia - Borderline (punteggio 52-60)"
    else:
        interpretazione = "Non indicativo di alessitimia (punteggio ≤ 51)"
    
    return {
        'punteggio_totale': punteggio_totale,
        'interpretazione': interpretazione,
        'range_massimo': 100
    }

def calcola_stai_y1(risposte):
    """
    Calcola il punteggio dello STAI-Y-1 (State-Trait Anxiety Inventory - Ansia di Stato)
    
    Parametri:
    risposte: lista di 20 valori (1-4)
    
    Item reverse (formulati positivamente): 1, 2, 5, 8, 10, 11, 15, 16, 19, 20 (0-indexed: 0, 1, 4, 7, 9, 10, 14, 15, 18, 19)
    """
    item_reverse = [0, 1, 4, 7, 9, 10, 14, 15, 18, 19]
    
    punteggio_totale = 0
    
    for i, risposta in enumerate(risposte):
        if i in item_reverse:
            # Inverti il punteggio: 1->4, 2->3, 3->2, 4->1
            punteggio_invertito = 5 - risposta
            punteggio_totale += punteggio_invertito
        else:
            punteggio_totale += risposta
    
    if punteggio_totale >= 40:
        interpretazione = "Livello di ansia di stato elevato (soglia di riferimento ≥ 40)"
    else:
        interpretazione = "Livello di ansia di stato moderato-basso (punteggio < 40)"
    
    return {
        'punteggio_totale': punteggio_totale,
        'interpretazione': interpretazione,
        'range_massimo': 80
    }


def calcola_stai_y2(risposte):
    """
    Calcola il punteggio dello STAI-Y-2 (State-Trait Anxiety Inventory - Ansia di Tratto)
    
    Parametri:
    risposte: lista di 20 valori (1-4)
    
    Item reverse (formulati positivamente): 1, 3, 6, 7, 10, 13, 14, 16, 19 (0-indexed: 0, 2, 5, 6, 9, 12, 13, 15, 18)
    """
    item_reverse = [0, 2, 5, 6, 9, 12, 13, 15, 18]
    
    punteggio_totale = 0
    
    for i, risposta in enumerate(risposte):
        if i in item_reverse:
            # Inverti il punteggio: 1->4, 2->3, 3->2, 4->1
            punteggio_invertito = 5 - risposta
            punteggio_totale += punteggio_invertito
        else:
            punteggio_totale += risposta
    
    if punteggio_totale >= 40:
        interpretazione = "Livello di ansia di tratto clinicamente significativo (soglia di riferimento ≥ 40)"
    else:
        interpretazione = "Livello di ansia di tratto moderato-basso (punteggio < 40)"
    
    return {
        'punteggio_totale': punteggio_totale,
        'interpretazione': interpretazione,
        'range_massimo': 80
    }


def calcola_gsrs(risposte):
    """
    Calcola il punteggio della GSRS (General Sleep Disturbance Scale)
    
    Parametri:
    risposte: lista di 15 valori (1-7)
    
    Sottoscale:
    - Reflux: item 2, 3 (0-indexed: 1, 2)
    - Pain: item 1, 4, 5 (0-indexed: 0, 3, 4)
    - Indigestion: item 6, 7, 8, 9 (0-indexed: 5, 6, 7, 8)
    - Diarrea: item 11, 12, 14 (0-indexed: 10, 11, 13)
    - Constipation: item 10, 13, 15 (0-indexed: 9, 12, 14)
    """
    # Normalizza ogni item da scala 1-7 a scala 0-1
    risposte_normalizzate = [(r - 1) / 6 for r in risposte]
    
    # Calcola le sottoscale come medie
    reflux = (risposte_normalizzate[1] + risposte_normalizzate[2]) / 2
    pain = (risposte_normalizzate[0] + risposte_normalizzate[3] + risposte_normalizzate[4]) / 3
    indigestion = (risposte_normalizzate[5] + risposte_normalizzate[6] + risposte_normalizzate[7] + risposte_normalizzate[8]) / 4
    diarrea = (risposte_normalizzate[10] + risposte_normalizzate[11] + risposte_normalizzate[13]) / 3
    constipation = (risposte_normalizzate[9] + risposte_normalizzate[12] + risposte_normalizzate[14]) / 3
    
    # Punteggio totale: media di tutte le sottoscale
    punteggio_totale = (reflux + pain + indigestion + diarrea + constipation) / 5
    
    return {
        'punteggio_totale': round(punteggio_totale, 3),
        'sottoscale': {
            'reflux': round(reflux, 3),
            'pain': round(pain, 3),
            'indigestion': round(indigestion, 3),
            'diarrea': round(diarrea, 3),
            'constipation': round(constipation, 3)
        },
        'interpretazione': f"Punteggio normalizzato GSRS: {round(punteggio_totale, 3)} (scala 0-1)",
        'range_massimo': 1
    }

def calcola_isi(risposte):
    """
    Calcola il punteggio ISI (Insomnia Severity Index)
    Scala: 0-4 per tutte le 7 domande
    Punteggio totale: 0-28
    
    Interpretazione:
    - 0-7: Nessuna insonnia
    - 8-14: Insonnia subclinica
    - 15-21: Insonnia moderata
    - 22-28: Insonnia grave
    """
    if not risposte or len(risposte) < 7:
        return None
    
    # Somma i punteggi delle 7 domande
    punteggio_totale = sum(int(r) for r in risposte[:7])
    
    # Determina la severità
    if punteggio_totale <= 7:
        severita = "Nessuna insonnia"
    elif punteggio_totale <= 14:
        severita = "Insonnia subclinica"
    elif punteggio_totale <= 21:
        severita = "Insonnia moderata"
    else:
        severita = "Insonnia grave"
    
    return {
        'punteggio': punteggio_totale,
        'max_punteggio': 28,
        'percentuale': round((punteggio_totale / 28) * 100, 2),
        'severita': severita
    }


def calcola_asi(risposte):
    """
    Calcola il punteggio ASI (Aberrant Salience Inventory)
    Scala: 0-1 (No/Si) per tutte le 29 domande
    Punteggio totale: 0-29
    
    Interpretazione:
    - 0-9: Basso (normale)
    - 10-19: Moderato
    - 20-29: Alto (possibile indicatore di salienza aberrante)
    """
    if not risposte or len(risposte) < 29:
        return None
    
    # Somma i punteggi delle 29 domande
    punteggio_totale = sum(int(r) for r in risposte[:29])
    
    # Determina il livello
    if punteggio_totale <= 9:
        livello = "Basso (normale)"
    elif punteggio_totale <= 19:
        livello = "Moderato"
    else:
        livello = "Alto (possibile indicatore di salienza aberrante)"
    
    return {
        'punteggio': punteggio_totale,
        'max_punteggio': 29,
        'percentuale': round((punteggio_totale / 29) * 100, 2),
        'livello': livello
    }



def calcola_ocir(risposte):
    """
    Calcola il punteggio dell'OCI-R (Obsessive-Compulsive Inventory - Revised)
    
    Parametri:
    risposte: lista di 18 valori (0-4)
    
    Sottoscale:
    - Hoarding: item 1, 7, 13 (0-indexed: 0, 6, 12)
    - Checking: item 2, 8, 14 (0-indexed: 1, 7, 13)
    - Ordering: item 3, 9, 15 (0-indexed: 2, 8, 14)
    - Mental Neutralizing: item 4, 10, 16 (0-indexed: 3, 9, 15)
    - Washing: item 5, 11, 17 (0-indexed: 4, 10, 16)
    - Obsessing: item 6, 12, 18 (0-indexed: 5, 11, 17)
    """
    punteggio_totale = sum(risposte)
    
    # Calcola le sottoscale
    hoarding = risposte[0] + risposte[6] + risposte[12]
    checking = risposte[1] + risposte[7] + risposte[13]
    ordering = risposte[2] + risposte[8] + risposte[14]
    mental_neutralizing = risposte[3] + risposte[9] + risposte[15]
    washing = risposte[4] + risposte[10] + risposte[16]
    obsessing = risposte[5] + risposte[11] + risposte[17]
    
    if punteggio_totale >= 21:
        interpretazione = "Sintomi OCD clinicamente significativi (punteggio ≥ 21)"
    elif punteggio_totale >= 8:
        interpretazione = "Sintomi OCD moderati (punteggio 8-20)"
    else:
        interpretazione = "Sintomi OCD minimi (punteggio < 8)"
    
    return {
        'punteggio_totale': punteggio_totale,
        'sottoscale': {
            'hoarding': hoarding,
            'checking': checking,
            'ordering': ordering,
            'mental_neutralizing': mental_neutralizing,
            'washing': washing,
            'obsessing': obsessing
        },
        'interpretazione': interpretazione,
        'range_massimo': 72
    }
def calcola_percentile_da_tabella(punteggio, tabella_percentili):
    """
    Restituisce il percentile approssimativo sulla base di una tabella ordinata
    del tipo [(1, 17), (2.5, 20), (5, 23), ...]
    """
    percentile_stimato = None

    for percentile, cutoff in tabella_percentili:
        if punteggio >= cutoff:
            percentile_stimato = percentile
        else:
            break

    return percentile_stimato


def calcola_asq(risposte, genere=None):
    """
    Calcola i punteggi dell'ASQ (Attachment Style Questionnaire)

    Parametri:
    risposte: lista di 40 valori (1-6)
    genere: stringa opzionale ('maschio', 'femmina', 'm', 'f')
    """

    if not risposte or len(risposte) < 40:
        return None

    # Scale principali
    fiducia = risposte[0] + risposte[1] + risposte[2] + risposte[18] + risposte[19] + risposte[30] + risposte[36] + risposte[37]
    disagio_intimita = risposte[4] + risposte[13] + risposte[15] + risposte[16] + risposte[20] + risposte[22] + risposte[24] + risposte[25] + risposte[33] + risposte[35]
    secondarieta = risposte[3] + risposte[5] + risposte[6] + risposte[7] + risposte[8] + risposte[9] + risposte[33] + risposte[35]
    bisogno_approvazione = risposte[10] + risposte[11] + risposte[12] + risposte[14] + risposte[23] + risposte[26] + risposte[34]
    preoccupazione = risposte[17] + risposte[21] + risposte[27] + risposte[28] + risposte[29] + risposte[31] + risposte[32] + risposte[38] + risposte[39]

    evitamento = disagio_intimita + secondarieta - fiducia
    ansia = bisogno_approvazione + preoccupazione - fiducia

    # Percentili complessivi
    percentili_globali = {
        'fiducia': [
            (1, 17), (2.5, 20), (5, 23), (10, 25), (25, 28),
            (50, 32), (75, 36), (90, 38), (95, 40), (97.5, 42), (99, 43)
        ],
        'disagio_intimita': [
            (1, 21), (2.5, 23), (5, 25), (10, 28), (25, 32),
            (50, 37), (75, 42), (90, 47), (95, 49), (97.5, 52), (99, 54)
        ],
        'secondarieta': [
            (1, 7), (2.5, 7), (5, 8), (10, 9), (25, 12),
            (50, 15), (75, 19), (90, 25), (95, 27), (97.5, 30), (99, 35)
        ],
        'bisogno_approvazione': [
            (1, 9), (2.5, 11), (5, 11), (10, 13), (25, 17),
            (50, 21), (75, 25), (90, 29), (95, 32), (97.5, 34), (99, 36)
        ],
        'preoccupazione': [
            (1, 13), (2.5, 15), (5, 18), (10, 21), (25, 25),
            (50, 29), (75, 33), (90, 36), (95, 38), (97.5, 40), (99, 42)
        ]
    }

    risultati = {
        'scale': {
            'fiducia': fiducia,
            'disagio_intimita': disagio_intimita,
            'secondarieta': secondarieta,
            'bisogno_approvazione': bisogno_approvazione,
            'preoccupazione': preoccupazione
        },
        'fattori_latenti': {
            'evitamento': round(evitamento, 2),
            'ansia': round(ansia, 2)
        },
        'percentili_globali': {
            'fiducia': calcola_percentile_da_tabella(fiducia, percentili_globali['fiducia']),
            'disagio_intimita': calcola_percentile_da_tabella(disagio_intimita, percentili_globali['disagio_intimita']),
            'secondarieta': calcola_percentile_da_tabella(secondarieta, percentili_globali['secondarieta']),
            'bisogno_approvazione': calcola_percentile_da_tabella(bisogno_approvazione, percentili_globali['bisogno_approvazione']),
            'preoccupazione': calcola_percentile_da_tabella(preoccupazione, percentili_globali['preoccupazione'])
        },
        'interpretazione': 'ASQ calcolato correttamente. I punteggi vanno interpretati principalmente sulle cinque scale; i fattori latenti di ansia ed evitamento sono indicatori dimensionali da leggere con cautela.'
    }

    # Percentili per sesso
    if genere:
        genere_norm = genere.strip().lower()

        if genere_norm in ['maschio', 'm', 'uomo']:
            tabelle_sesso = {
                'fiducia': [
                    (1, 16), (2.5, 18), (5, 22), (10, 24), (25, 28),
                    (50, 32), (75, 35.25), (90, 39), (95, 40), (97.5, 41), (99, 43.33)
                ],
                'disagio_intimita': [
                    (1, 20.67), (2.5, 23), (5, 26), (10, 28), (25, 32),
                    (50, 37), (75, 42), (90, 48), (95, 50), (97.5, 53), (99, 57)
                ],
                'secondarieta': [
                    (1, 7), (2.5, 7), (5, 8), (10, 10), (25, 13),
                    (50, 17), (75, 21), (90, 26), (95, 29), (97.5, 32), (99, 36)
                ],
                'bisogno_approvazione': [
                    (1, 8.67), (2.5, 11), (5, 11), (10, 13), (25, 16),
                    (50, 20), (75, 24), (90, 29), (95, 31), (97.5, 32), (99, 34)
                ],
                'preoccupazione': [
                    (1, 13), (2.5, 14), (5, 17), (10, 20), (25, 24),
                    (50, 29), (75, 33), (90, 36), (95, 38), (97.5, 40), (99, 42)
                ]
            }

        elif genere_norm in ['femmina', 'f', 'donna']:
            tabelle_sesso = {
                'fiducia': [
                    (1, 17.76), (2.5, 21), (5, 23), (10, 25), (25, 29),
                    (50, 33), (75, 36), (90, 38), (95, 40), (97.5, 42), (99, 43)
                ],
                'disagio_intimita': [
                    (1, 20.76), (2.5, 23.40), (5, 25), (10, 27), (25, 32),
                    (50, 37), (75, 42), (90, 46), (95, 49), (97.5, 51), (99, 53.24)
                ],
                'secondarieta': [
                    (1, 7), (2.5, 7), (5, 7), (10, 9), (25, 11),
                    (50, 14), (75, 18), (90, 23), (95, 26), (97.5, 29), (99, 32.24)
                ],
                'bisogno_approvazione': [
                    (1, 9), (2.5, 10), (5, 11), (10, 14), (25, 17),
                    (50, 21), (75, 26), (90, 30), (95, 32), (97.5, 34), (99, 36.24)
                ],
                'preoccupazione': [
                    (1, 12), (2.5, 15), (5, 18.80), (10, 22), (25, 26),
                    (50, 30), (75, 33), (90, 37), (95, 38.20), (97.5, 40), (99, 42.24)
                ]
            }
        else:
            tabelle_sesso = None

        if tabelle_sesso:
            risultati['percentili_per_sesso'] = {
                'fiducia': calcola_percentile_da_tabella(fiducia, tabelle_sesso['fiducia']),
                'disagio_intimita': calcola_percentile_da_tabella(disagio_intimita, tabelle_sesso['disagio_intimita']),
                'secondarieta': calcola_percentile_da_tabella(secondarieta, tabelle_sesso['secondarieta']),
                'bisogno_approvazione': calcola_percentile_da_tabella(bisogno_approvazione, tabelle_sesso['bisogno_approvazione']),
                'preoccupazione': calcola_percentile_da_tabella(preoccupazione, tabelle_sesso['preoccupazione'])
            }

    return risultati


# ============================================================================
# ABAS-II — Adaptive Behavior Assessment System, Second Edition
# Tabelle normative: A.9/A.12 (grezzi→ponderati) e A.10/A.13 (somme→compositi)
# Fasce età coperte: adulto_auto 16-74, adulto_etero 16-74,
#                   insegnante 17-21, genitore 17-21
# ============================================================================

def _pp_da_grezzo(grezzo, tabella):
    """tabella: lista [(max_grezzo, pp), ...] ordinata per max_grezzo crescente."""
    for max_g, pp in tabella:
        if grezzo <= max_g:
            return pp
    return 15


def _composito_da_somma(somma, tabella):
    """
    tabella: lista [(soglia_min, composito), ...] ordinata per soglia_min crescente.
    Restituisce il più alto composito la cui soglia_min è ≤ somma.
    """
    result = 40
    for soglia, comp in tabella:
        if somma >= soglia:
            result = comp
        else:
            break
    return result


# ---------------------------------------------------------------------------
# TABELLE GREZZI → PONDERATI  (Tabelle A.9 e A.12)
# Struttura: {fascia: {subscala: [(max_grezzo, pp), ...]}}
# Fonte: Tabella A.9 (autovalutazione) pagine 8-9; A.12 (eterovalutazione) pgg. 20-21
# ---------------------------------------------------------------------------

# -- AUTOVALUTAZIONE (A.9) --

_A9_16_21 = {
    # Righe 1-5 solo Co e Lav sono differenziate; pp 6-10 non distinguibili dall'OCR;
    # righe 11-15 complete. Per pp 6-10 si usa interpolazione lineare sui limiti noti.
    'Co':  [(51,1),(55,2),(60,3),(64,4),(67,5),(68,6),(69,7),(70,8),(71,9),(72,10),(73,11),(74,12),(75,13)],
    'Am':  [(62,6),(63,7),(64,8),(65,9),(66,10),(68,11),(70,12),(72,13)],
    'Sco': [(75,6),(77,7),(78,8),(79,9),(80,10),(81,11)],
    'VC':  [(63,6),(64,7),(65,8),(66,9),(67,10),(68,11),(69,12)],
    'SS':  [(56,6),(57,7),(58,8),(59,9),(60,10)],
    'TL':  [(61,6),(64,7),(65,8),(67,9),(68,10),(69,11)],
    'Cur': [(73,6),(74,7),(75,8)],
    'Ac':  [(66,6),(68,7),(69,8),(71,9),(72,10),(73,11),(74,12),(75,13)],
    'Soc': [(65,6),(66,7),(67,8),(68,9),(69,10),(70,11),(71,12)],
    'Lav': [(28,1),(35,2),(41,3),(46,4),(50,5),(62,6),(65,7),(67,8),(68,9),(69,10),(70,11),(71,12),(72,13)],
}

_A9_22_29 = {
    'Co':  [(51,1),(56,2),(60,3),(64,4),(67,5),(68,6),(69,7),(70,8),(71,9),(72,10),(73,11),(74,12),(75,13)],
    'Am':  [(63,6),(65,7),(66,8),(67,9),(68,10),(69,11),(70,12),(72,13)],
    'Sco': [(76,6),(77,7),(78,8),(79,9),(80,10),(81,11)],
    'VC':  [(63,6),(64,7),(65,8),(66,9),(67,10),(68,11),(69,12)],
    'SS':  [(56,6),(57,7),(58,8),(59,9),(60,10)],
    'TL':  [(62,6),(64,7),(65,8),(66,9),(67,10),(68,11),(69,12)],
    'Cur': [(73,6),(74,7),(75,8)],
    'Ac':  [(67,6),(68,7),(69,8),(70,9),(71,10),(72,11),(73,12),(74,13)],
    'Soc': [(65,6),(66,7),(67,8),(68,9),(69,10),(70,11),(71,12)],
    'Lav': [(28,1),(35,2),(41,3),(46,4),(50,5),(62,6),(64,7),(66,8),(68,9),(69,10),(70,11),(71,12),(72,13)],
}

_A9_30_39 = {
    'Co':  [(35,1),(42,2),(48,3),(53,4),(57,5),(61,6),(65,7),(68,8),(70,9),(71,10),(72,11),(73,12),(75,13)],
    'Am':  [(35,1),(41,2),(46,3),(49,4),(53,5),(56,6),(59,7),(61,8),(64,9),(67,10),(69,11),(71,12),(72,13)],
    'Sco': [(46,1),(51,2),(55,3),(59,4),(63,5),(68,6),(72,7),(75,8),(77,9),(78,10),(79,11),(80,12),(81,13)],
    'VC':  [(32,1),(38,2),(44,3),(49,4),(53,5),(56,6),(59,7),(62,8),(64,9),(65,10),(66,11),(68,12),(69,13)],
    'SS':  [(35,1),(40,2),(44,3),(47,4),(50,5),(52,6),(53,7),(55,8),(56,9),(57,10),(58,11),(60,12)],
    'TL':  [(29,1),(35,2),(40,3),(43,4),(47,5),(50,6),(53,7),(56,8),(59,9),(62,10),(65,11),(68,12),(69,13)],
    'Cur': [(59,1),(62,2),(64,3),(66,4),(68,5),(70,6),(71,7),(72,8),(73,9),(74,10)],
    'Ac':  [(36,1),(42,2),(47,3),(52,4),(56,5),(59,6),(63,7),(66,8),(68,9),(70,10),(72,11),(73,12),(75,13)],
    'Soc': [(36,1),(42,2),(47,3),(51,4),(55,5),(58,6),(60,7),(63,8),(65,9),(66,10),(67,11),(68,12),(69,13)],
    'Lav': [(44,1),(50,2),(55,3),(59,4),(62,5),(64,6),(66,7),(67,8),(68,9),(69,10),(70,11),(71,12),(72,13)],
}

_A9_40_49 = {
    'Co':  [(35,1),(42,2),(48,3),(53,4),(57,5),(61,6),(65,7),(68,8),(70,9),(72,10),(73,11),(74,12),(75,13)],
    'Am':  [(35,1),(41,2),(46,3),(49,4),(53,5),(57,6),(60,7),(63,8),(66,9),(68,10),(69,11),(70,12),(72,13)],
    'Sco': [(46,1),(51,2),(55,3),(59,4),(64,5),(69,6),(73,7),(76,8),(78,9),(79,10),(80,11),(81,12)],
    'VC':  [(32,1),(38,2),(44,3),(49,4),(53,5),(56,6),(59,7),(62,8),(64,9),(66,10),(67,11),(68,12),(69,13)],
    'SS':  [(35,1),(40,2),(44,3),(47,4),(50,5),(53,6),(55,7),(56,8),(57,9),(58,10),(59,11),(60,12)],
    'TL':  [(29,1),(35,2),(40,3),(43,4),(47,5),(50,6),(53,7),(56,8),(59,9),(62,10),(65,11),(68,12),(69,13)],
    'Cur': [(61,1),(63,2),(64,3),(66,4),(68,5),(70,6),(71,7),(72,8),(73,9),(74,10)],
    'Ac':  [(36,1),(42,2),(47,3),(52,4),(56,5),(59,6),(63,7),(66,8),(69,9),(71,10),(72,11),(73,12),(75,13)],
    'Soc': [(36,1),(42,2),(47,3),(51,4),(55,5),(58,6),(60,7),(63,8),(65,9),(66,10),(67,11),(68,12),(69,13)],
    'Lav': [(44,1),(50,2),(55,3),(59,4),(62,5),(64,6),(66,7),(67,8),(68,9),(69,10),(70,11),(71,12),(72,13)],
}

_A9_50_64 = {
    # Fonte: Tabella A.9 continua, pagina 9 (ruotata 180°)
    'Co':  [(41,1),(47,2),(52,3),(56,4),(59,5),(62,6),(65,7),(67,8),(69,9),(71,10),(72,11),(73,12),(75,13)],
    'Am':  [(28,1),(37,2),(44,3),(50,4),(55,5),(59,6),(62,7),(65,8),(68,9),(70,10),(71,11),(72,12)],
    'Sco': [(32,1),(40,2),(47,3),(53,4),(58,5),(63,6),(67,7),(70,8),(73,9),(76,10),(77,11),(78,12),(79,13)],
    'VC':  [(12,1),(22,2),(31,3),(39,4),(46,5),(52,6),(57,7),(61,8),(64,9),(66,10),(67,11),(68,12),(69,13)],
    'SS':  [(29,1),(35,2),(40,3),(43,4),(47,5),(50,6),(53,7),(55,8),(57,9),(59,10),(60,11)],
    'TL':  [(6,1),(14,2),(21,3),(27,4),(32,5),(37,6),(42,7),(48,8),(53,9),(60,10),(63,11),(66,12),(69,13)],
    'Cur': [(61,1),(63,2),(65,3),(67,4),(69,5),(71,6),(72,7),(73,8),(74,9)],
    'Ac':  [(36,1),(42,2),(47,3),(52,4),(56,5),(60,6),(64,7),(66,8),(69,9),(71,10),(72,11),(73,12),(75,13)],
    'Soc': [(36,1),(42,2),(47,3),(51,4),(55,5),(58,6),(60,7),(63,8),(65,9),(66,10),(67,11),(68,12),(69,13)],
    'Lav': [(44,1),(50,2),(55,3),(59,4),(62,5),(64,6),(66,7),(67,8),(68,9),(69,10),(70,11),(71,12),(72,13)],
}

_A9_65_74 = {
    # Fonte: Tabella A.9 continua, pagina 9 (ruotata 180°)
    'Co':  [(57,1),(61,2),(64,3),(67,4),(69,5),(71,6),(72,7),(73,8),(74,9),(75,10)],
    'Am':  [(12,1),(22,2),(31,3),(39,4),(46,5),(52,6),(57,7),(61,8),(64,9),(66,10),(67,11),(68,12),(69,13)],
    'Sco': [(65,1),(69,2),(73,3),(76,4),(78,5),(79,6),(80,7),(81,8)],
    'VC':  [(54,1),(56,2),(59,3),(62,4),(65,5),(67,6),(68,7),(69,8)],
    'SS':  [(21,1),(28,2),(34,3),(39,4),(43,5),(48,6),(52,7),(55,8),(57,9),(59,10),(60,11)],
    'TL':  [(6,1),(14,2),(21,3),(27,4),(32,5),(38,6),(43,7),(49,8),(54,9),(58,10),(62,11),(65,12),(69,13)],
    'Cur': [(52,1),(57,2),(61,3),(64,4),(66,5),(69,6),(71,7),(72,8),(73,9)],
    'Ac':  [(25,1),(34,2),(42,3),(49,4),(55,5),(60,6),(64,7),(67,8),(69,9),(71,10),(72,11),(73,12),(75,13)],
    'Soc': [(39,1),(45,2),(50,3),(54,4),(57,5),(59,6),(62,7),(64,8),(65,9),(66,10),(67,11),(68,12),(69,13)],
    'Lav': [(44,1),(50,2),(55,3),(59,4),(62,5),(64,6),(66,7),(67,8),(68,9),(69,10),(70,11),(71,12),(72,13)],
}

_TABELLE_A9 = {
    '16_21': _A9_16_21,
    '22_29': _A9_22_29,
    '30_39': _A9_30_39,
    '40_49': _A9_40_49,
    '50_64': _A9_50_64,
    '65_74': _A9_65_74,
}


# -- ETEROVALUTAZIONE (A.12) --
# Fonte: Tabella A.12, pagine 20-21 (ruotate 180°)

_A12_16_21 = {
    'Co':  [(30,1),(38,2),(45,3),(51,4),(56,5),(60,6),(64,7),(67,8),(70,9),(72,10),(73,11),(74,12),(75,13)],
    'Am':  [(20,1),(29,2),(37,3),(44,4),(50,5),(55,6),(59,7),(62,8),(65,9),(67,10),(69,11),(71,12),(72,13)],
    'Sco': [(30,1),(39,2),(47,3),(54,4),(60,5),(65,6),(69,7),(73,8),(76,9),(78,10),(79,11),(80,12),(81,13)],
    'VC':  [(15,1),(23,2),(30,3),(36,4),(41,5),(45,6),(49,7),(52,8),(56,9),(60,10),(63,11),(65,12),(67,13),(68,14),(69,15)],
    'SS':  [(23,1),(30,2),(36,3),(41,4),(45,5),(48,6),(51,7),(54,8),(56,9),(57,10),(58,11),(59,12),(60,13)],
    'TL':  [(20,1),(28,2),(35,3),(41,4),(46,5),(50,6),(54,7),(57,8),(60,9),(63,10),(66,11),(68,12),(69,13)],
    'Cur': [(40,1),(47,2),(53,3),(58,4),(62,5),(66,6),(69,7),(71,8),(73,9),(74,10)],
    'Ac':  [(16,1),(25,2),(33,3),(40,4),(46,5),(49,6),(53,7),(58,8),(62,9),(66,10),(69,11),(72,12),(74,13),(75,14)],
    'Soc': [(18,1),(27,2),(35,3),(42,4),(48,5),(53,6),(57,7),(60,8),(63,9),(65,10),(66,11),(67,12),(68,13),(69,14)],
    'Lav': [(26,1),(34,2),(41,3),(47,4),(52,5),(56,6),(59,7),(62,8),(65,9),(68,10),(70,11),(72,12)],
}

_A12_22_29 = {
    'Co':  [(38,1),(45,2),(51,3),(56,4),(60,5),(63,6),(66,7),(69,8),(71,9),(72,10),(73,11),(74,12),(75,13)],
    'Am':  [(29,1),(37,2),(44,3),(50,4),(55,5),(59,6),(62,7),(65,8),(67,9),(69,10),(70,11),(71,12),(72,13)],
    'Sco': [(39,1),(47,2),(54,3),(60,4),(65,5),(69,6),(72,7),(75,8),(77,9),(78,10),(79,11),(80,12),(81,13)],
    'VC':  [(22,1),(30,2),(37,3),(43,4),(48,5),(52,6),(56,7),(60,8),(63,9),(65,10),(66,11),(67,12),(68,13),(69,14)],
    'SS':  [(23,1),(30,2),(36,3),(41,4),(46,5),(50,6),(53,7),(55,8),(56,9),(57,10),(58,11),(59,12),(60,13)],
    'TL':  [(20,1),(28,2),(35,3),(41,4),(46,5),(50,6),(54,7),(57,8),(60,9),(63,10),(66,11),(68,12),(69,13)],
    'Cur': [(44,1),(51,2),(57,3),(62,4),(66,5),(69,6),(71,7),(72,8),(73,9),(74,10)],
    'Ac':  [(23,1),(31,2),(38,3),(44,4),(49,5),(54,6),(58,7),(62,8),(66,9),(69,10),(71,11),(73,12),(74,13),(75,14)],
    'Soc': [(35,1),(41,2),(46,3),(50,4),(53,5),(56,6),(59,7),(62,8),(64,9),(66,10),(68,11),(69,12),(70,13),(71,14)],
    'Lav': [(41,1),(47,2),(52,3),(56,4),(59,5),(62,6),(65,7),(67,8),(69,9),(70,10),(71,11),(72,12)],
}

_A12_30_39 = {
    'Co':  [(38,1),(45,2),(51,3),(56,4),(60,5),(63,6),(66,7),(69,8),(71,9),(72,10),(73,11),(74,12),(75,13)],
    'Am':  [(22,1),(31,2),(39,3),(46,4),(52,5),(57,6),(61,7),(64,8),(67,9),(69,10),(70,11),(71,12),(72,13)],
    'Sco': [(38,1),(46,2),(53,3),(59,4),(64,5),(68,6),(71,7),(74,8),(76,9),(78,10),(79,11),(80,12),(81,13)],
    'VC':  [(22,1),(30,2),(37,3),(43,4),(48,5),(52,6),(56,7),(60,8),(63,9),(65,10),(67,11),(68,12),(69,13)],
    'SS':  [(34,1),(40,2),(45,3),(49,4),(52,5),(54,6),(55,7),(56,8),(57,9),(58,10),(59,11),(60,12)],
    'TL':  [(20,1),(29,2),(36,3),(41,4),(46,5),(50,6),(54,7),(57,8),(60,9),(63,10),(66,11),(68,12),(69,13)],
    'Cur': [(44,1),(51,2),(57,3),(62,4),(66,5),(69,6),(71,7),(72,8),(73,9),(74,10)],
    'Ac':  [(25,1),(34,2),(42,3),(49,4),(55,5),(60,6),(64,7),(67,8),(69,9),(71,10),(72,11),(73,12),(74,13),(75,14)],
    'Soc': [(35,1),(41,2),(46,3),(50,4),(53,5),(56,6),(59,7),(62,8),(64,9),(65,10),(66,11),(67,12),(68,13),(69,14)],
    'Lav': [(41,1),(47,2),(52,3),(56,4),(59,5),(62,6),(65,7),(67,8),(69,9),(70,10),(71,11),(72,12)],
}

_A12_40_49 = {
    'Co':  [(38,1),(45,2),(51,3),(56,4),(60,5),(63,6),(66,7),(69,8),(71,9),(72,10),(73,11),(74,12),(75,13)],
    'Am':  [(29,1),(37,2),(44,3),(50,4),(55,5),(59,6),(62,7),(65,8),(67,9),(69,10),(70,11),(71,12),(72,13)],
    'Sco': [(39,1),(47,2),(54,3),(60,4),(65,5),(69,6),(72,7),(75,8),(77,9),(78,10),(79,11),(80,12),(81,13)],
    'VC':  [(22,1),(30,2),(37,3),(43,4),(48,5),(52,6),(56,7),(60,8),(63,9),(65,10),(66,11),(67,12),(68,13),(69,14)],
    'SS':  [(34,1),(40,2),(45,3),(49,4),(52,5),(54,6),(55,7),(56,8),(57,9),(58,10),(59,11),(60,12)],
    'TL':  [(20,1),(27,2),(33,3),(39,4),(44,5),(48,6),(52,7),(56,8),(59,9),(62,10),(65,11),(67,12),(69,13)],
    'Cur': [(45,1),(52,2),(58,3),(63,4),(67,5),(70,6),(71,7),(72,8),(74,9)],
    'Ac':  [(30,1),(38,2),(45,3),(51,4),(56,5),(61,6),(65,7),(68,8),(70,9),(72,10),(73,11),(74,12),(75,13)],
    'Soc': [(35,1),(41,2),(46,3),(50,4),(53,5),(56,6),(59,7),(62,8),(64,9),(65,10),(66,11),(67,12),(68,13),(69,14)],
    'Lav': [(41,1),(47,2),(52,3),(56,4),(59,5),(62,6),(65,7),(67,8),(69,9),(70,10),(71,11),(72,12)],
}

_A12_50_64 = {
    # Fonte: Tabella A.12 continua, pagina 21 (ruotata 180°)
    'Co':  [(41,1),(48,2),(54,3),(59,4),(63,5),(66,6),(69,7),(71,8),(72,9),(73,10),(74,11),(75,12)],
    'Am':  [(29,1),(37,2),(44,3),(50,4),(55,5),(59,6),(63,7),(65,8),(68,9),(70,10),(71,11),(72,12)],
    'Sco': [(32,1),(39,2),(46,3),(53,4),(59,5),(64,6),(68,7),(72,8),(74,9),(76,10),(78,11),(79,12),(80,13),(81,14)],
    'VC':  [(17,1),(26,2),(34,3),(41,4),(47,5),(52,6),(57,7),(60,8),(63,9),(65,10),(67,11),(68,12),(69,13)],
    'SS':  [(34,1),(40,2),(45,3),(49,4),(52,5),(54,6),(55,7),(56,8),(57,9),(58,10),(59,11),(60,12)],
    'TL':  [(11,1),(19,2),(26,3),(32,4),(37,5),(43,6),(48,7),(52,8),(55,9),(57,10),(60,11),(63,12),(66,13),(69,14)],
    'Cur': [(54,1),(57,2),(61,3),(64,4),(66,5),(69,6),(71,7),(72,8),(73,9),(74,10)],
    'Ac':  [(29,1),(37,2),(44,3),(50,4),(55,5),(59,6),(62,7),(65,8),(67,9),(69,10),(70,11),(71,12),(72,13),(75,14)],
    'Soc': [(35,1),(41,2),(46,3),(50,4),(53,5),(56,6),(59,7),(62,8),(64,9),(65,10),(66,11),(67,12),(68,13),(69,14)],
    'Lav': [(41,1),(47,2),(52,3),(56,4),(59,5),(62,6),(65,7),(67,8),(69,9),(70,10),(71,11),(72,12)],
}

_A12_65_74 = {
    # Fonte: Tabella A.12 continua, pagina 21 (ruotata 180°)
    'Co':  [(41,1),(49,2),(54,3),(58,4),(62,5),(65,6),(68,7),(70,8),(71,9),(72,10),(73,11),(74,12),(75,13)],
    'Am':  [(29,1),(37,2),(44,3),(50,4),(55,5),(59,6),(62,7),(65,8),(67,9),(69,10),(70,11),(71,12),(72,13)],
    'Sco': [(32,1),(39,2),(46,3),(53,4),(59,5),(65,6),(68,7),(71,8),(74,9),(76,10),(78,11),(79,12),(80,13),(81,14)],
    'VC':  [(15,1),(23,2),(30,3),(36,4),(41,5),(44,6),(48,7),(52,8),(56,9),(60,10),(63,11),(65,12),(67,13),(68,14),(69,15)],
    'SS':  [(34,1),(40,2),(45,3),(49,4),(52,5),(54,6),(55,7),(56,8),(57,9),(58,10),(59,11),(60,12)],
    'TL':  [(11,1),(19,2),(26,3),(32,4),(37,5),(43,6),(48,7),(52,8),(55,9),(57,10),(60,11),(63,12),(66,13),(69,14)],
    'Cur': [(54,1),(57,2),(61,3),(64,4),(66,5),(69,6),(71,7),(72,8),(73,9),(74,10)],
    'Ac':  [(25,1),(34,2),(42,3),(49,4),(55,5),(60,6),(64,7),(67,8),(69,9),(71,10),(72,11),(73,12),(74,13),(75,14)],
    'Soc': [(35,1),(41,2),(46,3),(50,4),(53,5),(57,6),(59,7),(62,8),(64,9),(65,10),(66,11),(67,12),(68,13),(69,14)],
    'Lav': [(41,1),(47,2),(52,3),(56,4),(59,5),(62,6),(65,7),(67,8),(69,9),(70,10),(71,11),(72,12)],
}

_TABELLE_A12 = {
    '16_21': _A12_16_21,
    '22_29': _A12_22_29,
    '30_39': _A12_30_39,
    '40_49': _A12_40_49,
    '50_64': _A12_50_64,
    '65_74': _A12_65_74,
}


# -- INSEGNANTE (età 17-21) — Tabella A.1 --
# Nota: la tabella A.1 per età 17-21 ha molte caselle vuote (scala top-out);
# i valori mostrati coprono solo pp 1 (molto bassa prestazione).
_A1_17_21 = {
    'Co':  [(75,1)],
    'Am':  [(75,1)],
    'VS':  [(75,1)],
    'SS':  [(60,1)],
    'TL':  [(69,1)],
    'Cur': [(75,1)],
    'Ac':  [(75,1)],
    'Soc': [(69,1)],
    'Lav': [(72,1)],
}

# -- GENITORE (età 17-21) — Tabella A.5 --
_A5_17_21 = {
    'Co':  [(75,1)],
    'Am':  [(72,1)],
    'Sco': [(81,1)],
    'VC':  [(69,1)],
    'SS':  [(60,1)],
    'TL':  [(69,1)],
    'Cur': [(75,1)],
    'Ac':  [(75,1)],
    'Soc': [(69,1)],
    'Lav': [(72,1)],
}


# ---------------------------------------------------------------------------
# TABELLE SOMME PONDERATI → COMPOSITI  (Tabelle A.10, A.13, A.2, A.5-cont)
# Struttura: {fascia: {colonna: [(soglia_min, composito), ...]}}
# Ogni lista è ordinata per soglia_min crescente.
# ---------------------------------------------------------------------------

def _costruisci_lookup_composito(dati):
    """
    dati: dict {composito: (GAC_s_min, GAC_c_min, DAC_min, DAS_min, DAP_s_min, DAP_c_min)}
    Restituisce dict {colonna: [(soglia_min, composito), ...]}
    """
    cols = ['GAC_s', 'GAC_c', 'DAC', 'DAS', 'DAP_s', 'DAP_c']
    lookup = {c: [] for c in cols}
    for comp in sorted(dati.keys()):
        vals = dati[comp]
        for i, col in enumerate(cols):
            v = vals[i]
            if v is not None:
                lookup[col].append((v, comp))
    return lookup


# -- AUTOVALUTAZIONE compositi (A.10) --
# Dati: composito → (GAC_senza_min, GAC_con_min, DAC_min, DAS_min, DAP_senza_min, DAP_con_min)
# None = valore non presente nella tabella per quel composito

_dati_A10_22_29 = {
    40: (9,  None, None, None, 4,    None),
    47: (72, 81,   23,   None, 33,   42  ),
    48: (73, 82,   None, None, 34,   43  ),
    49: (75, 84,   24,   17,   35,   44  ),
    50: (77, 86,   None, None, 36,   46  ),
    51: (79, 88,   25,   None, 37,   47  ),
    52: (80, 90,   26,   18,   38,   48  ),
    53: (82, 92,   27,   None, 39,   49  ),
    55: (86, 96,   28,   19,   40,   50  ),
    56: (88, 98,   29,   None, 41,   51  ),
    57: (90, 100,  30,   20,   42,   52  ),
    58: (91, 102,  None, 21,   None, 53  ),
    59: (93, 104,  31,   None, 43,   54  ),
    60: (95, 106,  32,   22,   None, None),
    61: (97, 108,  33,   None, 44,   55  ),
    62: (99, 110,  None, None, 45,   56  ),
    63: (100,111,  34,   23,   None, 57  ),
    64: (102,113,  None, None, 46,   None),
    65: (104,115,  35,   None, None, 58  ),
    66: (105,117,  None, 24,   47,   None),
    67: (107,118,  36,   None, None, 59  ),
    68: (108,120,  None, None, None, None),
    69: (110,122,  37,   None, 48,   60  ),
    70: (111,123,  None, 25,   None, None),
    71: (112,124,  None, None, None, 61  ),
    72: (113,126,  38,   None, 49,   None),
    73: (114,127,  None, None, None, 62  ),
    75: (116,130,  39,   26,   50,   None),
    76: (117,131,  None, None, None, 63  ),
    78: (119,133,  None, None, 51,   None),
    79: (120,134,  40,   27,   52,   64  ),
}

_dati_A10_16_21 = {
    # Fonte: pagina 10 (ruotata 180°) — struttura identica ad A.10
    40: (None,None, None, None, None, None),
    57: (None,None, None, None, None, None),
    67: (20,  None, None, None, None, None),
    69: (21,  14,   30,   None, None, None),
    70: (None,None, None, 31,   None, None),
    71: (22,  15,   32,   None, None, None),
    72: (None,None, None, None, None, None),
    73: (None,16,   None, 33,   None, None),
    74: (23,  None, None, None, 34,   None),
    75: (None,17,   None, None, 35,   None),
    76: (24,  None, None, 34,   None, 36  ),
    77: (None,18,   None, None, None, None),
    78: (25,  None, 35,   None, 36,   None),
    79: (None,None, None, 35,   None, 37  ),
    80: (None,19,   None, None, None, None),
    81: (26,  None, 36,   None, 37,   None),
    82: (27,  20,   None, None, 38,   None),
    83: (None,None, None, 36,   None, 38  ),
    84: (28,  None, None, None, 39,   None),
    85: (None,21,   37,   None, None, None),
    86: (None,None, None, 37,   None, 39  ),
    87: (29,  None, None, None, 40,   None),
    88: (None,22,   38,   None, None, 40  ),
    89: (30,  None, None, None, 41,   None),
    90: (None,23,   None, 38,   42,   None),
    91: (31,  None, 39,   None, None, 41  ),
    92: (None,None, None, None, None, None),
    93: (None,24,   None, None, None, None),
    94: (32,  None, 40,   39,   43,   None),
    95: (None,None, None, None, None, 42  ),
    96: (33,  25,   None, None, None, None),
    97: (None,None, 41,   None, 44,   None),
    98: (34,  None, None, 40,   None, 43  ),
    99: (None,26,   None, None, 45,   None),
    100:(35,  None, 42,   None, None, None),
    101:(None,None, None, 41,   None, 44  ),
    102:(None,27,   None, None, 46,   None),
    103:(36,  None, 43,   None, None, None),
    104:(None,None, None, 42,   None, 45  ),
    105:(None,28,   None, None, 47,   None),
    106:(37,  None, 44,   None, None, None),
    107:(None,None, None, 43,   None, 46  ),
    108:(None,29,   None, None, 48,   None),
    109:(38,  None, 45,   None, None, None),
    110:(None,None, None, 44,   None, 47  ),
    111:(None,30,   None, None, 49,   None),
    112:(39,  None, 46,   None, None, None),
    113:(None,None, None, 45,   None, 48  ),
    114:(None,31,   None, None, 50,   None),
    115:(40,  None, 47,   None, None, None),
    116:(None,None, None, 46,   None, 49  ),
    117:(None,32,   None, None, 51,   None),
    118:(41,  None, 48,   None, None, None),
    119:(None,None, None, 47,   None, 50  ),
    120:(39,  33,   49,   None, 52,   None),
    124:(None,None, None, 48,   None, 51  ),
    131:(None,38,   57,   None, 76,   None),
}

_dati_A10_30_39 = {
    40: (9,  2,    None, None, None, None),
    41: (10, 10,   None, None, None, None),
    43: (12, 12,   None, None, 4,    5   ),
    45: (14, 14,   None, None, 5,    6   ),
    47: (16, 16,   None, None, 6,    7   ),
    49: (18, 18,   3,    None, 7,    8   ),
    51: (20, 20,   4,    None, 8,    9   ),
    53: (22, 22,   5,    None, 9,    10  ),
    55: (24, 24,   6,    2,    10,   11  ),
    56: (25, 26,   None, None, None, 12  ),
    57: (26, 28,   7,    None, 11,   13  ),
    58: (27, 30,   None, 3,    None, 14  ),
    59: (28, 32,   8,    None, 12,   15  ),
    60: (29, 34,   None, None, None, 16  ),
    61: (30, 36,   9,    4,    13,   17  ),
    63: (34, 40,   10,   None, 14,   19  ),
    65: (38, 44,   11,   None, 15,   21  ),
    67: (42, 48,   12,   None, 16,   23  ),
    68: (44, 50,   None, 7,    None, 24  ),
    69: (46, 52,   13,   None, 17,   25  ),
    70: (48, 54,   14,   8,    18,   26  ),
    71: (50, 56,   None, None, None, 27  ),
    73: (53, 59,   None, None, 20,   29  ),
    74: (None,None,None, None, None, None),
    75: (54, 60,   16,   10,   21,   None),
    76: (55, 61,   None, None, None, 30  ),
    77: (56, 63,   None, 11,   23,   31  ),
    78: (None,None,None, None, None, 32  ),
    79: (58, 65,   None, None, None, None),
    80: (59, 68,   18,   None, 25,   34  ),
    116:(None,None,40,   26,   51,   63  ),
}

_dati_A10_40_49 = {
    40: (9,  2,    None, None, None, None),
    41: (10, 10,   None, None, None, None),
    43: (12, 12,   None, None, 4,    5   ),
    45: (14, 14,   None, None, 5,    6   ),
    47: (16, 16,   None, None, 6,    7   ),
    49: (18, 18,   3,    None, 7,    8   ),
    51: (20, 20,   4,    None, 8,    9   ),
    53: (22, 22,   5,    None, 9,    10  ),
    55: (24, 24,   6,    2,    10,   11  ),
    57: (26, 28,   7,    None, 11,   13  ),
    59: (28, 32,   8,    None, 12,   15  ),
    61: (30, 36,   9,    4,    13,   17  ),
    63: (34, 40,   10,   None, 14,   19  ),
    65: (38, 44,   11,   None, 15,   21  ),
    67: (42, 48,   12,   None, 16,   23  ),
    69: (46, 52,   13,   None, 17,   25  ),
    70: (48, 54,   14,   8,    18,   26  ),
    75: (54, 60,   16,   10,   21,   None),
    80: (59, 68,   18,   None, 25,   34  ),
    116:(None,None,40,   26,   51,   63  ),
}

_dati_A10_50_64 = {
    40: (None,None,None, None, None, None),
    57: (69,  71,  None, None, None, None),
    58: (71,  72,  None, None, 25,   None),
    59: (73,  74,  None, None, None, 26  ),
    60: (75,  76,  19,   None, None, None),
    61: (75,  76,  None, None, 26,   None),
    62: (77,  78,  None, None, None, 27  ),
    63: (79,  80,  20,   None, None, None),
    64: (None,None,None, None, 27,   28  ),
    65: (81,  82,  21,   14,   None, None),
    66: (83,  84,  None, None, 28,   None),
    67: (85,  86,  22,   None, None, 29  ),
    68: (87,  88,  None, None, 29,   None),
    69: (89,  90,  23,   15,   None, 30  ),
    70: (91,  92,  None, None, 30,   None),
    71: (93,  94,  24,   16,   None, 31  ),
    72: (95,  96,  25,   None, 31,   None),
    73: (97,  98,  None, 17,   None, 32  ),
    74: (None,None,26,   None, 32,   None),
    75: (99, 100,  None, None, None, 33  ),
    76: (101,102,  27,   18,   None, None),
    77: (103,104,  None, None, 33,   34  ),
    78: (105,106,  28,   19,   None, None),
    79: (107,108,  None, None, 34,   None),
    80: (None,None,29,   20,   None, 35  ),
    117:(None,None,40,   26,   51,   None),
}

_dati_A10_65_74 = {
    40: (None,None,None, None, None, None),
    57: (63,  63,  None, None, None, None),
    59: (66,  None,None, None, None, None),
    60: (None,None,None, 12,   None, None),
    61: (None,66,  None, None, None, None),
    62: (67,  None,None, None, 25,   None),
    63: (69,  70,  None, 13,   None, 32  ),
    64: (71,  72,  None, None, None, None),
    65: (None,None,None, None, 28,   33  ),
    66: (72,  73,  22,   14,   None, None),
    67: (None,75,  None, None, 29,   None),
    68: (74,  76,  23,   None, None, 34  ),
    69: (None,None,None, 15,   30,   None),
    70: (76,  79,  24,   None, None, 35  ),
    71: (None,80,  None, 16,   31,   None),
    72: (79,  82,  25,   None, None, 36  ),
    73: (None,83,  None, 17,   None, None),
    74: (80,  85,  26,   None, 32,   37  ),
    75: (83,  87,  None, 18,   None, None),
    76: (None,88,  27,   None, None, 38  ),
    77: (86,  90,  None, 19,   33,   None),
    78: (89,  91,  None, None, None, 39  ),
    79: (91,  92,  28,   None, None, None),
    80: (93,  98,  29,   20,   34,   40  ),
    120:(120, 134, 40,   26,   51,   63  ),
}

_LOOKUP_A10 = {
    '16_21': _costruisci_lookup_composito(_dati_A10_16_21),
    '22_29': _costruisci_lookup_composito(_dati_A10_22_29),
    '30_39': _costruisci_lookup_composito(_dati_A10_30_39),
    '40_49': _costruisci_lookup_composito(_dati_A10_40_49),
    '50_64': _costruisci_lookup_composito(_dati_A10_50_64),
    '65_74': _costruisci_lookup_composito(_dati_A10_65_74),
}


# -- ETEROVALUTAZIONE compositi (A.13) --
# Stessa struttura di A.10

_dati_A13_16_21 = {
    # Fonte: pagina 22 (ruotata 180°)
    40: (None,None,None, None, None, None),
    62: (67,  75,  None, None, None, None),
    63: (68,  76,  None, 13,   None, 29  ),
    64: (69,  77,  None, None, None, None),
    65: (70,  78,  None, None, None, 30  ),
    66: (71,  79,  None, None, None, None),
    67: (72,  80,  None, None, None, 31  ),
    68: (73,  81,  None, 14,   None, None),
    69: (74,  82,  None, None, None, 32  ),
    70: (75,  83,  None, 15,   None, None),
    71: (76,  84,  None, None, None, 33  ),
    72: (77,  85,  None, 16,   None, None),
    73: (78,  86,  None, None, None, 34  ),
    74: (None,87,  None, 17,   None, None),
    75: (None,88,  None, None, None, 35  ),
    76: (None,90,  None, 18,   None, None),
    77: (None,91,  None, None, None, 36  ),
    78: (None,92,  None, 19,   None, None),
    79: (None,94,  None, None, None, 37  ),
    80: (None,95,  None, 20,   None, None),
    81: (None,96,  27,   None, None, 38  ),
    82: (None,98,  None, 21,   None, None),
    83: (None,99,  None, None, None, 39  ),
    84: (None,100, None, None, None, None),
    85: (None,101, 28,   None, None, 40  ),
    86: (None,103, None, None, None, None),
    87: (None,104, 29,   None, None, 41  ),
    88: (None,105, None, None, None, None),
    89: (None,106, 30,   None, None, 42  ),
    90: (None,107, 31,   None, None, None),
    91: (None,108, None, None, None, 43  ),
    92: (None,110, 31,   None, None, None),
    93: (None,111, None, None, None, None),
    94: (None,112, 32,   None, None, 44  ),
    95: (None,113, None, None, None, None),
    97: (None,115, 33,   None, None, None),
    98: (None,116, None, None, None, 45  ),
    99: (None,117, 34,   None, None, None),
    100:(None,118, None, None, None, None),
    101:(None,119, 35,   None, None, 46  ),
    102:(None,120, None, None, None, None),
    103:(None,121, 36,   None, None, None),
    105:(None,122, None, None, None, None),
    106:(None,123, 37,   None, None, 47  ),
    107:(None,124, None, None, None, None),
    108:(None,125, 38,   None, None, None),
    109:(None,126, None, None, None, 48  ),
    110:(None,127, 39,   None, None, None),
    111:(None,128, None, None, None, None),
    112:(None,129, None, None, None, 49  ),
    113:(None,130, None, None, None, None),
    117:(None,None,40,   None, None, 50  ),
    118:(None,None,41,   None, None, None),
    125:(None,138, 57,   None, None, 76  ),
}

_dati_A13_22_29 = {
    # Fonte: pagina 23 (ruotata 180°)
    40: (None,None,None, None, None, None),
    62: (67,  75,  None, None, None, None),
    63: (68,  76,  None, 13,   None, 32  ),
    64: (69,  77,  None, None, None, None),
    65: (70,  78,  None, None, None, None),
    66: (71,  79,  None, None, None, None),
    67: (72,  80,  None, None, None, None),
    68: (73,  81,  None, None, None, None),
    69: (74,  82,  None, 14,   None, 33  ),
    70: (75,  83,  None, None, None, None),
    71: (76,  84,  None, None, None, None),
    72: (77,  85,  None, None, None, None),
    73: (78,  86,  None, 15,   None, None),
    74: (79,  87,  None, None, None, 34  ),
    75: (81,  88,  24,   None, 33,   None),
    76: (83,  89,  None, 16,   None, 35  ),
    77: (85,  90,  None, None, 34,   None),
    78: (87,  91,  25,   None, None, 36  ),
    79: (89,  92,  None, 17,   35,   None),
    80: (None,93,  26,   None, None, 37  ),
    81: (91,  95,  27,   None, 36,   None),
    82: (83,  96,  None, None, None, None),
    83: (85,  97,  28,   18,   37,   38  ),
    84: (87,  98,  29,   None, None, None),
    85: (89,  99,  None, 19,   38,   39  ),
    86: (91, 100,  None, None, None, None),
    87: (92, 101,  30,   None, 39,   None),
    88: (94, 103,  None, None, None, 40  ),
    89: (96, 104,  None, 20,   40,   None),
    90: (None,105, 31,   None, None, 41  ),
    91: (None,106, None, None, 41,   None),
    92: (None,107, 32,   None, None, None),
    93: (None,108, None, 21,   42,   42  ),
    94: (None,109, 33,   None, None, None),
    95: (None,110, None, None, 43,   None),
    96: (None,111, 34,   None, None, 43  ),
    97: (None,112, None, 22,   44,   None),
    98: (None,113, 35,   None, None, None),
    99: (None,114, None, None, 45,   44  ),
    100:(None,115, 36,   None, None, None),
    101:(None,116, None, 23,   46,   None),
    102:(None,117, None, None, None, 45  ),
    103:(None,118, 37,   None, None, None),
    104:(None,119, None, None, 47,   None),
    105:(None,120, None, 24,   None, 46  ),
    106:(None,121, 38,   None, 48,   None),
    107:(None,122, None, None, None, None),
    108:(None,123, None, 25,   None, 47  ),
    109:(None,124, None, None, 49,   None),
    110:(None,125, 39,   None, None, None),
    111:(None,126, None, None, None, 48  ),
    112:(None,127, None, 26,   50,   None),
    113:(None,128, None, None, None, None),
    114:(None,129, None, None, None, 49  ),
    116:(None,130, 39,   None, 51,   None),
    117:(None,131, None, 27,   None, None),
    125:(None,138, 57,   38,   76,   65  ),
}

_dati_A13_30_39 = {
    # Fonte: pagina 24 (ruotata 180°)
    40: (None,None,None, None, None, None),
    61: (None,70,  None, None, None, None),
    62: (None,72,  None, None, None, None),
    63: (None,74,  None, None, None, None),
    64: (None,75,  20,   13,   None, 27  ),
    65: (None,76,  None, None, None, None),
    66: (None,77,  21,   None, None, None),
    67: (None,78,  None, None, None, 28  ),
    68: (None,79,  22,   None, None, None),
    69: (None,80,  23,   None, None, 29  ),
    70: (None,81,  None, None, None, None),
    71: (None,82,  None, None, None, 30  ),
    72: (None,83,  None, None, None, None),
    73: (None,84,  24,   None, None, 31  ),
    74: (None,85,  25,   None, None, None),
    75: (None,86,  None, None, None, 32  ),
    76: (None,87,  None, None, None, None),
    77: (None,88,  26,   None, None, 33  ),
    78: (None,89,  None, None, None, None),
    79: (None,90,  27,   None, None, 34  ),
    80: (None,91,  28,   None, None, None),
    81: (None,92,  None, None, None, 35  ),
    82: (None,93,  29,   None, None, None),
    83: (None,94,  None, None, None, 36  ),
    84: (None,95,  None, None, None, None),
    85: (None,96,  30,   None, None, 37  ),
    86: (None,97,  31,   None, None, None),
    87: (None,98,  None, None, None, 38  ),
    88: (None,99,  None, None, None, None),
    89: (None,100, 32,   None, None, 39  ),
    90: (None,101, 33,   None, None, None),
    91: (None,102, None, None, None, 40  ),
    92: (None,103, None, None, None, None),
    93: (None,104, 34,   None, None, None),
    94: (None,105, None, None, None, 41  ),
    95: (None,106, None, None, None, None),
    96: (None,107, 35,   None, None, 42  ),
    97: (None,108, None, None, None, None),
    98: (None,109, None, None, None, 43  ),
    99: (None,110, 36,   None, None, None),
    100:(None,111, None, None, None, 44  ),
    102:(None,113, 37,   None, None, None),
    103:(None,114, None, None, None, 45  ),
    104:(None,115, None, None, None, None),
    105:(None,116, 38,   None, None, 46  ),
    106:(None,117, None, None, None, None),
    107:(None,118, None, None, None, 47  ),
    108:(None,119, 39,   None, None, None),
    109:(None,120, None, None, None, 48  ),
    120:(None,131, 40,   None, None, 62  ),
    125:(None,138, 57,   38,   76,   95  ),
}

_dati_A13_40_49 = {
    # Fonte: pagine 25-26
    40: (None,None,None, None, None, None),
    70: (68,  None,19,   None, 27,   34  ),
    71: (70,  None,None, 13,   28,   36  ),
    72: (72,  None,20,   None, 29,   37  ),
    73: (75,  None,21,   14,   30,   38  ),
    74: (77,  None,None, None, 31,   39  ),
    75: (79,  None,22,   None, 32,   41  ),
    76: (81,  None,23,   15,   33,   42  ),
    77: (83,  None,24,   None, 34,   43  ),
    78: (86,  None,25,   16,   35,   44  ),
    79: (88,  None,26,   None, 36,   45  ),
    80: (90,  None,None, 17,   37,   46  ),
    81: (92,  None,27,   None, 38,   47  ),
    82: (94,  None,28,   18,   39,   None),
    83: (96,  None,29,   None, None, 48  ),
    84: (98,  None,30,   19,   None, 49  ),
    85: (100, None,None, None, 40,   None),
    86: (None,None,None, None, None, None),
    87: (101, None,31,   20,   41,   None),
    88: (103, None,None, None, None, 50  ),
    89: (105, None,32,   None, 42,   None),
    90: (107, None,None, 21,   None, 51  ),
    91: (109, None,33,   None, 43,   None),
    92: (110, None,None, None, None, 52  ),
    93: (111, None,None, None, 43,   None),
    94: (112, None,34,   22,   None, None),
    95: (113, None,None, None, None, 53  ),
    97: (115, None,None, None, 44,   None),
    98: (116, None,35,   None, None, 54  ),
    99: (117, None,None, None, None, None),
    100:(118, None,36,   None, None, 55  ),
    101:(119, None,None, None, 45,   56  ),
    102:(120, None,None, None, None, None),
    103:(121, None,37,   23,   46,   None),
    104:(122, None,None, None, None, 57  ),
    105:(123, None,None, None, 47,   None),
    106:(None,None,36,   24,   None, 58  ),
    107:(None,None,None, None, None, None),
    108:(None,None,37,   None, 48,   None),
    109:(None,None,None, None, None, 59  ),
    110:(None,None,38,   None, None, None),
    112:(None,None,39,   25,   49,   None),
    113:(None,None,None, None, None, 61  ),
    114:(None,None,None, None, None, None),
    116:(None,None,39,   26,   50,   None),
    117:(None,None,None, None, None, 62  ),
    118:(None,138, 40,   27,   51,   None),
    125:(None,None,57,   38,   76,   63  ),
}

_dati_A13_50_64 = {
    # Fonte: pagine 27-28
    40: (None,None,None, None, None, None),
    69: (None,70,  None, None, None, None),
    70: (None,72,  19,   None, None, 27  ),
    71: (None,74,  None, None, 28,   None),
    72: (None,76,  20,   14,   None, None),
    73: (None,78,  21,   None, 29,   36  ),
    74: (None,80,  None, 15,   30,   None),
    75: (None,82,  22,   None, 31,   38  ),
    76: (None,84,  23,   None, None, None),
    77: (None,85,  None, 16,   32,   39  ),
    78: (None,87,  24,   None, 33,   None),
    79: (None,89,  25,   17,   None, 40  ),
    80: (None,91,  None, None, 34,   None),
    81: (None,93,  26,   18,   35,   41  ),
    82: (None,94,  27,   None, 36,   None),
    83: (None,96,  28,   19,   None, 42  ),
    84: (None,97,  None, None, 37,   None),
    85: (None,98,  None, None, 38,   43  ),
    86: (None,99,  29,   20,   None, None),
    87: (None,101, None, None, 39,   None),
    88: (None,102, None, None, None, 44  ),
    89: (None,103, 30,   None, 40,   None),
    90: (None,104, None, 21,   None, None),
    91: (None,106, 31,   None, 41,   None),
    92: (None,107, None, None, None, 45  ),
    93: (None,108, 32,   None, None, None),
    94: (None,109, None, 22,   42,   46  ),
    95: (None,110, 33,   None, None, None),
    96: (None,111, None, None, 43,   None),
    97: (None,112, None, None, None, 47  ),
    98: (None,113, 34,   None, None, None),
    99: (None,114, None, 23,   44,   48  ),
    100:(None,115, 35,   None, None, None),
    101:(None,116, None, None, 45,   None),
    102:(None,117, None, None, None, 49  ),
    103:(None,118, 36,   None, None, None),
    104:(None,119, None, 24,   46,   50  ),
    105:(None,120, 37,   None, None, None),
    106:(None,121, None, None, 47,   None),
    107:(None,122, None, None, None, 51  ),
    108:(None,123, 38,   None, None, None),
    109:(None,124, None, 25,   48,   52  ),
    110:(None,125, None, None, None, None),
    111:(None,126, 39,   None, None, None),
    112:(None,127, None, 26,   None, 53  ),
    117:(None,131, 39,   None, 50,   None),
    118:(None,132, 40,   27,   51,   None),
    125:(None,138, 57,   38,   76,   64  ),
}

_dati_A13_65_74 = {
    # Fonte: pagine 29-30
    40: (None,None,None, None, None, None),
    69: (None,70,  None, None, None, 27  ),
    70: (None,72,  19,   None, 28,   None),
    71: (None,74,  None, None, 29,   None),
    72: (None,76,  20,   14,   None, 37  ),
    73: (None,78,  21,   None, 30,   38  ),
    74: (None,80,  None, 15,   31,   39  ),
    75: (None,82,  22,   None, 32,   None),
    76: (None,84,  23,   None, None, 40  ),
    77: (None,85,  None, 16,   33,   None),
    78: (None,87,  24,   None, None, 41  ),
    79: (None,89,  25,   17,   34,   None),
    80: (None,91,  None, None, None, 42  ),
    81: (None,93,  26,   18,   35,   None),
    82: (None,94,  27,   None, None, 43  ),
    83: (None,96,  28,   None, 36,   None),
    84: (None,97,  None, None, None, 44  ),
    85: (None,98,  29,   19,   37,   None),
    86: (None,99,  None, None, None, 45  ),
    87: (None,101, 30,   None, None, None),
    88: (None,102, None, None, 38,   46  ),
    89: (None,103, None, None, None, None),
    90: (None,104, 31,   None, None, None),
    91: (None,106, None, None, 39,   None),
    92: (None,107, 32,   None, None, 47  ),
    93: (None,108, None, 21,   40,   None),
    94: (None,109, 33,   None, None, None),
    95: (None,110, None, None, 41,   None),
    96: (None,111, None, 22,   None, 48  ),
    97: (None,112, 34,   None, 42,   None),
    98: (None,113, None, None, None, None),
    99: (None,114, None, 23,   43,   49  ),
    100:(None,115, 35,   None, None, None),
    101:(None,116, None, None, 44,   None),
    102:(None,117, None, None, None, 50  ),
    103:(None,118, 36,   None, 45,   None),
    104:(None,119, None, 24,   None, None),
    105:(None,120, None, None, 46,   51  ),
    106:(None,121, 37,   None, None, None),
    107:(None,122, None, None, 47,   None),
    108:(None,123, None, 25,   None, 52  ),
    109:(None,124, None, None, 48,   None),
    110:(None,125, 38,   None, None, None),
    111:(None,126, None, None, None, 53  ),
    112:(None,127, None, 26,   49,   None),
    113:(None,128, 39,   None, None, None),
    114:(None,129, None, None, None, 54  ),
    117:(None,132, None, None, 50,   None),
    118:(None,None,40,   27,   51,   None),
    125:(None,138, 57,   38,   76,   64  ),
}

_LOOKUP_A13 = {
    '16_21': _costruisci_lookup_composito(_dati_A13_16_21),
    '22_29': _costruisci_lookup_composito(_dati_A13_22_29),
    '30_39': _costruisci_lookup_composito(_dati_A13_30_39),
    '40_49': _costruisci_lookup_composito(_dati_A13_40_49),
    '50_64': _costruisci_lookup_composito(_dati_A13_50_64),
    '65_74': _costruisci_lookup_composito(_dati_A13_65_74),
}


# -- INSEGNANTE compositi (A.2) — età 17-21 —  Fonte: foto Tabella A.2 --
_dati_A2_insegnante = {
    # composito → (GAC_min, DAC_min, DAS_min, DAP_min)
    # Colonne: GAC | DAC | DAS | DAP
    40: (9,   None, None, None),
    41: (9,   None, None, None),
    42: (10,  None, None, None),
    43: (11,  None, None, None),
    44: (12,  None, None, None),
    45: (13,  None, None, 5   ),
    46: (14,  None, None, None),
    47: (15,  None, None, 6   ),
    48: (16,  3,    None, None),
    49: (17,  None, None, 7   ),
    50: (18,  None, None, None),
    51: (19,  4,    None, 8   ),
    52: (20,  None, None, None),
    53: (21,  5,    None, 9   ),
    54: (22,  None, 2,    None),
    55: (23,  6,    None, 10  ),
    56: (24,  None, None, None),
    57: (25,  7,    3,    11  ),
    58: (26,  None, None, None),
    59: (27,  8,    None, 12  ),
    60: (28,  None, 4,    None),
    61: (29,  9,    None, 13  ),
    62: (30,  None, 5,    None),
    63: (31,  10,   None, 14  ),
    64: (32,  None, 6,    None),
    65: (33,  11,   None, 15  ),
    66: (34,  None, 7,    None),
    67: (35,  12,   None, 16  ),
    68: (36,  None, 8,    None),
    69: (37,  13,   None, 17  ),
    70: (38,  14,   9,    18  ),
    71: (39,  None, None, None),
    72: (40,  15,   10,   19  ),
    73: (41,  None, None, None),
    74: (42,  None, None, None),
    75: (43,  16,   11,   20  ),
    76: (44,  None, None, None),
    77: (45,  17,   12,   21  ),
    78: (47,  None, None, 22  ),
    79: (50,  None, None, None),
    # Dalla foto, sezione destra (Insegnante):
    81: (56,  18,   13,   26  ),
    82: (59,  None, None, None),
    83: (62,  19,   None, 28  ),
    84: (63,  None, None, None),
    85: (64,  None, 14,   None),
    86: (66,  20,   None, 30  ),
    87: (68,  21,   15,   31  ),
    88: (70,  None, None, 32  ),
    89: (72,  22,   None, None),
    90: (74,  None, None, 33  ),
    91: (75,  23,   None, None),
    92: (77,  None, None, 34  ),
    93: (78,  None, 16,   None),
    94: (79,  None, None, None),
    95: (80,  None, None, None),
    96: (81,  29,   17,   None),
    97: (82,  None, None, None),
    98: (85,  None, None, None),
    99: (86,  30,   None, 36  ),
    100:(87,  None, None, None),
    101:(88,  None, None, None),
    102:(89,  31,   None, None),
    103:(91,  None, None, None),
    104:(92,  None, 18,   None),
    105:(93,  None, None, None),
    106:(94,  None, None, None),
    107:(95,  32,   None, 37  ),
    108:(96,  None, None, None),
    109:(97,  None, None, None),
    110:(98,  None, 19,   None),
    111:(99,  None, None, None),
    112:(101, 33,   None, None),
    113:(102, None, None, None),
    114:(103, None, None, None),
    115:(104, None, 20,   None),
    116:(105, None, None, None),
    117:(107, 34,   None, 38  ),
    118:(108, None, None, None),
    119:(109, None, None, None),
    120: (113,None, 21,   None),
    121: (None,None,None, None),
    131: (35, 35,   25,   47  ),
}

_LOOKUP_A2 = {}
for comp, vals in _dati_A2_insegnante.items():
    cols = ['GAC', 'DAC', 'DAS', 'DAP']
    for i, col in enumerate(cols):
        if col not in _LOOKUP_A2:
            _LOOKUP_A2[col] = []
        v = vals[i]
        if v is not None:
            _LOOKUP_A2[col].append((v, comp))


# -- GENITORE compositi (A.5 continua) — età 17-21 --
# Fonte: pagina 5
_dati_A5_genitore = {
    # composito → (GAC_min, DAC_min, DAS_min, DAP_min)
    40: (None, None, None, None),
    43: (61,   None, None, None),
    44: (64,   None, None, None),
    45: (66,   None, None, None),
    46: (68,   None, None, None),
    47: (71,   None, None, None),
    48: (73,   None, None, None),
    49: (75,   24,   None, None),
    50: (78,   25,   None, None),
    51: (80,   26,   None, None),
    52: (82,   27,   17,   None),
    53: (85,   None, None, None),
    54: (None, None, 18,   None),
    55: (88,   29,   19,   None),
    57: (89,   30,   20,   42  ),
    58: (None, None, None, None),
    59: (91,   31,   None, None),
    60: (93,   32,   21,   43  ),
    61: (94,   None, None, None),
    62: (95,   None, None, None),
    63: (97,   33,   None, 45  ),
    64: (98,   None, None, None),
    65: (99,   None, None, 46  ),
    66: (100,  34,   None, None),
    67: (101,  None, None, 47  ),
    68: (103,  None, 23,   None),
    69: (104,  None, None, None),
    70: (105,  35,   None, 48  ),
    71: (106,  None, None, None),
    72: (107,  None, None, None),
    73: (108,  None, 24,   49  ),
    74: (110,  36,   None, None),
    75: (111,  None, None, 50  ),
    76: (112,  None, None, None),
    77: (113,  None, 25,   None),
    78: (115,  None, None, None),
    80: (116,  37,   26,   51  ),
    116:(152,  57,   38,   76  ),
}

_LOOKUP_A5 = {}
for comp, vals in _dati_A5_genitore.items():
    cols = ['GAC', 'DAC', 'DAS', 'DAP']
    for i, col in enumerate(cols):
        if col not in _LOOKUP_A5:
            _LOOKUP_A5[col] = []
        v = vals[i]
        if v is not None:
            _LOOKUP_A5[col].append((v, comp))


# ---------------------------------------------------------------------------
# TABELLA PERCENTILI (standard: media=100, DS=15)
# ---------------------------------------------------------------------------
_PERCENTILI_COMPOSITI = {
    40: '<0.1', 41: '<0.1', 42: '<0.1', 43: '<0.1', 44: '<0.1',
    45: '<0.1', 46: '<0.1', 47: '<0.1', 48: '<0.1', 49: '<0.1',
    50: '<0.1', 51: 0.1,    52: 0.1,    53: 0.1,    54: 0.1,
    55: 0.1,   56: 0.2,    57: 0.2,    58: 0.3,    59: 0.3,
    60: 0.4,   61: 0.5,    62: 1,      63: 1,      64: 1,
    65: 1,     66: 1,      67: 1,      68: 2,      69: 2,
    70: 2,     71: 3,      72: 3,      73: 4,      74: 4,
    75: 5,     76: 5,      77: 6,      78: 7,      79: 8,
    80: 9,     81: 10,     82: 12,     83: 13,     84: 14,
    85: 16,    86: 18,     87: 19,     88: 21,     89: 23,
    90: 25,    91: 27,     92: 30,     93: 32,     94: 34,
    95: 37,    96: 39,     97: 42,     98: 45,     99: 47,
    100: 50,   101: 53,    102: 55,    103: 58,    104: 61,
    105: 63,   106: 66,    107: 68,    108: 70,    109: 73,
    110: 75,   111: 77,    112: 79,    113: 81,    114: 82,
    115: 84,   116: 86,    117: 87,    118: 88,    119: 90,
    120: '>90',
}


# ---------------------------------------------------------------------------
# FUNZIONE PRINCIPALE
# ---------------------------------------------------------------------------

def calcola_abas(punteggi_grezzi, scheda, eta, con_lavoro=True):
    """
    Calcola i punteggi compositi ABAS-II.

    Parametri:
    punteggi_grezzi: dict con chiavi:
        'Co'  = Comunicazione
        'Am'  = Uso dell'ambiente
        'Sco' = Competenze scolastiche (genitore/adulto) o 'VS' = Vita a scuola (insegnante)
        'VC'  = Vita a casa (genitore/adulto)
        'SS'  = Salute e sicurezza
        'TL'  = Gioco/Tempo libero
        'Cur' = Cura di sé
        'Ac'  = Autocontrollo
        'Soc' = Socializzazione
        'Lav' = Lavoro (solo adulti, opzionale)
    scheda:    'adulto_auto' | 'adulto_etero' | 'insegnante' | 'genitore'
    eta:       età in anni (intero)
    con_lavoro: True/False — include la sottoscala Lavoro nel calcolo (solo adulti)

    Restituisce dict con:
        'punteggi_ponderati': {Co, Am, Sco/VS, VC, SS, TL, Cur, Ac, Soc, Lav}
        'somme_domini':       {DAC, DAS, DAP_senza, DAP_con, GAC_senza, GAC_con}
        'compositi':          {GAC, DAC, DAS, DAP}
        'percentili':         {GAC, DAC, DAS, DAP}
        'errore':             None oppure stringa descrittiva
    """

    # --- Selezione fascia d'età e tabelle ---
    if scheda in ('adulto_auto', 'adulto_etero'):
        if 16 <= eta <= 21:
            fascia = '16_21'
        elif 22 <= eta <= 29:
            fascia = '22_29'
        elif 30 <= eta <= 39:
            fascia = '30_39'
        elif 40 <= eta <= 49:
            fascia = '40_49'
        elif 50 <= eta <= 64:
            fascia = '50_64'
        elif 65 <= eta <= 74:
            fascia = '65_74'
        else:
            return {'errore': f'Età {eta} fuori dalle fasce supportate (16-74) per scheda {scheda}.'}

        tab_grezzi  = _TABELLE_A9[fascia] if scheda == 'adulto_auto' else _TABELLE_A12[fascia]
        lookup_comp = _LOOKUP_A10[fascia] if scheda == 'adulto_auto' else _LOOKUP_A13[fascia]
        subscale_vc = 'VC'

    elif scheda == 'insegnante':
        if not (17 <= eta <= 21):
            return {'errore': f'Età {eta} fuori dalla fascia supportata (17-21) per scheda insegnante.'}
        fascia = '17_21'
        tab_grezzi  = _A1_17_21
        lookup_comp = {col: sorted(lst) for col, lst in _LOOKUP_A2.items()}
        subscale_vc = 'VS'

    elif scheda == 'genitore':
        if not (17 <= eta <= 21):
            return {'errore': f'Età {eta} fuori dalla fascia supportata (17-21) per scheda genitore.'}
        fascia = '17_21'
        tab_grezzi  = _A5_17_21
        lookup_comp = {col: sorted(lst) for col, lst in _LOOKUP_A5.items()}
        subscale_vc = 'VC'

    else:
        return {'errore': f'Scheda "{scheda}" non riconosciuta.'}

    # --- Conversione grezzi → ponderati ---
    ponderati = {}
    chiave_vc = 'VS' if subscale_vc == 'VS' else 'VC'

    subs_richieste = ['Co', 'Am', 'Sco', chiave_vc, 'SS', 'TL', 'Cur', 'Ac', 'Soc']
    if scheda in ('adulto_auto', 'adulto_etero'):
        subs_richieste.append('Lav')

    for sub in subs_richieste:
        raw = punteggi_grezzi.get(sub)
        if raw is None:
            ponderati[sub] = None
            continue
        tab = tab_grezzi.get(sub, [])
        if tab:
            ponderati[sub] = _pp_da_grezzo(int(raw), tab)
        else:
            ponderati[sub] = None

    # --- Calcolo somme domini ---
    def _somma(*subs):
        vals = [ponderati.get(s) for s in subs]
        if any(v is None for v in vals):
            return None
        return sum(vals)

    # DAC: Co + Sco + Ac
    sco_key = 'Sco'
    dac = _somma('Co', sco_key, 'Ac')

    # DAS: TL + Soc
    das = _somma('TL', 'Soc')

    # DAP senza Lavoro: Am + VC/VS + SS + Cur
    dap_s = _somma('Am', chiave_vc, 'SS', 'Cur')

    # DAP con Lavoro: Am + VC/VS + SS + Cur + Lav
    lav_pp = ponderati.get('Lav')
    dap_c = (dap_s + lav_pp) if (dap_s is not None and lav_pp is not None) else None

    gac_s = (dac + das + dap_s) if None not in (dac, das, dap_s) else None
    gac_c = (dac + das + dap_c) if None not in (dac, das, dap_c) else None

    somme = {
        'DAC':      dac,
        'DAS':      das,
        'DAP_senza':dap_s,
        'DAP_con':  dap_c,
        'GAC_senza':gac_s,
        'GAC_con':  gac_c,
    }

    # --- Conversione somme → compositi ---
    def _comp(col, somma):
        if somma is None:
            return None
        tab = lookup_comp.get(col, [])
        if not tab:
            return None
        return _composito_da_somma(somma, tab)

    if scheda in ('adulto_auto', 'adulto_etero'):
        gac_col = 'GAC_c' if con_lavoro else 'GAC_s'
        dap_col = 'DAP_c' if con_lavoro else 'DAP_s'
        gac_somma = gac_c if con_lavoro else gac_s
        dap_somma = dap_c if con_lavoro else dap_s
    else:
        gac_col   = 'GAC'
        dap_col   = 'DAP'
        gac_somma = gac_s
        dap_somma = dap_s

    compositi = {
        'GAC': _comp(gac_col, gac_somma),
        'DAC': _comp('DAC',   dac),
        'DAS': _comp('DAS',   das),
        'DAP': _comp(dap_col, dap_somma),
    }

    percentili = {
        k: _PERCENTILI_COMPOSITI.get(v, None) if v is not None else None
        for k, v in compositi.items()
    }

    return {
        'punteggi_ponderati': ponderati,
        'somme_domini':       somme,
        'compositi':          compositi,
        'percentili':         percentili,
        'errore':             None,
    }


# ============================================================================
# SEZIONE DI TEST - Verifica che tutte le funzioni funzionino correttamente
# ============================================================================

if __name__ == "__main__":
    print("Ambiente di sviluppo pronto per webapp_autismo.\n")
    
    # Test RAADS-R
    print("--- Test RAADS-R ---")
    risposte_raads = [2] * 80  # Valori di test
    risultato_raads = calcola_raads_r(risposte_raads)
    print(f"Punteggio: {risultato_raads['punteggio_totale']}")
    print(f"Interpretazione: {risultato_raads['interpretazione']}\n")
    
    # Test AQ
    print("--- Test AQ ---")
    risposte_aq = [2] * 50  # Valori di test
    risultato_aq = calcola_aq(risposte_aq)
    print(f"Punteggio: {risultato_aq['punteggio_totale']}")
    print(f"Interpretazione: {risultato_aq['interpretazione']}\n")
    
    # Test EQ
    print("--- Test EQ ---")
    risposte_eq = [2] * 40  # Valori di test
    risultato_eq = calcola_eq(risposte_eq)
    print(f"Punteggio: {risultato_eq['punteggio_totale']}")
    print(f"Interpretazione: {risultato_eq['interpretazione']}\n")
    
    # Test ISI
    print("--- Test ISI ---")
    risposte_isi = [2] * 7  # Valori di test
    risultato_isi = calcola_isi(risposte_isi)
    print(f"Punteggio: {risultato_isi['punteggio_totale']}")
    print(f"Interpretazione: {risultato_isi['interpretazione']}\n")
    
    # Test TAS-20
    print("--- Test TAS-20 ---")
    risposte_tas20 = [3] * 20  # Valori di test
    risultato_tas20 = calcola_tas20(risposte_tas20)
    print(f"Punteggio: {risultato_tas20['punteggio_totale']}")
    print(f"Interpretazione: {risultato_tas20['interpretazione']}\n")
    
    # Test STAI-Y-1
    print("--- Test STAI-Y-1 ---")
    risposte_stai_y1 = [2] * 20  # Valori di test
    risultato_stai_y1 = calcola_stai_y1(risposte_stai_y1)
    print(f"Punteggio: {risultato_stai_y1['punteggio_totale']}")
    print(f"Interpretazione: {risultato_stai_y1['interpretazione']}\n")
    
    # Test STAI-Y-2
    print("--- Test STAI-Y-2 ---")
    risposte_stai_y2 = [2] * 20  # Valori di test
    risultato_stai_y2 = calcola_stai_y2(risposte_stai_y2)
    print(f"Punteggio: {risultato_stai_y2['punteggio_totale']}")
    print(f"Interpretazione: {risultato_stai_y2['interpretazione']}\n")
    
    # Test GSRS
    print("--- Test GSRS ---")
    risposte_gsrs = [4] * 15  # Valori di test
    risultato_gsrs = calcola_gsrs(risposte_gsrs)
    print(f"Punteggio: {risultato_gsrs['punteggio_totale']}")
    print(f"Sottoscale: {risultato_gsrs['sottoscale']}")
    print(f"Interpretazione: {risultato_gsrs['interpretazione']}\n")
    
    # Test ASI
    print("--- Test ASI ---")
    risposte_asi = [1] * 29  # Valori di test
    risultato_asi = calcola_asi(risposte_asi)
    print(f"Punteggio: {risultato_asi['punteggio_totale']}")
    print(f"Interpretazione: {risultato_asi['interpretazione']}\n")
    
    # Test OCI-R
    print("--- Test OCI-R ---")
    risposte_ocir = [2] * 18  # Valori di test
    risultato_ocir = calcola_ocir(risposte_ocir)
    print(f"Punteggio: {risultato_ocir['punteggio_totale']}")
    print(f"Sottoscale: {risultato_ocir['sottoscale']}")
    print(f"Interpretazione: {risultato_ocir['interpretazione']}\n")
    
    # Test ASQ
    print("--- Test ASQ ---")
    risposte_asq = [3] * 40  # Valori di test
    risultato_asq = calcola_asq(risposte_asq)
    print(f"Scale: {risultato_asq['scale']}")
    print(f"Fattori latenti: {risultato_asq['fattori_latenti']}")
    print(f"Tipo di attaccamento: {risultato_asq['tipo_attaccamento']}\n")
    
    print("=" * 80)
    print("TUTTI I TEST SONO PRONTI!")
    print("=" * 80)
