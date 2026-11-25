---
name: job-search-profile
description: >-
  Editor delle ricerche del sistema Job Hunter (cartella searches/ nel repo:
  defaults.yaml + un file per intento). Usa SEMPRE questa skill quando
  l'utente vuole modificare i criteri di ricerca lavoro DOPO l'onboarding,
  o gestire il ciclo di vita degli intenti (crea/pausa/archivia):
  "aggiorna il mio profilo di ricerca", "cambia i ruoli che
  cerco", "aggiungi/togli una location", "escludi gli stage", "non voglio
  più annunci in spagnolo", "alza/abbassa la seniority", "cambia i settori",
  "aggiorna le esclusioni" — anche per richieste parziali tipo "aggiungi
  Amsterdam" o "togli i ruoli manageriali" se il contesto è la ricerca
  lavoro. NON usare per l'onboarding iniziale né per creare il profilo da
  zero: quello è mestiere della skill agent-config. NON usare per il
  master-profile (esperienze, skill, certificazioni, retribuzione, vincoli):
  questa skill tocca solo i criteri di ricerca — per il profilo del candidato
  esiste la skill master-profile-editor.
---

# job-search-profile

Modulo 1.2 del progetto Job Hunter. Modifica le ricerche **già esistenti** nella cartella `searches/` del repo (D2: `defaults.yaml` condiviso + un file per intento), dopo l'onboarding. È un editor, non un creatore *ex novo del sistema*: la nascita del profilo (il primo intento) e lo schema canonico vivono in `agent-config` (1.1) — questa skill non li duplica. Ma dopo l'onboarding è QUI che si aggiungono/mettono in pausa/archiviano gli intenti successivi: creare un intento in più NON è rifare l'onboarding (riusa il `master-profile` esistente), quindi NON si reindirizza ad `agent-config` per quello.

## Precondizioni di readiness

A differenza delle altre skill dello Studio, qui il gate non è un singolo booleano — due casi distinti:

1. **Sistema vergine** (nessun `master-profile.yaml` valorizzato, `searches/` assente o con solo `defaults.yaml` scaffold): NON creare nulla qui. L'utente non ha ancora fatto l'onboarding. Fermati e reindirizza ad `agent-config` con una frase specifica al gap reale, non un generico "profilo non trovato", es.: "Per modificare i tuoi criteri di ricerca mi serve prima un profilo — non risulta ancora configurato: vuoi che partiamo dall'onboarding per crearlo adesso?". Un intento creato fuori dall'intervista di onboarding salterebbe le domande su vincoli/preferenze e nascerebbe monco.
2. **Master-profile presente ma nessun intento** (caso raro): NON è "sistema vergine" — non reindirizzare ad `agent-config`. Puoi creare qui il primo intento con la conversazione breve descritta in "Ciclo di vita degli intenti" (riusa il `master-profile` esistente, non rifà l'intervista completa).

## Cosa fa / cosa NON fa

- FA: legge `searches/` dal repo, applica modifiche puntuali richieste dall'utente (ruoli, location, seniority, esclusioni, settori, lingue annuncio, fonti, parametri esecuzione, anagrafica aziende in `searches/companies.yaml`), distinguendo se toccano i `defaults` condivisi o un singolo intento; gestisce il ciclo di vita degli intenti (crea, pausa, archivia); riscrive i file e committa.
- NON FA: creare il PRIMO profilo da zero quando `searches/` non esiste ancora e non c'è master-profile (se il sistema è vergine → redirect ad `agent-config`); modificare `master-profile.yaml` (chi è l'utente, non cosa cerca → `master-profile-editor`, 1.1.1); inventare campi fuori schema; rifare l'intervista di onboarding.

## Schema di riferimento (contratto)

Lo schema canonico è `search-profile.schema.yaml` dentro la skill `agent-config` (percorso in-repo `.claude/skills/agent-config/references/search-profile.schema.yaml`). Leggilo prima di modificare: definisce la struttura `defaults.yaml` + `searches/<intent-id>.yaml`, campi validi, enum e semantica. NON esiste una copia dello schema qui dentro — è voluto, per avere un'unica fonte di verità.

Se il file schema non è raggiungibile (installazione parziale del pacchetto skill): usa come contratto la struttura dei file `searches/` esistenti dell'utente (i campi che già contengono sono per costruzione conformi allo schema), segnala all'utente che lo schema canonico non è raggiungibile, e limita le modifiche ai campi già presenti — niente campi nuovi a schema non verificabile.

Un'istanza di esempio compilata (dati della prima istanza di test del progetto, nessun dato anagrafico) è in `references/example-search-profile.yaml`: mostra `defaults.yaml` + un intento. Usala per capire come si compila un campo, MAI come default da copiare nel profilo di un altro utente.

## Precondizioni tecniche

**Repo del sistema** — sei in una sessione Claude Code su un clone del repo (nessun `tool_search`: `searches/` è un file locale, non un connettore). Se stessi girando da chat claude.ai pura, il connettore GitHub è di sola lettura: potresti mostrare le modifiche ma NON scriverle — in quel caso dichiaralo e rimanda il salvataggio a una sessione Claude Code.

(Il gate su sistema vergine vs master-profile-senza-intento è in "Precondizioni di readiness" in testa al file — qui resta solo il prerequisito tecnico dell'ambiente.)

## Flusso

### 1. Leggi lo stato attuale e risolvi l'intento bersaglio

Leggi `searches/defaults.yaml` e i file `searches/<intent-id>.yaml`. Se uno YAML è corrotto/non parsabile: mostra all'utente il contenuto grezzo e l'errore, chiedi come procedere (correzione manuale guidata campo per campo, oppure ricreazione via `agent-config`) — NON riscrivere silenziosamente un file che non riesci a leggere.

**Risolvi QUALE intento è il bersaglio** (D2 — passo cruciale che prima non esisteva):
- Un solo intento nel repo → è quello, ma dichiaralo ("modifico l'intento `data-engineering-eu`").
- Più intenti → se la richiesta non lo dice, CHIEDI su quale agire (mostra l'elenco per `nome`/`id`/`stato`). Non indovinare dal contenuto della modifica.
- Se la modifica riguarda un campo dei `defaults` (esclusioni, lingue_annuncio, parametri_esecuzione), vedi il passo 2: potrebbe non essere un intento ma il file condiviso.

### 2. Interpreta la richiesta → defaults o intento, e campi target

Prima distingui **dove** vive il campo, poi **cosa** cambiare. Campi in `defaults.yaml`: `esclusioni`, `lingue_annuncio`, `parametri_esecuzione`. Campi nell'intento: `ruoli_target`, `location_target`, `seniority`, `settori`, `fonti`, `stato`.

Per i campi che vivono nei `defaults`, la modifica è ambigua di natura: **chiedi se vale per tutti gli intenti o solo per questo**. Es. "non voglio più annunci in spagnolo" → modifico `defaults.lingue_annuncio` (vale ovunque) oppure aggiungo un `override.lingue_annuncio` nel solo intento corrente? La distinzione è reale, non pedante: cambia il comportamento della routine su TUTTI gli altri intenti.

Esempi di mappatura:

- "aggiungi Amsterdam" → `location_target` dell'intento risolto (nuova voce: chiedi anche `accetta_remoto`/`accetta_ibrido`/`priorita`, non inventarli)
- "togli i ruoli manageriali" → `esclusioni.titoli_da_escludere` — chiedi: nei `defaults` (tutti) o `override` di questo intento?
- "non voglio più annunci in spagnolo" → `lingue_annuncio` — stessa domanda defaults vs override (chiedi anche: escluso se prevalente, se obbligatorio, o entrambi?)
- "cerca anche Data Platform Engineer" → `ruoli_target` dell'intento (nuovo titolo o sinonimo di uno esistente? Chiedi se ambiguo)
- "non voglio più annunci per junior" / "abbassa la seniority" → `seniority.livello` + `anni_esperienza_*` dell'intento. Ricorda che `livello` (`medio`/`senior`/`lead`) attiva il **filtro di scarto** della routine sui marcatori di sotto-livello nel titolo (job-watch passo 4).
- "i ruoli junior verso l'architettura però vanno bene" / "fai passare i Junior Architect" → `seniority.ruoli_ammessi_sotto_livello` dell'intento (lista di token di ruolo — es. `[architect, "tech lead"]` — per cui un "junior" nel titolo NON scarta). Chiedi quali ruoli, non dedurli.
- "non voglio più il settore X" → attenzione, **due campi diversi con lo stesso nome**: `settori.esclusi` dell'intento **filtra** (gli annunci di quel settore spariscono dalla raccolta), mentre `master-profile.preferenze_generali.settori_da_evitare` **pesa** solo nel giudizio di `role-fit`. Se l'utente vuole smettere di *vederli* → intento (mestiere di questa skill). Se vuole solo che il settore conti come segnale negativo continuando a riceverli → è il master-profile, che questa skill NON tocca: reindirizza a `master-profile-editor` (1.1.1). Se la richiesta è ambigua, chiedi quale dei due effetti vuole — non sceglierlo tu.
- "alza il cap ad annunci più recenti" → `parametri_esecuzione` — defaults vs override
- "aggiungimi Generali tra le aziende che seguo" → `searches/companies.yaml` —
  esegui SEMPRE il runbook di probe (references/company-probe-runbook.md):
  discovery del careers vero (chiedi QUALE entità se è un gruppo),
  classificazione A/B/C, verifica robots, compila la voce con adapter e
  `robots_ok: si` SOLO se la verifica è stata fatta davvero in questa
  conversazione. Mostra la classificazione ottenuta nel diff prima di
  scrivere. Se l'esito è C, dillo: la routine non la leggerà, resterà
  tracciata e candidabile via link diretto. Non esiste una scorciatoia "salta
  la probe": se per qualunque motivo non riesci a completarla (tool non
  disponibili, sito non raggiungibile), scrivi comunque la voce ma con
  `robots_ok: da_verificare` — MAI `si` senza verifica reale — e dillo
  all'utente esplicitamente ("non sono riuscito a verificare X, l'azienda
  resta tracciata ma non verrà interrogata finché non la riverifico"). Per
  tier A/B, il runbook include anche lo sblocco del dominio (Passo 6-bis) —
  **in due posti diversi**: `sandbox.network.allowedDomains` in
  `.claude/settings.json` per il sandbox Bash locale (questo lo scrivi tu),
  e Network access → Allowed domains nell'ambiente della Routine su
  claude.ai/code/routines per la routine cloud (**questo NON lo puoi
  scrivere tu**: dillo esplicitamente all'utente come passo manuale suo).
  Senza entrambi l'azienda risulta attiva ma la routine cloud la trova
  bloccata al primo run (incidente reale del 2026-07-12).
- "togli/sospendi Generali" → `attiva: false` nella voce (congela, non
  cancella — stessa semantica di stato:pausa).

Se la richiesta è vaga ("migliora il profilo", "sistemalo"): mostra i valori attuali raggruppati (defaults + intento/i) e chiedi cosa cambiare — non proporre modifiche di tua iniziativa.

Se la richiesta non ha posto nello schema (es. "escludi le aziende sotto i 50 dipendenti" — non esiste un campo per dimensione azienda): dillo esplicitamente, NON forzare il dato in un campo affine e NON inventare un campo nuovo. Un campo nuovo è un'evoluzione dello schema, che si decide a livello di progetto, non dentro una modifica.

### 3. Mostra il diff, poi conferma

Prima di scrivere, mostra SEMPRE un confronto prima/dopo dei soli campi toccati (non l'intero file, salvo richiesta), indicando in quale file atterrano (`defaults.yaml` o quale intento). Puoi appoggiarti al **diff git reale** (`git diff` dopo aver scritto in locale, prima del commit) invece di un confronto simulato — è più affidabile. Le modifiche multiple in un'unica richiesta si raggruppano in un solo diff e una sola conferma. Aspetta conferma esplicita.

### 4. Riscrivi i file nel repo + commit

Riscrivi SOLO i file interessati (`searches/defaults.yaml` e/o `searches/<intent-id>.yaml`) completi, preservando INTATTI tutti i campi non toccati. Confronta il file in uscita con quello in entrata: l'unica differenza devono essere i campi confermati al passo 3. Poi **committa** tu (D7 — l'utente non tocca git), con messaggio chiaro (es. `search: <intent-id> — aggiunta location Amsterdam`).

Se la scrittura/commit fallisce: mostra in chat lo YAML completo aggiornato così l'utente non perde la modifica, spiega il problema e ritenta. (Se giri da chat claude.ai pura, il connettore GitHub è read-only: mostra la modifica e rimanda il salvataggio a una sessione Claude Code — vedi Precondizioni.)

### 5. Promemoria a valle (obbligatorio, non opzionale)

Dopo ogni scrittura riuscita, segnala le conseguenze a valle in base ai campi toccati. Ragiona **per intento**: gli alert sono per-intento, quindi un cambiamento va riallineato solo per gli alert di quell'intento (o per tutti, se hai toccato i `defaults`).

- `ruoli_target`, `location_target`, `seniority` modificati → **gli alert LinkedIn/Indeed dell'intento sono ora disallineati**: proponi di rigenerare le istruzioni con `job-alert-config` (1.2.1). Gli alert sono impostati a mano dietro login: nessun sistema li aggiorna da solo.
- `lingue_annuncio`, `esclusioni`, `parametri_esecuzione`, `fonti` modificati → nessuna azione manuale sugli alert: la routine li applica a valle alla prossima esecuzione (leggendo i file aggiornati dal repo).
- `stato` di un intento cambiato (pausa/archivio/riattivazione) → gli alert dell'intento congelato andrebbero eliminati sulle piattaforme (la routine smette di iterarlo, ma le email continuerebbero ad arrivare): proponi il riallineamento con `job-alert-config`.
- **Disciplina push**: la routine cloud vede solo lo stato committato *e pushato*. Dopo il commit, esegui tu il push (D7) — altrimenti la modifica resta invisibile alla routine fino al prossimo push.

## Ciclo di vita degli intenti (D2)

Oltre a modificare un intento esistente, questa skill ne gestisce la vita. NON è un onboarding: riusa il `master-profile` e i `defaults` che già esistono.

- **Creare un nuovo intento** ("voglio cercare anche ruoli di management in Italia"): conversazione BREVE, mirata ai soli campi dell'intento (`id` slug stabile, `nome`, `ruoli_target`, `location_target`, `seniority`, `settori`, `fonti`; `stato: attivo`, `creato` = oggi). Non richiedere di nuovo CV/vincoli/retribuzione: sono nel master-profile. Proponi un `id` e fallo confermare (è la chiave che viaggia in log/valutazioni/candidature). Scrivi `searches/<id>.yaml`, committa, poi proponi `job-alert-config` per i suoi alert. NON reindirizzare ad `agent-config`.
- **Mettere in pausa** ("sospendi la ricerca in Spagna"): `stato: pausa`. Congela, non cancella — la routine smette di iterarlo, il file resta. Proponi di eliminare i suoi alert sulle piattaforme.
- **Archiviare** ("non cerco più data engineer"): `stato: archiviato`. Come la pausa ma semanticamente definitivo; il file NON si cancella (storico, e l'`id` potrebbe comparire in log/candidature passate). Proponi di eliminare i suoi alert.
- **Riattivare**: `stato: attivo`, e proponi di ricreare gli alert.

## Coerenza con master-profile (avvisa, non bloccare)

Se una modifica contraddice quanto noto dal `master-profile` (es. aggiunge una location in un paese dove `diritto_al_lavoro` risulta `no` o `da_verificare`, o una lingua annuncio che l'utente non ha dichiarato di conoscere): segnala la tensione e chiedi conferma, ma se l'utente conferma procedi — il search-profile è suo, la skill avvisa, non decide. Non leggere il master-profile preventivamente a ogni modifica: solo quando il campo toccato ha una controparte lì (location↔diritto al lavoro/trasferimento, lingue annuncio↔lingue).

## Cosa NON fare

- Non inizializzare il sistema da zero (sistema vergine, nessun master-profile → `agent-config`). Creare un intento IN PIÙ su un sistema già onboardato invece è compito di questa skill (vedi Ciclo di vita).
- Non scrivere senza il diff + conferma del passo 3.
- Non riempire campi collaterali con default plausibili non richiesti (es. `priorita: media` su una location nuova senza averlo chiesto).
- Non usare la memoria dell'account per decidere i valori: i valori li dà l'utente attivo, la skill deve funzionare identica per un utente di cui non sai nulla.
- Non rilanciare l'intervista completa di onboarding per una modifica puntuale.
