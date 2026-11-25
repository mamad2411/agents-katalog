---
name: li-profilo
description: >-
  Valuta un profilo LinkedIn su 100 punti con una griglia di 12 voci e riscrive
  le parti che perdono punti: titolo, informazioni, esperienze, in primo piano,
  immagine di copertina, profilo in lingua secondaria. Usala quando l'utente
  dice "ottimizza il mio profilo", "valuta il mio LinkedIn", "riscrivi il mio
  titolo", "sistema la sezione informazioni", o incolla il profilo e chiede
  come appare.
---

# li-profilo

Un profilo non è un curriculum. Il curriculum risponde a "cosa hai fatto". Il
profilo risponde a "dovrei scrivere a questa persona?", e lo fa in circa
quattro secondi, con il titolo e le prime due righe delle informazioni.

## Cosa serve

Chiedi all'utente di incollare: titolo, sezione informazioni, ruolo attuale e
le ultime due esperienze, e se ha immagine di copertina e sezione in primo
piano. Per il primo giro basta uno screenshot della parte alta. Non entrare
in LinkedIn al suo posto.

## Il punteggio

Leggi `rubrica.json` in questa cartella: dodici voci, 100 punti, ognuna con
come appare il punteggio pieno. Valuta ogni voce, mostra la tabella e il
totale. Sii onesto: al primo giro quasi tutti i profili stanno tra 30 e 50, e
un punteggio generoso non serve a niente.

```
PUNTEGGIO PROFILO  41/100

  titolo                 3/12   solo il ruolo, nessun risultato, nessun pubblico
  informazioni apertura  2/10   apre con "appassionato di"
  informazioni corpo     4/10   storia personale, non un'offerta
  in primo piano         0/8    vuoto
  copertina              0/6    sfondo predefinito
  ...
```

## Poi riscrivi, in quest'ordine

Sistema in ordine di punti persi. Non riscrivere tutto insieme: ogni pezzo
l'utente lo deve incollare a mano.

**1. Titolo (220 caratteri).** La formula che funziona:
`{cosa fai per chi} | {prova} | {come iniziare}`. Non il nome del ruolo. Non
"Aiuto X a fare Y" come prime tre parole, che ormai apre un profilo su due.
Non "Frontend Developer | React | TypeScript | Node | AWS". Dai tre opzioni.

**2. Informazioni, prime due righe.** Su mobile tutto ciò che viene dopo è
nascosto da "vedi altro", quindi per la maggior parte dei lettori quelle due
righe sono l'intera sezione. Devono dire chi aiuti e cosa cambia. Niente
"appassionato", niente "orientato ai risultati", niente biografia in terza
persona, niente apertura con il proprio nome.

**3. Informazioni, corpo.** Scritto a un lettore, in seconda persona (tu o Lei
secondo `voce.md`). Struttura: il problema che ha, cosa fai, una prova con un
numero, cosa fare dopo. Sotto i 1.400 caratteri, anche se il limite è 2.600.

**4. In primo piano.** Tre elementi: il post migliore, una prova del lavoro, il
modo per contattarti. Una sezione vuota sono otto punti, ed è l'unico posto
del profilo che controlli del tutto.

**5. Esperienze.** Ogni ruolo: una riga sul perimetro e due o tre risultati con
numeri, non mansioni. Tutto ciò che ha più di dieci anni, una riga sola. Se
lavori come consulente per un cliente (tipico in Italia: società di consulenza
che ti mette su un progetto), scrivi il nome della società che ti paga e il
settore del cliente; il nome del cliente solo se sei autorizzato.

**6. Copertina.** Una frase di posizionamento e un modo per contattarti. Lo
sfondo blu predefinito è il segnale più chiaro che non c'è nessuno.

**7. Lingua secondaria.** Se l'utente lavora con l'estero o ci si è
trasferito, non mischiare italiano e inglese nello stesso profilo. LinkedIn
permette di creare una versione del profilo in un'altra lingua: chi la
visita la vede nella lingua del suo LinkedIn. Per scriverla usa `/li-bilingue`.

## Output

Tabella dei punteggi, poi le riscritture in blocchi pronti da copiare,
nell'ordine di priorità, ognuna già passata per `/li-umano`. Alla fine
ricalcola e mostra il miglioramento con onestà: se la riscrittura arriva a
88 e non a 98, di' 88, e di' cosa servono i punti mancanti (di solito
segnalazioni, una copertina vera e un po' di storico di post, cose che una
riscrittura non può creare).

Questa skill non salva niente su LinkedIn. L'utente incolla ogni sezione.
