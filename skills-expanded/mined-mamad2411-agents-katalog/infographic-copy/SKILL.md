---
name: infographic-copy
description: Transforms research and knowledge base material into information-dense infographic copy—clear, scannable, authoritative, and reference-worthy. Use when converting clinical algorithms, decision trees, comparison data (drug vs drug, treatment options), trial results, myth vs truth content, patient preparation guides, checklists, or sequential process workflows into structured copy ready for single-image infographic formats. Supports multiple infographic types including hero stats, dense multi-section layouts, side-by-side comparisons, myth-busters, step-by-step processes, and patient checklists. Outputs structured copy with compressed noun-heavy phrasing, specific numbers, trial citations, and JSON-formatted handoff data for downstream infographic generation.
---

# Infographic Copy Skill

Transform research and knowledge base material into information-dense infographic copy—clear, scannable, authoritative, reference-worthy.

---

## Key Principle

Infographics are saved, screenshotted, and returned to. Write for the second and third viewing.

**Compressed, noun-heavy style:**
```
"SGLT2i: 26% reduction in HF hospitalization. Start if EF ≤40%."
```
**Not:**
```
"SGLT2 inhibitors have been shown to reduce heart failure hospitalization by 26%..."
```

Authority comes from precision: specific numbers, trial names, dosing details—not from "I" statements.

---

## 3-Step Transformation Workflow

### Step 1: Identify the Infographic Type

| Content | Template |
|---------|----------|
| Single striking statistic | `infographic-hero` |
| Multiple related facts/sections | `infographic-dense` |
| Two options to compare | `infographic-comparison` |
| Misconception to correct | `infographic-myth` |
| Sequential steps or algorithm | `infographic-process` |
| Patient prep or to-do list | `infographic-checklist` |

### Step 2: Extract and Compress

For each fact: isolate the core claim (3–5 words), keep only essential context, cut the rest. Place the most important information first.

**Compression examples:**

| Original | Compressed |
|----------|------------|
| "Patients should discontinue aspirin 7 days before the procedure if instructed" | "Stop aspirin 7 days before (if advised)" |
| "BP measured seated after 5 minutes of rest" | "BP: seated, after 5 min rest" |
| "PARADIGM-HF: 20% relative risk reduction in CV mortality" | "CV mortality: ↓20% (PARADIGM-HF)" |

**After compressing:** verify the clinical accuracy of every compressed item against the source. Do not discard dose thresholds, qualifiers (e.g., "if contraindicated"), or population-specific details.

### Step 3: Assemble Copy Using the Template

Use the template format below for the identified type. Before handoff, confirm all required fields are populated and every statistic has a source.

---

## Copy Templates

### HERO
```
STAT:     [Number + unit]            →  "26%"
LABEL:    [Outcome, patient-focused] →  "Mortality Reduction"
CONTEXT:  [HR/NNT/ARR/vs comparator] →  "HR 0.74 (95% CI 0.65–0.85)"
SOURCE:   [Trial/guideline]          →  "PARADIGM-HF Trial"
TAG:      [Category label]           →  "LANDMARK TRIAL"
```

### DENSE
```
TAG:      [Category]
TITLE:    [Main topic]
SUBTITLE: [Scope/audience]

SECTION N:
  TITLE:   [Section name]
  BULLETS: [2–4 items, ≤8 words each, parallel structure, no periods]

CALLOUT:  [Single key takeaway]
```

### COMPARISON
```
TAG:      [Category]
TITLE:    [What's being compared]

LEFT / RIGHT:
  LABEL:      [Option]
  STAT:       [Key number]
  STAT LABEL: [What it measures]
  BULLETS:    [Differentiators—lead with when to choose; same count each side]

SOURCE:   [Evidence base]
```
Keep sides parallel. Lead with differentiators, not similarities. Be clinically fair to both options.

### MYTH
```
TAG:      [e.g., "MYTH BUSTED"]
TITLE:    [The misconception]
MYTH:     [State belief as holders state it—no strawman]
TRUTH:    [Direct correction + key number + action/reassurance]
EVIDENCE: [Supporting data]
SOURCE:   [Citation]
```

### PROCESS
```
TAG:      [Category]
TITLE:    [Process name]
SUBTITLE: [Context]

STEP N:
  TITLE:       [Verb, 2–4 words]
  DESCRIPTION: [Specifics: dose, timing, threshold]

NOTE:     [Critical hold/exception criteria]
```

### CHECKLIST
```
TAG:      [Category]
TITLE:    [What it's for]
SUBTITLE: [Additional context]

CATEGORY N:
  TITLE: [Timeframe or theme]
  ITEMS: [Verb-led, specific, ordered by timeline or priority]

CALLOUT:  [Critical warning with ⚠ icon]
FOOTER:   [Disclaimer if patient-facing]
```

---

## Citation Formats

- Inline after stats: `Mortality: ↓26% (DAPA-HF)`
- Bottom source line: `Source: ACC/AHA Guidelines 2023`
- Abbreviate: `NEJM 2019`, `ACC/AHA 2023`, `n=8,000`

---

## Audience Framing

The same clinical content reframes by audience. Example — Beta-Blocker Initiation in HFrEF:

| Audience | Title | Key Framing |
|----------|-------|-------------|
| **Clinician** | Beta-Blocker Initiation in HFrEF | Confirm euvolemia → start dose (Carvedilol 3.125mg BID or Metoprolol XL 12.5mg) → uptitrate q2wk. Hold if SBP <90 or HR <60. |
| **Patient** | Starting Your Beta-Blocker | Doctor confirms stability → very low starting dose → slow weekly increases. Tell doctor if dizzy or very tired. |
| **Caregiver** | Beta-Blocker Monitoring Checklist | Watch for: dizziness, fatigue, pulse <50. When to call: worsening breathlessness, fainting. |

Apply the same compression principles; adjust terminology and action language for the audience.

---

## End-to-End Example

### Input
```
Angiography preparation:
- NPO after midnight; hold metformin 48h before contrast
- Stop warfarin 5 days before; bridge with heparin if high-risk
- Continue aspirin unless directed otherwise
- Arrive 2h early; bring medication list; arrange transport home
- Tell staff: contrast allergies, kidney problems, recent bleeding
```

### Output: Infographic Copy
```
TAG: PATIENT GUIDE
TITLE: Before Your Angiogram
SUBTITLE: Complete preparation checklist

CATEGORY 1: "48 Hours Before"
  - "Stop metformin (if using)"
  - "Stop warfarin (if instructed)"
  - "Continue aspirin and BP meds"

CATEGORY 2: "Night Before"
  - "No food after midnight"
  - "Water OK until 2h before"
  - "Confirm ride home arranged"

CATEGORY 3: "Morning Of"
  - "Arrive 2 hours early"
  - "Bring medication list"
  - "Wear comfortable clothing"

CALLOUT:
  ICON: warning
  TEXT: "Tell staff about: contrast allergies, kidney problems,
         recent bleeding, or if you might be pregnant"

FOOTER: "Educational guide. Follow your doctor's specific instructions."
```

---

## JSON Handoff Format

Provide structured copy as JSON for the infographic-generator skill:

```json
{
  "template": "infographic-checklist",
  "data": {
    "tag": "PATIENT GUIDE",
    "title": "Before Your Angiogram",
    "subtitle": "Complete preparation checklist",
    "categories": [
      {
        "title": "48 Hours Before",
        "items": [
          {"text": "Stop metformin (if using)"},
          {"text": "Stop warfarin (if instructed)"},
          {"text": "Continue aspirin and BP meds"}
        ]
      }
    ],
    "callout": {
      "icon": "warning",
      "text": "Tell staff about: contrast allergies, kidney problems, recent bleeding"
    }
  }
}
```

**Pre-handoff validation checklist:**
- All required template fields populated
- Every statistic has a source cited
- Clinical qualifiers preserved (doses, thresholds, populations)
- Each bullet ≤8 words; parallel structure within sections
- Patient-facing content reviewed for plain language

---

## Integration

**Workflow:**
1. Research → Knowledge base
2. **This skill:** Knowledge base → Structured copy + JSON
3. Infographic generator: Structured copy → Visual output

---

*Part of Dr. Shailesh Singh's Integrated Content OS*
