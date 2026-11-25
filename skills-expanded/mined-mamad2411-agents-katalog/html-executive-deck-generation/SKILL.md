---
name: html-executive-deck-generation
description: >-
  Guided 6-step executive presentation deck pipeline from CSV/XLSX or free-text
  input to HTML slides plus copy-paste prompts for Gamma and Kimi AI. Default
  visual system is the bundled DAYMARK mood board (navy / teal / gold / bone).
  Step 5 optionally accepts a PDF/PPTX/HTML layout reference for 排版 and
  exhibit structure only — never replacing DAYMARK color, type, or logo. Use
  when building executive decks, year-end performance presentations, pulse
  survey slides, or any slide deck where the user provides data as a file or
  text and wants HTML + Gamma + Kimi outputs.
user-invocable: true
---

# Executive Presentation Deck Pipeline (6 Steps)

Guide the user from **raw input** (file or text) to three deliverables:

1. **HTML slide deck** (stable 1280×720 when template is HTML-based)
2. **Gamma prompt** (copy-paste into [Gamma](https://gamma.app))
3. **Kimi AI prompt** (copy-paste into Kimi slide generation)

Pause after each step unless user says **run all** / **auto**.

Arguments passed: `$ARGUMENTS`

---

## Input types (Step 0 ? detect before Step 1)

| Type | Examples | Agent behavior |
|------|----------|----------------|
| **Structured file** | CSV, XLSX | Run **Python** first ([python-metrics.md](references/python-metrics.md)); cite only `metrics.json` |
| **Free text** | Pasted brief, bullet notes, year-end narrative, email draft | Extract facts, metrics, themes; **never invent numbers** — mark missing data as `[TBD]` or ask user |
| **Mixed** | Text + partial table | Python on the file for numbers; text for context |

### Session opener

```text
I'll build your presentation in 6 steps:
0 Python metrics (CSV/XLSX only) → 1 Insights → 2 Charts → 3 Storyline → 4 DAYMARK mood board → 5 Layout reference (optional PDF/PPTX) → 6 Outputs (HTML + Gamma + Kimi)

Visual system: DAYMARK (locked). At Step 5 you may attach a deck as 排版 reference only — colors and logo stay DAYMARK.

Provide your content as a CSV/XLSX file OR paste/write your text.
I'll pause after each step unless you say "run all".
```

### Deck context to confirm early

- Topic (e.g. "HR Year-End Performance Review 2025")
- Audience (default: leadership / CHRO)
- Period and language
- Output folder or save location

---

## Mood board (Step 4) vs layout reference (Step 5)

**Step 4 — DAYMARK locked.** Read [daymark-visual-guide.md](references/daymark-visual-guide.md). Color, type, logo, gold-once. Do not replace these because a layout PDF arrived.

**Step 5 — optional 排版 reference.** User may attach PPTX / PDF / HTML / screenshots. Analyze layout, elements, 排版, dataviz *methods*. Apply structure only. See [step5-layout-reference.md](references/step5-layout-reference.md).

Brand override only if the user explicitly says **replace DAYMARK** or **use HR fallback** (`HRBP/pulse_survey_eng/engagement_survey_executive_deck.html`).

---

## Pipeline

| Step | Name | Output | Reference |
|------|------|--------|-----------|
| 0 | Python metrics (CSV/XLSX) | `metrics.json` + chart PNGs | [python-metrics.md](references/python-metrics.md) · sibling `pulse-survey-analysis` |
| 1 | Insight analysis | Insight Brief | [step1-insight-analysis.md](references/step1-insight-analysis.md) |
| 2 | Chart plan | Chart Plan + data JSON | [step2-chart-plan.md](references/step2-chart-plan.md) |
| 3 | Storyline | Storyline Plan (SCQA) | [step3-storyline.md](references/step3-storyline.md) |
| 4 | DAYMARK mood board | Template Profile (tokens + logos) | [step4-layout.md](references/step4-layout.md) · [daymark-visual-guide.md](references/daymark-visual-guide.md) |
| 5 | Layout reference (排版) | Adaptation + interactions + Deck Build Brief | [step5-layout-reference.md](references/step5-layout-reference.md) |
| 6 | Generate outputs | HTML + Gamma prompt + Kimi prompt | [step6-generate-outputs.md](references/step6-generate-outputs.md) |

After Step 6 HTML: run [verification-checklist.md](references/verification-checklist.md).

---

## Step 6 deliverables

Write three files beside input (or user-specified folder):

| File | Purpose |
|------|---------|
| `{topic}_deck.html` | Interactive HTML slides |
| `{topic}_gamma_prompt.md` | Gamma paste prompt ? see [gamma-prompt-template.md](references/gamma-prompt-template.md) |
| `{topic}_kimi_prompt.md` | Kimi paste prompt ? see [kimi-prompt-template.md](references/kimi-prompt-template.md) |

---

## HTML build rules (Step 6A)

- **Paint:** always [daymark-visual-guide.md](references/daymark-visual-guide.md) unless user said replace DAYMARK. Copy logos from `assets/daymark-visual-guide/`.
- **排版:** Step 5 Part B if a layout reference was analyzed; otherwise Step 4 Part B.
- Engine: [layout-contract.md](references/layout-contract.md) (viewport, nav, print). Do not clone the reference deck’s CSS colors.
- Legacy HR clone only when user confirmed: `HRBP/pulse_survey_eng/engagement_survey_executive_deck.html`

Hard constraints: 1280×720, no emoji (SVG only), UTF-8, print-safe KPIs.

---

## Orchestration rules

1. Extract insights from **file or text** — do not fabricate metrics.
2. For every CSV/XLSX: run Python (pulse runner or `compute_deck_metrics.py`) **before** Step 1. Never average, rank, or % change a file in the LLM.
3. One step at a time; 3-line summary + "Proceed to Step N?" between steps.
4. Carry Python `metrics.json` + all artifacts forward into Deck Build Brief (Step 5).
5. No HTML / Gamma / Kimi output before Step 6.
6. Gamma and Kimi prompts use **same storyline and numbers** as HTML (copied from Python JSON), DAYMARK paint, and Step 5 排版.

---

## Use-case examples

| User request | Input | Template |
|--------------|-------|----------|
| Pulse survey deck | CSV | Python via `pulse-survey-analysis`; DAYMARK paint; optional layout PDF at Step 5 |
| Year-end performance | Pasted narrative | DAYMARK paint; optional company PPTX at Step 5 for 排版 |
| Board briefing | XLSX + bullets | Python via `compute_deck_metrics.py`; DAYMARK paint; optional brand PDF at Step 5 |

---

## Quick paths

| User says | Action |
|-----------|--------|
| CSV or text only | CSV/XLSX: Python Step 0 then Step 1. Text-only: Step 1 extract. DAYMARK at Step 4; at Step 5 ask for optional layout PDF |
| "Run all" | Steps 1–5 inline; skip layout reference if none attached; do not block |
| "HTML only" | Still produce Gamma/Kimi prompts unless user explicitly opts out |
| "Skip to slides" | Refuse without Steps 1?5 artifacts |
| "Fix broken HTML" | Diagnose vs layout contract; patch; re-verify |

---

## Related skills

- `pulse-survey-analysis` — **required** Python math + PNG/PDF for pulse/engagement CSVs (`EmpID`, `Manager`, Q1–Q20). Bundled in this repo.
- `lecture-course-design-guideline` — JSON brand spec only if user rejects DAYMARK and has no other template
