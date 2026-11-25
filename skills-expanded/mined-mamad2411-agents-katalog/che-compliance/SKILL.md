---
name: "che-compliance"
description: "Two-stage security & compliance review: LIGHT per-task diff scan and HEAVY final full-session scan. Checks for secrets, PII leaks, SQL injection patterns, auth/RLS bypasses, dangerous URLs. Invoke ONLY by che-act. NEVER fixes code directly — only reports findings."
---

# Che — Compliance & Security

> **SHARED REFERENCES (CANONICAL — DO NOT DUPLICATE body here):**
> - Security + PII + RLS full checklist: see `_shared_checklists/SECURITY_PII_COMMON.md`
> - GitHub CLI auth preflight + operations: see `_shared_checklists/GITHUB_CLI_COMMON.md` (final ship PR checks)
> - Nx/pnpm run order local verification: see `_shared_checklists/NX_PNPM_COMMON.md`

Security/PII/security pattern scanner. Two stages:
- **Stage `per-task` (LIGHT)**: scans only files changed in the current task.
- **Stage `final` (HEAVY)**: scans FULL cumulative session diff + global patterns missed by per-task.

**CRITICAL RULE: This skill MUST NEVER modify source code directly. It only produces a structured FINDINGS report. Developer fixes, SM validates.**

---

## -0.1 STORAGE BOUNDARY PREFLIGHT (CANONICAL, NON-NEGOTIABLE — run BEFORE §0 and BEFORE FIRST WRITE)

NO compliance report is written to the USER WORKTREE by default. All reports land in che-sessions via centralized helper. UNIQUE exception: user explicitly asks VERBATIM to save a specific report there.

```bash
# 1. Resolve the `che` CLI (owns the 5-tier Che-home cascade)
command -v che >/dev/null 2>&1 || { echo "❌ FATAL: 'che' CLI not found on PATH. Aborting write."; exit 98; }

# 2. SESSION_ID + RELATED_ID (per-task = T<id>; final = worktree slug)
SESSION_ID="${SESSION_ID:-${CHE_SESSION_ID:-${HARNESS_SESSION_ID:-compliance-$(date -u +%Y%m%d-%H%M%S)}}}"
if [[ "${stage}" == "final" ]]; then
  COMPLIANCE_RELATED_ID="compliance-final-${WORKTREE_SLUG_CANONICAL:-$(basename "$WORKTREE_ROOT" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g; s/--*/-/g; s/^-//; s/-$//')}"
else
  COMPLIANCE_RELATED_ID="T${TASK_ID:-0000}-${TASK_SLUG:-per-task}"
fi

# 3. Canonical paths + dirs (if not inherited)
if [[ -z "${CHE_SESSION_DIR}" ]]; then
  eval "$(che compute_paths "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD")"
  che ensure_dirs "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD"
fi

# 4. Double-guard outside worktree
che assert_outside_worktree "${CHE_SESSION_DIR}"      "$WORKTREE_ROOT" --label "CHE_SESSION_DIR"
che assert_outside_worktree "${CHE_WORKSPACE_SHARED}" "$WORKTREE_ROOT" --label "CHE_WORKSPACE_SHARED"

# ==== OUTPUT PATH OF THIS SKILL (constructed ONCE) ====
# stage = final     → scope=workspace (durable: cross-session comparison)
# stage = per-task  → scope=session   (ephemeral: this session only)
COMPLIANCE_SCOPE="session"
[[ "${stage}" == "final" ]] && COMPLIANCE_SCOPE="workspace"
COMPLIANCE_REPORT_PATH="$(che output_path "report" "compliance-${stage}" "${COMPLIANCE_RELATED_ID}" "${COMPLIANCE_SCOPE}" "md")"
# → per-task example:  $CHE_SESSION_DIR/reports/T2-refund/20260902-143000-compliance-per-task.md
# → final example:     $CHE_WORKSPACE_SHARED/report/compliance-final-wt-feat-X/20260902-143000-compliance-final.md
# → Intrinsic ordering by UTC timestamp prefix. Atomic write via: cat <<EOF | che write_file_atomic "$COMPLIANCE_REPORT_PATH"
```

---

## 0. Preconditions

Must receive:
- `WORKTREE_ROOT`
- `stage`: `"per-task"` OR `"final"`
- If `per-task`: current task changed files list
- If `final`: entire session cumulative diff files list
- Che session task-id (to know where to write report; uses `$COMPLIANCE_REPORT_PATH` from preflight above)

---

## 1. SCAN CATEGORY 1 — Secrets & Credentials (CRITICAL / HARD BLOCK)

Run ALL checks. A match = SEVERITY:CRITICAL.

### 1.1 Generic secret regex patterns

Scan changed files (grep / content scan) for these patterns:

| Pattern | Matches |
|---|---|
| `sk-[a-zA-Z0-9]{20,}` | Stripe live/test secret keys |
| `pk_live_[a-zA-Z0-9]{20,} / pk_test_[a-zA-Z0-9]{20,}` | Stripe publishable live/test keys (live = BLOCK; test = WARN) |
| ` Bearer [A-Za-z0-9\-._~+/]+=*` | Bearer tokens in code strings |
| `-----BEGIN (RSA|EC|OPENSSH|PGP|PRIVATE) KEY-----` | Private key material |
| `ghp_[A-Za-z0-9]{20,} \| gho_\| ghs_\| ghu_` | GitHub PATs |
| `xox[baprs]-[A-Za-z0-9-]{10,}` | Slack tokens |
| `AIza[0-9A-Za-z\-_]{35}` | Google API keys |
| `AKIA[0-9A-Z]{16}` | AWS Access Key ID |
| `(?i)(password\s*[:=]\s*["'][^"']{8,}["']` | Hardcoded password strings |
| `(?i)(api[_-]?key\|secret[_-]?key\|access[_-]?token\|client[_-]?secret)\s*[:=]\s*["'][^"']{6,}["']` | Generic API keys assigned to literals |

### 1.2 `.env` files and leaking

- Check if `.env*` files ADDED or EDITED:
  - `.env` → CRITICAL if git tracked (must be in .gitignore)
  - `.env.example` → OK, but verify no real values
- Check if any code does:
  - `console.log(process.env)` or similar full env object output
  - Passing env vars to frontend bundles (Next.js public env secret leak)

---

## 2. SCAN CATEGORY 2 — PII / Personal Data (CRITICAL / HARD BLOCK when leaked)

### 2.1 Logging & persistence patterns

Scan for:
- `console.log(email)` / `logger.*email`, `logger.*password` — any raw PII field logged. (Must use hashing / correlation secret, never raw)
- Direct storage of: credit card numbers (PAN), CVV, SSN equivalents
- Email addresses / phone numbers persisted without explicit PII hash / masking
- Any logger.info/debug lines containing: username + password together

### 2.2 Known PII fields (heuristic — match any occurrence then contextual review)

If found in NEW code: flag and REQUIRE rationale for each instance:
```
<file>:<line>: contains assignment of <field> — flagged as possible PII
Context: <3 lines before, the finding line, 3 lines after context>
Rationale required: is this hashed? masked? needed?
```

---

## 3. SCAN CATEGORY 3 — Injection & Input Validation (HIGH severity)

### 3.1 SQL injection patterns

Scan for:
- String concatenation / template literals building SQL:
  ```
  `SELECT * FROM users WHERE id = ${userId}`
  "SELECT * FROM users WHERE id = " + userId
  ```
  Except when inside well-known ORM parameterized builder (Knex `.whereRaw` only when params array provided).
- `.whereRaw / .raw / queryRaw` with string template without parameter array
- Dynamically concatenating table names / column names from user input (whitelist needed)

### 3.2 Command injection patterns

Scan for:
- `child_process.exec` / `execSync` with unsanitized user input in command string (use `execFile` or `spawn` + args array)
- Shell commands with `;`, `&&`, `|`, backticks interpolated from external input
- `system()` / `os.popen()` / `Runtime.getRuntime().exec()` in other languages with tainted args

### 3.3 XSS patterns (web projects)

Scan for:
- `dangerouslySetInnerHTML` without sanitization
- `.innerHTML =` user_input
- `document.write(user_input)`
- `<script>user_input</script>` in SSR output
- `eval()` / `new Function()` with user-controlled strings

---

## 4. SCAN CATEGORY 4 — Auth & Authorization (HIGH severity)

### 4.1 Auth check (web / API projects)

Scan changed auth-related files for:
- Open routes defined without missing authentication checks (`@deprecated` / `@Public()` auth)
- Intentionally skipping auth without explicit `// eslint-disable-next-line` comments
- Hard bypass of RLS policies if Postgres+Supabase:
  - `.select().then(result => result)` — rows returned from Supabase without RLS enforced
  - usage of service_role key on client-side (service_role MUST be server only)

### 4.2 Permission checks

- Any endpoint / route:
  - Does it check ownership / roles BEFORE database read/write?
  - Is the check EARLY RETURN on request lifecycle? (fail-early)

---

## 5. SCAN CATEGORY 5 — Dangerous URLs (CRITICAL when pointing to prod-looking destinations)

Check ALL new URLs. Block any new AWS / RDS / Supabase / Neon / production DB:

- Hostname patterns to block (case-insensitive):
- `*.rds.amazonaws.com`
- `*.supabase.co`
- `*.neon.tech`
- `*.cockroachlabs.cloud`
- `*.azure.com` + `/sql` or `/db`

If used in NEW code → flag SEVERITY:HIGH + ask: is this DEV or PROD? correct env?

---

## 6. SCAN CATEGORY 6 — Destructive operations (HIGH / medium/low depending)

Scan for NEW code:
- DROP TABLE / TRUNCATE / DELETE FROM without WHERE
- `fs.rm(force:true, recursive:true)`
- destructive migration without NODE_ENV check + consent string checks
- destructive script

---

## 6.5 SCAN CATEGORY 7 — Test Naming Behavioral Conventions (Che RULE 7.9)

**Applies ONLY to:** new/edited files matching `*.test.*`, `*.spec.*`, or inside `__tests__/` folder. If task did not touch tests → SKIP this category.

**Goal:** avoid `describe()` / `it()` / `test()` names containing ONLY internal IDs, forcing title to describe OBSERVABLE BEHAVIOR (valid for months, not just task duration).

**🔴 HARD RULE — PROHIBITED INVERSION (NEVER do this):**
> ❌ **WRONG:** Complain / report finding because a test DOES NOT HAVE `FLO-xxx` / `T<N>` / `AC<N>` in the title string.
> ✅ **CORRECT:** Having these references IN THE TITLE is ANTI-PATTERN (bad = finding). NOT having them and describing behavior is GOOD / COMPLIANT.
>
> **1-sentence decision:** `title contains FLO-ID? → BAD = FINDING. title does NOT contain FLO-ID? → GOOD = NEVER generate finding for missing ID.`

**Scan pattern:** look for strings inside `describe("...")`, `it("...")`, `test("...")`. For each title found, check anti-patterns:

| Anti-pattern (regex case-insensitive) | Reason | Severity |
|---|---|---|
| `FLO-\d+` / `[A-Z]{2,}-\d+` | Linear/Jira Ticket IDs in TITLE. Valid only while ticket open; invalidates CI report in 6 months. | WARN |
| `Task?\s*T\d+(\.\d+)?` / `Item\s*\d+` | Che Task IDs in TITLE. Task rearrangement breaks name. | WARN |
| `AC\s*\d+` / `Criteria\s*\d+` | SPEC/PRD Acceptance Criteria IDs in TITLE. | WARN |
| `§\s*\d+(\.\d+)?` / `RULE\s*\d+` / `SPEC[_-]\w+` / `PRD\s*§` | Planning doc section references IN TITLE. | WARN |
| `Phase\s*\d+` / `Story\s*#?\d+` | Temporary phase/story IDs in TITLE. | WARN |

**Correct traceability (DOES NOT generate finding — use these):**
1. JSDoc comment ABOVE block: `/** @ticket FLO-714 · @ac 3.2 · @task T1.4 */`
2. 1st line comment INSIDE block: `// @ticket FLO-714 | @ac 3.2 | @task T1.4`

**Severity rule (FINDING only if BAD patterns ABOVE present in TITLE):**
- 1–9 bad titles → **WARN** (non-blocking; detailed list in report)
- ≥10 bad titles in same diff → **HIGH** (blocking; engineering-contracts becomes non-review-friendly)
- Good titles = contain action verb + condition + result; DO NOT have regexes above. A GOOD title not having FLO-xxx or Task-id IS EXPECTED.

**❌ NEVER generate finding for missing FLO/T/AC in title** → this is default correct. If your report has "missing FLO prefix in title" it's a REGRESSION of this category, discard the line before output.

**How to report:**
```
## Scan 7 — Test naming (RULE 7.9)
Total spec files modified: 3 | Test titles inspected: 24
Good (behavioral, NO internal IDs): 20 | Bad (contains internal IDs in TITLE STRING): 4
  1. /src/__tests__/auth.test.ts:88 — it("Task T2.3 validates AC 4.2 service role") → BAD in title: "Task T2.3" + "AC 4.2"
     Suggest rename: it("blocks non-service-role callers with 403 Forbidden when anon key used")
     Keep traceability: inside block line 1: // @ac 4.2 | @task T2.3 | @ticket FLO-745
  2. ...
```

---

## 7. REPORT FORMAT — Stage: findings

### Findings report structure

```markdown
# Compliance Report — <TASK-ID> — Stage: <per-task | final>

Scan date: <ISO datetime> | Files scanned: N

## Summary
Total findings: <count>
CRITICAL: N | HIGH: N | MEDIUM: N | LOW: N | WARN: N

## Table of findings

| # | Severity | Category | File:Line | Finding | Status |
|---|----------|----------|-----------|---------|--------|
| 1 | CRITICAL | Secrets | /path:42 | Hardcoded Stripe live sk_* | OPEN |
| 2 | HIGH | PII | /path:8 | Raw email in logger | OPEN |
| 3 | MEDIUM | Injection | ... | ... | OPEN |

## Detailed findings

### #1 — CRITICAL — Secrets leak
**File:** <path>
<line context 3 before, finding line, 3 lines context after>
**Recommendation:** <recommended steps>

### #2 — HIGH — PII leak
**File:** ...
**Recommendation:** ...

## Appendix: passed checks
- [x] No private keys
- [x] No AWS keys
- [x] Supabase service_role not in client bundles
- [ ] PII hash/masking (1 instance reviewed)
```

Severity definitions:
- **CRITICAL**: immediate prod breach potential or credential leak. Hard block. FIX before next step. → back to Dev
- **HIGH**: vulnerability with clear exploit path in realistic scenario. Hard block. → back to Dev
- **MEDIUM**: plausible but requires unlikely preconditions. Soft block: if tiny patch release or justification; or explicit user override.
- **LOW**: best-practice violations, readability / smell. Non-blocking logged.
- **WARN**: cosmetic / informational. Non-blocking.

### How to write report to disk (NOT inside worktree)

Always use path and atomic write from PREFLIGHT. NEVER construct `$CHE_*` manually, never use `./reports`, never write to `<WORKTREE_ROOT>/.trae/`.

```bash
# Generate markdown report in memory and atomic write:
cat <<'EOF' | che write_file_atomic "$COMPLIANCE_REPORT_PATH"
# Compliance Report — <TASK-ID> — Stage: <per-task | final>
... (§7 structure above)
EOF

303→# Print to user in English:
304→#   Compliance <stage> completed. 0 CRITICAL. 0 HIGH.
305→#   Full report saved at: $COMPLIANCE_REPORT_PATH (outside your worktree).
306→#   No untracked/modified files added to git status.
```

If stage=`final` (cross-session durable): decision-log via helper for audit trail:
```bash
che decision_append "$WORKTREE_ROOT" "COMPLIANCE_HEAVY_RUN"   '{"report_path":"'"${COMPLIANCE_REPORT_PATH}"'","total_findings":<N>,"critical":<N>,"high":<N>}'
```
DO NOT manual append (`cat >> $CHE_DECISIONS_PATH`) — non-atomic + JSONL corruption risk.

---

## 8. FINAL STAGE extras (only when `stage: final`)

Same scans, plus:

### 8.1 Cross-file consistency

- Scan FULL session diff. If secret moved from file A to B in different tasks. Per-task scans separately — final catches cross-task.
- Architecture boundary violations: Does diff introduce cross-layer onion/clean violations.
- Circular imports / dependency direction.

### 8.2 ENV check / environment-specific code

Look for:
- `NODE_ENV === 'production'` checks inverted or missing
- Hardcoded `localhost` or staging/dev hostnames in prod-bound paths
- Timezone / currency hardcoded vs env-driven

### 8.3 Result

Final stage produces 1 additional overall verdict:

```
Final Compliance verdict:
- CRITICAL found: 0
- HIGH found: 0
- MEDIUM: 2 (Dev+1 logged)
- LOW: 3
- WARN: 5
- OVERALL: PASS / FAIL
Blocking issues remain → back to SM → to Dev for fixes.
```

---

## A: What Compliance must NEVER do

- Fix source code / files directly. Compliance = reviewer, never executor.
- Run tests, build, lint. That's QA's job.
