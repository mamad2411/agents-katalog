---
name: application-tracker
description: >-
  Tracker delle candidature del sistema Job Hunter, repo-first (cartella
  applications/ nel repo: 1 candidatura = 1 sottocartella <id>/ con
  application.yaml + events.jsonl). Usa SEMPRE questa skill quando l'utente
  vuole: aggiungere o promuovere una candidatura ("aggiungi al tracker",
  "mi sono candidato a X", "promuovi questo annuncio"), aggiornare uno stato
  ("ho fatto il colloquio", "mi hanno rifiutato", "ho ritirato la
  candidatura"), controllare le risposte ("ci sono novità sulle
  candidature?", "guarda se mi hanno risposto"), preparare un follow-up
  ("prepara il follow-up per X", "cosa c'è in sospeso?"), chiudere le
  candidature ferme ("chiudiamo le candidature ferme", "pulizia del
  tracker"), o vedere la pipeline ("a che punto sono
  le candidature"). Usala ANCHE per la revisione in blocco della coda di
  staging ("fammi rivedere le offerte in coda", "triage dello staging",
  "rivediamo le pending in blocco", "smaltiamo il backlog dello staging",
  "mostrami le offerte in attesa di revisione"): presenta le voci pending
  in lotti ordinati per score e raccoglie decisioni rapide di scarto o
  promozione. NON usare per la gestione produttività generale
  (backlog, roadmap, task personali): questa skill tocca SOLO la cartella
  applications/ del sistema Job Hunter.
---

# application-tracker

Modulo 2.3 del progetto Job Hunter: lo stato-workflow delle candidature vive qui, **nel repo**, sotto `applications/` (D8 — repo-first). È l'unica fonte di verità per "a che punto è" una candidatura (il `role-fit-output` in `role-fit/` si ferma a `promosso_a_tracker`, per costruzione). Due principi sopra tutto:

1. **Nessuna candidatura nasce da sola**: la promozione dal digest/valutazione al tracker è SEMPRE un'azione esplicita dell'utente (decisione fissa del progetto). La routine NON scrive in `applications/` (la legge soltanto, per le scadenze del digest) — **con una sola eccezione delimitata**: `scripts/sync_todoist.py` ci scrive per rispecchiare 1:1 lo spostamento di una card che l'utente ha fatto a mano su Todoist (vedi «Dal sync Todoist» più sotto). Anche lì la decisione è umana: cambia solo dove l'utente l'ha espressa. Questa skill, comunque, non crea candidature "per completezza".
2. **Nessun cambio di stato silenzioso**: ogni modifica derivata da una email va mostrata (email + azione proposta) e confermata prima di toccare i file.

**Dove giri conta (D5, D7)**: la scrittura richiede una sessione Claude Code (file locali + commit). Da chat claude.ai pura il connettore GitHub è di sola lettura: puoi leggere e proporre, ma NON persistere — dichiaralo e rimanda la scrittura a una sessione Claude Code. Ogni mutazione la committi TU: l'utente non tocca mai git.

## Precondizioni di readiness

- **Profilo configurato (prerequisito minimo)**: esiste `master-profile.yaml` nella radice del repo ed è non vuoto. Se manca, l'utente non ha ancora fatto l'onboarding: non procedere e non iniziare a tracciare candidature su un sistema non inizializzato. Fermati e reindirizza ad `agent-config` con una frase specifica al gap reale, es.: "Prima di tracciare le candidature conviene configurare il tuo profilo, che non risulta ancora presente: vuoi che partiamo dall'onboarding adesso?". **Nota**: la cartella `applications/` NON è un prerequisito — la crea questa skill stessa alla prima promozione, quindi la sua assenza non è un gap da reindirizzare; il prerequisito è il profilo.
- **Repo del sistema** clonato, sessione Claude Code (nessun `tool_search`: `applications/` è filesystem locale).
- **Gmail** — `tool_search` query "Gmail": serve per il controllo risposte e per le bozze di follow-up. Se manca, le funzioni di promozione/avanzamento manuale funzionano comunque; solo il pezzo email si ferma finché non è collegato.

## Contratto di storage: `applications/<id>/`

```text
applications/
  <id>/                    # il nome della cartella È l'id (data inclusa)
    application.yaml       # solo STATO CORRENTE (snapshot)
    events.jsonl           # solo STORIA (append-only)
    jd.md                  # la JD CONGELATA al momento della promozione
    materials/             # CV/cover/DM prodotti da cv-tailoring (2.2)
      cv.md  cover-letter.md  recruiter-dm.md  (+ PDF renderizzati)
      diff-report.md       #   verifica di veridicità master↔generato (D3)
```

**Perché `jd.md` esiste.** L'annuncio online sparisce: fra tre mesi il link è
morto e con esso l'unica traccia di *contro cosa* ti sei candidato. Senza il
testo congelato si sa **che** una candidatura è stata rifiutata, ma non **con
quale CV** né **contro quale annuncio** — e nessuna analisi a posteriori
(cosa converte, cosa no) diventa più possibile. Lo staging non lo salva: porta
solo `links.jd`, e la retention lo pota comunque. La promozione è **l'ultimo
momento utile** per catturarlo.

**Regola sull'id**: include la data (es. `acme-data-engineer-2026-07`) per evitare collisioni su ricandidature stessa azienda+ruolo. La cartella e il campo `id` in `application.yaml` coincidono sempre.

**Invariante snapshot/storico** (non violarlo mai): `application.yaml` è solo lo stato corrente; `events.jsonl` è solo la storia. Ogni mutazione **appende l'evento E aggiorna lo YAML nello stesso commit**. Lo YAML NON replica i campi dell'ultimo evento (niente "ultimo aggiornamento: ..." copiato dall'evento — si legge da `events.jsonl`).

### `application.yaml` (snapshot)

- `id` — coincide col nome cartella.
- `company`, `role`.
- `status: da_candidare | candidata | in_corso | offerta | chiusa` — è il funnel (i vecchi stati-sezione).
- `outcome: null | rifiuto | ritiro | accettata | nessuna_risposta` — valorizzato **se e solo se** `status: chiusa`. `nessuna_risposta` = chiusa dall'utente dopo un silenzio prolungato (vedi «Follow-up»): non è un `rifiuto` (nessuno l'ha comunicato) né un `ritiro` (l'utente non ha rinunciato a un processo vivo). Tenerli distinti è ciò che permette di misurare a posteriori quante candidature cadono nel vuoto.
- `source: indeed | linkedin_alert | indeed_alert | manuale` — enum unico
  condiviso con lo `staging.yaml` (`job-watch`) e il `sorgente` del `role-fit`.
  **Il valore è copiato 1:1** dallo staging/role-fit alla promozione: mai
  reinterpretato, rimappato o normalizzato dall'agente (es. `linkedin_alert`
  resta `linkedin_alert`, non diventa `linkedin`). Per una candidatura nata in
  chat senza staging/role-fit, `manuale`.
- `intent_id` — l'intento (D2) da cui viene la candidatura; ereditato dal role-fit se promossa da lì, altrimenti chiesto/`null`.
- `links` — `jd` (URL annuncio), `role_fit` (percorso relativo al file in `role-fit/`, se esiste).
- `next_action` — `{ type: follow_up | interview | reply | none, due: <YYYY-MM-DD | null> }`. È QUI che vive la scadenza, non negli eventi.
- `materials` — percorsi relativi ai file in `materials/` (popolato da cv-tailoring).

### `events.jsonl` (storia, append-only)

Un oggetto JSON per riga. Chiavi minime: `date` (YYYY-MM-DD), `type`, `note`. Chiavi aggiuntive per tipo sono ammesse senza rompere nulla (stessa proprietà che ha fatto scegliere JSONL in D6). Tipi:

- `created` — candidatura creata nel tracker.
- `applied` — candidatura inviata.
- `status_change` — con `from`/`to`.
- `email_processed` — con `gmail_message_id` e `classificazione`. **È il dedup email**.
- `follow_up_sent` — follow-up inviato (l'evento si scrive quando il follow-up è INVIATO; la *scadenza* del follow-up è `next_action` nello snapshot, non un evento).
- `interview` — colloquio (data/esito).
- `closed` — con `outcome`.
- `note` — annotazione libera.

Il log si APPENDE, mai riscrive.

**Ogni transizione porta quando e perché (requisito per l'analisi a posteriori).**
`events.jsonl` è già il ledger delle transizioni: `status_change` con `from`/`to`
esiste, `date` esiste. Due precisazioni che lo rendono davvero analizzabile:

- **`at` (ISO 8601 UTC) — raccomandato su ogni nuovo evento**, accanto a `date`
  (che resta obbligatorio e invariato: nessuna rottura per gli eventi già
  scritti). `date` ha granularità giornaliera e non ordina due transizioni dello
  stesso giorno — che è precisamente il caso di una giornata movimentata
  (risposta la mattina, colloquio fissato il pomeriggio). Senza `at` i tempi di
  funnel si calcolano male e nessuno se ne accorge.
- **La causa non è opzionale.** Ogni `status_change` dichiara *perché*: `note`
  in linguaggio naturale, più — quando l'origine è un'email — il
  `gmail_message_id` che l'ha provocata. Uno stato che cambia senza una causa
  registrata è un buco nella storia: fra sei mesi non si distingue un rifiuto
  ricevuto da un ritiro deciso.

Esempio di transizione ben formata:

```json
{"date":"2026-07-20","at":"2026-07-20T14:32:05Z","type":"status_change","from":"candidata","to":"in_corso","note":"invito a colloquio tecnico ricevuto via email","gmail_message_id":"18f…"}
```

Non è una migrazione: gli eventi vecchi restano validi senza `at`. Chi legge
tratta `at` come opzionale e ricade su `date` quando manca.

**Righe malformate (robustezza di lettura)**: come per il source-log del tuner,
una riga non parsabile (JSON rotto, chiavi minime mancanti) non deve MAI far
fallire la lettura né essere "corretta" riscrivendo il file — il JSONL è scelto
apposta perché una riga rotta non comprometta le altre. Scartala dal parsing,
segnala all'utente che la storia della candidatura è incompleta ("N righe
malformate in `events.jsonl` di <id>"), e tratta le decisioni che dipendono da
quella storia come prese su dati parziali. Caso delicato: se la riga rotta
potrebbe essere un evento `email_processed` (il dedup email), NON assumere che
l'email non sia mai stata processata — in ambiguità mostra l'email e chiedi
prima di agire: riprocessare un `rejection` già gestito è esattamente il danno
che il dedup esiste per evitare.

## Promozione di una candidatura (manuale)

Su richiesta esplicita ("aggiungila al tracker", "mi sono candidato a X", "promuovi questa dallo staging"). Tre punti d'ingresso — i primi due li esegui tu in sessione, il terzo è meccanico e arriva dalla routine:

- **Da chat** (una JD/valutazione in corso): raccogli i dati come sotto.
- **Dallo staging** (D4 — l'utente approva una voce che la routine `job-watch` ha pre-lavorato): la voce `staging/<id>/` porta già `staging.yaml` + `fit.yaml` + eventuali `materials/`. Promuovere = crea `applications/<id>/` (stesso `id`), **archivia** materiali e JD (vedi «Archiviazione alla promozione» qui sotto), **persisti** `fit.yaml` in `role-fit/` e mettine il percorso in `links.role_fit`, eredita `intent_id`/`links.jd`/`source`. Poi rimuovi (o marca `approved` e archivia) la voce staging: è uscita dall'anticamera. Lo scarto di una voce staging non crea nulla (`status: discarded`; l'annuncio resta in `state.json` così non rientra). Vedi `job-watch/references/staging-schema.md`.

- **Dal sync Todoist** (seconda via d'ingresso, meccanica): l'utente sposta una
  card dalla board Todoist in «Da candidare» e `scripts/sync_todoist.py` (passo
  6-bis di `job-watch`) esegue la promozione al posto tuo, nella run successiva.
  **Non è una promozione automatica**: la decisione resta umana (D3), lo script
  la rispecchia e basta. Quello che produce è **volutamente parziale**, e lo
  dichiara nei file che scrive:
  - `applications/<id>/application.yaml` con `status: da_candidare`, `source`
    copiato 1:1, `links.role_fit: null`, `next_action: {type: none, due: null}`
    (nessun follow-up deciso al posto dell'utente);
  - `jd.md` con `completezza: non_disponibile` — lo script non ha il corpo
    dell'annuncio e non lo inventa;
  - `materials/` copiati da staging, se c'erano;
  - un evento `created` in `events.jsonl` con causa esplicita
    `"promosso via sync Todoist"` e il `todoist_task_id`;
  - la voce staging marcata **`approved` e NON rimossa**: il `fit.yaml` deve
    restare recuperabile, perché lo script non scrive `role-fit/` (fuori
    dall'eccezione D5).

  **Cosa resta a te**, quando l'utente ti chiede di completare (o quando vedi una
  voce `approved` ancora in staging): recuperare il testo della JD e aggiornare
  `completezza`, persistere il `fit.yaml` in `role-fit/` valorizzando
  `links.role_fit`, proporre la `next_action` di follow-up, e solo allora
  rimuovere la voce da `staging/`. È l'«Archiviazione alla promozione» qui sotto,
  ripresa dal punto in cui lo script si è fermato.

### Archiviazione alla promozione (obbligatoria, non rimandabile)

È il passo che rende ricostruibile a posteriori cosa è stato davvero inviato.
Va fatto **prima** di rimuovere la voce da staging, e nell'ordine seguente —
copia, verifica, poi rimuovi: se qualcosa fallisce a metà non hai perso nulla.

1. **Materiali** — copia `staging/<id>/materials/` in
   `applications/<id>/materials/` (incluso `diff-report.md`), verifica che i
   file siano arrivati, e solo allora rimuovi l'originale da staging. Se la voce
   non ha materiali (fit `parziale`/`debole` promosso a mano), salta senza
   rumore: li genererà `cv-tailoring` quando servono.
2. **JD** — congela il testo dell'annuncio in `applications/<id>/jd.md`, con
   un'intestazione di provenienza:

   ```markdown
   ---
   fonte: linkedin_alert          # copiato da staging.yaml → source
   url: https://…                 # links.jd
   catturata_il: 2026-07-20
   completezza: completa | parziale | non_disponibile
   ---

   <testo dell'annuncio>
   ```

   Da dove prendere il testo, in quest'ordine:
   - **Indeed** → connettore `get_job_details` (testo completo);
   - **career page** → l'URL è fetchabile se il dominio è allowlistato;
   - **LinkedIn** → non fetchabile (V5): **chiedi all'utente di incollarlo**. È
     il momento giusto per farlo, perché sta candidandosi e ha l'annuncio aperto;
   - **annuncio già sparito** → `completezza: non_disponibile`, salva comunque
     `jd.md` con la sola intestazione più quello che è ricostruibile dal
     `fit.yaml`, dichiarandone la natura. **Non ricostruire il testo
     inventandolo**: una JD plausibile ma falsa è peggio di una mancante, perché
     nessuno la ri-metterà in discussione.

   Il campo `completezza` non è burocrazia: distingue un archivio affidabile da
   uno che *sembra* affidabile, e chi legge fra sei mesi non ha altro modo di
   saperlo.
3. **Solo dopo** rimuovi (o marca `approved`) la voce in staging.

1. **Raccogli il minimo**: ruolo, azienda, link JD, `source`, e `intent_id` se noto (da un `role-fit` in chat, o dallo `staging.yaml`, lo hai già, insieme al percorso del file role-fit da mettere in `links.role_fit`; se l'utente arriva dal digest, fatti dare il link).
2. **DEDUP PRIMA di creare** (obbligatorio): cerca tra le cartelle/`application.yaml` di `applications/` (attive E chiuse — sono tutte lì, la ricerca è semplice) per azienda e ruolo, con normalizzazione fuzzy: minuscolo, senza punteggiatura, senza suffissi societari (S.r.l., S.p.A., B.V., GmbH, Inc, Ltd, AB, SA), tolleranza per varianti di titolo ("BI Developer" ~ "Business Intelligence Developer"). Match probabile → mostra la candidatura esistente e chiedi: è la stessa (aggiorno quella) o una posizione diversa nella stessa azienda (creo una nuova `<id>`)? NON creare in caso di dubbio non risolto.
3. **Crea la candidatura**: costruisci l'`id` (`<azienda-slug>-<ruolo-slug>-<YYYY-MM>`), crea `applications/<id>/` con `application.yaml` (`status: da_candidare` se deve ancora inviare, `candidata` se ha già inviato — chiedi quale, non assumere) e `events.jsonl` con il primo evento `created` (+ `applied` se già inviata). Se esiste un role-fit per la posizione, mettine il percorso in `links.role_fit`. **Committa** (snapshot + eventi nello stesso commit).

   **Collisione legittima nello stesso mese (F17)**: l'`id` ha granularità mensile, quindi non distingue due candidature diverse per la stessa azienda+ruolo aperte nello stesso mese — caso reale: ricandidatura dopo un rifiuto, o due posizioni distinte con lo stesso titolo alla stessa azienda. Se al passo 2 il dedup fuzzy ha già escluso che sia la stessa candidatura (l'utente ha confermato che è un caso nuovo), non riusare l'id esistente: aggiungi un suffisso numerico progressivo (`-2`, `-3`, ...) o, se preferisci maggiore leggibilità nel contesto, la data (`-YYYY-MM-DD`). Verifica che l'id risultante non collida a sua volta prima di creare la cartella.
4. Ricorda (alla skill `role-fit`, o direttamente se il contesto è in chat) di aggiornare l'`esito` del role-fit a `promosso_a_tracker`.

## Triage in blocco della coda di staging

Serve quando le voci `pending` in `staging/` sono decine o centinaia: rivederle
una alla volta, ogni volta come una sessione a sé, è un lavoro che non si
esaurisce mai — e una coda che nessuno consuma smette di essere azionabile
(è il collo di bottiglia reale osservato su questa istanza). Questa modalità
**accelera la raccolta delle decisioni**, non le prende al posto dell'utente.

**Trigger**: "fammi rivedere le offerte in coda", "triage dello staging",
"rivediamo le pending in blocco", "smaltiamo il backlog dello staging",
"mostrami le offerte in attesa di revisione". Non serve che l'utente nomini la
skill: il segnale è l'intento di smaltire la coda.

### 1. Selezione e ordinamento

Leggi tutte le `staging/*/staging.yaml` con **`status: pending`** — escludi
`expired`, `discarded` e `approved`: sono già uscite dal flusso e riproporle è
esattamente il rumore che erode la fiducia nella coda. Escludi di default anche
le **`archiviata`** (non riviste entro 30 giorni, staging-schema 3f), ma dillo
con il loro conteggio e includile se l'utente lo chiede ("mostrami anche le
archiviate"). Una `archiviata` che l'utente vuole riprendere torna `pending`
(togli `archiviata_il`); una che vuole scartare va direttamente a `discarded`.

Ordina:
1. per **`score` decrescente**: `forte` > `buono` > `parziale` > `debole`
   (ordinale, mai numerico — vedi `role-fit`);
2. a parità di score, per **età decrescente** (la più vecchia prima), dove
   l'età è `oggi − il `fetched_at` più vecchio tra i `sources[]`` (campo già
   presente per sorgente nello `staging.yaml`; se manca del tutto, ricadi su
   `run_id`).

Le più vecchie prima a parità di score perché sono quelle con più probabilità
di puntare a un annuncio ormai chiuso: deciderle libera la coda dal materiale
che invecchia peggio.

**Il triage è l'unica uscita per le voci sotto la soglia Todoist.** Se la board
è attiva, il sync spinge solo i fit al di sopra di `todoist.push_score_minimo`
(`routine-config.yaml`, default `buono`): le voci con fit più basso non hanno
card, quindi nessuno le sposterà mai da telefono e restano `pending` qui finché
non passi di qui. Dillo quando presenti la coda, e non stupirti se il grosso
del backlog è proprio lì. Se l'utente ti chiede di **eliminarle davvero**
(niente `discarded`, nessuna traccia nelle viste), è la rimozione definitiva per
fit — 3e del contratto `job-watch/references/staging-schema.md`: cartelle
rimosse con `git rm -r`, `state.json.seen` **invariato** perché non tornino, e
— per le voci che una card ce l'avevano — card cancellata su Todoist *prima* di
togliere la voce da `todoist-sync-state.json`.

### 2. Presentazione in lotti

Presenta **~10-15 voci alla volta** (default; l'utente può dire "fammene vedere
20" o "5 per volta" — assecondalo, non è un numero rigido). Formato compatto,
una riga per voce, numerata **all'interno del lotto**:

```text
Lotto 1/7 — 99 pending totali

[1]  Senior Java Developer @ Acme S.p.A. — forte — career_page — 3 giorni
[2]  Backend Engineer @ Beta Srl — buono — indeed — 12 giorni
[3]  ⚠ Full Stack Developer @ Gamma — buono — linkedin_alert — 28 giorni
     (da verificare — JD non disponibile)
[4]  Software Engineer @ Delta — parziale — linkedin_alert — 40 giorni
```

- Se la voce ha **`confidenza: bassa`** (contratto in
  `job-watch/references/staging-schema.md`), prefissala con **⚠** e aggiungi
  "da verificare — JD non disponibile": quello score è orientativo, prodotto
  senza il corpo dell'annuncio, e non ha lo stesso peso degli altri. L'utente
  deve poterlo vedere **prima** di decidere, non dopo.
- Se la voce ha `materials_generated: true`, segnalalo ("📄 materiali pronti");
  se ha `materials_flagged: true`, aggiungi "⚠ materiali non verificati".
- Se ha `possible_duplicate_of`, dillo: è la revisione umana a sciogliere il
  dubbio che il matcher non ha voluto sciogliere da solo.

Niente riassunti lunghi nel lotto: se l'utente vuole approfondire una voce
("apri la 3", "che dice il fit della 7?"), mostrale il `fit.yaml` per intero e
poi torna al lotto.

### 3. Decisioni rapide

L'utente risponde con comandi brevi, riferiti ai numeri del lotto corrente:

| Comando | Effetto |
|---|---|
| "scarta 3,5,7" | `status: discarded` su quelle tre voci |
| "promuovi 2" | promozione completa della voce 2 (vedi sotto) |
| "salta il lotto" / "avanti" | passa al lotto successivo, nessuna decisione presa |
| "apri la 4" | mostra il `fit.yaml` completo, poi torna al lotto |
| "basta" / "fermiamoci" | chiudi il triage (vai al punto 4) |

**Nessuna semantica di stato nuova**: uno scarto da qui è identico a uno scarto
singolo (`status: discarded` in `staging.yaml`, l'`annuncio_id` resta in
`state.json` così l'offerta non rientra alle run successive, nessuna
candidatura creata). Una promozione da qui esegue **lo stesso identico flusso**
della sezione «Promozione di una candidatura» e della sezione «Archiviazione
alla promozione» — copia dei materiali → congelamento della JD in `jd.md` →
persistenza del `fit.yaml` in `role-fit/` → creazione di `applications/<id>/` →
solo dopo, rimozione (o `approved`) della voce staging. Il triage non
semplifica quel flusso e non ne salta i passi: se una promozione richiede
l'intervento dell'utente (es. incollare la JD LinkedIn, non fetchabile per V5),
chiedilo lì per lì — è il momento giusto, l'annuncio è davanti a lui.

**Terza uscita, solo se la chiede l'utente: l'azzeramento.** Se davanti al lotto
dice che quel blocco non lo revisionerà mai ("buttale via", "azzera le più
vecchie"), esiste un'opzione diversa dallo scarto: eliminare le voci da
`staging/` **e** i loro `annuncio_id` da `state.json.seen` (punto 3d del ciclo
di vita in `job-watch/references/staging-schema.md`). Non confonderla con lo
scarto e non proporla al posto suo: `discarded` registra un giudizio ("non mi
interessa") e impedisce all'offerta di rientrare; l'azzeramento non registra
alcun giudizio e fa esattamente il contrario — se l'annuncio è ancora aperto la
routine lo ritrova e lo rivaluta da zero. Prima di eseguirla dì quanto costa:
i `materials/` pre-generati di quelle voci spariscono (restano nella storia
git) e le voci ritrovate rispendono slot del cap.

**Limite invalicabile (D3)**: ogni scarto e ogni promozione resta una **scelta
umana esplicita per singola voce**. Non esistono azioni di gruppo cieche:
"scarta tutte le deboli" NON si esegue come tale — presenta le voci `debole`
in un lotto, l'utente le vede e conferma i numeri. La differenza non è
formale: scartare senza vedere è precisamente il modo in cui un'opportunità
sparisce in silenzio.

**Commit**: committa le decisioni **a fine lotto** (un commit per lotto, con il
conteggio nel messaggio), non a fine sessione: se il triage si interrompe a
metà, il lavoro già fatto è salvo.

### 4. Chiusura

A fine sessione di triage (lotti esauriti o "basta"), riporta:

- quante voci sono state **scartate** e quante **promosse**;
- **quante restano `pending`** dopo le decisioni prese — è il numero che dice
  se la coda si sta consumando o solo accumulando;
- se restano lotti non visti, dillo e proponi di riprendere ("ne restano 62,
  vuoi continuare o ci fermiamo qui?").

## Avanzamenti dichiarati dall'utente

"Ho inviato la candidatura", "ho il colloquio martedì", "mi hanno fatto un'offerta": aggiorna `status` nello snapshot, appendi l'evento `status_change` (o `applied`/`interview`), gestisci `next_action` (vedi follow-up), committa.

**Lo stesso avanzamento può arrivare da Todoist**: spostando la card in
«Candidatura inviata», l'utente porta la candidatura da `da_candidare` a
`candidata` e il sync appende lo `status_change` con causa esplicita e
`todoist_task_id` (mai su una candidatura in stato più avanzato o inesistente:
lì lo script logga e non tocca nulla). Quel passaggio NON imposta alcuna
`next_action`: se vedi una candidatura passata a `candidata` per questa via e
senza scadenza, è il momento di proporre il follow-up a +7 giorni. Le dichiarazioni dirette dell'utente non richiedono la conferma extra prevista per le email — è lui la fonte.

**Anche «Colloquio fissato» e «Rifiutata» arrivano da Todoist**, con la stessa
disciplina: spostando la card in «Colloquio fissato» (solo se porta una
scadenza — senza, lo script logga un'incongruenza e non tocca nulla) la
candidatura passa `candidata → in_corso` con `next_action = {type: interview,
due: <data della card>}` già valorizzato — qui non serve proporlo, è già lì.
Spostandola in «Rifiutata» (da `candidata`, `in_corso` o `offerta`) diventa
`chiusa` con `outcome: rifiuto`. In entrambi i casi l'evento porta
`todoist_task_id` e causa esplicita, e — come per «Candidatura inviata» — mai
su uno stato che non ammette quella transizione: lì lo script non tocca nulla
e la sistemi tu a mano (in chat o spostando di nuovo la card).

Chiusure dichiarate in chat: "mi hanno rifiutato" → `status: chiusa`, `outcome: rifiuto`, evento `closed`. "Lascio perdere / ritiro" → `outcome: ritiro`, idem. "Non mi hanno mai risposto, chiudila" → `outcome: nessuna_risposta`, idem (vedi «Candidature ferme»). "Ho accettato!" → `outcome: accettata`, e proponi di chiudere per ritiro le altre candidature ancora attive (proponi: la decisione è sua). **In ogni chiusura, azzera anche `next_action` a `{type: none, due: null}`**: un follow-up o un colloquio rimasti valorizzati comparirebbero come scadenza nella sezione 4 del digest (che legge `next_action.due` senza guardare `status`) su una candidatura che non è più attiva.

## Follow-up

### Giorni di silenzio (derivati dai dati, mai salvati)

Una candidatura può tacere anche senza che nessuno abbia impostato una
`next_action`: succede ogni volta che arriva a `candidata` per una via che non
propone il follow-up (sync Todoist, o una proposta rifiutata in chat). Per non
dipendere da quel campo, il silenzio si **calcola** dalla storia, a ogni lettura:

```text
SOGLIA_SILENZIO_GIORNI = 7     # stesso default del follow-up +7
SOGLIA_FERMA_GIORNI    = 60    # oltre: proporre la chiusura, non un altro sollecito
MAX_FOLLOW_UP          = 2
```

- **Si applica solo a** `status: candidata | in_corso` — cioè a candidature
  inviate e ancora aperte. `da_candidare` non è mai "in silenzio": non è stato
  inviato nulla, nessuno è in ritardo a rispondere.
- **Ultimo contatto** = la `date` più recente tra gli eventi `applied`,
  `status_change`, `follow_up_sent`, `interview`, `email_processed`; se non ce
  n'è nessuno, quella di `created`. Gli eventi `note` non contano: sono
  annotazioni dell'utente, non contatti con l'azienda.
- **Giorni di silenzio** = oggi − ultimo contatto.
- **Follow-up inviati** = numero di eventi `follow_up_sent`.
- Righe malformate in `events.jsonl`: scartale dal calcolo (vedi «Righe
  malformate») e dichiara che il dato è parziale.

È un **valore derivato**: non si scrive in `application.yaml` (violerebbe
l'invariante snapshot/storico) e non si persiste da nessuna parte. Chi lo mostra
lo ricalcola. Lo leggono questa skill (pipeline, «cosa c'è in sospeso?») e il
digest della routine (`job-watch/references/digest-schema.md`, sezione 4).

### Il ciclo

- Al passaggio in `candidata`: proponi `next_action = { type: follow_up, due: +7 giorni }` (default del progetto, dichiarato — l'utente può cambiarlo o rifiutarlo). Se la candidatura ci è arrivata via Todoist, la `next_action` è `none`: proponilo alla prima occasione in sessione — ma anche senza, il silenzio la farà emergere.
- **Quando proporre il follow-up**: `next_action.due` raggiunta, **oppure** giorni di silenzio ≥ `SOGLIA_SILENZIO_GIORNI` con `next_action.type: none` — e in entrambi i casi solo se i follow-up inviati sono meno di `MAX_FOLLOW_UP`. Su richiesta dell'utente ("prepara il follow-up per X", "cosa c'è in sospeso?") genera la bozza: DM breve (60-100 parole, cortese, un riferimento concreto alla candidatura, una domanda chiara sullo stato) o **bozza email in Gmail** (bozza, MAI invio diretto).
- **Nessuna affermazione nuova nel follow-up.** Ogni riferimento concreto viene da ciò che l'azienda ha già ricevuto — `applications/<id>/materials/` — o da `jd.md`, mai da altre parti del `master-profile`. Un sollecito che introduce competenze o risultati assenti dai materiali inviati è un canale di invenzione che nessun gate controlla.
- **Canale**: lo stesso della candidatura quando è noto (la `note` dell'evento `applied`/`status_change`, o il `source`: per `linkedin_alert` il DM al recruiter, per un form ATS una email al contatto se esiste). Se non è noto, chiedilo: non indovinare un destinatario.
- Dopo che il follow-up è inviato (lo dice l'utente): evento `follow_up_sent` (con `canale` e una `note` di una riga su cosa è stato chiesto) + proponi nuova `next_action` a +7/+10 giorni o `type: none`.
- **Tetto**: arrivati a `MAX_FOLLOW_UP` follow-up senza risposta, non proporne un terzo. Proponi invece la chiusura con `outcome: nessuna_risposta`, ricordando da quanti giorni tace — la decisione resta dell'utente.
- Colloquio fissato: `next_action = { type: interview, due: <data> }`, `status: in_corso`. Proponi la preparazione con `interview-prep` (prep pack dai materiali inviati + simulazione); dopo il colloquio, registra qui stadio e feedback con un evento `interview`: è l'input del prep successivo.

### Candidature ferme (chiusura in blocco, sempre confermata)

Su richiesta ("chiudiamo le candidature ferme", "pulizia del tracker") o quando
la pipeline mostra candidature oltre `SOGLIA_FERMA_GIORNI` di silenzio: presenta
la lista (azienda, ruolo, giorni di silenzio, follow-up inviati) e chiedi quali
chiudere come `nessuna_risposta` — tutte, alcune, nessuna. **Mai chiudere senza
conferma esplicita**, nemmeno in blocco: è la stessa regola del triage dello
staging (D3). Per ognuna confermata: `status: chiusa`, `outcome:
nessuna_risposta`, `next_action = {type: none, due: null}`, evento `closed` con
`from`, `outcome` e la causa ("nessuna risposta dopo N giorni e M follow-up,
chiusa dall'utente"), tutto nello stesso commit. Se arriva una risposta dopo, si
appende alla candidatura chiusa senza riaprirla (vedi «Casi limite»), come per
ogni chiusura.

Nota: la funzione-promemoria non è più delegata a notifiche di app terze. Le scadenze (`next_action.due`) vivono nello snapshot, il silenzio si deriva da `events.jsonl`; entrambi sono letti dal digest della routine e su richiesta in sessione — è l'unico canale che li fa emergere.

## Aggiornamento stato via email (il pezzo delicato)

SOLO su richiesta esplicita ("controlla le risposte", "novità?") — mai in autonomia.

1. **Recupero**: Gmail `search_threads` su una finestra recente (default: 7 giorni, dichiaralo; l'utente può allargarla). Cerca in modo mirato: per ogni candidatura attiva, query con nome azienda e/o ruolo; più una passata generica su mittenti tipici di ATS/recruiting se le candidature attive sono poche. Leggi i thread candidati con il contenuto completo, non gli snippet.
2. **Mappatura email → candidatura** (fuzzy, a livelli):
   - *Match forte*: dominio o nome del mittente riconducibile all'azienda della candidatura E il titolo del ruolo compare in subject/body → procedi con conferma leggera.
   - *Match medio*: solo l'azienda matcha, e c'è UNA sola candidatura attiva per quell'azienda → proponi l'associazione, chiedi conferma.
   - *Ambiguo*: l'azienda matcha ma ci sono PIÙ candidature per quell'azienda, oppure scrive un'agenzia/ATS il cui dominio non c'entra con l'azienda (caso frequente: `no-reply@ats-di-terzi.com`) → mostra l'email e chiedi a quale candidatura appartiene. Se l'utente la associa, annota l'associazione mittente→candidatura con un evento `note` (`{"type":"note","note":"mittente <x> = questa candidatura"}`): le email successive dello stesso thread/mittente matcheranno da sole.
   - *Nessun match*: segnalala come "email orfana" e chiedi se riguarda una candidatura fuori tracker — NON forzare l'associazione alla candidatura più simile.
3. **Dedup email** (obbligatorio, prima di ogni azione): ogni email processata si registra come evento `email_processed` in `events.jsonl` (`gmail_message_id` + classificazione + data). **`date` e `at` sono quelli dell'email, non del momento in cui la processi** (che va, se serve, in `processato_il`): l'evento conta come contatto nel calcolo dei «Giorni di silenzio», e un'email vecchia processata oggi azzererebbe il silenzio di una candidatura che in realtà tace da settimane. Prima di proporre un'azione, controlla gli eventi `email_processed` della candidatura: `gmail_message_id` già presente → salta senza dire nulla (non è una novità).
4. **Classificazione** in quattro classi: `ack` (conferma ricezione candidatura) · `rejection` · `invito_colloquio` · `ping` (richiesta info/disponibilità/documenti). In dubbio tra due classi, mostra l'email e chiedi — un falso rejection che chiude una candidatura è il danno peggiore che questa skill possa fare.
5. **Azione per classe** (sempre: proposta → conferma → esecuzione → evento + evento `email_processed` di dedup, nello stesso commit):
   - `ack` → evento `note`/`applied`; nessun cambio `status`.
   - `rejection` → proponi: `status: chiusa` + `outcome: rifiuto` + evento `closed`. Conferma esplicita SEMPRE, anche su match forte.
   - `invito_colloquio` → proponi: `status: in_corso` + `next_action = { type: interview, due: <data se presente nella mail; altrimenti chiedi> }` + eventuale bozza di risposta.
   - `ping` → mostra la richiesta e proponi una bozza di risposta (bozza Gmail, mai invio).
6. **Riepilogo finale**: cosa è stato aggiornato, cosa è in attesa di decisione, le orfane.

## Pipeline view (artefatto generato, mai fonte di verità)

Su richiesta ("a che punto sono le candidature", "mostrami la pipeline"): genera una **tabella funnel in chat** leggendo gli `application.yaml` (raggruppati per `status`, con `next_action.due` in evidenza e, per `candidata`/`in_corso`, i **giorni di silenzio** e i follow-up inviati calcolati come in «Follow-up»). Se una candidatura supera `SOGLIA_SILENZIO_GIORNI` senza `next_action`, o `SOGLIA_FERMA_GIORNI`, dillo sotto la tabella con la proposta corrispondente (follow-up o chiusura). Su richiesta o come parte del digest, rigenera anche `PIPELINE.md` nel repo e committalo: GitHub lo renderizza (anche da mobile) — è la vista-da-telefono senza app terze. `PIPELINE.md` è SEMPRE rigenerabile dagli snapshot: non scriverci nulla che non derivi da `applications/`. È un artefatto **co-scritto** con la routine `job-watch` (eccezione dichiarata alla regola di proprietà D5, innocua perché mai fonte di verità): chi lo tocca lo rigenera SEMPRE integralmente da `applications/`, mai con merge manuale; in conflitto vince la rigenerazione più recente.

## Casi limite

- **Due candidature stessa azienda**: sempre chiedere, mai indovinare dal solo mittente.
- **Email su candidatura già chiusa** (es. rejection dopo un ritiro): appendi l'evento alla candidatura chiusa senza riaprirla (`status` resta `chiusa`), e segnalalo all'utente.
- **Scrittura/commit fallito a metà operazione**: riporta cosa è stato scritto/committato e cosa no, così l'utente non resta con uno stato a metà senza saperlo. Se lo snapshot è stato aggiornato ma l'evento no (o viceversa), sistema per ripristinare l'invariante prima di considerare chiusa l'operazione.
- **Volumi**: se le candidature attive sono tante (>15), fai il controllo email per gruppi e dillo, invece di degradare la qualità del matching.

## Cosa NON fare

- Non creare candidature senza richiesta esplicita (né dalla routine, né "già che ci sono").
- Non chiudere/spostare candidature su base email senza conferma.
- Non inviare mai email: solo bozze.
- Non proporre un terzo follow-up, non mettere nel follow-up affermazioni assenti dai materiali inviati, e non chiudere per `nessuna_risposta` senza conferma.
- Non salvare i giorni di silenzio in `application.yaml`: sono derivati, si ricalcolano.
- Non toccare cartelle del repo diverse da `applications/` (e, in lettura, `role-fit/` per i link).
- Non riscrivere `events.jsonl`: solo append.
- Non far divergere snapshot e storico: ogni mutazione aggiorna entrambi nello stesso commit.
- Non rimuovere una voce da `staging/` prima di aver verificato che materiali e `jd.md` siano arrivati in `applications/<id>/`: l'ordine è copia → verifica → rimuovi.
- Non ricostruire una JD sparita inventandone il testo: `completezza: non_disponibile` è un esito onesto, una JD plausibile ma falsa no.
- Non cambiare stato senza registrare la causa nell'evento.
- Non processare due volte la stessa email (evento `email_processed` di dedup prima di tutto).
- Non eseguire scarti o promozioni "di gruppo" alla cieca nel triage in blocco
  ("scarta tutte le deboli"): l'utente vede le voci e conferma i numeri, sempre
  (D3 — la modalità accelera la raccolta delle decisioni, non le prende).
