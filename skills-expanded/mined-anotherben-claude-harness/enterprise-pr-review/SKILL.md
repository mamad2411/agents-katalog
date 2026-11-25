---
name: enterprise-pr-review
description: "End-to-end PR conversation closer and advisory review harvester for enterprise work. Use this whenever the user mentions unresolved PR conversations, Copilot/GitHub review comments, a PR that cannot merge, skipped/non-blocking Copilot feedback, a failed PR review, or asks to address/resolve/learn from PR feedback. It supports blocking-closeout mode for merge blockers and advisory-harvest mode for valuable non-blocking comments, fixes real bugs with tests, verifies the current head, replies/resolves only where appropriate, and compounds learnings so the same review failure is caught earlier next time."
---

# Enterprise PR Review

## Helpdesk Overlay Bootstrap

When the current git root is a Helpdesk worktree, make the repo-local overlays
available before PR review work:

```bash
node /Users/ben/.codex/skills/enterprise-pr-review/scripts/ensure-helpdesk-overlays.cjs
```

This creates or refreshes `.codex/repo-skills/helpdesk-enterprise-pr-review`,
`.codex/repo-skills/helpdesk-enterprise-stack-review`, and the Helpdesk enterprise
manifest in whichever branch or worktree is active. After it runs, prefer the
repo-local `helpdesk-enterprise-pr-review` overlay for Helpdesk-specific rules.

## Global Precheck

Before reading further, writing artifacts, delegating, or changing files, run:

```bash
enterprise-precheck --skill enterprise-pr-review
```

If it exits non-zero, stop and report stderr verbatim. Do not hand-craft packet files or evidence markers to bypass it.

## Overview

This skill turns PR review feedback into a closed, verified engineering loop. It is not a comment-cleanup skill. Treat every unresolved blocking thread as a possible production bug until current code, tests, CI, and review evidence prove otherwise. Treat non-blocking Copilot/advisory comments as valuable review signal to harvest, classify, and learn from without making them default merge blockers.

Use this when the user says:

- "PR 123 has unresolved conversations"
- "address Copilot comments"
- "cannot merge because conversations are unresolved"
- "learn from this failed PR review"
- "skip Copilot conversations but learn from them"
- "harvest non-blocking Copilot comments"
- "resolve PR feedback"
- "make a harness skill that handles PR conversations"

## Modes

Use exactly one mode per run:

- `blocking-closeout`: for merge-blocking unresolved conversations, requested PR cleanup, or PRs that cannot merge. Blocking threads must be fixed/replied/resolved or explicitly reported as blocked before declaring merge-ready.
- `advisory-harvest`: for Copilot/GitHub comments that are valuable but not blocking after the repo's async-review wait and thread sweep have passed. Advisory comments do not block merge by default, but every useful finding must become one of: immediate fix, tracked follow-up, trap-matrix update, repo gate/script recommendation, contract/plan rule, or skill eval.

Escalate any advisory comment to `blocking-closeout` or an immediate hotfix if it credibly indicates security, data loss, tenant isolation, schema/query correctness, money/order/invoice/inventory corruption, or broken user-visible behavior in the current diff.

## Draft PR Policy

Do not make every PR draft by default. Use this policy:

- `normal`: open PR and keep it open until required gates, async review checks, review-thread state, and any repo-specific pre-merge sweep pass. Do not enable auto-merge by default.
- `high-risk`: draft PR until enterprise review/forge/verify/harness have passed and Copilot has either reviewed the current head or an explicit advisory-harvest follow-up is recorded.
- `draft-default`: only use draft for all PRs if the repo is confirmed to run Copilot review on draft PRs. If that setting is unknown or disabled, draft-by-default can hide the PR from useful review and slow delivery.

High-risk means schema/query/data-sensitive work, tenant/security, money, orders, invoices, inventory, external integrations, destructive writes, authentication, or UI/PDF/file workflows that affect real operators.

If a PR is already open and later becomes high-risk, do not churn the PR state mechanically. Instead, record the risk, run the required gates, request/re-request Copilot review where useful, and route advisory findings through `advisory-harvest`.

## Universal Enterprise Hardening Baseline

- Use the GPT-5.5 fresh baseline: outcome, success criteria, constraints, evidence, and stop rules come before legacy prompt ceremony.
- Green checks are not enough for blocking-closeout. Async review comments can arrive after checks pass, so live blocking thread state is the merge blocker source of truth.
- Non-blocking Copilot/advisory comments are not default merge blockers, but they are not disposable. Harvest them into fixes, follow-ups, traps, gates, contract/plan rules, or evals.
- Never resolve a review thread just because it is outdated, annoying, or probably fine. Reply with evidence first, then resolve only after proof.
- If a thread identifies a real bug class, add or update a regression test before or with the fix. Do not rely on mock-only, migration-only, or diff-only proof for schema/query/data-sensitive changes.
- If the fix touches UI, PDF upload, file upload, preview/download, modal, navigation, rendered output, print labels, or browser behavior, run headless browser proof.
- If the fix touches database shape, tenant isolation, query semantics, money, order, invoice, inventory, integrations, or writes, use current runtime code reads plus live or migrated-integration DB proof where available.
- If the fix touches a query path, including read-only SELECT/report/verifier/
  live-proof code, prove the DB/Query Ownership Packet: owner seam, current
  DB/schema, tenant/owner scope, affected-row or readback semantics, bounded
  proof, cleanup, and redaction.
- If the fix touches a mixed-responsibility file, apply the Touched File SRP
  Assessment from the contract or create a blocking recycle item. Review-thread
  cleanup must not leave the touched responsibility tangled just because the
  thread was narrow.
- If the review comment reveals the final diff drifted from the original user
  intent, update the Intent Continuity Ledger and recycle before claiming the PR
  is ready.
- All verification must be headless. Manual browser or GitHub UI observation is supporting context only.
- If any code, contract, docs, or gate changes are made after review/forge/verify evidence, prior evidence for affected files expires.
- Keep PR review orchestration inside the current harness. Do not route enterprise PR review through external bridge roles.

## Entry Gate

Before doing PR work, the global precheck above must already have passed.

### PR Requirements Snapshot

Before deep work, read `.codex/enterprise-state/hook-ledger/latest-route-card.json`
and state the current PR target in one compact snapshot. Use the route card for
required PR body sections and PR/merge gate names; use live GitHub for the PR
facts:

- PR number/URL, target repository, base branch, head branch, and head SHA.
- Draft policy: `normal`, `high-risk`, or `draft-default`, with the reason.
- Required PR body sections from `route_card.required_pr_body_sections`.
- Async review/thread policy from `route_card.required_pr_gates`, plus required checks, review-ai/Copilot/Claude wait, live unresolved-thread query, and pre-merge sweep.
- Enterprise status: whether review, forge, verify, and `pr-readiness` or merge gate are already satisfied for the current head, or still required.

Then collect the current PR facts:

```bash
gh pr view <PR> --json url,state,isDraft,baseRefName,headRefName,headRefOid,mergeStateStatus,reviewDecision
gh pr checks <PR> --watch=false
```

Use GraphQL or the GitHub review-thread API to list review threads with:

- thread id
- resolved state
- outdated state
- file path and line
- top-level comment database id
- author
- body
- replies

Do not trust the PR page summary or stale transcript memory for unresolved count.

## Deep Think Precheck

Before fixing anything, state a compact precheck:

- Ask: PR number and requested outcome.
- Mode: `blocking-closeout` or `advisory-harvest`, and why.
- Source read: PR metadata, live thread list, current head SHA, changed files, checks.
- Root objective: close review blockers without hiding real bugs.
- Blast radius: changed runtime/doc/test/gate surfaces and required proof.
- Ownership: source-of-truth files/modules/contracts affected by each thread.
- Edge cases: stale/outdated thread, async new review, branch behind base, CI rerun, false positive, docs path deletion, test-only branch, UI/DB surface.
- SRP:
  - `fix-now`: real review findings and missing regression proof.
  - `follow-up`: broader gate improvements not required to unblock the PR.
  - `note-only`: historical comments or unrelated docs.
- Verification: local commands, repo gates, live thread re-query, CI status, head SHA, and merge readiness.

## Workflow

### 1. Snapshot The PR

Record:

- PR URL and number
- base branch, head branch, and head SHA
- current merge state
- all check names and statuses
- changed files against the PR base
- unresolved review threads

If the branch is behind the base, update/rebase first only when safe for the task. If the local workspace is dirty with unrelated files, use or create an isolated worktree.

### 2. Build The Conversation Matrix

Create a matrix with one row per relevant thread or comment:

| Thread/comment | File | Author | Blocking? | Outdated | Classification | Required action | Evidence |
|----------------|------|--------|-----------|----------|----------------|-----------------|----------|

Classify each thread as exactly one:

- `real-bug`: code, test, contract, doc, or gate must change.
- `already-fixed`: current head already addresses it; needs evidence and reply.
- `false-positive`: reviewer is wrong; needs code-grounded explanation and proof.
- `duplicate`: same root cause as another thread; still reply and resolve both after proof.
- `stale-but-valid-learning`: no PR fix needed, but update compound/trap learning.
- `advisory-learning`: non-blocking comment with useful prevention value; track and compound it without resolving/holding merge.
- `blocked`: cannot classify without missing credentials, failing checkout, or unclear branch state.

In `blocking-closeout`, if any blocking thread is `blocked`, stop before resolving anything.

In `advisory-harvest`, do not hold merge for advisory-only comments. Stop only when an advisory comment escalates to a credible P0/P1/P2 correctness risk and the required proof/fix is unavailable.

### 3. Fix Real Findings

For every `real-bug`:

1. Read the current implementation and the consumer path before editing.
2. Trace the root cause and same-class siblings.
3. Add or update a contract/postcondition when the finding reveals a missing invariant.
4. Add a regression test that fails for the bug class.
5. Implement the smallest correct fix.
6. Run the focused test and the relevant repo gate.

Use the PR reviewer trap matrix:

- migration-runner compatibility
- SQL OR/AND precedence, literal wildcard, typed parameter, sargability, and valid falsy input hazards
- SQL tenant/owner/current-database gaps, aliases, latest-versus-earliest semantics, and affected-row checks after repair/update/delete paths
- SELECT-then-INSERT races and retry/idempotence gaps
- stale state-transition metadata and cleanup masking primary errors
- live-test production safety and portable env loading
- mocks that do not match real selected columns or runtime shape
- route catalogs or scenario packs that drift from mounted source paths, HTTP methods, auth boundaries, or consumers
- evidence artifacts that are stale, dry-run-only, wrong-base, missing required fields, string booleans, or not tied to the current PR head
- UI setter plumbing, enum clamp, render escaping, print/PDF/preview parity, layout overflow
- zero/falsy UI values, duplicate React keys, unlabeled controls, and unconditional polling
- duplicate helpers/writers, especially money/date/count/status helpers and DB write/convergence paths
- unowned read/query/report/proof paths that bypass the source-of-truth reader,
  tenant/owner/current-DB scope, bounded query budget, or readback expectation
- touched mixed-responsibility files where the PR fixed a symptom but skipped the
  required SRP/refactor-as-you-touch action
- original intent drift where green tests no longer prove operator acceptance
- unsafe substring environment checks such as `dev`/`staging` matches instead of explicit allowlists
- docs/contracts that cite deleted paths or commands
- original-vs-transformed identity fields

### 4. Verify The Current Head

Verification must run against the current PR head, not an older local commit.

Minimum proof:

```bash
git diff --check <base>..HEAD
node scripts/enterprise-delivery-gate.cjs --base <base> --head HEAD
OPENAI_API_KEY= node scripts/review/local-review.cjs --base <base> --head HEAD --live-db off --fail-on-high --json
```

Also run:

- focused tests named in the conversation fixes
- `review-hard` or local equivalent if available
- live/integration DB proof for schema/query/data-sensitive fixes
- headless browser/E2E proof for UI/PDF/file/rendered-output fixes
- no-new-mock and DB-write ownership gates when relevant
- intent-continuity, touched-file SRP, and DB/query ownership proof when relevant

If any verification fails, fix or report the blocker. Do not reply "fixed" while proof is red or stale.

### 5. Push, Wait, Re-query

After blocking-closeout changes:

1. Commit and push.
2. Re-read PR head SHA.
3. Re-read checks.
4. Re-read review threads.
5. Wait for async blocking review comments if the repo normally posts them after push.

If new review threads appear, loop back to the conversation matrix. Do not merge based on the previous unresolved-thread count.

For advisory-harvest, do not wait indefinitely for slow Copilot comments. Query what exists now, record `harvested_at`, PR head SHA, and remaining async uncertainty, then route each useful comment into fix/follow-up/trap/gate/eval learning.

### 5.25 Last-150 Trap Bank Refresh

When the user asks to learn why PRs fail, update enterprise skills, or harvest review failures across a branch window, build a compact trap bank before changing skills or declaring prevention complete:

- identify the branch/head window and PR set, such as the last 150 commits on `dev`
- count review comments by reviewer and PR, and classify failure classes rather than pasting raw comments
- include CI/check failures from the same window, especially false-green or preflight failures after review/proof refresh commits
- extract prevention targets: plan questions, contract postconditions, build ratchets, review checks, forge lenses, verify/harness commands, repo gates, or skill evals
- prove each accepted trap has a prevention target; `fixed in the PR` is not enough unless a ratchet or upstream rule now catches the class earlier

For Helpdesk-like evidence, seed the trap bank with stale UI/read-model rehydration, config/env/outage semantics, proof-lane selector misses, stale proof-subject/preflight failures, weak assertions, DB/query ownership gaps, integration side-effect/idempotency faults, redaction/diagnostic leaks, and SRP/domain-boundary drift.

### 5.5 Pre-Merge Async Review Sweep

Immediately before any merge command, run the executable sweep from the current repo:

```bash
node /Users/ben/.codex/skills/enterprise-pr-review/scripts/pre-merge-review-sweep.cjs <PR>
```

This is a hard stop, especially after green checks. Do not merge if it reports:

- any pending/running check
- any failed check
- missing async review checks
- pending `review-ai`, `review-hard`, `claude`, Copilot, or equivalent review checks
- any unresolved review thread, including outdated-looking threads

If the sweep blocks, return to the conversation matrix. Reply with evidence and resolve only after the current-head fix or proof is green, then rerun the sweep.

### 6. Reply And Resolve

For each thread, reply with:

- commit SHA or "current head"
- what changed or why no change was needed
- exact regression test or command proof
- any remaining limitation

Then resolve the thread only when:

- the reply is posted
- the fix/evidence applies to the current PR head
- the relevant local proof is green
- the thread was re-read and is still the same blocker

Never resolve without a reply unless the user explicitly asks for administrative cleanup and there is no engineering content.

### 7. Final Merge Readiness Gate

Before saying a blocking-closeout PR is clean:

- `pre-merge-review-sweep.cjs <PR>` passed after the latest push
- live unresolved blocking thread count is 0
- latest head SHA matches the verified local head or verified remote head
- all required checks are passing
- review-hard / review-ai status is understood
- branch is not behind base
- PR body gate requirements are satisfied
- no unrelated dirty changes were included

If merge is requested, use the repository's allowed merge strategy. If squash and merge commits are disallowed, try rebase merge. Never push directly to protected `main`.

For advisory-harvest, final readiness means every harvested advisory comment is classified and routed. The report must not claim advisory threads are resolved unless they actually were; it should say `advisory harvested` and list any follow-ups opened or recommended.

### 8. Compound The Learning

After the PR is clean or merged, capture what the review taught:

- reviewer finding
- missed prevention point
- root cause
- fix pattern
- regression proof
- whether the trap should become a contract, plan, forge, verify, or deterministic gate check
- whether the miss was an intent-continuity, touched-file SRP/refactor, or
  DB/query ownership failure that should become a skill eval or gate

If the finding class can be detected mechanically, recommend or implement a trap-matrix/gate update. If it changes skill behavior, update the relevant enterprise skill or create an eval for skill-creator.

For advisory-harvest, compound is the main output. The run is incomplete until every useful advisory comment has a prevention disposition: `implemented`, `tracked-follow-up`, `gate-recommended`, `eval-added`, or `blocked-with-reason`.

## Review Feedback Harvester Hard Gate

For blocking-closeout, the run is also incomplete until every accepted P1/P2/P3 finding has exactly one prevention target: plan question, contract postcondition, build authority scan, review check, forge lens, verify command, CI/gate recommendation, repo trap, or skill eval. Do not treat "fixed in this PR" as prevention unless the upstream rule or deterministic proof path was also updated or explicitly tracked.

For branch-window retrospectives, the run is incomplete until the trap bank has both an old-skill/baseline verdict and a new-skill verdict for the accepted eval cases, or a clear blocker explaining why model-based A/B could not be run and what deterministic proof was used instead.

## Output Format

Use this final report:

```markdown
## PR Review Closeout

Mode: blocking-closeout | advisory-harvest
PR: #<number> — <url>
Head verified: <sha>
Blocking unresolved threads: <count>
Advisory comments harvested: <count>
Checks: <pass/fail summary>

Fixed:
- <thread/file>: <root cause> -> <fix> -> <proof>

Resolved:
- <thread id>: <reply evidence>

Learned:
- <what should be caught earlier next time>

Routed advisory:
- <comment id/file>: <classification> -> <fix/follow-up/trap/gate/eval>

Remaining risk:
- <none or concrete blocker>
```

Keep the user-facing version short unless they ask for the full matrix.

## Stop Rules

Stop and report clearly if:

- PR number or repository cannot be determined.
- GitHub review thread API is unavailable.
- The branch has unrelated dirty changes that would mix into the PR.
- A real finding needs credentials, live DB, or browser proof that is unavailable.
- CI fails on an unrelated pre-existing blocker and the user has not asked to fix that broader issue.
- In blocking-closeout, new review comments keep arriving faster than they can be fixed.
- In advisory-harvest, an advisory comment escalates to credible security, data-loss, tenant, schema/query, money/order/invoice/inventory, or user-visible correctness risk and cannot be proven safe.
