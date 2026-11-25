---
name: northstar
description: Use for Northstar docs-spine and AGENTS/CLAUDE instruction-surface work in this repo or a consumer project—planning, planning-readiness reviews, specs, contracts, roadmaps, research promotion, recovery after drift, ongoing normalization, and explicit AGENTS file reviews. Invoke automatically for “northstar planning readiness review”, “northstar wayfinder”, “northstar AGENTS file review”, plan, roadmap, contract, spec, research, recover, refocus, sweep, normalize/migrate/setup, readiness mapping, intent rounds, project language, decision prototypes, questionnaires, or explicit orchestrator-thread language. Handoff or continuation brief only when the user explicitly asks for a handoff, fresh thread, or spin-off—not for bare continue or context limits alone.
---

# Northstar

Single entry for the Northstar planning and docs system. **Do not** load every
mode up front.

## First step (required)

Open [`references/router.md`](./references/router.md), classify intent, then
open **one** [`references/modes/`](./references/modes/) file and follow it.

| Mode | When |
| --- | --- |
| Handoff | User explicitly asks for a continuation brief / fresh thread |
| Planning readiness review | User asks for `northstar planning readiness review` or the shorthand `northstar wayfinder` on an existing project |
| Agent instruction review | User asks for a `northstar AGENTS file review`, or to review/optimize `AGENTS.md`/`CLAUDE.md` |
| Pre-execution discovery | Readiness mapping, intent rounds, project language, decision prototypes, or questionnaires |
| Orchestrator | User wants question-led planning plus a separate worker/PR loop |
| Normalize docs | Bootstrap, migrate, or keep docs spine healthy over time |
| Research | Evidence → architecture/contracts |
| Recovery | Drifted or changed planning state |
| Planning | Default: plan, promote, compile roadmaps (sub-modes in router) |

Runtime authority comes from the target repo's `AGENTS.md` and local contracts.
When the target is the Northstar source repo, also read
`bundle-docs/protocol-kernel.md`. Its absence is normal in consumer repos and
is not a contract gap by itself.

Worker startup is intentionally light: before `effigy tasks`, `effigy doctor`,
or broad repository reads, run the router's four-command worktree probe. Reuse a
clean, dedicated, non-`main` registered launcher worktree even when its generated
path or branch differs from a handoff placeholder; never create a second one for
that reason.

## Outcomes by mode

- **Planning:** coherent architecture/contracts/roadmaps; no invented system
  behavior; ready cards only when rubric satisfied.
- **Planning readiness review:** read-only verdict on whether an existing
  project's planning is incomplete, drifted, materially ambiguous, or coherent,
  with one routed next step.
- **Pre-execution discovery:** frontier-based intent rounds and bounded
  project-language, prototype, and questionnaire routes; no execution authority.
- **Research:** promoted decisions in architecture/contracts, not stranded memos.
- **Recovery:** trustworthy planning surfaces and canonical refs restored.
- **Normalize:** baseline or strict spine installed/maintained; Effigy-first QA.
- **Orchestrator:** question-led planning, one pushed worker handoff under `docs/handoffs/`, bounded PR review loop.
- **Handoff:** a human-friendly seven-section file under `docs/handoffs/`, with
  an absolute path returned to the operator; not a substitute for log/roadmap
  closeout.

## Conversation style

Use a natural, human conversational tone across all Northstar threads. Keep useful
recommendations, trade-offs, and next steps, but do not turn ordinary replies
into dry status reports or bureaucratic protocol recitations.

- be clear, warm, and easy to respond to;
- keep the connective language that makes reasoning understandable;
- stay concise and high-signal without becoming telegraphic;
- use summaries and outcome/state/next structure when they help, not by reflex;
- preserve room for curiosity, tentative ideas, and productive exploration.

Orchestrator threads have a stronger version of this rule: act as a creative,
exploratory thinking partner as well as a planner and reviewer. Ask focused
questions, explore alternatives and edge cases, explain why a question matters,
offer recommendations without pretending they are decisions, and make it easy
for the operator to think aloud and redirect the conversation. Keep the planning
and authority boundaries firm without making the conversation feel like a
workflow form.


## Papercuts loop (required during execution)

- Locate the root of the repository that owns the work and read
  `PAPERCUTS.md` if it exists.
- When a small, solvable execution hurdle appears, append a terse entry to that
  file before continuing. If it is missing, create it without asking the
  operator.
- Capture the friction, impact, plausible fix, and affected surface. Do not
  stop the current task, wait for permission, or fix the papercut unless that
  fix is already in scope.
- Do not log ordinary one-off failures, external blockers, sensitive data, or
  duplicate open entries. Papercuts are observations for later triage, not an
  automatic backlog or roadmap commitment.

The starter file is available at `assets/templates/PAPERCUTS.md`. Seed it on
adopt/upgrade before exact-SHA / clean-tree release prep; do not add it during
tag closeout after a green pinned SHA.

## Refactoring posture

When work touches code or automation: no pre-1.0 compat shims; ask the operator
on breaking changes; from v1.0 preserve expected stable behavior. Follow the
target repo's `docs/contracts/001-working-rules.md` when present. In the
Northstar source repo, expanded doctrine lives at
`bundle-docs/sections/07-delivery-framework-and-autonomy.md`.

## Assets

- Setup/templates: [`assets/templates/`](./assets/templates/)
- Claude Code bridge: `assets/templates/CLAUDE.md.template` must reference
  `@AGENTS.md`; add Claude-only guidance there only when it cannot live in the
  shared contract.
- Papercuts starter: `assets/templates/PAPERCUTS.md`
- Handoff template: [`assets/templates/northstar-handoff.md.template`](./assets/templates/northstar-handoff.md.template)
- Orchestrator worker handoff extension: [`assets/templates/northstar-orchestrator-run.md.template`](./assets/templates/northstar-orchestrator-run.md.template)
- Handoff directory: `docs/handoffs/`
- Handoff contract: [`references/handoff-contract.md`](./references/handoff-contract.md)

## Do not

- Skip the router.
- Use handoff mode for compaction-only or ordinary `continue`.
- Start roadmap execution to discover missing contracts.
- Mirror Effigy tasks into `package.json` scripts.
- Alias `tasks.health` to `qa` (doctor orientation must stay cheap; full
  validation is `effigy qa` — see `references/setup/repo-contract.md`).
