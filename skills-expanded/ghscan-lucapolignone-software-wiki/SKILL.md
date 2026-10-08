---
description: Inizializza una wiki di prodotto software in questo progetto. Crea raw/, wiki/ con sottocartelle, copia CLAUDE.md alla radice, popola index/log/overview/glossary di partenza. Da invocare in un repo dove la wiki non esiste ancora.
disable-model-invocation: true
argument-hint: "[nome-prodotto]"
---

# Bootstrap di una nuova wiki

Inizializzi una wiki di prodotto software in questo progetto seguendo lo schema della skill `software-wiki:conventions`.

## Pre-flight

1. Verifica che la wiki NON esista già: se `./CLAUDE.md` o `./wiki/` esistono, **fermati** e segnalalo all'utente (potrebbe già essere bootstrappata, o c'è un conflitto). Proponi `/software-wiki:ingest` come prossimo passo se è già impostata.
2. Carica lo schema da `software-wiki:conventions/assets/CLAUDE.md` se non l'hai già in contesto. È la fonte di verità per la struttura.

## Interview

Chiedi all'utente (e aspetta le risposte prima di procedere):

1. **Nome del prodotto** — se `$ARGUMENTS` contiene già un nome, conferma quello.
2. **Fonti grezze esistenti** — c'è già una cartella di documenti? In che formato? Vanno spostate dentro `raw/` ora o le aggiungerà l'utente dopo?
3. **Personalizzazioni** rispetto allo schema di default:
   - Sotto-cartelle `tech/` aggiuntive (es. `tech/protocols/`, `tech/security/`)?
   - Status custom per le feature (es. `internal-only`, `private-beta`, `ga`)?
   - Owner team obbligatorio anche su feature, non solo component?
   - Frontmatter di dominio (es. `compliance: [gdpr, soc2]`)?

## Esecuzione

Una volta confermate le risposte:

1. **Crea la struttura** secondo lo schema (`raw/`, `wiki/index.md`, `wiki/log.md`, `wiki/overview.md`, `wiki/glossary.md`, `wiki/features/`, `wiki/user/{tasks,concepts,reference,troubleshooting}/`, `wiki/tech/architecture.md`, `wiki/tech/{components,apis,data-models,infra,runbooks}/`, `wiki/decisions/`, `wiki/sources/`).

2. **Copia lo schema in `./CLAUDE.md`** alla radice del progetto. Applica le personalizzazioni concordate prima di scrivere il file (es. aggiungi sotto-cartelle, modifica status, ecc.).

3. **Popola le pagine iniziali**:
   - `wiki/index.md` — sezioni stub per ciascuna categoria (Features, User concepts, Tech components, ADR, Sources). Ogni sezione vuota con commento `<!-- popolare con la prima ingest -->`.
   - `wiki/log.md` — prima voce: `## [YYYY-MM-DD] decision | bootstrap della wiki` con nota tipo "Wiki inizializzata. Schema in CLAUDE.md. Personalizzazioni: ...".
   - `wiki/overview.md` — frontmatter `type: concept`, titolo con nome prodotto, breve frase placeholder: "Da popolare dopo le prime ingest. Sintetizza qui chi sono gli utenti, l'architettura macro, e i temi caldi."
   - `wiki/glossary.md` — frontmatter `type: concept`, titolo "Glossario", elenco vuoto pronto.

4. **Riepiloga** all'utente:
   - Path delle directory create.
   - Quali personalizzazioni sono state applicate al `CLAUDE.md`.
   - Se l'utente ha già fonti pronte, proponi di iniziare con `/software-wiki:collect` (per raccoglierle in `raw/`) seguito da `/software-wiki:ingest <source>` (per processarle una alla volta).
   - Se non ne ha, suggerisci di committare lo stato iniziale in git prima di andare avanti.

## Note

Se l'utente preferisce un nome di plugin diverso o personalizzazioni invasive (es. non vuole `tech/` separato da `user/`), lo schema può essere modificato in `CLAUDE.md` dopo il bootstrap — logga il cambio come `refactor` in `wiki/log.md`.
