---
name: dipesh-task-planner-skill
description: "Plan-first workflow for any non-trivial coding task in any repo or language — new feature, change request, refactor, migration, integration or multi-file bug fix. Understands the requirement, reads the repo's own rules/docs/code, raises doubts, presents ONE plan (3-5 tasks in dependency waves) for a single approval, then executes (in parallel subagents where available), updates docs alongside code, verifies end-to-end and hands over a manual test checklist. Never commits or pushes until asked. Use whenever the user describes work that touches more than one file or needs decisions — \"build/implement/add X\", \"new requirement\", \"change request\", \"plan this task\", \"break this down\", \"how should we implement\", a plain-language task or feature description, a pasted ticket/spec/user story — even if they don't ask for a plan. Also use for plan-only requests (\"just plan it, don't code yet\"). Skip for typos, one-liners and pure questions."
---

# Dipesh Task Planner

A repeatable path from "here's a requirement" to "here's working, verified, documented
code". Works in any language, framework, repo size and coding agent (Claude Code, Codex,
Cursor, …). Follow the phases in order. The plan in Phase 4 is the **only** approval gate;
after it, execute without asking again — re-asking after approval is the most common way
this workflow wastes the user's time.

**Skip this workflow** for a typo, a one-line/obvious fix, a single-constant change or a
pure question — just do it.

**Scale it to the work.** The phases are a checklist, not a ceremony:

| Size | Looks like | How much of the workflow |
|---|---|---|
| Small | 2-3 files, one layer, no open decisions | Phases 1-4 in one short message (restate + plan), then execute; verification still mandatory |
| Medium | several files/layers, a decision or two | Full workflow |
| Large | many layers, schema changes, > 5 natural tasks | Propose splitting into separate features first; plan only the first one |

**Plan-only mode.** If the user asks for a plan, estimate or breakdown ("just plan it",
"don't code yet"), stop after Phase 4 and say what approval would kick off.

**Without agent extras.** Subagents, task lists and question UIs are accelerators, not
requirements. Where they're missing, do the same steps sequentially and ask questions as a
plain numbered list.

**The repo always wins.** Wherever this skill and the project's own instructions
(`CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, rules files, a team playbook) disagree, follow
the project. This skill gives the shape; the project gives the specifics.

---

## Phase 1 — Understand

Any input works: a plain-language description of a task or feature ("add CSV export to
the reports page"), a few bullet points, a pasted ticket/spec/user story, or a link. A
ticket ID, issue number or formal spec is **never required** — do not ask for one or wait
on one. If a ticket reference is given, use it (fetch it when a tool allows, use it in the
branch name); if not, work from the description and fill gaps through Phase 3 questions.

Restate the requirement in a few lines:

- **Goal** — what the user (or system) can do afterwards that it cannot do now.
- **In scope / out of scope** — say explicitly what you will *not* build.
- **Surfaces touched** — e.g. API, background jobs, database schema, UI, CLI, config,
  infrastructure, docs, public interfaces other teams depend on.
- **Acceptance** — how anyone will know it works.

## Phase 2 — Recall the repo (before planning)

Never plan from how the code "probably" works. Read what applies:

| Need | Look for |
|---|---|
| Agent / contributor instructions | `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`, `CONTRIBUTING.md`, `.claude/rules/`, `docs/adr/` |
| Architecture and flows | `README.md`, `docs/`, `ARCHITECTURE.md`, diagrams |
| How to build, test, lint, run | `package.json` scripts, `Makefile`, `justfile`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Taskfile`, CI config (`.github/workflows/`, `Jenkinsfile`, `.gitlab-ci.yml`) |
| Conventions in practice | 2-3 neighbouring files of the kind you will write, and their tests |
| History of the area | `git log --oneline -- <path>`, recent PRs, any memory/notes folder the project keeps |
| The code itself | modules you will change, their callers, and their tests |

Note the project's **test, lint, typecheck and run commands** — Phase 6 and 7 need them.
If none are documented, infer from CI config and say so.

**Research in parallel when you can.** If your environment supports subagents, split the
recall into independent questions ("how does auth work here", "where are jobs enqueued",
"what does library X actually support") and launch one read-only agent per question in a
single message. Keep only their conclusions (file:line references, facts, open questions),
not file dumps. If subagents aren't available, do the same reads yourself, one question at
a time.

## Phase 3 — Doubts and suggestions

Before any plan, post:

- **Doubts** — ambiguities that change what gets built.
- **Suggestions** — a simpler approach, existing code to reuse, risks, conflicts with an
  existing rule or convention.

Ask only about decisions that are genuinely the user's (product behaviour, trade-offs,
scope). Put the recommended option first. Pick conventional defaults yourself and state
them. Wait for answers before planning.

When a decision needs evidence (compare two libraries, probe what an API really returns,
weigh two designs), investigate each option separately — in parallel subagents if
available — and recommend one, rather than presenting a survey.

## Phase 4 — Plan (single approval)

Present the plan in this shape:

```
## Plan: <feature>
Approach: <2-4 sentences>
Changes:
- <area/layer>: <files / modules / endpoints / components>
- <area/layer>: …
- schema/data: <migration name + what it adds> (or "none")
- config/env: <new settings> (or "none")
- docs: <README / docs / instructions files / diagrams to update>
Tests: <unit / integration / e2e / manual>
Risks: <breaking changes, data, performance, security>
Tasks (3-5):
 1. <task> — verify by <…> — owner: main | subagent — depends on: none | N
 2. …
Waves (tasks with no unmet dependency run together):
 Wave 0 (main, inline): shared contract — types/schemas, constants, migration, interfaces
 Wave 1 (parallel):     tasks 2, 3, 4 — files owned: <task → files, disjoint>
 Wave 2 (parallel):     task 5 + review
```

- 3-5 tasks. Fewer for small work; split bigger work into separate features.
- Default to the widest safe wave: two tasks are parallel unless one consumes the other's
  output or they share a file.
- Create a feature branch (`feature/<slug>` or the project's naming) from the current base.
  With no ticket ID, derive the slug from the description (`feature/csv-export-reports`);
  if the project's naming demands an ID, name it without one and mention it, don't block.
  Creating a branch needs no approval; working directly on a shared/protected branch does.

After the user approves, do not ask again unless the plan must change materially.

**When reality disagrees with the plan** (an API doesn't support what was assumed, a task
turns out twice as big): small deviations — adjust and mention it in the next update.
Material ones (scope, behaviour the user sees, data, a new dependency) — stop, explain what
you found, propose the revised plan, and get approval for the change only.

**Resuming.** If a session is interrupted or picked up later, re-read the plan and the
branch's diff, post which tasks are done, and continue from the first unfinished one —
don't restart from Phase 1.

## Phase 5 — Docs alongside the code (not after)

Update, as part of the same change:

- The project's agent/contributor instructions (`CLAUDE.md`, `AGENTS.md`, rules) when a
  convention, command or gotcha changed.
- `README` / `docs/` / API reference for new behaviour, endpoints, settings, env vars.
- Architecture diagrams when topology or a flow changed (or list it as a follow-up in the
  hand-over — never skip silently).
- A changelog entry if the project keeps one.

A doc or rule the change contradicts is fixed in the same change.

## Phase 6 — Execute in waves (no further approval)

1. **Wave 0 — the contract, inline.** Write what every later task codes against: types,
   schemas, interfaces, shared constants, the migration. Nothing fans out until this exists.
2. **Each next wave — fan out together.** With subagents: launch one per task in one
   message so they run concurrently; each brief names the files it owns (disjoint across the
   wave) and the files it must not touch. Without subagents: do the wave's tasks one by one.
   While agents run, the main session does only non-overlapping work (docs, test plans).
3. **Join.** As each task reports, review its diff and run its checks; post its update. A
   failed task goes back to the same agent with the specifics.
4. **Integrate, then next wave.** Run the cross-task checks (the feature's tests, lint on
   all touched files) once the wave is joined, then start the next.

Each task:

1. **Plan it** — files, order.
2. **Implement** — production quality, matching the surrounding code's naming, structure,
   comment density and idioms. No mock data, no TODO stubs passed off as done, no secrets in
   code or logs, no magic values the project would put in a constant or config.
3. **Test, targeted** — run only the tests the task added or touched, plus existing tests
   covering the changed modules. Never the whole suite per task; that runs once in Phase 7.
   Lint/format/typecheck the files you touched (explicit paths — don't reformat untouched
   files).
4. **Post the update:**

```
✅ Task N/M done — <title>
Changed: <files>
Verified: <commands + result>
Next: <task N+1>
```

A failing check blocks the next wave until fixed. A failure you believe is pre-existing
must be **proven** pre-existing (run it on a clean checkout of the base, e.g. a
`git worktree`) and reported — never just ignored.

### Coordinating subagents (if available)

- **Brief fully.** A subagent sees nothing of this conversation. Give: goal, exact files to
  create/edit and files not to touch, the contract it codes against (signatures, types,
  response shapes), the project conventions that apply, the test command, and the report
  shape you want (files changed, tests run, anything unfinished).
- **Pick the right kind:** read-only explorer for locating code; a general agent for new
  modules/components/tests; a reviewer for the final diff.
- **One writer per file, always.** Research agents are read-only; code agents own disjoint
  files. If two units must touch one file, run them sequentially. Use an isolated worktree
  for a risky or large parallel unit.
- **Hand results across.** When agent B needs what A found, put it in B's brief (or message
  B if it's still running). For long multi-agent work keep one scratch notes file of shared
  decisions and file ownership.
- **Continue, don't restart** — follow-ups go to the same agent so it keeps its context.
- **A subagent's "done" is a claim, not evidence.** Read the diff, rerun the tests yourself.
  Keep risky operations (migrations, deploys, anything touching real data or external
  systems) in the main session.
- **Stay proportionate.** A one-file change is done inline; spawning agents for trivial work
  costs more than it saves.

## Phase 7 — Final verification

Run independent checks concurrently where possible:

- The **full** test suite(s) — first and only full run; this is where regressions elsewhere
  surface.
- Lint, format check, typecheck, build — whatever CI runs.
- Migrations applied cleanly; existing data intact (compare read-only counts before/after).
- The app actually runs and the feature works end-to-end (start it, hit the endpoint, open
  the page, run the CLI) — tests passing is not the same as the feature working.
- A review pass over the full diff (a reviewer subagent if available, else yourself):
  bugs, security, edge cases, leftover debug code.
- `git status` / `git diff --stat` — only intended files changed; no stray scratch files,
  no unrelated formatting churn.

## Phase 8 — Hand over

```
## Done: <feature> (branch <name>, uncommitted)
What changed: <grouped by area>
Verified: <suites, lint, build, live checks — with results>
Known limits / follow-ups: <…>

### Test it manually
1. <page / endpoint / command> → <action> → expect <result>
2. …
Negative cases:
- <bad input / unauthorized / edge case> → expect <error / refusal>
```

If the project keeps session notes or a decisions log, add an entry for decisions and
gotchas worth keeping.

## Never

- **Commit or push** until the user explicitly asks, in that turn. Finishing the workflow is
  not that ask; an earlier approval doesn't carry over to later changes.
- **Lose data** — no dropping/truncating tables, wiping volumes, resetting databases,
  destructive migrations or force-pushes to make something pass. Fix forward, back up
  before risky steps, experiment on a scratch copy. If loss looks unavoidable, stop and ask.
- **Run destructive or outward-facing actions** (deploys, writes to shared/production
  systems, messages to external services) without explicit confirmation.
- **Work directly on a shared/protected branch** (`main`, `master`, `develop`, release
  branches) unless the project says to.
- **Hide** a skipped step or failing check in the hand-over. Report it plainly.
