---
name: claim-safety
description: >
  Claim a Forge issue and then PROVE you hold the live lease before you touch it, using `forge
  issue owns <id>` (exit 0 iff you hold the single unexpired lease). Use this whenever winning
  the claim matters: right after `forge claim`, before you `dev`/edit/`close`/`release` a
  claimed issue, when two agents or a subagent fan-out contend for the same work, or before
  any irreversible step. A claim's `ok:true` does NOT prove you won — duplicate replays return
  it and expired leases get reclaimed; only `owns` proves it, so re-verify before
  close/release. Trigger on "claim this issue safely", "did I actually win the lease",
  "verify/prove ownership", "claim conflict", "two agents grabbed the same issue", "check I
  still own it before closing", or before ANY mutation of a claimed issue. NOT for plain
  single-issue create/update/close/comment with no ownership question (that is issue-basics),
  and NOT for read-only selecting or ranking the next ready issue without claiming (that is
  triage-ready).
allowed-tools: Read, Bash(forge:*)
next: dev
terminal: false
---

# Claim safety — claim, then prove you own the lease

> **Chain:** once you have PROVEN the lease (`forge issue owns <id>` exits 0), continue to `dev` to work the issue (`smith` proceeds into plan/dev after this proof). Usable standalone whenever ownership is in question.

Claiming is not owning. The Forge kernel keys a claim's idempotency on
`claim.create:<issue_id>:<actor>`, so a **same-key duplicate replay returns
`ok:true`** echoing the *current* call's `claim_id`. A genuine cross-actor
conflict returns `ok:false` (the partial-UNIQUE active-lease index guarantees one
lease) — but `ok:true` **alone does not prove sole ownership**. A live lease can
also be **reclaimed on expiry** (an expired lease is superseded by the next
claimant). Therefore every worker MUST verify ownership before mutating a claimed
issue, and RE-verify before `close`/`release`.

This is a reusable, standalone procedure: any skill or agent that mutates a
claimed issue embeds it (it is NOT folded into one orchestrator).

## The verification primitive

```bash
forge issue owns <id>          # exit 0 iff YOU hold the live lease; non-zero otherwise
forge issue owns <id> --json   # { ok:true, data:{ owned, claimed_by, expired, actor, expires_at } }
```

`owns` resolves your actor the same way the kernel does — `FORGE_ACTOR` →
`FORGE_SESSION_ID` → default `forge` — then reports `owned:true` iff you hold the
**single active claim** AND that lease **has not expired**. It exits `0` when you
own it and non-zero (conflict, code 4) when you do not, with a clear "you do not
own the lease for `<id>` (held by `<actor>`)" message. It is a strict READ — it
never mutates kernel state. (`data.claimed_by` is lease-derived; there is no
`claims` command.)

## Procedure

1. **Select** work — `forge issue ready --json` (see the `triage-ready` skill).
   Never claim epics/decisions or defer-windowed items.
2. **Claim** — `FORGE_ACTOR=<your-actor> forge claim <id>`. Always run under a
   distinct actor so a losing claim reaches the conflict guard instead of
   collapsing to a shared-actor duplicate.
3. **Prove ownership BEFORE working** — `forge issue owns <id>`.
   - **exit 0 (OWNED)** → the lease is yours; proceed to work.
   - **non-zero (NOT OWNED)** → you lost the race, or your claim collapsed to a
     foreign/duplicate-collapsed claim. Do NOT work the issue. **Reselect** via
     `forge issue ready --json` and start over at step 1.
4. **Work** the issue (`dev`/edit/etc.).
5. **RE-verify before `close`/`release`** — a live lease can be reclaimed on
   expiry while you worked. Run `forge issue owns <id>` again:
   - **OWNED** → `forge release check --target <release-ref> --json` (release-readiness; omit `--target` to use the project default), then
     `forge close <id> --reason "…"` or `forge release <id>`.
   - **NOT OWNED** → the lease was reclaimed (likely expired). Do NOT close/
     release someone else's lease; reselect and, if the work is still needed,
     re-claim and reconcile.

## Contract (what each result means)

| `forge claim` result | Meaning | Action |
|----------------------|---------|--------|
| `ok:false` (conflict, code 4) | A live lease is held by another actor | Reselect (`ready`) |
| `ok:true` | Provisionally yours — **not proof** (duplicate replays also return ok:true) | **Run `forge issue owns <id>`** |

| `forge issue owns` | Meaning | Action |
|--------------------|---------|--------|
| exit 0, `owned:true` | You hold the live, unexpired lease | Work / close / release |
| non-zero, `owned:false` | Someone else holds it, or your lease expired | Reselect; never mutate |

## Fork points

- **Actor source** — how `<your-actor>` is derived (`FORGE_ACTOR` explicit id →
  `FORGE_SESSION_ID` → default `forge`). Use a distinct per-agent actor so
  contending claims reach the conflict guard rather than collapsing to a duplicate.
- **Expiry / lease TTL** — whether claims carry an `expires_at` and how long;
  `owns` treats an expired lease as NOT owned (it can be reclaimed).
- **Re-verify cadence** — verify after claim and again before `close`/`release`;
  a longer task may re-verify more often (e.g. before each irreversible step).
- **Reselection policy** — on NOT-OWNED, how the next item is chosen (ranking /
  filters live in the `triage-ready` skill).
- **Fail-closed posture** — with no usable clock/state, treat ownership as NOT
  proven (mirror the readiness model's "no usable clock ⇒ not workable").

## Reliability notes

- A genuine cross-actor conflict returns `ok:false` — there is no phantom
  `ok:true`-on-conflict. The real hazards are (a) a duplicate replay's `ok:true`
  and (b) expiry-driven reclaim. `owns` closes both.
- Full multi-agent safety depends on the actor-identity kernel fix (distinct
  actors per agent, kernel `d71a824b`): without distinct actors, two agents
  share one idempotency key and `owns` cannot tell them apart.
