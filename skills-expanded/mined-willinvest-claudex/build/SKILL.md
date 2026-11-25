---
name: build
description: Turn an approved spec into a merged-ready PR with Codex doing the writing. Claude conducts; Codex writes the plan and the implementation; a Codex reviewer and a Claude reviewer independently attack each artifact; a fresh Codex agent reconciles them into one verdict (go / fix-go / fix-review). Use when the user runs /claudex:build, or asks to build/implement an existing spec with Codex as the builder and an adversarial review loop.
---

# claudex:build — Codex-driven build orchestrator

You are the **conductor**. **Codex does the writing** — both the implementation
plan and the real implementation. You sequence the phases, integrate parallel
outputs, resolve conflicts, and decide verdict handling. You never hand-write
the plan or the implementation yourself; you dispatch that to Codex and review
its work.

Invoke this **after a spec exists** (e.g. from `/claudex:think`). The spec is an
**input**. The terminal state is an **opened PR** — never a direct push to
`main`.

## Prerequisites

- An approved spec (path under `docs/superpowers/specs/`, or the user points you at one).
- The **Codex plugin** (the `codex-companion` runtime + `/codex:status`/`/codex:result`/`/codex:cancel`) and **superpowers**.
- Run everything inside an **isolated git worktree** (see Phase setup). This keeps
  the user's working copy clean during a long multi-phase run.

> If Codex isn't available, see **Tool failure** below — core steps (builder,
> reconciler) hard-stop and ask the user; only a redundant review leg degrades.

## Setup (once, before Phase 0)

1. Confirm the spec path. If unsure, ask the user which spec to build.
2. Enter an isolated worktree (`EnterWorktree`, or the `using-git-worktrees`
   skill / `git worktree` fallback). Do all work there.
3. Locate the Codex runtime once and reuse it:
   ```bash
   COMPANION=$(ls -t ~/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs 2>/dev/null | head -1)
   ```

## How you talk to Codex

| Need | Mechanism | Mode |
|---|---|---|
| **Build / fix** (write the plan or implementation, or apply fixes) | `node "$COMPANION" task --write --background "<builder prompt>"` — run **yourself, from the conductor session, inside the worktree** | write-capable, **tracked** |
| **Codex adversarial review** of an implementation diff | `node "$COMPANION" adversarial-review --wait --scope working-tree "<focus>"` | read-only |
| **Codex review of a plan doc** (no diff yet) | `node "$COMPANION" task --fresh --effort <e> "<adversarial plan-review prompt>"` | read-only (no `--write`) |
| **Reconcile** two reviews → one verdict | `node "$COMPANION" task --fresh --effort <e> "<reconcile prompt>"` | read-only (no `--write`) |

**Dispatch the builder yourself — do not route it through the `codex:rescue`
subagent.** The companion buckets its job store by `git rev-parse --show-toplevel`
*and* filters `/codex:status` to the current `CODEX_COMPANION_SESSION_ID`. The
`codex:rescue` subagent (and the `/codex:rescue` command, which only wraps that
subagent) runs the companion from a **different cwd and session**, so the job
lands in another bucket and **never appears in your `/codex:status`**. Calling
`node "$COMPANION" task ...` directly from the conductor session keeps the job in
*this* worktree's bucket under *this* session — so it is trackable. `--background`
returns a **job id immediately**; poll it with `/codex:status <job-id>` (or
`--wait`), pull output with `/codex:result <job-id>`, and stop it with
`/codex:cancel <job-id>`.

> **Tracking caveat — `/codex:status` is worktree-scoped.** Because jobs are
> bucketed by worktree toplevel, `/codex:status` only lists jobs created in the
> **same worktree it is run from**. Run it (and surface job ids to the user) from
> the build worktree. From elsewhere, query by explicit job id.

For **parallel** builders, fire several `task --write --background` calls in one
batch — each prints its own job id; track them with `/codex:status <job-id>`
(see `dispatching-parallel-agents` essence).

**Routing fixes back to the builder — do not trust `--resume`.** `--resume`
resolves to `--resume-last` (the *latest tracked Codex thread*), not a named
builder. After parallel builders, a review, or a reconcile, the latest thread is
almost certainly the **wrong** one. So:

- Only use `--resume` for fixes in a **single-builder phase with no intervening
  Codex task** (no parallel builders, no Codex-side review/reconcile in between).
- Otherwise, start a **fresh write task** that re-supplies everything the fix
  needs: the target files, a short summary of the original builder's context, and
  the **specific findings** to address. Never `--resume-last` after parallel
  builders.

## Top-level flow

```
Phase 0 — Spec readiness gate
Phase 1 — Plan    ── unified verdict loop, target = plan doc
Phase 2 — Build   ── unified verdict loop, target = implementation diff
Phase 3 — Integrate → branch + PR (human merge gate)
```

### Phase 0 — Spec readiness gate

Run **one** Codex read-only review of the spec for **actionability only** —
scope, ambiguity, acceptance criteria, risks, missing constraints. (It is not a
redesign.) Use a `task` prompt that asks Codex to list *blocking* gaps that would
stop a plan from being written.

- **Blocking gaps?** Only **non-semantic** edits may be folded in automatically
  (typo / broken link / wrong path). **Any semantic change** — acceptance
  criteria, constraints, dependencies, user-visible behavior, security posture,
  or risk — is a **material scope change** and is **user-gated**.
- **Material scope change** proposed? **PAUSE and ask the user.** Do not edit the
  approved spec's meaning without approval.
- Before leaving Phase 0, record a **spec diff** (what changed vs. the approved
  spec) so the change is auditable.
- **No blocking gaps?** Proceed to Phase 1.

### Phases 1 & 2 — the unified verdict loop

The same control flow runs for the **plan** (Phase 1) and the **build** (Phase 2).

**Step 1 — BUILD (Codex writes the artifact).**
- *Plan phase:* one Codex builder writes the implementation plan from the spec
  (follow the *essence* of `writing-plans` — staged tasks, acceptance criteria,
  test strategy). Save under `docs/superpowers/plans/`.
- *Build phase:* **you decide per plan.** Parallel background `task --write`
  builders for genuinely independent units (you integrate the outputs and resolve
  conflicts); a single builder for tightly-coupled work — shared files,
  migrations, fragile test suites. **No parallelism for coupled work.**

**Step 2 — DUAL ADVERSARIAL REVIEW (independent, in parallel).**
- **Codex side:** `adversarial-review` on the diff (build phase) or a read-only
  `task` plan-review (plan phase).
- **Claude side (adaptive):**
  - *plan phase* → a Claude subagent prompted to **attack** the plan doc.
  - *build phase* → the local `/code-review` skill on the diff.
  - *escalate* to a stronger independent subagent for high-risk work
    (cross-cutting, security-sensitive, large, or ambiguous).
- Each reviewer must return the **review contract**:
  1. **blocking findings** (correctness / security / merge-blockers)
  2. **requirement gaps** (spec / acceptance criteria not met)
  3. **test gaps**
  4. a **merge-readiness signal**

**Step 3 — RECONCILE (a fresh Codex agent → one verdict).**
Hand both reviews (verbatim) to a **new** read-only Codex `task`. Ask it to
dedupe/weigh them and return exactly one verdict:

| Verdict | Meaning | Action |
|---|---|---|
| **go** | no fixes needed | phase complete |
| **fix-go** | low-risk/mechanical fixes only | original builder applies fixes; **then a post-fix check** (see below); phase complete |
| **fix-review** | consequential fixes | original builder applies fixes; **loop back to Step 2** on the fixed artifact |

Report the reconciler's verdict + rationale back in the main session before acting.

**`fix-go` post-fix check.** After the builder applies a `fix-go`, inspect the
resulting diff/scope. If the change turns out **non-mechanical** (touches logic,
interfaces, behavior, or new files beyond the stated fix), **upgrade it to
`fix-review`** — re-review it and count it against the loop guard. `fix-go` only
ends a phase when its fixes were genuinely mechanical.

**Step 4 — LOOP GUARD.**
Count `fix-review` verdicts (including upgraded `fix-go`s and Phase 3 red-test
returns, below) **per phase**. The first triggers one re-review. If a re-review
returns `fix-review` **again** (the second attempt), **STOP and ask the user** —
do not loop further. A material scope change at any point also **pauses for the
user**.

### Phase 3 — Integrate

1. Run the project's **tests / build**. They must pass. A red result is treated
   as blocking findings → loop back into the Phase 2 verdict loop (do not
   integrate). **A red-test return counts as a `fix-review` attempt** under the
   Phase 2 loop guard — a second one stops and asks the user rather than looping
   forever.
2. Emit a **final report**: per-phase verdicts, any **degraded gates**, any
   **scope deltas**, and a **diff summary**.
3. After the user OKs the report, **push the branch and open a PR**. The PR is the
   human merge gate. **Never push to `main` directly.**

## Cross-cutting policies

- **Tool failure:** retry the failing Codex call **once**, then apply the policy
  **by call type** — degrading a core step would advance toward a PR with a
  skipped gate, so core steps never degrade:
  - **Builder / fixer fails** → **hard stop, ask the user.** There is no artifact
    to ship without it; do not degrade regardless of `failClosed`.
  - **Reconciler fails / returns no clear verdict** → **hard stop, ask the user.**
    No verdict means no decision; never infer `go` from a failed reconcile.
  - **One review leg fails** (Codex *or* Claude reviewer) → **degrade only if the
    other leg succeeded**, so the reconciler still has a real signal; log it and
    surface it in the final report. If **both** legs fail → hard stop.
  - `failClosed: true` in `~/.claude/claudex/config.json` turns even the
    single-leg degrade into a halt.
- **Scope authority:** material scope changes are **user-only** — pause for
  approval. Plain fixes flow automatically.
- **Verification before completion:** never claim a phase passed without the
  reconciler's verdict; never integrate without green tests/build.
- **Config:** reuse `~/.claude/claudex/config.json` — `effort`, `failClosed`,
  `timeoutMs`.

## Enforcement note

This skill is **model-driven** — there is no hook forcing the loop. The verdict
loop *is* the control structure; follow it as written. (Contrast `/claudex:think`,
which is hook-enforced.)
