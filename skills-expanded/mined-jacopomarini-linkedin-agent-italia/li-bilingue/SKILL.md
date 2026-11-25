---
name: li-bilingue
description: >-
  Per chi su LinkedIn parla a due pubblici, italiano e internazionale: scrive lo
  stesso post in italiano e in inglese come due testi nativi (non uno tradotto
  dall'altro), prepara il profilo in lingua secondaria e decide quale lingua
  usare per ogni contenuto. Usala quando l'utente dice "fallo anche in
  inglese", "versione inglese", "profilo in inglese", "lavoro all'estero",
  "cerco lavoro fuori dall'Italia", o scrive per un pubblico misto.
---

# li-bilingue

Molti professionisti italiani hanno due pubblici: chi li conosce in Italia e
il mercato internazionale (un trasferimento all'estero, clienti fuori, un
lavoro da remoto per un'azienda straniera). Il pacchetto originale era solo
in inglese; quello italiano, da solo, ignorerebbe metà di queste persone.
Questa skill tiene insieme le due lingue senza far sembrare nessuna delle due
una traduzione.

## Prima di tutto: una lingua per post, o due?

Chiedi (o leggi in `voce.md`) chi sono i due pubblici e quanto pesano. Poi:

| situazione | cosa fare |
| --- | --- |
| Il pubblico è al 70%+ in una lingua | scrivi in quella. L'altra solo per i post che la riguardano davvero |
| Due pubblici simili per peso | **due post separati**, in giorni o orari diversi, ognuno nativo |
| Post sull'Italia per stranieri, o sull'estero per italiani | la lingua di chi legge, non di chi scrive |

**Mai lo stesso post con italiano sopra e inglese sotto.** Raddoppia la
lunghezza, taglia l'apertura a metà e chi legge una lingua scorre via. Se
serve proprio un post unico, scegli una lingua e metti l'altra nel primo
commento.

## Due testi nativi, non una traduzione

Parti dall'idea, non dal testo. Per ogni lingua:

1. Scegli l'apertura giusta **per quella lingua** da `li-post/hooks.json`. In
   inglese funzionano frasi più corte e secche; in italiano regge una frase
   in più di contesto. Non serve che le due aperture siano la stessa formula.
2. Adatta gli esempi al pubblico: euro o dollari, "partita IVA" o "contractor",
   "RAL" o "base salary", riferimenti che chi legge riconosce.
3. Passa ciascun testo per `/li-umano` con la sua lingua (`--lingua it` e
   `--lingua en`): i cliché sono diversi, e un testo tradotto ha i suoi
   ("this makes sense" da "ha senso", "at the end of the day" da "alla fine").
4. Controlla i calchi nei due sensi. In italiano: "fare senso", "giocare un
   ruolo", "applicare per una posizione", "realizzare" per "rendersi conto".
   In inglese: "I'm graduated", "since 3 years", "make a question",
   "actual" per "attuale".

## Il profilo in lingua secondaria

LinkedIn permette di creare il profilo in un'altra lingua: chi lo visita lo
vede nella lingua del suo LinkedIn, se disponibile. È molto meglio di un
profilo con le due lingue mescolate.

- **Lingua principale**: quella del mercato in cui cerchi lavoro o clienti
  adesso.
- **Titolo**: riscritto per ciascun mercato, non tradotto. Ruoli e titoli
  cambiano tra paesi ("Sviluppatore frontend" non è sempre "Frontend
  Developer", e "consulente" in italiano spesso vuol dire dipendente di una
  società di consulenza, cosa che fuori dall'Italia va spiegata).
- **Esperienze**: in inglese spiega cosa sono le realtà italiane che chi legge
  non conosce ("Agenzia delle Entrate" → "the Italian Revenue Agency"; una
  società di consulenza IT → di' che lavori per i suoi clienti).
- **Titoli di studio**: non tradurre "laurea" con "degree" alla leggera, e non
  rendere più forte di quanto è un percorso non concluso. Scrivi cosa hai fatto.
- Valuta entrambe le versioni con `/li-profilo`.

## Output

```
POST BILINGUE  ·  idea: "test che passano in locale e falliscono in CI"

[IT]  apertura #17 · 1.050 caratteri · umano 82 PASSA
...testo...

[EN]  apertura #2  ·   880 caratteri · umano 79 PASSA
...testo...

Pubblica l'italiano martedì alle 8:15 ora di Roma, l'inglese giovedì alle 8:30
ora del tuo pubblico estero. Non lo stesso giorno: chi ti segue in entrambe
le lingue vedrebbe due volte la stessa cosa.
```

Non si pubblica niente: i testi li incolla l'utente.
