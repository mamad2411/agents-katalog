---
name: i2r-elicitation-mode
description: Cold-start interview discipline for I2R intake and context stages — separates STATED past-behavior evidence from ASSUMED generics, maps assumptions by risk. Internal I2R authoring mode.
when_to_use: When `i2r-intake-clarifier` or `i2r-context-analyst` is processing a raw idea or clarification answers before writing `01-intake.json` or `02-context.json`, and needs to classify evidence and surface riskiest assumptions.
user-invocable: false
---

# i2r-elicitation-mode

## Purpose

This mode governs how I2R agents extract signal from a founder's raw idea or interview answers. It encodes two disciplines that prevent the most common early-stage defects — vague generalizations promoted to `stated` evidence, and hidden assumptions that silently become requirements.

Sources: The Mom Test (Rob Fitzpatrick) for evidence discipline; BMAD analyst/brainstorming pattern for assumption mapping; Product Requirement Craft (problem framing) for STATED/ASSUMED/DECISION separation.

**Vendor-not-install:** these are I2R-local implementations; no runtime calls to external skills.

---

## The three-bucket separation (most important rule)

Every piece of information from a founder or brief falls into exactly one bucket:

| Bucket | Meaning | Schema key |
|---|---|---|
| `stated` | Direct evidence of past or specific behavior | `stated[]` in `01-intake.json` |
| `assumed` | Inference or generic claim not yet evidenced | `assumed[]` in `01-intake.json` |
| `decisions` | Explicit scoping choice or locked constraint | `decisions[]` in `01-intake.json` |

**Never silently promote an assumption to `stated`.** An agent that conflates these produces UNSOURCED requirements — a BLOCKER per CONTRACT §7.

Full classification rules and examples: `references/mom-test-filter.md`.

---

## Assumption map

Every `assumed[]` entry must carry a structured risk assessment:

```json
{
  "text": "Only internal support staff use this tool",
  "category": "viability",
  "importance": "high",
  "evidence": "medium",
  "risk": "medium",
  "source_ref": "raw/idea.md#L6"
}
```

`category` ∈ `{ desirability | viability | feasibility | usability }`

**Risk escalation rule:** an assumption with `importance: high` AND `evidence: low` is **riskiest** — it must surface as a `blocking` open question. The agent may not proceed to scope without resolving it.

Full assumption map model and risk escalation: `references/assumption-map.md`.

---

## Quick-reference filter rules

1. **Keep as `stated`:** direct quote of past/specific behavior with a `source_ref` to `raw/`.
2. **Demote to `assumed`:** any generic ("I usually do X"), future promise ("I will need Y"), or hypothetical ("I might want Z") — classify and risk-score.
3. **Promote to `decisions`:** explicit scoping choice locked by the founder/brief that I2R must respect as a constraint.
4. **Surface as `open_questions`:** riskiest assumptions (high importance + low evidence) and any information that would materially change `FR/NFR/scope` if wrong.

---

## Output discipline

- Every `stated[]` entry has a `source_ref` pointing into `raw/`.
- Every `assumed[]` entry has all four risk fields: `category`, `importance`, `evidence`, `risk`.
- `open_questions[]` lists only blocking questions (non-blocking → resolved with an assumption, never asked).
- `clarification_status` = `"needs_clarification"` if any open question is blocking; otherwise `"clear"`.
- Never fabricate a `source_ref`. If evidence is absent, it is `assumed`, not `stated`.
- When recording a `decisions[]` entry, also fill the OPTIONAL fields the raw idea actually grounds — `context` (what prompted it), `rationale` (why), `consequences` (what it implies), `reversibility` (can it be undone), and `alternatives`/`tradeoffs` — ONLY when the idea states or directly implies them. Omit any field the idea does not support; never fabricate a rationale. These project into the ADR body (`out/decisions/ADR-*.md`).

---

## What this mode does NOT do

- Does not author functional requirements (that is `i2r-fr-authoring-mode`).
- Does not decide scope (that is `i2r-scope-mode`).
- Does not ask the user directly — only the root orchestrator (`i2r-orchestrator`) surfaces blocking questions per `i2r-discussion-mode`.
