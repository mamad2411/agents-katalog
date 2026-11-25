---
name: awesome-plan
description: Plan-first workflow: research, draft a readable plan, get approval, execute, track in TODO.md, or in the conversation when the task changes no repo file.
---

# awesome-plan

Core loop: **research → plan → approve → execute → track**.

## Concepts

- **Epic**: a `.agents/plans/<date>-<slug>/` dir holding `PLAN.md` (what/why) and
  `TODO.md` (checklist). An epic is *active* while its TODO.md has open `- [ ]` items.
- **Repo plan vs in-context plan**: a repo plan is an epic dir (above). An
  in-context plan carries the same content in the conversation: the plan in a
  reply, and a `- [ ]` checklist kept there and ticked with `- [x]` as items
  land. Use a repo plan when the task changes files in this workspace. When
  the work product lives anywhere else (another system such as Notion or
  Google Docs, another repository, an answer to a question), use an in-context
  plan and create nothing in this repo.
- **Fast path**: skip plan+approval when the change is trivial (one-liner,
  single-file tweak) or the user's message already is the plan. When unsure, plan.
- **Approval gate**: never execute a non-trivial plan before the user replies `go`.
  Feedback → refine the plan → ask again.
- **Decided plans**: a plan shown for approval contains decisions, not open questions.
- **Delegation tiers**: long-running items run in sub-agents, never in the
  coordinator's own loop. Mechanical, spec-only work → the cheap `awesome-worker`
  (fast model; it reports a terse result with minimal reasoning). Reasoning-heavy
  work → a sub-agent on the parent-tier model. Parallel sub-agents share the one
  working tree and TODO.md — partition by disjoint files. The coordinator
  validates every returned result before ticking anything.
- **Visual-first review**: approval summaries use show-me style visuals (trees,
  flows, diffs) over prose — the user should grasp the plan at a glance.
- **Challenge the idea**: don't silently accept the request. Push back
  respectfully on weak assumptions, risks, and hidden costs; name them in the
  plan or the approval ask rather than agreeing to a shaky shortcut.
- **Research, don't ask**: find answers yourself from code, docs, and web
  before asking the user; ask only what only the user can decide.
- **Ask before shifting the ask**: when planning would change the original
  request — a tradeoff, scope cut, or different approach — name the shift and
  get the user's confirmation before writing it into the plan.

## Workflow

1. **Place the task.** Add it to the active epic whose goal it matches. If the
   message only asks to continue, resume the active epic (the one with open
   items) instead of adding a task. Several match → ask which. None fits → ask
   before creating a new epic. Never invent one silently. A task that changes no
   file in this repo has no epic: keep it as an in-context plan (step 3) and
   create nothing on disk.
2. **Research before deciding.** Resolve non-obvious questions from code, docs,
   web, and prior epics *before* writing the plan. Research, don't ask: check
   the codebase and docs yourself first; challenge the idea with what you find
   and name risks/tradeoffs instead of rubber-stamping the request. Compare
   real options; name rejected alternatives and why they lost. Surface
   trade-offs, limitations, and contradictions to the user rather than picking
   silently. When the plan shifts from the original ask (tradeoff, scope,
   approach), get the user's confirmation while planning — not after. If
   something is truly undecidable, make it the first TODO item and flag it in
   the approval ask — never hide an open decision inside implementation work.
3. **Draft the plan.** PLAN.md sections, or the same sections in the approval
   reply for an in-context plan: Goal, Approach, Decisions (one-line rationale
   each), Milestones, Risks — short, one idea per line. TODO.md: small,
   independently verifiable items in execution order, and the in-context
   checklist holds the same items.
4. **Ask approval — visual-first, like the show-me skill.** Brief prose,
   then the smallest visuals that make the plan reviewable: a file tree for
   scope, a mermaid or flow sketch for the approach, a diff-shaped sketch when
   changing existing structures, one line per decision with its rationale. End
   with: "Reply `go` to execute, or give feedback to refine." Then stop.
5. **Execute on `go`.** Work top to bottom. Give each item only a minimal check
   (it exists, runs, no syntax error) and mark `[x]` right away — update TODO.md,
   or the in-context checklist, as you go, never batch status at the end. Leave
   the full tests, build, and similar checks for the final verification step.
   Keep TODO.md current as scope evolves. Write the smallest change that works
   — reuse what exists, prefer the standard library and native features over new
   code or dependencies, skip unrequested abstractions — and keep the prose
   terse: code first, no filler, say only what's needed.
6. **Parallelize independent items.** Run them as background sub-agents in the
   same working tree — no worktrees, no branches. All read the same plan, PLAN.md
   or the in-context one, and share the one checklist. Split items across disjoint
   files so edits don't collide, and let the coordinator own the `[x]` ticks so
   TODO.md isn't written concurrently. `awesome-worker` for mechanical specs, a
   same-tier sub-agent for reasoning-heavy items; validate each result before
   ticking it.
7. **Verify at the end.** Once every item is done, run the project's real checks
   — tests, build, typecheck, lint as applicable — as their own step; fix and
   re-run until green.
8. **New effort → new session.** For work that changes a repo, create a new
   date-prefixed epic dir and delegate execution to a fresh same-tier sub-agent (it
   carries judgment, so not the worker); this session supervises and validates.
