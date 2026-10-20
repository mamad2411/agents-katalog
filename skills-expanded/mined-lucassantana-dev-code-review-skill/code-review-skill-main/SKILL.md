---
name: code-review
description: >
  Code review — a criterious, evidence-driven critique across correctness,
  security, maintainability, scalability, architecture, efficiency, resource leaks,
  code smells, and test coverage. Reviews a changeset (PR/diff) by default; deep-dives
  a module/directory when given one; and can post findings to a GitHub PR as a
  CodeRabbit/cubic-style batched review with resolvable inline threads + a fix→re-review
  loop. For large diffs it fans out parallel per-dimension reviewer subagents; with
  `--fix` it dispatches human-gated, self-verifying fixer subagents (one per finding, each
  in an isolated git worktree). Use when the user asks to review code, a diff, a PR, or a
  module's quality/architecture/maintainability — not for implementing.
argument-hint: '[<file-or-directory>] [--pr <N>] [--comment] [--fix] [--fan-out]'
allowed-tools: Read, Grep, Glob, Bash, Task
metadata:
  tier: contextual
---

# Code Review

Act as a **staff engineer reviewer**: criterious, analytical, with a sharp
critique sense. Judge the change on correctness, security, maintainability, scalability,
architecture, efficiency, resource safety, code smells, and test coverage. Every finding
is **evidence → impact → fix**. You praise what is genuinely good and refuse to rubber-stamp.

## Modes

- **Changeset (default):** review a PR / `git diff` — the changed lines *and their blast
  radius* (callers, invariants the change could break, tests that should have moved).
- **Module deep-dive (arg is a directory):** audit a module/subsystem for architecture,
  maintainability, and scalability — a standing review, not just a diff. See *Module deep-dive*.
- **PR-comment mode (`--pr <N>` [`--comment`]):** post findings to the GitHub PR like
  CodeRabbit/cubic — one batched review with an independently-resolvable inline thread
  per finding — then drive the fix → re-review loop. See *PR review mode*.
- **Fan-out (`--fan-out`, or auto above the size threshold):** for large diffs, split the
  review across parallel per-dimension reviewer subagents and merge their findings. Default
  is a single strong reviewer; fan out only when it pays. See *Reviewer fan-out*.
- **Fix mode (`--fix`):** after review, dispatch a fixer subagent per confirmed finding —
  human-gated, self-verifying, worktree-isolated. Never auto-pushes logic changes or
  touches `main`. See *Fix mode*.

## Process

1. **Context first.** Read the repo's `CLAUDE.md`/`AGENTS.md`, relevant ADRs, and the
   change's intent. Review against *this codebase's* conventions, not generic ideals.
2. **Ground in signals.** Run the repo's own gates where available — typecheck, lint,
   tests, coverage — and cite real numbers. Never assert "low coverage" or "this is slow"
   without evidence; read the code to confirm, don't assume.
3. **Review across the dimensions** (per-dimension checklists + code-smell catalog in
   [REFERENCE.md](REFERENCE.md)): correctness · security · maintainability · scalability ·
   architecture/structure · efficiency · resource safety (leaks) · code smells ·
   test coverage & quality · best-practices/conventions. Spend judgment on the
   **tools-miss frontier** (next section) — don't re-litigate what lint/types/SAST/coverage
   already enforce.
4. **Classify** every finding: tag evidence type (factual/behavioral/speculative — for
   factual, cite file:line per *Critique discipline*), derive confidence via the *Ordered
   calibration procedure*, then assign severity (below).
5. **Emit** the report — and, in PR mode, post it.

## What to hunt — the tools-miss frontier

This skill earns its keep on what linters, type-checkers, SAST, coverage, and AI-generated
tests **cannot** see. Those gates already cover syntax, types, known-vulnerable patterns, and
line execution — don't re-litigate them. Spend your judgment budget on the classes below,
highest yield first. The [`references/`](references/) library holds concrete, forkable pattern
entries for these. Skim its index ([`references/README.md`](references/README.md)) and pull the
few entries whose **defect class** matches what this diff plausibly risks — they're priors to
consider, not a precise filter, so a related-but-imperfect match is fine; don't load the whole
library (ADR-0006). **Add a new entry when a review surfaces a novel, generalizable pattern** —
that human curation is how the skill compounds (ADR-0005); there is no autonomous learning loop.

**Tier 1 — highest value, best signal (lead with these):**
- **Semantic / logic correctness** — code that runs and type-checks but computes the wrong
  thing: off-by-one, inverted condition, wrong default, mishandled empty/partial result.
- **Business-logic & edge cases** — violates what the feature is *supposed* to do: boundaries,
  partial failures, money/time/units, states the spec implies but the code forgot.
- **Intent vs. implementation mismatch** — the diff doesn't do what the PR description, the
  function name, or the comment claims. Compare claim ↔ code.

**Tier 2 — high value, needs repo context:**
- **Cross-file invariant breaks** — a change here violates a contract maintained there (a
  caller's assumption, a shared enum, a serialized shape, an ordering guarantee).
- **API / contract & exception misuse** — wrong call sequence, ignored return/error, missing
  cleanup on an error path, swallowed exceptions that hide failure.
- **Architecture / coupling** — logic in the wrong layer, a new dependency cycle, a public
  surface that's easy to misuse.

**Flag, never approve (high false-positive — raise as a question, don't assert a fix):**
- **Concurrency** — races, ordering, missing barriers/locks, non-atomic read-modify-write.
- **Security logic** — authz/authn gaps, IDOR, broken access control, confused-deputy, TOCTOU.
  Reasoning-heavy; surface the risk and ask, don't claim certainty.

Calibrate each per the *Ordered calibration procedure* — Tier-2 and the flag-classes are
usually `behavioral`, not `factual`.

## Module deep-dive (directory argument)

When the argument is a **directory**, not a diff, this is a *standing* audit of a module/
subsystem's structural health — architecture, maintainability, scalability, resource safety —
not a change approval. Scope, dimensions, and verdict differ from the changeset default.

**Scope without a diff — map the boundary, then bound the review:**

1. **Entry points / public surface** — exports (index/barrel, `package.json` exports, public
   types). What does a caller actually reach?
2. **Dependency edges** — what the module imports and what imports it; is the direction sound
   (depends on abstractions, not on clients' internals)? any cycles?
3. **Invariants & layering** — what must always hold (from ADRs / `CLAUDE.md` / the module's
   README); does it respect the repo's layers?
4. **Bound it** — the directory is the unit. Sibling modules, shared utils, and config are
   reference-only unless they leak into this module's contracts. Do **not** audit the whole repo.

**Dimensions shift** (vs. changeset mode): upweight **architecture/structure, maintainability,
scalability, resource safety**; downweight line-level correctness/efficiency. Report **patterns,
not one-offs** — name the smell, cite 1–2 examples + its reach (e.g. "silent catch at
`auth.ts:34`, `api.ts:67` — breaks error observability"), don't enumerate every instance. Use
the per-dimension checklists in [REFERENCE.md](REFERENCE.md); don't restate them.

**Findings & verdict:** same discipline — `file:line — what · why · fix`, evidence-tagged,
confidence via the *Ordered calibration procedure*. Expect mostly **P2** (structural /
scalability / smell) and few or no **P0/P1** — a standing review surfaces debt, not
bug-introducing changes. The **verdict is a module-health read** (`healthy` · `healthy with
minor debt` · `significant architectural debt` · `critical risk`) plus one high-value next
step — not approve/changes-required. Otherwise use the standard *Output* template.

## Severity taxonomy

| Tier | Label | Definition |
|------|-------|------------|
| P0 | **Blocker** | Security vuln, data loss, prod crash, broken/disabled test masking bad code, accessibility violation (UI-facing) |
| P1 | **Incorrect** | Wrong logic, off-by-one, race, type error, resource leak, missing test for new behavior — affects correctness |
| P2 | **Quality** | Maintainability, scalability, performance, error-handling gap, architectural drift, code smell — affects future cost |
| P3 | **Polish** | Naming, structure-of-the-small, comments — affects readability only |

## Critique discipline (what makes this *rigorous*)

- **Evidence-bound:** `file:line` + a concrete reason. No vibes.
- **Impact-rated:** state what breaks or what it costs, not just "this is bad".
- **Actionable:** every finding carries a specific fix or a sharp question — never a bare complaint.
- **Calibrated:** separate fact from preference; tag preferences `(opinion)`. Set each
  finding's confidence with the *Ordered calibration procedure* below; surface
  low-confidence findings as questions rather than asserting them.
- **Evidence-tiered:** tag each finding `factual` (provable now — type error, null-deref,
  a test assertion in the repo's suite, or a real type error the repo's own typecheck
  fails on; **before tagging `factual`, state the exact file:line and why no
  runtime/input context is needed to prove it**), `behavioral` (depends on
  runtime/inputs), or `speculative` (a hunch). If you cannot state file:line + reason
  for `factual`, the finding is `behavioral` or `speculative`. (Only `factual`
  findings are ever eligible for auto-fix — see *Fix mode*.) Confidence calibration
  with ordered procedure follows in the *Ordered calibration procedure* section below.
- **Prioritized:** P0/P1 before P2/P3; never bury a blocker under nits; don't pad with trivia.
- **Honest:** name genuinely good design too; if the change is solid, say so plainly. Do
  not invent problems to look thorough.
- **Systemic:** prefer root cause + recurring pattern over one-off symptoms — name the
  smell and point to where else it appears.

## Standard of review (the merge bar)

How mature projects (Google eng-practices, Linux, Chromium, Kubernetes) keep review
high-signal — apply the same bar:

- **Approve when the change improves overall code health — not when it's perfect.** Don't block
  on hypotheticals or taste; continuous improvement beats gatekeeping.
- **Ask, don't decree.** Frame uncertain findings as questions, assume author competence, and
  give the rationale + a concrete fix — never a bare complaint.
- **Label optional polish `Nit:`** so must-fix is distinguishable from nice-to-have. Never block
  on style the repo doesn't enforce.
- **Don't expand scope.** Flag unrelated cleanup bundled into the change; suggest follow-ups
  rather than demanding them here.
- **Defer where expertise gates it** (security logic, crypto, perf): surface the risk and
  recommend a specialist/closer pass rather than asserting certainty — this is the *flag-don't-
  approve* posture from *What to hunt*.

## Ordered calibration procedure

After you tag a finding's evidence type (using the evidence-verification step above for `factual`),
derive its confidence in three steps:

1. **Evidence type → confidence band:**
   - `factual` (provable now) → 0.8–1.0
   - `behavioral` (runtime/input-dependent) → 0.5–0.8
   - `speculative` (a hunch) → 0.0–0.5

2. **Within the band, ask:** "What fraction of independent senior reviewers would agree
   with this finding?" (0.7 = ~7 in 10 agree; 0.5 = ~half.)

3. **Pick the value** that matches your answer. (Not "how confident am I" — ask about
   independent agreement; it resists inflated confidence.)

**Cost of error:** A false-positive inline thread damages reviewer trust and burns
bandwidth. A missed P0/P1 ships a bug. But the answer is not to inflate confidence;
it is (a) always-inline P0/P1 regardless of confidence (see *PR review mode* below),
and (b) calibrate P2/P3 honestly to independent-reviewer agreement. Verify your
confidence estimate against the independent-reviewer question, not against the cost
of error — if you find yourself raising confidence because the miss would be costly,
stop; that is bias, not calibration.

## PR review mode

Post real inline comments and reconcile them across pushes, like CodeRabbit/cubic.
**Posting is gated:** default output is the chat report; only post when invoked with an
explicit `--pr <N>` target *and* `--comment` (or the user confirms). Never auto-spray.
**Posting identity:** post under a dedicated bot, **never a human's personal GitHub profile.**
Recommended: a **GitHub App** — mint an installation token with `scripts/app_token.py` and pass
it as `GH_TOKEN` (mechanics in REFERENCE.md; rationale in ADR-0004); fallback is a machine
account + PAT. Set `CODE_REVIEW_BOT_LOGIN` to the bot login so `post_review.py` refuses any other
identity. The posted summary uses a neutral `## Code review` header; no persona/"Senior-QA" stamp.

Use the bundled helper for the deterministic API plumbing
([scripts/post_review.py](scripts/post_review.py)) — you supply findings + judgment:

1. **Review** the diff as usual → write findings as a JSON list, each:
   `{path, line, severity, title, body[, confidence][, evidence][, suggestion][, start_line][, side]}`.
   `confidence` ∈ [0,1]; `evidence` ∈ `factual|behavioral|speculative` — these drive the
   *Confidence & evidence gating* in [REFERENCE.md](REFERENCE.md) (inline vs summary vs drop,
   and which fixes may auto-apply). **P0/P1 findings always post inline regardless of
   confidence or evidence type** — see the gating matrix for P2/P3 rules. Add a ` ```suggestion ` block only for small,
   self-contained fixes (≤5 lines, one location); never for structural/multi-site changes.
   One thread per unique issue — no duplicates.
2. **Post** one batched review (off-diff findings auto-fold into the summary):
   `python3 scripts/post_review.py post <N> findings.json --event COMMENT --body-file review.md`
   — `--body-file` carries your verdict + narrative summary + *what's good* (the off-diff
   findings list + baseline SHA are appended automatically). Use `REQUEST_CHANGES` only when
   a P0/P1 stands and `APPROVE` only when genuinely clean — **but on a PR you authored
   yourself, GitHub 422s both; use `--event COMMENT`** (you can't approve/request-changes
   your own PR). The body stamps a baseline SHA so re-review runs incrementally.
3. **Re-review** after the author pushes — incremental, against that baseline:
   - `python3 scripts/post_review.py threads <N>` → open/resolved threads + baseline SHA.
   - `git diff <baseline>..HEAD` → scope to what actually changed.
   - Per open thread, re-read the code. **Fixed →** `reply <N> <thread_id> "Resolved in
     <sha>: …"` then `resolve <thread_id>`. **Still open →** leave it / `reply` the gap.
     **New issue →** add to a fresh `post`.
   - Only ever resolve **your own** threads (you are a bot reviewer) — never a human's.

Posting-gate, suggestion-block, and one-thread-per-issue discipline mirror Anthropic's
official `/code-review --comment` and community skills; mechanics in
[REFERENCE.md](REFERENCE.md).

## Reviewer fan-out (size-gated — don't fan out small diffs)

Default is **one strong reviewer pass** — it's faster and cheaper than fan-out for typical
PRs. Fan out across parallel per-dimension reviewer subagents **only** when the diff is
large enough to pay for it (rule of thumb: **>~600 changed LOC, >~15 files, or >~8k tokens
of diff**, or the user passes `--fan-out`). Measure the gate with
`git diff --shortstat <base>..HEAD` — changed LOC = insertions + deletions, files = the
reported file count, tokens ≈ 4 × LOC. Each lane sees the *whole* diff through one
dimension — do **not** token-chunk the diff (the context window holds it; chunking loses
cross-file signal). When you fan out:

1. Drive it with the `Workflow` primitive (`parallel`/`pipeline` + `agent({schema})`), not
   ad-hoc Agent calls — deterministic and budget-aware.
2. One reviewer subagent per dimension lane (correctness · security · perf · tests ·
   maintainability), each returning **structured findings** (the same JSON shape as posting).
3. **Dedup** the merged findings by `(path, line, overlapping-severity)` — collapse the
   "two lanes flagged the same line" case into one thread (see [REFERENCE.md](REFERENCE.md)).
4. The orchestrator (you) owns synthesis, dedup, posting, and the merge-gate — never a lane.

Below the threshold, skip all of this and review in one pass. Log what you did (`fan-out: 5
lanes` or `single-pass`) so the choice is visible.

## Fix mode (`--fix`) — human-gated, self-verifying fixers

After review, `--fix` dispatches a **fixer subagent per confirmed finding** to close the
comment→fix→re-review loop. This is the half that touches code, so the gates are strict:

- **Tier the action by risk** (full matrix in [REFERENCE.md](REFERENCE.md)):
  - **Mechanical / P3** (rename, dead-code removal, formatting, typo, missing-await on a
    fire-and-forget) → may auto-apply.
  - **Logic-bearing / P1–P2** (control flow, conditions, data flow, query changes) →
    **propose-only**; show the diff and get explicit approval before applying.
  - **Protected paths** (auth, payments, deploy/CI config, migrations, `main` itself) →
    never auto-apply; always propose.
- **Worktree-isolated:** each fixer runs in its own git worktree, created with
  `git worktree add .worktrees/<finding-id>` (or the repo's configured worktree location)
  and removed with `git worktree remove` once it completes (parallel mandate). On a single
  PR branch, run fixers **sequentially**
  (one finding → fix → re-verify → next) — no parallel pushes to one branch.
- **Self-verify before resolving:** every fixer must run the affected suite + diff its own
  branch and report real output. **Never** trust a fixer's "✅" — re-verify yourself, then
  `reply`+`resolve` the thread only on confirmed green. (Subagents here have misreported.)
- **Never push to `main`, never bypass the human pre-merge review** — merge auto-deploys to
  prod, so the human gate is the last catch for a bad fix. Fixers push to the PR branch only.

## Pre-review checklist (run in order)

1. Secrets, injection, null-deref, races, auth/permission gaps → P0.
2. If UI-facing: accessibility (alt text, ARIA, keyboard traps, contrast) → P0 or N/A.
3. Type errors, logic bugs, missing guards, leaks, missing test for new behavior → P1.
4. Maintainability/scalability/architecture/perf/smells → P2; readability → P3.
5. Confirm the tests actually exercise the new behavior (not just that they exist).

## Output

```
## Verdict
<approve / approve-with-nits / changes-required> — one line, why.

## P0 — Blocker
## P1 — Incorrect / missing coverage
## P2 — Quality (maintainability · scalability · architecture · perf · smells)
## P3 — Polish
<each finding: file:line — what · why it matters · fix>

## What's good
<1–3 things done well — specific and evidence-anchored (file:line or named pattern), not
generic praise; e.g. "input validated at the trust boundary in `api/upload.ts:18`" not
"good error handling".>

## Dimensions checked
Correctness ✓ | Security ✓ | Maintainability ✓ | Scalability ✓ | Architecture ✓ | Efficiency ✓ | Leaks ✓ | Smells ✓ | Tests ✓ | A11y ✓/N/A
P0:<n> P1:<n> P2:<n> P3:<n>
```

> If there are >3 P2/P3 findings, list the top 3 inline and note: "X more — ask for the full list."

## Failure / Stop conditions

- Stop if required context/access is missing rather than guessing.
- Never report unverified work as reviewed-clean; read the code to confirm each claim.
- Do not fabricate findings to appear rigorous, and do not rubber-stamp to be agreeable.
- Do not post to a PR without an explicit `--pr` target + `--comment`/confirmation.
- Never post/resolve/reply under a human operator's personal GitHub account — bot identity only.
- Never stamp the posted review with a persona/"Senior-QA" label; use the neutral `## Code review` header.
- Never resolve or dismiss a human reviewer's thread; bots-only.
- Do not bypass required gates unless the user explicitly asks.
- **Fan-out only above the size threshold** — fanning out a small diff burns tokens for no gain.
- **`--fix` gates:** never run fixers without `--fix`/explicit request; never auto-apply a
  logic-bearing or protected-path fix (propose + wait for approval); never push to `main`
  or bypass the human pre-merge review; never resolve a thread on a fixer's self-report —
  re-verify the green yourself first.

## Memory hooks

- Read memory when product, repo, or convention history affects the review.
- Write memory only when the review establishes a durable policy or recurring-smell convention.
