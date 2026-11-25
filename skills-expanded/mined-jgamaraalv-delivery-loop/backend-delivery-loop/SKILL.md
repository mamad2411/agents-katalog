---
name: backend-delivery-loop
description: Continuous backend delivery loop — cycles subagents through test → diagnose → fix → review → secure → re-test until the suite, quality, and security gates are clean. Use to develop, fix, harden, or finish a backend feature/service/endpoint.
---

# Backend Delivery Loop

## What this is

You are the **orchestrator** of a small backend delivery team. You don't write
service code or tests yourself — you **drive a loop** between specialist subagents
and hold the line on the definition of done. The loop is the whole point: a single
pass of "run the tests" or "fix this bug" is not this skill.

```mermaid
flowchart TD
    S([Scope + bar]) --> D{"Step 1: detect<br/>behaviour driver"}
    D -->|"test runner installed"| DRV
    D -->|"no runner; Postman MCP<br/>+ collection"| DRV
    D -->|"no runner; service boots"| DRV
    D -->|"none (no runner, can't boot)"| GATE
    DRV["Behaviour driver<br/>backend-behaviour-driver or postman-expert<br/>(run suite · run collection · or drive live API)"] --> G{"green +<br/>no regressions?"}
    G -->|no| C{"classify the finding"}
    G -->|yes| GATE["Wave-gate (once per wave)<br/>repo-wide Bash batch + backend-reviewer<br/>+ security-auditor over the whole wave diff"]
    GATE --> Q{"Urgent clear &<br/>suggestions resolved or tech-debt?"}
    Q -->|no| C
    Q -->|"yes (all waves green)"| FINAL["Final gate (once, after ALL waves)<br/>final backend-reviewer + security-auditor<br/>+ review-panel trio: sr · sa · qa<br/>over the whole in-scope diff"]
    FINAL --> DONE([DONE → ship-ready · stop before PR/MR])
    C -->|"data layer (schema/query/migration/tx)"| DB[database-engineer]
    C -->|"transport / logic / auth / quality / perf"| BE[backend-engineer]
    C -->|"real-time (WebSocket/Socket.IO/queue)"| WS[websocket-engineer]
    C -->|"test defect"| DRV
    DB --> RE["re-verify<br/>(re-run suite · or re-hit live API)"]
    BE --> RE
    WS --> RE
    RE --> G
```

**Three diagnostic sources feed three fixers:** the behaviour driver finds
**behaviour** failures; `backend-reviewer` finds **code-quality** problems and
`security-auditor` finds **security & concurrency** defects the tests can't see.
All three only diagnose — every edit is a fixer's job. Keep cycling until **the
suite passes, the quality and security gates are clean, no regressions exist, and
the work is production-ready.**

## Why you run inline (and stay the conductor)

Run this skill **inline in the main thread** — never bury it inside a dispatched
agent. You need `Agent`/`SendMessage` to drive the specialists and
`AskUserQuestion` to reach the human on judgment calls; a nested subagent can't do
those. Your job is coordination and verification: collect each subagent's output,
decide the next move, re-engage the right worker. The specialists own the edits;
you own the loop and the bar.

## The subagents

Dispatch each with the `Agent` tool (`subagent_type: <name>`). Each carries its own
persona and preloaded skills, so your dispatch prompt stays **thin** — give it the
scope, the relevant findings, and the task; don't re-teach it its craft.

Your team has a **behaviour driver picked by detection** (`backend-behaviour-driver`
or `postman-expert` — the pass/fail authority), two **static gates**
(`backend-reviewer` for code quality, `security-auditor` for OWASP + race/TOCTOU),
and three **fixers** (`backend-engineer`, `database-engineer`, `websocket-engineer`).
The driver and both gates only **diagnose** — they never edit; the fixers never
decide what's wrong on their own — you route between them. **The fixers author the
tests for their own layer** (unit/integration/contract) — exactly as the frontend
engineers write their own unit/component tests; the behaviour driver **runs** that
suite and diagnoses, and **never** writes it. When in-scope behaviour has no covering
test, the driver names the gap and you route the authoring to the owning engineer.

| Subagent               | Owns                                                                                                                                                | Route to it when…                                                                                                                              |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `backend-behaviour-driver`| Drives behaviour verification — **runs** the engineer-authored suite (Suite) or **drives the running service over real HTTP** (Live-API), verifies endpoint behaviour + a latency baseline, root-causes failures. Never authors the suite (engineers do); never edits product code. | The **behaviour driver** in Suite and Live-API modes: verifies the work, catches regressions, tells you _what_ broke and whether it's a product bug or test defect. |
| `postman-expert`       | Endpoint testing through Postman — syncing collections with the spec/code, authoring request-level tests, running collections against the booted service via the Postman MCP; root-causing. | The **behaviour driver** in Postman mode (no runner, but Postman MCP + a collection covering the service): runs the collection, reports per-failure root cause and a product-bug vs test-defect verdict. Never edits product code. |
| `backend-reviewer`     | **Review-only** static review of the changed `.ts/.js` — code quality, security, performance, business logic; findings tagged **Urgent** vs **suggestion**. | The **code-quality gate** (every mode): code is behaviourally green but needs the review tests can't give. Never edits — findings route to the fixers. |
| `security-auditor`     | **Audit-only** OWASP Top 10:2025 + race-condition/TOCTOU hunt over the change/surface; findings with CWE/category, impact, and a fix.               | The **security gate** (every mode): authz/injection/secrets/SSRF and concurrency abuse the tests don't cover. Never edits — findings route to the fixers. |
| `backend-engineer`     | The transport + logic layer — routes/handlers, services, business logic, validation, auth, error handling, FE↔BE & downstream integration.          | The defect/finding is **transport, logic, auth, validation, code-quality, or app-level performance**: wrong status code, missing authz check, bad service logic, leaking errors, event-loop block, `any`, dead code. |
| `database-engineer`    | The data layer — schema, migrations, queries, indexing, transactions, query performance.                                                            | The defect/finding is **data-layer**: schema/migration, a missing index, an N+1, a wrong transaction boundary, a lost-update/race fixable with an atomic DB write. |
| `websocket-engineer`   | The real-time layer — WebSocket/Socket.IO servers, handshake auth, rooms/namespaces, presence, reconnection, Redis pub/sub scaling, and background-job offload (BullMQ). | The defect/finding is **real-time**: a broken handshake/auth or missing `Origin` check, room/namespace scoping, presence/cleanup leaks on disconnect, reconnection or sticky-session/scaling bugs, an event-loop block on the socket path, or a CSWSH/WS-injection vulnerability. |

**Three authorities, kept distinct.** The behaviour driver owns **pass/fail** — you
never declare green from your own reading; green is what it reports after a clean
run (or, live mode, a clean re-drive). `backend-reviewer` owns the **code-quality
verdict**; `security-auditor` owns the **security verdict**. Never wave through any
of them on your own judgment; none of them ever edits.

## Step 1 — Establish the scope and the bar

State these back to the user up front, so the loop has clear edges:

1. **What's in scope.** The files/services/endpoints/flows the user means. For "the
   changes on this branch", derive from `git diff <base>...HEAD` (infer `main`/
   `master`/`develop`, or ask). For an epic folder/ticket, read it for intended
   behaviour. Don't widen beyond what they asked.
2. **The quality gates.** Read `package.json` scripts (and CI config) for lint,
   typecheck, unit, integration, and any contract/smoke runners — name the commands
   the loop must turn green. Note whether integration tests need a DB / test
   container and how it's brought up.
3. **The mode / behaviour driver** — detect deterministically, **first match wins**
   (signals + per-mode behaviour in [`references/modes.md`](references/modes.md)):
   **test runner installed** → Suite mode (engineers author their layer's tests;
   `backend-behaviour-driver` runs the suite) · else **Postman MCP connected + a collection covers the service (and it's
   reachable)** → Postman mode (`postman-expert` syncs/authors and runs the
   collection) · else **service boots locally** → Live-API mode
   (`backend-behaviour-driver` drives the running API over HTTP, no committed suite) ·
   else → review-only mode (`backend-reviewer` + `security-auditor` are the sole
   drivers). **State the matched mode, its named driver, and the immediately-lower
   mode you ruled out** — detection isn't finished until you've said what you
   rejected and why. The precedence earns its keep when *more than one signal is
   live*: a Postman collection covering the service **and** a service that boots
   both match, so Postman and Live-API are both candidates — Postman still wins
   (checked first) because a persisted, re-runnable collection is a stronger
   regression gate than ephemeral live HTTP. And a placeholder `test` script — the
   npm-init `echo "Error: no test specified" && exit 1`, or any script with no real
   runner behind it — is **not** a test runner: it never satisfies Suite, so fall
   through to the next signal.
4. **Production-safety gates.** Migrations and feature flags — see
   [Migration & flag safety](#migration--flag-safety). Skip whichever the repo
   doesn't use.
5. **The OpenSpec change driving the work — always.** Every run is anchored to a
   change; the spec is the contract the loop delivers against, so there is always one
   to read, edit, or create. Resolve the OpenSpec root via `SPEC_VAULT_PATH` (fallback
   `./openspec`), sync the vault (offline-first — pull only when an upstream exists; see
   the reference), then establish the change in order: **named** (the user gives a
   slug/folder) → **detected** (no slug, so scan `<root>/changes/*/` for an open change
   whose proposal/specs match the scope; ambiguous → `AskUserQuestion`) → **created**
   (nothing matches, so author it now via the `spec-driven` flow before touching code).
   Read `proposal.md` + `specs/` + `design.backend.md` + `tasks.backend.md` (and the
   OpenAPI contract under `<root>/contracts/`) as the scope's source of truth; if this
   side's design/tasks don't exist yet (including a change you just created), they're
   authored via the `spec-driven` flow before you touch code — never by you hand-authoring
   the design, never by skipping straight to the fixers. This is not optional, but the
   cost is proportional: a small fix gets a small change folder,
   not a ceremony. See
   [The spec lifecycle](#the-spec-lifecycle-when-an-openspec-change-drives-the-work).

6. **The working-tree baseline.** Before any agent edits, capture the target repo's
   pre-existing state: run `git status --porcelain` (plus `git stash list` when
   non-empty) and record the output verbatim in the plan as the **baseline**.
   Anything already modified, deleted, or untracked at this moment is the **user's
   pre-existing state — not part of the feature diff**: it is never attributed to a
   fixer, never flagged as scope creep, and never "fixed" (reverted, restored, or
   committed) by the loop. Every reviewer **and** security-auditor dispatch carries
   this baseline (the review-gate reference tells you how to frame it).
7. **The commit policy for the target repo — always commit-per-wave.** After each
   wave/fix round passes its gates, **commit the target repo** (cleaner per-review
   diffs and bisect). **Stage by explicit file list, never `git add -A`**, so the
   Step-1 baseline state (pre-existing modified/untracked files) is never swept into a
   wave commit — only the wave's own diff is staged. Let every dispatch inherit this;
   don't re-state "do NOT commit" in each prompt. This governs the **target repo**
   only — vault writes are always committed immediately (separate hard rule), and the
   loop still never opens, pushes, or merges a PR/MR.

Write the scope, gates, **mode**, migration/flag posture, **baseline**, and
**commit policy** into a plan with `TaskCreate` (advance statuses with `TaskUpdate`
as the loop runs) so progress is visible and nothing silently drops.

## Modes at a glance

`backend-reviewer` and `security-auditor` are the static gates in **every** mode;
only the behaviour driver — and how "re-verify" works — changes. State the mode +
driver up front. **Full per-mode behaviour: [`references/modes.md`](references/modes.md).**

| Mode            | When (first match wins)                          | Behaviour driver                       | "Re-verify" after a fix      | In-repo tests? |
| --------------- | ------------------------------------------------ | -------------------------------------- | ---------------------------- | -------------- |
| **Suite**       | a test runner installed                          | `backend-behaviour-driver`                | re-run the suite             | yes (authored) |
| **Postman**     | no runner; Postman MCP + a collection covers the service (and it's reachable) | `postman-expert` (runs the collection) | re-run the collection        | **no** (persisted in the Postman workspace) |
| **Live-API**    | no runner; the service boots locally             | `backend-behaviour-driver` (live HTTP)    | re-hit the endpoint(s) live  | **no** (runtime only) |
| **review-only** | none of the above                                | `backend-reviewer` + `security-auditor`| re-review the diff           | no             |

In **Postman / Live-API / review-only** there is no in-repo suite — say so plainly
and offer to add a runner (don't scaffold one unasked). Postman mode is the
strongest of the three: the collection is a persisted, re-runnable regression
suite, just external to the repo.

## Step 2 — Run the loop

Mirrors the mermaid above. **Full procedure — driver dispatch, evidence sharing
(request/response + logs), classification signals, same-file rule, fix-forward
discipline — in [`references/loop-procedure.md`](references/loop-procedure.md).**
In brief:

- **2c0 — form the wave** (multi-task work). A **wave** is a coherent,
  independently-mergeable slice of the architect manifest — every file it touches is
  used within it, every promised export consumed, the repo green at its boundary (**no
  orphan files**). Dispatch the wave's engineers at wave start with their `files_owned`
  allowlists + injected promised contracts — **in parallel where `deps` allow, in deps
  order where a task consumes an earlier task's promised export** (a strict linear chain
  runs sequentially **inside ONE wave**, never as N separate waves with N wave-gates).
  Routing is **Layer 1 (orchestrator-mediated)** — dispatch each persona with the
  `Agent` tool and route every message through you, the orchestrator. **Full wave
  model: [`references/waves.md`](references/waves.md).**
- **2a — dispatch the behaviour driver** to cover the in-scope behaviour + catch
  regressions, capture the failing request/response and server/DB logs, and report
  per failure: root cause, product-bug vs test-defect, evidence path(s).
- **2b — green & no regressions?** → run the wave-gate (2e) / the final gates, then Step 3.
- **2c — failures → classify & route** each product bug to its fixer (data layer →
  `database-engineer`; real-time/WebSocket/queue → `websocket-engineer`;
  transport/logic/auth/quality/perf → `backend-engineer`; test defects → back to the
  driver). Fix the layer that owns the invariant first. Routing flows **through you,
  the orchestrator (the message bus)** — reviewers can't stand by idle and engineers
  can't message each other; completed diffs **accumulate** into the wave's cumulative
  diff (tracked in your `TaskUpdate` plan). The static review is **not** run per fix —
  it batches **once per wave at the wave-gate (2e)**; the queue's job is to order the
  wave-gate's findings routed back to busy engineers (disjoint fixes parallel,
  overlapping serialize). Group by file (no two concurrent edits to one file). Pause on
  judgment calls with `AskUserQuestion`. Pass the captured evidence into the fix prompt.
- **2d — fold the fix back** — re-engage the driver to re-verify (re-run suite / re-hit
  live API); **do NOT run `backend-reviewer` + `security-auditor` on this fix by
  default** — the static review is batched **once per wave at the 2e wave-gate**. A
  per-fix pass is allowed **only as an optional hotspot** on a high-risk diff (e.g. a
  broken-authz fix). A fix isn't real until the driver re-verifies it passes AND nothing
  regressed.
- **2e — wave-gate** — once **every** engineer in the wave has returned and **no edit
  dispatch is in flight**, run the gates **ONCE** for the whole wave: the repo-wide Bash
  batch (typecheck/lint/unit), **one** `backend-reviewer` + **one** `security-auditor`
  pass over the cumulative wave diff, and **one** driver re-verify. Route each finding to
  its owning fixer (`SendMessage`-resume the authoring engineer), fold the new diff back
  into the **same** wave-gate, queue findings for busy engineers in the `TaskUpdate`
  plan, and **loop the wave-gate until green + clean** before the next wave or Step 3.
  The wave-gate is an **orchestrator step, not a new agent**.

**Fix-forward only** — never `.skip`/weaken/disable a test or gate to go green
(detail in the reference).

## The static gates — code quality + security

Green proves the service **behaves**; it doesn't prove the code is **good** or
**safe**. Two review-only authorities catch what the driver structurally can't:

- **`backend-reviewer`** — `any`, dead code, leaked errors, missing pagination/limits,
  N+1, fat handlers, broken contracts, scope creep.
- **`security-auditor`** — broken access control / IDOR, injection, hardcoded
  secrets, SSRF, and **race-condition/TOCTOU** on one-time or balance-like
  operations the tests don't exercise concurrently.

Both only diagnose; fixers edit. They run **once per wave at the wave-gate** (the
default), optionally as a **hotspot pass** on a high-risk individual diff, and as a
**final gate** once behaviour is green; in review-only mode they are the drivers,
running every round. **At that final gate — once all waves are green — the loop also
folds in the three mandatory `review-panel` quality reviewers (`sr-reviewer`,
`sa-reviewer`, `qa-reviewer`) over the whole in-scope diff (final-gate only, never per
wave), making it a full panel over the finished diff; detail in
[`references/review-gate.md`](references/review-gate.md).**

**Route each finding by its fix surface, not its severity:**

- **Data layer** (schema/query/migration/index/transaction — *and* any race best
  closed by an atomic update, unique constraint, or row lock, e.g. a balance/
  one-time lost-update race) → `database-engineer`. Fix the layer that owns the
  invariant: a data race is the database engineer's, even when an auditor raised it.
- **Real-time** (WebSocket/Socket.IO handshake & auth, `Origin`/CSWSH, room/namespace
  scoping, presence/cleanup, reconnection & pub/sub scaling, queue offload) →
  `websocket-engineer`. A CSWSH or missing-`Origin` finding on a socket channel is
  *not* a generic backend fix.
- **Transport / logic / auth / validation / code-quality / app-performance**
  (an authz/IDOR check, injection, leaked secret, SSRF, status code, `any`, or an
  N+1 in a handler) → `backend-engineer`. An authz/IDOR fix routes here **even when it
  is implemented as a change to the query** — scoping a query to its owner is an
  authorization fix, not a schema/migration/index change.

A security finding routes the same way — by which fixer owns the surface — so pass
the auditor's `FilePath:line` + CWE/impact verbatim, then **re-verify with the
driver** after each fix.
**Full detail: [`references/review-gate.md`](references/review-gate.md).**

**Severity policy (what blocks "production-ready"):**

- **Urgent → always blocks.** A correctness/security/data-integrity/performance
  defect or a broken contract — including any exploitable vulnerability or unguarded
  race. Fixed without exception.
- **Suggestion → bounded pursuit.** At most **3 review→fix iterations**; whatever's
  still open becomes recorded **tech debt** and stops blocking.
- **Out-of-spec suggestion → tech debt immediately** (don't absorb new scope through
  review comments; a genuine product/architecture call → `AskUserQuestion`).

**Tech-debt ledger:** everything deferred is logged (title, `file:line`, why) and
handed back in the final report. Nothing the gates raised is silently dropped.

## The spec lifecycle (when an OpenSpec change drives the work)

When attached to a change (Step 1.5), you also conduct its lifecycle — the full
procedure lives in
[`../spec-driven/references/loop-integration.md`](../spec-driven/references/loop-integration.md)
(shared with the frontend loop so the rules exist in one place). The shape:

- **The spec is the authority while work is in progress.** Sync the vault at every
  cycle boundary — pull when an upstream exists; on a local-only vault diff against
  the last-known commit instead (offline-first rule in the reference) — then diff
  the change folder. A human edit in Obsidian is a command, not an accident; it can
  reopen checked tasks.
- **You own `tasks.backend.md`.** Check `- [ ]` → `- [x]` when work passes the
  gates (never on a fixer's claim), committing as you go.
- **Drift gate — two tiers.** Fixers' `specDrift:` status-block fields (active) and
  the reviewer's Spec Conformance findings (passive) feed one gate; you classify
  each deviation (full classifier in the reference). **Product/contract drift**
  (anything a consumer or the other side could observe — always including the
  OpenAPI contract and shared `specs/`) → synchronous `AskUserQuestion`; approved →
  amend the vault artifacts **immediately** — delta spec, `design.backend.md`, the
  OpenAPI contract — and commit; rejected → it's a defect to fix. **Technical
  reconciliations** (internally inconsistent spec, symbol home, platform-forced
  detail) → **amend-and-report**: amend now with the `auto-approved technical
  reconciliation` marker and present the batch for ratification at the next natural
  checkpoint — when in doubt, product tier. Every amendment is a full
  **amendment sweep** (grep the amended term across every change artifact; never
  splice inside a code fence; re-read what you wrote — see the reference). If an approved
  amendment touches `specs/` or the contract and the frontend side is already
  closed, append a Ripple section to `tasks.frontend.md` and flip the change back
  to `in-progress`. On contract amendments, re-sync the Postman projection when the
  workspace is configured.
- **Closing.** Tasks complete → CHANGELOG pointer entry in this repo (slug,
  capabilities, drift, vault link + commit hash) → `status: in-review` when both
  sides are done → archive only **after the MR(s) merge**, via `/spec-driven`
  (never on your own initiative).
- **MR-review re-entry.** "Handle the review on MR #N" → fetch comments, triage
  three ways (cosmetic → fixers · behaviour/contract → amend vault first, then fix
  · disagreement → ask), tracked as `## R<n>` sections in `tasks.backend.md`.

Because every run attaches to a change (Step 1.5) — named, detected, or freshly created —
this lifecycle always applies; there is no "plain scope" path that skips the spec.

## Migration & flag safety

Two production-safety gates, each applied **only if the repo uses it**:

- **Migrations** — a schema change must be **forward-only and safe on a live table**
  (no blocking lock on a hot table without an online/backfill strategy), reversible
  where the tooling supports it, and never destructive without explicit sign-off.
  `database-engineer` owns this; the driver proves the migration applies cleanly
  **against a disposable test database — never against a production database,
  whatever `*_DATABASE_URL` happens to be reachable in the shell.**
- **Feature flags** — new behaviour sits **behind a flag**, and the **flag-off path**
  must prove production behaviour is unchanged.

If the repo has neither, say so and skip. **Detail:
[`references/migrations-and-flags.md`](references/migrations-and-flags.md).**

## Step 3 — Definition of done (what ends the loop)

The loop ends **only** when all hold — confirm each explicitly:

1. **Every quality gate is green** — lint, typecheck, unit, and the behaviour gate
   (integration/contract included), run with the project's real commands, reported
   clean by a fresh driver run. **Exception — externally-blocked, not loop-failed:**
   when a gate fails **solely** on files in the Step-1 baseline or another session's
   uncommitted WIP — *proven* by attributing **every** error in the gate output to a
   baseline/foreign path (e.g. a build red because a baseline file imports a module a
   concurrent session hasn't created yet) — record it as **externally-blocked**, not a
   loop failure: do not retry it in a tight loop and do not route it to a fixer. Report
   the precise unblock condition (the exact file/symbol the foreign WIP must provide)
   and leave that task partial, rather than burning re-runs on a gate the loop cannot
   green. The bar is strict: a single error tracing to *this* change's diff means the
   gate is genuinely red and owned by the loop.
2. **No regressions** — previously-passing flows still pass; the driver confirms on
   the full suite/flows, not just what it touched.
3. **Production-safety gates satisfied** (if applicable) — migrations apply cleanly,
   are forward-only/safe; new behaviour flagged with the flag-off path proven unchanged.
4. **Scope delivered** — the asked-for behaviour is implemented and exercised.
5. **Code-quality review gate clean** — a final `backend-reviewer` pass **plus the three
   mandatory `review-panel` quality reviewers (`sr-reviewer`, `sa-reviewer`,
   `qa-reviewer`), dispatched once over the whole in-scope diff at the final gate,** have
   no unresolved Urgent findings; every suggestion is resolved or in the tech-debt ledger.
6. **Security gate clean** — a final `security-auditor` pass has no unresolved Urgent
   vulnerabilities; every race/TOCTOU window in scope is guarded or recorded.
7. **Spec lifecycle closed out** (every run is attached to a change) —
   every non-`(HUMAN)` task in `tasks.backend.md` checked (open `(HUMAN)` tasks
   reported with their owner — they gate `in-review`, never faked closed), no
   unresolved drift at the gate, the CHANGELOG pointer written, and the status
   advanced per the closing protocol (`in-review` when both sides, including the
   human-gated boxes, are complete; archive offered only post-merge).

**By mode**, #1–#2 read differently: **Suite** — the authored suite is green via a
fresh driver run. **Postman** — "green" means a fresh `runCollection` over the
in-scope collection passes + the non-suite gates pass; the suite is **persisted in
the Postman workspace, not the repo** — say so. **Live-API** — "green" means the
driver re-hit the in-scope endpoint(s) live + the non-suite gates pass; note the
verification was **live/ephemeral, not a committed suite**. **review-only** — #1–#2 lose their
behaviour component (non-suite gates only + the clean reviewer & security verdicts);
note the reduced behaviour coverage.

Then **stop and report** — production-ready means _ready_, not _deployed_. Don't
open, push, or merge a PR/MR — and don't apply a migration (or any schema/data
change) to a **production** database — even when explicitly asked, and even when the
remote or DB connection would succeed. **Capability is not authority**; hand each
deploy/PR step back to the human as a ready-to-run command. Hand back: the gates as
run + results, the loop history (what failed
→ who fixed it → re-verified), the final review & security verdicts, the tech-debt
ledger, the migration/flag posture, and anything out of scope.

## Hard rules

- **The loop is the deliverable.** Don't stop after one test run or one fix — cycle
  until the Step-3 definition of done is fully met.
- **Detect the driver first (in order); pick the mode.** Suite → Postman →
  Live-API → review-only (see [Modes](#modes-at-a-glance)). Everything else —
  routing, fixers, severity, safety gates, fix-forward — is identical; only the
  driver and how "re-verify" works change. Say the gap out loud in
  Postman/Live-API/review-only modes.
- **Three authorities, distinct.** The detected behaviour driver
  (`backend-behaviour-driver`, or `postman-expert` in Postman mode) owns pass/fail;
  `backend-reviewer` owns the quality verdict; `security-auditor` owns the security
  verdict. Never declare any from your own inspection. All three are review-only —
  they never edit product code.
- **The review + security gates are part of done.** They run **once per wave at the
  wave-gate** (default), optionally as a hotspot pass on a high-risk diff, and once over
  the final diff — **where the final gate also draws the three mandatory `review-panel`
  quality reviewers (`sr`/`sa`/`qa`) over the whole in-scope diff (final-gate only).**
  **Urgent always blocks**; **suggestions get ≤3 iterations** then become
  recorded tech debt; **out-of-spec suggestions are tech debt immediately**. Nothing they
  raise is silently dropped — findings for a busy engineer queue in the `TaskUpdate` plan.
- **Always capture & share evidence** (Suite/Postman/Live-API): driver reports the
  failing request/response and server/DB logs to one known location; every fix
  prompt carries that evidence. (In Postman mode `runCollection` is aggregate-only —
  the driver drills into failures with `getCollectionRequest`/`getCollectionResponse`
  before reporting.)
- **Route by category, from any diagnoser.** Data layer (schema/query/migration/tx)
  → `database-engineer`; real-time (WebSocket/Socket.IO/queue) → `websocket-engineer`;
  transport/logic/auth/quality/perf → `backend-engineer`; test defects → back to the
  driver. Fix the layer that owns the invariant first (an atomic DB write often beats
  an app-level guard for a data race).
- **Fix-forward only.** Never skip, weaken, or disable a test or gate to go green.
- **No same-file parallel edits.** Same file → sequential; independent files →
  parallel, each dispatch with an explicit file allowlist. A task that needs a
  symbol an in-flight parallel task has **promised to export** is sequenced after
  it — or dispatched with the promised contract (name, owning file, signature)
  injected so it imports rather than duplicates. Repo-wide gates (typecheck/lint)
  run only at wave boundaries — never while parallel edits are in flight. Wave
  engineers dispatch in parallel at wave start with disjoint `files_owned`;
  **reviewers cannot stand by idle** (CC subagents run to completion and can't message
  each other) — **you are the message bus**. As each engineer returns you **accumulate
  its diff** (no per-fix static review); the `backend-reviewer` + `security-auditor`
  pass runs **once per wave at the wave-gate** over the cumulative diff (a per-fix pass
  is allowed only as an optional hotspot on a high-risk diff), and the queue orders the
  wave-gate's findings routed back to engineers still busy. The **wave-gate is that wave
  boundary**: the repo-wide gates and the one-pass static review run there, never
  mid-wave. **Full wave model: [`references/waves.md`](references/waves.md).**
- **Engineers verify change-scoped, not category-wide.** Every wave engineer is
  dispatched with the **scoped-test directive**: verify with a change-scoped run over its
  own `files_owned` (the tests targeting what it changed, by path/name filter), never the
  category-wide ("all the route tests") or repo-wide suite. Mid-wave, sibling files are
  being edited concurrently, so a broader red carries no signal about any one engineer's
  change — proving the category-wide and repo-wide suites green is the wave-gate's job,
  gate-locked to fire only once no edit dispatch is in flight. No engineer burns a turn
  triaging an out-of-scope red.
- **Flag the production-safety gates** when they apply: migrations forward-only/safe;
  new behaviour behind a flag with the flag-off path proven unchanged.
- **Pause on judgment calls** with `AskUserQuestion` — never pick a debatable
  product/architecture decision silently.
- **Spec drift never passes silently** (when attached to a change) — *silently*
  means undetected or unrecorded, not unasked. Every `specDrift` declaration and
  Spec Conformance finding goes through the two-tier gate: product/contract drift
  is asked synchronously; technical reconciliations are amended-and-reported and
  ratified at the next checkpoint. Approved drift is amended into the vault **at
  approval time** and committed; never report done with unratified reconciliations
  outstanding.
- **Every vault write is committed immediately** — an uncommitted vault is state
  only your session can see, and the other repo's session builds on the stale truth.
- **Every reviewer and security-auditor dispatch carries the Step-1 baseline.**
  Pre-existing working-tree state is the user's, not the feature's: never attributed
  to the diff, never flagged as scope creep, never reverted by a fixer.
- **Stay in scope** and **stop before the PR/MR.** Surface scope creep as a follow-up.
  Archive is likewise gated on the human's merge — offer it, never run it preemptively.

## References

Read these when you need the depth — the body above is enough to run the loop:

- [`references/modes.md`](references/modes.md) — the three modes in full: detection
  signals, per-mode driver behaviour, the live/review-only honesty rules. Read in
  **Step 1** when the mode isn't obvious.
- [`references/loop-procedure.md`](references/loop-procedure.md) — the detailed
  2a–2e procedure: driver dispatch, evidence sharing, classification signals,
  same-file rule, the review queue, the wave-gate, fix-forward discipline. Read in
  **Step 2**.
- [`references/waves.md`](references/waves.md) — the wave model: what makes a wave
  coherent/mergeable (no orphan files), dispatch-at-wave-start, the orchestrator-held
  review queue, and the Layer-1-vs-Agent-Teams routing choice. Read in **Step 2** when
  running a multi-task wave.
- [`references/review-gate.md`](references/review-gate.md) — the two static gates in
  full: the once-per-wave cadence + hotspot pass + final gate, the **final-gate
  `review-panel` trio (`sr`/`sa`/`qa`)**, thin dispatch, category routing, the severity
  policy, the tech-debt ledger. Read when running the **quality/security gates**.
- [`references/migrations-and-flags.md`](references/migrations-and-flags.md) — the
  production-safety gates: migration safety (forward-only, live-table-safe) and the
  feature-flag both-path proof. Read in **Step 1** when either applies.
- [`../spec-driven/references/loop-integration.md`](../spec-driven/references/loop-integration.md)
  — the full spec-lifecycle procedure: attach, vault sync, task tracking, the drift
  gate, ripple, closing, MR re-entry. Read when **attached to an OpenSpec change**.
