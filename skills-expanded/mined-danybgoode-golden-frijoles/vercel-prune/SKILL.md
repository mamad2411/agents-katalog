---
name: vercel-prune
summary: "Reports stale Vercel preview deployments for a frontend project; dry-run by default."
description: >
  Reports stale Vercel PREVIEW deployments for a named frontend project — dry-run only, never deletes
  anything on its own. Use when the product owner asks to "check stale previews", "run vercel prune",
  "how many dead previews are there", "clean up Vercel previews", or as the nightly ops routine's
  second step. Wraps scripts/vercel-prune-previews.mjs with the open-PR-protected branch list
  computed fresh each run. --apply is a SEPARATE, human-confirmed action this skill never takes on
  its own — see Stage 3.
# Repo-local scripts this skill wraps — its FULL closure: the entry script, everything it imports,
# scripts it runs as subprocesses, and data files it reads by path. Paths are relative to the
# CONSUMING project's scripts/ dir; they deliberately do NOT ship inside this plugin. CI
# (scripts/check-skill-scripts.mjs) walks the import graph and fails if this list understates it.
requires_scripts:
  - vercel-prune-previews.mjs
---

# vercel-prune — nightly stale-preview report (dry-run by default, apply is human-gated)

<!-- kit block: frozen at the move out of the plugin (plugin-1-0 S3.3); nothing renders it now, and in this repo
     the local scripts/ copy always wins, so the pinned version below is only the fallback. -->
> **Running this skill's scripts.** Each `node scripts/<name>.mjs <args>` below means, from the project root:
> `if [ -f scripts/<name>.mjs ]; then node scripts/<name>.mjs <args>; else npx -y @golden-frijoles/kit@0.45.0 <name> <args>; fi`
> The project's own copy always wins. The kit needs no install and copies nothing into the repo. If npx fails on
> the network or the registry (ENOTFOUND, ECONNREFUSED, ETIMEDOUT, E404, a proxy error), report **could not
> look: the kit is unreachable**, not a broken project, and offer to retry online or to copy the script into
> `scripts/`. This covers the scripts the kit carries (`frijoles-kit --list`). Any other `scripts/` command here is
> project tooling: if the project lacks it, say so and stop. Never re-implement a script's logic inline.
> If a script prints `GF-NEEDS-SETTING {"key",…}`, ask the user that question once, save the answer with
> `npx -y @golden-frijoles/kit@0.45.0 config set <key> <value>` (always the kit, never local-wins: a project
> may own an unrelated `scripts/config.mjs`), tell them they can change it later the same way, and run the
> script again if it exited 7.
<!-- kit:end -->

> **This skill's scheduled/default action is ALWAYS a dry-run report.** `--apply` is a distinct,
> explicitly-requested action (Stage 3) that only runs when the product owner asks for it in the
> SAME conversation — never automatically, never from the nightly routine.

## Project config — TEMPLATE FILL-IN

Supply these per consuming project. This skill **refuses to guess them** — if one isn't filled in,
say which and stop.

| Value | What it is |
|---|---|
| `<VERCEL_PROJECT>` | the Vercel project whose previews this run targets. **Required: `--project <VERCEL_PROJECT>`** — the underlying script has no default and exits with a usage error without it, because a defaulted name once meant pruning whichever account the default happened to name. The standup reads the same value from `reporting.config.json` → `vercelProject`. |
| `<PR_REPO>` | the GitHub repo whose open PRs protect a branch from pruning — the repo that actually deploys to `<VERCEL_PROJECT>` |

> One Vercel project per invocation. A project with several deployed frontends runs this once per
> frontend, each with its own `<VERCEL_PROJECT>`/`<PR_REPO>` pair — never one run assumed to cover all.

## When to run me
The product owner asks about stale Vercel previews, or the nightly **ops-nightly** routine invokes me
as its second step (dry-run report only).

## What already exists (reuse, don't rebuild)
- **`scripts/vercel-prune-previews.mjs`** — does all the actual work: pages Vercel deployments, filters
  to `target !== 'production'` (production is never touched, regardless of flags), computes age,
  respects `--keep-branch`. Dry-run by default; `--apply` is opt-in. Zero new automation needed here —
  this skill is just the two-command recipe below plus the apply-gating discipline.
- **`gh pr list`** — the source of truth for "which branches have an open PR right now" (the live
  review target that must never be pruned).

## Stage 1 — compute the keep-branch list
`gh pr list --repo <PR_REPO> --state open --json headRefName --jq '.[].headRefName'` → join the
results into a comma-separated list (empty is fine — means no open PRs).

## Stage 2 — the scheduled/default action: dry-run report (always this, never more)
`node scripts/vercel-prune-previews.mjs --project <VERCEL_PROJECT> --age 7 --keep-branch <list from
Stage 1>`

Report back: total previews scanned, count/branches flagged for removal, and confirm the open-PR
branches from Stage 1 are excluded from that list. **This step never passes `--apply`.**

## Stage 3 — apply (ONLY when the product owner explicitly asks, in this exact conversation, to actually delete)
1. Re-run Stage 1 (branch list may have changed) + Stage 2 to restate exactly what would be deleted.
2. Get one more explicit go-ahead from the product owner on that exact list.
3. Re-run with `--apply` added: `node scripts/vercel-prune-previews.mjs --project <VERCEL_PROJECT>
   --age 7 --keep-branch <list> --apply`.
4. Report the actual delete count/failures.

**Never invoke Stage 3 from the nightly routine or without a fresh, explicit ask in-conversation** —
"the nightly routine ran vercel-prune" is never sufficient authorization for `--apply`.

---

## Gotchas
- **Production deployments are never touched, by the underlying script itself** — `target ===
  'production'` is filtered out unconditionally, independent of any flag this skill passes. That's the
  real safety net; this skill's dry-run-then-human-confirm discipline is the second layer, not the
  only one.
- **An open-PR preview is the live review target — always compute `--keep-branch` fresh (Stage 1)
  before either a report or an apply.** A branch that merged since the last run should no longer be
  protected; a branch that just opened a PR must be. Don't reuse a stale keep-list from an earlier
  session.
- **The underlying script's own bare default is `--age 0`**, which flags literally every
  non-production preview, including one from a PR opened yesterday. This skill always passes `--age 7`
  to match the meaningful "stale" bar `standup.mjs` already established — don't drop that flag.
- **`--apply` deletes are irreversible and hit real Vercel infra** — this is the epic's one
  destructive-op story. Even after the first live apply is confirmed, treat every subsequent `--apply`
  as its own explicit ask, not a standing permission — the routine structurally never runs Stage 3, so
  there's no "it's already automated, skip the check" shortcut to reach for.
- **`--project` has no default, on purpose.** The script was written for one specific Vercel project
  and used to default to it, which let an invocation that omitted `--project` scan and flag previews in
  an account unrelated to this project. It now refuses to run without one — do not "fix" that by
  adding a default back. Each additional Vercel project is its own explicit
  invocation, not an extra flag on this one.
