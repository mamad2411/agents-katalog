# Observe — Skill Execution Logger

## Trigger
Run **after every skill execution** (generate, distribute, expand, critique, research, showcase, suggest-themes, visual, ingest, scraper).

## Purpose
Skills cannot improve if the system has no memory of what happened when they ran. This skill logs structured observations so the system can later inspect patterns and propose amendments.

## Process

### Step 1 — Capture execution context
After a skill completes, record:
- **skill**: Which skill was executed (e.g., `generate`)
- **timestamp**: ISO date (YYYY-MM-DD)
- **task_summary**: One-line description of what was attempted
- **outcome**: `success` | `partial` | `failure`
- **format**: Which format was generated (linkedin / twitter / newsletter / carousel / all)

### Step 2 — Capture quality signals
For generation skills (generate, distribute, expand):
- Rubber Duck Escalator scores per phase (MIRROR, PROBE, CHALLENGE, ILLUMINATE, CRYSTALLIZE)
- Which phases scored below 8? (these are the weak points)
- How many revision rounds before passing?
- Which AI decontamination patterns triggered?
- Which expert library was loaded and was it relevant?
- Which angle was selected (contrarian / framework / story)?

For critique:
- Overall pass/fail
- Weakest phase and score
- Was the feedback actionable or generic?

For research:
- Insight Novelty Score distribution (how many scored 4+?)
- Gap map coverage — did it find genuine gaps?
- Were Brain sections loaded relevant?

For suggest-themes:
- Did the user accept any suggestions?
- Were suggestions novel or repetitive of past themes?

For visual:
- Did the visual match the post's framework?
- Was the layout pattern appropriate?

For ingest/scraper:
- Data quality — errors, empty results, parsing failures?
- Were new mental models or evidence extracted?

### Step 3 — Write observation log
Write the observation to `_logs/` using this format:

```markdown
---
skill: {skill_name}
timestamp: {YYYY-MM-DD}
outcome: {success|partial|failure}
format: {format_if_applicable}
---

## Task
{One-line summary}

## Result
{What happened — 2-3 sentences max}

## Quality Signals
- Rubber Duck scores: M:{x} P:{x} C:{x} I:{x} C:{x}
- Revision rounds: {N}
- Decontamination triggers: {patterns}
- Expert loaded: {name} — relevant: {yes|no}

## Drift Indicators
{Signs that this skill's instructions may need updating}
- Format practices outdated? (platform algorithm changes)
- Brain data stale? (new mental models not reflected)
- Expert technique misapplied?
- Angle selection bias? (same angle always chosen)
```

**File naming**: `_logs/{skill_name}-{YYYY-MM-DD}-{seq}.md`

### Step 4 — Flag critical observations
If outcome is `failure`, or Rubber Duck score < 6 on any phase, or same drift indicator appears 2+ times, append to `_logs/_flags.md`:
```
- [{timestamp}] {skill_name}: {one-line description of issue}
```

## Primary Metric
**Rubber Duck first-attempt pass rate** — % of drafts that score 8+ on all 5 phases without revision.

This is the single number that tells us if the generation skills are working. Track it in each observation log's frontmatter:
```
first_attempt_pass: {yes|no}
```

When this rate drops below **50%** over 10+ generation runs, the generation or critique skill needs inspection.

## Auto-Learn Gate
Before logging an observation, it must pass ALL 4 criteria:
1. **Genuine discovery** — not just a routine pass or a standard decontamination trigger
2. **Durable value** — will this signal still matter in 6 months?
3. **Verified signal** — the quality signal is confirmed, not speculative
4. **Clear trigger** — you can describe exactly what condition caused it

If any criterion fails, skip the log. This prevents observation noise.

## Rules
- Keep observations factual, not interpretive
- Never modify skill files from this workflow — observation only
- One log file per skill execution
- Apply the Auto-Learn Gate — do not log routine successful runs that don't pass all 4 criteria
