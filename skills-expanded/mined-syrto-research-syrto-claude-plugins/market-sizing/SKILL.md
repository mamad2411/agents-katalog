---
name: market-sizing
description: >
  Market sizing for the Italian market with Syrto: defines which
  companies really make up a market (by real business activity, beyond rigid Ateco codes) and
  measures how many they are, their revenue, margins and growth. Two methods, chosen at the
  start: Syrto semantic search (default) or Ateco/NACE codes.
  Trigger on: market sizing, market size, "how big is the [X] market", TAM, industry aggregates,
  "dimensione del mercato", "quanto vale il mercato di [X]", "quante aziende ci sono nel mercato
  di [X]", "perimetro di mercato", "dimensiona il settore [X]", "aggregati di settore",
  especially cross-Ateco sectors (facility management, fintech, digital health, IoT). Also when
  another Syrto skill needs the market a company operates in.
  Not for: benchmarking one company against its sector (use market-benchmark), a peer or
  competitor list (use syrto-comparables), or a single-company report (use company-analysis).
  Start from a company only if the user explicitly wants the MARKET it operates in sized.
---

# Syrto Market Sizing

Segui `${CLAUDE_PLUGIN_ROOT}/shared/core.md` (metodo, output, efficienza) e la capability map (`${CLAUDE_PLUGIN_ROOT}/shared/syrto-reference.md`), che dice quale strumento Syrto corrisponde a ogni capacità citata qui.

Questa skill fa **market sizing**: definisce il perimetro di un mercato e ne misura la dimensione. Il metodo di default è **semantico**, cioè definisce il perimetro — in base a cosa fanno davvero le aziende — anziché per codici Ateco/NACE. È particolarmente utile per settori che attraversano più codici Ateco (facility management, fintech, digital health, ecc.) dove nessun singolo codice cattura il mercato reale.

## Modalità di esecuzione

La skill esegue in una di due modalità, decise allo Step 1:

- **Modalità A — Singola Search**: per mercati atomici, dove tutte le aziende fanno fondamentalmente la stessa cosa. Una sola ricerca semantica, una soglia, niente decomposizione né deduplicazione.
- **Modalità B — Decomposizione**: per mercati ampi che attraversano dimensioni diverse (HW vs SW, prodotto vs servizio, ecc.). Più sotto-mercati calibrati in sequenza, calibrazione indipendente, conteggio del perimetro unico al netto delle sovrapposizioni.

La scelta della modalità avviene allo Step 1 con conferma esplicita dell'utente.

## Obiettivo

Dato un mercato richiesto dall'utente, questa skill deve:

1. Decidere se il mercato è atomico (Modalità A) o ampio (Modalità B)
2. Definire uno o più testi di ricerca in inglese ottimizzati per la semantic search di Syrto
3. Per ciascuna ricerca, calibrare la soglia di match controllando i risultati al confine
4. Produrre in output la dimensione reale del mercato

Il flusso è semplice e lineare: **valuta atomicità → cerca → valida → aggiusta → aggrega**.

## Dove ti fermi e aspetti

In alcuni punti ti fermi, chiedi e aspetti la risposta prima di proseguire. Chiedi con una scelta strutturata se il tuo client la offre, altrimenti con una breve domanda a opzioni numerate. Testi e opzioni sono nei file `references/`.

- **Domande iniziali** (fonti, metodo, anno): cambiano cosa cerchi, da dove prendi il contesto e su quale anno conti.
- **Conferma del mercato** (Step 0, solo se parti da un'azienda): tutto il resto si costruisce su quella definizione.
- **Checkpoint 1: il perimetro** (testo della singola search in Modalità A, decomposizione e testi in Modalità B, lista di codici nel percorso ATECO). La calibrazione costa decine di ricerche, e un perimetro sbagliato le spreca tutte.
- **Checkpoint 2: la calibrazione** (soglie, conteggi, le 20 aziende al confine con il verdetto IN/OUT). Il giudizio al confine è l'unico passo soggettivo e decide se il mercato conta 30 o 1.000 aziende, quindi l'utente deve poterlo correggere prima dell'output.

Una risposta libera si interpreta: approvazione → prosegui; richiesta di modifica → applicala e ripresenta lo stesso checkpoint; risposta ambigua → richiedi. Se l'utente ti chiede esplicitamente di procedere senza conferme, salta il checkpoint e scrivilo nella nota **Metodo** del deliverable.

---

## Comunicazione durante l'esecuzione

Alcune chiamate Syrto sono lente: se lavori in silenzio la chat sembra ferma e l'utente non capisce se il lavoro è partito. Per questo, prima di ogni attività scrivi una riga con cosa stai per fare e perché serve, e dopo scrivi l'esito. In particolare:

- Le **prime chiamate di setup** (risoluzione dell'azienda, lettura della documentazione dei filtri di ricerca): è lì che i tool tendono a partire senza una riga davanti.
- Prima della **prima calibrazione**, il **piano**: quanti sotto-mercati calibrerai e in che ordine, così l'utente sa cosa aspettarsi mentre le chiamate girano. Es.: *"Ho 3 sotto-mercati (formule, cereali/omogeneizzati, svezzamento/integratori). Calibro le soglie uno alla volta, cercando per ciascuno la più bassa che tiene ≥15/20 aziende pertinenti al confine. Parto dal primo."*
- All'inizio di **ogni attività** (calibrazione di un sotto-mercato, conteggio del perimetro unico) cosa stai facendo e cosa ti aspetti.
- Quando una **calibrazione va a buon fine**, dillo subito: **soglia trovata** e **quante aziende** ci sono in quel sotto-mercato, poi il passo successivo. Es.: *"✅ Sotto-mercato 2 chiuso: soglia 0.83, 3 aziende. Passo al sotto-mercato 3."*
- Se una chiamata va in **timeout e la ripeti**, dillo in una riga (*"Syrto ha risposto lento, ripeto la chiamata"*), così l'attesa è comprensibile.

Vale anche quando la skill è chiamata da un'altra skill.

---

## Inputs

Serve uno di questi:

1. **Un nome azienda o una partita IVA** — in questo caso parti dallo Step 0 (Identificazione Mercato)
2. **Una descrizione libera del mercato** — l'utente descrive il mercato direttamente (es. "facility management", "baby food", "Medtech") — in questo caso salta lo Step 0

---

## Passo iniziale: fonti, metodo e anno (chiedi prima di tutto)

Prima dello Step 0 chiedi all'utente, in un solo messaggio, le scelte che cambiano come conduci l'analisi. Salta quelle a cui ha già risposto nella richiesta.

1. *"Prima di partire: hai documenti sul settore da caricare, da incorporare nell'analisi?"* → `Sì, ti carico dei documenti` · `No, nessun documento`
2. *"Da dove pesco i dati: solo Syrto (più i tuoi documenti), o anche dal web citando ogni fonte?"* → `Solo Syrto e miei documenti` · `Anche web, citando ogni fonte`
3. *"Come vuoi definire il perimetro del mercato?"* → `Ricerca semantica Syrto (per vera attività aziendale)` · `Codici ATECO`
4. **L'anno di riferimento**: opzioni e avvertenza sono in «Anno di Riferimento» (`references/perimeter.md`).

Regole conseguenti:

- Il **perimetro quantitativo** (conteggi, medie, size) viene **sempre e solo da Syrto**: è la fonte dei dati aziendali. Documenti caricati e web servono a definire meglio il mercato, i sotto-mercati e il commento — **non** a sostituire o correggere i numeri Syrto.
- Se ci sono **documenti caricati**, leggili e sintetizzali *prima* di proporre la definizione di mercato (Step 0/1): possono suggerire i confini del settore, i segmenti e i termini giusti per i testi di ricerca.
- Se l'utente sceglie **"Solo Syrto e miei documenti"**, **non fare alcuna ricerca web**, nemmeno per identificare il mercato di un'azienda allo Step 0.
- Se sceglie **"Anche web"**, ogni affermazione presa dal web deve avere una **citazione con link inline**; non riportare mai un dato dal web senza fonte verificabile.
- **Semantico** → è il percorso completo di questa skill (dallo Step 0 in poi): definizione del mercato, atomicità, calibrazione della soglia, perimetro unico. Trova le aziende per quello che *fanno davvero*, oltre i limiti degli ATECO.
- **ATECO** → vai al **Percorso ATECO** (in `references/perimeter.md`) e salta gli Step 0–5: atomicità, calibrazione e overlap non si applicano (l'ATECO è un filtro netto, senza soglia).

### Quando ti chiama un'altra skill

Se questa skill è chiamata da un'altra (per esempio `company-analysis` quando serve il mercato di un'azienda), usa le scelte che la catena ha già fatto (anno, fonti, metodo) e chiedi solo quelle che mancano. I checkpoint restano. Restituisci la modalità eseguita, i testi di ricerca, le soglie calibrate, i conteggi e gli aggregati: non ripresentare l'intero output.

---

## Workflow ad alto livello

Sotto ci sono i nomi degli step e cosa fanno; il **dettaglio operativo completo** (criteri, esempi, testi dei checkpoint, layout di output) vive nei file `references/`, da leggere al momento indicato.

**Metodo ATECO (alternativa al semantico).** Se l'utente sceglie ATECO, non si applicano atomicità, calibrazione e overlap: leggi il **Percorso ATECO** in `references/perimeter.md` e seguilo, poi produci l'output col formato Modalità A (`references/output.md`).

**Percorso semantico:**

1. **Step 0 — Identificazione del Mercato** (solo se l'input è un'azienda): risolvi l'azienda su Syrto, leggi la descrizione dell'attività dal suo profilo, proponi un mercato e fatti confermare.
2. **Step 1 — Atomicità**: valuta se il mercato è atomico (Modalità A, singola search) o ampio (Modalità B, decomposizione), con il **test di copertura** (nomina 3-5 aziende reali). In Modalità A lo step si chiude con il **Checkpoint 1**.
3. **Step 2 — Decomposizione** (solo Modalità B): scomponi in 3-6 sotto-mercati, ciascuno con un testo di ricerca in inglese, e fai il check di copertura. Lo step si chiude con il **Checkpoint 1**.

→ **Prima delle domande iniziali e degli Step 0–2, leggi `references/perimeter.md`** (anno di riferimento, criteri di atomicità, regole per i testi di ricerca, esempi Medtech/Baby food, testi del Checkpoint 1).

4. **Step 3 — Calibrazione delle soglie** (entrambe le modalità): per ogni search trova la soglia più bassa che tiene ≥ 15/20 aziende pertinenti al confine, con rubrica IN/OUT binaria e registro per azienda, poi un solo conteggio aggregato alla soglia scelta. È il cuore della ripetibilità. Lo step si chiude con il **Checkpoint 2**.
5. **Step 4 — Aggregati finali**: riusa il conteggio dello Step 3 (uno per ricerca); nessun conteggio su anni precedenti.
6. **Step 5 — Perimetro unico** (solo Modalità B): conta l'unione dei sotto-mercati in un solo aggregato quando il loro numero rientra nel limite della ricerca semantica; oltre quel limite, stima l'overlap a campione (50 aziende per sotto-mercato) ed etichetta il risultato come approssimato. Le size per sotto-mercato restano esatte.

→ **Prima di calibrare (Step 3), leggi `references/calibration.md`** (come funziona la ricerca semantica, il test a soglia `c`, la rubrica IN/OUT, l'algoritmo a griglia deterministico, gli esempi, il Checkpoint 2, gli aggregati e il perimetro unico dello Step 5).

7. **Step 7 — Output finale**: la nota **Metodo** in cima, poi l'output nel formato della modalità eseguita.

→ **Prima di costruire l'output, leggi `references/output.md`** (nota Metodo, layout tabellare Modalità A e B, aziende campione, regole di formattazione).

## Note Importanti

- La **semantic search è il cuore** di questa skill. Trova aziende per quello che fanno realmente, bypassando i limiti degli Ateco. Questo è un differenziale chiave di Syrto.
- La **scelta della modalità** (atomica vs decomposta) è la prima decisione operativa. Sbagliare modalità significa o introdurre rumore artificiale (decomposizione di un mercato già stretto) o perdere granularità (singola search su un mercato cross-categoria). Il test di copertura allo Step 1 è il filtro principale.
- Il **ciclo di calibrazione** (trova la soglia minima che produce ≥15/20 fitting al confine, con verdetti IN/OUT binari e registro per azienda) è il meccanismo che garantisce qualità, ampiezza e ripetibilità del perimetro. Non saltarlo mai, in nessuna modalità.
- La **decomposizione in sotto-mercati** è ciò che rende questa skill efficace per mercati ampi. La qualità dei testi di ricerca determina direttamente la qualità del perimetro.
- Chiudi ogni deliverable con la riga di fonte Syrto indicata nella capability map.

### Se la conversazione è andata avanti

Se in questa conversazione sono passati molti turni o hai svolto altri task (codice, layout, altre analisi) prima di arrivare a questa skill, rileggi `references/calibration.md` prima di calibrare. La memoria di un dettaglio operativo (algoritmo di calibrazione, modalità A vs B) decade rapidamente: meglio una rilettura di 30 secondi che un'esecuzione approssimativa.

---
_Fonte dati: Syrto Financial Intelligence_
