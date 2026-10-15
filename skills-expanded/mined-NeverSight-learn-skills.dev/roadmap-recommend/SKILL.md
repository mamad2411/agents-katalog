---
skill_id: roadmap_recommend
name: roadmap-recommend
description: Recommend the next roadmap-backed change, then after explicit confirmation scaffold it as a normal spec-driven change.
author: auto-spec-driven
type: agent_skill
version: 1.0.0
---

You are helping the user choose the next change from the roadmap and turn the
accepted recommendation into a normal spec-driven change.

## Prerequisites

The `.spec-driven/` directory must exist at the **project root**. Before
proceeding, verify:
```
ls .spec-driven/
```
If this fails, the project is not initialized. Run `/spec-driven-init` first.

If `.spec-driven/roadmap/` is missing, repair the scaffold first:
```
node {{SKILL_DIR}}/scripts/spec-driven.js init
```

## Steps

1. **Read roadmap context first** — before recommending anything, read:
   - `.spec-driven/config.yaml`
   - `.spec-driven/roadmap/INDEX.md`
   - the milestone files relevant to the current phase
   - `.spec-driven/specs/INDEX.md`
   - the relevant main spec files the recommended change is likely to touch
   - `node {{SKILL_DIR}}/scripts/spec-driven.js roadmap-status`

2. **Understand what the user wants optimized** — determine whether the user
   wants the next change chosen for impact, urgency, dependency order, risk
   reduction, or some other planning goal.

3. **Recommend one candidate change** — propose:
   - a kebab-case change name
   - which milestone it comes from
   - why it is the best next candidate
   - what alternatives were not chosen yet
   The recommended candidate MUST already appear under a milestone
   `## Planned Changes` section.

4. **Present a proposal checkpoint** — before creating any files, summarize:
   - the proposed change name
   - which milestone it comes from
   - the goal and scope of the recommended change
   - the main spec areas expected to change
   - why this item is the best next step
   - any unresolved questions that would go into `questions.md`

   Then ask for explicit confirmation. If the user wants revisions, continue the
   recommendation discussion and re-summarize until confirmed.

5. **Scaffold the change after confirmation** — run:
   ```
   node {{SKILL_DIR}}/scripts/spec-driven.js propose <name>
   ```
   This creates `.spec-driven/changes/<name>/` with the seeded templates.

6. **Fill the five proposal artifacts** — after scaffolding, complete the same
   proposal workflow used by `/roadmap-propose`:
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

7. **Validate before presenting the proposal** — run:
   ```
   node {{SKILL_DIR}}/scripts/spec-driven.js verify <name>
   ```
   - Fix any safe artifact-format issues immediately and rerun `verify`
   - If only open questions remain, treat that as expected at proposal time and
     surface those questions clearly
   - If any non-question error remains, stop and report it instead of presenting
     the proposal as ready

8. **Offer the execution handoff** — show the user the generated artifacts,
   summarize the final proposed scope, list any open questions that must be
   answered before implementation, and ask whether they want to:
   - enter `/spec-driven-apply <name>` for the stepwise execution path
   - enter `/spec-driven-auto` for the end-to-end execution path
   Do not auto-enter either execution path without the user's explicit choice.

## Rules

- Do not implement code — this skill is planning only
- Use roadmap context and roadmap-status output as the basis for recommendation
- Explain why the recommended change should come next
- Recommend only work that already exists under `Planned Changes`
- Do not scaffold proposal artifacts until the user explicitly confirms the
  recommendation summary and change name
- After confirmation, follow the same artifact-writing and validation standard as
  `/roadmap-propose`
