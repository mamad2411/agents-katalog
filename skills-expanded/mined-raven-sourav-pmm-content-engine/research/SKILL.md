# Skill: Research a Theme

## Trigger
User provides a theme for research, or research is needed before generation.

## Process

### Step 1: Load references
- **Always load:** `references/research-protocol.md`
- **Load for gap map:** `data/brain/pmm_brain.json` (pmm_value_landscape section)

### Step 2: Web Research (Stage 1)
Use WebSearch tool to research the theme from 5-8 angles:
- Statistics and hard data
- Contrarian perspectives and criticisms
- Real company case studies
- Recent developments (last 90 days)
- Adjacent domain insights
- Practitioner takes

Synthesize into a Research Brief with:
- Key claims (with source URLs)
- Evidence anchors (stats, case studies, analogies)
- Contrarian angles
- Saturation report

### Step 3: Gap Map (Stage 2)
Cross-reference research against:
- User's past posts (read from `data/user/my_posts.docx` context or ChromaDB)
- Reference writers' content (from brain's writer DNA profiles)
- PMM value landscape (from brain)

Identify: already said, white space, user unique angles, recommended angles.

### Step 4: Insight Novelty Scoring (Stage 3)
Score every candidate insight on the 1-5 Insight Novelty Scale (see `references/research-protocol.md`).
- Only insights scoring 4+ ("Opinionated" or "Earned") proceed
- If all insights score below 4, dig deeper — the research hasn't found the real angle yet

### Step 5: Anchor Assignment (Stage 4)
Assign evidence anchors to 3 recommended angles:
- 1 opinionated reframe, 1 framework, 1 story-led
- Each must have at least 1 evidence anchor AND Insight Novelty Score 4+
- Suggest hooks matching Sourav's voice

### Step 6: Present to user
Show the Research Brief summary:
- Top evidence anchors
- Saturation level
- 3 recommended angles with rationale and Insight Novelty Scores
- Ask user to confirm angles or adjust before generation

## Output Format
```
━━━━ RESEARCH BRIEF: "{theme}" ━━━━

SATURATION: [Low/Medium/High] — [what's been covered vs. what hasn't]

EVIDENCE ANCHORS:
1. [type] [content] — [source]
2. ...

RECOMMENDED ANGLES:
1. OPINIONATED REFRAME: [angle] — Novelty: [4-5]/5 — Evidence: [anchors]
2. FRAMEWORK: [angle] — Novelty: [4-5]/5 — Evidence: [anchors]
3. STORY: [angle] — Novelty: [4-5]/5 — Evidence: [anchors]

Proceed with these angles? (yes / adjust)
```

---
**See also:** `skills/generate/` (consumes research output) | `skills/suggest-themes/` (alternative entry point for theme discovery)

---
**See also:** `skills/generate/` (consumes research output) | `skills/suggest-themes/` (Brain-informed alternatives) | `skills/_index.md` for full data flow
