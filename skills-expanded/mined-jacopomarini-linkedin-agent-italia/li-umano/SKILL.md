---
name: li-umano
description: >-
  Toglie l'impronta da macchina da qualsiasi bozza, in italiano o in inglese:
  lineette lunghe, cliché da IA ("in un mondo in continua evoluzione", "sono
  entusiasta di annunciare", "sinergia"), caratteri invisibili, strutture tipiche
  ("Non è solo X, è Y", elenchi di ✅), e la valuta con un pannello di cinque
  controlli prima che esca. Usala quando un testo deve suonare umano, quando
  l'utente dice "umanizza", "sembra scritto dall'IA?", "togli le lineette",
  "ripuliscilo", "verrà segnalato?", e sempre prima di mostrare un post, un
  commento, una risposta o un messaggio LinkedIn.
---

# li-umano

In questa cartella ci sono due strumenti, e funzionano davvero. Usali. Non
andare a occhio.

```bash
python3 umanizza.py bozza.txt --report        # ripulisce e mostra cosa è cambiato
python3 rileva.py bozza.txt                    # punteggio, cinque controlli
python3 rileva.py prima.txt dopo.txt           # dimostra il miglioramento
```

La lingua si riconosce da sola. Per forzarla: `--lingua it` o `--lingua en`.

Ci sono due lessici: `lessico.it.json` (cliché italiani dell'IA e di LinkedIn
Italia) e `lessico.en.json` (quello originale inglese). Sono fatti per essere
modificati: se l'utente usa davvero una parola che il lessico toglie, va tolta
dal file.

## Cosa si sistema da solo

**1. Caratteri invisibili.** Spazi a larghezza zero, word joiner, trattini
morbidi, BOM, caratteri tag Unicode, spazi non separabili. Una tastiera non li
produce, sopravvivono al copia-incolla e sono la traccia più meccanica del
testo generato.

**2. Tipografia.** Lineetta lunga → virgola, lineetta media → trattino,
virgolette alte curve → dritte, puntini → tre punti. **In italiano le
«virgolette basse» restano** e l'apostrofo tipografico (’) che iPhone e Mac
mettono da soli in "l’IA" viene normalizzato ma **non penalizzato**.

**3. Il lessico.** Le voci con un sostituto vengono cambiate:
"in un mondo in continua evoluzione" → "oggi", "gioca un ruolo fondamentale"
→ "conta molto", "sono entusiasta di annunciare" → "annuncio", "sinergia" →
"collaborazione", "è importante sottolineare che" → eliminata.

**Le citazioni non si toccano.** Il testo tra virgolette ("...", «...»,
“...”) è una citazione, non un uso: non viene riscritto e non conta nel
punteggio. Così un post che critica i cliché può citarli.

## Cosa NON si sistema da solo

**Parole da riscrivere.** In italiano molti aggettivi cambiano con genere e
numero: "innovativo/innovativa/innovativi/innovative". Una sostituzione
automatica romperebbe l'accordo, quindi queste voci (`"replace": null` nel
lessico) vengono solo segnalate, spesso con un suggerimento: "innovativo",
"olistico", "a 360 gradi", "mindset", "mettersi in gioco", "fare la
differenza", "resilienza", "inoltre" a inizio frase.

**Strutture.** Vengono segnalate, mai riscritte, perché cambiare la forma di
una frase richiede giudizio:

- "Non è solo X, è Y", "Non solo X ma anche Y", "Non si tratta di X, si tratta di Y"
- La domanda-rivelazione su una riga sola: "Il risultato?", "La verità?"
- Tre aggettivi in fila: "veloce, semplice e sicuro."
- **Elenchi con ✅ 👉 ➡️**: il formato più riconoscibile dei post generati in italiano
- "Sono entusiasta di...", "Ecco cosa ho imparato", "La verità è che", "Spoiler:"
- "In conclusione", "In sintesi", "Tirando le somme"
- La domanda finale di riflesso: "Tu cosa ne pensi?", "Siete d'accordo?"
- Emoji razzo, fuoco, lampadina, scintille, bersaglio. Muri di hashtag.
- Frasi tutte della stessa lunghezza

Questa lista è lavoro tuo. Riscrivi ogni riga segnalata a mano, mantenendo il
senso, poi rilancia `rileva.py`. È questa parte che porta il punteggio da
RIVEDI a PASSA, ed è quella che uno script non può fare.

## I cinque controlli

`rileva.py` dà un punteggio da 0 a 100 a cinque segnali. Più alto è più umano.

| controllo | cosa misura | come appare una macchina |
| --- | --- | --- |
| RITMO | variazione della lunghezza delle frasi | frasi tutte uguali |
| CONCRETEZZA | numeri, nomi, sigle, date ogni 100 parole | nomi astratti, nessun dato |
| CLICHÉ | voci del lessico ogni 100 parole | linguaggio da comunicato |
| IMPRONTA | invisibili, lineette lunghe, virgolette curve | tipografia perfetta |
| VOCE | prima e seconda persona, registro parlato, strutture | impersonale, rivelazioni messe in scena |

In italiano VOCE non conta le contrazioni (non esistono) e non può contare
solo i pronomi, perché il soggetto si omette ("ho fatto", non "io ho fatto").
Conta le forme verbali e i possessivi di prima e seconda persona, e i segnali
di parlato ("insomma", "onestamente", "tipo", "alla fine", "un sacco").

Il verdetto pesa la media al 60% e **il controllo più debole** al 40%, perché
a un rilevatore basta un segnale. PASSA richiede almeno 70 complessivo e
nessun controllo sotto 55.

## Dillo con onestà

Sono cinque euristiche locali modellate sui segnali dei rilevatori pubblici.
Girano sul computer dell'utente e non caricano niente online. **Non** sono
GPTZero, Originality, Copyleaks, Winston o Turnitin, non chiamano le loro API
e non possono promettere il loro verdetto. Sistemare quello che misurano
tende a spostare anche quei numeri, perché misurano le stesse cose. Questa è
la promessa. Non farne una più grande per conto dell'utente e non dirgli mai
che il suo testo è "non rilevabile".

## Ordine delle operazioni

1. `umanizza.py bozza.txt -o pulito.txt --report`
2. Leggi parole e strutture segnalate. Riscrivi tu quelle righe.
3. `rileva.py bozza.txt pulito.txt` per mostrare il prima e dopo.
4. Se il verdetto non è PASSA, sistema il controllo più debole indicato e
   rifai. Due giri sono normali. Cinque vogliono dire che la bozza è scritta a
   formula, e la soluzione è un'altra bozza, non altri passaggi.
5. Mostra all'utente il testo pulito e il punteggio. Mai il punteggio da solo.
