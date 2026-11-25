---
name: li-inbox
description: >-
  Fa ordine nella casella LinkedIn: divide inviti e messaggi in clienti,
  recruiter, colleghi, richieste e spam, e prepara le risposte che vale la pena
  mandare. Usala quando l'utente dice "la mia casella è un disastro", "smista i
  messaggi", "devo rispondere a questo?", incolla una serie di messaggi
  LinkedIn, o è sommerso da richieste di collegamento.
---

# li-inbox

Quasi tutte le caselle LinkedIn sono per l'80% rumore, e il costo del rumore è
che il 20% che conta resta senza risposta per una settimana. Questa skill li
separa, poi scrive solo quello che vale la pena scrivere.

## Cosa serve

L'utente incolla i messaggi. Gli screenshot vanno bene. Non entrare nel suo
account e non leggere la casella con un browser.

## Cinque gruppi

| gruppo | segnale | azione |
| --- | --- | --- |
| **CLIENTE** | descrive un problema che l'utente risolve, o chiede di lavorare insieme | risposta oggi, completa |
| **RECRUITER** | un ruolo, un'azienda, una RAL | rispondi se il ruolo è vero, una riga se no |
| **COLLEGA** | qualcuno dello stesso campo con qualcosa da dire | rispondi in settimana, da persona |
| **RICHIESTA** | vuole un consiglio, tempo, un contatto, un favore | rispondi se è veloce e preciso, declina con garbo se no |
| **SPAM** | agenzia, sequenza automatica, crypto, "una domanda veloce" senza domanda | archivia, nessuna risposta |

Stampa prima i conteggi. Vedere "3 clienti, 2 recruiter, 41 spam" è già metà
del valore.

## Riconoscere una sequenza automatica

L'outreach automatico ha una forma: una nota d'invito senza niente di
specifico, un messaggio che arriva pochi minuti dopo che hai accettato, "una
domanda veloce", "ho notato che lavori nel settore {settore}", un link al
calendario nel primo messaggio, poi un sollecito esattamente quattro giorni
dopo. Quando la vedi, segnala SPAM e di' quale indizio l'ha tradita. L'utente
non deve una risposta a uno script.

## Risposte

- **CLIENTE**: rispondi alla domanda vera, per intero, gratis. Se c'è
  sintonia, l'offerta è una frase alla fine. Se non c'è, dillo e indica
  qualcuno di utile. Vanno bene entrambe.
- **RECRUITER**: se il ruolo interessa davvero, chiedi le tre cose che il
  messaggio non dice quasi mai: **RAL** (lorda annua, e se c'è una parte
  variabile), **tipo di contratto e CCNL** (indeterminato, determinato,
  partita IVA, consulenza tramite società), e **modalità** (sede, ibrido,
  remoto, e quanti giorni). Se il ruolo non interessa: una riga, non cerco,
  posso indicarti qualcuno, e indicalo davvero.
- **RICHIESTA**: se costa meno di dieci minuti ed è precisa, falla. Se è "ti
  posso rubare un caffè virtuale per farti qualche domanda", declina con una
  frase gentile e dai la risposta che avresti dato in chiamata. È la versione
  educata, ed è anche la più utile.
- **I NO** sono brevi, gentili e definitivi. Niente "risentiamoci dopo l'estate"
  se dopo l'estate non c'è.

## Dati personali

I messaggi contengono dati di altre persone. Usali per rispondere, non per
creare archivi: non copiare nomi, numeri o contenuti dei messaggi in file di
log, e non proporre di esportarli altrove. Nel `log.md` basta un conteggio
("12 inviti, 2 clienti risposti").

## Output

Diviso per gruppi, prima i conteggi, bozze solo per i gruppi che ricevono una
risposta, ognuna umanizzata. Poi il cancello: le manda l'utente.

```
CASELLA  ·  52 messaggi  ·  3 CLIENTE, 2 RECRUITER, 4 COLLEGA, 2 RICHIESTA, 41 SPAM

SPAM  (41) - archivia. 38 sono la stessa sequenza: invito senza dettagli,
"una domanda veloce" 4 minuti dopo l'accettazione, link al calendario nel
primo messaggio.
```
