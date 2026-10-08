# CLAUDE.md

Guidance for Claude Code working in this repo. Source of truth for *how to work here*; the codebase itself is the source of truth for *what exists*.

## Read First

Before touching a feature or bug, read the relevant doc(s):

| Doc | When to read |
|-----|--------------|
| `docs/ARCHITECTURE.md` | Data flow, node roles, sync loop, rebalance engine, lane model, capabilities |
| `docs/IMPLEMENTATION.md` | File-by-file map (API + web), routing, frontend patterns, layout constraints |
| `docs/API.md` | Complete endpoint reference with access rules |
| `docs/DATABASE.md` | Schema, migrations, key tables |
| `docs/LOOP_SETUP.md` | Loop Out setup + production gotchas (prepay model, min capacity, restart cascade) |
| `docs/COINBASE_INTEGRATION.md` | Cloudflare Worker architecture, secrets, redeploy |
| `learnings.md` | Scar index (repo root) — past failures and the generalized lesson from each; skim when about to repeat a class of mistake |

For per-version history: `git log`. This file is not a changelog.

## Mission

Bitcorn Lightning is a **Lightning Treasury Capital Allocation Engine** — not a wallet, not a UI product, not a generic routing node. Net sats is the only number that matters:

```
Net Sats = inbound + forwarding fees − outbound fees − rebalance costs
```

See `docs/ARCHITECTURE.md` for the full mission, roles, and capabilities.

### Non-Negotiables

- Guardrails cannot be bypassed by automation
- Capital reserve floors must always be respected
- Deploy ratio limits must always be enforced
- Rebalance costs must always be accounted for
- Automation must be auditable and deterministic
- Safety > growth
- **Ask before touching networking, auth, Lightning flows, or Umbrel manifests** — this is a production Lightning application

## Project Layout

- `app/api/` — TypeScript API (port 3101)
- `app/web/` — React + Vite UI (port 3200)
- `cloudflare-worker/` — Worker holding CDP credentials + commodity price cache
- `docs/` — architecture and reference
- No automated test suite yet. Migrations run automatically on API startup.

## Build & Dev

```bash
# API
cd app/api && npm run build && npm start

# Web dev server (hot reload)
cd app/web && npm run dev

# Full stack
docker compose up -d --build
```

Frontend deps: `react`, `react-dom`, `react-router-dom`, `recharts`, `date-fns`, `qrcode`.

**Verification stop-gate:** a committed Stop hook runs `scripts/verify-gate.mjs` at every turn end — with uncommitted `app/api`/`app/web` changes it runs that side's tsc + vitest and blocks completion on real failures (known-baseline tsc errors are allowlisted; a broken runner warns instead of blocking; clean/read-only sessions are never gated). Escape hatch: `VERIFY_GATE_SKIP=1`. Details in the script header.

**Parallel sessions (worktrees):** `claude --worktree <name>` creates an isolated checkout at `.claude/worktrees/<name>/` on branch `worktree-<name>` — already gitignored by the existing `.claude/*` rule. `.worktreeinclude` copies in the gitignored files a fresh checkout can't regenerate (the four `.env.dev.*` files, `cloudflare-worker/.dev.vars`); dependencies are NOT copied — install per worktree, and note `better-sqlite3` compiles native bindings each time.

⚠ **`worktree.baseRef` is set to `"head"`, which makes branch hygiene load-bearing.** The default `"fresh"` branches from the *remote default branch* — predictable, and wrong here: it starts every worktree from `main`, so accumulated `develop` work is silently absent. That bit us for real: a worktree created while on `develop` landed two commits behind, on `main`, carrying a stale copy of the very script being fixed. `"head"` branches from your current local `HEAD` instead — correct when you're on a current `develop`, and **faithfully wrong when you're on a stale one.** This repo's standing rule is that branch position is a query, never a remembered fact, and `"head"` puts that rule directly in the path of worktree creation. So: **launch worktrees from a freshly-pulled `develop`, then run `git log --oneline -1` inside the new worktree before doing any work.** Inside a worktree, `"head"` resolves to *that* worktree's HEAD, not the main checkout's. (Set in `.claude/settings.json`, which is strict JSON and takes no comments — hence this note.)

## STATE.md — Generated Ground Truth

`scripts/state-snapshot.mjs` generates `STATE.md` (repo root, gitignored) from actual current reality: git state for this repo + the sibling stablecoin-rail checkout, a features inventory (API routes, pages, migrations/tables), and — when configured — Base chain and deployment reads. A committed SessionStart hook (`.claude/settings.json`) auto-runs the fast tier each session (`--fast`: local sections refreshed, chain/deployment carried over with their timestamp) and surfaces STATE.md into context.

- Full snapshot (chain + deployment): `node scripts/state-snapshot.mjs` — config in `state-snapshot.config.example.json`, details in `scripts/README.md`
- STATE.md is **generated — never hand-edit it**; trust it over memory for "what's on which branch / what's deployed"
- **Volatile state is a query, not a fact — cite the invocation, never the value.** Branch position, push status, merge status, deploy status, and what's-in-prod all change without anyone editing the note that claims otherwise. So don't write the value down: write the command that answers it (`git log --oneline origin/main..HEAD`, `git status -sb`, `gh run list`, STATE.md) and re-run it at read time. This includes beliefs about what a file contains — grep it, don't recall it. (All three have burned us: a commit described as unpushed two weeks after it reached origin, a runbook cited by the wrong date, and a skill claimed to document a trap it never mentioned.)

## Branching & Deployment

- `main` — production; pushes trigger Docker image builds via GitHub Actions (only for paths in `docker-publish.yml`'s `paths:` filter)
- `develop` — integration branch
- `feature/*` — feature branches

**Name the direction. The two are not symmetric and confusing them has caused real misreadings:**

- **Promotion** — `feature/*` → `main`, or `develop` → `main`. Moves code toward production. Triggers a build.
- **Back-merge** — `main` → `develop`. Returns released code to the integration branch. Ships nothing.

"Merge to main" is a promotion; "merge main" is a back-merge. Say which.

### Two promotion paths, chosen by change size. Both are legitimate.

**Small, single-purpose change → `feature/*` → `main`,** shipped immediately as its own release. This is most work, and it does not need `develop`.

**Large multi-commit work that must accumulate before shipping → `feature/*` → `develop` → `main`,** promoted as one release. The stablecoin rail is the live example.

⚠ **NEVER PROMOTE APP CODE TO `main` WITHOUT A VERSION BUMP.** The build fires on any push to `main` touching `docker-publish.yml`'s filtered paths, and the published image tag is read from `umbrel-app.yml`'s version. **Since `ce0080d` (2026-08-12) the consequence is a RED BUILD, not a republish:** `get-version` asserts that `refs/tags/v<version>` does not already exist, and every build job declares `needs: get-version`, so the assert trips before `build-api`, `build-web` or `build-loopd` starts and **nothing reaches ghcr.io.** The rule stands — you still must bump — but forgetting it now blocks the release loudly instead of shipping quietly. Re-derive rather than trusting this paragraph: `grep -n 'Assert the release tag does not exist' -A 30 .github/workflows/docker-publish.yml` and `grep -n 'needs: get-version' .github/workflows/docker-publish.yml`. This is not specific to `develop`.

**What that assert prevents** — described here in the present tense because it is still exactly what a same-tag republish does, not because it can still happen by accident: nodes already on that version see no update — the version string didn't change, so `umbreld` has nothing to offer — and keep their cached image, while any fresh install or re-pull gets the new content under the same tag. Two nodes then report the same version while running different code, and **nothing on either node distinguishes them.** It is the same mechanism as the same-tag hotfix in § Umbrel Gotchas below, which is deliberate and remains reachable by deleting the tag first. What changed in `ce0080d` is only that CI no longer lets it happen unnoticed.

**It has already happened.** `1.17.19` has been published three times, from three different trees, all builds succeeding: `887d814` (the actual v1.17.19 release, 2026-06-18), then `34c20c2` (PR #224, 2026-07-21) and `f323faf` (PR #227, 2026-07-21) — both of which changed `app/api/**` and `app/web/**` with no bump. So `1.17.19` does not uniquely identify a build, and a node reporting it could be running any of the three. Re-derive rather than trusting this paragraph: walk `git log --first-parent --merges main` and, for each merge, check `git diff <m>^1 <m> --name-only` for `app/` paths against whether `umbrel-app.yml`'s version changed in that same merge.

`develop` → `main` is the case most likely to forget, not the only case that can: a large accumulated merge doesn't carry a bump the way a single-commit release branch naturally does. Put the version-bump commit on `develop` BEFORE promoting — one build, correct tag, nothing overwritten. See `docs/RELEASE.md` § Releasing from `develop`.

**Back-merge is required arc closure, not an afterthought.** After merging a release to `main` — by EITHER promotion path — immediately back-merge `main` → `develop` as the closing step of the arc; never defer it. The back-merge happens BEFORE the implementation deltas are placed via Cowork — both are part of arc closure, not optional. (Deferring it has caused `develop` to silently drift multiple releases behind `main` more than once.)

**This rule is load-bearing on the DIRECT path specifically** — which is easy to miss, since the direct path never touches `develop` on the way out. Most releases since 2026-03-06 went straight to `main`; `develop` is nonetheless not behind, because the back-merge is being done every time. Verify rather than trust this sentence: `git rev-list --left-right --count origin/main...origin/develop` (left number is what `main` has that `develop` lacks — it should be 0), and `git log --merges --oneline develop | grep -i "main into develop"` for the record of them. Do not scope this rule to the `develop` path.

### ⚠ OPEN QUESTION — the sideload test gate went missing

The previous convention read `feature/* → develop → sideload test on Umbrel → main`. That **sideload test on a real Umbrel node is the only verification this repo has ever had that installs the app on real hardware**, and the direct path dropped it silently — nobody decided to retire it; it stopped happening when the path changed.

**Undecided — do not assume either way:** whether to reinstate it for the direct path, require it on both, or deliberately retire it. Recorded here so the gate stays on the record instead of vanishing with the old text.

Note what its absence leaves in place — and note that this changed under the section without answering it. **CI now hard-gates every PR** (`.github/workflows/pr-checks.yml`); don't trust a job list written here, read it: `grep -n '^    name:' .github/workflows/pr-checks.yml` for what runs, `gh run list --workflow=pr-checks.yml` for whether it's passing. Two of those gates enforce hazards this file documents by hand above — version agreement across the two files, and the app-code-without-a-bump footgun.

**None of them install anything.** Every job runs on a GitHub runner with no Umbrel and no LND, so the install failures in § Umbrel Gotchas below — flipping back to "Install" at 0%, the ~50% port-conflict reset, a half-installed app, images missing from ghcr.io — remain reachable only by installing a real release on a real node. That is the gap the missing sideload test used to cover, and CI does not narrow it.

One residual caveat, down from two: the local `verify-gate` Stop hook — bypassable via `VERIFY_GATE_SKIP=1`, and absent for anyone working from another machine — is still the only check between a commit and opening the PR.

**The other caveat is closed, and the correction matters more than the caveat did.** It used to read: "the workflow triggers on `pull_request` only, so it gates PRs rather than pushes (fine while direct pushes to `main` stay forbidden, **load-bearing on that**)." The trigger observation is still true — `pr-checks.yml` has no `push:` trigger, by design. What was load-bearing on a *convention* is now enforced mechanically: **repository ruleset `20756755` ("main protection", `enforcement: active`)** carries a `pull_request` rule and a `non_fast_forward` rule, with `bypass_actors: []` and `current_user_can_bypass: "never"`, so a direct push to the default branch is refused rather than merely discouraged. It also carries `deletion` and `required_status_checks` (eight contexts, `strict_required_status_checks_policy: true`).

Do not take that from this paragraph — it is exactly the class of volatile fact this file says to re-query: `gh api repos/ethancail/bitcorn-lightning-application/rulesets/20756755`. Two things that read confirm which this sentence cannot: the ruleset's condition is `ref_name.include: ["~DEFAULT_BRANCH"]`, so it governs `main` **only** — `develop` has no ruleset and no classic protection (`gh api repos/ethancail/bitcorn-lightning-application/branches/main/protection` returns 404 "Branch not protected", confirming there is no classic layer anywhere) — and the eight required contexts are pinned **by exact string**, so renaming any job `name:` in `pr-checks.yml` makes the ruleset require a check that never appears, which blocks merges permanently. Changing a required job's name is a two-part change: workflow *and* ruleset.

### Umbrel Gotchas (read before releasing)

**The full release procedure is `docs/RELEASE.md`** — nine steps, which are MANUAL vs AUTOMATED, the GHCR verification step that prevents the 0%-install failure below, the `develop`-release footgun (merging without a version bump — which since `ce0080d` fails at `get-version`'s tag assert rather than overwriting the current release's image tags), and an honest untested-rollback section. The gotchas below are the recovery commands; the doc is the procedure.

**Version must match in two files.** Bump `umbrel-app.yml` AND `bitcorn-lightning-node/docker-compose.yml` image tags together. Drift → Umbrel pulls stale images.

**If install fails (flips back to "Install" at 0%):** Docker images likely don't exist on ghcr.io yet. Check `gh run list` for a failed build. Common cause: transient npm 403 errors (e.g. `npm install -g serve` rate-limited). Re-run with `gh run rerun <run-id> --failed`. Always verify the build is green after a version bump.

**If install reaches ~50% then resets:** Port conflict. Check `sudo journalctl -u umbreld -n 100` for "already allocated". Remove conflicting container (`sudo docker rm -f <name>`) and retry.

**Half-installed after early user click:** If the user triggers Umbrel update before ghcr.io images finish building, app gets stuck. Fix: `sudo docker pull ghcr.io/ethancail/bitcorn-lightning-application/<api|web>:<version>` then `sudo umbreld client apps.restart.mutate --appId bitcorn-lightning-node`.

**Hotfix under same tag:** Umbrel won't auto-detect image changes for an unchanged tag. Force-pull + restart with the same commands as above.

**Umbrel restart command (newer Umbrel):**
```bash
sudo umbreld client apps.restart.mutate --appId <appId>
```
The older `sudo ~/umbrel/scripts/app restart <appId>` does not exist on newer Umbrel.

**Docker QEMU ARM64 crashes:** `node:20-alpine` (musl libc) causes `qemu: uncaught target signal 4 (Illegal instruction)` during multi-arch builds on GitHub Actions. Fix: `node:20-slim` (Debian/glibc). Web build stage can use `--platform=$BUILDPLATFORM` (Vite output is platform-independent); API cannot because `better-sqlite3` native bindings must compile for the target arch — install `python3 make g++` in the build stage instead.

## Ports (do not change without approval)

| Port | Purpose |
|------|---------|
| 3101 | User/Admin API (JWT, Umbrel-aware) |
| 3109 | Node-to-Node API — **reserved, no implementation** |
| 3200 | Web UI |

Do not reuse 3001 or 3009. Do not expose 3109 via Umbrel app-proxy. Port 3109 is reserved in `ports.ts` but has no implementation — the stub files were removed 2026-05; the longer-term fate of the reservation itself is an open decision. No member liquidity coordination uses it.

## Security Constraints

- Secrets generated on first run and stored under `/data/secrets` — never hardcode or commit
- User/Admin API (3101): JWT auth
- Node-to-Node API (3109): reserved port, no implementation. Original design called for HMAC + timestamp + nonce; not built.
- No `docker.sock` mounts, no privileged containers, no host networking

## Environment Variables

`app/api/src/config/env.ts` is authoritative. Variables worth knowing by heart:

- `TREASURY_PUBKEY` — hard-coded in `docker-compose.yml` as `02b759b1552f6471599420c9aa8b7fb52c0a343ecc8a06157b452b5a3b107a1bca`. Identifies the treasury node so all member installs get correct role detection automatically.
- `LND_GRPC_HOST` — default `lightning_lnd_1:10009`
- `REBALANCE_SCHEDULER_ENABLED` — default `false` (treasury-side Loop Out scheduler — edge-case + external-inbound maintenance only; off in steady state)
- `RATE_LIMIT_MAX_SINGLE_PAYMENT` — default `250000` sats
- `REBALANCE_MAX_FEE_PPM` — default `1000` (caps effective fee-to-amount ratio; prevents net-negative micro-rebalances)
- `COINBASE_APP_ID` + `COINBASE_WORKER_URL` — required for Fund Node button (503 if either unset)

## Files to Share When Getting External AI Assistance

Docs describe *what* exists; source code shows *how* it works. When using Claude chat or another AI for brainstorming, paste the relevant source files:

| Area | Files to share |
|------|----------------|
| Channel ROI / peer scoring | `src/api/treasury-channel-metrics.ts`, `src/api/treasury-liquidity-health.ts`, `src/api/treasury.ts` |
| Capital guardrails | `src/utils/capital-guardrails.ts`, migration `013_treasury_capital_policy.sql` |
| Member Liquidity Advisor (steady-state rebalancing) | `src/memberAdvisor/*`, migrations `027`, `028`, `032` |
| Treasury push (provisioning + edge-case) | `src/memberLiquidity/*`, migration `026` |
| Loop Out (treasury, edge-case maintenance) | `src/lightning/loop.ts`, `src/lightning/rebalance-loop.ts`, `src/lightning/rebalance-scheduler.ts`, migrations `014`, `015` |
| Expansion engine | `src/api/treasury-expansion.ts`, `src/utils/capital-guardrails.ts` |
| Metrics / net yield | `src/api/treasury.ts`, migrations `007`–`009`, `014` |
| All routes | `src/index.ts` |
| Coinbase Onramp | `app/api/src/api/coinbase-onramp.ts`, `cloudflare-worker/src/index.ts` |

Always include `CLAUDE.md` + `docs/IMPLEMENTATION.md` as base context.

## Hard-Won Gotchas

Things that cost hours to find. Read before debugging in that area.

### General

- **Raw HTTP server, not Express:** `src/index.ts` uses `http.createServer` with an if/else chain. More specific routes (`/api/contacts/sync-peers`) must come before general ones (`/api/contacts`). CORS must list every method used (PATCH/DELETE).
- **`lnd_node_info` is local-only:** It's a singleton storing the local node. For remote peer aliases, use `getNode` from ln-service (gossip graph).
- **Formatting helpers need null guards:** `fmtSats`, `truncPubkey`, `resolveContactName` receive data from API/SQLite that may be undefined. Crashed historically on `pubkey.slice()` without a guard. Always handle falsy inputs. Reuse existing helpers — don't duplicate truncation logic.
- **Sync loop must DELETE stale rows, not just upsert:** `persistChannels()` and `persistPeers()` previously used `INSERT OR REPLACE` only — closed channels stayed `active=1` forever. Now they `DELETE WHERE channel_id NOT IN (current IDs)` after upserting.
- **Umbrel DB requires sudo:** `data/db/` is owned by root. All `sqlite3` commands need `sudo`. Without it, `ls` shows an empty directory.

### Payments

- **Members with direct channels bypass treasury:** LND pathfinding picks cheapest route — a direct member-to-member channel = 0 fees, 1 hop, no forwarding through hub. Treasury earns nothing. Fixed by forcing `outgoing_channel` to the treasury channel in `payInvoice()`. Works because treasury node has no channel to itself → lookup returns null → routes normally.
- **`decodePaymentRequest` is ASYNC and requires `lnd`:** Old type declaration had it sync with only `{request}`. Reading `.tokens` off a Promise gave undefined → "— sats" and `$NaN`. All call sites must use `await decodePaymentRequest({lnd, request})`.
- **`navigator.clipboard.writeText` requires HTTPS or localhost:** Fails silently on plain HTTP (Tailscale IPs). Use `document.execCommand('copy')` fallback with a temporary textarea.
- **`lncli fwdinghistory` defaults to last 24h:** Use `--start_time 0` for full history.
- **`lncli updatechanpolicy` requires `--time_lock_delta`:** Missing this flag errors. Use `--time_lock_delta 40` as default.

### Loop Out

See `docs/LOOP_SETUP.md` for the full gotcha list. Highlights that bite regularly:
- **Prepay is a HOLD not a fee:** ~30k sats returned in the on-chain payment. Net fee = swap + miner only.
- **ACINQ caps in-flight at 45% of capacity:** Need ≥556k channel for 250k minimum swap.
- **Restart cascade:** Restarting LND requires restarting **Bitcorn** (`apps.restart.mutate --appId bitcorn-lightning-node`) — loopd is a service in Bitcorn's own compose, a different Umbrel app from Lightning, so only a Bitcorn restart reaches it. This used to say `--appId lightning-terminal`, which targets an app this stack has not used since v1.18.9 and did not reach loopd even before that. `certExpiry.ts:159-163` states the same model.
- **Channel ID uint64 conversion:** `(block<<40)|(tx<<16)|output` via BigInt; `longs: String` in proto-loader.

### Rebalancing

- **Steady-state rebalancing is member-driven, not treasury-coordinated:** the Member Liquidity Advisor on each member node recommends Loop In (merchant) or Loop Out (farmer) locally; the treasury does not orchestrate steady-state rebalancing. Treasury push and treasury-side Loop Out are reserved for provisioning and edge cases. See `docs/ARCHITECTURE.md` § Liquidity Management.
- **Keysend push ≠ rebalance:** In hub-and-spoke topology with no external peers for circular routes, keysend push permanently transfers sats — it is *not* a rebalancing tool, and is disabled as such. Keysend remains the execution path for *treasury push* (provisioning + edge cases). Keysend enforcement (preflight + 24h skip on rejection) is retained for that path.
- **Role matters:** `channel_role` (merchant/farmer/unknown) is set by the user and controls whether the advisor recommends Loop In, Loop Out, or a channel upgrade. Never auto-classify by balance heuristics.

### Cloudflare Worker

- **Clear KV cache after changing API keys:**
  ```bash
  npx wrangler kv key delete commodity_prices --namespace-id=62c68c41830141cc8b0b6e7cdb193461
  ```
- **Secret format:** paste the raw key / raw PEM from the CDP JSON — do NOT wrap in quotes when piping to `wrangler secret put`.

## Working Style

- Read the relevant doc before making changes — `docs/` is current as of this CLAUDE.md rewrite
- Don't add features, refactor, or "improve" code beyond what was asked
- Don't add speculative error handling for scenarios that can't happen
- When docs drift from code, **update the doc in the same PR** — the reason this file used to be 500 lines was that nobody updated `docs/` and it all piled up here
