---
name: project-brief
version: 1.0.0
description: Turn a rough client request into a structured project brief with phases, tasks, owners, deadlines and risks. Ready to paste into Asana, ClickUp or Notion.
author: MarcoZorn
license: MIT
tags: [agency, workflow, operations, planning]
compatible: claude-code, codex-cli, cursor, gemini-cli, openclaw
---

# Project Brief

## When to use this skill

**English:** "new project", "start a project", "client brief", "project kickoff", "set up a new client project", "scope this project".

**Italiano:** "nuovo progetto", "nuovo cliente", "brief progetto", "imposta progetto", "kickoff".

## What this skill does

Takes a vague, half-formed client request and turns it into a complete project brief a whole team can execute from: a clear objective, the operational phases, a task list with owners and deadlines, and the risks worth naming before they become fires. The output is structured so it can be pasted straight into a project management tool without reformatting.

## Inputs required

Before generating anything, ask these five questions and wait for the answers. Do not guess.

1. **Client name** — who is this for?
2. **Service type** — social media management, video production, web build, branding, campaign, retainer, other?
3. **Deadline** — hard delivery date, or the first milestone if it is an ongoing retainer.
4. **Budget range** — even a rough band. It sets the ambition and the team size.
5. **Main KPI** — the one number that defines success (followers, leads, sales, views, delivery on time).

If the user cannot answer one, mark it `TBD` in the output and add a task to confirm it. Never invent a budget or a deadline.

## Output format

Two blocks, in this order:

1. **RECAP PROGETTO** — the header card: client, service, objective, deadline, owner, teams, status, priority.
2. **FASI OPERATIVE** — a phase table.
3. **TASK** — the task list.
4. **RISCHI E BLOCCHI** — named risks with impact and mitigation.

Everything is plain Markdown tables and lists so it survives a copy-paste into Asana, ClickUp or Notion.

---

## Brand voice

If a `BRAND.md` file exists in this skill's folder (`.claude/skills/project-brief/BRAND.md`) or in `.claude/brand/BRAND.md` (global fallback), read it before generating output and apply its tone, terminology, and examples to all text you produce. A skill-local `BRAND.md` overrides the global one; if neither exists, use a clean, professional default voice.

## Instructions

You are producing an operational brief, not a proposal and not a pitch. Assume the project is already sold. Your job is to make it executable.

### 1. Confirm the inputs

Ask the five questions above in a single message. Keep them tight. When the answers come back, restate them in one line so the user can catch a misread before you build on it.

### 2. Derive the objective

Turn the KPI and service type into one sentence a team member could read and immediately know what "done well" looks like. Bad: "grow social media". Good: "Grow Bloom Studio's Instagram from 8k to 12k engaged followers in 90 days, driving 40+ qualified DMs/month to the booking link."

### 3. Assign an owner and priority

- **Responsabile / Owner** — one named person accountable for the whole brief. If unknown, write `TBD — assign at kickoff` and add it as the first task.
- **Priorità** — High / Medium / Low. High = revenue-critical or hard external deadline. Medium = important, some slack. Low = nice-to-have, movable.

### 4. Build the phases

Break the work into 3–6 operational phases. Each phase has: name, owner, expected output, deadline, status (default `Da fare / To do`). Phases should be sequential milestones a client would recognise — Discovery, Concept, Production, Review, Delivery — adapted to the service type.

### 5. Build the task list

Explode each phase into concrete tasks. Every task has an owner, a deadline, a priority and a one-line description of the deliverable. Deadlines must work backwards from the final delivery date and leave buffer. Do not create a task without a named or `TBD` owner — an unowned task is a task that will not happen.

### 6. Name the risks

List 2–4 real risks. For each: the risk, its impact if it lands, and a concrete mitigation. Focus on the boring killers — late client feedback, unclear assets, scope creep, single points of failure — not hypotheticals.

### Output template

```
RECAP PROGETTO
Cliente: [name]
Servizio: [type]
Obiettivo: [one clear sentence tied to the KPI]
Deadline: [date]
Responsabile: [owner]
Reparti coinvolti: [teams]
Stato: Da fare
Priorità: [High / Medium / Low]

FASI OPERATIVE
| Fase | Responsabile | Output atteso | Deadline | Stato |
|------|--------------|---------------|----------|-------|
| ...  | ...          | ...           | ...      | Da fare |

TASK
| Task | Responsabile | Deadline | Priorità | Descrizione |
|------|--------------|----------|----------|-------------|
| ...  | ...          | ...      | ...      | ...         |

RISCHI E BLOCCHI
| Rischio | Impatto | Soluzione |
|---------|---------|-----------|
| ...     | ...     | ...       |
```

### Edge cases

- **Ongoing retainer, no end date:** use the first monthly cycle as the deadline horizon and note it recurs.
- **Multiple deliverables in one project:** create a phase per deliverable rather than cramming them into tasks.
- **Client gave you everything in one paragraph:** still ask the five questions — a paragraph rarely contains a real deadline or KPI.
- **User pushes to skip the questions:** produce the brief but mark every unconfirmed field `TBD` and open the brief with a one-line warning that the plan rests on assumptions.

---

## 🇮🇹 Versione italiana

### Quando usare questa skill

Usala quando parte un nuovo progetto o un nuovo cliente: "nuovo progetto", "nuovo cliente", "brief progetto", "kickoff". Trasforma una richiesta vaga del cliente in un brief operativo che tutto il team può eseguire.

### Cosa fa

Prende una richiesta grezza e la trasforma in un brief completo: obiettivo chiaro, fasi operative, lista task con responsabili e scadenze, rischi da nominare prima che diventino incendi. L'output è pronto da incollare in Asana, ClickUp o Notion senza riformattare.

### Cosa ti serve (chiedilo prima di generare)

Fai queste cinque domande e aspetta le risposte. Non tirare a indovinare.

1. **Nome cliente** — per chi è?
2. **Tipo di servizio** — gestione social, produzione video, sito, branding, campagna, retainer, altro?
3. **Deadline** — data di consegna, o la prima milestone se è un retainer continuativo.
4. **Range di budget** — anche approssimativo. Definisce l'ambizione e la dimensione del team.
5. **KPI principale** — il numero che definisce il successo (follower, lead, vendite, view, consegna nei tempi).

Se manca un dato, scrivi `TBD` nell'output e aggiungi un task per confermarlo. Non inventare mai budget o deadline.

### Voce del brand

Se esiste un file `BRAND.md` nella cartella di questa skill (`.claude/skills/project-brief/BRAND.md`) o in `.claude/brand/BRAND.md` (fallback globale), leggilo prima di generare l'output e applica tono, terminologia ed esempi a tutto il testo che produci. Il `BRAND.md` locale ha la precedenza su quello globale.

### Istruzioni

Stai producendo un brief operativo, non una proposta e non un pitch. Il progetto è già venduto. Il tuo compito è renderlo eseguibile.

1. **Conferma gli input.** Fai le cinque domande in un solo messaggio. Alla risposta, ripeti in una riga per farti correggere subito.
2. **Deriva l'obiettivo.** Una frase da cui chiunque nel team capisca cosa significa "fatto bene", legata al KPI.
3. **Assegna responsabile e priorità.** Un solo responsabile accountable. Priorità Alta / Media / Bassa.
4. **Costruisci le fasi.** Da 3 a 6 fasi operative, sequenziali, ciascuna con responsabile, output, deadline e stato (default `Da fare`).
5. **Costruisci i task.** Esplodi ogni fase in task concreti, ognuno con responsabile, scadenza, priorità e descrizione. Nessun task senza responsabile (anche `TBD`).
6. **Nomina i rischi.** Da 2 a 4 rischi reali: rischio, impatto, soluzione concreta. Concentrati sui killer noiosi — feedback cliente in ritardo, asset poco chiari, scope creep, single point of failure.

### Template di output

```
RECAP PROGETTO
Cliente: [nome]
Servizio: [tipo]
Obiettivo: [una frase chiara legata al KPI]
Deadline: [data]
Responsabile: [owner]
Reparti coinvolti: [team]
Stato: Da fare
Priorità: [Alta / Media / Bassa]

FASI OPERATIVE
| Fase | Responsabile | Output atteso | Deadline | Stato |
|------|--------------|---------------|----------|-------|

TASK
| Task | Responsabile | Deadline | Priorità | Descrizione |
|------|--------------|----------|----------|-------------|

RISCHI E BLOCCHI
| Rischio | Impatto | Soluzione |
|---------|---------|-----------|
```

### Casi limite

- **Retainer continuativo senza data di fine:** usa il primo ciclo mensile come orizzonte e segnala che è ricorrente.
- **Più deliverable in un progetto:** una fase per deliverable, non tutto stipato nei task.
- **Cliente che dà tutto in un paragrafo:** fai comunque le cinque domande.
- **L'utente vuole saltare le domande:** genera il brief ma marca ogni campo non confermato come `TBD` e apri con un avviso di una riga che il piano poggia su assunzioni.
