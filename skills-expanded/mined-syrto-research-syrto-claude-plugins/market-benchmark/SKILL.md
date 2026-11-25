---
name: market-benchmark
description: >
  Benchmark a single Italian company (name or P.IVA) against the aggregate of its true peers,
  using Syrto. Derives one semantic search from the company's real business activity (beyond
  Ateco), calibrates a clean peer perimeter with the same boundary
  logic as market sizing, restricts peers to the company's size class, and shows the company's
  key metrics vs the peer averages (above/below), plus the number of peers and the aggregate
  value of the perimeter.
  Trigger on: "benchmark [azienda]", "come si posiziona [azienda]", "[azienda] vs settore",
  "[azienda] vs mercato", "benchmarking competitivo di [azienda]", "confronta [azienda] con il
  suo settore", "è sopra o sotto la media del settore", "benchmark [company] against its peers",
  "how does [company] compare to its sector".
  Not for: sizing a market/sector (use market-sizing), a named list of competitors (use
  syrto-comparables), a full single-company report (use company-analysis).
---

# Market Benchmark

Segui `${CLAUDE_PLUGIN_ROOT}/shared/core.md` (metodo, output, handoff) e la mappa delle capacità (`${CLAUDE_PLUGIN_ROOT}/shared/syrto-reference.md`: quale tool risponde a ogni capacità, e gli slug delle metriche). Se esiste un `SYRTO-HANDOFF` a monte, riusane id e dati prima di chiamare Syrto (core §8).

Questa skill posiziona **una singola azienda** contro l'**aggregato dei suoi veri peer** — le aziende che fanno davvero la stessa cosa, trovate per attività reale via ricerca semantica Syrto, non per codice ATECO. Restituisce le metriche dell'azienda affiancate alla **media dei peer** (sopra/sotto), il **numero di aziende** del perimetro e il **valore aggregato** dei peer di pari classe dimensionale.

Si differenzia da:

- **market-sizing**: quella dimensiona un mercato; questa confronta un'azienda con il suo.
- **syrto-comparables**: quella dà una *lista* di competitor nominati con confronto 1-a-1; questa dà l'**aggregato** (medie e mediane) di un perimetro calibrato. Se l'utente vuole anche i nomi, vedi "Peer nominati" allo Step 5.

> **Aggiorna l'utente passo passo.** Le chiamate a Syrto sono lente e la calibrazione ne fa diverse di fila, quindi senza aggiornamenti l'utente vede solo attesa. Prima di ogni fase (identificazione, anno di riferimento, ogni soglia testata con il suo esito, aggregato finale) scrivi una riga visibile: cosa stai per fare e perché. All'inizio dichiara il piano in una riga.

## Come si trova la similarità

La similarità si costruisce con la ricerca semantica sulla descrizione dell'attività dell'azienda (lo stesso principio di syrto-comparables). Quindi **derivo automaticamente** il testo di ricerca dalla descrizione dell'attività e calibro la soglia **senza fermarmi a farlo confermare** all'utente; il testo compare comunque nell'output, per trasparenza e riproducibilità.

---

## Input

Un'azienda: **nome** o **partita IVA**. Se l'utente non ha indicato un'azienda, chiedila prima di procedere.

Come nelle altre skill Syrto, all'inizio conviene chiedere se l'utente vuole che si peschi anche dal **web citando le fonti** (per il commento/contesto) o si lavori **solo su Syrto**. I numeri del benchmark vengono comunque sempre e solo da Syrto. Se ti chiama un'altra skill, usa la sua scelta e non chiedere di nuovo.

---

## Step 1 — Identifica l'azienda

Annuncia, poi:

1. Risolvi l'azienda per nome o P.IVA. La risoluzione restituisce anche la classe dimensionale e l'anno dell'ultimo bilancio a cui appartiene: quell'anno è l'**anno di riferimento** e quella classe è il filtro dei peer, così i due sono coerenti.
2. Leggi il profilo dell'azienda per la **descrizione dell'attività**.
3. Leggi l'analisi finanziaria dell'azienda (una chiamata) e tieni da parte le sue metriche: ti servono nel confronto allo Step 4.

La classe dimensionale arriva già come XS/S/M/L, lo stesso formato del filtro peer: nessuna conversione.

Se la descrizione dell'attività **manca** (capita con aziende piccole): se il web è abilitato, cerca il sito dell'azienda (nome + città/provincia dai dati Syrto), fallo confermare all'utente e leggilo per capire l'attività; altrimenti chiedi all'utente una breve descrizione dell'attività. Non proseguire senza sapere cosa fa l'azienda.

---

## Anno di Riferimento

Nessuna detection, nessuna chiamata di conteggio. L'**anno di riferimento** è l'ultimo anno di bilancio dell'azienda target, che hai già dallo Step 1. I bilanci su Syrto arrivano in ritardo e non tutte le aziende depositano nello stesso momento, ma l'ultimo anno del target è il riferimento naturale: è l'anno più recente per cui abbiamo il suo dato, quindi quello su cui ha senso confrontarla coi peer.

> Annuncia, es.: *"Uso come anno di riferimento il {Y}, l'ultimo bilancio disponibile per l'azienda target."*

La crescita nel tempo non richiede un anno storico separato: la leggi dal CAGR ricavi a 3 anni (già nel set di default), sia per l'azienda sia per l'aggregato peer.

---

## Step 2 — Deriva la query semantica (senza conferma)

Dalla descrizione dell'attività, scrivi **UN** testo di ricerca in inglese che descrive **cosa fa** l'azienda: attività, processi, prodotti/servizi, tecnologie, materiali. **10–25 parole**, in inglese, solo attività operative — **niente** clienti target ("for hospitals"), niente qualità/claim ("leading", "innovative"), niente etichette di categoria. Usa la stessa lingua per tutta la calibrazione: cambiare lingua cambia gli score e quindi la soglia. Non fermarti a farlo confermare: procedi alla calibrazione. (Il testo va comunque mostrato nell'output finale, per trasparenza e riproducibilità.)

---

## Step 3 — Calibra il perimetro dei peer (filtro taglia A MONTE)

Stesso motore di calibrazione di market-sizing, **una sola query**, con la classe dimensionale già nel filtro: così calibri e aggreghi direttamente sui peer di pari taglia. Il valore aggregato che ne esce è quello dei peer della stessa classe, non la dimensione del settore: per quella serve market-sizing.

> Annuncia, es.: *"Calibro la soglia sui peer di classe {M}: cerco la più bassa che tiene ≥15/20 aziende pertinenti al confine."*

**Filtri per ogni chiamata** (ricerca e aggregato): il testo semantico, la soglia di pertinenza `c`, la classe dimensionale dell'azienda e l'anno di riferimento (la classe è per anno, quindi l'anno serve sempre). Azienda e peer sulla stessa base di bilancio: di default i bilanci individuali; se l'azienda è letta sul consolidato, filtra anche i peer sui consolidati e dillo nella nota di metodo.

### Come funziona la search
Lo score di match è una proprietà fissa della coppia (testo, azienda): non dipende dalla soglia, che filtra soltanto. Quindi:

- **Confine per match crescente**: ordinando i risultati per score di match crescente con soglia `c`, la prima pagina della ricerca sono le aziende con score più basso ancora sopra `c`, cioè il confine; ogni risultato semantico porta già la descrizione breve e lo score.
- **Registro per id**: lo score è fisso, quindi il verdetto IN/OUT di un'azienda è fisso. Tieni un registro e non ri-giudicare due volte la stessa azienda.

### Il test a una soglia `c`
1. **Confine**: ricerca con i filtri sopra, ordinata per score crescente. Prendi le prime **20** aziende (o quante ce ne sono, se meno).
2. **Giudizio IN/OUT** su ciascuna con la rubrica sotto, riusando il registro.
3. **Esito**: **≥ 15/20 IN** → fitta; **< 15/20** → non fitta. Se al confine ci sono **meno di 20** aziende, applica la stessa soglia **in percentuale**: fitta se **≥ 75%** sono IN.

### Rubrica IN/OUT (binaria)
Un'azienda è **IN** solo se svolge come business primario **l'attività che definisce la verticale dell'azienda target**. È **OUT** se: fornisce alla filiera (fornitore, non operatore), è cliente, rivende/distribuisce soltanto (quando la verticale è produzione, e viceversa), è holding/immobiliare/generica, o fa un'attività adiacente ma diversa. **Prodotto vs servizio è una linea di taglio esplicita**: se la verticale è produzione di un bene, chi eroga il servizio collegato è OUT (e viceversa); nei casi dubbi leggi il profilo dell'azienda e usa l'ATECO (sez. C manifattura vs sez. servizi) come discriminante. Tieni un tally `nome → attività core → IN/OUT → motivo`.

### Algoritmo (griglia fissa, deterministico)
Parti da **0.80**; muoviti di **±0.02** finché l'esito cambia, poi **una** verifica a **−0.01**. Scegli il **cutoff più basso che rispetta 15/20** (o ≥75% su set piccoli).

- **0.80 fitta** → scendi 0.78, 0.76… finché non fitta più; poi verifica −0.01 tra l'ultima che fittava e la prima che no.
- **0.80 non fitta** → sali 0.82, 0.84… finché fitta; poi verifica −0.01.

**Limiti di sanità**: se devi scendere sotto ~0.78 o salire sopra ~0.90 senza mai fittare, la query è troppo larga o vaga → ricavane una più precisa dall'attività e riparti.

> Nota: l'azienda di solito rientra nel suo stesso perimetro, quindi è dentro le statistiche dei peer. Per la calibrazione è un peer come gli altri; nel confronto contala a parte (peer = N − 1). Su perimetri piccoli (sotto ~30 aziende) togli l'azienda dalla media: media peer = (media × n − valore azienda) / (n − 1), dove n è il numero di aziende con un valore per quella metrica, non il numero di aziende del perimetro. Mediana, minimo e massimo non si correggono così: dillo in una riga. Se non sei sicuro che l'azienda sia nel perimetro, una ricerca con gli stessi filtri ristretta alla sola azienda lo conferma.

---

## Fallback — pochi peer (solo se < 10)

Se, con la soglia ottimale e il filtro di classe dimensionale, i peer sono **meno di 10**, non allargare da solo: il modo di allargare cambia cosa stai confrontando, quindi decide l'utente. Fermati e chiedi con una scelta strutturata se il tuo client la offre, altrimenti con una domanda breve e numerata; aspetta la risposta prima di proseguire.

1. Di' all'utente che il perimetro è sottile e **per cosa hai cercato**: il testo semantico usato **e** la classe dimensionale del filtro. Se l'anno di riferimento è appena uscito, aggiungi che parte dei peer potrebbe non aver ancora depositato quell'anno.
2. Chiedi come procedere. Opzioni: **"Estendi"** (togliere o allargare il filtro taglia, es. includere le classi adiacenti, o allentare la soglia), **"Ti do un altro testo di ricerca"** (l'utente fornisce una descrizione alternativa), **"Usa ATECO"** (proponi tu i codici NACE più pertinenti e falli confermare), **"Va bene così"** (procedi coi pochi peer, segnalando la scarsa robustezza).

Applica questo controllo **solo** sotto le 10 aziende.

---

## Step 4 — Aggrega i peer e affianca l'azienda

> Annuncia la chiamata.

1. **Peer**: **una sola** aggregazione della popolazione con i filtri calibrati (testo semantico, soglia ottimale, classe dimensionale), per il **solo anno di riferimento**, con le metriche di default (sotto), chiedendo anche i **totali**. La crescita è già coperta dal CAGR ricavi 3 anni dentro il set: **non** fare una seconda aggregazione sull'anno − 3. Ottieni il numero di aziende e, per ogni metrica, media, mediana, minimo e massimo. Il **valore aggregato** del perimetro (fatturato totale, EBITDA totale) è il totale restituito dall'aggregazione, esatto. Non ricavarlo da numero di aziende × media: la media è calcolata solo sulle aziende che hanno quel dato, che possono essere meno del perimetro. Per margini e rapporti un totale non esiste.
2. **Azienda**: le sue metriche le hai già dall'analisi finanziaria dello Step 1 (stesso anno di riferimento) — riusale, non rifare la chiamata. Se ti serve una metrica non presente nell'analisi, leggi quella metrica per la sola azienda.

Su perimetri molto grandi (migliaia di aziende) la mediana è una stima campionaria che varia di qualche punto tra chiamate identiche: arrotondala.

### Metriche di default (adattabili su richiesta)
- Fatturato
- Crescita ricavi 3y (CAGR ricavi a 3 anni)
- EBITDA
- EBITDA margin
- ROE
- Solidità (Debt/EBITDA o PFN/EBITDA)

Gli slug sono nella mappa delle capacità: confermali con la ricerca nelle definizioni delle metriche prima di aggregare (per un concetto che la mappa non ha, cercalo lì), perché un'aggregazione con uno slug sconosciuto fallisce per intero.

Se l'utente vuole tagliare o estendere il set, assecondalo.

---

## Step 5 — Output

I blocchi qui sotto sono il **contenuto** del deliverable. Il rendering — formato, canone estetico, offerta del PDF, digest in chat — segue `${CLAUDE_PLUGIN_ROOT}/shared/core.md` (leggi le preferenze, core §3, sovrascrivibili da un template dell'utente). Non costruire un HTML con stile proprio.

Apri con una riga di contesto: azienda, testo semantico usato, soglia calibrata, classe dimensionale, anno di riferimento.

**Perimetro peer**
- **N. aziende** del perimetro (peer, esclusa l'azienda stessa se rientra nel perimetro).
- **Valore aggregato** (fatturato totale ed EBITDA totale del perimetro, dai totali dell'aggregazione).

**Benchmark azienda vs peer** — tabella:

| Metrica | Azienda | Media peer | Mediana peer | Posizione |
|:--------|-------:|-----------:|-------------:|:----------|
| Fatturato | … | … | … | sopra/sotto media; dove nel range min–max |
| CAGR ricavi 3y | … | … | … | … |
| EBITDA | … | … | … | … |
| EBITDA margin | … | … | … | … |
| ROE | … | … | … | … |
| Debt/EBITDA | … | … | … | … |

La **posizione** è qualitativa: sopra/sotto la media, sopra/sotto la mediana, e dove cade nell'intervallo min–max. **Niente percentili/quantili.**

Chiudi con un **verdetto di 1–2 righe** (dove l'azienda è forte/debole rispetto ai pari) e, se il web è abilitato, eventuale contesto con **fonti citate inline**.

**Peer nominati**: non fanno parte dell'output di default. Se l'utente li chiede, o fai una ricerca con gli stessi filtri calibrati (con un testo semantico i più vicini arrivano per primi), oppure indirizza alla skill **syrto-comparables** (che è pensata per quello, con confronto 1-a-1).

### Formattazione
I numeri seguono lo stile della casa di `core.md` §5. Dato mancante: "N/D".

---

## Nota di metodo (in fondo al deliverable)

Chiudi il deliverable con una breve nota **Metodo**, scritta per il lettore: fonti (solo Syrto oppure Syrto + web), testo semantico usato, soglia calibrata, classe dimensionale, anno di riferimento, base di bilancio, numero di peer, e se il fallback è scattato con la scelta dell'utente. Serve a rendere il perimetro riproducibile: se uno step non è stato eseguito, scrivilo con il motivo.

---

## Comunicazione e robustezza (vale per tutta l'esecuzione)

- Le ricerche semantiche possono essere **lente** o andare in **timeout/vuoto** per motivi transitori del backend, **non** perché il perimetro sia vuoto. Un timeout o una risposta vuota **non è un dato**: non registrarlo mai come "0 aziende" o "non fitta". **Ritenta la stessa chiamata** (idempotente), fino a ~3 volte; se persiste, fermati e dillo all'utente. Segnala in una riga quando ripeti una chiamata andata lenta.
- Chiamate una alla volta (core §6).
- Chiudi il deliverable con la riga di fonte indicata nella mappa delle capacità.

## Quando ti chiama un'altra skill

Se arrivi da company-analysis o da un'altra skill con un `SYRTO-HANDOFF`, riusa id, profilo e analisi dell'azienda, non rifare la domanda sul web e restituisci al chiamante i blocchi "Perimetro peer" e "Benchmark azienda vs peer" con la nota di metodo: rendering e file li gestisce lui.

## Posizionamento radar (facoltativo)

Se la domanda è *dove si colloca* l'azienda più che quali numeri fa, il radar di posizionamento la mette su dimensione × efficienza contro il suo perimetro, senza una ricerca preliminare (vedi la mappa delle capacità). Usalo quando il posizionamento è il punto, non come passo di routine.

---
_Fonte dati: Syrto Financial Intelligence_
