---
name: client-report
version: 1.0.0
description: Turn a month of campaign data into a confident client report — executive summary, what worked, what didn't, next month's plan and a clean channel/KPI table with deltas.
author: MarcoZorn
license: MIT
tags: [agency, workflow, operations, reporting]
compatible: claude-code, codex-cli, cursor, gemini-cli, openclaw
---

# Client Report

## When to use this skill

**English:** "monthly report", "performance report", "send report to client", "campaign results", "wrap up the month".

**Italiano:** "report mensile", "resoconto", "risultati campagna", "report cliente", "chiudi il mese".

## What this skill does

Turns a pile of numbers into a report a client actually reads and trusts. It leads with a plain-language summary, names the three things that worked with real figures, is honest about what did not and what you are doing about it, sets three priorities for next month, and backs it all with one clean data table showing month-over-month deltas. The tone is confident and clear — not defensive, not a data dump.

## Inputs required

1. **Client name** and the **reporting period** (e.g. March 2026).
2. **The channels** in scope (Instagram, TikTok, Meta Ads, email, Google Ads, web).
3. **This period's numbers** and **last period's numbers** for each KPI. If last period is missing, mark deltas `n/a — first report`.
4. **The goal** the client cares about (the KPI from the brief).
5. **Anything notable** — a launch, a budget change, an outage, a viral post. Context that explains the numbers.

If numbers are missing, ask for them. Do not fabricate metrics — a made-up figure in a client report is the fastest way to lose the account.

## Output format

1. **EXECUTIVE SUMMARY** — three sentences, no jargon.
2. **WHAT WORKED** — top 3 results, each with a number.
3. **WHAT DIDN'T** — honest, solution-focused, never defensive.
4. **NEXT MONTH** — three priorities.
5. **THE NUMBERS** — a table: channel / KPI / this period / last period / delta.
6. **CLOSING LINE** — one branded, forward-looking sentence.

---

## Brand voice

If a `BRAND.md` file exists in this skill's folder (`.claude/skills/client-report/BRAND.md`) or in `.claude/brand/BRAND.md` (global fallback), read it before generating output and apply its tone, terminology, and examples to all text you produce. A skill-local `BRAND.md` overrides the global one; if neither exists, use a clean, professional default voice.

## Instructions

### 1. Write the executive summary last, place it first

Three sentences a busy founder can read in ten seconds: where we landed against the goal, the single biggest win, and the direction of travel. No percentages stacked on percentages. If the month was down, say so in sentence one and pivot to the plan — do not bury it.

### 2. What worked — three, with numbers

Pick the three results that matter most to the client's goal, not the three that are easiest to brag about. Each gets a concrete number and, where useful, the delta. "Reels drove reach up 62% (412k vs 254k), and the three top performers all used the founder's voice-over — a format we'll lean into."

### 3. What didn't — honest and solved

Name one or two things that underperformed. State it plainly, give the likely cause in a phrase, and immediately attach what you are changing. Honesty here is what makes the "what worked" section believable. Never blame the client, the algorithm, or the weather without also owning a lever you control.

### 4. Next month — three priorities

Three, not ten. Each is an action with an intended outcome. Tie at least one directly to the goal KPI. These should read like decisions, not a wish list.

### 5. The numbers table

One table. Columns: Channel, KPI, This period, Last period, Δ. Compute the delta as both absolute and percentage where it helps. Round sensibly — nobody needs four decimal places. Flag standout rows but let the table stay clean.

### 6. Closing line

One sentence, forward-looking, in the agency's voice. Not "let me know if you have questions" — something that signals momentum and partnership.

### Output template

```
[CLIENT] — Performance Report · [Period]

EXECUTIVE SUMMARY
[Three sentences: result vs goal, biggest win, direction.]

WHAT WORKED
1. [Result with number]
2. [Result with number]
3. [Result with number]

WHAT DIDN'T
• [Honest point] — [cause in a phrase]. Fix: [what changes].

NEXT MONTH
1. [Priority → intended outcome]
2. [Priority → intended outcome]
3. [Priority → intended outcome]

THE NUMBERS
| Channel | KPI | This period | Last period | Δ |
|---------|-----|-------------|-------------|---|
| ...     | ... | ...         | ...         | ... |

[Branded closing line.]
```

### Tone rules

- Confident, not boastful. Clear, not clever.
- Lead with the client's goal, not your activity. Clients pay for outcomes, not busywork.
- Every negative gets a next step in the same breath.
- No jargon a non-marketer would need to Google. "Engagement rate" is fine; "ROAS blended across MOF touchpoints" is not, unless the client speaks it.

### Edge cases

- **A down month:** own it in the summary, be specific about the cause, and spend proportionally more words on the plan. A well-handled bad month builds more trust than a vague good one.
- **First report, no comparison data:** mark deltas `n/a — baseline`, and frame the numbers as the baseline you will beat.
- **A viral outlier:** report the real number but note it as an outlier so next month's dip is not read as failure.
- **Client only cares about one number:** lead with it every time and relegate the rest to the table.

---

## 🇮🇹 Versione italiana

### Quando usare questa skill

A fine mese o fine campagna: "report mensile", "resoconto", "risultati campagna", "report cliente". Trasforma i numeri in un report che il cliente legge e di cui si fida.

### Cosa fa

Trasforma un mucchio di numeri in un report leggibile: sintesi in linguaggio semplice, le tre cose che hanno funzionato con dati reali, cosa non ha funzionato e come lo stai risolvendo, tre priorità per il mese dopo, e una tabella pulita con i delta mese-su-mese. Tono sicuro e chiaro, mai difensivo, mai un data dump.

### Cosa ti serve

1. **Nome cliente** e **periodo** (es. Marzo 2026).
2. **I canali** (Instagram, TikTok, Meta Ads, email, Google Ads, sito).
3. **Numeri del periodo** e **del periodo precedente** per ogni KPI. Se manca il precedente, delta `n/d — primo report`.
4. **L'obiettivo** che interessa al cliente (il KPI del brief).
5. **Fatti rilevanti** — un lancio, un cambio budget, un blocco, un post virale.

Se mancano numeri, chiedili. Non inventare metriche: un numero falso in un report cliente è il modo più veloce di perdere l'account.

### Voce del brand

Se esiste un file `BRAND.md` nella cartella di questa skill (`.claude/skills/client-report/BRAND.md`) o in `.claude/brand/BRAND.md` (fallback globale), leggilo prima di generare l'output e applica tono, terminologia ed esempi a tutto il testo che produci. Il `BRAND.md` locale ha la precedenza su quello globale.

### Istruzioni

1. **Scrivi la sintesi per ultima, mettila per prima.** Tre frasi leggibili in dieci secondi: dove siamo arrivati rispetto all'obiettivo, la vittoria principale, la direzione. Se il mese è andato giù, dillo nella prima frase e passa al piano.
2. **Cosa ha funzionato — tre, con numeri.** I tre risultati che contano per l'obiettivo del cliente, ciascuno con un numero concreto.
3. **Cosa non ha funzionato — onesto e risolto.** Uno o due punti sotto le aspettative, causa in una frase, e subito cosa cambi. Mai dare la colpa al cliente o all'algoritmo senza prendere una leva tua.
4. **Mese prossimo — tre priorità.** Tre, non dieci. Ognuna un'azione con un risultato atteso, almeno una legata al KPI obiettivo.
5. **La tabella.** Colonne: Canale, KPI, Questo periodo, Periodo precedente, Δ. Arrotonda con buonsenso.
6. **Frase di chiusura.** Una frase, in avanti, nella voce dell'agenzia. Non "fammi sapere".

### Template di output

```
[CLIENTE] — Report Performance · [Periodo]

SINTESI
[Tre frasi: risultato vs obiettivo, vittoria principale, direzione.]

COSA HA FUNZIONATO
1. [Risultato con numero]
2. [Risultato con numero]
3. [Risultato con numero]

COSA NON HA FUNZIONATO
• [Punto onesto] — [causa in una frase]. Fix: [cosa cambia].

MESE PROSSIMO
1. [Priorità → risultato atteso]
2. [Priorità → risultato atteso]
3. [Priorità → risultato atteso]

I NUMERI
| Canale | KPI | Questo periodo | Periodo prec. | Δ |
|--------|-----|----------------|---------------|---|

[Frase di chiusura.]
```

### Casi limite

- **Mese in calo:** prendine possesso nella sintesi, sii specifico sulla causa, dedica più parole al piano.
- **Primo report, niente confronto:** delta `n/d — baseline`, inquadra i numeri come la base da battere.
- **Picco virale:** riporta il numero reale ma segnalalo come outlier.
- **Cliente interessato a un solo numero:** aprilo sempre con quello, il resto in tabella.
