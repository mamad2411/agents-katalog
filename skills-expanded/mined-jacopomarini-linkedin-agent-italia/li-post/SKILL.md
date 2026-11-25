---
name: li-post
description: >-
  Scrive un post LinkedIn in italiano partendo da un'idea grezza, con 21 formule
  di apertura, nella voce dell'utente e ripulito con /li-umano perché non sembri
  scritto dall'IA. Usala quando l'utente vuole un post LinkedIn, un'apertura,
  una bozza per il feed, "scrivi un post su X", "trasforma questo in un post",
  o chiede opzioni di apertura. Produce tre aperture, una bozza completa e un
  blocco pronto da copiare, che non viene mai pubblicato senza un sì esplicito.
---

# li-post

Trasforma un'idea grezza in un post LinkedIn che suona come la persona che lo
pubblica.

## Prima di scrivere

1. Leggi `~/.claude/linkedin/voce.md` se esiste. È il profilo di voce
   dell'utente: come parla, cosa non direbbe mai, a chi si rivolge, se dà del
   tu o del Lei. Se non esiste, chiedi **tre post scritti da lui**, ricava la
   voce da quelli e scrivi il file. Non saltare questo passaggio e non
   inventare una voce: un post con la voce sbagliata è peggio di nessun post.
2. Leggi `hooks.json` in questa cartella: le 21 formule, con schema, esempio,
   a cosa servono e come di solito si rovinano.
3. Se l'idea è debole ("un post sull'IA"), non riempire il vuoto. Fai una
   domanda sola, raggruppata: cosa è successo, a chi, e quanto è costato o
   cosa ha reso. Un post ha bisogno di una cosa vera e precisa. Prendila prima
   di scrivere.

## La forma

```
Riga 1     l'apertura. Da sola. Deve reggere al taglio a ~140 caratteri su mobile.
Riga 2     il compimento della riga 1, non la preparazione della riga 3.
Corpo      paragrafi brevi, 1-3 righe, una riga vuota tra uno e l'altro.
           Niente muro di testo. Lo spazio bianco è il formato.
La svolta  una riga che rilegge quello che è venuto prima.
Chiusura   una domanda precisa, oppure un'istruzione. Mai entrambe.
```

Lunghezza: 900-1.300 caratteri è la fascia che funziona per un post di solo
testo. L'italiano è più lungo dell'inglese: se sei sopra 1.500, togli, non
comprimere.

## Il giro

**1. Tre aperture, non una.** Passa l'idea per `hooks.json` e scegli le tre
formule che ci stanno davvero. Formule diverse, non tre varianti della stessa.
Mostrale come tre righe numerate e di' quale pubblicheresti e perché, in una
frase.

**2. Scrivi il post completo** sull'apertura più forte.

**3. Umanizzalo.** Passa la bozza per `/li-umano` prima di mostrarla. Ogni
post di questa skill esce umanizzato. Non è un passaggio facoltativo: è il
motivo per cui vale la pena leggere la bozza.

**4. Stampa il blocco.** Pronto da copiare, in un blocco di codice, esattamente
come va incollato. Sotto:

```
POST PRONTO
apertura:   #17 L'ancora di tempo
lunghezza:  1.140 caratteri
umano:      6 tracce tolte, punteggio 84 PASSA
pubblica:   martedì 8:15 (dal tuo piano)

Rispondi "sì" per registrarlo, oppure dimmi cosa cambiare.
```

**5. Non pubblicare mai.** Questa skill produce testo. Lo pubblica l'utente.
Al "sì", aggiungi il post a `~/.claude/linkedin/log.md` con data, formula usata
e prima riga, così `/li-audit` avrà uno storico su cui lavorare.

## Le regole che fanno la differenza

- **Un'idea per post.** Se la bozza ne ha due, sono due post. Dillo.
- **Numeri, non aggettivi.** "4.200 euro" batte "tanti soldi". Se l'utente non
  ti ha dato un numero, chiedilo invece di scrivergli intorno.
- **Niente esche.** "Che ne pensate?" e "Siete d'accordo?" sono morte. La
  domanda finale deve essere una che solo questo post può fare.
- **Niente elenchi di ✅.** In Italia sono il segno più riconoscibile di un post
  generato. Se serve un elenco, trattini e frasi intere.
- **Al massimo tre hashtag**, in fondo, e solo se sono categorie che qualcuno
  segue davvero.
- **Niente link nel corpo del post.** Mettilo nel primo commento e dillo nel
  riepilogo.
- **Tu o Lei, coerente.** Segui `voce.md`. Nel dubbio, in Italia su LinkedIn il
  tu è la norma tra professionisti del digitale; il Lei resta per settori come
  legale, sanitario, PA e per chi scrive a un pubblico senior tradizionale.
- **Mai inventare.** Niente metriche, clienti, fatturati o risultati inventati
  sotto il nome dell'utente, nemmeno come segnaposto. Se serve un numero che
  non hai, lascia `{{il tuo numero}}` nella bozza e segnalalo.
- **Niente dati del cliente o del datore di lavoro.** Se il post nasce da un
  progetto di lavoro, togli nomi, cifre e dettagli riconoscibili, oppure usa
  `/li-dal-codice`, che lo fa in modo sistematico.

## Esempio

```
/li-post abbiamo fatto uno strumento interno che porta i preventivi da 5 ore a 20 minuti
```

```
APERTURE
1. #17 L'ancora di tempo   Un preventivo mi richiedeva 5 ore. Ora ci metto 20 minuti.
2. #12 Il confronto        Un consulente da 12.000 euro contro un weekend e un modello. Ha vinto il weekend.
3. #3  L'errore confessato Per due anni ho fatto pagare ai clienti ore che sprecavo a impaginare.

Pubblicherei la #17: il rapporto è credibile e il numero è tuo.
```
