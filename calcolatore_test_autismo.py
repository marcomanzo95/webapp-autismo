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


def calcola_asq(risposte):
    """
    Calcola il punteggio dell'ASQ (Attachment Style Questionnaire)
    
    Parametri:
    risposte: lista di 40 valori (1-6)
    
    Scale principali:
    1. Fiducia (Trust): item 1, 2, 3, 19, 20, 31, 37, 38 (0-indexed: 0, 1, 2, 18, 19, 30, 36, 37)
    2. Disagio per l'intimità: item 5, 14, 16, 17, 21, 23, 25, 26, 34, 36 (0-indexed: 4, 13, 15, 16, 20, 22, 24, 25, 33, 35)
    3. Secondarietà delle relazioni: item 4, 6, 7, 8, 9, 10, 34, 36 (0-indexed: 3, 5, 6, 7, 8, 9, 33, 35)
    4. Bisogno di approvazione: item 11, 12, 13, 15, 24, 27, 35 (0-indexed: 10, 11, 12, 14, 23, 26, 34)
    5. Preoccupazione per le relazioni: item 18, 22, 28, 29, 30, 32, 33, 39, 40 (0-indexed: 17, 21, 27, 28, 29, 31, 32, 38, 39)
    """
    # Scale principali
    fiducia = risposte[0] + risposte[1] + risposte[2] + risposte[18] + risposte[19] + risposte[30] + risposte[36] + risposte[37]
    disagio_intimita = risposte[4] + risposte[13] + risposte[15] + risposte[16] + risposte[20] + risposte[22] + risposte[24] + risposte[25] + risposte[33] + risposte[35]
    secondarieta = risposte[3] + risposte[5] + risposte[6] + risposte[7] + risposte[8] + risposte[9] + risposte[33] + risposte[35]
    bisogno_approvazione = risposte[10] + risposte[11] + risposte[12] + risposte[14] + risposte[23] + risposte[26] + risposte[34]
    preoccupazione = risposte[17] + risposte[21] + risposte[27] + risposte[28] + risposte[29] + risposte[31] + risposte[32] + risposte[38] + risposte[39]
    
    # Fattori latenti di secondo ordine
    # Attaccamento Evitante = Disagio + Secondarietà - Fiducia (negativo)
    # Attaccamento Ansioso = Bisogno approvazione + Preoccupazione - Fiducia (negativo)
    
    evitamento = disagio_intimita + secondarieta - fiducia
    ansia = bisogno_approvazione + preoccupazione - fiducia
    
    # Normalizza i fattori per interpretazione
    evitamento_normalizzato = evitamento / 100  # Normalizzazione approssimativa
    ansia_normalizzata = ansia / 100  # Normalizzazione approssimativa
    
    # Determina il tipo di attaccamento
    if ansia_normalizzata < 0.5 and evitamento_normalizzato < 0.5:
        tipo_attaccamento = "SICURO"
    elif ansia_normalizzata >= 0.5 and evitamento_normalizzato < 0.5:
        tipo_attaccamento = "PREOCCUPATO"
    elif ansia_normalizzata < 0.5 and evitamento_normalizzato >= 0.5:
        tipo_attaccamento = "DISTANZIANTE"
    else:
        tipo_attaccamento = "TIMOROSO"
    
    return {
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
        'tipo_attaccamento': tipo_attaccamento,
        'interpretazione': f"Stile di attaccamento: {tipo_attaccamento}"
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

