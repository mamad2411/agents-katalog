---
name: agent-config
description: >-
  Onboarding guidato per il sistema Job Hunter. Usa questa skill quando un
  nuovo utente vuole attivare il sistema di ricerca lavoro autonoma:
  ingerisce il CV, fa domande su vincoli/preferenze (trasferimento, remoto,
  retribuzione, preavviso, diritto al lavoro, lingue), produce
  master-profile.yaml e il primo intento di ricerca in searches/ nel repo
  del sistema, genera e attiva la config della routine job-watch. Trigger
  su qualsiasi richiesta di avviare/configurare/inizializzare il sistema o
  la ricerca lavoro, anche breve o generica — es. "inizializza il
  progetto", "salva queste skill e configurami", "iniziamo a fare
  job-hunting", "configurami il sistema". Non richiedere che l'utente
  nomini "agent-config" o "onboarding": il segnale è l'intento di avviare
  il processo. NON usarla per modificare un search-profile già esistente
  ("aggiorna il mio profilo di ricerca", "cambia i ruoli/le location"):
  per quello esiste la skill job-search-profile.
---

# agent-config

Orchestratore conversazionale che porta un utente da zero a sistema attivo (Modulo 1.1 del progetto Job Hunter). Passa la palla a `job-alert-config` (1.2.1) per la config degli alert, e si chiude con due run di validazione (passo 6-ter: una interattiva, una della routine cloud triggerata a mano).

**Artefatti che l'onboarding lascia nel repo** (tutti scritti e committati da te, D7):
- `master-profile.yaml` (radice) — chi è l'utente;
- `searches/defaults.yaml` + il primo `searches/<intent-id>.yaml` — cosa cerca;
- `searches/companies.yaml` — scaffold vuoto (`companies: []`), per la fonte career page che si accenderà più avanti;
- `cv-facts.yaml` (radice) — seed del gate di veridicità, da `cv-facts.example.yaml`;
- `routine-config.yaml` (radice) — config operativa della routine (passo 6, e blocco `todoist:` al 6-bis se accettato).

**Nota architetturale (D5, D7 — da non dimenticare in futuri aggiornamenti)**: architettura a binario unico. TUTTO vive nello stesso repo — profili (`master-profile.yaml`, `searches/`), valutazioni (`role-fit/`), candidature (`applications/`), telemetria operativa (`source-log/`, `state.json`, staging, digest) e le skill stesse sotto `.claude/skills/`. Fatto tecnico che motiva l'impianto: l'integrazione GitHub di base disponibile in chat claude.ai (Impostazioni → Connettori) è di **sola lettura** — sincronizza i contenuti per contesto ma non espone tool di scrittura/commit. Per questo ogni SCRITTURA reale (profili, valutazioni, candidature, stato) avviene in **sessione Claude Code** (Desktop o routine cloud), che ha accesso git nativo indipendente dai connettori di chat. Regola di proprietà: le sessioni interattive scrivono profili/valutazioni/candidature; la routine scrive solo lo strato operativo append-only (log/state/digest/staging).

Non eseguire questa skill silenziosamente: è interattiva per costruzione. Ogni sezione sotto corrisponde a un blocco di domande da fare in chat, una alla volta o in piccoli gruppi coerenti — mai tutte insieme in un unico wall of text.

## Passo 0 — Messaggio di apertura fisso

Prima di qualunque verifica tecnica, invia sempre questo messaggio (adattalo minimamente se necessario, ma mantieni struttura, contenuto e tono):

---

Ciao! 👋 Iniziamo la configurazione del sistema Job Hunter.

Ti spiego prima cosa serve e cosa succederà, così puoi preparare tutto senza interruzioni a metà strada :)

**La casa del sistema è un repository GitHub** 🏠 — un'unica repo (questa, in cui stiamo lavorando ora) contiene tutto: il tuo profilo, le ricerche, le valutazioni, le candidature e la routine automatica. Se stai leggendo questo messaggio in Claude Code, la repo c'è già: la verifico tra un attimo. La routine lavora sul branch `main`, ed è lì che scrive quello che trova.

🔒 **La repo deve essere privata.** Conterrà i tuoi dati personali reali — email, telefono, retribuzione attuale e attesa. Se la crei ora, creala privata; se esiste già, te lo faccio verificare prima di attivare la routine. Non renderla mai pubblica: per condividere il sistema con altri esiste una versione "template" senza i tuoi dati.

⚠️ Una sola cosa può fermarci a metà: se questa cartella non è ancora collegata a una repo GitHub tua (il "remote"), l'ultimo passo — l'attivazione della routine — non può partire, perché la routine legge solo ciò che è stato caricato su GitHub. Te lo dico subito dopo la verifica, così eventualmente crei la repo mentre facciamo il resto: il profilo e le ricerche si scrivono comunque.

**Cosa ti servirà — lato GitHub** (serve solo all'ultimo passo, l'attivazione della routine; i passi prima girano comunque):
- un **account GitHub** e la possibilità di creare una **repo privata** tua;
- se la repo esiste già ma ha regole di **branch protection** su `main` (review obbligatoria, status check), la routine non riuscirà a pushare: andrà esentata l'identità con cui gira, oppure si passa al modello PR + auto-merge. Te lo chiedo esplicitamente al passo 6;
- l'identità con cui gira la routine cloud deve avere **permesso di push su `main`** (su una repo personale è già così; su una repo di organizzazione va verificato).
Niente di tutto questo va fatto ora: te lo guido voce per voce al passo 6. Lo elenco qui solo perché tu sappia che l'attivazione tocca la configurazione della repo, non solo la chat.

**Cosa ti servirà collegato prima di iniziare:**
1. **Gmail** 📧 — necessario alla routine di ricerca automatica per leggere gli alert LinkedIn/Indeed, e per preparare le bozze di follow-up più avanti.
2. **Indeed** 🔍 — necessario alla routine per cercare annunci.

Se non li hai già collegati, puoi farlo da Impostazioni → Connettori. Te li verifico comunque uno per uno tra un attimo.

**Cosa ti chiederò:**
- Il tuo CV 📄 (in qualsiasi formato che riesci a caricare qui in chat)
- Alcune domande su vincoli e preferenze: disponibilità a trasferirti o lavorare da remoto, retribuzione attuale e aspettativa, preavviso, diritto al lavoro nei paesi che ti interessano, eventuale iscrizione alle categorie protette (L. 68/99), lingue
- Conferma su ruoli, location e criteri di esclusione per la ricerca

**Cosa succederà dopo:**
1. Scrivo il tuo profilo nel repo (e lo committo io — non devi toccare git)
2. Ti do le istruzioni per impostare gli alert LinkedIn/Indeed
3. Attiviamo insieme la routine di ricerca automatica — questo passaggio si fa dall'**app desktop di Claude Code** 🖥️ (niente terminale, solo click) — e la facciamo girare una volta insieme, subito, per vedere che arrivi in fondo prima di lasciarla ai suoi orari
4. Se ti va, ti preparo anche una **board Todoist** 📋 per decidere dal telefono quali offerte scartare e quali portare avanti — è facoltativa, te la propongo alla fine

Da lì in poi il sistema lavora per te: ogni mattina trovi in Gmail una **bozza** di digest con gli annunci trovati — una bozza, non una mail inviata: la apri, la leggi e resta lì finché non decidi tu. Poi usi la chat per valutare gli annunci, preparare CV su misura e tenere traccia delle candidature.

Cominciamo dal CV — puoi caricarlo ora? 😊

---

Dopo questo messaggio, procedi comunque con la verifica tecnica concreta delle Precondizioni sotto — il messaggio dichiara i requisiti all'utente, ma non sostituisce il controllo reale via `tool_search`. Non fidarti della sola dichiarazione dell'utente "ce li ho tutti collegati": verificalo.

## Precondizioni

Prima di iniziare l'intervista, verifica CONCRETAMENTE (non a parole) i requisiti del sistema, anche quelli che questa skill non usa direttamente — è il primo punto di contatto interattivo, il posto giusto per bloccare l'intero onboarding se manca qualcosa:

1. **Repo del sistema clonato e git funzionante** — verifica DIRETTAMENTE in Claude Code (nessun `tool_search`, non è un connettore di chat): sei dentro un clone di lavoro del repo, `git` risponde, ed esiste un remote configurato (`git remote -v`). È la casa dell'intero sistema — profili, ricerche, valutazioni, candidature, telemetria della routine. Il remote serve perché la routine cloud legge solo ciò che è committato+pushato (vedi passo 6). Se non c'è un remote, dillo e chiedi all'utente di crearlo/collegarlo (repo GitHub sua, nome a scelta) prima del passo 6: i passi 1–4 scrivono in locale e committano, ma senza push la routine non li vedrebbe.
2. **Gmail** — `tool_search` query "Gmail". Necessario alla routine (lettura alert) e a valle per follow-up/bozze.
3. **Indeed** — `tool_search` query "Indeed jobs". Necessario alla routine per la ricerca.
4. **CV disponibile** — chiedilo come primo passo se non è già stato allegato in chat.
5. **Todoist (facoltativo)** — `tool_search` query "Todoist". Serve solo se
   l'utente vuole la board di revisione del passo 6-bis: la sua assenza NON
   blocca l'onboarding e non va segnalata come mancanza qui. Verificalo quando
   arrivi a quel passo, non prima.
6. **Hook di protezione presente ed eseguibile** — verifica DIRETTAMENTE nel
   clone che `.claude/hooks/protect-files.sh` esista e abbia il bit di
   esecuzione (`ls -l .claude/hooks/protect-files.sh` → deve mostrare `x`). È la
   rete di sicurezza primaria della routine (con `JOB_HUNTER_ROUTINE=1` blocca
   le scritture su `master-profile.yaml`, `searches/`, `role-fit/`,
   `applications/`). Un clone che ha perso il bit di exec fa fallire l'hook **in
   silenzio**: la variabile risulterebbe impostata ma la protezione spenta. Se
   il bit manca, ripristinalo tu (`chmod +x .claude/hooks/protect-files.sh`) e
   committalo prima del passo 6; se il file manca del tutto, fermati — il clone
   è incompleto.

Per Gmail/Indeed mancanti: fermati, dì per nome quale manca e perché serve, e chiedi di collegarlo prima di proseguire. Non generare un profilo incompleto "per ora" e non saltare la verifica assumendo che l'utente li abbia già collegati solo perché ha caricato il pacchetto di skill: il pacchetto di skill e i connettori dell'account sono due cose diverse, installate in due posti diversi (il repo l'uno, Impostazioni → Connettori gli altri).

**Connettore o scrittura che fallisce a metà flusso**: se un tool call fallisce durante l'intervista (connettore Gmail/Indeed scaduto, permesso revocato) o se la scrittura/commit al passo 4 fallisce, non perdere il lavoro fatto: mostra subito in chat lo stato completo dei dati raccolti fino a quel punto (lo YAML parziale, se già formato), spiega cosa ha fallito e come rimediare, e riprendi ESATTAMENTE dal passo interrotto — non ricominciare l'intervista da capo. In particolare, se la scrittura file al passo 4 riesce ma il commit no, i file sono comunque salvati in locale: ritenta solo il commit.

## Schema di riferimento

Gli schemi dato-agnostici sono in:
- `references/master-profile.schema.yaml`
- `references/search-profile.schema.yaml`

E la procedura di attivazione della routine (passo 6) in:
- `references/routine-setup.md`

Leggili prima di condurre l'intervista: ogni campo dello schema è una domanda potenziale. Non inventare campi che non sono nello schema; se durante l'intervista emerge un dato utile che non ha posto nello schema, segnalalo all'utente invece di infilarlo a forza da qualche parte — potrebbe voler dire che lo schema va aggiornato (torna al progetto, non decidere da solo).

## Flusso

### 1. Ingestione CV → bozza master-profile

- Chiedi il CV se non presente.
- Estrai dal CV tutto ciò che mappa direttamente sui campi di `master-profile.schema.yaml`: esperienze, progetti, skill tecniche, lingue, formazione, certificazioni.
- Presenta la bozza risultante e chiedi conferma/correzioni prima di proseguire. Un CV può essere ambiguo o incompleto (date mancanti, stack non esplicito) — segnala i buchi invece di indovinare.
- Non chiedere ancora i campi che il CV non può contenere (retribuzione, preavviso, disponibilità): vengono dopo, sono domande dirette non deducibili da un documento.

### 2. Domande su vincoli e preferenze

Copri, in gruppi tematici separati (non tutto insieme):

**Anagrafica e contatti**
- **Città di residenza attuale** → `anagrafica.location_attuale`. Non è deducibile dalla mobilità: "disponibile a trasferirsi a Milano" non dice dove l'utente vive oggi. Il CV non sempre la riporta, e quando la riporta può essere vecchia — chiedila, non ricavarla.
- **Link esterni** → `anagrafica.link_esterni` (LinkedIn, GitHub, sito personale/portfolio). Il passo 1 li raccoglie solo se compaiono sul CV: chiedi esplicitamente se ce ne sono altri, o se quelli sul CV sono ancora validi.
- Dì **perché** li chiedi: entrambi finiscono nell'**intestazione** di CV e cover letter generati da `cv-tailoring`. Se mancano, l'intestazione esce incompleta a ogni candidatura.
- Nessuna assunzione silenziosa: se l'utente non ha un sito o un GitHub, il campo resta **vuoto** — è una risposta legittima, non un buco da riempire con un profilo indovinato.

**Mobilità**
- Disponibilità trasferimento (sì / no / solo alcune aree — e quali)
- Disponibilità remoto (full remote / ibrido / solo sede / indifferente)

**Economico**
- Retribuzione attuale (valore, lordo/netto, periodicità)
- Aspettativa (range, stesse unità)
- Eventuale flessibilità/note

**Contrattuale**
- Preavviso (durata, eventuali vincoli particolari)

**Legale**
- Cittadinanza/e
- Diritto al lavoro per le aree in cui l'utente vuole cercare (non dare per scontato che coincida con la cittadinanza — un permesso di soggiorno, un passaporto UE aggiuntivo, ecc. possono cambiare la risposta)
- **Categorie protette / collocamento mirato (L. 68/99)**: "Sei iscritto/a alle liste del collocamento mirato (categorie protette — L. 68/99 o assimilati)?" → `anagrafica.categoria_protetta` (`si`/`no`/`preferisco_non_rispondere`). Ponila in modo neutro e spiega **perché la chiedi**: molte offerte "developer" sono *riservate* a chi è iscritto a quelle liste, e senza questa risposta il sistema continuerebbe a proportele (o a scartartele) alla cieca. Se `no` o `preferisco_non_rispondere`, la routine scarta a monte le offerte esplicitamente riservate (`scartato_idoneita`); se `si`, restano in valutazione. Campo saltabile: se l'utente non risponde, lascialo assente (= trattato come `no` dal filtro, ma senza aver "deciso" per lui).

**Lingue**
- Livello per ciascuna lingua rilevante, e contesto d'uso (lavorativo quotidiano vs solo letto) — serve sia a `master-profile` sia, a valle, a filtrare gli annunci in `search-profile`

**Adozione AI** (`strato_ai_adoption`)
- Quali strumenti AI usa davvero nel lavoro, in quali contesti (scrittura codice, analisi, automazione, documentazione…), con che livello di autonomia (`uso_base` / `uso_avanzato` / `costruisce_soluzioni_ai_per_altri`) ed eventuali note sull'approccio
- Non è un campo di colore: `cv-tailoring` lo usa per decidere se e come far comparire lo strato AI nel CV quando la JD o l'azienda lo rendono rilevante. Se l'utente non usa strumenti AI, lascia il campo vuoto — è una risposta legittima, non un buco da riempire

**Preferenze generali** (`preferenze_generali`)
- Settori preferiti e settori da evitare **come persona** (vedi la regola di disambiguazione sotto), dimensione azienda preferita (`startup` / `pmi` / `enterprise` / `indifferente`), note libere: obiettivi di carriera, cosa cerca in un ambiente di lavoro, cosa lo farebbe dire di no
- Le legge `role-fit`, che le usa come **peso nel giudizio** di un annuncio, mai come filtro

> **Regola di disambiguazione (settori — due campi, due mestieri).** Ci sono due
> posti che parlano di settori e non sono intercambiabili:
> `master-profile.preferenze_generali.settori_preferiti/settori_da_evitare` sono
> affinità **stabili della persona** e **pesano nel giudizio** (`role-fit`: un
> settore gradito rafforza, uno sgradito diventa una considerazione contraria) —
> non filtrano niente, non fanno sparire nessun annuncio.
> `searches/<intento>.settori.target/esclusi` sono criteri della **singola
> ricerca** e **filtrano la raccolta** (`job-watch` e gli alert).
> In breve: se un settore deve far sparire gli annunci → va nell'intento (passo
> 3); se deve solo spostare il giudizio → va nel master-profile. Dillo
> all'utente quando fai la domanda, così sa cosa sta decidendo: la stessa
> parola in due posti diversi ha due effetti diversi.

Ogni gruppo di domande scrive direttamente nei campi corrispondenti dello schema. Se l'utente salta una domanda o risponde "non so", lascia il campo vuoto/null nello YAML — non riempirlo con un default plausibile.

### 3. Produzione del primo intento di ricerca

A questo punto hai i dati per derivare (non indovinare — derivare, con conferma esplicita) la ricerca. Con D2 la ricerca non è un file unico ma una cartella `searches/` con un `defaults.yaml` condiviso e un file per intento. All'onboarding produci **un solo intento** (l'utente potrà aggiungerne altri dopo, via `job-search-profile`). Le domande NON cambiano: cambia solo dove atterrano le risposte.

Dove atterra cosa (vedi `references/search-profile.schema.yaml`):
- **`searches/defaults.yaml`** (default ereditabili, stabili tra intenti): `esclusioni`, `lingue_annuncio`, `parametri_esecuzione`.
- **`searches/<intent-id>.yaml`** (l'intento): `id` (slug stabile, chiedi/proponi un nome breve — es. `data-engineering-eu` — perché è la chiave che comparirà in log, valutazioni e candidature), `nome` (etichetta leggibile), `stato: attivo`, `creato` (data odierna), più `ruoli_target`, `location_target`, `seniority`, `settori`, `fonti`. All'onboarding l'intento non ha `override` (eredita tutti i defaults); lo si aggiunge solo se in futuro un intento diverge.

I campi da raccogliere (invariati nella sostanza):

- **Seniority**: dagli anni di esperienza e dal tipo di ruoli avuti in `master-profile.esperienze`, proponi un livello (`junior/medio/senior/...`) e chiedi conferma — non scriverlo senza validazione, perché la percezione di seniority dell'utente può differire dal dato grezzo. Chiedi anche se ci sono **ruoli per cui un livello "junior" resta accettabile** nonostante il livello dichiarato: tipicamente un ruolo di transizione (es. "Junior Architect" per chi è mid come developer ma punta all'architettura) — vanno in `seniority.ruoli_ammessi_sotto_livello`. Serve al filtro seniority della routine (job-watch passo 4): senza, un "Junior <qualunque cosa>" nel titolo viene scartato; con `["architect"]`, "Junior Integration Architect" passa.
- **Ruoli target**: chiedi esplicitamente quali titoli cercare (non dedurli automaticamente dal ruolo attuale — un utente potrebbe voler cambiare ruolo).
- **Location target**: chiedi le aree geografiche di interesse, incrociando con `disponibilita_remoto`/`disponibilita_trasferimento` già raccolti.
- **Esclusioni**: chiedi se ci sono titoli o tipi di contratto da escludere sempre (es. ruoli manageriali, stage) — proponi i default tipici (Head of/Director/VP/C-level, Internship/Traineeship/Stage) ma fai confermare, non assumerli silenziosamente.
- **Settori**: target ed esclusi **per questa ricerca** — sono i settori che filtrano la raccolta, non le affinità della persona raccolte al passo 2 (vedi la regola di disambiguazione lì). Parti da `preferenze_generali.settori_preferiti/da_evitare` come proposta ("li uso anche come criterio di ricerca?") e fai confermare: spesso coincidono, ma un settore gradito non implica che l'utente voglia scartare tutto il resto, e un settore da evitare in generale non sempre va escluso in una ricerca specifica.
- **Fonti**: quali piattaforme sono attive per questo intento (`indeed`, `linkedin_alert`, `indeed_alert`, `career_page`, ciascuna con `attiva: true|false` e una `note` che dica perché). Non è un campo decorativo: `job-alert-config` lo legge davvero e salta le fonti `attiva: false`, e la routine ci decide da dove raccogliere — se resta vuoto, a valle nessuno sa cosa saltare. Proponi la configurazione plausibile dal contesto e **fai confermare** (stessa regola degli altri campi derivati, nessuna assunzione silenziosa): `indeed` normalmente attiva (ricerca diretta via connettore, non richiede setup da parte dell'utente); `linkedin_alert`/`indeed_alert` attive solo se l'utente intende davvero crearli al passo 5 — è la stessa decisione, quindi chiedila qui una volta sola e riusala lì invece di riproporla; `career_page` di norma `attiva: false` all'onboarding (si accende quando `searches/companies.yaml` avrà aziende, aggiunte più avanti con `job-search-profile`).
- **Lingue annuncio**: da `master-profile.lingue`, proponi quali lingue sono accettabili per il corpo di un annuncio e quali lo scartano se prevalenti/obbligatorie — richiede una domanda esplicita, perché "so l'inglese" non implica automaticamente "accetto annunci il cui corpo è in inglese ma richiede altra lingua come requisito".
- **Parametri esecuzione**: finestra temporale e max annunci per esecuzione — proponi i default usati nella routine esistente (48 ore, 15 annunci) solo come punto di partenza dichiarato, fai confermare.

### 4. Scrittura nel repo + commit

- Verifica se esistono già i file di profilo (`master-profile.yaml` nella radice, `searches/`): se sono già valorizzati, l'utente ha probabilmente già fatto l'onboarding — chiedi conferma prima di sovrascrivere, non ripartire da zero in silenzio. (Un `master-profile.yaml` vuoto/placeholder o un `searches/` con solo `defaults.yaml` scaffold NON è "già onboardato": procedi.)
- Mostra il contenuto finale all'utente PRIMA di scriverlo. Non scrivere silenziosamente — è un dato che alimenta tutto il resto del sistema (routine, role-fit, cv-tailoring): un errore qui si propaga ovunque.
- **Scaffold degli altri artefatti che l'onboarding deve lasciare pronti.** Non sono file "di contorno": sono file che qualcosa a valle legge davvero, e che se mancano producono un'anomalia permanente o una fonte muta. Creali in questo passo, senza chiedere nulla all'utente (non contengono sue scelte):
  - **`cv-facts.yaml`** (radice) — copia il contenuto di `cv-facts.example.yaml` **azzerando `allow_metrics` a `[]`** e tenendo le `forbidden_phrases` generiche. Lo legge `scripts/verify_cv_facts.py`, il gate di veridicità che `job-watch` (passo 6) invoca su **ogni** materiale pre-generato: se il file manca, lo script esce 3 e il digest riporta un'anomalia a ogni run con fit forte o buono, per sempre. Si parte con `allow_metrics` **vuoto** di proposito — le deroghe si aggiungono quando si presenta un falso positivo reale, e le aggiunge **l'utente**, mai l'agente per far passare il proprio output.

    **Spiegalo all'utente in due righe** (non solo scriverlo): esiste un gate che confronta ogni numero in un CV/cover/DM generato con `master-profile.yaml` e **blocca** i claim non tracciabili. Conseguenza pratica per lui: la prima volta che un materiale conterrà una metrica legittima ma *derivata* (una percentuale aggregata, un totale calcolato) verrà rifiutato, ed è lui a dover aggiungere la deroga in `cv-facts.yaml` — l'agente può proporla ma non inserirla da sé. Senza questo avviso, il primo blocco sembra un guasto.
  - **`searches/companies.yaml`** — scaffold vuoto con `companies: []` e l'header di contratto. Al passo 3 la fonte `career_page` è spenta, quindi il file non serve ancora a nessuno; esiste perché `job-search-profile` ci scriva le aziende senza doverlo inventare, e perché la routine non debba degradare su un file assente.
- Ultimo atto del passo, eseguito da te (l'utente non tocca git — D7): scrivi i file (`master-profile.yaml`, `searches/defaults.yaml`, `searches/<intent-id>.yaml`, `searches/companies.yaml`, `cv-facts.yaml`) e **committa** con un messaggio chiaro (es. `onboarding: master-profile + primo intento <intent-id>`). Il push si fa al passo 6, quando si attiva la routine (prima non serve: nulla legge ancora questi file da remoto).

### 5. Passaggio a job-alert-config (alert LinkedIn/Indeed)

L'ordine è vincolato, non è una preferenza di stile: prima si scrive il primo intento in `searches/` (passo 4), poi si configurano gli alert, e solo dopo si attiva la routine (passo 6). La routine legge gli alert LinkedIn via Gmail: attivarla prima che gli alert esistano la farebbe partire su una fonte vuota.

- Richiama esplicitamente la skill `job-alert-config` (1.2.1), passandole l'intento appena creato in `searches/`. Non duplicarne la logica qui: quella skill produce le istruzioni su come impostare i campi degli alert su LinkedIn/Indeed (sono dietro login, quindi istruzioni per l'utente, non config programmatica) **e** conduce la scelta guidata sull'**etichetta Gmail** (creata via connettore o a mano) e sul **filtro Gmail** che la applica ai quattro mittenti degli alert — il filtro resta manuale in ogni caso, il connettore non espone tool sui Filtri. Se in quel passaggio si concorda o si cambia il nome dell'etichetta, `routine-config.yaml` viene allineato lì: al passo 6 lo verifichi, non lo richiedi da capo.
**Checkpoint bloccante — tre conferme separate, non una sola «fatto».** Prima di passare al passo 6 devi avere tutte e tre. Chiedile una per una: «fatto» detto di fretta copre di norma solo la prima, ed è esattamente il modo in cui un onboarding esce da qui con `gmail_label` dichiarata e nessuna etichetta dietro.

1. **Alert creati** sulle piattaforme (LinkedIn/Indeed), per le fonti che al passo 3 sono `attiva: true`.
2. **Etichetta Gmail esistente**, col nome **esatto** che finirà in `routine-config.yaml → gmail_label`. Nel percorso A di `job-alert-config` l'hai creata tu col connettore, quindi è già confermata; nel percorso B (manuale) deve dirtelo l'utente. **Verificala col connettore** (`list_labels`) invece di fidarti: è un controllo che costa una chiamata.
3. **Filtro Gmail creato**, e che applica quell'etichetta ai quattro mittenti degli alert. È **sempre** manuale, in entrambi i percorsi — il connettore non espone tool sui Filtri — e **non è ispezionabile**: qui resti sulla parola dell'utente, quindi chiediglielo in modo esplicito e non deducibile da un sì generico.

**Se hai (1) ma non (2)+(3), non proseguire al passo 6.** Spiega perché, concretamente: attivare la routine con un nome di etichetta dichiarato ma senza etichetta e filtro corrispondenti produce un'**anomalia nel digest a ogni run, per sempre**. Gli alert verrebbero comunque raccolti (la routine ha un fallback per mittente), quindi non si rompe nulla — ma l'anomalia resta rumore permanente che nasconde le anomalie vere. Offri le due uscite legittime, entrambe accettabili:

- **completare ora** etichetta e filtro (torna a `job-alert-config`, che ha le istruzioni); oppure
- **lasciare `gmail_label` vuota** e affidarsi al fallback per mittente. È un esito pienamente legittimo, non un ripiego difettoso: nessuna anomalia, la routine legge dai quattro mittenti noti. Ciò che non deve mai esistere è un nome dichiarato senza etichetta dietro.

Non proseguire per inerzia e non "rimandare al passo 6": al passo 6 il file è già scritto e la routine sta per partire.

### 6. Verifica e attivazione della routine

Architettura a **binario unico** (D5): tutto vive in questo repo — i profili (`master-profile.yaml`, `searches/`) scritti al passo 4, e lo strato operativo che la routine scriverà (`source-log/`, `state.json`, staging, digest). Non c'è un secondo storage.

Compiti di questo passo:
- **`routine-config.yaml` (radice del repo, F5) — mostralo e fallo confermare prima di attivare la routine.** È la config operativa che la routine legge a ogni run. Due valori si decidono qui (il terzo blocco, `todoist:`, solo se l'utente accetta la board opzionale del passo 6-bis):
  - `gmail_label` — l'etichetta Gmail da cui la routine legge gli alert. Di norma è già stata concordata (e il file già allineato) al passo 5 con `job-alert-config`: qui **verifichi** che il file dica esattamente il nome dell'etichetta che esiste davvero in Gmail, non lo richiedi da capo. Se al passo 5 l'utente ha scelto il percorso manuale e non ha ancora creato etichetta e filtro, questo è l'ultimo momento utile per farglielo notare: attivare la routine con un'etichetta dichiarata ma inesistente produce un'**anomalia nel digest a ogni run**, per sempre. Se l'utente preferisce non usare affatto un'etichetta, lascia il campo vuoto — la routine ha un fallback per mittente ed è un esito legittimo, non un'anomalia; ciò che non deve mai succedere è un nome dichiarato senza etichetta corrispondente.
  - `cadenza_dichiarata` — la cadenza che stai per impostare davvero nella routine (es. `"1 run/giorno"`), scritta in chiaro: è il valore con cui il digest calcola la "prossima run attesa" e con cui `job-alert-tuner` confronterà la cadenza reale. Falla confermare insieme alla schedulazione che crei sotto, così i due valori nascono coerenti.
  - Se il file **non esiste** nel repo dell'utente, scrivilo tu (D7 — l'utente non tocca file) con i valori confermati, mantenendo i commenti esplicativi: cosa sono i due campi, la trappola dell'operatore `label:` che non accetta l'ID interno di `list_labels` (solo il nome), e il promemoria che l'ambiente della routine cloud deve impostare `JOB_HUNTER_ROUTINE=1` nei propri secret (non è derivabile dal repo). Committalo insieme al resto.
- **Push obbligatorio prima di attivare la routine**: la routine cloud gira su un clone del repo e vede SOLO ciò che è stato committato *e pushato*. Esegui tu il push del commit del passo 4 (D7 — l'utente non tocca git). Se al prerequisito 1 mancava il remote, è il momento di risolverlo: fatti dare l'URL della repo GitHub dell'utente, collegala come remote, poi push. Senza questo, la routine partirebbe su un profilo vuoto.
- **La repo deve essere privata — verificalo qui, dove si collega il remote.** Contiene PII reali: email, telefono, retribuzione attuale e attesa in `master-profile.yaml` (vincolo F7). Dillo esplicitamente — «la repo va creata privata; non renderla mai pubblica, contiene i tuoi dati personali» — e, dopo il collegamento del remote, **fai verificare all'utente** su GitHub che sia effettivamente privata (Settings → General → Danger Zone: deve dire *Private*). Nessun controllo automatico rileva un cambio di visibilità fatto per errore, quindi questo è l'unico momento in cui qualcuno guarda. Se l'utente vuole condividere il sistema, la risposta è il branch `template` (snapshot senza dati personali), mai rendere pubblica la sua repo.
- **Regola di proprietà (ricordala all'utente)**: da qui in poi la routine scrive solo lo strato operativo append-only (log/state/digest/staging); i profili, le valutazioni e le candidature restano scritti dalle sessioni interattive. La routine *legge* i profili e `applications/` (per le scadenze del digest), non li modifica.
- **Attivazione vera e propria: segui `references/routine-setup.md`, voce per voce.** Non improvvisare questo passo e non riassumerlo: quel file è la procedura ordinata e completa (modello di push e branch protection, creazione della routine con prompt e cron, ri-approvazione dei connettori nell'ambiente cloud, secret, Network access, prima run). Conducilo come una **checklist spuntabile** — leggi una voce, aspetta conferma, passa alla successiva — perché è quasi tutto fuori dal repo e nessun agente può farlo al posto dell'utente.

  Le tre voci che si dimenticano più spesso, e che quindi devi far spuntare esplicitamente invece di darle per scontate:
  1. **`JOB_HUNTER_ROUTINE=1`** nei secret/variabili dell'ambiente della routine (routine → icona ambiente → variabili/secret). È il contratto che distingue una sessione-routine da una interattiva: attiva l'hook `.claude/hooks/protect-files.sh`, che impedisce meccanicamente alla routine di scrivere `master-profile.yaml`, `searches/`, `role-fit/`, `applications/`. Senza, la rete di sicurezza primaria è spenta e resta solo l'allowlist, che è più larga.
  2. **Connettori ri-approvati nell'ambiente cloud.** Gli ID MCP in allowlist sono legati all'account: su un clone fresco Gmail e Indeed vanno riautorizzati al collegamento, altrimenti la routine si ferma su un prompt di conferma che nessuno vedrà — gira non presidiata.
  3. **Cron coerente con `cadenza_dichiarata`.** I due valori nascono qui e devono dire la stessa cosa: il digest calcola su `cadenza_dichiarata` la "prossima run attesa", e `job-alert-tuner` ci confronterà la cadenza reale. **Dillo all'utente**: i due valori vivono in due posti diversi (il cron nella UI Routines, `cadenza_dichiarata` nel repo) e niente li tiene sincronizzati da solo — se un giorno cambia lo schedule della routine deve dirlo in chat, così `routine-config.yaml` viene riallineato nella stessa sessione; altrimenti il digest e il tuner ragioneranno su una cadenza sbagliata senza segnalare nulla.

  **Registra la scelta del modello di push** (diretto su `main` — default — oppure branch di servizio + PR con auto-merge) come una riga nella nota di chiusura o nel messaggio di commit: è la prima cosa da sapere quando un giorno una run non pusherà.
- **Digest = bozza, non invio.** Nella routine cloud il digest arriva come **bozza Gmail** che l'utente apre e rivede: l'invio SMTP diretto non funziona nel sandbox per costruzione. Dillo con queste parole, così nessuno resta in attesa di una mail che non arriverà. Conseguenza pratica: **nessun secret SMTP** (`GMAIL_ADDRESS`/`GMAIL_APP_PASSWORD`) da impostare — servono solo nella variante Desktop locale, documentata in `routine-setup.md` e non consigliata a un nuovo utente.
- Mostra, a scopo di verifica, i valori committati al passo 4, così l'utente capisce cosa la routine leggerà dal clone.

### 6-bis. Board Todoist per la revisione (opzionale — proponila, non imporla)

Il collo di bottiglia reale del sistema non è trovare gli annunci: è
**decidere** su quelli trovati, perché lo scarto/promozione richiede una
sessione Claude Code. La board Todoist sposta quella decisione sul telefono:
la routine crea una card per ogni offerta in attesa, l'utente la trascina, e al
giro successivo `scripts/sync_todoist.py` (passo 6-bis di `job-watch`)
rispecchia lo spostamento nel repo. **È opzionale**: senza, il sistema funziona
esattamente come prima (revisione in chat, anche a lotti con il triage di
`application-tracker`). Proponila con una frase sola e accetta il no senza
insistere.

Se l'utente dice sì:

1. **Connettore Todoist** — `tool_search` query "Todoist". Se manca, dillo:
   senza connettore puoi comunque procedere, ma la board dovrà crearla lui a
   mano e gli ID delle sezioni non sono leggibili dall'interfaccia (l'URL
   mostra solo quello del progetto) — quindi in pratica **conviene collegarlo**.
2. **Crea la board tu** (D7 — l'utente non tocca file né configurazioni che
   puoi fare tu): un progetto (nome a scelta dell'utente, proponi "Job Hunter")
   in **vista board**, con **nove sezioni** dai nomi ESATTI, nell'ordine:
   `Da valutare · fit forte` · `Da valutare · fit buono` ·
   `Da valutare · fit parziale` · `Da valutare · fit debole` · `Scartate` ·
   `Da candidare` · `Candidatura inviata` · `Colloquio fissato` · `Rifiutata`.

   Due gruppi di sezioni, con due mestieri diversi:
   - le quattro **di anticamera** (`Da valutare · fit …`) sono dove nasce la
     card. L'anticamera è divisa per fit di proposito: in un blocco unico i due
     fit forti della settimana annegano fra ottanta deboli e la board smette di
     essere una lista di decisioni. Spostare una card **fra** questi gruppi non
     è una decisione — il sync la registra e basta;
   - le cinque **di esito** (`Scartate` → `Rifiutata`) sono le uniche che
     muovono qualcosa nel repo, e sono **tutte obbligatorie**, incluse le due
     post-invio `Colloquio fissato` e `Rifiutata`: senza, quelle due transizioni
     di stato non sarebbero esprimibili dalla board e `sync_todoist.py`
     rifiuterebbe la config (esce 3, passo saltato a ogni run).

   I nomi servono all'utente; il sync lavora sugli **ID**, così rinominare una
   sezione più avanti non rompe nulla. Se l'utente ha già un progetto suo che
   vuole riusare, usa quello e crea solo le sezioni mancanti.
3. **Scrivi il blocco `todoist:` in `routine-config.yaml`** con `project_id` e
   gli ID di sezione restituiti dal connettore (schema in `job-watch/SKILL.md`,
   passo 6-bis), e committalo insieme al resto:

   ```yaml
   todoist:
     project_id: "<id progetto>"
     sezioni:
       da_valutare_forte: "<id>"
       da_valutare_buono: "<id>"
       da_valutare_parziale: "<id>"
       da_valutare_debole: "<id>"
       scartate: "<id>"
       da_candidare: "<id>"
       candidatura_inviata: "<id>"
       colloquio_fissato: "<id>"
       rifiutata: "<id>"
     push_score_minimo: debole
   ```

   **La regola vera di `push_score_minimo`** (dilla così, è l'unica che conta
   quando si sceglie): è la soglia sotto la quale **non si crea alcuna card**, e
   il sync pretende un gruppo di anticamera per **ogni** fit sopra soglia — se
   ne manca uno esce 3 e il passo si salta a ogni run. Le cinque sezioni di
   esito servono sempre, qualunque sia la soglia.

   **Proponi `debole`** (tutti gli score arrivano sulla board, ognuno nel
   proprio gruppo: serve le nove sezioni sopra) e presenta l'alternativa
   `buono`, che tiene la board corta — solo fit forte e buono ricevono una
   card, e bastano sette sezioni. È una scelta dell'utente, non tua: la
   differenza è se la board debba essere **lo specchio completo della coda**
   (`debole`) o **solo le decisioni che valgono la pena** (`buono`, che è anche
   il default dello script se il campo manca). Con `buono`, le voci
   `parziale`/`debole` restano `pending` in staging nel repo e si smaltiscono
   in chat col triage in blocco di `application-tracker`; il loro conteggio
   compare comunque nel digest, quindi non spariscono dal radar. Se cambia idea
   più avanti, abbassare la soglia richiede di creare prima i gruppi mancanti.

   Il **token non va mai qui** (né in nessun altro file del repo).
4. **Gate di rete locale — lo sistemi tu adesso (D7).**
   `scripts/sync_todoist.py` contatta `api.todoist.com`, che deve comparire in
   `sandbox.network.allowedDomains` di `.claude/settings.json`. **Verificalo e,
   se manca, aggiungilo e committalo** in questo stesso passo: sul branch
   `template` quel dominio è rimosso dalla genericizzazione, quindi in un clone
   fresco non c'è, e senza di esso una run locale/Desktop di `sync_todoist.py`
   fallirebbe con errore di rete. (Stessa manutenzione servirà in futuro per i
   domini delle career page, quando l'utente aggiungerà aziende con
   `job-search-profile`.)
5. **Dichiara i due passi che restano all'utente** — sono suoi per costruzione,
   nessun agente può farli, quindi dillo esplicitamente invece di darli per
   scontati:
   - **`TODOIST_API_TOKEN`** nei secret dell'ambiente della routine
     (in Todoist: Impostazioni → Integrazioni → Sviluppatore → API token;
     su claude.ai: routine → icona ambiente → variabili/secret). Stesso
     trattamento di `JOB_HUNTER_ROUTINE=1`: non è derivabile dal repo.
   - **Rete — gate cloud: `api.todoist.com` raggiungibile dall'ambiente** della
     routine cloud. È il **secondo gate**, indipendente dal gate locale del
     punto 4 e non scrivibile da nessun agente. Cosa serve dipende
     dall'opzione scelta al passo 5 di `references/routine-setup.md`: con
     l'**accesso di rete libero** (opzione consigliata) è già soddisfatto e non
     c'è nulla da fare; con la **whitelist esplicita** l'utente deve aggiungere
     a mano `api.todoist.com` (icona ambiente → Network access → Custom →
     Allowed domains). Senza, lo script esce con errore di rete a ogni run.
6. **Spiega la semantica in due righe**, perché è ciò che rende la board
   affidabile: il push è in **sola creazione** (una card già spostata non torna
   mai indietro da sé) e il pull agisce **solo** sul cambio di sezione — quindi
   niente si muove nel repo se non lo muove l'utente. Spostare una card fra i
   gruppi «Da valutare · fit ...» non è una decisione: il sync la registra e
   basta, nel repo non cambia nulla. Se una card viene
   spostata in una sezione che non corrisponde allo stato dei file (es. «Da
   candidare» su un'offerta già scartata), il sync non forza nulla: lo segnala
   nel digest come incongruenza da sistemare a mano.
7. **Cosa fa la promozione da Todoist, e cosa no**: crea la candidatura in
   `applications/` con `status: da_candidare`, copia i materiali già generati e
   congela un `jd.md` con `completezza: non_disponibile` (lo script non ha il
   corpo dell'annuncio e non lo inventa). Restano da fare in chat la cattura
   della JD, la persistenza della valutazione in `role-fit/` e la scadenza di
   follow-up — per questo la voce di staging resta lì marcata `approved`.

Se l'utente dice no (o rimanda): non scrivere il blocco `todoist:`. Senza
blocco, la routine salta il passo e nota una riga nel digest — nessun errore.
Si può attivare in qualunque momento più avanti, questo passo non è una porta
che si chiude.

### 6-ter. Run di validazione (due, non saltarle)

Fin qui hai una routine *dichiarata* attiva. Nessuno l'ha ancora vista arrivare
in fondo: etichetta Gmail, connettori approvati nell'ambiente, secret, push,
gate di veridicità, `JOB_HUNTER_ROUTINE`, branch protection sono tutte cose che
si scoprono rotte **alla prima run reale** — e se quella è la prima run
schedulata, succederà alle cinque del mattino, senza nessuno che interpreti il
risultato. Chiudere qui l'onboarding significa consegnare una configurazione
non verificata.

Servono **due** run, non una: hanno oggetti di verifica diversi e nessuna
sostituisce l'altra.

**Run A — invocazione interattiva, ora, in questa stessa sessione.**

1. **Invoca `job-watch` a mano.** È esplicitamente invocabile a mano, non solo
   schedulata. Attenzione: questa è una sessione **interattiva**, quindi non ha
   `JOB_HUNTER_ROUTINE=1` e non ha i secret dell'ambiente cloud — la run valida
   la catena delle fonti e dei materiali (alert Gmail, connettori, gate di
   veridicità), **non** l'hook di protezione né il sync Todoist, che dipendono
   da secret presenti solo in cloud.
2. **Mostra il digest risultante all'utente** e leggetelo insieme. È anche il
   momento giusto per fargli vedere com'è fatto: da domani ne riceverà uno al
   giorno e deve sapere dove guardare per primo.
3. **Usa la sezione «Anomalie della run» come checklist di sanità**, voce per
   voce. Le anomalie tipiche di un onboarding appena fatto, e cosa dicono
   davvero:
   - *etichetta Gmail vuota o inesistente* → il passo 5 è passato senza il
     filtro, o il nome in `gmail_label` non corrisponde. Torna al passo 5;
   - *connettore assente / fonte saltata* → un connettore non collegato o non
     approvato in **questa** sessione;
   - *gate di veridicità non girato (exit 3)* → `cv-facts.yaml` manca. Non
     dovrebbe, dopo il passo 4: verifica di averlo scritto e committato;
   - *sync Todoist saltato (exit 3)* → in Run A è **atteso**, non un difetto:
     `TODOIST_API_TOKEN` vive solo nei secret dell'ambiente cloud e qui non c'è
     (stesso caso dell'hook di protezione). Dillo all'utente e non rimandarlo a
     debuggare il passo 6-bis. Va verificato per davvero solo in Run B;
   - *zero offerte trovate* → non è di per sé un'anomalia: gli alert appena
     creati non hanno ancora prodotto email. Dillo, così l'utente non lo legge
     come un guasto.

**Run B — la routine cloud vera, triggerata a mano dalla UI.**

La Run A gira con la tua identità e i tuoi permessi, non con quelli della
routine cloud: `JOB_HUNTER_ROUTINE=1` + hook, connettori ri-approvati
*nell'ambiente*, `TODOIST_API_TOKEN`, Network access, permesso di push
dell'identità della routine, branch protection, cron — nessuna di queste è
stata ancora esercitata. Se restano non verificate, il primo test reale è la
prima run schedulata, alle cinque del mattino, senza nessuno che la legga.

4. **Fai triggerare all'utente una run della routine adesso**, dalla UI Routines
   (claude.ai/code → Routines → la routine → "Run now" / esegui ora). È l'unico
   modo di esercitare l'ambiente cloud con qualcuno che guarda.
5. **Leggete insieme l'output/log di quella run** (nella UI della routine) e il
   commit+push che ha prodotto su `main`. Controlla in particolare:
   - la run è arrivata **in fondo** (commit e push su `main` andati a buon
     fine — se il push è fallito: branch protection o permessi dell'identità,
     torna a `routine-setup.md` §1);
   - nessun prompt di conferma rimasto appeso (connettore non approvato
     nell'ambiente → la run si blocca lì non presidiata);
   - se c'è la board Todoist: il passo 6-bis del digest **non** riporta più
     `exit 3` per token/rete; le card sono comparse sul progetto Todoist;
   - le «Anomalie della run» del digest cloud, con lo stesso metro del punto 3.
6. **L'onboarding è completo solo dopo che la Run B è arrivata in fondo** — con
   commit+push su `main` riusciti — e le anomalie di entrambe le run sono
   **comprese e accettate** esplicitamente dall'utente (es. "gli alert sono di
   stamattina, il primo digest sarà magro"). Un'anomalia lasciata lì senza
   diagnosi non è accettata: è rimandata, e tornerà ogni giorno. Una routine
   "dichiarata attiva" ma mai vista arrivare in fondo in cloud **non** chiude
   l'onboarding.

### 7. Utente operativo

Solo a questo punto l'onboarding è completo: profilo scritto, alert impostati, routine attiva **e vista arrivare in fondo almeno una volta in cloud** (passo 6-ter, Run B). Dillo esplicitamente all'utente e ricorda dove vivono i canali con cui interagirà da qui in poi (la bozza del digest in Gmail — da aprire, non da aspettare in posta in arrivo — più la copia nel repo in `digests/`, la chat per lo Studio, e — se ha attivato il passo 6-bis — la board Todoist per le decisioni rapide: ricordagli che le card compaiono solo dopo la prima run della routine, non subito). Ricorda anche che da qui in poi nulla richiede di rifare l'onboarding: i criteri di ricerca si modificano con `job-search-profile` (e dopo ogni modifica gli alert LinkedIn/Indeed si riallineano con `job-alert-config`), mentre il profilo — nuove esperienze, competenze, certificazioni, RAL aggiornata — si aggiorna con `master-profile-editor`, che lavora per delta senza mai ricostruirlo da zero.

## Cosa NON fare

- Non riempire mai un campo con un valore plausibile ma non confermato dall'utente ("assunzione silenziosa").
- Non usare dati di memoria dell'account per rispondere a domande che l'intervista dovrebbe porre all'utente attivo in quel momento — la skill deve funzionare identica per un utente di cui non sai nulla.
- Non saltare la conferma finale prima della scrittura dei file nel repo.
- Non inventare campi fuori schema: se serve un campo nuovo, fermati e segnalalo invece di forzarlo in un campo esistente.
