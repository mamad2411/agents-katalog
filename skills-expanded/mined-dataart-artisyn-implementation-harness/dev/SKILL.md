---
name: dev
metadata:
  version: 3.1.0
description: >
  Full dev lifecycle (/dev {ticket}): Context Gathering → Ceremony → Plan → Implement
  → Test → Document → Completion, or a single stage via
  /dev context|ceremony|plan|implement|test|document|complete {ticket}.
  Trigger: "build ND-XX", "implement ND-XX", "finish ND-XX", or starting a ticket from scratch.
---

The developer wants to run the dev lifecycle for a ticket. Here is their input:

---

## $ARGUMENTS

---

## How approvals work

A request to run the dev lifecycle authorises everything routine: reading context,
planning, reversible local edits in scope, running non-guarded checks, updating the
report, moving between stages. That authorisation holds for the whole ticket. Do not
ask again per file, per finding, per step or per phase.

The developer should feel like they are reviewing a senior colleague's work, not
approving every move of a junior one. So:

- **Two stops per phase, both at its end.** The sign-off (`patterns/phase-sign-off.md`):
  Context on the written intent, Ceremony on the branch, Plan, Implement, Test and
  Document on their results. Then the commit: proposed, run by the developer, checked
  in Git before the stage closes. Context is the exception: it has no commit of its
  own, its files ride in Ceremony's first commit after the checkout. Completion ends
  with one combined ask for external actions.
- **Inside a phase, keep going.** Steps use intelligent checkpoints
  (`patterns/approval-intelligent.md`): run the checks yourself, auto-approve when
  the content qualifies, and say in one line what you checked. Escalate only on
  real doubt.
- **Stop mid-phase only for** something only the developer can do or decide: a
  check needing their eyes or their access, a guarded command, a material scope or
  architecture choice, accepting a real risk, or an external mutation (tracker,
  publish, deploy). Prepare the content first, combine related questions, ask once.
- **Never invent extra gates.** If a stage reference does not name a stop, there is
  no stop.

Commits are always the developer's. Each phase ends by proposing the commit(s) and
waiting for them; the next phase starts on a clean worktree.

## Route

See [references/00-router.md](references/00-router.md) for what each stage
produces. Parse `$ARGUMENTS` into an optional leading stage word and the
rest:

- `context {input}` → Stage tasks for **Context Gathering** only, then `references/01-context-gathering.md`
- `ceremony {input}` → Stage tasks for **Ceremony** only, then `references/02-ceremony.md`
- `plan {input}` → Stage tasks for **Plan** only, then `references/03-plan.md`
- `implement {input}` → Stage tasks for **Implement** only, then `references/04-implement.md`
- `test {input}` → Stage tasks for **Test** only, then `references/05-test.md`
- `document {input}` → Stage tasks for **Document** only, then `references/06-document.md`
- `complete {input}` → Stage tasks for **Completion** only, then `references/07-completion.md`.
  Use this for any story that reached Document but was never archived.
- No stage word (bare ticket or free-form) → run the **full chain**: Entry check,
  then Phase 1 through Phase 7 below
- Unrecognised stage word → ask which stage was meant, or whether the full chain
  was intended, before doing anything else

**Compatibility:** `/dev-plan`, `/dev-implement`, `/dev-test`, `/dev-document` are
retired — use `/dev context|ceremony|plan|implement|test|document|complete {ticket}`.

Ticket-tracker activity is entirely `@scrum-master`'s job. Dev only asks it to act
on a ticket by state name ("transition to In Progress", "transition to Done"); the
transition IDs live in `@scrum-master`'s own definition, so the two never drift.

---

## Entry check — every entry, full-chain or direct stage

This is the one place that decides fresh vs. resume. Stage references do not repeat it.

Parse the ticket number from `$ARGUMENTS` (`ND-\d+`). For free-form
input with no ticket, search existing story folders for a matching local ID
(`DEV-YYYYMMDD-XXXX`) and title; reuse it when found, otherwise generate a
collision-checked one. A local ID does not imply a tracker record.

Then look for existing work:

- Glob `docs/Stories/*{TICKET}*/impl/2-report.md` (use `*{TICKET}*` wildcard — never
  `[{TICKET}]*`); include `docs/Stories/archive/`
- If it exists, read the `Status` and `Phase` rows, and check which stage artifacts
  exist (`0-intent.md`, `1-plan.md`, archive location)

Decide:

- **No report** → fresh. Full chain starts at Phase 1; a direct stage word starts at
  that stage (and Plan will write the missing intent first, see its Step 1).
- **Status `✅ Complete`** → say so and stop. The ticket is finished.
- **Report exists** → one question, same words everywhere:

  > "I found existing work for `{TICKET}`: `{phase-row}`. {Artifacts found, one line.}
  >
  > **resume** where it left off, or **restart** {this stage / from scratch}?"

  **Stop and wait.**
  - **resume** — full chain: jump to the first stage not ✅ (e.g. `🔨 Implement 🔄`
    → Phase 4; `📝 Document ✅ · 🏁 Completion ⏳` → Phase 7). Direct stage: enter it
    and build on what is there; do not redo completed steps or re-ask given sign-offs.
  - **restart** — full chain: from Phase 1. Direct stage: that stage from its first
    step, overwriting its own artifact only (`0-intent.md` for Context, `1-plan.md`
    for Plan); earlier stages' artifacts stay.

The story folder found here is `$IMPL_DIR` (`docs/Stories/[{TICKET}] {name}/impl/`,
or its `archive/` twin) for every stage and every metrics command from now on. Stages
do not search for it again; a direct folder path given as input is used as is.

Run metrics `recover --dir "$IMPL_DIR"` when a `stat.json` exists, before recording
anything. Then apply **Stage tasks** below and go to the target phase.

---

## Stage tasks — apply once, every entry (mandatory)

Do this on every entry, full-chain or single-stage, resumed or fresh. A system
reminder about native progress tools is the cue to do it now.

Apply `.claude/skills/dev/patterns/task-tracking.md`. It inspects existing
state (the native tracker or `2-report.md`) and decides create vs. reuse vs.
reconcile; this router does not. For the full chain the unit list is the seven stages
(Context Gathering, Ceremony, Plan, Implement, Test, Document, Completion) in order.
For a direct single-stage call it is that one stage. Mark a stage `in_progress` on
entry and `completed` only when the phase banner shows it done. A stage reference
tracks its own child units (plan steps, in Implement's case).

---

## Metrics

Apply `patterns/metrics.md` throughout. Each ticket has `impl/stat.json` beside
`2-report.md`. Use `scripts/timing.mjs` with an explicit `--dir` for every metric
change; never edit the JSON by hand. Each stage reference says where its `stage
start`, `wait start`, `resume` and `stage complete` calls go; the phase sign-off
pattern owns the sequence around every stop. The entry check runs `recover` on resume.
Keep unknown measurements explicit.

---

## Phase tracker

Show this banner at every phase transition, with the active phase marked:

```
🎯 Context [status] · 🚀 Ceremony [status] · 📋 Plan [status] · 🔨 Implement [status] · 🧪 Test [status] · 📝 Document [status] · 🏁 Completion [status]
```

`[status]` is `🔄` (active) · `✅` (done) · `⏳` (pending). Example when entering Plan:

```
🎯 Context ✅ · 🚀 Ceremony ✅ · 📋 Plan 🔄 · 🔨 Implement ⏳ · 🧪 Test ⏳ · 📝 Document ⏳ · 🏁 Completion ⏳
```

---

## Phase 1 — Context Gathering

Follow `references/01-context-gathering.md`. Ends with a phase sign-off on the
intent. Announce the outcome and continue; direct-stage entry ends here.

## Phase 2 — Ceremony

Follow `references/02-ceremony.md`. Ends with a phase sign-off on the branch.
Announce the outcome and continue; direct-stage entry ends here.

## Phase 3 — Plan

Follow `references/03-plan.md`. Ends with a phase sign-off. Announce the outcome
and continue; direct-stage entry ends here.

## Phase 4 — Implement

Follow `references/04-implement.md`. Ends with a phase sign-off. Announce the
outcome and continue; direct-stage entry ends here.

## Phase 5 — Test

Follow `references/05-test.md`. Ends with a phase sign-off. Announce the outcome
and continue; direct-stage entry ends here.

## Phase 6 — Document

Follow `references/06-document.md`. Ends with a phase sign-off. Announce the
outcome and continue; direct-stage entry ends here.

## Phase 7 — Completion

Follow `references/07-completion.md`. It archives the story, finalises metrics,
hands over the commit and PR text, offers the tracker and tech-debt actions once,
and ends with a clear "this ticket is complete" message. There is nothing after it.
