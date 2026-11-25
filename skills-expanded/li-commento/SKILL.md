---
name: li-commento
description: >-
  Scrive commenti ai post LinkedIn di altre persone che sembrano di qualcuno con
  un'opinione, non di un bot. Usala quando l'utente incolla un post e vuole un
  commento, dice "commenta questo", "cosa scrivo qui", "fammi un giro di
  commenti", o vuole una serie di commenti per la sua sessione giornaliera.
---

# li-commento

Commentare è la cosa che rende di più su LinkedIn ed è la più facile da fare
male. Un commento sotto un post con 400 reazioni lo vedono più persone di
molti post tuoi. Uno generico non lo vede nessuno e ti costa credibilità con
l'autore.

## Cosa serve

L'utente incolla il testo del post (e, se li ha, nome e ruolo dell'autore). Se
incolla uno screenshot, leggilo. Se ti dà un link che non puoi aprire, chiedi
di incollare il testo: non indovinare cosa diceva il post e non usare un
browser per leggere il feed.

## I nove tipi di commento

Scegli in base a cos'è davvero il post. Mai il tipo 1 per default.

| # | tipo | quando | forma |
| --- | --- | --- | --- |
| 1 | **Aggiungi un dato** | il post afferma qualcosa che puoi sostenere con un numero | "Da noi è successo lo stesso: il 40% dei..." |
| 2 | **Il caso mancante** | il post ha ragione ma è incompleto | "Vale finché {condizione}. Dopo..." |
| 3 | **Disaccordo rispettoso** | pensi davvero che sia sbagliato | prima il punto d'accordo, poi dove ti separi |
| 4 | **Estendi una riga** | una frase del post è quella buona | citala, poi costruisci sopra |
| 5 | **La domanda vera** | il post ha saltato la parte difficile | una domanda sola, precisa, senza "sarei curioso di sapere" |
| 6 | **L'esperienza** | hai fatto la cosa che descrive | cosa è successo, in due frasi |
| 7 | **La correzione** | c'è un errore di fatto | abbi ragione, sii breve, gentile e sicuro |
| 8 | **Un'altra lettura** | i fatti giusti, la cornice sbagliata | "Si può leggere anche così:" |
| 9 | **La battuta** | il post non ha bisogno di niente, vuoi esserci | sotto le 12 parole, divertente o vera |

## Regole

- **Da 2 a 4 frasi.** Di più sembra un dirottamento. Di meno, un riempitivo.
- **Mai iniziare con** "Ottimo post", "Bellissimo", "Verissimo", "Non potrei
  essere più d'accordo", "Grazie per aver condiviso", "Spunto interessante", o
  con il nome dell'autore seguito da un punto esclamativo. Sono invisibili.
- **Niente emoji in apertura.** Né 🔥 né 👏 né 💯 come primo carattere.
- **Non riassumere il post.** L'autore sa cosa ha scritto, e anche chi legge.
- **Un'idea.** Un commento con due punti sembra un tentativo di articolo.
- **Dì la cosa specifica.** Se il commento potrebbe stare sotto qualsiasi post
  sull'argomento, non è un commento, è rumore.
- **Il disaccordo è permesso e funziona**, ma prima viene l'accordo, e deve
  essere vero.
- **Tu o Lei** come lo usa l'autore del post. Se l'autore dà del Lei e il
  contesto è formale (legale, PA, sanità), rispondi col Lei.

## Output

Dai **due opzioni di tipo diverso**, etichettate, più una riga sul perché
pubblicheresti una delle due. Passale entrambe per `/li-umano` prima: un
commento con una lineetta lunga sembra scritto da una macchina più di un post,
perché è corto e lo si legge con attenzione.

```
OPZIONI  (sul post di @autore sulle assunzioni)

[6 · Esperienza]
L'anno scorso abbiamo fatto 3 assunzioni senza CV. Due sono state le migliori
che abbiamo mai fatto. La terza un disastro, e la differenza era se avevano
già fatto quel lavoro, non come andava il colloquio.

[3 · Disaccordo rispettoso]
D'accordo sul problema del segnale. Ma a noi non è servito togliere il CV: è
servito dare a tutti la stessa prova pagata da 90 minuti. Stesso risultato,
molte meno discussioni interne.

Pubblicherei la prima: sono dati tuoi e ammetti un fallimento, che è la parte
a cui la gente risponde.
```

## Modalità serie

Se l'utente vuole un giro di commenti, chiedi i 5-10 post incollati in un solo
messaggio, restituisci un commento per post in un blocco unico, e tieni nota
in `~/.claude/linkedin/log.md` di chi ha già commentato questa settimana.
Commentare sempre le stesse tre persone ogni giorno si vede, e sembra quello
che è.

## Mai

Non pubblicare in automatico. Non usare un browser per pubblicare commenti al
posto dell'utente. Pubblicazione automatica e scraping violano il Contratto
di licenza di LinkedIn e mettono a rischio l'account. Questa skill scrive il
commento. Lo pubblica l'utente.
