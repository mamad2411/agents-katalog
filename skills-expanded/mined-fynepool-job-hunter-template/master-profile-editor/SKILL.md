---
name: master-profile-editor
description: >-
  Editor del profilo del candidato del sistema Job Hunter (master-profile.yaml
  nella radice del repo: CHI è l'utente — esperienze, skill, lingue,
  formazione, certificazioni, retribuzione, vincoli, preferenze). Usa SEMPRE
  questa skill quando l'utente vuole aggiornare un dato del proprio profilo
  DOPO l'onboarding: "aggiungi questa certificazione", "ho preso questo
  attestato", "aggiorna la mia RAL / le mie aspettative economiche", "ho
  cambiato lavoro", "aggiungi questa esperienza", "ho imparato Kubernetes",
  "aggiungi questa competenza", "correggi il mio profilo", "ho cambiato
  città", "è cambiato il mio preavviso", "ecco il mio CV aggiornato". Il
  profilo è CUMULATIVO: si aggiorna per delta, non si ricostruisce mai da
  zero. NON usare per i criteri di ricerca (ruoli cercati, location, alert,
  esclusioni): quello è mestiere di job-search-profile. NON usare per
  l'onboarding iniziale di un sistema vergine: quello è agent-config. NON
  usare per generare un CV su misura per una posizione: quello è cv-tailoring.
---

# master-profile-editor

Modulo 1.1.1 del progetto Job Hunter. Mantiene nel tempo il `master-profile.yaml` **già esistente**: il nucleo condiviso che descrive CHI è l'utente e che alimenta tutto il resto del sistema (`role-fit` per il giudizio, `cv-tailoring` per i materiali, il gate di veridicità per i numeri). La nascita del profilo e lo schema canonico vivono in `agent-config` (1.1) — questa skill non li duplica: qui si aggiorna un profilo che c'è già.

È la controparte di `job-search-profile` (1.2) sull'altro artefatto: **quella tocca solo `searches/` (cosa cerchi), questa tocca solo `master-profile.yaml` (chi sei)**. Nessuna delle due sconfina nell'altra.

**Requisito non negoziabile 2 del progetto — profilo cumulativo**: il master-profile non si ricostruisce mai da zero. Ogni intervento è un **delta** su un file esistente: si aggiunge, si corregge, si aggiorna un campo, preservando intatto tutto il resto. Un profilo rigenerato da capo perde ciò che l'utente aveva confermato a mano in sessioni precedenti (sfumature, note, correzioni al CV) e non è recuperabile se non dalla storia git.

## Precondizioni di readiness

Prima di modificare, verifica il prerequisito minimo di questa skill: esiste `master-profile.yaml` nella radice del repo ed è non vuoto. Se manca o è vuoto/placeholder, l'utente non ha ancora fatto l'onboarding: non creare qui un profilo parziale a partire dalla singola cosa che ti ha appena detto — nascerebbe monco, saltando le domande su vincoli, retribuzione e diritto al lavoro. Fermati e reindirizza ad `agent-config` con una frase specifica al gap reale, es.: "Per aggiungere questa certificazione mi serve il tuo profilo, che non risulta ancora configurato: vuoi che partiamo dall'onboarding per crearlo adesso? Bastano pochi minuti e una copia del tuo CV — la certificazione la mettiamo dentro strada facendo."

## Cosa fa / cosa NON fa

- FA: legge `master-profile.yaml`, applica le modifiche puntuali richieste dall'utente (nuova esperienza, nuova skill/certificazione/formazione, aggiornamento di retribuzione, preavviso, mobilità, lingue, link esterni, adozione AI, preferenze generali), valida contro lo schema, mostra il diff, riscrive il file preservando tutto il resto e committa.
- NON FA: modificare `searches/` (criteri di ricerca → `job-search-profile`), `role-fit/`, `applications/`; creare il primo profilo su un sistema vergine (→ `agent-config`); generare CV/cover (→ `cv-tailoring`); inventare campi fuori schema; ricostruire il profilo da zero.

## Schema di riferimento (contratto)

Lo schema canonico è `master-profile.schema.yaml` dentro la skill `agent-config` (percorso in-repo `.claude/skills/agent-config/references/master-profile.schema.yaml`). Leggilo PRIMA di scrivere: definisce campi validi, enum chiusi e formati. NON esiste una copia dello schema qui dentro — è voluto, per avere un'unica fonte di verità.

Vincoli che si sbagliano più spesso, da verificare esplicitamente prima di scrivere:

- **Enum chiusi** — `diritto_al_lavoro.stato` (`si|no|da_verificare`), `categoria_protetta` (`si|no|preferisco_non_rispondere` — campo opzionale che FILTRA a monte: se lo tocchi, ricorda all'utente al passo 5 che cambia quali offerte la routine gli mostra), `disponibilita_trasferimento` (`si|no|solo_alcune_aree`), `disponibilita_remoto` (`full_remote|ibrido|solo_sede|indifferente`), `retribuzione.*.lordo_netto` (`lordo|netto`) e `periodicita` (`annuo|mensile`), `esperienze[].tipo_ruolo`, `progetti[].contesto`, `livello_per_skill[].livello`, `lingue[].livello` (scala CEFR + `madrelingua`), `strato_ai_adoption.livello_autonomia`, `preferenze_generali.dimensione_azienda_preferita`. Un valore fuori enum non è "quasi giusto": rompe i consumatori a valle. Se il dato dell'utente non entra in nessun valore dell'enum, dillo e chiedi come mapparlo — non inventare un valore nuovo.
- **Formati** — `esperienze[].periodo.da/a` in `YYYY-MM` (`a: "presente"` per il ruolo corrente); `durata_mesi` è **derivato**: ricalcolalo tu quando tocchi un periodo, non lasciarlo incoerente.
- **Campi vuoti** — un campo che l'utente non sa o non vuole dichiarare resta vuoto/null. Non riempirlo con un valore plausibile (stessa regola anti-assunzione-silenziosa di `agent-config`).

Se la richiesta non ha posto nello schema (es. "segna che ho la patente B"): dillo esplicitamente, NON forzare il dato in un campo affine (`note_libere` come discarica) e NON inventare un campo nuovo. Un campo nuovo è un'evoluzione dello schema, che si decide a livello di progetto.

## Precondizioni tecniche

**Repo del sistema** — sei in una sessione Claude Code su un clone del repo (nessun `tool_search`: `master-profile.yaml` è un file locale, non un connettore). Da chat claude.ai pura il connettore GitHub è di sola lettura: puoi mostrare la modifica ma non scriverla — dichiaralo e rimanda il salvataggio a una sessione Claude Code.

**Mai dalla routine** — `master-profile.yaml` è di proprietà delle sessioni interattive (D5). Nelle sessioni con `JOB_HUNTER_ROUTINE=1` l'hook `.claude/hooks/protect-files.sh` blocca meccanicamente la scrittura: se ti trovi lì, non aggirarlo — la routine non aggiorna profili, punto.

## Flusso

### 1. Leggi lo stato attuale e risolvi il campo bersaglio

Leggi `master-profile.yaml`. Se lo YAML è corrotto/non parsabile: mostra all'utente il contenuto grezzo e l'errore, chiedi come procedere (correzione guidata campo per campo) — NON riscrivere silenziosamente un file che non riesci a leggere, e NON rigenerarlo dal CV per "ripartire pulito".

Risolvi QUALE campo tocca la richiesta e dichiaralo ("lo metto in `certificazioni`"). Le richieste ambigue vanno chieste, non indovinate. Casi ricorrenti:

- *"ho fatto un corso su X"* → `formazione` o `certificazioni`? Dipende se rilascia un attestato verificabile: chiedi.
- *"ora uso anche Terraform"* → `skill_tecniche.piattaforme_e_tool` (elenco) e/o `livello_per_skill` (con livello e anni): chiedi il livello solo se l'utente vuole quella granularità, non forzarla.
- *"ho cambiato ruolo in azienda"* → è una NUOVA voce in `esperienze` o l'aggiornamento di quella corrente? Cambia come il CV racconterà la progressione: chiedi.
- *"guadagno di più"* → `retribuzione.attuale` (e chiedi se cambia anche `aspettativa`, che non si aggiorna da sola).

### 2. Verifica il dato prima di scriverlo (il profilo è la fonte di verità dei materiali)

Questo file non è un appunto personale: è ciò contro cui viene misurato ogni CV generato. `scripts/verify_cv_facts.py` confronta i claim numerici dei materiali con `master-profile.yaml` e blocca quelli non tracciabili. Conseguenza pratica: **un numero scritto qui diventa automaticamente un claim legittimo in tutti i CV futuri**, senza ulteriori controlli.

Quindi, per ogni dato quantificato che stai per scrivere (`risultati_quantificabili`, `anni_esperienza`, `durata_mesi`, valori di `retribuzione`):

- Scrivilo **come l'utente può sostenerlo in un colloquio**, non come suona meglio: se il dato è stimato o approssimato, dillo nel testo del risultato ("~30% su base trimestrale") invece di arrotondare in silenzio verso l'alto.
- Se l'utente propone una metrica vaga ("ho migliorato molto le performance"), chiedi il numero o registra il risultato senza numero — un risultato qualitativo onesto vale più di una cifra inventata che poi il gate lascia passare perché ormai è "nel profilo".
- NON toccare `cv-facts.yaml` per far quadrare qualcosa: quel file è dell'utente, e un agente può al massimo *proporre* una voce (è scritto nel file stesso). L'allowlist esiste per le metriche legittime **assenti** dal profilo, non per legittimare ciò che stai scrivendo ora.

### 3. Mostra il diff, poi conferma

Prima di scrivere, mostra SEMPRE un confronto prima/dopo dei soli campi toccati (non l'intero file, salvo richiesta). Puoi appoggiarti al **diff git reale** (`git diff` dopo aver scritto in locale, prima del commit) invece di un confronto simulato — è più affidabile. Modifiche multiple in un'unica richiesta: un solo diff, una sola conferma. Aspetta conferma esplicita.

Se la modifica **sovrascrive** un dato preesistente (correzione di una data, di una RAL, di una descrizione), dillo a chiare lettere nel diff: sostituire non è aggiungere, e il valore vecchio sparisce dall'HEAD (resta solo nella storia git).

### 4. Riscrivi il file + commit

Riscrivi `master-profile.yaml` completo, preservando INTATTI tutti i campi non toccati — inclusi commenti, ordine delle sezioni e formulazioni che l'utente aveva già confermato. Confronta il file in uscita con quello in entrata: l'unica differenza devono essere i campi confermati al passo 3. Poi **committa** tu (D7 — l'utente non tocca git), con messaggio chiaro (es. `profile: aggiunta certificazione AWS SAA`).

Se la scrittura/commit fallisce: mostra in chat lo YAML aggiornato così l'utente non perde la modifica, spiega il problema e ritenta solo la parte fallita.

### 5. Promemoria a valle (obbligatorio, non opzionale)

Dopo ogni scrittura riuscita, segnala le conseguenze in base ai campi toccati. Segnala e proponi: non eseguire da solo modifiche su altri artefatti.

- **Nuova esperienza, salto di seniority, nuovo stack forte** → i tuoi intenti in `searches/` potrebbero essere disallineati (`seniority`, `ruoli_target`): proponi `job-search-profile`, e da lì eventualmente `job-alert-config` per riallineare gli alert. Il profilo che cambia NON aggiorna le ricerche da solo.
- **`lingue` modificate** → `defaults.lingue_annuncio` (quali lingue accetti negli annunci) è un'altra cosa e non si aggiorna da sola: proponi `job-search-profile` se la modifica la rende obsoleta.
- **`preferenze_generali.settori_*`** → ricorda la distinzione: qui i settori **pesano** nel giudizio di `role-fit`, non filtrano niente. Se l'utente vuole smettere di *vedere* annunci di un settore, serve `settori.esclusi` nell'intento (`job-search-profile`).
- **`retribuzione` modificata** → entra nelle considerazioni di `role-fit` sui range retributivi degli annunci; le valutazioni già salvate in `role-fit/` NON si riscrivono (sono fotografie datate), semmai si rivaluta un annuncio specifico su richiesta.
- **`categoria_protetta` modificata** → cambia quali offerte la routine `job-watch` scarta a monte al prossimo run (esito `scartato_idoneita`): `si` fa ricomparire le offerte riservate alle categorie protette, `no`/`preferisco_non_rispondere` le fa sparire. Nessuna azione manuale sugli alert. Le voci già in `staging/` non si rivalutano da sole: se l'utente vuole, si ripuliscono col triage in blocco di `application-tracker`.
- **Qualunque modifica** → i materiali già generati in `staging/` e `applications/*/materials/` restano quelli di prima: se una candidatura è in corso e il dato cambiato è rilevante, dillo.
- **Disciplina push**: la routine cloud vede solo lo stato committato *e pushato*. Dopo il commit esegui tu il push (D7).

## Aggiornamento a partire da un CV nuovo (delta, mai ricostruzione)

Se l'utente carica un CV aggiornato ("ecco il mio CV nuovo, aggiorna il profilo"), NON rifare l'ingestione da zero e NON sovrascrivere il file con quanto estratto dal documento. Procedura:

1. Estrai dal CV i dati come farebbe `agent-config`.
2. **Confrontali con il profilo esistente** e presenta tre elenchi separati: (a) NOVITÀ da aggiungere, (b) DIFFERENZE su dati già presenti (con vecchio e nuovo affiancati), (c) dati presenti nel profilo ma ASSENTI dal CV.
3. Sul gruppo (c) la regola è: **non cancellare**. Un CV è un documento tagliato per un pubblico, non lo stato completo della persona — l'assenza di una voce nel CV non significa che vada rimossa dal profilo. Chiedi voce per voce solo se l'utente vuole davvero eliminarne qualcuna.
4. Applica solo ciò che l'utente conferma, poi diff + commit come al flusso normale.

## Cosa NON fare

- Non ricostruire il profilo da zero, per nessun motivo (requisito non negoziabile 2). Neanche "per pulizia", neanche se il file sembra disordinato.
- Non cancellare esperienze, progetti o certificazioni passate perché "non servono più": il master-profile è cumulativo; è `cv-tailoring` a decidere cosa mostrare per una specifica posizione.
- Non scrivere senza il diff + conferma del passo 3.
- Non riempire campi collaterali con default plausibili non richiesti, e non usare la memoria dell'account per dedurre valori: la skill deve funzionare identica per un utente di cui non sai nulla.
- Non toccare `searches/`, `role-fit/`, `applications/`, `cv-facts.yaml` da qui.
- Non rilanciare l'intervista completa di onboarding per una modifica puntuale.
