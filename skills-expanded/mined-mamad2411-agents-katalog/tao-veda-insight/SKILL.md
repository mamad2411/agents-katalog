---
name: tao-veda-insight
description: "Genera bozze di articoli per il Diario di Tao Veda (hub /conoscenza) e contenuti per l'area Formazione (formazione.tao-veda.org), nella voce editoriale Tao Veda. Attiva questa skill SEMPRE quando l'utente menziona 'articolo Tao Veda', 'post per il diario', 'nuovo contenuto per /conoscenza', 'articolo per il blog Tao Veda', 'pillar', 'voce di glossario', 'voce di bibliografia', 'lezione formazione', 'modulo formazione', 'revisione corso', oppure quando fornisce appunti, riflessioni, estratti di dispense (Ayurveda, Medicina Cinese), appunti del corso Hakusha sui Tarocchi, o spunti culturali e chiede di trasformarli in un contenuto pubblicabile. Si attiva anche quando l'utente chiede di pianificare il calendario editoriale del diario o proporre temi. Restituisce file Markdown con front matter conforme alle content collection del repo tao-veda.org (src/content/diario, glossario, bibliografia, tradizioni), pronti per Sveltia CMS o per l'editing su GitHub. NON confondere con la skill veda-insight (sito VEDA Consulting, consulenza marketing) né con tao-veda-mappa-restituzione (questionario)."
---

# Tao Veda Insight Generator

Questa skill produce bozze di contenuti per l'hub culturale **Conoscenza** del sito Tao Veda (`https://www.tao-veda.org/conoscenza`).

Tipi di contenuto, in ordine di frequenza:

1. **Diario** — articoli sempreverdi (`src/content/diario/<slug>.md`).
2. **Glossario** — voci brevi (`src/content/glossario/<slug>.md`).
3. **Bibliografia** — schede di opere con nota ragionata (`src/content/bibliografia/<slug>.md`).
4. **Tradizioni** — pagine pillar (`src/content/tradizioni/<slug>.md`).

Lo schema dei campi è definito in `src/content/config.ts`. **Leggilo prima di emettere un file**: è la fonte di verità e può cambiare.

## Voce editoriale Tao Veda

Tao Veda è un approccio al benessere e una ricerca culturale sul corpo. La voce è **sobria, colta, evocativa ma mai New Age**. La regola di fondo: **affermazioni semplici e dirette di un pensiero, non frasi solenni o costruite.** Una frase, un'idea.

Regole anti-teatralità (vincolanti — sono la versione operativa di `CLAUDE.md`):

- **Scrivi in positivo e in modo diretto.** Di' cosa una cosa È o può diventare. Evita le costruzioni a effetto: "La formula più precisa, oggi, è questa:", "prima di tutto", "con cautela", i chiasmi e gli epigrammi ("non è una formalità — è…", "non è X: è Y").
- **Niente trattino lungo " — " nella prosa.** Usa virgola, due punti, "e", parentesi, o spezza la frase. Il "—" resta solo come separatore nei `<title>` SEO e nei `<cite>`.
- **Riduci al minimo la parola "non".** Elimina le negazioni "a elefante": nominare ciò che nessuno avrebbe pensato fa l'effetto opposto (es. "non una collezione", "non vende trattamenti", "Non è ancora un'associazione…"). Riformula in positivo.

Regole di perimetro e stile (restano valide):

- **Mai clinico o diagnostico.** Niente promesse di guarigione, niente affermazioni mediche, psicologiche o sessuologiche. Coerenza con la Carta dei Principi e con le pagine Confini e Consenso.
- **Totalità al posto dell'elenco.** Si parla del lavoro sulla persona nella sua interezza (etimologia di *olistico*, gr. *hólos*, intero). Non nominare né elencare singole zone "intime" come diverse dal resto: separarle le sessualizza. Ogni parte appartiene allo stesso insieme.
- **Il tema sessuale/generativo** è energia vitale a cui attingere per **sublimarla** in conoscenza e consapevolezza, mai agita, mai esplicita, mai come finalità. È il livello più delicato: trattalo con misura.
- **Consenso continuo.** Il consenso vive nell'ascolto e nei gesti, si rinnova momento per momento e resta revocabile. Niente moduli scritti per singole manualità. Pagina di riferimento: `/consenso`.
- **Niente sensazionalismo**, niente esoterismo di maniera, niente «segreti», «poteri», «miracoli».
- **Cita le fonti.** Quando possibile collega le opere della [bibliografia](https://www.tao-veda.org/conoscenza/bibliografia), i termini del [glossario](https://www.tao-veda.org/conoscenza/glossario) e le [tradizioni](https://www.tao-veda.org/conoscenza/tradizioni).
- **Citazioni** dai classici in `blockquote` con `<cite>` (es. Tao Te Ching), brevi e attribuite. Le citazioni d'autore conservano la loro forma originale, negazioni comprese (es. «il Tao che può essere nominato non è il vero Tao»).
- **"tu" cortese** col lettore; «Tao Veda» in terza persona per il progetto. La prima persona singolare solo se l'articolo è dichiaratamente firmato.
- **Tono rispettoso e inclusivo**, frasi pulite, ritmo disteso.

> Le negazioni che delimitano confini reali restano (perimetro sessuale del principio 6 e di Confini, distinzioni cliniche, disclaimer su Dario): sono sostanza, non teatralità. La regola sul "non" riguarda solo le negazioni retoriche.

## Workflow per un articolo del Diario

### 1. Capire il punto di partenza
Se l'utente passa appunti grezzi (dispense, note Hakusha, riflessioni), leggi tutto e proponi in una riga **il nodo** dell'articolo prima di scrivere. Se manca, chiedi una cosa alla volta:
- la **domanda** o il tema (cosa il lettore porta a casa);
- la **tradizione** prevalente (`tao | veda | kundalini | occidente | tarocchi | pratica`);
- almeno **un collegamento** alla visione Tao Veda (perché questo tema riguarda il corpo come luogo di conoscenza).

### 2. Verificare lo schema
Leggi `src/content/config.ts`: e' la fonte di verita' e puo' cambiare. Schema della collection `diario` al 5 settembre 2026:

```yaml
title: string
description: string            # sommario per liste e meta
data: date                     # YYYY-MM-DD
aggiornato: date               # opzionale
tradizione: enum               # tao | veda | kundalini | occidente | tarocchi | pratica
pillar: enum                   # opzionale: tradizione di riferimento per il cluster
tags: string[]
autore: 'dario-pagnoni'        # valore unico ammesso, e' anche il default
cover: string                  # opzionale, path in /uploads o /assets
ogImage: string                # OBBLIGATORIO: /assets/og/diario-<slug>.png
fonti:                         # OBBLIGATORIO, almeno una voce
  - titolo: string
    url: string                # URL assoluto e verificato
    tipo: primaria | istituzionale | bibliografica
faq:                           # opzionale: Q&A mostrate in pagina, generano lo schema FAQPage
  - domanda: string
    risposta: string
draft: boolean                 # default false
```

Tre campi fanno fallire la validazione se sbagliati: `autore` accetta solo `dario-pagnoni`,
`ogImage` e `fonti` sono obbligatori. L'immagine social va anche generata davvero: aggiungi una
card in `scripts/generate-og-images.mjs` e lancia `npm run og:generate`, altrimenti l'audit in
build si ferma con `og:image locale mancante`.

### 3. Struttura dell'articolo (GEO-friendly)
- **Apertura** che, nelle prime 2-3 frasi, dà una **definizione netta** o un'osservazione chiara (estraibile come risposta diretta dai motori di ricerca e dai motori di risposta AI).
- **2-4 sezioni** con titoli `##` che dicono la cosa, non alludono.
- eventuale **citazione** breve da un classico.
- **chiusura "Per approfondire"**: rimanda a 1-2 opere della bibliografia, ai termini di glossario citati e alla pillar della tradizione.
- Lunghezza utile: **500-900 parole** per gli articoli ordinari.
- **FAQ facoltative**: 3-5 domande nel campo `faq`, solo dove sono domande vere con risposte che
  si reggono da sole. Il template le mostra in fondo alla pagina e genera lo schema FAQPage. La
  roadmap SEO ammette quello schema soltanto dove le risposte sono visibili, e vieta le FAQ
  ripetitive costruite per moltiplicare keyword.

**Da non scrivere nel markdown**, perche' li genera gia' il template
`src/pages/conoscenza/diario/[slug].astro`: il titolo H1, la firma con le date, l'indice (compare
con almeno 3 titoli `##`), il blocco "Domande frequenti", la sezione "Fonti e riferimenti", i tag,
il riquadro "Approfondisci" e la CTA finale.

### 4. Interlinking (pillar + cluster)
Collega in modo naturale, con link Markdown relativi:
- termini → `/conoscenza/glossario#<slug>` (controlla gli slug esistenti in `src/content/glossario/`);
- opere → `/conoscenza/bibliografia#<tradizione>`;
- tradizione → `/conoscenza/tradizioni/<tradizione>`;
- altri articoli → `/conoscenza/diario/<slug>`.
Non forzare i link: solo dove aiutano davvero il lettore.

### 5. Front matter
```yaml
---
title: "<titolo, senza virgolette interne non bilanciate>"
description: "<una frase di sintesi, ~120-200 caratteri>"
data: <YYYY-MM-DD>            # usa la data odierna se non concordata: `date +%Y-%m-%d`
tradizione: <enum>
pillar: <enum>               # di norma uguale alla tradizione; ometti se non pertinente
tags: ["...", "..."]
autore: "dario-pagnoni"
ogImage: "/assets/og/diario-<slug>.png"
fonti:
  - titolo: "<titolo della fonte>"
    url: "<URL verificato>"
    tipo: "istituzionale"
faq:                         # opzionale, solo per domande reali
  - domanda: "<domanda>"
    risposta: "<risposta che si regge da sola>"
draft: false
---
```
- **Slug del file:** minuscole, trattini, 4-7 parole, senza preposizioni inutili. Es. `cinque-movimenti-leggere-il-corpo`, `via-del-drago-e-kundalini`.
- **data:** verifica la data corrente con `date +%Y-%m-%d`.

### 6. Rilettura
Applica `references/checklist.md`. Se un punto fallisce, correggi prima di emettere.

### 7. Salvataggio
Salva in `src/content/diario/<slug>.md` e comunica: slug e path, titolo, sommario, tradizione, stato `draft`, e il prossimo passo (revisione su GitHub o pubblicazione via Sveltia CMS su `/admin`).

## Glossario, bibliografia, tradizioni (contenuti brevi)
- **Glossario:** `termine`, `tradizione`, `definizione` (1-2 frasi atomiche, GEO), `sinonimi?`, `vediAnche?` (slug), `ordine`. Una parola, una voce. Niente body se non serve.
- **Bibliografia:** `titolo`, `autore`, `anno?`, `titoloOriginale?`, `tradizione`, `livello` (`fondamentale|approfondimento|contemporaneo`), `descrizione` (la nota ragionata: perché conta per Tao Veda), `ordine`. Verifica sempre l'accuratezza dei dati bibliografici; in caso di dubbio sul titolo italiano, usa il titolo originale.
- **Tradizioni (pillar):** `titolo`, `tradizione` (= slug del file), `eyebrow`, `sommario` (apertura GEO), `ordine`, + corpo con 2-3 sezioni e link al cluster.

## Pianificazione editoriale
- **Frequenza:** almeno 2 articoli al mese. Meglio costanza che picchi.
- **Mix di tradizioni:** ogni 4 articoli, copri almeno 3 delle 6 correnti. Valorizza i ponti Oriente↔Occidente (es. Hakusha: arcani e chakra; Jung e kundalini).
- **Temi che funzionano:** una parola-chiave spiegata in profondità, un parallelo fra tradizioni, la lettura di un classico, una pratica di presenza, un equivoco comune da chiarire.
- **Temi da evitare:** promesse terapeutiche, oroscopi/divinazione, contenuti celebrativi, riassunti di terzi.
- Quando l'utente chiede idee, proponi 3-4 spunti (tema, taglio, tradizione, collegamenti) e aspetta che scelga. La banca spunti è in `references/idee-rubrica.md`.

## Lezioni dell'area Formazione
Per scrivere o rivedere corsi, moduli e lezioni di `formazione.tao-veda.org` (collection in `formazione/src/content/`), segui `references/lezioni-formazione.md`: schema dei campi, forma delle lezioni per tipo, regola "meno difensivo" e regola della durata onesta. Le regole di voce di questa skill valgono per intero anche lì.

## File di riferimento
- `references/template-articolo.md` — template pronto da compilare.
- `references/checklist.md` — checklist di rilettura.
- `references/idee-rubrica.md` — banca di spunti editoriali.
- `references/lezioni-formazione.md` — schema e regole per i contenuti dell'area Formazione.

## Attivare la skill fuori dal repo
La skill vive nel repo per restare versionata col sito. Per usarla come skill globale, copia la cartella `docs/skills/tao-veda-insight/` nella cartella delle skill utente, oppure usa `skill-creator` per importarla.
