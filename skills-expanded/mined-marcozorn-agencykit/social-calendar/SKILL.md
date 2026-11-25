---
name: social-calendar
version: 1.0.0
description: Build a 4-week social content calendar with channels, formats, hooks and posting times, plus fully written week-one captions and a format breakdown per week.
author: MarcoZorn
license: MIT
tags: [agency, workflow, operations, social, content]
compatible: claude-code, codex-cli, cursor, gemini-cli, openclaw
---

# Social Calendar

## When to use this skill

**English:** "content calendar", "social plan", "posting schedule", "editorial plan", "plan the month's content".

**Italiano:** "piano editoriale", "calendario social", "piano contenuti", "scheduling", "programmazione".

## What this skill does

Builds a month of social content that a team can actually produce and post. Four weeks in a table — date, channel, format, topic/angle, the first line of the hook, and the posting time — plus week one written out in full captions so production can start today. It ends the blank-calendar paralysis and the "what do we post tomorrow" scramble.

## Inputs required

1. **Client / brand** and what they do.
2. **Channels** — Instagram, TikTok, LinkedIn, YouTube Shorts, Facebook, and which are primary.
3. **Goal for the month** — awareness, engagement, leads, launch, sales.
4. **Content pillars** — 3–5 recurring themes the brand posts about. If none exist, propose them from the brand.
5. **Any fixed events** — launches, promos, holidays, shooting dates that must anchor the calendar.
6. **Cadence** — how many posts per week per channel, and the brand's voice.

## Output format

1. **4-WEEK CALENDAR** — one table: date / channel / format / topic-angle / hook first line / posting time.
2. **WEEK 1 CAPTIONS** — every week-one post written in full, ready to schedule.
3. **FORMAT BREAKDOWN** — Reel / Carousel / Static / Story counts per week.
4. **POSTING TIMES** — recommended slots per channel with a one-line rationale.

---

## Brand voice

If a `BRAND.md` file exists in this skill's folder (`.claude/skills/social-calendar/BRAND.md`) or in `.claude/brand/BRAND.md` (global fallback), read it before generating output and apply its tone, terminology, and examples to all text you produce. A skill-local `BRAND.md` overrides the global one; if neither exists, use a clean, professional default voice.

## Instructions

### 1. Anchor the calendar

Place the fixed events first — launches, promos, shooting outputs, relevant holidays. Build the rest of the month around them so the calendar serves the goal instead of just filling slots. Distribute the content pillars so no single theme dominates a week and no week is monotone in format.

### 2. Build the calendar table

One row per post. Columns: Date, Channel, Format, Topic/Angle, Hook (first line), Time. The **hook first line** matters most — it is what stops the scroll, so write it as the actual opening line, not a topic label. "3 things I'd never do as a florist" beats "florist tips". Vary formats across the week; do not schedule five carousels in a row.

### 3. Write week one in full

Every week-one post gets a complete, ready-to-schedule caption in the brand's voice: hook line, body, and a clear CTA. Match caption length to the channel (punchy for TikTok, room to breathe for LinkedIn). Include hashtag guidance where the channel rewards it, but do not stuff. Weeks 2–4 stay as calendar rows — enough to approve the plan, not so much you waste writing on posts that may shift.

### 4. Format breakdown

A small table: for each week, how many Reels, Carousels, Statics and Stories. This is the production planning view — it tells the team what to shoot and design. Keep the mix realistic for the crew size; a calendar of 20 Reels a team of two cannot make is a fantasy, not a plan.

### 5. Posting times

Recommend a slot per channel with a one-line reason (audience active window, platform behaviour). Keep them consistent so the audience learns the rhythm. Note that these are starting points to refine against the brand's own analytics, not laws.

### Output template

```
SOCIAL CALENDAR — [Brand] · [Month] · Goal: [goal]

WEEK 1  ([dates])
| Date | Channel | Format | Topic / Angle | Hook (first line) | Time |
|------|---------|--------|---------------|-------------------|------|
| ...  | ...     | ...    | ...           | "..."             | ...  |

WEEK 2 / 3 / 4  — same table structure

WEEK 1 CAPTIONS
— [Date] · [Channel] · [Format]
[Hook line]
[Body]
[CTA]
[#hashtags if relevant]

(repeat for each week-1 post)

FORMAT BREAKDOWN
| Week | Reel | Carousel | Static | Story |
|------|------|----------|--------|-------|
| 1    | ...  | ...      | ...    | ...   |

POSTING TIMES
Instagram: [slot] — [why]
TikTok:    [slot] — [why]
LinkedIn:  [slot] — [why]
```

### Edge cases

- **Single-channel brand:** drop the other channels entirely rather than padding the table; depth on one channel beats a thin spread.
- **Launch month:** build a pre-launch → launch → post-launch arc across the four weeks instead of even distribution.
- **Low production capacity:** bias toward formats the team can make repeatably (statics, carousels, talking-head Reels) and flag the ambitious ones as stretch.
- **B2B / LinkedIn-led:** fewer, denser posts; lead with point of view, not product.

---

## 🇮🇹 Versione italiana

### Quando usare questa skill

Per pianificare un mese di contenuti: "piano editoriale", "calendario social", "piano contenuti", "scheduling". Costruisce un mese di contenuti che il team può davvero produrre e postare.

### Cosa fa

Quattro settimane in tabella — data, canale, formato, tema/angolo, prima riga dell'hook, orario — più la settimana 1 scritta per intero, pronta da schedulare. Chiude la paralisi del calendario vuoto e la corsa dell'ultimo minuto.

### Cosa ti serve

1. **Cliente / brand** e cosa fa.
2. **Canali** — Instagram, TikTok, LinkedIn, YouTube Shorts, Facebook, e quali sono primari.
3. **Obiettivo del mese** — awareness, engagement, lead, lancio, vendite.
4. **Pilastri di contenuto** — 3–5 temi ricorrenti. Se non ci sono, proponili dal brand.
5. **Eventi fissi** — lanci, promo, festività, date shooting che ancorano il calendario.
6. **Cadenza** — quanti post a settimana per canale, e la voce del brand.

### Voce del brand

Se esiste un file `BRAND.md` nella cartella di questa skill (`.claude/skills/social-calendar/BRAND.md`) o in `.claude/brand/BRAND.md` (fallback globale), leggilo prima di generare l'output e applica tono, terminologia ed esempi a tutto il testo che produci. Il `BRAND.md` locale ha la precedenza su quello globale.

### Istruzioni

1. **Ancora il calendario.** Metti prima gli eventi fissi, poi costruisci il mese attorno. Distribuisci i pilastri così nessun tema domina una settimana e nessuna settimana è monotona nei formati.
2. **Costruisci la tabella.** Una riga per post: Data, Canale, Formato, Tema/Angolo, Hook (prima riga), Orario. La **prima riga dell'hook** conta di più: scrivila come frase d'apertura reale, non come etichetta. Varia i formati.
3. **Scrivi la settimana 1 per intero.** Ogni post con caption completa nella voce del brand: hook, corpo, CTA chiara. Lunghezza adatta al canale. Settimane 2–4 restano righe di calendario.
4. **Format breakdown.** Per ogni settimana quanti Reel, Caroselli, Statici, Storie. È la vista di produzione. Mix realistico per la crew.
5. **Orari.** Uno slot per canale con motivo in una riga. Coerenti, come punti di partenza da rifinire con gli analytics del brand.

### Template di output

```
CALENDARIO SOCIAL — [Brand] · [Mese] · Obiettivo: [obiettivo]

SETTIMANA 1  ([date])
| Data | Canale | Formato | Tema / Angolo | Hook (prima riga) | Ora |
|------|--------|---------|---------------|-------------------|-----|

SETTIMANA 2 / 3 / 4 — stessa struttura

CAPTION SETTIMANA 1
— [Data] · [Canale] · [Formato]
[Hook]
[Corpo]
[CTA]
[#hashtag se rilevanti]

FORMAT BREAKDOWN
| Settimana | Reel | Carosello | Statico | Storia |
|-----------|------|-----------|---------|--------|

ORARI DI PUBBLICAZIONE
Instagram: [slot] — [perché]
TikTok:    [slot] — [perché]
LinkedIn:  [slot] — [perché]
```

### Casi limite

- **Brand mono-canale:** togli gli altri canali invece di riempire la tabella.
- **Mese di lancio:** costruisci un arco pre-lancio → lancio → post-lancio invece di distribuzione uniforme.
- **Bassa capacità produttiva:** favorisci formati ripetibili e segnala gli ambiziosi come stretch.
- **B2B / LinkedIn:** meno post ma più densi, apri con il punto di vista, non col prodotto.
