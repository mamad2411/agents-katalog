---
name: cobb
description: "Product-development workflow toolkit. Subcommands: prd, design, implement, review, commit (incl. finalise and hotfix modes), context, compact. Use to create/update/list PRDs, design UI/UX/motion/imagery, implement a PRD in code, review a branch for correctness/security/scope, create atomic commits and finalise a branch, maintain tasks/context.md, and compact it. Triggers: cobb, write prd, plan feature, create spec, list prds, design ui, improve ux, add transitions, implement prd, build feature from prd, review branch, readiness check, commit changes, split commits, finalise branch, hotfix, urgent fix to main, update context, decision log, compact context."
---

# cobb

A single skill for ongoing product development. Route a request to the right phase, then execute that phase under the shared guardrails below.

The full flow is: `prd` → `design` (optional, UI/UX-heavy work) → `implement` → `commit` (`commit` mode, followed by automatic `review`) → selected fixes/suggestions and re-review when needed → `commit` (`finalise` mode) → `compact` (periodic). `context` is captured inline throughout, not as a separate step.

Default delivery order: `implement -> commit -> review -> finalise`. Review the stable atomic branch diff, not a moving pre-commit worktree.

---

## Progressive Disclosure Contract

This file is navigation, not the full operating manual. On activation:

1. If `AGENTS.md` exists in the repo root and has not already been read in this context, read it first — it carries repo-wide instructions and points to `SOUL.md` (voice) and `MEMORY.md` (lessons). Read it once per session, not per phase.
2. Do not preload every file listed in References.
3. Load only the selected phase reference from Dispatch.
4. For nested routers, load the router first, then only the selected child reference.
5. Load templates, examples, and secondary references only when the selected reference explicitly requires them for the current task.
6. For multi-phase requests, complete one phase at a time and load the next phase reference only when that phase begins.

---

## Dispatch

Parse the first token of the args and route to the matching phase. Load **only** that phase's reference file, then execute it.

| First token              | Phase            | Load reference                  |
|--------------------------|------------------|---------------------------------|
| _(none)_                 | orchestrate      | (no file — see "Bare `/cobb`")  |
| `prd`                    | PRD create/update/list | `references/prd.md`       |
| `design`                 | design sub-router (ui/ux/motion/imagery) | `references/design.md` |
| `implement`              | implement a PRD  | `references/implement.md`       |
| `review`                 | branch review    | `references/review.md`          |
| `commit`                 | atomic commit    | `references/commit.md`          |
| `commit finalise` / `finalise` | finalise branch | `references/finalise.md` |
| `commit hotfix` / `hotfix` | hotfix commit  | `references/commit.md` (hotfix mode) |
| `context`                | maintain context.md | `references/context.md`      |
| `compact`                | compact context.md | `references/compact.md`       |

### Routing rules

1. If the first token matches a phase, load that reference and execute it; pass the rest of the args through as the phase's input.
2. If no token matches but intent is clear from the request (e.g. "write a prd for X" → `prd`, "review my branch" → `review`), infer the phase, state which phase you picked in one line, then proceed.
3. If intent is ambiguous, fall back to the bare `/cobb` behaviour below.
4. `design` is itself a router: `/cobb design ui` selects the `ui` mode inside `references/design.md`.

### Bare `/cobb` (no subcommand)

Do not execute any phase. Instead:

1. Read `tasks/` — list active PRDs (`f-##`, name, `Status`, `Priority`) and check git branch/commit state.
2. Print the subcommand menu (the dispatch table above) so the user sees the options.
3. Render the phase recommended from repository state as option `0` **Recommended** and the remaining phases as `1..N` (do not repeat the recommended phase in `1..N`). Do not require the user to type a command name.
4. Recommend the single next phase based on state, for example:
   - no `tasks/context.md` or no PRDs → "start with `/cobb prd`"
   - a `Status: ready` PRD with no feature branch → "`/cobb implement <prd>`"
   - feature branch ahead of base with uncommitted changes → "`/cobb commit` (review runs after the final clean commit group)"
   - all commits reviewed and clean on a feature branch → "`/cobb commit finalise` (it trusts the completed review and merges)"
   - all commits done but not yet reviewed → "`/cobb review`, then `/cobb commit finalise`"
   - `tasks/context.md` long/noisy → "`/cobb compact`"
5. Wait for the user's option number or explicit subcommand before acting.

---

## Shared Guardrails (apply to every phase)

- **Number every closed choice.** Whenever a response ends by asking the user to choose, confirm, approve, continue, stop, or select a next step, provide numbered reply options. Accept the number alone. Use open-ended input only when honest answers cannot be bounded without losing essential information.
- **Option `0` is the recommendation.** In every numbered menu, render exactly one recommended choice as `0` **Recommended:** with a brief evidence-based reason (repository evidence, safety, best practice, critical reasoning), and render each alternative once as `1..N`. Never repeat the `0` option inside `1..N`. Accept `default` as an alias for `0`. The recommendation may be to stop, investigate, split, or defer; do not mechanically recommend proceeding. Wherever a phase reference says "mark one **Recommended**", it means render that choice as option `0`. Sole exception: commit finalise uses per-field codes such as `1A 2B`, where `0`/`default` selects the recommended complete bundle.
- **Show questionnaire progress.** Before a one-question-at-a-time interview, explore enough context to build the question queue and state the total. Label every prompt `Question X of Y`. If a new answer creates or removes dependent questions, announce the revised total and why before continuing.
- **Context capture is built-in.** Update `tasks/context.md` inline whenever durable decisions, risks, or gotchas emerge, except in read-only `review`, which reports proposed entries for the next implement/finalise commit. Context updates include a README freshness check for affected areas. See `references/context.md` for what/where to record.
- **Honour repo instructions.** Follow the repo's `AGENTS.md` (if present) for any files you touch; it is read once at activation (see Progressive Disclosure Contract).
- **Handoff-friendly.** Assume a junior dev (or another AI) picks this up later. Plain language, explicit edge cases, no hidden assumptions.
- **Never claim untested success.** Do not say tests/checks/builds passed unless you actually ran them; if you didn't run it, say so.
- **Status block.** End every standalone phase reply with:
  - **Files changed**: created/updated files
  - **Key decisions**: assumptions or choices made (if any)
  - **Next step**: recommended next phase or action
  - If the next step requires a user decision, follow it immediately with numbered options and one **Recommended** option.

---

## Files cobb manages

- `tasks/f-##-<slug>.md` — one PRD per feature, with `Status` (draft | ready), `Priority` (P0–P3), `Type` (feat | fix | chore), and a progress checklist.
- `tasks/context.md` — durable project state, key decisions, milestones, gotchas (handoff record).
- `tasks/archive/` — completed PRDs moved here during `commit` finalise (same filename, no rename).

---

## References

Phase bodies (loaded on dispatch only):

- `references/prd.md` — create, update, or list PRDs.
- `references/design.md` — design sub-router (ui / ux / motion / imagery); selects one child reference.
- `references/implement.md` — implement a PRD and check off progress.
- `references/tdd.md` — shared behavioural testing contract, loaded by PRD/implement only when applicable.
- `references/review.md` — branch review with a go/no-go decision.
- `references/commit.md` — atomic commit core and hotfix mode.
- `references/commit-review.md` — post-commit review action tree; load only after a review result.
- `references/finalise.md` — finalise/merge/cleanup mode; load only for finalise.
- `references/context.md` — maintain `tasks/context.md` (inline or standalone).
- `references/compact.md` — compact `tasks/context.md`.

Conditional design references (load only after `design` routes):

- `references/design/ui.md`
- `references/design/ux.md`
- `references/design/motion.md`
- `references/design/imagery.md`
- `references/design/ui-tokens.md` — only for Tailwind/token-system changes.
- `references/design/ui-examples.md` — only when concrete snippets are needed.

Templates and rubrics (loaded only when the active phase asks for them):

- `references/templates/prd-template.md`
- `references/templates/report-template.md`
- `references/templates/context-template.md`
- `references/templates/compact-templates.md`
- `references/templates/commit-rules.md`
- `references/templates/finalise-policy.md`
