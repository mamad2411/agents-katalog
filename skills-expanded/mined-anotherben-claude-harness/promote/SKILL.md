---
name: promote
description: Promote dev to production (dev→main PR → gates → merge → migrations-first → pinned API deploy → portal verify → canary watch). Use when the user says "promote", "ship to main/prod", or "deploy the changes to main".
---

# /promote — ship dev to production

Repo: `anotherben/helpdesk`. Prod = `main`. Integration = `dev`.
Prod API service: `srv-d5bmjnmuk2gs73fcubeg` (autoDeploy OFF by design — deploy is a deliberate step).
Portal static sites (autoDeploy ON — rebuild themselves on a real merge push):
admin `srv-d5bmvvre5dus73fqn4t0`, supplier `srv-d74r6f94tr6s73culpvg`, repairer `srv-d5bn0c6r433s7392o7b0`,
customer `srv-d5bms6a4d50c73fbpqdg`, repairer-api `srv-d5bmnmchg0os73do2l6g`, admin-api `srv-d5bmmva4d50c73fbm8tg`,
customer-api `srv-d5bmmai4d50c73fblsng`.
Render key: `security find-generic-password -a ben -s htn-render-api -w` (never echo it or any DSN).
Prod Postgres: `dpg-d5bmg0uuk2gs73fcs6kg-a` — **the agent NEVER connects to it; all prod DB steps are operator-run scripts.**

Optional arg: `watch=N` (canary cycles, default 6; use 12 when the release carries migrations).

## Promote SMALL and OFTEN (read first)
The single most important rule, learned the hard way 2026-06-13: **never let main drift far behind dev.** Promote per-feature or roughly daily. A small delta sails through; a big backlog hits every wall below at once. If `git rev-list origin/main..origin/dev --count` is large (tens of commits) or the diff is near/over the cap, expect pain — prefer promoting a recent small slice and letting the rest drain over subsequent promotions, rather than one giant batched promotion.

## Hard-won gate mechanics (don't relearn these)
- **Size cap counts TOTAL churn (insertions + deletions), not insertions.** `check-pr-size-cap.cjs` (in enterprise-delivery-gate.yml) hard-rejects main PRs >100 files OR >5,000 total lines (no `incident-response` label). Compute split points on `git diff --numstat main..HEAD | awk '{i+=$1;d+=$2} END{print i+d}'`, not on insertions.
- **Splitting at a mid-dev commit ORPHANS the purchasing full-kit proof artifact** → preflight-main fails `purchasing-full-kit: proof_subject_not_ancestor_of_current_head`. A valid promotion PR must include the artifact's `proof_subject` commit AND stay under the cap — often impossible for a big backlog, which is why splitting needs per-batch artifact re-pinning (`docs/verify/*full-kit*`, re-pin proof_subject to the batch head). Another reason to promote small (no split needed).
- **copilot-review-wait treats SKIPPED as PASSING** (`PASSING_CONCLUSIONS = SUCCESS, NEUTRAL, SKIPPED`). For main PRs it requires preflight-main (not preflight-dev); preflight-dev is filtered out and vice-versa.
- **CANCEL-RACE — the big time-sink:** every `pull_request` event (push, body-edit, reopen) re-fires BOTH preflight-main and copilot-review-wait. preflight-main takes ~10 min; a second event cancels the in-flight run, and a *cancelled* check reads as non-passing → copilot-review-wait reports `blocking check failed: preflight-main:FAILURE` and gives up (non-waitable). **Fire exactly ONE event, then poll READ-ONLY only** (gh pr view / gh run list never fire events). Let copilot-review-wait's own ~20-min wait loop ride preflight-main to completion.
- To re-run copilot-review-wait WITHOUT restarting preflight-main: `gh run rerun <copilot-review-wait-run-id>` (isolated; re-evaluates current state). Body-edit/reopen restart everything (cancel-race risk).
- Pre-push to a `promote/*` branch needs an AI receipt: `node scripts/review/pr-readiness-substance-check.cjs --base <main-sha> --head <head>` with `TEST_DATABASE_URL`/`DATABASE_URL` from `~/.htn-purchasing-cert.creds` set (it's a DB-backed candidate); retry to `pass` only after verifying the code is correct.

## Steps

### 0. Preconditions (abort on any failure; report plainly)
- `git fetch origin --quiet`; require `origin/dev` strictly ahead of `origin/main` (else: "nothing to promote").
- List the delta: `git log origin/main..origin/dev --oneline` (show the user; >100 files or >5,000 lines changed → split the promotion, NEVER squash).
- Migration delta: `git diff --name-only origin/main..origin/dev -- apps/api/database/migrations/`. Remember the result for step 4.
- No open `incident-response`-labeled issue; prod `/health` reachable (200 or the known backlog-503).

### 1. Raise the promotion PR
- `gh pr create -R anotherben/helpdesk -B main -H dev --title "release: promote dev to main (<date>)" --body <body>`.
- Body MUST satisfy the main-PR schema enforced by `enterprise-delivery-gate.cjs` — read the required section list from that gate script in-repo at runtime (do not trust memory); include the commit list and the migration delta verdict.

### 2. Gates (no shortcuts)
- Trigger `@codex review` on the PR (Codex always reviews before merge).
- Wait for: all checks green, every review thread fixed-or-replied (no bulk resolve), quiet period satisfied. Re-run gates only via push/edit/rerun triggers.

### 3. Merge
- Merge-commit or rebase only (squash is disabled repo-wide). Confirm `origin/main` advanced to the expected sha.

### 4. Database first (ONLY if step 0 found migration files)
- HARD ORDER: migrations before API deploy, always.
- Generate an operator script following the proven pattern in
  `docs/plans/release-train/dev-to-main-2026-06-05/19-agentic-migration/scripts/run-prod-db-cutover.sh`
  (fetch DSN in-script from Render API, never echo; fail-closed checks; registered files via
  `applyVerifiedPendingMigrations.js --apply --only=<files>` run from a clean checkout with
  `env -u SHOPIFY_STORE_DOMAIN DEFAULT_TENANT_ID=cad85567-d14f-445e-aae3-d2f25f5bfe1f DOTENV_CONFIG_QUIET=true`;
  unregistered files via a transactional manual apply mirroring `.rehearsal-tmp/apply_9131.js`).
- Hand the user ONE line: `! bash <script>`. Do not proceed until it prints its COMPLETE marker.

### 5. Deploy the API (pinned, deliberate)
- `POST https://api.render.com/v1/services/srv-d5bmjnmuk2gs73fcubeg/deploys` with `{"commitId":"<new main sha>"}`.
- Poll every 30s to `live` (background). On `build_failed`/`update_failed`: rollback = POST a deploy pinned to the previous live commit; report loudly.

### 6. Verify the portal fleet
- For each portal service: latest deploy commit must equal the new main sha (auto-deploy fires on real merges).
- Any portal still on the old sha after ~5 min: trigger its pinned deploy explicitly. (Lesson from 2026-06-13: API-driven ref updates don't fire auto-deploy; merges do.)

### 7. Canary
- Baseline BEFORE the deploy when possible: `scripts/canary-health-gate.sh baseline` (bundled in this skill; state lands in `scripts/state/`).
- After deploy live: `scripts/canary-health-gate.sh watch` in background for N cycles (arg, default 6).
- Gate is baseline-relative (db connected, backlog ≤ baseline×1.2+25, no NEW issue codes). On FAIL: halt, diagnose trajectory before any rollback — a restart releases worker claims and re-flags items, which looks like a spike but drains; only a climbing backlog or db-down is rollback-class.

### 8. Close out
- Report: shipped commits, deploy id, canary verdict, anything waived (with reason).
- Comment-and-close issues whose fixes shipped (only with the user's standing authorization or explicit ok).
- If migrations shipped: note ledger delta in the report.
- **Sweep merged worktrees** — a promotion merges a batch of dev branches into main, so their per-feature worktrees are now stale. Run `~/.claude/scripts/cleanup-merged-worktrees.sh --repo /Users/ben/helpdesk --fetch --apply` (keeps active/open-PR worktrees, patch-backs any stray uncommitted change, removes only merged/remote-gone ones). Prevents the worktree-accumulation disk-full recurrence (memory: `worktree-accumulation`). Drop `--apply` to dry-run (default) and eyeball the list first.

## Hard rules
- Never `PUT` the env-vars collection endpoint; per-key writes only, and only with explicit operator approval.
- Never run migration tooling inside the prod Render runtime.
- Never echo credentials; prod DB work is always an operator-run script.
- One promotion at a time; if a canary from a previous promotion is still open, finish it first.
