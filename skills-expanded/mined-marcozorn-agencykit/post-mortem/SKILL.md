---
name: post-mortem
version: 1.0.0
description: Run a fast, blame-free project retrospective — what worked, what didn't, root causes and three concrete changes — and append a structured entry to LESSONS.md.
author: MarcoZorn
license: MIT
tags: [agency, workflow, operations, retrospective]
compatible: claude-code, codex-cli, cursor, gemini-cli, openclaw
---

# Post-Mortem

## When to use this skill

**English:** "post-mortem", "retrospective", "project done", "lessons learned", "wrap-up", "close out the project".

**Italiano:** "post-mortem", "retrospettiva", "progetto chiuso", "lezioni apprese", "chiusura progetto".

## What this skill does

Runs a tight retrospective on a finished project and turns it into learning the agency keeps. It separates what to keep doing from what to stop, digs one level past the symptom to the root cause, and commits to three concrete changes for next time. Then it appends a structured entry to `LESSONS.md` in the project root, so the lesson survives past the meeting nobody wrote down.

## Inputs required

1. **Project name** and a one-line description of what it was.
2. **Outcome** — delivered on time / late, on budget / over, client happy / not.
3. **What the team felt went well and badly** — gather a few honest points; if the user only gives one side, prompt for the other.
4. **Any hard numbers** — hours vs estimate, revisions, margin if known.

The tone is blame-free. The goal is better systems, not a search for who to fault. If the input names a person as "the problem", reframe it as a process gap.

## Output format

1. **WHAT WORKED** — keep doing.
2. **WHAT DIDN'T** — stop or fix.
3. **ROOT CAUSES** — 1–2 per issue, one level past the symptom.
4. **THREE CHANGES** — concrete actions for the next similar project.
5. **LESSONS.md ENTRY** — a structured block appended to the project's `LESSONS.md`.

---

## Brand voice

If a `BRAND.md` file exists in this skill's folder (`.claude/skills/post-mortem/BRAND.md`) or in `.claude/brand/BRAND.md` (global fallback), read it before generating output and apply its tone, terminology, and examples to all text you produce. A skill-local `BRAND.md` overrides the global one; if neither exists, use a clean, professional default voice.

## Instructions

### 1. What worked — name it so it repeats

List the things that genuinely helped: a process, a decision, a person's call, a tool. Be specific enough that it can be deliberately repeated. "Good communication" is not a lesson; "daily 5-minute standup kept the client's feedback from piling up" is.

### 2. What didn't — without blame

List what hurt: delays, rework, scope creep, thin margin, a missed dependency. State it factually. Where a name comes up, translate it into the system that let it happen — "the edit sat for three days" not "Marco was slow". You are fixing the machine, not the operator.

### 3. Root causes — go one level deeper

For each problem, ask why once or twice until you hit something you can actually change. "Revisions ballooned" → because "the brief had no locked reference" → because "we started before the moodboard was approved". The last one is the lesson. Stop at the first cause you have the power to fix.

### 4. Three changes — concrete, next-project ready

Exactly three. Each is a specific, adoptable change, not an aspiration. "Lock the moodboard before production starts, no exceptions" beats "communicate better". Where possible, tie a change to an existing skill or artifact — e.g. "run the `project-brief` skill at kickoff so the KPI is locked".

### 5. Append to LESSONS.md

Write a structured entry and append it to `LESSONS.md` in the project root. If the file does not exist, create it with a header. Never overwrite existing entries — append. The entry is dated and named so the log stays searchable over time.

Check whether `LESSONS.md` exists before writing. If it does, append below the last entry. If not, create it with a top-level heading `# Lessons Learned` and then the entry.

### Output template

```
POST-MORTEM — [Project]
Outcome: [on time? on budget? client happy?]

WHAT WORKED (keep doing)
• ...

WHAT DIDN'T (stop or fix)
• ...

ROOT CAUSES
• [Problem] → [why] → [root cause you can fix]

THREE CHANGES FOR NEXT TIME
1. ...
2. ...
3. ...
```

LESSONS.md entry format (appended):

```
## [Date] — [Project]
**Outcome:** [summary]
**Worked:** [1-line]
**Didn't:** [1-line]
**Root cause:** [1-line]
**Changes adopted:**
- [change 1]
- [change 2]
- [change 3]
```

### Edge cases

- **Project went well:** still run it — success has repeatable causes worth naming, and the "what didn't" section can be small but should not be empty.
- **Only one person available:** run it solo but flag that a single perspective is partial and worth cross-checking with the team.
- **Recurring client:** scan prior `LESSONS.md` entries for the same client and note if a lesson is repeating — a repeated lesson is a change that never actually got adopted.
- **Blame in the input:** acknowledge the frustration, then convert every personal criticism into a process fix before it lands in the log.

---

## 🇮🇹 Versione italiana

### Quando usare questa skill

A progetto finito: "post-mortem", "retrospettiva", "progetto chiuso", "lezioni apprese". Fa una retrospettiva veloce e la trasforma in apprendimento che l'agenzia conserva.

### Cosa fa

Separa cosa continuare a fare da cosa smettere, scava un livello oltre il sintomo fino alla causa radice, e si impegna su tre cambiamenti concreti. Poi aggiunge una voce strutturata a `LESSONS.md` nella root del progetto, così la lezione sopravvive alla riunione che nessuno ha verbalizzato.

### Cosa ti serve

1. **Nome progetto** e una riga su cos'era.
2. **Esito** — nei tempi / in ritardo, nel budget / oltre, cliente contento / no.
3. **Cosa è andato bene e male** — raccogli qualche punto onesto; se arriva un solo lato, chiedi l'altro.
4. **Numeri concreti** — ore vs stima, revisioni, margine se noto.

Tono senza colpe. L'obiettivo sono sistemi migliori, non trovare un colpevole. Se l'input indica una persona come "il problema", riformula come lacuna di processo.

### Voce del brand

Se esiste un file `BRAND.md` nella cartella di questa skill (`.claude/skills/post-mortem/BRAND.md`) o in `.claude/brand/BRAND.md` (fallback globale), leggilo prima di generare l'output e applica tono, terminologia ed esempi a tutto il testo che produci. Il `BRAND.md` locale ha la precedenza su quello globale.

### Istruzioni

1. **Cosa ha funzionato — nominalo così si ripete.** Specifico abbastanza da poterlo ripetere di proposito. "Buona comunicazione" non è una lezione; "lo standup di 5 minuti ha evitato l'accumulo di feedback" sì.
2. **Cosa non ha funzionato — senza colpe.** Fattuale. Dove spunta un nome, traducilo nel sistema che l'ha permesso: "il montaggio è rimasto fermo tre giorni", non "Marco era lento".
3. **Cause radice — un livello più giù.** Chiedi "perché" una o due volte finché arrivi a qualcosa che puoi cambiare. Fermati alla prima causa che hai il potere di risolvere.
4. **Tre cambiamenti — concreti, pronti per il prossimo progetto.** Esattamente tre, adottabili. Dove possibile legali a una skill esistente (es. "usa `project-brief` al kickoff così il KPI è bloccato").
5. **Aggiungi a LESSONS.md.** Controlla se esiste. Se sì, appendi sotto l'ultima voce. Se no, crealo con l'intestazione `# Lessons Learned`. Mai sovrascrivere.

### Template di output

```
POST-MORTEM — [Progetto]
Esito: [tempi? budget? cliente contento?]

COSA HA FUNZIONATO (continuare)
• ...

COSA NON HA FUNZIONATO (smettere o correggere)
• ...

CAUSE RADICE
• [Problema] → [perché] → [causa radice risolvibile]

TRE CAMBIAMENTI PER LA PROSSIMA VOLTA
1. ...
2. ...
3. ...
```

Formato voce LESSONS.md (appesa):

```
## [Data] — [Progetto]
**Esito:** [sintesi]
**Funzionato:** [una riga]
**Non funzionato:** [una riga]
**Causa radice:** [una riga]
**Cambiamenti adottati:**
- [cambiamento 1]
- [cambiamento 2]
- [cambiamento 3]
```

### Casi limite

- **Progetto andato bene:** falla comunque — anche il successo ha cause ripetibili da nominare.
- **Una sola persona disponibile:** falla da solo ma segnala che una prospettiva sola è parziale.
- **Cliente ricorrente:** scorri le voci precedenti in `LESSONS.md` e segnala se una lezione si ripete — è un cambiamento mai adottato davvero.
- **Colpa nell'input:** riconosci la frustrazione, poi converti ogni critica personale in un fix di processo.
