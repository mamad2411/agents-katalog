---
name: li-audit
description: >-
  Analisi a posteriori di quello che l'utente ha già pubblicato: quali post
  hanno funzionato davvero, perché, e cosa smettere di fare. Usala quando
  l'utente incolla le statistiche LinkedIn o i post passati e chiede "cosa sta
  funzionando", "perché questo è andato male", "leggi le mie statistiche",
  "analizza i miei contenuti", o vuole sapere su cosa insistere.
---

# li-audit

L'unica fonte onesta di cosa funziona per un account è quell'account. Ogni
regola di ogni guida su LinkedIn, comprese quelle di questo pacchetto, è
un'ipotesi di partenza. Gli ultimi 30 post dell'utente sono le prove.

## Cosa serve

Chiedi quello che l'utente ha:

- L'esportazione delle statistiche dei contenuti, che LinkedIn permette di
  scaricare dalla sezione delle statistiche. Attenzione: nei file esportati in italiano le
  migliaia possono usare il punto e i decimali la virgola. Controlla prima di
  fare i conti.
- Oppure uno screenshot per post con impressioni, reazioni, commenti, diffusioni.
- Oppure solo i post con il numero di reazioni, che basta per un primo giro.

Leggi anche `~/.claude/linkedin/log.md` se esiste: registra quale formula di
apertura ha usato ogni post.

## Cosa misurare davvero

Le impressioni sono il numero meno utile della pagina, perché dipendono quasi
solo da quanti follower ha già l'utente. Calcola invece questi, mostrando i
conti:

| metrica | come | cosa dice |
| --- | --- | --- |
| **Tasso di interazione** | (reazioni + commenti + diffusioni) / impressioni | se il post si è meritato la sua portata |
| **Rapporto commenti** | commenti / reazioni | se ha fatto discutere o ha solo ricevuto un cenno |
| **Moltiplicatore di portata** | impressioni / follower | se è arrivato oltre il pubblico che già c'era |
| **Salvataggi e invii** | se disponibili | il segnale più forte di portata futura |

Ordina per tasso di interazione e moltiplicatore, non per impressioni. Un post
con 900 impressioni e 40 commenti ha battuto quello con 12.000 impressioni e 6.

## Poi cerca lo schema

Con i 5 migliori e i 5 peggiori uno accanto all'altro, cerca cosa li
distingue davvero, e sii pronto a concludere qualcosa che all'utente non
piacerà:

- Formula di apertura. Quali numeri di `hooks.json` stanno nei primi 5?
- Formato. Testo, documento, immagine, video.
- Lunghezza.
- Tema.
- Lingua, se l'utente pubblica sia in italiano sia in inglese.
- Giorno e ora: controllali **per ultimi**, e solo se il resto non mostra
  niente. Non sono quasi mai la causa, ed è lì che le persone vorrebbero
  trovarla. Escludi dal confronto i post usciti ad agosto o durante i ponti.
- Commenti nella prima ora. Post a cui l'utente ha risposto entro un'ora
  contro quelli no.

Scrivi la conclusione come un'affermazione con le prove accanto, e di' quanto
sei sicuro. Con 30 post si vede uno schema; con 6 no, e devi dirlo invece di
inventarne uno.

## Output

```
ANALISI  ·  31 post  ·  12 giu - 5 set

I 5 MIGLIORI PER TASSO DI INTERAZIONE
  8,1%  #3  L'errore confessato   "4.000 euro: ecco quanto mi è costato..."   1.940 imp
  6,4%  #20 L'addio               "Ho chiuso con il cliente che pagava di più"  2.210 imp
  ...

I 5 PEGGIORI
  0,4%  #5  La lista               "7 strumenti che ogni freelance deve avere"  11.400 imp
  ...

COSA DICONO I DATI
1. I post in cui facevi brutta figura tu: media 6,2% contro 1,1% del resto.
   n=6. È il segnale più forte e non è vicino.
2. Le liste di strumenti fanno impressioni e nient'altro. Molta portata,
   niente commenti, nessun contatto. Tre dei tuoi cinque peggiori.
3. Il giorno della settimana non mostra niente. Martedì e venerdì sono dentro
   il rumore. Smetti di ottimizzarlo.

SMETTI: liste di strumenti.
FAI DI PIÙ: i post con un costo che hai pagato tu, e un numero.
```

Poi passa le conclusioni a `/li-piano`, così il piano della settimana dopo si
basa sulle prove dell'utente e non sui valori predefiniti.
