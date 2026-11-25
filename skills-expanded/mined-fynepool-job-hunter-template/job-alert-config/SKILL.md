---
name: job-alert-config
description: >-
  Genera le istruzioni passo-passo per impostare gli alert di lavoro su
  LinkedIn e Indeed a partire dagli intenti di ricerca del sistema Job Hunter
  (cartella searches/ nel repo). Usa SEMPRE questa skill quando: l'utente
  chiede "imposta gli alert", "come configuro gli
  alert LinkedIn/Indeed", "genera le ricerche salvate", "istruzioni per gli
  alert"; quando l'onboarding agent-config arriva al passo alert (passo 5);
  quando l'utente ha appena modificato il search-profile con
  job-search-profile e gli alert vanno riallineati. Produce istruzioni
  testuali da eseguire a mano (LinkedIn/Indeed sono dietro login: nessuna
  configurazione programmatica possibile) E scrive il registro degli alert
  (searches/alerts-registry.yaml) che rende gli annunci attribuibili alla
  ricerca giusta a valle. Imposta anche l'etichetta Gmail su cui la routine
  legge gli alert (creata via connettore o a mano, a scelta dell'utente) e
  guida la creazione del filtro Gmail che la applica — trigger anche su "crea
  l'etichetta Gmail", "come faccio ad etichettare gli alert".
---

# job-alert-config

Modulo 1.2.1 del progetto Job Hunter. Trasforma il `search-profile` in **istruzioni operative** per impostare gli alert su LinkedIn e Indeed. L'impostazione resta manuale per l'utente: è una delle tre eccezioni manuali strutturalmente non eliminabili del progetto (servizi terzi dietro login, nessuna API pubblica utilizzabile) — non tentare scorciatoie tipo fetch/automazione delle pagine LinkedIn, non funzionano e non sono previste.

## Precondizioni di readiness

Prima di derivare alert, verifica il prerequisito minimo di questa skill: la cartella `searches/` contiene almeno un intento con `stato: attivo`, e quell'intento ha `ruoli_target` e `location_target` non vuoti (senza almeno un ruolo e una location non c'è nulla da cui derivare un alert sensato). Se `searches/` non contiene alcun intento attivo utilizzabile, l'utente non ha ancora definito le sue ricerche via onboarding: non inventare parametri e non procedere. Fermati e reindirizza ad `agent-config` con una frase specifica al gap reale, es.: "Per impostarti gli alert mi serve almeno una ricerca attiva con ruoli e location, che non risulta ancora configurata: vuoi che partiamo dall'onboarding per definirla adesso?". (Distinzione importante: se un intento attivo esiste ma è quel singolo intento a essere incompleto, vale la regola già descritta in "Input" — salti quell'intento e lo dici, non fermi l'intero flusso; la guardia qui scatta solo quando NON c'è alcun intento attivo usabile.)

## Input

1. Leggi la cartella `searches/` dal repo: `defaults.yaml` + i file `searches/<intent-id>.yaml`. Sei in una sessione Claude Code (file locali, nessun `tool_search`: `searches/` non è un connettore). Se `searches/` non contiene alcun intento: non inventare parametri — spiega che serve prima l'onboarding (`agent-config`) e fermati.
2. **Deriva gli alert PER INTENTO, solo per gli intenti `attivo`** (D2). Gli intenti in `pausa`/`archiviato` si saltano (dillo). Per ogni intento, i valori effettivi sono quelli del suo file più i `defaults` ereditati (l'eventuale blocco `override` dell'intento sostituisce i defaults corrispondenti).
3. Campi usati per intento: `ruoli_target` (titoli + sinonimi), `location_target` (aree + priorità + remoto/ibrido), `seniority`, `fonti` (quali piattaforme sono attive), `parametri_esecuzione.finestra_temporale_ore` (per la frequenza alert, da defaults/override).
4. Se in un intento `attivo` `ruoli_target` o `location_target` sono vuoti: salta quell'intento e dillo — un alert senza ruolo o senza location non è configurabile sensatamente.

## Derivazione degli alert (algoritmo, applicato per ogni intento attivo)

1. **Base**: una combinazione ruolo × location = un potenziale alert. I `sinonimi` NON generano alert separati: entrano nella stessa query con OR dove la piattaforma lo consente (vedi `references/mappa-campi-piattaforme.md`), altrimenti si sceglie il solo `titolo_principale`.
2. **Priorità**: ordina per `location_target.priorita` (alta prima). Le location `accetta_remoto: true` generano anche la variante con filtro "Remoto" attivo dove la piattaforma la gestisce come filtro separato.
3. **Cap dichiarato, applicato PER INTENTO**: proponi al massimo ~8-10 alert per piattaforma *per ciascun intento*. Se le combinazioni di un intento superano il cap, mostra l'elenco completo ordinato per priorità e chiedi dove tagliare — non tagliare in silenzio. Troppi alert = digest rumoroso e email duplicate; il tuning a posteriori è mestiere di `job-alert-tuner` (1.2.2).
4. **Fonti disattive**: se in `fonti` di quell'intento una piattaforma è `attiva: false`, salta le sue istruzioni e dillo.
5. **URL pre-filtrato + chiave canonica — inversione del flusso**: invece di far impostare i filtri a mano (fonte di errori "l'utente ha messo un filtro diverso"), **costruisci tu l'URL di ricerca LinkedIn pre-filtrato** (`keywords` + `geoId` + eventuale `f_E`/`f_WT`) e chiedi all'utente solo di aprirlo, verificarlo e cliccare "Crea avviso". Così la **chiave canonica `<keywords-slug>:<geoId>` è nota PRIMA che l'alert esista** → il registro si scrive senza chiedere nulla. La tabella `area → geoId` è in `references/mappa-campi-piattaforme.md`. Il `ricerca_id` dell'alert è `<intent_id>:linkedin_alert:<keywords-slug>:<geoId>` (stessa chiave che la routine ricostruisce dal corpo email — vedi `job-watch/SKILL.md`, sezione «Attribuzione alert → ricerca», e `references/alerts-registry.schema.yaml`).

## Cosa gli alert NON possono fare (dichiaralo sempre all'utente)

Gli alert di LinkedIn/Indeed non applicano: esclusioni di titoli (Head of/Director/...), esclusioni di tipo contratto (stage), filtri di lingua del corpo annuncio, filtri su requisiti linguistici obbligatori. Questi filtri vengono applicati A VALLE dalla routine job-watch, che legge gli alert via Gmail e scarta secondo il `search-profile`. Dillo esplicitamente nelle istruzioni: l'utente NON deve aspettarsi alert già puliti, deve aspettarsi un digest già pulito.

## Vincoli critici di consegna (senza questi la routine è cieca)

Includi SEMPRE, in testa alle istruzioni, questi due punti:

1. **Consegna via email ATTIVA** verso la casella Gmail collegata al sistema: la routine legge gli alert da Gmail, cercando i quattro mittenti che LinkedIn e Indeed usano davvero — `jobs-noreply@linkedin.com`, `jobalerts-noreply@linkedin.com`, `alert@indeed.com`, `noreply@indeed.com` (stessa lista di `job-watch/SKILL.md`, sezione «Fonti dati»: se ne tocchi una, allinea l'altra). Un alert solo-notifica-app è invisibile al sistema.
2. **Frequenza giornaliera** (o la più frequente disponibile): la routine lavora su una finestra di `finestra_temporale_ore` ore (default 48) — alert settimanali arriverebbero già vecchi.

## Etichetta e filtro Gmail — scelta guidata (obbligatoria, prima della checklist)

Perché questo passo esiste: la routine `job-watch` restringe la query Gmail
all'etichetta dichiarata in `routine-config.yaml → gmail_label` (radice del
repo, F5). Se l'etichetta è **dichiarata ma non esiste** in Gmail, il controllo
di sanità della routine segnala un'**anomalia nel digest a ogni run**, per
sempre, finché l'etichetta non c'è. Nessun altro passo del sistema crea
l'etichetta né il filtro: se non li imposti qui, non li imposta nessuno.

Due oggetti distinti, non confonderli quando ne parli all'utente:
- **l'etichetta** — il contenitore. Creabile programmaticamente dal connettore
  Gmail (`create_label`).
- **il filtro** — la regola che applica l'etichetta alle mail future. **Il
  connettore Gmail non espone alcun tool sui Filtri**: resta manuale in
  entrambi i percorsi. Dichiaralo sempre, non promettere di automatizzarlo e
  non tentare workaround: è la stessa classe delle altre eccezioni manuali del
  progetto (alert LinkedIn/Indeed dietro login).

Dopo aver derivato gli alert degli intenti attivi e **prima** di produrre la
checklist finale, fermati e chiedi all'utente quale percorso vuole. Aspetta la
risposta esplicita: non scegliere un default al posto suo.

**Percorso A — automatica dove possibile** (l'etichetta la crei tu):
1. Leggi `routine-config.yaml`. Se esiste ed è valorizzato, il nome da usare è
   il suo `gmail_label`. Se il file manca o il campo è vuoto, proponi
   `Job Hunter`, fai confermare il nome e **allinea `routine-config.yaml` nella
   stessa sessione** (scrivendolo se manca): è l'unica copia versionata del
   valore, e la routine legge quella, non Gmail.
2. Verifica con `list_labels` che un'etichetta con quel nome non esista già —
   se c'è, dillo e passa direttamente al filtro, non ricrearla.
3. Chiama `create_label` con quel nome esatto.
4. Opzionale, se l'utente lo vuole: etichetta retroattivamente gli alert già
   arrivati (`search_threads` sui quattro mittenti + `label_thread`). È
   l'equivalente della casella "applica anche alle conversazioni esistenti" del
   filtro (punto 6 delle istruzioni sotto): se l'utente spunta quella, questo
   non serve.
5. Guida l'utente **solo sul filtro** (istruzioni sotto): l'etichetta appena
   creata compare già pronta nel menu a tendina "Applica l'etichetta".

**Percorso B — guida completa manuale** (l'utente non vuole concedere ora la
scrittura su Gmail, o preferisce farlo di persona): istruzioni testuali per
creare prima l'etichetta, poi il filtro. L'etichetta si crea da Gmail → barra
laterale sinistra → "Altro" → "Crea nuova etichetta" → nome **identico** a
`gmail_label` di `routine-config.yaml` (carattere per carattere: la routine
cerca `label:"<nome>"`, non fa match approssimato). Se il nome che l'utente
preferisce è diverso, aggiorna tu `routine-config.yaml` di conseguenza.

**Scrittura su Gmail solo in sessione interattiva**: `create_label` (e
l'eventuale etichettatura retroattiva) si invocano qui o durante l'onboarding,
mai dalla routine — la routine legge Gmail, non ci scrive mai (regola di
proprietà D5).

### Istruzioni per il filtro (identiche nei due percorsi — sempre manuali)

1. Gmail → ⚙️ → "Visualizza tutte le impostazioni" → scheda **"Filtri e
   indirizzi bloccati"** → **"Crea un nuovo filtro"**.
2. Nel campo **"Da"** incolla i quattro mittenti uniti da OR:
   `jobs-noreply@linkedin.com OR jobalerts-noreply@linkedin.com OR alert@indeed.com OR noreply@indeed.com`
3. **"Crea filtro"** (in basso a destra nel riquadro di ricerca).
4. Nella schermata delle azioni spunta **"Applica l'etichetta:"** e seleziona
   dal menu a tendina l'etichetta giusta.
5. Opzionale — **"Ignora Posta in arrivo (Archivia)"**: da spuntare se si vuole
   la Inbox pulita. Rassicura esplicitamente l'utente: **archiviare NON rende
   gli alert invisibili al sistema**, perché la ricerca Gmail della routine
   include per costruzione anche la posta archiviata (non usa mai `in:inbox`).
   È l'esitazione più comune davanti a questa casella.
6. Opzionale — **"Applica il filtro anche alle N conversazioni corrispondenti"**:
   etichetta retroattivamente gli alert già in casella.
7. **"Crea filtro"** per confermare.

Salvo il punto 6, il filtro vale solo per le mail **future**: gli alert arrivati
prima restano senza etichetta (irrilevante a regime, ma spiega perché una
verifica immediata "per etichetta" può tornare vuota).

## Output (checklist in chat + registro su file)

Produci una checklist numerata, **raggruppata per intento** e poi per piattaforma (se ci sono più intenti attivi, intitola ogni blocco con `nome`/`id` dell'intento), nello stile:

```
INTENTO: data-engineering-eu — "Data Engineering in Europa"

LINKEDIN — alert 1 di N
Apri questo link (già pre-filtrato) e clicca "Crea avviso":
  https://www.linkedin.com/jobs/search/?keywords=<keywords>&geoId=<geoId>[&f_E=..&f_WT=..]
1. Verifica che i filtri corrispondano (keywords, area, livello, remoto)
2. Clicca "Crea avviso di offerte" per questa ricerca
3. Nelle impostazioni dell'avviso: frequenza Giornaliera, canale Email
(ricerca_id = data-engineering-eu:linkedin_alert:<keywords-slug>:<geoId>)
```

**Scrittura del registro (`searches/alerts-registry.yaml`)**: per OGNI alert che
proponi, aggiungi/aggiorna la voce corrispondente nel registro (schema in
`references/alerts-registry.schema.yaml`) con `ricerca_id`, `intent_id`,
`keywords`, `geoId`, `area`, `etichetta` leggibile, `stato: attivo`, `creato`.
Poiché costruisci tu l'URL, keywords+geoId (la chiave) sono noti **prima** che
l'alert esista: il registro si scrive subito, non serve la conferma dell'utente
per popolarlo (la conferma serve solo a sapere che l'alert è stato *creato* sulla
piattaforma). Alla riscrittura del profilo (invocazione post `job-search-profile`):
metti `stato: da_rimuovere` sulle voci di alert non più coerenti (intento in
pausa/archiviato, ruolo/location rimossi), non cancellarle a mano — è la traccia
che il tuner e l'utente usano per sapere cosa disattivare sulla piattaforma.
**Verifica opzionale (deterministica)**: dopo che l'utente conferma, puoi cercare
su Gmail le mail di conferma-creazione-alert di LinkedIn e controllare che le
chiavi canoniche coincidano con quelle scritte nel registro — intercetta subito
un filtro impostato diverso o un alert saltato.

Le mappature esatte campo-per-campo (nomi dei filtri, sintassi query, mappatura seniority→livelli piattaforma) sono in `references/mappa-campi-piattaforme.md`: leggilo prima di generare le istruzioni. I nomi dei menu delle piattaforme cambiano nel tempo: se l'utente segnala che un campo indicato non esiste più, adatta l'istruzione al concetto (es. "il filtro che limita per data di pubblicazione") invece di insistere sul nome esatto.

Chiudi SEMPRE con: l'elenco riassuntivo degli alert da creare (per spuntarli), **la voce «etichetta Gmail» con l'esito reale** (creata da te nel percorso A, oppure da creare a mano nel percorso B) e **la voce «filtro Gmail», sempre a carico dell'utente**, e la richiesta di **tre conferme separate**, non un unico "fatto": (1) alert creati sulle piattaforme, (2) **etichetta** Gmail esistente col nome esatto, (3) **filtro** Gmail creato e attivo sui quattro mittenti. È l'interfaccia che `agent-config` (passo 5) aspetta prima di procedere all'attivazione della routine — e lì le tre conferme sono un **checkpoint bloccante**: con (1) ma senza (2)+(3), `agent-config` non prosegue al passo 6. Raccoglile quindi distinte, così quel passo trova una risposta per ciascuna invece di un sì generico da reinterpretare. Se l'utente conferma gli alert ma non il filtro, dillo chiaramente: senza filtro l'etichetta resta vuota e la routine segnalerà un'anomalia a ogni run (il fallback per mittente raccoglie comunque le mail, ma l'anomalia resta rumore permanente nel digest). Le due uscite legittime da offrire sono completare etichetta+filtro adesso, oppure lasciare `gmail_label` **vuota** e affidarsi al fallback per mittente — mai un nome dichiarato senza etichetta dietro. Se invece sei stato invocato dopo una modifica del profilo (via `job-search-profile`), ragiona **per intento**: riallinea solo gli alert dell'intento toccato (o di tutti, se la modifica era ai `defaults`), e ricorda di ELIMINARE o aggiornare gli alert vecchi non più coerenti — inclusi TUTTI gli alert di un intento appena messo in `pausa`/`archiviato` — non solo aggiungere i nuovi.

## Cosa NON fare

- Non tentare di CREARE gli alert al posto dell'utente (LinkedIn/Indeed sono dietro login): l'impostazione resta manuale. Il file che questa skill scrive è il **registro** (`searches/alerts-registry.yaml`), non una config che crea alert: registra alert che l'utente crea a mano.
- Non inventare valori mancanti dal profilo (es. seniority assente → ometti il filtro e dillo, non scegliere tu un livello).
- Non promettere che gli alert filtreranno esclusioni/lingue (vedi sopra).
- Non dare per impostati gli alert senza conferma esplicita dell'utente.
- Non promettere (né tentare) di creare il **filtro** Gmail: il connettore non
  espone tool sui Filtri. L'unica automazione ammessa su Gmail qui è
  `create_label` (+ l'eventuale etichettatura retroattiva di thread già
  esistenti), e solo in sessione interattiva.
- Non saltare la scelta etichetta/filtro perché "l'utente ha fretta": saltarla
  lascia un'anomalia permanente nel digest di ogni run.
