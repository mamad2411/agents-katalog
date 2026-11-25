---
name: li-dal-codice
description: >-
  Trasforma il lavoro tecnico di uno sviluppatore (un bug risolto, una pull
  request, un refactoring, una migrazione, un incidente, una cosa imparata con
  Claude Code) in un post LinkedIn, togliendo prima tutto ciò che è del cliente
  o del datore di lavoro. Usala quando l'utente dice "fammi un post da questo
  bug", "ho risolto X, ne faccio un post?", "trasforma questa PR in un post",
  incolla un diff, un log, un messaggio di commit o descrive un problema tecnico
  da raccontare.
---

# li-dal-codice

Gli sviluppatori hanno ogni settimana materiale per tre post e ne pubblicano
zero, per due motivi: pensano che il loro lavoro "non interessi a nessuno", e
temono di dire troppo su un progetto che non è loro. Questa skill risolve il
secondo problema in modo sistematico, e così anche il primo.

## Passo 1: il filtro di riservatezza (sempre, prima di tutto)

Prima di scrivere una riga, passa il materiale per questo filtro e **mostra
all'utente cosa hai tolto**:

| togli o generalizza | esempio | diventa |
| --- | --- | --- |
| Nome del cliente o del committente | "il portale di Banca X" | "un portale bancario" |
| Nomi di persone, colleghi, utenti | "Marco del team backend" | "un collega del backend" |
| Codice proprietario | il diff reale | un esempio minimo riscritto da zero, o nessun codice |
| URL interni, host, IP, nomi di repository | `gitlab.cliente.it/...` | niente |
| Chiavi, token, credenziali, anche parziali | `sk-...4f2a` | niente, e avvisa l'utente se erano nel testo |
| Cifre del cliente (utenti, fatturato, volumi) | "1,2 milioni di contribuenti" | "milioni di utenti", o chiedi se il dato è pubblico |
| Dettagli di sicurezza non risolti | una vulnerabilità aperta | **non se ne parla** finché non è chiusa e autorizzato |
| Progetti pubblici o della PA | dettagli di architettura o sicurezza | solo ciò che è già pubblico |

Se dopo il filtro non resta niente di raccontabile, dillo: meglio nessun post
che un post che costa il lavoro. Se l'utente lavora per una società di
consulenza su un cliente, ricordagli che spesso servono **due** autorizzazioni,
della società e del cliente, per nominare il progetto.

## Passo 2: trova la storia nel lavoro tecnico

Il post non parla della tecnologia, parla di cosa è successo. Cerca:

- **Il costo**: quanto tempo, quanti soldi, quanti utenti bloccati, quante
  notti. È il numero dell'apertura.
- **Il momento in cui hai sbagliato pista**: la parte che gli altri sviluppatori
  riconoscono, e quella che fa commentare.
- **Il meccanismo**: la causa vera, spiegata in una frase che capisce anche un
  non sviluppatore. Se serve un paragrafo, il post è per un pubblico tecnico:
  va bene, ma decidilo.
- **La regola che ti porti via**: quella che metteresti in un CLAUDE.md, in una
  checklist di revisione, in un README.

Se il lavoro è stato fatto con l'IA, di' **cosa ha fatto l'IA e cosa hai fatto
tu**. "Claude l'ha trovato in un minuto" senza dire cosa gli hai dato e cosa
hai controllato dopo è il tipo di post che fa sembrare l'IA magia e chi scrive
un passacarte.

## Passo 3: scegli il pubblico

| pubblico | come scrivere |
| --- | --- |
| Altri sviluppatori | termini tecnici sì, uno snippet minimo va bene, la lezione è tecnica |
| Recruiter e responsabili tecnici | meno codice, più impatto e decisioni: cosa hai capito, cosa hai cambiato nel processo |
| Clienti non tecnici | zero gergo, solo costo, rischio evitato e risultato |

## Passo 4: scrivi

Passa a `/li-post` con l'idea già filtrata, il numero e il pubblico. Formule
che di solito funzionano per i post tecnici: #17 L'ancora di tempo, #3 L'errore
confessato, #9 Si apre col dialogo (il messaggio del collega o dell'errore),
#21 Il regalo (la checklist, il prompt o il file di configurazione, riscritto
da zero e senza riferimenti al progetto).

Se nel post c'è codice: **massimo 5-6 righe**, scritto da zero per il post, mai
copiato dal repository. LinkedIn non formatta il codice: valuta un'immagine o
un link a un gist nel primo commento.

## Output

```
FILTRO RISERVATEZZA
  tolti:          nome cliente, 2 nomi di colleghi, URL interno, numero utenti
  generalizzato:  "portale per la dichiarazione dei redditi" -> "un portale pubblico molto usato"
  da chiedere:    puoi dire che è un progetto per la PA? (sì/no)

STORIA
  costo:          3 ore, test bloccato in CI
  pista sbagliata: ho riscritto il componente due volte
  meccanismo:     fuso orario del runner diverso dal mio
  regola:         prima del codice, controlla ambiente, fuso, versioni

Pubblico: sviluppatori. Passo a /li-post con apertura #17?
```

Come tutto il pacchetto: nessuna pubblicazione automatica. Il post lo
pubblica l'utente, dopo averlo riletto pensando al suo contratto.
