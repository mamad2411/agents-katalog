---
name: bug-factory
description: >-
  Standard rigorous multi-agent pipeline for bugs and build tasks that "must be workflowed".
  Engage when the user says "workflow this", "must be workflowed", "run the bug factory",
  "process the open bugs", "sweep and fix the bugs", or flags a build/bug task for the full
  pipeline. Sweeps open issues tagged `bug` (closes already-resolved ones), then runs each
  surviving bug through: confirm to plan/zoom-out/blast-radius convergence loop (fresh eyes) to
  build (one agent per file) to test to review (blast-radius + patch-or-fix + zoom-out) to
  verify (computer-use + Chrome on the local Cortex instance, explicit demonstrative proof) to
  ship (PR to dev, babysit, test on dev, PR to main, babysit, confirm on main). One agent = one
  job. Proof-or-STFU. The main merge is the only human-gated step.
metadata:
  type: skill
---

# bug-factory

A standard, repeatable, **separation-of-duties** pipeline for bugs/build tasks. The orchestrator (main loop) **only** sweeps, sets up isolation, runs deterministic gates, integrates verified results, babysits CI, and escalates the `main` merge. Every unit of real work is a **separate single-job agent**.

## THE ONE RULE
**One agent, one job.** The jobs are: *confirm, plan, zoom-out, blast-radius, build (one per file), test, review, verify*. No agent ever performs two of these. No agent works on two different bugs. A builder never tests or reviews its own build. A planner never approves its own plan. Always fresh eyes.

## Engage
Triggered by: `/bug-factory`, or the user saying a task "must be workflowed" / "workflow this" / "run the bug factory" / "process the open bugs". Also the standing pipeline for any build/bug task the user flags for workflowing.

---

## PHASE 0 — Intake & resolved-sweep
1. **List open bugs.** `gh issue list --label bug --state open --json number,title,body,url --limit 200`. (Also vault bugs if in scope: `mcp__vault-index__list_vault(project, type="bug", status="open")`.)
2. **Sweep for resolved (one CONFIRM agent per bug, parallel).** Each agent independently checks: is this still reproducing on current `dev`/`main`? Is the fix already merged (grep the code/commits)? Has the error stopped in monitoring? If **resolved** → close the issue with an evidence comment (`gh issue close <n> --comment "Resolved: <evidence — commit/behaviour/monitoring>"`). If **still open** → it enters the worklist. Never close without pasted evidence.
3. Output: the confirmed-open worklist.

---

## PER-BUG PIPELINE (each stage a DIFFERENT agent)

### 1. CONFIRM
Reproduce the bug; produce concrete evidence it is real (failing test, log signature, DB state, repro steps). If not reproducible → bounce back to sweep and close as not-reproducible **with evidence**.

### 2. PLAN ⟲ ZOOM-OUT ⟲ BLAST-RADIUS convergence loop
Repeat until **zero open concerns**, then **one extra clean pass with brand-new agents** (fresh eyes) that must also find nothing:
- **plan** agent — design the minimal fix.
- **zoom-out** agent — map the area in plain language; correct any hallucinated symbol names (verify by grep).
- **blast-radius** agent — trace downstream callers/tests/SQL/tenant/siblings. **MANDATORY: validate the plan against the LIVE LOCAL DB for schema drift, with pasted evidence** (`psql "$TEST_DATABASE_URL" -c "\d <table>"`, real sample queries, constraint/index checks). Migrations & schema files are contract-truth; the live DB is runtime-truth — reconcile both.
- If **any** concern is unresolved → a **new** plan agent refines, then re-run zoom-out + blast-radius with **fresh** agents. Loop. Resolving concerns ALWAYS triggers a fresh re-run — never self-certify a resolution.
- Convergence = a full plan→zoom-out→blast-radius pass with fresh agents that surfaces no new concern. Lock the plan.

### 3. BUILD — one agent per file
Take the locked plan's file list. Dispatch **one build agent per touched file** (a builder touches exactly one file). Builders share the bug's isolated worktree and run **sequentially** (file N+1 builder sees file N's commit) to keep the multi-file change coherent; each commits only its file by explicit path. TDD: the RED test is authored first (its own build-of-a-test job). No production code without a failing test. Each builder re-reads its own file-diff against the plan before handing off.

### 4. TEST — separate agent
Independently run the relevant unit + integration suites **against the live DB**, pasted proof. Confirms the bug behaviour is fixed and nothing in the touched modules regressed. Distinguish pre-existing failures (prove identical on the parent commit).

### 5. REVIEW — separate agent, MUST include three lenses
On the built diff, run: **blast-radius** (completeness — missed callers/siblings), **patch-or-fix** (root-cause vs symptom — reject band-aids), and **zoom-out** (does it fit the architecture). Any HIGH finding bounces back to the plan loop (Phase 2) with fresh eyes.

### 6. VERIFY — separate agent. Surface decides the method (HARD RULE):
- **UI surface** (`apps/admin/**` or `apps/api/src/routes/**` with a UI flow) → **real browser** (Chrome via Playwright/computer-use) against the local Cortex instance (pm2 `helpdesk-local-*`, admin `http://localhost:5173`, api `http://localhost:3000`). Drive the actual user flow; capture screenshots/DOM before→after.
- **Shopify integration** (services/shopify*, gift-card/voucher) → a **real dev-Shopify canary** — an actual call to the **dev Shopify store** demonstrating the fixed behaviour (capture the real request + response). NOT a mocked unit test.
- **REX integration** (services/retailExpress/, rex* clients, SOAP) → a **real dev-REX canary** — an actual **dev REX** call (capture the real response). NOT a mock.
- **Any other API / script / backend** → a **real live-dev canary** — exercise the live dev runtime/DB (e.g. run the job/script against the dev DB and capture output). NOT unit/mocked tests + an app smoke alone.

Proof must be explicit & demonstrative, e.g.:
> "Fix `<change>` resolved bug `#<n>`: before, `<real call/flow>` produced `<broken result>` (captured); after, the same `<real call/flow>` produces `<correct result>` (captured before+after)."

**REJECTED:** "seems to work" / "should be fine" / no artifact / unreplaced `behaviour Y` placeholders / angle-bracket `<...>` markup / **mocked tests standing in for a live canary**. A green unit test is necessary but NOT sufficient — the verify gate requires the real browser run (UI) or the real dev Shopify/REX/dev-DB canary (API/scripts). Enforced by `verify-proof-gate.cjs`.

### 7. SHIP
0. **VERIFY-PROOF GATE (HARD — runs before the dev PR exists).** The Verify phase (step 6) must have written `docs/verify/<slug>-browser-proof.md`. Run:
   `node ~/.claude/skills/bug-factory/verify-proof-gate.cjs --proof docs/verify/<slug>-browser-proof.md --diff-base origin/dev --repo <worktree>`
   If it exits non-zero → **STOP, do NOT create the dev PR.** It blocks when the proof is missing, thin, non-demonstrative ("seems to work"), or — for `apps/admin/**`/`apps/api/src/routes/**` diffs — lacks a real browser-run (Playwright/Chrome on localhost:5173). This closes the "rely on the orchestrator to remember" hole. (Optional team-wide: add this to `scripts/review/pre-push-gate.cjs` so it gates *every* contributor's dev PR — but that's a repo-wide change; do it only on explicit request.)
1. **PR → dev** — narrow diff (only the fix), correct **5-header body** (`## What changed` / `## Regression check` / `## Blast radius` / `## Edge cases` / `## Conversations addressed`), substance receipt generated, all gates green. Never `--no-verify`.
   **CI gates are satisfied UP FRONT, not discovered (learned 2026-06-09/10, ~5 wasted cycles):**
   - **No new mocked-DB tests** for schema-coupled files (`ensureNoNewMockTests.cjs` push-block) → live `.live.test.js` from the RED phase.
   - **Live-proof registry**: every DB-backed source file changed needs a `scripts/review/live-proof-registry.cjs` REGISTRY entry (pattern + live-proof command) or required `review-hard` fails ("Live DB proof registry gap"). The registry `command` must require `TEST_DATABASE_URL` and **never promote `DATABASE_URL`** into it (mutable-DDL safety — bots flag the promotion P1); CI sets `TEST_DATABASE_URL` directly, so copy a sibling entry's `test -n "$TEST_DATABASE_URL"` fail-closed shape. The `pattern` must match EVERY file the proof covers (incl. the test files), else a PR touching only those silently skips the lane.
   - **DB-proof body line is a strict regex** (`enterprise-delivery-gate`, `~/scripts/enterprise-delivery-gate.cjs`): the `## Regression check` section MUST contain a line shaped `Real DB/schema proof: <cmd> - PASS` — colon **immediately** after "proof", and a plain ` - PASS`/` - FAIL` (NO bold `**PASS**`, NO `(parenthetical)` between "proof" and the colon). **main's gate is STRICTER than dev's** — the identical body can pass on dev and fail on main. Marking it "Not run / N/A" is rejected when DB/schema/registry files changed (incident-response label does NOT waive this content rule).
   - **Code Placement Law** (`domain-only-new-code` ratchet): NEVER add a NEW runtime file under `apps/api/src/services/` — it fails the frozen-baseline ratchet (`legacyServiceFiles may only shrink`). Put shared helpers under `apps/api/src/scripts/**` (exempt prefix) or a `domains/**` home, and update consumer imports. Also the **SRP cohort ratchet** fails any file crossing **400 lines** without an evidence-quality `srp_justification` — keep new/edited files under 400 or extract helpers.
   - **Purchasing full-kit**: any `apps/api/src/domains/purchasing/**` diff requires the full-kit artifact re-subjected to HEAD (freshness refresh: re-prove PC-LIVE-DB live via `purchasing-cert-env.sh`, update `docs/verify/2026-05-02-purchasing-dev-full-kit-closeout-artifact.json`+md; recipe `git show 67ab6381e`). This MUST be the **last commit before push** — any code commit after the proof subject re-fails it.
   - **Receipts are per-SHA**: regenerate the substance receipt after every rebase/commit, before push.
   - **Batch into ONE push**: every push restarts Copilot re-review + the quiet period and invites new bot threads — never push a comment-tweak alone.
2. **Babysit dev PR to green** — when a bot (Copilot/codex/cursor) opens a thread, dispatch a **separate fix agent** (its own job) + tester, then reply substantively and resolve each thread individually (no bulk-resolve).
   - **CODEX REVIEW IS MANDATORY (user rule 2026-06-10):** do not merge until `chatgpt-codex-connector` has reviewed the current head. If absent, trigger it (`gh pr comment <n> --body "@codex review"`) and wait. Copilot alone does not satisfy this.
   - `copilot-review-wait` passes only when: **all blocking checks green (it treats `preflight-dev` as blocking even though preflight isn't a required context)** + zero unresolved threads + ~300s quiet. After resolving threads with NO new push, **`gh run rerun` the gate** — it does not self-retrigger. ALL duplicate runs of the gate must conclude (one stuck `in_progress` run blocks merge).
   - **Theoretical/incorrect findings**: resolve with a substantive evidence-backed reply, NO new commit (a commit restarts the whole bot cycle). For **code-issue / reply-required threads**, `copilot-review-wait` requires a substantive **human reply as the LAST comment before resolution**. The reply-required authors (`REVIEW_WAIT_REPLY_REQUIRED_AUTHORS`, default **`chatgpt-codex-connector` + `copilot-pull-request-reviewer`**; CI also pulls in **`coderabbitai`** code-issue threads) **all** behave this way, and **any** of them frequently **re-acks after your reply — becoming the last commenter and re-blocking the gate**; reply once more so the human has the last word, confirm no bot re-ack landed, then re-run the gate. (Cursor is NOT a reply-required reviewer — its distinct hazard is pushing its own commits; see below.)
   - **Gates read the PR body from the *event payload*, not the live API.** A body-only edit is SKIPPED by the gate `if` (`github.event.action == 'edited'`), and `gh run rerun` **replays the stale body**. So after editing the PR body to satisfy a gate (e.g. fixing the DB-proof line), `gh pr close && gh pr reopen` (or push a commit) to re-fire `preflight-*`/`enterprise-delivery-gate` with the current body.
   - **Bot agents (Cursor) push their own commits to the branch**: never trust them — vet with an independent reviewer + tester before building on top; tighten weak guards (bots favor plausible-but-loose checks); expect the race and keep your local work rebased on origin.
   - **dev moves in bursts + strict up-to-date**: rebase onto origin/dev immediately after a burst, then run a **self-merging poll** that merges the instant mergeState=CLEAN (a human-paced merge loses the race).
3. **Test on dev** — after merge, confirm the fix on the dev deploy (monitoring signature gone / behaviour correct), explicit evidence.
4. **PR → main** — cherry-pick narrow to `main`. Split any dev→main PR >100 files / >5,000 lines. Never squash.
5. **Babysit main PR to green.**
6. **Confirm on main** — post-deploy, verify the behaviour/monitoring on production.
7. **TEARDOWN (MANDATORY — do not skip).** Once the fix is confirmed merged (dev, or main when promoted), remove this bug's worktree so it does not accumulate (memory: `worktree-accumulation` — hundreds of stale worktrees filled the disk to 100% twice). The remote branch auto-deletes on merge (`delete_branch_on_merge:true`); you must clean the **local** worktree + branch:
   `~/.claude/scripts/cleanup-merged-worktrees.sh --repo <repo-main> --scope session --current .claude/worktrees/<slug> --apply` — it patch-backs any stray uncommitted change, then removes; it **refuses to remove anything not actually merged**, so if the ship was abandoned (unmerged) the worktree is left intact. Never force-discard unmerged work.
- **The actual `main` merge is the single human-gated step** — prepare it green-and-mergeable and hand it to the user unless they have explicitly authorised the main merge.

---

## HARD RULES (enforced every run)
- One agent, one job; one bug per agent; one file per build agent.
- Plans converge via plan→zoom-out→blast-radius; resolving a concern always re-runs with fresh agents; +1 clean pass before lock.
- All planning is validated against the **live local DB for schema drift, with evidence**.
- Review **must** include blast-radius + patch-or-fix + zoom-out. Run **patch-or-fix to a clean FIX verdict, not just once** — a PARTIAL/PATCH verdict means a gap remains: its ownership/single-owner check catches sibling code paths sharing the same defect (e.g. a second migration runner reached via `db:migrate`). Close the gap and re-verify until FIX. Loop an **independent high-rigor review** between fixes (Claude Code: `/code-review` xhigh; codex/cursor or any driver: the equivalent review pass / a fresh reviewer sub-agent) — the review tool is driver-specific but **patch-or-fix is the driver-agnostic exit gate**: do not ship until it returns FIX.
- Verify is **surface-gated (HARD)**: UI → real browser (Chrome) flow; Shopify/REX → real **dev Shopify / dev REX canary**; other API/scripts → real **live-dev canary** (dev DB/runtime). Mocked tests are necessary but **never sufficient** for the verify gate. Explicit demonstrative proof only (never "seems to work").
- Ship dev→main with babysitting at every gate; confirm on dev and on main.
- **Clean up after merge** — every shipped bug ends with SHIP step 7 teardown (remove the merged worktree + local branch via `cleanup-merged-worktrees.sh`). A run is not "done" while its merged worktree still sits on disk.
- **Proof-or-STFU** — pasted evidence only; stale evidence after any git op is void.

## REPO MECHANICS (helpdesk)
- **Isolation:** one git worktree per bug off `origin/dev` (`git worktree add -b fix/<slug> .claude/worktrees/<slug> origin/dev`). Symlink `node_modules` from the main checkout into the worktree (root + apps/api + apps/admin + packages/shared) — fresh worktrees lack them. **Tear it down at SHIP step 7 once merged** — the worktree is created per-bug and must not outlive the merge.
- **DB:** tests/schema-checks use `TEST_DATABASE_URL` from the **repo-root `.env`** (the Render dev DB). NOT `apps/api/.env` (that points at a drifted local `cortex_local`). See `reference_db_env_files_gotcha`.
- **Local Cortex instance for verify:** pm2 `helpdesk-local-api` (:3000), `helpdesk-local-admin` (:5173), `helpdesk-local-browser-worker`; DB `helpdesk_dev_local_linked`; Playwright config `apps/admin/playwright.config.js`. If the env is occupied/on another branch, deploy the fix branch carefully and **restore** it after, or use an isolated instance — never leave the shared env broken.
- **PR gates:** `enterprise-delivery-gate` requires the 5 H2 headers (see `reference_pr_body_schema`); pre-push needs a substance receipt (`node scripts/review/pr-readiness-substance-check.cjs --base origin/dev --head <sha>`) and `TEST_DATABASE_URL` set for live-proof; `copilot-review-wait` blocks on unresolved bot threads + a ~5-min quiet period.
- **Subagent limits:** subagents have no MCP and the Read tool is blocked on source files >50 lines — they must use `sed`/`grep`/`git` and edit via Edit (small files) or `perl`/`git apply` (large). Pre-feed code or let them self-serve via shell.
- **Pin unpushed work by SHA:** when a later-stage agent must operate on an UNPUSHED commit, its prompt must pin the exact SHA (`git reset --hard <sha>`, verify `git rev-parse HEAD`) and explicitly FORBID `git fetch`/`reset to origin` — the reflexive fetch+reset discards unpushed commits silently (cost 2 cycles on 2026-06-10; recovery is `git reflog`). Orchestrator verifies the commit chain (`git log --oneline -3`) before pushing.
- **Forbidden auto-fix:** concurrency/locks (e.g. `withProductPriceLock` / 55P03) → escalate, never auto-fix.

## ORCHESTRATION
Run the agent-heavy phases (confirm, plan-loop, build, test, review) via the companion Workflow `bug-factory/per-bug-pipeline.workflow.js` (pass the bug worklist as `args`). The orchestrator does Phase 0 sweep, workspace setup, the **verify (browser)** step, and **ship/babysit/main-escalation** between/after Workflow runs — these span time and human gates and cannot live inside a single Workflow run. Scale agent count to bug count; token cost is not the constraint, correctness and proof are.
