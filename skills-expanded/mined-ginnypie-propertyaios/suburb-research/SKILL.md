---
name: suburb-research
description: "Use when you want to assess a suburb or area before researching specific listings."
---

# Skill — Suburb Research

**Stage:** 1 — Analyse
**Hook:** Run a structured suburb risk scan before you inspect.
**Use when:** You want to assess a suburb or area before researching specific listings.

---

## Purpose

This skill produces a structured suburb analysis covering employment base, infrastructure, supply and demand signals, lender appetite flags, and known risk overlays. It is preparation for property research — not a recommendation.

---

## Reads from

- Property File: INVESTOR PROFILE section (optional)

## Writes to

- Property File: SUBURB & DEMAND section

---

> **Running this standalone:** This skill is self-contained. If you don't have a "Property File" or the paired skills listed below, just fill in the Inputs block — that's all this skill needs. The "Reads from" and "Pairs with" references are optional extras, not requirements.

---

## Inputs required

```
SUBURB: [suburb name, state, postcode]
PROPERTY TYPE I AM RESEARCHING: [house / townhouse / apartment / unit / acreage]
MY PURPOSE: [investor / owner-occupier / first home buyer / downsizer]
BUDGET RANGE: $[min] to $[max]
```

---

## Data sources — how to populate this

Without live data, this skill produces a **"verify these" scaffold**, not findings. Where you can pull data, name the source and freshness against every figure (e.g. `median $720k — Domain, Jun 2026`). Suggested lookups:

- **Medians, days-on-market, price/rent trends:** CoreLogic, Domain, PropTrack, REA (realestate.com.au)
- **Vacancy rate:** SQM Research
- **Population and demographics:** ABS QuickStats
- **Flood, bushfire, contaminated land, planning overlays:** the relevant state planning portal + the local council's planning/hazard maps

If a figure has no source, label it **Assumption — verify** and do not present it as fact.

---

## Output contract

Return exactly these 8 sections:

### 1. SUBURB SNAPSHOT
- State, LGA, postcode
- Dominant property types and land sizes
- Distance from CBD or major employment centre
- Population and demographic signals

### 2. EMPLOYMENT AND ECONOMIC BASE
- Major employers and industries
- Single-employer dependency risk
- Economic diversity signal (low/medium/high)

### 3. INFRASTRUCTURE AND LIVEABILITY
- Transport: proximity to train/bus/freeway
- Schools, hospitals, retail, parks
- Planned infrastructure (confirm with council)
- Flight path, industrial, or hazard proximity (flag to verify)

### 4. SUPPLY AND DEMAND SIGNALS
- Development pipeline: new apartments, estates, townhouse projects
- Historical median price and rent trends (label as historical, not predictive)
- Days on market signal (higher = softer demand)
- Vacancy rate signal for investors

### 5. LENDER APPETITE FLAGS
Flag any of the following if applicable:
- High-density postcode (many lenders cap LVR at 70-80%)
- Regional or rural location (some lenders restrict)
- Mining, tourism, or resort-dependent economy
- Known postcode restrictions (verify with a mortgage broker)

### 6. RISK OVERLAYS TO VERIFY
- Flood zone: check council flood map and state hazard portals
- Bushfire: check state's BAL (Bushfire Attack Level) map
- Contaminated land: check council and EPA registers
- Coastal erosion, subsidence, or heritage overlays
- (These require confirmation from council and licensed professionals)

### 7. SUBURB SCORE SUMMARY
A simple summary table:

| Factor | Signal | Confidence |
|---|---|---|
| Employment diversity | [low/medium/high] | [High/Medium/Low — based on: ...] |
| Infrastructure | [weak/moderate/strong] | [High/Medium/Low — based on: ...] |
| Supply pressure | [low/medium/high] | [High/Medium/Low — based on: ...] |
| Lender appetite | [unrestricted/flagged/restricted] | [Low — verify with broker] |
| Risk overlays | [none identified/verify X] | [High/Medium/Low — based on: ...] |

**Confidence rubric (how to rate each signal):**
- **High** — backed by a named, current source (dated within ~12 months) from the Data sources list above.
- **Medium** — inferred from an older or indirect source, or one dataset only; directionally useful but re-check before acting.
- **Low** — assumption, anecdote, or a domain that needs a licensed professional (e.g. lender appetite, hazard overlays). Treat as a question to answer, not a finding.

### 8. BEAR CASE — WHAT WOULD MAKE THIS SUBURB A POOR FIT
Required, not optional. State the strongest reasons an investor should walk away or wait — e.g. single-employer dependency, a heavy development pipeline diluting supply, a lender-restricted postcode, a hazard overlay, or thin/soft demand signals. If the data is too thin to judge, say so explicitly rather than skipping this section.

---

## Safety boundaries

- Never recommend a suburb as "the right choice" or "best for investment"
- Never present price growth or rental growth as predictable
- Always flag when data is thin or assumed
- Always direct lender appetite questions to a mortgage broker

---

## Professional review prompts

- "Ask your mortgage broker: Are there any lender restrictions on this postcode for my property type and LVR?"
- "Check with council: Is this area in a flood or bushfire overlay?"
- "Ask a local property manager: What is the current vacancy rate and rental demand for [property type] in this suburb?"

---

## Pairs with

- → [Due Diligence Risk Scan](due-diligence-risk-scan.md) — deepen the hazard and disclosure checks for a specific property in this suburb
- → [Property Cash Flow](property-cash-flow.md) — stress-test the numbers once you have a target property here

---

## Disclaimer

> This output is general information and educational preparation only. It is not financial advice, credit advice, tax advice, legal advice, or a property recommendation. All figures and signals are starting points requiring verification. See [disclaimers/general-information.md](../disclaimers/general-information.md) and [disclaimers/professional-review-required.md](../disclaimers/professional-review-required.md).
