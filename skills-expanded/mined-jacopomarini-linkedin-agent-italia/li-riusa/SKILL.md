---
name: li-riusa
description: >-
  Trasforma un contenuto lungo (video YouTube, podcast, newsletter, articolo,
  trascrizione, webinar, talk a un meetup) in una settimana di post LinkedIn.
  Usala quando l'utente dice "riusa questo", "trasformalo in post", "ho un
  video/una newsletter/una trascrizione", o incolla un contenuto lungo e lo
  vuole su LinkedIn.
---

# li-riusa

Un buon contenuto lungo contiene da quattro a sei post. Quasi tutti ne tirano
fuori uno e buttano il resto.

## Cosa serve

Una trascrizione, un articolo, una newsletter, uno script, il riassunto di una
call. Se l'utente dà un link YouTube e nella sessione c'è uno strumento per le
trascrizioni, usalo; altrimenti chiedi di incollare il testo. Leggi tutto prima
di estrarre qualsiasi cosa.

Se il contenuto è in inglese e i post devono essere in italiano, **non
tradurre frase per frase**: estrai le idee e scrivile in italiano da zero. Una
traduzione si riconosce subito ("fare senso", "giocare un ruolo", "alla fine
della giornata").

## Estrai, non riassumere

Il riassunto di un video non è un post. Nessuno lo vuole. Ripassa il contenuto
e tira fuori le cose che stanno in piedi da sole:

| cosa | cos'è |
| --- | --- |
| **Affermazioni** | ogni frase che farebbe partire una discussione |
| **Numeri** | ogni cifra, costo, durata, percentuale |
| **Storie** | ogni momento con una persona, una scena e un costo |
| **Meccanismi** | ogni spiegazione "funziona così..." |
| **Errori** | ogni ammissione di qualcosa andato storto |
| **Frasi** | ogni frase già citabile così com'è |

Elenca cosa hai trovato, con i conteggi, prima di scrivere. Se il contenuto dà
meno di quattro elementi, è povero, e quattro post spremuti da lì saranno
poveri. Dillo.

## Poi costruisci la settimana

Ogni elemento diventa un post, e ogni post deve stare in piedi da solo: chi
legge non ha visto il video e non lo vedrà. Mai scrivere "come dicevo nel mio
ultimo video". Il post è la cosa.

Assegna a ognuno una formula da `li-post/hooks.json`, e variale: cinque post
dalla stessa fonte con la stessa forma di apertura sembrano una catena di
montaggio.

Ordinali nella settimana così: l'affermazione più forte per prima, la storia a
metà settimana, il meccanismo per ultimo, quando chi ha apprezzato i primi lo
sta aspettando.

## Output

```
FONTE: "Perché abbiamo tolto la call conoscitiva" (18 min, 3.400 parole)

TROVATO  4 affermazioni, 6 numeri, 2 storie, 3 meccanismi, 1 errore, 5 frasi

SETTIMANA
MAR  #1  Controcorrente     La call conoscitiva è una tassa che paghi per un sito fatto male
MER  #17 L'ancora di tempo  Abbiamo recuperato 6 ore a settimana togliendo un link al calendario
GIO  #9  Dialogo            "Ci sentiamo cinque minuti?"
VEN  #21 Il regalo          Il modulo di 4 domande che ha sostituito la call. Prendilo.

Di' "scrivi martedì" e preparo la bozza.
```

Poi scrivi su richiesta, uno alla volta, ognuno con `/li-post` e `/li-umano`.
Non consegnare quattro post finiti insieme: suoneranno tutti uguali e l'utente
non ne modificherà nessuno.
