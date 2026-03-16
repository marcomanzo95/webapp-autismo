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
    'raads_r': {
        'nome': 'RAADS-R',
        'descrizione': 'Ritvo Autism Asperger Diagnostic Scale-Revised - versione italiana',
        'istruzioni': 'Segna una sola casella per ogni riga. Le risposte possibili sono: Vero ora e quando ero giovane; Vero solo ora; Vero solo quando ero giovane (<16 anni); Mai vero.',
    
        'item_count': 80,
    
        # Mappatura pratica coerente con la tua funzione calcola_raads_r,
        # che lavora su valori 0-3.
        'scale_options': [
            {'value': 3, 'label': 'Vero ora e quando ero giovane'},
            {'value': 2, 'label': 'Vero solo ora'},
            {'value': 1, 'label': 'Vero solo quando ero giovane (<16 anni)'},
            {'value': 0, 'label': 'Mai vero'}
        ],
    
        'campi_preliminari': [
            {
                'name': 'stato_civile_raads',
                'label': 'Stato civile',
                'type': 'radio',
                'options': ['Single', 'Sposato', 'Divorziato', 'Impegnato']
            },
            {
                'name': 'hai_figli',
                'label': 'Hai figli?',
                'type': 'radio',
                'options': ['Si', 'No']
            },
            {
                'name': 'figli_specifica',
                'label': "Se sì, specifica sesso, età, presenza di qualsiasi condizione psichiatrica o neurologica incluse l'autismo e la Sindrome di Asperger",
                'type': 'textarea'
            },
            {
                'name': 'patente_guida',
                'label': 'Hai mai avuto la patente di guida?',
                'type': 'radio',
                'options': ['Si', 'No']
            },
    
            {
                'name': 'istruzione_raads',
                'label': 'Qual è il grado di istruzione più alto di cui sei in possesso?',
                'type': 'radio',
                'options': [
                    'Licenza elementare',
                    'Licenza media',
                    'Diploma di scuola superiore',
                    'Diploma di Laurea (triennale)',
                    'Diploma di Laurea (specialistica)',
                    'Master post Laurea',
                    'Specializzazione post-laurea',
                    'Dottorato di Ricerca'
                ]
            },
            {
                'name': 'sostegno_scuola',
                'label': 'A scuola avevi il sostegno?',
                'type': 'radio',
                'options': ['Si', 'No']
            },
            {
                'name': 'misure_compensative',
                'label': 'A scuola avevi misure compensative o dispensative?',
                'type': 'radio',
                'options': ['Si', 'No']
            },
    
            {
                'name': 'diagnosi_pregressa_presenza',
                'label': "Sei mai stato diagnosticato con Disturbo dello Spettro Autistico, Autismo, Sindrome di Asperger, Autismo ad alto funzionamento, Disturbo pervasivo dello sviluppo, Disturbo generalizzato dello sviluppo, Dislessia, Disgrafia, Discalculia, Disortografia, Disprassia, ritardo del linguaggio, disturbo specifico del linguaggio, ritardo mentale, disturbo specifico dell'apprendimento, deficit d'attenzione, iperattività, disturbo ossessivo compulsivo, anoressia, disturbi della condotta alimentare, disturbo della sfera affettiva, disturbo della relazione, epilessia o qualsiasi altra diagnosi psichiatrica, psicologica o neurologica?",
                'type': 'radio',
                'options': ['Si', 'No']
            },
            {'name': 'diagnosi_pregressa', 'label': 'Diagnosi', 'type': 'text'},
            {'name': 'chi_ha_fatto_diagnosi', 'label': "Nome del dottore, clinica o altro", 'type': 'text'},
            {'name': 'data_diagnosi', 'label': 'Data della diagnosi', 'type': 'text'},
    
            {
                'name': 'prima_parola',
                'label': 'A che età hai iniziato a parlare? Prima parola',
                'type': 'radio',
                'options': ['Prima dei 12 mesi', 'Prima dei 2 anni', 'Prima dei 3 anni', 'Prima dei 4 anni']
            },
            {
                'name': 'prima_frase',
                'label': 'A che età hai iniziato a parlare? Prima frase',
                'type': 'radio',
                'options': ['Prima dei 12 mesi', 'Prima dei 2 anni', 'Prima dei 3 anni', 'Prima dei 4 anni']
            }
        ],
    
        'domande': [
            "Sono una persona amichevole: gradevole, gioviale, affettuosa con gli altri.",
            "Uso spesso parole o frasi tratte da film e televisione durante le conversazioni.",
            "Sono spesso sorpreso quando gli altri mi dicono che sono stato insensibile o maleducato.",
            "A volte parlo a voce troppo alta o troppo bassa e non me ne accorgo.",
            "Spesso non so come comportarmi nelle situazioni sociali.",
            "Sono capace a mettermi 'nei panni degli altri'.",
            "A volte ho difficoltà a capire cosa significano frasi come: 'sei la luce dei miei occhi'.",
            "Mi piace parlare solo con le persone che condividono i miei interessi speciali.",
            "Mi focalizzo sui dettagli invece che sull'idea generale.",
            "Noto sempre la sensazione fisica che mi dà il cibo in bocca. Questo per me è più importante che il sapore.",
            "Mi mancano i miei migliori amici o la famiglia quando siamo distanti per lungo tempo.",
            "A volte offendo gli altri dicendo quello che penso, anche se non ne ho intenzione.",
            "Mi piace pensare e parlare solo di quelle poche cose che mi interessano.",
            "Se devo andare a mangiare al ristorante, preferisco andarci da solo piuttosto che con qualcuno che conosco.",
            "Non saprei immaginare come sarebbe essere qualcun altro.",
            "Mi è stato detto che sono goffo o scoordinato.",
            "Gli altri mi considerano strano e diverso.",
            "Capisco quando gli amici hanno bisogno di conforto.",
            "Sono ipersensibile alla sensazione tattile causata dai vestiti sulla mia pelle. Come li sento addosso è più importante di come appaiono esteriormente.",
            "Preferisco copiare il modo in cui certe persone parlano o si comportano. Mi aiuta a sembrare più normale.",
            "Posso provare una forte ansia se devo parlare con più di una persona contemporaneamente.",
            "Devo 'agire come una persona normale' per accontentare gli altri e farmi accettare.",
            "Di solito per me è facile conoscere nuove persone.",
            "Mi confonde (perdo il filo del discorso) quando qualcuno mi interrompe mentre sto parlando di qualcosa per me molto interessante.",
            "È difficile per me capire cosa provano le altre persone mentre stiamo parlando.",
            "Mi piace avere una conversazione con molte persone contemporaneamente, ad esempio a pranzo, a scuola o a lavoro.",
            "Prendo le cose troppo letteralmente, quindi spesso non colgo cosa le persone intendono dire.",
            "Per me è molto difficile capire il motivo per cui una persona è imbarazzata o gelosa.",
            "Alcuni tessuti comuni che non danno fastidio agli altri, mi procurano molto fastidio quando toccano la mia pelle.",
            "Mi agito molto quando sono obbligato a cambiare improvvisamente il modo abituale con cui faccio le cose.",
            "Non ho mai voluto avere o ho sentito il bisogno di una relazione che le altre persone chiamano 'intima'.",
            "Per me è difficile sia iniziare che terminare una conversazione. Sento il bisogno di proseguire finché non ho finito.",
            "Parlo con un ritmo di voce normale.",
            "Lo stesso suono, colore o tessuto può passare improvvisamente dal provocarmi forti reazioni fisiche o emotive all'essermi indifferente (e viceversa).",
            "La frase 'ti sento dentro' mi provoca una sensazione di disagio.",
            "A volte il suono di una parola o un rumore acuto possono essere dolorosi per le mie orecchie.",
            "Sono disponibile a comprendere le ragioni degli altri.",
            "Non mi immedesimo emotivamente con i protagonisti dei film e non riesco a provare ciò che loro provano.",
            "Non so capire quando qualcuno sta flirtando con me.",
            "Sono in grado di visualizzare nei minimi dettagli ciò che mi interessa.",
            "Tengo liste di cose che mi interessano, anche se non hanno un uso pratico (es. statistiche sportive, calendari, fatti storici, date, etc.).",
            "Troppi stimoli sensoriali mi sovraccaricano e mi sento schiacciato. Per stare meglio ho bisogno di isolarmi.",
            "Mi piace discutere di diversi argomenti con i miei amici.",
            "Non sono in grado di capire se qualcuno è interessato o annoiato da quello di cui sto parlando.",
            "Mi risulta molto difficile interpretare le espressioni del viso e il linguaggio del corpo delle persone con cui sto parlando.",
            "Le stesse cose (come i vestiti o la temperatura) possono darmi sensazioni molto diverse in momenti differenti.",
            "Mi trovo molto a mio agio durante un appuntamento o nelle situazioni sociali.",
            "Quando le persone mi parlano dei loro problemi, cerco di aiutarle al meglio delle mie possibilità.",
            "Mi è stato detto che ho una voce strana (ad esempio piatta, monotona, infantile, acuta, etc.).",
            "A volte un pensiero o un argomento mi si fissa nella mente a tal punto che non riesco a fare a meno di parlarne anche se nessuno sembra interessato.",
            "Tendo a fare in continuazione movimenti particolari con le mani (come sfarfallare, rigirare lacci o bastoncini, muoverle davanti ai miei occhi, etc.).",
            "Non sono mai stato interessato agli argomenti considerati interessanti dalla maggioranza delle persone.",
            "Sono considerata una persona compassionevole: se vedo qualcuno stare male provo anche io una sensazione di sofferenza e il desiderio di aiutarlo.",
            "Quando sto insieme agli altri seguo un insieme specifico di regole che mi aiutano a sembrare normale.",
            "Per me è molto difficile lavorare e sentirmi a mio agio in un gruppo.",
            "Quando parlo con qualcuno, è difficile cambiare l'argomento della conversazione. Quando lo fa la persona con cui sto parlando posso diventare molto agitato e confuso.",
            "A volte ho bisogno di coprirmi le orecchie per bloccare rumori fastidiosi (come aspirapolveri o persone che parlano troppo o sono troppo rumorose).",
            "Sono in grado di parlare facilmente con le persone e fare chiacchiere di cortesia.",
            "A volte non provo dolore per cose che lo provocano negli altri (per esempio quando mi faccio male da solo o mi brucio una mano su una pentola bollente).",
            "Quando parlo con qualcuno, trovo molto difficile capire quando è il mio turno di parlare e quando quello di ascoltare.",
            "Chi mi conosce bene mi considera un solitario.",
            "Solitamente parlo con un tono di voce normale.",
            "Mi piace che le cose siano esattamente le stesse, giorno dopo giorno, anche piccoli cambiamenti nelle mie routine mi agitano.",
            "Per me è un mistero come fare amici e socializzare.",
            "Mi calma girare su me stesso o dondolarmi su una sedia quando sono stressato.",
            "La frase 'gli ha parlato con il cuore in mano' non ha senso per me.",
            "Se sono in un ambiente in cui ci sono molti odori, sensazioni tattili, rumori e luci brillanti, mi sento ansioso o spaventato.",
            "Sono in grado di capire quando qualcuno intende comunicare una cosa diversa da quella che dice a parole.",
            "Mi piace stare per conto mio più tempo possibile.",
            "I miei penseri sono conservati nella memoria come fossero schede di un archivio, quando devo prendere quelli che mi interessano cerco all'interno dello schedario per trovare quello giusto (o qualsiasi altro modo unico di pensare).",
            "Lo stesso suono sembra a volte molto rumoroso e altre volte molto leggero anche se sono consapevole che non è cambiato.",
            "Mi piace trascorrere il mio tempo mangiando e parlando con familiari ed amici.",
            "Non riesco a tollerare le cose che non mi piacciono (come odori, tessuti, suoni o colori).",
            "Non mi piace essere abbracciato o ricevere altre manifestazioni fisiche di affetto.",
            "Quando devo andare da qualche parte ho bisogno di seguire una strada familiare, altrimenti posso sentirmi molto confuso ed agitato.",
            "È difficile immaginare ciò che gli altri si aspettano da me.",
            "Mi piace avere amici intimi.",
            "Le persone mi dicono che fornisco spesso troppi dettagli.",
            "Mi dicono spesso che faccio domande imbarazzanti.",
            "Tendo a puntualizzare gli errori degli altri."
        ]
    },
    # Dizionario per il test AQ (Autism‑Spectrum Quotient)
    'aq': {
        'nome': 'AQ (Autism‑Spectrum Quotient)',
        'descrizione': 'Questionario autosomministrato che misura i tratti autistici negli adulti',
        'item_count': 50,
        # Ogni opzione ha un valore (1–4) coerente con lo scoring: 1=totale d’accordo, 4=totale in disaccordo
        'scale_options': [
            {'value': 1, 'label': 'Totalmente d’accordo'},
            {'value': 2, 'label': 'Parzialmente d’accordo'},
            {'value': 3, 'label': 'Parzialmente in disaccordo'},
            {'value': 4, 'label': 'Totalmente in disaccordo'}
        ],
        'domande': [
            'Preferisco fare le cose in compagnia anziché da solo.',
            'Preferisco fare le cose sempre allo stesso modo.',
            'Se tento di immaginare qualcosa, trovo molto facile creare un’immagine nella mia mente.',
            'Mi capita spesso di essere tanto assorbito da qualcosa da perdere di vista le altre cose.',
            'Spesso avverto suoni deboli di cui gli altri non si accorgono.',
            'Abitualmente presto attenzione ai numeri delle targhe delle auto o a particolari del genere.',
            'Frequentemente le altre persone mi dicono che quello che ho detto è scortese, mentre invece io penso che sia corretto.',
            'Quando leggo una storia, posso facilmente immaginare l’aspetto dei personaggi.',
            'Sono affascinato dalle date.',
            'Nelle occasioni sociali riesco facilmente a seguire le conversazioni di diverse persone.',
            'Nelle situazioni sociali mi sento a mio agio.',
            'Tendo a notare dettagli che gli altri non notano.',
            'Preferisco recarmi in biblioteca piuttosto che ad un party.',
            'Riesco facilmente ad inventare delle storie.',
            'Trovo che mi attirano molto più le persone che le cose.',
            'Tendo ad avere interessi molto forti, e mi disturba fortemente se non posso perseguirli.',
            'Mi piace partecipare alla conversazione.',
            'Quando parlo io, per gli altri non è sempre facile inserirsi nella conversazione.',
            'Sono affascinato dai numeri.',
            'Quando sto leggendo una storia, mi riesce difficile capire le intenzioni dei personaggi.',
            'Non amo particolarmente leggere narrativa.',
            'Mi è difficile farmi dei nuovi amici.',
            'Noto continuamente schemi nelle cose.',
            'Vado più volentieri a teatro che in un museo.',
            'Non mi disturba se viene alterata la mia routine giornaliera.',
            'Mi capita frequentemente di non saper come continuare una conversazione.',
            'Quando qualcuno sta parlando con me, trovo facile leggere tra le righe.',
            'Di solito io mi concentro più sull’immagine intera che sui piccoli dettagli.',
            'Non sono molto bravo a ricordarmi i numeri telefonici.',
            'Di solito non noto i piccoli cambiamenti in una situazione o nell’aspetto di una persona.',
            'So distinguere se qualcuno che mi ascolta si sta annoiando.',
            'Riesco facilmente a fare più di una cosa allo stesso tempo.',
            'Quando sono al telefono non sono sicuro di quando tocca a me parlare.',
            'Mi piace fare le cose spontaneamente.',
            'Spesso sono l’ultimo ad afferrare il senso di una battuta.',
            'Riesco facilmente a intuire quello che una persona pensa o prova solo guardandola in faccia.',
            'Se mi interrompono mentre sono impegnato a fare qualcosa, riesco a riprendere molto rapidamente.',
            'Riesco bene nella conversazione sociale.',
            'Spesso la gente mi dice che io insisto sempre sullo stesso argomento.',
            'Quando ero piccolo mi piaceva giocare con altri bambini a “far finta di…”.',
            'Mi piace raccogliere informazioni su categorie di cose (ad esempio tipi di auto, uccelli, treni, piante).',
            'Mi è difficile immaginare come sarebbe la mia vita se io fossi un’altra persona.',
            'Mi piace pianificare attentamente tutte le attività alle quali io partecipo.',
            'Amo le occasioni sociali.',
            'Mi è difficile comprendere le intenzioni della gente.',
            'Le situazioni nuove mi rendono ansioso.',
            'Mi piace incontrare nuove persone.',
            'Sono un buon diplomatico.',
            'Non sono molto bravo a ricordarmi la data di nascita delle persone.',
            'Per me è molto facile giocare coi bambini a “far finta di…”.'
        ]
    },
    'eq': {
        'nome': 'EQ (Empathy Quotient)',
        'descrizione': 'Questionario autosomministrato per la valutazione dell’empatia negli adulti',
        'istruzioni': 'A seguire sono riportate una lista di affermazioni. Leggi ciascuna affermazione molto attentamente e indica quanto fortemente sei in accordo o in disaccordo con esse, cerchiando la tua risposta. Non ci sono risposte giuste o sbagliate.',
        'item_count': 40,
    
        'scale_options': [
            {'value': 1, 'label': 'Assolutamente d’accordo'},
            {'value': 2, 'label': 'Parzialmente d’accordo'},
            {'value': 3, 'label': 'Parzialmente in disaccordo'},
            {'value': 4, 'label': 'Assolutamente in disaccordo'}
        ],
    
        'domande': [
    
            "Capisco con facilità se qualcuno vuole partecipare ad una conversazione.",
            "Trovo difficile spiegare agli altri concetti che io comprendo facilmente, quando loro non capiscono alla prima spiegazione.",
            "Prendermi cura degli altri è qualcosa che mi fa veramente piacere.",
            "Trovo difficile capire come comportarmi in una situazione sociale.",
            "Le persone spesso mi dicono che insisto troppo sul mio punto di vista in una discussione.",
            "Non mi preoccupa più di tanto essere in ritardo ad un appuntamento con un amico.",
            "Le amicizie e le relazioni sociali sono troppo difficili per me, così tendo a non occuparmene.",
            "Spesso trovo difficile giudicare se qualcosa è sgarbato o cortese.",
            "In una conversazione tendo a focalizzarmi sulle mie idee piuttosto che su cosa potrebbe stare pensando il mio interlocutore.",
            "Quando ero bambino/a mi divertivo a sezionare i vermi per vedere cosa succedeva.",
            "Riesco facilmente a capire se qualcuno dice una cosa ma ne intende un’altra.",
            "Non capisco perché la gente si offende tanto per certe cose.",
            "Riesco facilmente a mettermi nei panni degli altri.",
            "Sono bravo/a a predire i sentimenti degli altri.",
            "Mi accorgo subito se qualcuno in un gruppo è a disagio o imbarazzato.",
            "Se ciò che dico offende qualcuno, penso che questo sia un suo problema, non mio.",
            "Se qualcuno mi chiede un parere sul suo nuovo taglio di capelli, rispondo sinceramente anche se non mi piace.",
            "Non riesco sempre a capire perché qualcuno possa essersi sentito offeso da un commento.",
            "Vedere qualcuno piangere non mi turba più di tanto.",
            "Sono molto diretto e questo viene spesso interpretato come scortesia, anche se non è mia intenzione.",
            "Non ho la tendenza a sentirmi confuso nelle situazioni sociali.",
            "Le persone mi dicono che sono bravo/a a comprendere cosa stanno provando o cosa stanno pensando.",
            "Quando parlo con le persone tendo a discutere più delle loro esperienze che delle mie.",
            "Mi turba vedere soffrire un animale.",
            "Riesco a prendere le decisioni senza lasciarmi influenzare dalle opinioni degli altri.",
            "Riesco facilmente a capire se il mio interlocutore è interessato o annoiato da ciò che dico.",
            "Mi turbano le immagini di gente che soffre quando guardo le notizie in TV.",
            "Gli amici spesso mi parlano dei loro problemi perché si sentono capiti.",
            "Riesco a percepire se la mia presenza è indesiderata, anche se non mi viene detto espressamente.",
            "Talvolta le persone mi dicono che ho esagerato nel prendere in giro.",
            "La gente mi dice spesso che sono insensibile sebbene io non sempre ne capisca il perché.",
            "Se vedo una persona nuova in un gruppo, penso che stia a lui fare uno sforzo per inserirsi.",
            "Solitamente rimango emotivamente distaccato quando guardo un film.",
            "Riesco ad entrare in sintonia con ciò che qualcun altro sta provando in modo rapido e intuitivo.",
            "Riesco facilmente ad intuire di cosa il mio interlocutore desidera parlare.",
            "Capisco se qualcuno sta celando le sue vere emozioni.",
            "Nelle situazioni sociali ho difficoltà a decifrare le regole in modo consapevole.",
            "Sono bravo/a a prevedere ciò che una persona farà.",
            "Tendo a farmi coinvolgere emotivamente dai problemi degli amici.",
            "Di solito tengo in considerazione il punto di vista degli altri anche se non lo condivido."
    
        ]
    },
    'isi': {
        'nome': 'ISI (Insomnia Severity Index)',
        'item_count': 5,
        'scale_type': 'custom',  # Scala personalizzata per ogni domanda
        'domande': [
            {
                'numero': '1a',
                'testo': 'Difficoltà ad addormentarsi',
                'scale_labels': ['No', 'Lieve', 'Media', 'Grave', 'Molto grave']
            },
            {
                'numero': '1b',
                'testo': 'Difficoltà a restare addormentato',
                'scale_labels': ['No', 'Lieve', 'Media', 'Grave', 'Molto grave']
            },
            {
                'numero': '1c',
                'testo': 'Risveglio troppo precoce',
                'scale_labels': ['No', 'Lieve', 'Media', 'Grave', 'Molto grave']
            },
            {
                'numero': '2',
                'testo': 'Quanto si sente soddisfatto/insoddisfatto del suo attuale sonno?',
                'scale_labels': ['Molto soddisfatto', 'Soddisfatto', 'Neutro', 'Non molto soddisfatto', 'Molto insoddisfatto']
            },
            {
                'numero': '3',
                'testo': 'In quale misura ritiene che il problema di sonno interferisca con la sua efficienza diurna? (affaticamento diurno, capacità di svolgere lavoro/faccende di casa, concentrazione, memoria, umore, ecc.)',
                'scale_labels': ['Per nulla', 'Un po', 'Abbastanza', 'Molto', 'Moltissimo']
            },
            {
                'numero': '4',
                'testo': 'Quanto pensa che il suo problema di sonno sia evidente agli altri, in termini di peggioramento di qualità della sua vita?',
                'scale_labels': ['Per nulla', 'Un po', 'Abbastanza', 'Molto', 'Moltissimo']
            },
            {
                'numero': '5',
                'testo': 'Quanto si sente preoccupato/a – stressato/a a causa del suo attuale problema di sonno?',
                'scale_labels': ['Per nulla', 'Un po', 'Abbastanza', 'Molto', 'Moltissimo']
            }
        ]
    },
    'tas20': {
        'nome': 'TAS-20 (Toronto Alexithymia Scale)',
        'descrizione': 'Questionario autosomministrato per la valutazione dell’alessitimia',
        'item_count': 20,
        'scale_options': [
            {'value': 1, 'label': 'Non sono per niente d’accordo'},
            {'value': 2, 'label': 'Non sono molto d’accordo'},
            {'value': 3, 'label': 'Non sono né d’accordo né in disaccordo'},
            {'value': 4, 'label': 'Sono d’accordo in parte'},
            {'value': 5, 'label': 'Sono completamente d’accordo'}
        ],
        'domande': [
            'Sono spesso confuso/a circa le emozioni che provo',
            'Mi è difficile trovare le parole giuste per esprimere i miei sentimenti',
            'Provo delle sensazioni fisiche che neanche i medici capiscono',
            'Riesco facilmente a descrivere i miei sentimenti',
            'Preferisco approfondire i miei problemi piuttosto che descriverli semplicemente',
            'Quando sono sconvolto/a non so se sono triste, spaventato/a o arrabbiato/a',
            'Sono spesso disorientato dalle sensazioni che provo nel mio corpo',
            'Preferisco lasciare che le cose seguano il loro corso piuttosto che capire perché sono andate in quel modo',
            'Provo sentimenti che non riesco proprio ad identificare',
            'È essenziale conoscere le proprie emozioni',
            'Mi è difficile descrivere ciò che provo per gli altri',
            'Gli altri mi chiedono di parlare di più dei miei sentimenti',
            'Non capisco cosa stia accadendo dentro di me',
            'Spesso non so perché mi arrabbio',
            'Con le persone preferisco parlare di cose di tutti i giorni piuttosto che delle loro emozioni',
            'Preferisco vedere spettacoli leggeri, piuttosto che spettacoli a sfondo psicologico',
            'Mi è difficile rivelare i sentimenti più profondi anche ad amici più intimi',
            'Riesco a sentirmi vicino ad una persona, anche se ci capita di stare in silenzio',
            'Trovo che l’esame dei miei sentimenti mi serve a risolvere i miei problemi personali',
            'Cercare significati nascosti in films o commedie distoglie dal piacere dello spettacolo'
        ]
    },
    'stai_y1': {
        'nome': 'STAI-Y1 (State Anxiety)',
        'descrizione': 'Scala di valutazione dell’ansia di stato',
        'istruzioni': 'Legga ciascuna frase e indichi come si sente adesso, in questo momento.',
        'item_count': 20,
        
        'scale_options': [
            {'value': 1, 'label': 'Per nulla'},
            {'value': 2, 'label': 'Un po'},
            {'value': 3, 'label': 'Abbastanza'},
            {'value': 4, 'label': 'Moltissimo'}
        ],
    
        'domande': [
            "Mi sento calmo",
            "Mi sento sicuro",
            "Sono teso",
            "Ho dei rimpianti",
            "Mi sento tranquillo",
            "Mi sento turbato",
            "Sono attualmente preoccupato per possibili disgrazie",
            "Mi sento riposato",
            "Mi sento ansioso",
            "Mi sento a mio agio",
            "Mi sento sicuro di me",
            "Mi sento nervoso",
            "Sono agitato",
            "Mi sento molto teso",
            "Sono rilassato",
            "Mi sento contento",
            "Sono preoccupato",
            "Mi sento sovraccaricato e scosso",
            "Mi sento allegro",
            "Mi sento bene"
        ]
    },
    'stai_y2': {
        'nome': 'STAI-Y2 (Trait Anxiety)',
        'descrizione': 'Scala di valutazione dell’ansia di tratto',
        'istruzioni': 'Indichi come si sente generalmente.',
        'item_count': 20,
    
        'scale_options': [
            {'value': 1, 'label': 'Per nulla'},
            {'value': 2, 'label': 'Un po'},
            {'value': 3, 'label': 'Abbastanza'},
            {'value': 4, 'label': 'Moltissimo'}
        ],
    
        'domande': [
            "Mi sento bene",
            "Mi sento teso ed irrequieto",
            "Sono soddisfatto di me stesso",
            "Vorrei poter essere felice come sembrano gli altri",
            "Mi sento un fallito",
            "Mi sento riposato",
            "Io sono calmo, tranquillo e padrone di me",
            "Sento che le difficoltà si accumulano tanto da non poterle superare",
            "Mi preoccupo troppo di cose che in realtà non hanno importanza",
            "Sono felice",
            "Mi vengono pensieri negativi",
            "Manco di fiducia in me stesso",
            "Mi sento sicuro",
            "Prendo decisioni facilmente",
            "Mi sento inadeguato",
            "Sono contento",
            "Pensieri di scarsa importanza mi passano per la mente e mi infastidiscono",
            "Vivo le delusioni con tanta partecipazione da non poter togliermele dalla testa",
            "Sono una persona costante",
            "Divento teso e turbato quando penso alle mie attuali condizioni"
        ]
    },
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
    },
    'ocir': {
        'nome': 'OCI-R (Obsessive Compulsive Inventory-Revised)',
        'descrizione': 'Questionario autosomministrato per la valutazione dei sintomi ossessivo-compulsivi',
        'istruzioni': 'Nella colonna denominata DISAGIO contrassegni il numero che meglio descrive quanto quella particolare esperienza le ha causato disagio o fastidio nell’ultimo mese. Non ci sono risposte giuste o sbagliate.',
    
        'item_count': 18,
    
        'scale_options': [
            {'value': 0, 'label': 'Per nulla'},
            {'value': 1, 'label': 'Un poco'},
            {'value': 2, 'label': 'Abbastanza'},
            {'value': 3, 'label': 'Molto'},
            {'value': 4, 'label': 'Moltissimo'}
        ],
    
        'domande': [
    
            "Ho conservato talmente tante cose che ora sono intralciato da esse.",
            "Ho la tendenza a controllare e ricontrollare le cose molto più spesso del necessario.",
            "Mi irrito notevolmente se gli oggetti non sono sistemati al loro giusto posto.",
            "Mi sento costretto a ripetere dei numeri mentre sto facendo delle cose.",
            "Trovo difficile toccare un oggetto quando so che è stato toccato da estranei o da certe persone.",
            "Trovo difficile controllare i miei pensieri.",
            "Accumulo cose di cui non ho bisogno.",
            "Controllo ripetutamente porte, finestre e cassetti.",
            "Mi agito se gli altri cambiano il modo in cui ho sistemato le cose.",
            "Sento di dover ripetere certi numeri.",
            "Qualche volta devo lavarmi o pulirmi semplicemente perché mi sento contaminato.",
            "Sono turbato da pensieri spiacevoli che entrano nella mia mente contro la mia volontà.",
            "Evito di buttare via le cose perché temo che in futuro potrei averne bisogno.",
            "Controllo ripetutamente i rubinetti del gas, dell’acqua e gli interruttori della luce dopo averli chiusi/spenti.",
            "Ho bisogno che le cose attorno a me siano sistemate secondo un particolare ordine.",
            "Ho la sensazione che ci siano numeri buoni e numeri cattivi.",
            "Mi lavo le mani più spesso e più a lungo del necessario.",
            "Frequentemente ho pensieri sgradevoli e ho difficoltà a liberarmene."
    
        ]
    },
    'asq': {
        'nome': 'ASQ (Attachment Style Questionnaire)',
        'descrizione': 'Questionario autosomministrato per la valutazione dello stile di attaccamento adulto',
        'istruzioni': 'Indichi quanto concorda con ciascuna delle seguenti affermazioni, valutandole in base a questa scala: 1 = Totalmente in disaccordo; 2 = Fortemente in disaccordo; 3 = Lievemente in disaccordo; 4 = Lievemente d’accordo; 5 = Fortemente d’accordo; 6 = Totalmente d’accordo.',
        'item_count': 40,
    
        'scale_options': [
            {'value': 1, 'label': 'Totalmente in disaccordo'},
            {'value': 2, 'label': 'Fortemente in disaccordo'},
            {'value': 3, 'label': 'Lievemente in disaccordo'},
            {'value': 4, 'label': 'Lievemente d’accordo'},
            {'value': 5, 'label': 'Fortemente d’accordo'},
            {'value': 6, 'label': 'Totalmente d’accordo'}
        ],
    
        'domande': [
            "Nel complesso sono una persona valida",
            "E’ più facile arrivare a conoscere me che la maggior parte delle altre persone",
            "Sono fiducioso che gli altri ci saranno quando avrò bisogno di loro",
            "Preferisco dipendere da me stesso invece che dagli altri",
            "Preferisco stare sulle mie",
            "Chiedere aiuto equivale ad ammettere di essere un fallimento",
            "Il valore di una persona andrebbe valutato in base ai suoi successi",
            "Raggiungere degli obbiettivi è più importante che costruire delle relazioni",
            "Dare il massimo è più importante che andare d’accordo con gli altri",
            "Se hai un lavoro da fare, non dovrebbe importarti di chi ne avrà un danno",
            "Per me è importante piacere agli altri",
            "Per me è importante evitare di fare delle cose che agli altri non piacciono",
            "Trovo difficile prendere una decisione a meno che non sappia ciò che pensano gli altri",
            "Le mie relazioni con gli altri sono solitamente superficiali",
            "A volte penso di non valere nulla",
            "Ho difficoltà a fidarmi degli altri",
            "Ho difficoltà a dipendere dagli altri",
            "Trovo che gli altri siano riluttanti ad entrare in confidenza quanto io vorrei",
            "Trovo relativamente facile entrare in confidenza con gli altri",
            "Mi fido facilmente degli altri",
            "Mi trovo a mio agio nel dipendere dagli altri",
            "Mi preoccupo che agli altri non importerà di me quanto a me importa di loro",
            "Mi preoccupo quando la gente entra troppo in confidenza",
            "Mi preoccupo di non essere all’altezza degli altri",
            "Ho sentimenti contrastanti circa l’essere in confidenza con gli altri",
            "Se da un lato voglio entrare in confidenza con gli altri, dall’altro mi sento a disagio",
            "Mi chiedo perché la gente voglia avere a che fare con me",
            "Per me è veramente importante avere una relazione stretta",
            "Mi preoccupo molto delle mie relazioni",
            "Mi chiedo come me la caverei senza qualcuno che mi ami",
            "Mi sento fiducioso nelle relazioni con gli altri",
            "Spesso mi sento lasciato in disparte o solo",
            "Spesso mi preoccupo di non riuscire ad entrare in sintonia con gli altri",
            "Gli altri hanno i loro problemi, per cui non li infastidisco coi miei",
            "Quando discuto dei miei problemi con gli altri, di solito mi vergogno o mi sento stupido",
            "Sono troppo impegnato in altre attività per dedicare molto tempo alle relazioni",
            "Se qualcosa mi disturba, gli altri solitamente ne sono consapevoli e preoccupati",
            "Sono fiducioso di essere gradito e rispettato dagli altri",
            "Mi sento frustrato quando gli altri non sono disponibili nel momento in cui ne ho bisogno",
            "Gli altri spesso mancano alle mie aspettative"
        ]
    },
}

@app.route('/')
def index():
    # Deve essere QUESTIONARI (maiuscolo) dopo l'uguale!
    return render_template('index.html', questionari=QUESTIONARI)




@app.route('/questionario/<nome_test>')
def questionario(nome_test):
    if nome_test not in QUESTIONARI:
        return "Test non trovato", 404
    test_data = QUESTIONARI[nome_test]
    return render_template('questionario.html', test_name=nome_test, test_data=test_data)


@app.route('/api/invia_risultati', methods=['POST'])
def invia_risultati():
    """
    Riceve le risposte del test e invia i risultati via email al clinico
    """
    try:
        test_name = request.form.get('test_name')
        codice_paziente = request.form.get('codice_paziente')
        telefono = request.form.get('telefono')
        indirizzo = request.form.get('indirizzo')
        genere = request.form.get('genere')
        istruzione = request.form.get('istruzione')
        
        # Estrai le risposte dal form
        risposte = {}
        for key in request.form:
            if key.startswith('item_'):
                item_num = int(key.split('_')[1])
                risposte[item_num] = int(request.form.get(key))
        
        # Converti il dizionario in lista ordinata
        risposte_lista = [risposte.get(i, 0) for i in range(1, len(risposte) + 1)]
        
        # Calcola il punteggio in base al test
        if test_name == 'gsrs':
            risultato = calcola_gsrs(risposte_lista)
        elif test_name == 'isi':
            risultato = calcola_isi(risposte_lista)
        elif test_name == 'asi':
            risultato = calcola_asi(risposte_lista)
        elif test_name == 'aq':
            risultato = calcola_aq(risposte_lista)
        elif test_name == 'eq':
            risultato = calcola_eq(risposte_lista)
        elif test_name == 'tas20':
            risultato = calcola_tas20(risposte_lista)
        elif test_name == 'stai_y1':
            risultato = calcola_stai_y1(risposte_lista)
        elif test_name == 'stai_y2':
            risultato = calcola_stai_y2(risposte_lista)
        elif test_name == 'ocir':
            risultato = calcola_ocir(risposte_lista)
        elif test_name == 'asq':
            risultato = calcola_asq(risposte_lista, genere=genere)
        elif test_name == 'raads_r':
            risultato = calcola_raads_r(risposte_lista)
        else:
            return jsonify({'success': False, 'message': 'Test non riconosciuto'})
        
        # Prepara il messaggio email in HTML
        email_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h1>Risultati Test {QUESTIONARI[test_name]['nome']}</h1>
            <hr>
            
            <h2>Dati Paziente</h2>
            <p><strong>Codice Paziente:</strong> {codice_paziente}</p>
            <p><strong>Genere:</strong> {genere}</p>
            <p><strong>Istruzione:</strong> {istruzione}</p>
            <p><strong>Telefono:</strong> {telefono}</p>
            <p><strong>Indirizzo:</strong> {indirizzo}</p>
            <p><strong>Data:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            
            <h2>Risultati</h2>
            <p><strong>Punteggio:</strong> {risultato['punteggio']}/{risultato['max_punteggio']}</p>
            <p><strong>Percentuale:</strong> {risultato['percentuale']}%</p>
        """
        
        # Aggiungi l'interpretazione in base al test
        if test_name == 'gsrs':
             risultato = calcola_gsrs(risposte_lista)
        elif test_name == 'isi':
            risultato = calcola_isi(risposte_lista)
        elif test_name == 'asi':
            risultato = calcola_asi(risposte_lista)
        elif test_name == 'tas20':
            risultato = calcola_tas20(risposte_lista)
        else:
            return jsonify({'success': False, 'message': 'Test non riconosciuto'})
        
        email_body += f"""
            <h2>Risposte Dettagliate</h2>
            <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%;">
                <tr style="background-color: #f2f2f2;">
                    <th>Domanda</th>
                    <th>Risposta</th>
                </tr>
        """
        
        for i, risposta in enumerate(risposte_lista, 1):
            email_body += f"<tr><td>Domanda {i}</td><td>{risposta}</td></tr>\n"
        
        email_body += """
            </table>
            <hr>
            <p style="font-size: 12px; color: #999;">Email inviata automaticamente dal sistema di valutazione ADHD/Autismo</p>
        </body>
        </html>
        """
        
        # Invia l'email usando Gmail SMTP
        try:
            mittente = EMAIL_MITTENTE
            destinatario = EMAIL_DESTINATARIO
            
            # Crea il messaggio
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'Risultati Test {test_name.upper()} - Codice Paziente: {codice_paziente}'
            msg['From'] = mittente
            msg['To'] = destinatario
            msg.attach(MIMEText(email_body, 'html'))
            
            # Usa Gmail SMTP con SSL
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(mittente, PASSWORD_APP)
            server.sendmail(mittente, destinatario, msg.as_string())
            server.quit()
            
            print(f"Email inviata con successo a {destinatario}")
        except Exception as e:
            print(f"Errore nell'invio dell'email: {str(e)}")
        
        return jsonify({
            'success': True,
            'codice_paziente': codice_paziente,
            'punteggio': risultato['punteggio'],
            'max_punteggio': risultato['max_punteggio']
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


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
