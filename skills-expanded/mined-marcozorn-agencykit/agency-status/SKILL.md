---
name: agency-status
version: 1.0.0
description: Produce a weekly agency status — traffic-light health per project, the week's top three priorities, blocked items with owners, and a Slack/WhatsApp-ready morning briefing.
author: MarcoZorn
license: MIT
tags: [agency, workflow, operations, management]
compatible: claude-code, codex-cli, cursor, gemini-cli, openclaw
---

# Agency Status

## When to use this skill

**English:** "status update", "team briefing", "weekly update", "what's happening", "Monday briefing", "agency status".

**Italiano:** "stato agenzia", "briefing team", "aggiornamento settimanale", "riunione lunedì", "come stiamo".

## What this skill does

Gives an agency owner or PM a single, honest read of the whole studio in thirty seconds: every active project on a traffic light, the three things that actually matter this week, what is blocked and who unblocks it, and a briefing message ready to drop in Slack or WhatsApp on Monday morning. It replaces the vague "how's everything going" with a picture you can act on.

## Inputs required

1. **The active projects** — names and, for each, a line on where it stands.
2. **Deadlines** coming up this week or next.
3. **Anything stuck** — waiting on a client, a person, an asset, a payment.
4. **The team** — who owns what, so blockers get a name attached.

If the user dumps everything unstructured, sort it yourself. If a project has no clear owner or next step, that absence is itself a finding — surface it.

## Output format

1. **PROJECT STATUS** — traffic-light per project with a one-line reason.
2. **TOP 3 PRIORITIES** — what the week turns on.
3. **BLOCKED** — each blocker with owner and the single next action.
4. **MORNING BRIEFING** — Slack/WhatsApp-ready message, copy-paste as-is.

---

## Brand voice

If a `BRAND.md` file exists in this skill's folder (`.claude/skills/agency-status/BRAND.md`) or in `.claude/brand/BRAND.md` (global fallback), read it before generating output and apply its tone, terminology, and examples to all text you produce. A skill-local `BRAND.md` overrides the global one; if neither exists, use a clean, professional default voice.

## Instructions

### 1. Traffic-light every project

Assign each project a status and one line explaining it:

- **🟢 On track** — moving, no help needed, deadline safe.
- **🟡 At risk** — a deadline is tight, feedback is slow, or a dependency is wobbling. Not on fire yet, but watch it.
- **🔴 Blocked** — cannot progress without a specific unblock.

Be honest. A status report that is all green is a status report nobody trusts. If everything really is green, say why in a sentence so it reads as earned, not lazy.

### 2. Top 3 priorities for the week

The three things that, if they happen, make the week a win — usually the intersection of nearest deadline, biggest client, and thinnest slack. Not a task list. Three. Each phrased as an outcome with an owner.

### 3. Blocked items — owner and next action

For every 🟡 and 🔴, name the single next action and who does it. A blocker without a named owner and a concrete next step is not tracked, it is just worrying. "Waiting on client" is not an action; "Sara calls the client today to get the logo files" is.

### 4. Morning briefing

A short, energising, copy-paste block for the team channel. Lead with the one thing that matters most this week, list the traffic lights compactly, call out the blockers with their owners, and close with a single clear focus. Warm and direct, not corporate. This is the message the team actually reads.

### Output template

```
AGENCY STATUS — week of [date]

PROJECT STATUS
🟢 [Project] — [one line: why it's on track]
🟡 [Project] — [one line: what to watch]
🔴 [Project] — [one line: what's blocking it]

TOP 3 PRIORITIES THIS WEEK
1. [Outcome] — [owner]
2. [Outcome] — [owner]
3. [Outcome] — [owner]

BLOCKED
• [Project] — blocked on [X]. Next: [action] — [owner], by [when].

MORNING BRIEFING (Slack / WhatsApp)
☀️ Morning team — week of [date]

Big one this week: [the single most important thing].

Status:
🟢 [Project]  🟢 [Project]  🟡 [Project]  🔴 [Project]

Blocked:
• [Project]: [owner] → [next action] today.

Focus: [one clear line]. Let's go.
```

### Edge cases

- **One project is on fire:** lead the briefing with it and let it dominate; do not bury a 🔴 under routine greens.
- **Very small team:** collapse owners into "we" but still name the next action — the action matters more than the name here.
- **Nothing blocked:** keep the section with "Nothing blocked — clear runway" rather than deleting it, so the team knows it was checked, not skipped.
- **Too many projects to fit:** group the healthy greens into one line and spend the detail on the yellows and reds, where attention is actually needed.

---

## 🇮🇹 Versione italiana

### Quando usare questa skill

Per una lettura settimanale dell'agenzia: "stato agenzia", "briefing team", "aggiornamento settimanale", "come stiamo". Da a un titolare o PM una lettura onesta di tutto lo studio in trenta secondi.

### Cosa fa

Ogni progetto attivo su un semaforo, le tre cose che contano davvero questa settimana, cosa è bloccato e chi lo sblocca, e un messaggio di briefing pronto da incollare in Slack o WhatsApp lunedì mattina. Sostituisce il vago "come va tutto" con un quadro su cui agire.

### Cosa ti serve

1. **I progetti attivi** — nomi e, per ciascuno, una riga su dove sta.
2. **Le scadenze** di questa settimana o della prossima.
3. **Cosa è fermo** — in attesa di cliente, persona, asset, pagamento.
4. **Il team** — chi possiede cosa, così i blocchi hanno un nome.

Se l'utente butta tutto disordinato, ordinalo tu. Se un progetto non ha owner o next step chiaro, quell'assenza è già un risultato: segnalala.

### Voce del brand

Se esiste un file `BRAND.md` nella cartella di questa skill (`.claude/skills/agency-status/BRAND.md`) o in `.claude/brand/BRAND.md` (fallback globale), leggilo prima di generare l'output e applica tono, terminologia ed esempi a tutto il testo che produci. Il `BRAND.md` locale ha la precedenza su quello globale.

### Istruzioni

1. **Semaforo per ogni progetto.**
   - **🟢 On track** — si muove, nessun aiuto serve, scadenza al sicuro.
   - **🟡 A rischio** — scadenza stretta, feedback lento, dipendenza traballante.
   - **🔴 Bloccato** — non avanza senza uno sblocco specifico.
   Sii onesto. Un report tutto verde è un report di cui nessuno si fida.
2. **Top 3 priorità della settimana.** Le tre cose che, se accadono, rendono la settimana vinta. Non una to-do list. Tre, come risultato con owner.
3. **Bloccati — owner e prossima azione.** Per ogni 🟡 e 🔴, la singola prossima azione e chi la fa. "In attesa del cliente" non è un'azione; "Sara chiama il cliente oggi per i file del logo" sì.
4. **Briefing del mattino.** Blocco corto ed energico da incollare nel canale del team. Apri con la cosa più importante, semafori compatti, blocchi con owner, chiudi con un focus. Caldo e diretto, non corporate.

### Template di output

```
STATO AGENZIA — settimana del [data]

STATO PROGETTI
🟢 [Progetto] — [una riga: perché è on track]
🟡 [Progetto] — [una riga: cosa tenere d'occhio]
🔴 [Progetto] — [una riga: cosa lo blocca]

TOP 3 PRIORITÀ DELLA SETTIMANA
1. [Risultato] — [owner]
2. [Risultato] — [owner]
3. [Risultato] — [owner]

BLOCCATI
• [Progetto] — bloccato su [X]. Prossima: [azione] — [owner], entro [quando].

BRIEFING DEL MATTINO (Slack / WhatsApp)
☀️ Buongiorno team — settimana del [data]

La grande di questa settimana: [la cosa più importante].

Stato:
🟢 [Progetto]  🟢 [Progetto]  🟡 [Progetto]  🔴 [Progetto]

Bloccati:
• [Progetto]: [owner] → [prossima azione] oggi.

Focus: [una riga chiara]. Andiamo.
```

### Casi limite

- **Un progetto in fiamme:** aprilo per primo e lascialo dominare; non seppellire un 🔴 sotto i verdi.
- **Team piccolissimo:** collassa gli owner in "noi" ma nomina comunque la prossima azione.
- **Niente bloccato:** tieni la sezione con "Nessun blocco — pista libera" invece di cancellarla.
- **Troppi progetti:** raggruppa i verdi sani in una riga e dedica il dettaglio a gialli e rossi.
