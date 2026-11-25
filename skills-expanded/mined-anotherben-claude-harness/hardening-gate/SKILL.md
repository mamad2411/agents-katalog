---
name: hardening-gate
description: "Standards-enforcement gate that runs BEFORE implementation. Takes a plan, TDD, or fix proposal and hard-blocks it if SRP, seam, ownership, blast radius, edge cases, or root-cause reasoning are missing. Emits a hardening-report.md that downstream skills (enterprise-plan, enterprise-contract, patch-or-fix, b-deep-debug) require. Use this whenever you are about to commit to an implementation approach."
---

### LEARNED BEHAVIORS (auto-loaded)

Before starting, load domain-specific lessons:
1. Call `cortex_lessons(tag='feedback:HARDEN')` to retrieve corrections specific to this skill
2. If results exist, read each lesson and apply it to your behavior for this session
3. During execution, if the user corrects your approach, write a domain-tagged annotation:
   ```json
   {"target":"skill:hardening-gate","note":"<correction>","author":"hardening-gate","tags":["feedback","feedback:HARDEN","lesson"],"timestamp":"<ISO>"}
   ```
   Append to `.cortex/knowledge.jsonl`

# Hardening Gate

You are a standards enforcement engineer. Your job is to stand between a plan/fix proposal and the code that implements it, and **hard-block** anything that has not been checked against the standards that prevent the bug from coming back in a different form. This skill exists because the codebase is in a patch loop: 48% of recent commits are `fix:`, the same files get patched 4–5 times in a week, and symptom-patching ships when root-cause reasoning was skipped.

**You do not write code. You produce a verdict and a report. A `FAIL` verdict blocks the downstream skill.**

**Input:** one of
- A plan file at `docs/plans/YYYY-MM-DD-<slug>-plan.md`
- A TDD at `docs/designs/YYYY-MM-DD-<slug>-tdd.md`
- A fix proposal from `patch-or-fix` or `b-deep-debug*`

**Output:** `docs/hardening/YYYY-MM-DD-<slug>-hardening.md`, status `PASS` or `FAIL`, and a structured verdict block the caller can grep for.

```
/hardening-gate docs/plans/2026-04-14-refund-concurrency-plan.md
/hardening-gate docs/designs/2026-04-14-supplier-portal-csv-tdd.md
/hardening-gate --fix-proposal "apps/api/src/services/rexRefundWorkflowService.js: null-guard at line 412"
```

---

## Why This Exists

Git forensics on this repo:
- **48% `fix:` commits** in the last 50
- `rexRefundWorkflowService.js` touched by 5 fix commits in 4 days
- `orderPaymentsGatekeeperService.js` touched by 4 fix commits in 4 days
- `dispatcher.cjs` repaired 4× post-feature (DH-1 → DH-4)
- 40% of recent fix commit messages have no WHY — just symptom lists

Every standard the user cares about (SRP, seam proof, ownership, blast radius, edge cases, root cause) **already exists** in `.cortex/standards.json`. The failure was not the rules — it was that planning skills never invoked them before code was written. This gate closes that loop.

---

## The Seven Phases

### Phase 1 — Standards Resolve (2 min)

Pin the exact rule set the proposal must satisfy. Do not guess — fetch the current standards.

1. Infer `task_type` from the input: `bug_fix`, `feature`, `refactor`, `migration`, `integration`, `ui_component`, `performance`, `security`.
2. Call `mcp__standards-mcp__standards_for_task({ task_type })`. Record every rule ID returned.
3. Call `mcp__standards-mcp__standards_domain({ domain })` for each domain the proposal touches (`ARCH`, `DB`, `OWN`, `FLOW`, `SEC`, `ERR`, `FUNC`, `FILE`, `TEST`).
4. Write the resolved ruleset to the report as a table. If any referenced rule is missing or cannot be loaded, FAIL the phase.

**Hard-block condition:** no ruleset loaded (standards-mcp offline, empty result, or standards.json missing).

---

### Phase 2 — SRP Check (3 min) — `ARCH.SRP.PRESERVE`

For every file the proposal creates or modifies, answer:

1. **What is the single responsibility of this file today?** (one sentence)
2. **Does the proposed change fit inside that responsibility?** Yes / No / Stretches it
3. If No or Stretches, **where should the code actually live?**
4. **Does line count create an SRP review trigger (400+ lines or 800+ lines)?** Treat size as a smell only: do not split cohesive code just to get under a number, and do not accept a short file that has multiple responsibilities. Trigger Phase 3 seam analysis when size combines with unclear ownership, mixed responsibility, changed imports, or extraction/move work.

Write one row per modified file:

| File | Current SRP | Fits? | Alternative | `FILE.SIZE` |
|------|-------------|-------|-------------|-------------|

**Hard-block conditions:**
- Any row says "No" without a listed alternative
- Any modified file already touched by ≥ 3 fix commits in the last 90 days AND the proposal adds more code to it (this is the "recidivist file" signal — the fix needs an SRP split, not more lines)

Run the recidivist check with:
```bash
git log --oneline -200 -- <file> | grep -iE "^[a-f0-9]+ fix" | wc -l
```

---

### Phase 3 — Seam Check (3 min) — `ARCH.SEAM.PROOF`

This phase fires if any of these are true:
- A file in Phase 2 has a 400+ line-count smell plus unclear ownership, mixed responsibility, changed imports, or extraction/move work
- The proposal extracts or moves code between modules
- The proposal renames exported symbols
- The proposal adds a new service/module that other code must import

For each triggered case:

1. Name the **seam** being crossed (module boundary, startup load order, router mount point, DI registration)
2. Write the **seam proof plan** — which test verifies the seam is preserved?
   - Module-graph proof: `require('./foo')` still resolves
   - Startup-seam proof: app boots without errors
   - Contract proof: exported signature unchanged OR all callers updated
3. List **every existing importer** of the file being split (use `cortex_find_importers` or grep)

**Hard-block conditions:**
- Seam triggered but no seam proof plan written
- Importers not enumerated
- Renames with no caller update plan

---

### Phase 4 — Ownership Map (5 min) — `OWN.TABLE.LANE`, `OWN.PRESERVE.GUARDS`

For every database write, queue enqueue, external API call, or file-system write in the proposal:

1. Identify the **resource** (table name, queue name, external service, filesystem path)
2. Look up the owner:
   - **Database tables**: read `apps/api/ownership/db-write-owners.json`. Match the table to its `ownerPath`. If the proposal's write does not go through that owner, FAIL.
   - **Queues**: find the owning service via `grep -r 'enqueue.*queueName'`
   - **External APIs**: find the owning client/service wrapper
3. Check whether the proposal routes through the owner or bypasses it
4. If bypassed, is there an explicit `standards_exception` filed? If not, FAIL.

Write one row per write operation:

| Resource | Owner path | Proposal routes through owner? | Exception filed? |
|----------|------------|--------------------------------|------------------|

**Hard-block conditions:**
- Any `No` in column 3 without an exception in column 4
- Any existing guard/check being removed without a replacement (triggers `OWN.PRESERVE.GUARDS`)
- Any insert without `tenant_id` (triggers `FLOW.TENANT.SCOPE`)

Ownership registry loaded from: `apps/api/ownership/db-write-owners.json`. If the file is missing or the table is not listed, flag it as UNKNOWN and require human confirmation before PASS.

---

### Phase 5 — Blast Radius Scan (5–10 min)

This phase is adapted from `enterprise-debug` Phase 2 — the structure that is already proven strong for debugging. Apply it proactively to the plan.

For every symbol or pattern the proposal touches, scan for siblings:

1. **Same-file siblings** — every function in the same file. Do they share the defect / constraint / pattern the proposal addresses? Cite function names + line numbers.
2. **Cross-file siblings** — functions in the same directory doing similar operations. Use `cortex_find_references` on the symbol, plus `grep -r` for the pattern.
3. **Consumer scan** — `grep -r "<exported symbol>" apps/` — every caller. Will the proposal break any of them?
4. **Validator/guard scan** — do peer validators / guards / middleware need the same change?
5. **Branch divergence** — `git diff main..dev -- <file>` for every modified file. If diverged, read the diff and flag any risk of overwriting another branch's fix.

Each sibling found becomes one of:
- A **postcondition** the downstream contract will enforce
- An **explicit out-of-scope note** with a reason
- A **follow-up vault item** the user is told about

**Hard-block conditions:**
- Any sibling found with no disposition (must be postcondition / out-of-scope / follow-up)
- Any branch divergence with a meaningful diff on a modified file
- The scan was not performed (no evidence of the grep/cortex queries in the report)

The rule: **if the blast radius scan finds it, the hardening gate owns it.** Never defer siblings as "review will catch it."

---

### Phase 6 — Edge Case Synthesis (5 min)

Apply the 10-category checklist from `enterprise-debug` Phase 4 **proactively**. For each category, either name a concrete edge case the proposal must handle, or mark it `N/A` with one sentence of justification.

| # | Category | Edge case in this proposal | Status |
|---|----------|----------------------------|--------|
| 1 | Null / undefined / empty | | |
| 2 | Type boundaries (int overflow, UUID vs int, string length) | | |
| 3 | Concurrency (TOCTOU, duplicate events, retries) | | |
| 4 | Ordering (events out of order, partial writes) | | |
| 5 | State transitions (already-cancelled, already-refunded) | | |
| 6 | Volume (pagination, bulk, N+1) | | |
| 7 | Permissions (cross-tenant, auth bypass, escalation) | | |
| 8 | Schema evolution (missing column, new-column-old-row, dual-column drift) | | |
| 9 | External failure (API 5xx, rate limit, timeout, partial response) | | |
| 10 | Time (DST, TZ, UTC, clock skew, expiry) | | |

**Hard-block conditions:**
- Any category without an answer (blank = not considered)
- More than 4 categories marked `N/A` (too many dismissals — one of them is probably real)

Each concrete edge case named in this table becomes a postcondition the downstream contract enforces. The point is to find the edge case at plan time, not after the bug fires in production.

---

### Phase 7 — But-Why Drilldown (5 min)

Invoke the `but-why` skill (already at `~/.codex/skills/but-why/SKILL.md`) on the **design choice itself**, not the bug it addresses. Ask 3–5 questions drilling into:

- Why this approach over the obvious alternative?
- What does this proposal assume about scale / latency / concurrency that is not stated?
- If this is a bug fix: what's the root cause, and why did the existing tests not catch it? (If the answer is "no test covered that path", Phase 6 must enumerate it as an edge case.)
- Says who? — where is the authority for each load-bearing claim? (Cortex lesson, standards rule, incident report, stakeholder decision.)
- Magic Wand — if we could wave away the specific symptom, would this proposal still be the right shape?

Record the chain in the report as a `### But-Why Chain` section. Each question must reach **bedrock**: concrete fact, platform constraint, deliberate decision with rationale, or explicit knowledge boundary. "That's how it's always been" is not bedrock.

**Hard-block conditions:**
- Fewer than 3 questions asked
- Any question answered with "just because" / "it should work" / vague deflection
- The chain never reaches bedrock on any thread

---

## Verdict Format

Emit this block verbatim at the end of the report. The downstream skill greps for `HARDENING GATE VERDICT:` to decide whether to proceed.

```
HARDENING GATE VERDICT: PASS | FAIL
Target: <plan-or-tdd-or-fix-path>
Phases:
  1. Standards Resolve:   PASS | FAIL — <rule count>
  2. SRP Check:           PASS | FAIL — <file count>
  3. Seam Check:          PASS | FAIL | N/A — <seam count>
  4. Ownership Map:       PASS | FAIL — <write count>
  5. Blast Radius:        PASS | FAIL — <sibling count>
  6. Edge Case Synthesis: PASS | FAIL — <category answered / 10>
  7. But-Why Drilldown:   PASS | FAIL — <questions / bedrock hits>
Report: docs/hardening/YYYY-MM-DD-<slug>-hardening.md
```

**Any phase FAIL → overall FAIL.** There is no "advisory" level. The only escape hatch is a formal `standards_exception` filed through `mcp__standards-mcp__standards_exception` with written justification, which must be listed in the report under `## Exceptions`.

---

## Report Template

Save to: `docs/hardening/YYYY-MM-DD-<slug>-hardening.md`

```markdown
# Hardening Report: <slug>

**Date**: YYYY-MM-DD
**Target**: docs/plans/YYYY-MM-DD-<slug>-plan.md (or TDD, or fix proposal path)
**Caller**: enterprise-plan | patch-or-fix | b-deep-debug* | manual
**Verdict**: PASS | FAIL

## Phase 1 — Standards Resolved

| Rule ID | Domain | One-line |
|---------|--------|----------|

## Phase 2 — SRP Check

| File | Current SRP | Fits? | Alternative | FILE.SIZE | Recidivist (fix count 90d) |
|------|-------------|-------|-------------|-----------|----------------------------|

## Phase 3 — Seam Check

Triggered: yes / no
If triggered, one row per seam:

| Seam | Proof type | Test that proves it | Importers listed |
|------|-----------|---------------------|------------------|

## Phase 4 — Ownership Map

| Resource | Owner path | Routes through owner? | Exception filed? |
|----------|------------|----------------------|------------------|

## Phase 5 — Blast Radius

### Same-file siblings
### Cross-file siblings
### Consumers
### Validator / guard peers
### Branch divergence

Each finding: disposition (postcondition / out-of-scope / follow-up vault item).

## Phase 6 — Edge Case Synthesis

| # | Category | Edge case | Status |
|---|----------|-----------|--------|

## Phase 7 — But-Why Chain

**Objective**: <what we set out to question>

1. Q: ... → A: ... → **Bedrock: ...**
2. Q: ... → A: ... → **Bedrock: ...**
3. Q: ... → A: ... → **Bedrock: ...**

## Exceptions

(standards_exception items, one per row, with rule ID, justification, expiry)

## Verdict

HARDENING GATE VERDICT: PASS | FAIL
...
```

---

## How Downstream Skills Use This

- **`enterprise-plan`** — calls `hardening-gate` as its Phase 0. If the verdict is FAIL or the report is missing, the plan cannot be written. If PASS, the plan's `Regression Risk Assessment` section imports the blast-radius table from the report.
- **`enterprise-contract`** — checks that `hardening-report.md` exists and has `PASS`. The quality gate rejects a contract whose blast-radius siblings are not traced to postconditions, whose ownership map is missing, or whose seam triggers have no seam proof plan.
- **`patch-or-fix`** — invokes `hardening-gate --fix-proposal` before emitting its verdict. The verdict output includes `srp_verdict`, `seam_verdict`, `ownership_verdict`, `blast_radius_siblings[]` fields sourced from the report.
- **`b-deep-debug*`** — after Phase 6 "Deliver report", calls `hardening-gate --fix-proposal` with the proposed fix so the fix itself is standards-checked at source, not in review.

---

## Anti-Patterns

| Don't | Do Instead | Why |
|-------|-----------|-----|
| Skip Phase 5 because "this is just a config change" | Every change has siblings. Scan. | Config changes create 40% of production incidents in this repo. |
| Mark 7+ edge case categories `N/A` | Revisit Phase 6. One of them is real. | Dismissing everything defeats the purpose. |
| Wave through Phase 4 by citing `git log` | Read `db-write-owners.json`. It is the authority, not git log. | Git log shows history, not ownership. |
| File a `standards_exception` without expiry | Every exception has an expiry date and a ticket. | Exceptions become permanent if they don't expire. |
| Return PASS with a blank But-Why chain | Ask the questions. Reach bedrock. | The chain is the reason we caught 3 bugs on the `rexRefundWorkflowService` rewrite that Phase 6 missed. |
| Treat recidivist files as "just needs one more fix" | Flag as SRP split required — Phase 2 hard-block | The file is in the patch loop BECAUSE its SRP is broken. |

---

## Auto-mode addendum

When `auto_mode === true` in `.codex/enterprise-state/<slug>.json`:

- Hardening gate runs automatically before `enterprise-plan` Phase 0.
- If verdict = FAIL → call `auto-stop` with reason `"hardening gate failed: <phase list>"`.
- If verdict = PASS → record in `.codex/enterprise-state/<slug>.json` as `hardening_gate: { status: "PASS", report_path: "..." }` and advance.
- If the hardening report is older than the target plan (modified-time comparison), the gate re-runs automatically.

```bash
node scripts/enterprise-process-guard.cjs auto-stop --slug <slug> --reason "hardening gate failed: <phase>" --cwd .
```

---

## Context Loss Recovery

If context is lost mid-gate:
1. Check `docs/hardening/YYYY-MM-DD-<slug>-hardening.md` — how many phases are written?
2. Resume from first incomplete phase
3. Re-run Phase 1 always (standards may have changed)
4. Re-emit verdict block

The report IS the state. A new agent reads the report, checks completeness, and continues.
