# Skill: Critique a Draft

## Trigger
User submits a draft for critique, or critique runs as part of generation.

## Process

### Step 1: Load references
- **Always load:** `references/rubber-duck-escalator.md`
- **Load for voice check:** `data/brain/pmm_brain.json` (voice_profile_sourav, quality_bar_examples)

### Step 2: Run 5 phases sequentially
Each phase sees the draft + all prior phase results:

1. **MIRROR** — Is this lived experience or knowledge-reporting?
2. **PROBE** — What uncomfortable truth is being dodged?
3. **CHALLENGE** — Where is the logic soft? Evidence check.
4. **ILLUMINATE** — What threads haven't been connected?
5. **CRYSTALLIZE** — Does it sound like Sourav specifically?

### Step 3: Score and gate
- Score each phase 1-10 (critique first, score based on own critique)
- All 5 must be 8+ to pass
- If any < 8: provide specific rewrite instructions
- If composite < 4.0: flag for fundamental rethinking

### Step 4: Present scorecard
Show phase-by-phase results with specific line references.

## Output Format
```
━━━━ RUBBER DUCK SCORECARD ━━━━

MIRROR:      [score]/10 — [one-line summary]
PROBE:       [score]/10 — [one-line summary]
CHALLENGE:   [score]/10 — [one-line summary]
ILLUMINATE:  [score]/10 — [one-line summary]
CRYSTALLIZE: [score]/10 — [one-line summary]

COMPOSITE: [score] | STATUS: [PASS/REWRITE/FLAG]

[If REWRITE: specific instructions ranked by severity]
[If FLAG: what needs fundamental rethinking]
```

---
**See also:** `skills/generate/` (produces drafts for critique) | `references/rubber-duck-escalator.md` (full protocol)

---
**See also:** `skills/generate/` (revision loop with critique) | `references/rubber-duck-escalator.md` (full protocol) | `skills/_index.md` for full data flow
