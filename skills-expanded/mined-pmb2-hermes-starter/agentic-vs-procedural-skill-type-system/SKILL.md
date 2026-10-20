---
name: agentic-vs-procedural-skill-type-system
description: Type-system taxonomy for Hermes skills — mark each SKILL.md as 'agentic' (open-ended exploration) or 'procedural' (fixed steps), enabling auto-routing and task-appropriate skill selection
version: 1.0.0
author: Hermes Agent (Skillmate)
license: MIT
metadata:
  hermes:
    tags: [skill-taxonomy, agentic, procedural, skill-type, skill-router, meta-skill]
    triggers: [skill type, skill taxonomy, agentic vs procedural, skill classification, skill frontmatter, meta-skill]
    related_skills: [type-safe-skill-i-o-contracts, skill-library-maintenance, hermes-agent-skill-authoring]
---

# agentic-vs-procedural-skill-type-system

This type system adds a `skill_type` field to SKILL.md frontmatter: `agentic` (the agent figures out the approach within that domain) or `procedural` (exact steps to follow). The skill router then selects the right skill type per task — procedural for repetitive/known-step tasks, agentic for exploration/unknown-territory work.

## Motivation

Hermes has 380+ active SKILL.md files. Some are rigid checklists for well-understood workflows. Others are loose frameworks for exploratory domains where the agent must adapt. Without a type field:

- A procedural skill loaded for an exploratory task constrains the agent too much
- An agentic skill loaded for a well-known repetitive task wastes tokens on open-ended reasoning
- The skill router cannot make informed recommendations

## Type Definition

Add this field to every SKILL.md frontmatter:

```yaml
skill_type: procedural  # or 'agentic'
```

### `procedural` — Fixed Steps, Known Path

Use for skills where the **steps are well-defined, the output is predictable, and deviation causes errors**.

**Signals:**
- The skill has a numbered step sequence (1. 2. 3.) with explicit commands
- There's a "Verification" section with concrete checks
- Running the skill is an "execute and confirm" flow, not "explore and adapt"
- Examples: `setup-pre-commit`, `github-auth`, `static-site-deployment`

**Behavioral contract:** The agent follows the steps exactly. No creative reordering. No skipping. If a step fails, the agent reports the failure — it does not redesign the approach.

### `agentic` — Open-Ended, Domain Framework

Use for skills where **the agent must explore, adapt, and discover the path**.

**Signals:**
- The skill provides guidance, principles, and domain knowledge — not strict steps
- The output quality depends on the agent's reasoning and adaptation
- Different runs of the same skill may produce completely different approaches
- Examples: `systematic-debugging`, `writing-shape`, `domain-modeling`

**Behavioral contract:** The agent treats the skill as a framework of considerations, not a checklist. It adapts the approach to the specific situation. It can deviate from the described patterns when the situation warrants.

### Hybrid Pattern (Advanced)

A skill can contain **both** patterns via section-level annotation:

```yaml
skill_type: hybrid
```

Section-level markers in the body:
- `<!-- procedural:setup -->` — this section is a fixed checklist
- `<!-- agentic:diagnosis -->` — this section is exploratory

The agent reads the markers and switches mode per section. Hybrid is for skills like `systematic-debugging` where initial triage (agentic) leads to a repair checklist (procedural).

## Migration Strategy

### Phase 1 — Classify New Skills (Starting Now)
Every new SKILL.md must include `skill_type:` in frontmatter. Enforcement: the `hermes-agent-skill-authoring` validator should reject new skills missing this field after a grace period.

### Phase 2 — Batch-Update Existing Skills (380+)
Automated script at `scripts/classify-skills.sh` or the curation pipeline:

```bash
# Detect agentic vs procedural heuristically:
# - Has numbered steps + verification section -> procedural
# - Has long prose / frameworks / principles -> agentic
# - Both -> hybrid
find /path/to/skills -name SKILL.md | while read f; do
  if grep -qE "^## Steps?$" "$f" && grep -qE "^## Verification" "$f"; then
    echo "procedural: $f"
  elif grep -qE "^## Principles|^## Considerations|^## Framework" "$f"; then
    echo "agentic: $f"
  else
    echo "unclassifiable: $f"
  fi
done
```

### Phase 3 — Router Integration
The skill router (`skill_view` / tool-call dispatch layer) uses `skill_type` to:
- Recommend procedural skills for known-step tasks
- Recommend agentic skills for open-ended tasks
- Fall back to agentic (looser constraint) when unclassified
- Flag hybrid skills with a mode-annotation hint in the dispatch

## Verification

1. **Frontmatter check**: 100% of new SKILL.md files have `skill_type:` set
2. **Router picks correct type**: A procedural task loads a procedural skill; an exploratory task loads an agentic skill
3. **No regression**: Existing unclassified skills still load normally (agentic as default fallback)
4. **Hybrid mode-switching**: Hybrid skills correctly change behavior per section (manual spot-check)

## Pitfalls

- **False classification**: An agentic skill with a "Steps" section (e.g., `writing-shape`) would be misclassified as procedural by the heuristic script. The heuristic is a first pass — every auto-classified skill needs human/agent review.
- **Over-engineering hybrid**: Most skills are cleanly one type. Hybrid should be rare — only for skills that genuinely switch modes mid-stream.
- **Forcing change too fast**: Adding `skill_type` to 380 skills in one batch introduces risk. Phase 2 should be incremental — add the CI check, then batch-fix over a week.
- **Draft migration**: Existing _drafts already have a loose concept of this type system. The drafts README Tier 1/2/3 mapping partially correlates: Tier 1 (well-defined) → procedural candidates, vague stubs → agentic candidates. But this is a rough heuristic, not a 1:1 mapping.

## Related Skills

- **`type-safe-skill-i-o-contracts`** — Schema-validated input/output contracts for composable skills. The `skill_type` field is metadata at the dispatch layer, complementary to I/O contracts at the runtime layer.
- **`skill-library-maintenance`** — Bulk audit and reconciliation. The classification script in Phase 2 would run as a maintenance skill task.
- **`hermes-agent-skill-authoring`** — SKILL.md authoring conventions. The validator must enforce the new `skill_type` field.
