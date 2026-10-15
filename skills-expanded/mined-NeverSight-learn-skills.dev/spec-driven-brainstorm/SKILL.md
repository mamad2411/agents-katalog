---
skill_id: spec_driven_brainstorm
name: spec-driven-brainstorm
description: Discuss and brainstorm a spec-driven change from a rough idea, then propose a change name and, after explicit confirmation, generate the same five proposal artifacts as spec-driven-propose.
author: auto-spec-driven
type: agent_skill
version: 1.0.0
---

You are helping the user turn an early-stage idea into a spec-driven change
proposal.

## Prerequisites

The `.spec-driven/` directory must exist at the **project root**. Before
proceeding, verify:
```
ls .spec-driven/
```
If this fails, the project is not initialized. Run `/spec-driven-init` first.

## Steps

1. **Start from the idea, not the artifact list** — ask the user what they want
   to achieve, what problem they are trying to solve, and any known constraints
   or preferences. Do not require a change name up front.

2. **Read project context and existing specs early** — before narrowing scope,
   read:
   - `.spec-driven/config.yaml` — use `context` as project background and treat
     `rules` as binding constraints
   - `.spec-driven/specs/INDEX.md` — identify existing spec areas that may
     already cover the requested behavior
   - Every relevant main spec file referenced by `INDEX.md` that appears related
     to the idea being discussed

3. **Brainstorm until the change is decision-ready** — use the discussion to
   converge on:
   - the desired outcome and user-visible behavior
   - what is in scope and explicitly out of scope
   - important tradeoffs, constraints, risks, and unchanged behavior
   - which existing spec files will likely be modified, or whether a new spec
     area is needed
   - any questions that still need a human answer before implementation

4. **Suggest the change name** — once the idea is coherent enough, propose a
   short kebab-case change name. If the user already provided a valid name, keep
   it. If not, suggest one that reflects the agreed change scope.

5. **Present a proposal checkpoint** — before creating any files, summarize:
   - the proposed change name
   - the goal and scope
   - the main spec areas expected to change
   - key decisions or tradeoffs already settled
   - any unresolved questions that would go into `questions.md`

   Then ask for explicit confirmation. If the user wants revisions, continue the
   brainstorm and re-summarize until confirmed.

6. **Scaffold the change after confirmation** — run:
   ```
   node {{SKILL_DIR}}/scripts/spec-driven.js propose <name>
   ```
   This creates `.spec-driven/changes/<name>/` with the seeded templates.

7. **Fill the five proposal artifacts** — after scaffolding, complete the same
   proposal workflow used by `/spec-driven-propose`:
   - write `proposal.md` with **What**, **Why**, **Scope**, and
     **Unchanged Behavior**
   - write `design.md` with **Approach**, **Key Decisions**, and
     **Alternatives Considered**
   - populate `changes/<name>/specs/` with delta spec files aligned by path with
     the main `.spec-driven/specs/` structure
   - write `tasks.md` with atomic checklist items under `## Implementation`,
     `## Testing`, and `## Verification`
   - write `questions.md`, recording every unresolved point under `## Open`, or
     leave `<!-- No open questions -->` if nothing is unclear

8. **Validate before presenting the proposal** — run:
   ```
   node {{SKILL_DIR}}/scripts/spec-driven.js verify <name>
   ```
   - Fix any safe artifact-format issues immediately and rerun `verify`
   - If only open questions remain, treat that as expected at proposal time and
     surface those questions clearly
   - If any non-question error remains, stop and report it instead of presenting
     the proposal as ready

9. **Hand off like propose** — show the user the generated artifacts, summarize
   the final proposed scope, and list any open questions that must be answered
   before `/spec-driven-apply`.

10. **Offer auto hand-off** — after the hand-off, ask the user whether to enter
    `/spec-driven-auto` to execute the proposal end-to-end, or continue modifying
    the proposal with `/spec-driven-modify`. Do not auto-enter auto without the
    user's explicit choice.

## Rules

- Do not implement code — this skill is planning only
- Do not scaffold proposal artifacts until the user explicitly confirms the
  brainstorm summary and change name
- Read `.spec-driven/config.yaml`, `INDEX.md`, and relevant main specs before
  locking scope or writing delta specs
- Suggest a kebab-case change name when the user starts with only a rough idea
- Record unresolved ambiguity in `questions.md`; do not guess silently
- After confirmation, follow the same artifact-writing and validation standard as
  `/spec-driven-propose`
