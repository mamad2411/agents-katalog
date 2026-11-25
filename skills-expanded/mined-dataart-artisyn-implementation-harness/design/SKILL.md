---
name: design
metadata:
  version: 6.0.0
description: >
  Full design lifecycle (/design {ticket}): Context Gathering → Ceremony → Frame
  → Research → Evaluate → Solution → Review Gate → Address Feedback → Publish → Completion, or a
  single stage via /design
  context-gathering|ceremony|frame|research|evaluate|solution|review-gate|address-feedback|publish|complete {ticket}.
  Trigger: "design ND-XX", "run the design for ND-XX".
---

The developer wants to run the design workflow for a ticket. Here is their input:

---

## $ARGUMENTS

---

> ⚠️ Follow every step in order. Do not skip, summarize, or improvise. If you are unsure, ask before deviating.

> 🗂 **Two-track design** — Product (`docs/Harness/`) or Project (`docs/Target Architecture (HLD)/`). Resolved once in Context Gathering Step 3 (`patterns/context-resolution.md`) and recorded in `design/Report.md`'s `## Context` section; every later phase reads it from there.

## How approvals work

A request to run the design lifecycle authorises everything routine: context
inspection, drafting, delegating to `{resolved architect agent}`/`@docs-writer`,
reversible local writes in scope, running non-guarded checks, updating the
report, moving between stages. That authorisation holds for the whole ticket.
Do not ask again per file, per finding, per step, or per phase.

The developer should feel like they are reviewing a senior colleague's work, not
approving every move of a junior one. So:

- **Two stops per phase, both at its end.** The sign-off
  (`patterns/phase-sign-off.md`) and then the commit: proposed, run by the
  developer, checked in Git before the stage closes. Context Gathering has no
  commit of its own; its files ride in Ceremony's first commit after the checkout.
  Review Gate and Address
  Feedback are the exception — their stop waits on a real external fact (the
  actual MR approval state), not an agent decision.
- **Inside a phase, keep going.** Steps use intelligent checkpoints
  (`patterns/approval-intelligent.md`): run the checks yourself, auto-approve
  when the content qualifies, and say in one line what you checked. Escalate
  only on real doubt.
- **Stop mid-phase only for** something only the developer can do or decide: a
  check needing their eyes or access, a guarded command (branch checkout), a
  material scope or tradeoff choice not already settled, accepting a real risk
  (an unresolved OQ marked conditional, a WAF P1 gap accepted rather than
  fixed), or an external mutation (tracker, publishing) not already authorised.
  Present exact targets and prepared content first, combine related questions,
  ask once.
- **Never invent extra gates.** If a stage reference does not name a stop,
  there is no stop.

Commits are always the developer's. Each phase ends by proposing the commit(s)
and waiting for them; the next phase starts on a clean worktree.

## Route

See [references/00-router.md](references/00-router.md) for what each stage
reference produces. Parse `$ARGUMENTS` into an optional leading stage word and the
remaining ticket/free-form input:

- `context-gathering {input}` → apply Stage tasks below for **Context Gathering**
  only, then follow `references/01-context-gathering.md` exactly
- `ceremony {input}` → apply Stage tasks below for **Ceremony** only, then follow
  `references/02-ceremony.md` exactly
- `frame {input}` → apply Stage tasks below for **Frame** only, then follow
  `references/03-frame.md` exactly
- `research {input}` → apply Stage tasks below for **Research** only, then follow
  `references/04-research.md` exactly
- `evaluate {input}` → apply Stage tasks below for **Evaluate** only, then follow
  `references/05-evaluate.md` exactly
- `solution {input}` → apply Stage tasks below for **Solution** only, then follow
  `references/06-solution.md` exactly
- `review-gate {input}` → apply Stage tasks below for **Review Gate** only, then
  follow `references/07-review-gate.md` exactly
- `address-feedback {input}` → apply Stage tasks below for **Address Feedback**
  only, then follow `references/08-address-feedback.md` exactly
- `publish {input}` → apply Stage tasks below for **Publish** only, then follow
  `references/09-publish.md` exactly
- `complete {input}` → apply Stage tasks below for **Completion** only, then
  follow `references/10-completion.md` exactly
- No stage word (bare ticket or free-form input) → run the **full chain**: Resume
  Detection, then Phase 1 through Phase 10 below
- Unrecognized stage word: ask which stage was meant, or whether the full chain was
  intended, before doing anything else

**Compatibility:** `/design-frame`, `/design-research`, `/design-evaluate`,
`/design-solution`, `/design-review-gate`, `/design-review`,
`/design-address-feedback`, `/design-publish` are retired — use
`/design context-gathering|ceremony|frame|research|evaluate|solution|review-gate|address-feedback|publish|complete {ticket}`
instead. `/design-review`'s WAF assessment is now `patterns/waf-review.md`, applied
directly by Solution's Step 7 — there is no longer a standalone command for it.

Ticket-tracker activity is entirely `@scrum-master`'s responsibility. Design only
ever asks it to act on a ticket by state name ("transition to In Progress",
"transition to Done") — the actual transition IDs live in `@scrum-master`'s own
definition, not here. The tracker transition and branch checkout happen in the
dedicated Ceremony stage, after Context Gathering has resolved the ticket's
title/slug.

---

## Resume Detection (run first, every time)

**Step 1 — Locate the design folder**

For trackerless/free-form input, first reuse an existing `DESIGN-YYYYMMDD-XXXX`
folder whose title matches the request. If none exists, generate that stable local
ID (checking for a collision) before globbing and use it for the folder and all
subsequent artifacts.

Glob for `{stories root}*{TICKET}*/**` using a `*{TICKET}*` wildcard (never `[{TICKET}]*` — square brackets are glob metacharacters). The `/**` suffix is required because Glob matches files, not directories. Two-track deployments: the track isn't resolved yet at this point — glob both `docs/Stories/design/*{TICKET}*/**` and `docs/Stories/product-design/*{TICKET}*/**` (and their `approved/`/`declined/` archive subfolders) and take whichever one has a match; a ticket exists under exactly one root. Single-track deployments only have the one fixed root, so there's nothing to disambiguate.

- No files found → fresh start; resolve the local/tracker ID, then create the
  task tracker immediately (apply `patterns/task-tracking.md`, using the unit
  list appropriate to this invocation — ten stages for a full chain, or the
  one stage for a direct single-stage entry) — there is no `Report.md` yet to
  read, so nothing else needs to happen first. Then go to Phase 1.
- Files found → derive folder path from the first matched file, then continue
  to Step 2.

**Step 2 — Read Report.md**

If `design/Report.md` exists, read it. Its phase tracker and machine-readable state
block are the authoritative resume point. Also verify artifacts on disk. For Solution,
use `selected_artifacts` from the state block; an artifact not selected is not evidence
that the phase is incomplete.

| Artifact on disk                                       | Phase done                                                        |
| ------------------------------------------------------ | ----------------------------------------------------------------- |
| `design/Report.md` exists, `## Context` filled in      | Context Gathering ✅                                              |
| Report.md `Branch` row set                             | Ceremony ✅                                                       |
| `design/00 Frame.md`                                   | Frame ✅                                                          |
| `design/01 Research*.md`                               | Research ✅                                                       |
| `design/02 Evaluate*.md`                               | Evaluate ✅                                                       |
| Selected solution artifacts                            | Solution ✅                                                       |
| Report.md Gate — Draft MR set                          | Review 🔄 (pending)                                               |
| Report.md Gate — Approved set (a date)                 | Review ✅ · Address Feedback ✅ (or ⏭️ skipped)                   |
| Report.md Gate — Approved set to `declined`            | Review ✅ · Address Feedback ❌ (declined) · Publish ⏭️ (skipped) |
| `{stories root}{approved\|declined}/*{TICKET}*` folder | Completion ✅ (design lifecycle closed)                           |

**Resuming an existing design:** create (or reuse) the task tracker now,
immediately — before Step 3's confirmation prompt, not after it. Apply
`patterns/task-tracking.md` using the unit list appropriate to this
invocation, and set each stage's initial status from the artifact table just
read above (already-done stages `completed`, the resume point `in_progress`,
the rest `pending`) rather than creating everything as freshly pending.

**Step 3 — Present status and confirm**

> "Found existing design for `{TICKET}`:
>
> `🎯 Context Gathering [status] · 🚀 Ceremony [status] · 📋 Frame [status] · 🔍 Research [status] · 🏗 Evaluate [status] · 📦 Solution [status] · 🔎 Review [status] · 💬 Address Feedback [status] · 📤 Publish [status] · 🏁 Completion [status]`
>
> Resuming from **Phase N — {Name}**. Type **yes** to continue, or name a specific phase and step to jump to (e.g. 'Evaluate, Step 4')."

Wait for confirmation before proceeding. If the developer names a specific phase or phase+step, jump directly to it — do not re-run earlier steps.

On **resume**, the folder found here is `$DESIGN_DIR` — `{stories root}[{TICKET}] {name}/design/` or its `approved/`/`declined/` twin — for every stage and every metrics command from now on; `{stories root}` is whichever root Step 1's glob actually matched (Two-track checked both, so this is already settled). Stages do not search for it again; a direct folder path given as input is used as is. (`solution/` is the sibling directory at the same level as `design/`, not inside `$DESIGN_DIR`.)

On a **fresh start**, no `$DESIGN_DIR` exists yet — there is nothing to find, and no `design/Report.md` to read it from. Context Gathering's Step 3 resolves `{stories root}` first; only then does Step 4 create the folder at that root and `design/Report.md` inside it, fixing `$DESIGN_DIR` for every later stage to read as given.

Tracker creation already happened above — at Step 1 for a fresh start, right
after Step 2's artifact table for a resume — not here; this paragraph only
covers how `$DESIGN_DIR` itself is used by every later stage and metrics
command.

---

## Stage tasks — apply once, every entry (mandatory)

Applied inside Resume Detection — at Step 1 for a fresh start (no existing
design folder), or right after Step 2's artifact table for a resume (so
initial stage statuses reflect what Report.md already shows) — in both cases
before Step 3's confirmation prompt and before any phase work. This step is
not optional background information — it is a required action, on every
full-chain and every direct single-stage entry alike, resumed or fresh. Do
not treat repeated system reminders about native progress-tool availability
as informational only; they are the trigger to act on this step now, not
later.

Apply `.claude/skills/design/patterns/task-tracking.md` — it inspects existing state
itself (the available tracker or `design/Report.md`) and decides create vs. reuse; this router
never re-derives that logic per branch. For the full chain, the unit list is the
ten stages (Context Gathering, Ceremony, Frame, Research, Evaluate, Solution,
Review Gate, Address Feedback, Publish, Completion), chained in that order. For a
direct single-stage invocation, the unit list is just that one stage. Mark a stage
`in_progress` on entry and `completed` only once its phase-tracker banner (below)
shows it done. Research, Evaluate, and Solution track their own child units when
`references/00-decision-router.md`'s loop is active (2+ confirmed decisions) — one
task per decision, the same shape `dev`'s Implement stage uses for plan steps.
Outside that loop, design has no per-step child units to track.

---

## Metrics

Apply `patterns/metrics.md` throughout the lifecycle, including direct-stage entry.
Use `scripts/design-metrics.mjs` with explicit `--dir` pointing to the story's `design/`
directory. Context Gathering initializes `design/stat.json` beside `design/Report.md`;
interrupted sessions run `recover` before new work. Record waits and refresh the
report before each hard stop. Stages own timing; WBS implementation tasks are not
design steps. Review Gate opens the draft MR and parks for approval; Address
Feedback confirms the outcome and records the approval evidence, the rework,
or the skip; Completion finalizes metrics only after required close-out work
succeeds.

---

## Phase tracker

Display this banner at every phase transition:

```
🎯 Context Gathering [status] · 🚀 Ceremony [status] · 📋 Frame [status] · 🔍 Research [status] · 🏗 Evaluate [status] · 📦 Solution [status] · 🔎 Review [status] · 💬 Address Feedback [status] · 📤 Publish [status] · 🏁 Completion [status]
```

Where `[status]` is: `🔄` (active) · `✅` (done) · `⏳` (pending)

---

## Phase 1 — Context Gathering

> Skip if Report.md phase tracker shows Context Gathering ✅.

Follow `references/01-context-gathering.md` exactly — it resolves the ticket,
fetches tracker context, resolves the design context (track/subfolder), and
creates the story folder and Report.md. Ends with a phase sign-off, then
Report; no commit until Ceremony's checkout.

Then emit a progress announcement
(`.claude/skills/design/patterns/announce-progress.md`):
`"📋 Remaining: Ceremony → Frame → Research → Evaluate → Solution → Review → Publish → Completion"`
— then continue straight into Ceremony. Direct-stage entry ends here.

---

## Phase 2 — Ceremony

> Skip if Report.md phase tracker shows Ceremony ✅.

Follow `references/02-ceremony.md` exactly — it handles the ticket's tracker
transition and branch checkout, once the title/slug is known from Context
Gathering. Ends with a phase sign-off (the confirmed branch), then
Report → Commit.

Once commit is confirmed, emit a progress announcement
(`.claude/skills/design/patterns/announce-progress.md`):
`"📋 Remaining: Frame → Research → Evaluate → Solution → Review → Publish → Completion"`
— then continue straight into Frame. Direct-stage entry ends here.

---

## Phase 3 — Frame

> Skip if Report.md phase tracker shows Frame ✅.

Follow `references/03-frame.md` exactly. Ends with a phase sign-off, then
Report → Commit.

Once commit is confirmed, emit a progress announcement
(`.claude/skills/design/patterns/announce-progress.md`):
`"📋 Remaining: Research → Evaluate → Solution → Review → Publish → Completion"` — then
continue straight into Research. Direct-stage entry ends here.

---

## Phase 4 — Research

> Skip if Report.md phase tracker shows Research ✅.

Follow `references/04-research.md` exactly. Ends with a phase sign-off, then
Report → Commit.

Once commit is confirmed, emit a progress announcement
(`.claude/skills/design/patterns/announce-progress.md`):
`"📋 Remaining: Evaluate → Solution → Review → Publish → Completion"` — then continue
straight into Evaluate. Direct-stage entry ends here.

---

## Phase 5 — Evaluate

> Skip if Report.md phase tracker shows Evaluate ✅.

Follow `references/05-evaluate.md` exactly. Ends with a phase sign-off, then
Report → Commit.

Once commit is confirmed, emit a progress announcement
(`.claude/skills/design/patterns/announce-progress.md`):
`"📋 Remaining: Solution → Review → Publish → Completion"` — then continue straight into
Solution. Direct-stage entry ends here.

---

## Phase 6 — Solution

> Skip if Report.md phase tracker shows Solution ✅.

Follow `references/06-solution.md` exactly. Ends with a phase sign-off, then
Report → Commit.

Once commit is confirmed, emit a progress announcement
(`.claude/skills/design/patterns/announce-progress.md`):
`"📋 Remaining: Review → Publish → Completion"` — then continue straight into
opening the Review gate. Direct-stage entry ends here.

---

## Phase 7 — Review

> Skip if Report.md phase tracker shows Review ✅ (or Publish ✅).

Follow `references/07-review-gate.md` exactly — it opens a draft MR, records the gate, and ends the session there. Confirming the outcome is Phase 8's opening concern, not this phase's.

Once the draft MR is open, the session ends. The next invocation is `/design address-feedback {TICKET}`, which continues at Phase 8.

---

## Phase 8 — Address Feedback

> Runs on every post-gate resume, whether or not the approver raised concerns — its Step 1 is what confirms that. Skip if Report.md phase tracker shows Address Feedback ✅, ❌ (declined), or ⏭️ (skipped).

Follow `references/08-address-feedback.md` exactly. Its Step 1 completes Review Gate and confirms the outcome:

- **Approved, no concerns:** Step 1 skips this stage and emits a progress announcement
  (`.claude/skills/design/patterns/announce-progress.md`):
  `"📋 Remaining: Publish → Completion"` — then continue straight into Publish.
- **Declined:** Step 1 skips this stage, Publish, and routes to Completion directly.
- **Concerns raised** → Step 1 starts this stage and continues into its Steps 2–3,
  which identify which phase/step the concern traces to, suggest the named
  reiterate path, apply the fix in that phase, and loop Steps 2–3 (via Step 3's
  own re-check, the same question as Step 1) until an outcome resolves it:
  - **Re-approved** → emit a progress announcement:
    `"📋 Remaining: Publish → Completion"` — then continue straight into Publish.
  - **Declined** → emit a progress announcement: `"📋 Remaining: Completion"` —
    then continue straight into Completion, skipping Phase 9 entirely. There are
    no permanent docs to update for a declined design.

---

## Phase 9 — Publish

> Skip if Report.md phase tracker shows Publish ✅ or ⏭️ (skipped — design was declined).

Follow `references/09-publish.md` exactly — doc impact identification, doc
updates, `{resolved architect agent}` review, then a phase sign-off, Report →
Commit.

Once commit is confirmed, emit a progress announcement
(`.claude/skills/design/patterns/announce-progress.md`):
`"📋 Remaining: Completion"` — then continue straight into Completion.
Direct-stage entry ends here.

---

## Phase 10 — Completion

> Skip if Report.md phase tracker shows Completion ✅.

Follow `references/10-completion.md` exactly — publish implementation
tickets, archive, tracker sync, then a phase sign-off, Report, and the final
commit + PR handover. This is the final phase; the design lifecycle is closed
once it completes.
