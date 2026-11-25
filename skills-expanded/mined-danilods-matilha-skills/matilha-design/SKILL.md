---
name: matilha-design
description: Use when user is making UX, UI, or visual-design decisions in any phase — guides via core design heuristics and delegates to matilha-design-pack or matilha-ux-pack if installed.
category: matilha
version: "1.0.0"
optional_companions: ["matilha-design-pack", "matilha-ux-pack"]
---

## When this fires

User asks "how should this look?", "is this UX good?", "what component to use?", or is about to commit design-level changes. Cross-phase; most useful in Phase 20/30 spec authoring and Phase 40 execution.

## Preconditions

- None (works at any phase).

## Execution Workflow

1. **Pack detection**: Inspect the ambient skill list for skills with plugin namespace matching `matilha-*-pack` (e.g., `matilha-ux-pack:*`, `matilha-growth-pack:*`, `matilha-design-pack:*` if installed). Group by plugin namespace. See `skills/matilha-compose/SKILL.md` for the canonical detection logic.

2. **Intent classification**: Does the user's design question touch cognitive load, error presentation, forms, accessibility, visual perception, growth-relevant moments (signup, paywall, activation), or broader design-system concerns? Use pack skill descriptions to inform the decision. Classify per pack: yes / no / partial.

3. **Route based on intent**:
   - **Narrow intent** (e.g., "which form component?", "what error format?"): invoke the single most relevant pack skill directly via the Skill tool. No preamble needed.
   - **Exploratory intent** (e.g., "how should this flow feel?", "is this UX good?"): if `superpowers:brainstorming` available AND ≥1 pack classified yes, build preamble per `matilha-compose` Step 4 template, emit it, then invoke brainstorming via Skill tool.
   - **No packs installed OR packs irrelevant**: apply core heuristics inline — simplicity (Krug Fato 1), recognition > recall (Weinschenk), progressive disclosure, consistent navigation, 5-rule error format.

4. Emit design guidance linked to the user's current task.

## Rules: Do

- Prefer companion-pack skills when available (they carry neuroscience-backed depth).
- Cite sources in core heuristics (Weinschenk, Krug, wiki concept pages).
- Keep advice specific to the user's artifact.

## Rules: Don't

- Make subjective "good/bad" claims without evidence.
- Override user's explicit `aesthetic_direction` in project-status.md.

## Expected Behavior

Actionable design guidance. With companion pack installed, output quality is deeper; without companions, output is solid-core but less specialized.

## Quality Gates

- Output references at least one heuristic (source cited).
- If companion pack invoked, mentions which one and why.

## Companion Integration

Companion-pack awareness is handled via the pack detection + intent classification in steps 1–3 of the Execution Workflow. See `skills/matilha-compose/SKILL.md` for the canonical pack detection and preamble template.

- **Any skill with plugin namespace `matilha-*-pack`** (e.g., `matilha-ux-pack:ux-*`, `matilha-ux-pack:cog-*`, `matilha-growth-pack:*`, `matilha-design-pack:*` when installed) — detected at runtime via ambient skill list. Narrow-intent design questions invoke the most relevant pack skill directly; exploratory-intent questions emit a pack-aware preamble to `superpowers:brainstorming`.
- **superpowers:brainstorming** — invoked for exploratory-intent design questions (with pack-aware preamble emitted when ≥1 pack classifies yes).
- Otherwise: apply the core heuristics documented in Step 3 (simplicity, recognition > recall, progressive disclosure, consistency, 5-rule errors).

## Output Artifacts

Usually chat output only; occasionally a commit to `docs/matilha/design-decisions.md` logging the decision with rationale.

## Example Constraint Language

- Use "must" for: cite source for any design claim.
- Use "should" for: delegate to pack when available.
- Use "may" for: log decision in `design-decisions.md` if impactful.

## Troubleshooting

- **"no pack installed and user wants deep guidance"**: Recommend installing `matilha-ux-pack` or `matilha-design-pack`.
- **"aesthetic_direction set but user wants to deviate"**: Log the deviation decision in `recent_decisions` via Edit.

## CLI shortcut (optional)

> No CLI equivalent (design guidance is inherently AI-conversational).

## Sources

- [[concepts/leis-de-krug]]
- [[concepts/reservatorio-boa-vontade]]
- [[concepts/memoria-cognicao]]
- [[sources/100-things-every-designer]]
