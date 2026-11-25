---
name: skill-forge-create
description: "Create a new SKILL.md via discovery recap, pattern selection, WebFetch spec fetch, knowledge delta discipline, skill-forge-judge + skill-forge-hitl quality gate. Triggers: create a skill, write a skill, new skill, SKILL.md, build a skill."
---

# Skill Forge Create

Write skills that score ≥B on skill-forge-judge out of the box. Every section must earn its tokens.

---

## Phase 1 — Discovery

Build understanding through a running recap. Ask questions to fill gaps; after each exchange, show the current recap:

```
## Discovery Recap

**Domain:** [what the skill covers, or "unknown"]
**Decisions:** [non-obvious choices the agent must make, or "unknown"]
**Failure modes:** [what breaks without this skill, or "unknown"]
**Audience:** [fragile/creative output, or "inferred: ..."]
**Size:** [reference files needed, or "inferred: self-contained"]
```

Then ask: `(a)ccept / (r)evise / (q)uit`

- `a` — recap is complete; proceed to Phase 2
- `r` — user adds or corrects; update recap and loop
- `q` — abort

Do not proceed to Phase 2 until the user accepts the recap. Domain, decisions, and failure modes must be filled before accepting — do not accept a recap with "unknown" in those three fields.

---

## Phase 2 — Pattern Selection

**MANDATORY — READ [`references/pattern-selection.md`](references/pattern-selection.md)** before selecting a pattern. Do NOT load this file during Phase 1, Phase 3, or later phases.

Select one pattern. State your choice and the one-line reason before drafting.

---

## Phase 3 — Draft

**MANDATORY — WebFetch `https://agentskills.io/specification`** before writing the description. Use the live spec to verify current frontmatter requirements and description field constraints. If unreachable, proceed with the spec knowledge already in context; note it in the draft.

Write the description before the body. Draft the body around what the description promises.

Write to earn tokens. For every paragraph, ask: **"Does Claude already know this?"**

- If yes → delete it
- If "it's a useful reminder" → one line max, then move on
- If no → expand it; this is the value

Before writing each section, ask: **"What failure mode does this prevent?"** If you can't answer, you haven't earned the paragraph.

**Description requirements** (THE most critical field):
- Answers WHAT (what does it do?)
- Answers WHEN (trigger scenarios — "Use when...", "Trigger phrases:")
- Contains searchable KEYWORDS (domain terms, file extensions, action verbs)
- Max ~200 chars for the core sentence; trigger phrases can follow

**NEVER rules format** — every NEVER must have:
```
- **NEVER [specific construct/pattern]**
  **Instead:** [concrete alternative]
  **Why:** [non-obvious failure mode this avoids]
```

Vague warnings ("be careful", "avoid errors") are prohibited.

**Progressive disclosure thresholds**:
- Body > 300 lines → move heavy content to `references/`
- Any section with a decision tree of 4+ branches → extract to `references/` regardless of total line count
- Add MANDATORY READ triggers at the exact workflow step that needs it
- Add "Do NOT load" guidance for files irrelevant to the current scenario

---

## Phase 4 — Self-Evaluate

Invoke `/skill-forge-judge` on the draft. (Requires skill-forge-judge to be installed — if missing, ask the user to install it before continuing.)

Target: ≥B (80%+). For a SKILL.md with no bash guidance → U + S (120 pts max) → ≥96 pts.

Always invoke `/skill-forge-hitl` on the numbered improvements list skill-forge-judge produced, regardless of grade. Do not apply fixes manually — that's /skill-forge-hitl's job.

If the /skill-forge-hitl loop stalls on a dimension (same item rejected after 3 revisions), surface it to the user: "Stuck on [dimension] — here's what I tried. Options: accept the current draft, revise the scope, or skip."

---

## NEVER

- **NEVER write a section that restates Claude defaults** ("write clean code", "handle errors", "be helpful")
  **Instead:** Ask: "Would Claude do this without being told?" If yes, delete it.
  **Why:** Default restatements dilute expert signal and train authors that padding is acceptable.

- **NEVER add a NEVER rule without WHY and INSTEAD**
  **Instead:** Complete the three-part format before moving on.
  **Why:** A prohibition without an alternative gets violated when the obvious path is blocked.

- **NEVER dump all content in SKILL.md**
  **Instead:** Keep body under 300 lines; move detail to `references/` with MANDATORY READ triggers.
  **Why:** A 700-line SKILL.md loads all at once on every invocation — the agent drowns in irrelevant content.

- **NEVER skip Phase 4** (skill-forge-judge self-eval)
  **Instead:** Run it even if the draft feels good.
  **Why:** Skills that skip self-eval consistently have U1 or U3 gaps that aren't obvious to the author.

- **NEVER manually apply skill-forge-judge findings one-by-one**
  **Instead:** Invoke `/skill-forge-hitl` on the numbered improvements list skill-forge-judge produced.
  **Why:** Manual application skips the approval loop, bundles changes without diffs, and defeats the purpose of the numbered improvements format.

- **NEVER add README.md, CHANGELOG.md, or documentation about the skill itself**
  **Instead:** Include only what the agent needs to perform the task.
  **Why:** Meta-documentation about the skill is never loaded during execution — it wastes directory space and signals the wrong mental model (skill as software project, not agent instruction).

