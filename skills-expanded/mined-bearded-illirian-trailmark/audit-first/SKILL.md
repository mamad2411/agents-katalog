---
name: audit-first
description: |
  Audit-before-fix protocol — first find all gaps across 7 planes, prioritize, pin the
  gap table, and only then fix. Principle: never touch code until the full picture of
  problems is understood. Gap table → approval → flow-first per gap → library-first →
  plan → code.

  Use when: task begins with looking for problems ("find gaps in X", "audit security",
  "what's wrong with Y"), not with a specific fix
---

# Audit-First Protocol

For tasks where **you must first find all the problems**, and only then fix. Use when:

- An area is suspicious but the specific gap is unknown
- Need to make sure we're fixing the right problem, not a symptom
- Task sounds like "look at what's wrong in X" rather than "fix specific Y"
- Before an important deploy — a preventive audit

**Difference from `arch-first`:**

| | arch-first | audit-first |
|---|---|---|
| Purpose | Execute a complex task | Discover problems |
| Phase 0 | Understand the task | Find all gaps |
| Result | Decomposition into blocks | Gap table with priorities |
| When to fix | Immediately per the plan | Only after table approval |
| Launch | "Do X" | "Find what's wrong in X" |

## Input

A fix task where the specific problems are unknown; the module or integration area to audit.

## Output

`audit-doc.md` with a holes table across 7 planes (Security / Data / Logic / Integrations / Observability / UX / Performance), prioritized, plus per-hole reports as fixes close.

## Hands off to

Per-hole `flow-first` cycle for each prioritized hole, then `ship-first` at task-level closure.

---

## Principle 1 — Plane: Security

The most critical plane. HIGH by default. Checked first.

### 1.1 Auth / Authz

Endpoint accessible without token → HIGH. Internal endpoint protected only by hardcoded token → HIGH. Authorization doesn't check resource-to-tenant ownership (IDOR) → HIGH.

### 1.2 Injections (SQL, CMD, XSS)

String concatenation in queries, `shell=True`, `innerHTML` with user data → grep and flag.

### 1.3 Encryption

**In transit:** SMTP without TLS/SSL → HIGH. HTTP for external calls → MED. **At rest:** passwords in plaintext → HIGH. OAuth tokens in DB without encryption → LOW (single-tenant) / MED (multi-tenant).

### 1.4 OAuth / Tokens

- CSRF: `state = user_code` instead of `secrets.token_urlsafe()` → HIGH
- Token TTL: `access_token` used without checking `expires_at` → MED
- Storage: tokens in logs, git, unignored env → HIGH

### 1.5 Webhook validation

Two mandatory levels: signature (HMAC-SHA256 verified) + timestamp (abs(now - ts) > 300 rejected). Only level 1 → replay possible → MED. Neither → HIGH.

### 1.6 Secrets in code and configs

Hardcoded secret in code = HIGH always, even for a private repo.

---

## Principle 2 — Plane: Integrations architecture

Doesn't break immediately — breaks under load / when external service fails. MED default, HIGH on critical path.

### 2.1 Rate Limit (429)

Generic `except Exception` swallows FloodWaitError / RateLimitError → message lost silently. Correct: catch specific error before generic Exception, sleep + one retry.

### 2.2 Service-specific errors

Every external service has errors that must not fall into generic Exception. Telegram FloodWaitError → sleep + retry. Whisper 413 → check size BEFORE sending. Zoom webhook stale timestamp → reject with 400. SMTP wrong encryption → ValueError, not silent fail.

### 2.3 In-Memory state

Module-level dict resets on deploy. `_oauth_state_store` → in-flight OAuth breaks (MED). `_token_cache` → extra requests after restart (LOW). `_active_sessions` → everyone logged out on deploy (HIGH).

### 2.4 Validation BEFORE an expensive network request

File >25MB sent to Whisper without a check → learn about the problem only on 413 → retry loop. Correct: `if getsize > limit: raise` before opening the file.

### 2.5 Circuit Breaker

Every external HTTP call has `timeout=`. `ConnectionError` handled separately from business errors. Service unavailable → task marked failed, not hanging.

---

## Principle 3 — Plane: Data and DB

Rare but irreversible. Especially dangerous in multi-tenant systems.

### 3.1 Missing transactions (Race Condition)

Trigger for check: read → decide → write based on what was read. Two `execute` calls in a row without `with conn:` → concurrent requests can insert a duplicate.

### 3.2 Missing constraints

The DB must protect integrity independently of the code. Email without UNIQUE → duplicate accounts. FK without ON DELETE → orphans. Status without CHECK → invalid values. Numeric without NOT NULL DEFAULT 0 → NULL surprises.

### 3.3 N+1 queries

Query inside a loop. 100 records = 101 queries instead of 1. In SQLite less critical than in PostgreSQL, still noticeable on large datasets.

### 3.4 Plaintext for sensitive fields

User passwords in plaintext → HIGH always. OAuth tokens in DB → LOW / MED. API keys in DB → MED (better in env).

### 3.5 No TTL and no cleanup of temporary data

In-memory stores without cleanup, tokens/nonce tables without periodic `DELETE WHERE expires_at < now()`, logs without partitioning → LOW at small scale, grows with load.

---

## Principle 4 — Plane: Error handling

Most invisible plane. Gaps here don't obviously break — they make the system unpredictable.

### 4.1 Silent Failures

Exception swallowed with only a log + return False. Caller ignores False. Email didn't send, no one knows. Rule: either re-raise (critical operations) or return False + explicit caller-side check.

### 4.2 Retry loops without a limit

Retry on 413 (file too large) — won't help, file won't shrink. Retry on 401 (invalid key) — won't help either. Rule: retry only for **transient** errors (network dropped, service temporarily unavailable). For deterministic errors → fail fast with a clear message.

### 4.3 No Fallback

External service unavailable → what happens to user? Options (best to acceptable): degradation (simpler version) / queue with TTL / notify user of deferred / skip with log (non-critical only). Unacceptable: skip without log and without notification.

### 4.4 Uninformative error messages

`HTTPException(500, str(e))` leaks stack trace + internal details. Rule: 400 for invalid input, 401 auth, 403 access, 404 not found, 502 external service, 500 unexpected (no details externally, details in logs).

---

## Principle 5 — Plane: UI/UX

Breaks trust, not data. Empty screen instead of error, button that doesn't react, form that accepts garbage.

### 5.1 No Loading State

User clicked → nothing visual → clicks again → double submission. Rule: button `disabled = true` + indicator during any async action.

### 5.2 No Error State

Request failed → blank screen or stale data. Rule: show message (not technical details), give action ("Try again" / "Contact support"), don't hide behind blank.

### 5.3 No Empty State

List loaded, no data → empty space. Three states any list must have: Loading (skeleton), Empty ("No X yet. Create the first →"), Error ("Failed to load. Try again.").

### 5.4 No frontend validation

Form accepts invalid input → server returns 400 → user sees unclear error. Validate on frontend in addition to backend: required fields before submission, email/phone/URL format inline, numeric ranges, interdependent fields.

### 5.5 Broken Edge Cases

Golden path only. Typical failures: `title = null` → crash on `.length`; empty list → blank; very long name → overflow; number 0 → `if (count)` yields false; date in past → "Start" button active for expired.

### 5.6 Destructive actions without confirmation

Delete, disconnect, reset → without "Are you sure?". Rule: irreversible action requires explicit confirmation describing consequences.

---

## Principle 6 — Plane: Observability

Doesn't break — makes incidents impossible to investigate.

### 6.1 Silent Success without log

Operation done, nothing logged. Week later: "did it send Wednesday?". Every meaningful operation → log with identifiers.

### 6.2 No Structured Logging

`_log.info("sending email")` — can't tie to specific user. Include always: user_code + what's happening + relevant IDs (meeting, job, request_id).

### 6.3 Critical operations without Audit Trail

OAuth connect/disconnect, tenant settings change, data deletion, auth failure, webhook receipt — all must be logged always and immutably. For compliance, incident debugging, disputes.

### 6.4 No metrics for external calls

Whisper started answering in 30s instead of 3 — anyone notice before user complaints? Log elapsed for slow ops. Warning if slower than expected threshold.

### 6.5 Logging secrets

Tokens / passwords / API keys in log lines. Rule: log only non-confidential identifiers. Config with password → log only non-secret fields.

---

## Principle 7 — Plane: Config in code instead of source of truth

The most invisible. UI "works" (form saves), DB "works" (data stored), tests "pass" — but real effect is missing. User loses trust: "I did change this".

### 7.1 Hardcoded behavior parameters

`DIGEST_SEND_HOUR = 9` hardcoded in code. User sets 18:00 in UI → saved to `settings.digest_hour` → digest still goes at 9:00. Silent, invisible bug.

Typical cases: HOUR / DAYS / INTERVAL / REMIND / LIMIT / THRESHOLD / TEMPLATE_ID as constants when they should read from DB. Criticality: HIGH if affects money/sending/access. MED for UX (time, threshold). LOW for metadata.

### 7.2 Unused DB fields (saved but not read)

Settings table has a field. UI writes it. Business logic never reads it — uses default or constant instead. Grep test: field name → INSERT/UPDATE only, no reads outside migrations → confirmed gap.

### 7.3 "Phantom" settings forms

UI form saves data, backend doesn't apply. Check intersection: "what POST accepts" vs "what business logic reads". Excess on POST side → phantom fields.

---

## Output format — Gap table

After scanning all planes, consolidate into one table. Only format used. Approval point before fixes.

```
| # | Plane | Integration / Module | Gap | File:line | Criticality |
|---|---|---|---|---|---|
| 1 | Security | Zoom OAuth | state = user_code, no CSRF nonce | routes/oauth.py:34 | HIGH |
| 2 | Security | Email (SMTP) | No TLS, plaintext | services/email_service.py:91 | HIGH |
| 3 | Architecture | Telegram | FloodWaitError in generic except | services/telethon_manager.py:44 | MED |
```

### Criticality definitions

| Level | When to set |
|---|---|
| **HIGH** | Exploitable without privileges OR data loss/corruption/unauthorized access. Examples: CSRF in OAuth, plaintext passwords, webhook without signature, SQL injection, open authorization. |
| **MED** | Requires certain conditions OR data loss under a coincidence of factors. Examples: FloodWaitError in except, replay attack, file >25MB without check. |
| **LOW** | Technical improvement or potential vector at growing load. Doesn't break now, creates risk. Examples: in-memory cache without TTL, tokens in plaintext single-tenant, missing metrics. |

### Rules

- One row = one gap (don't group even if in same file)
- File:line = specific code line or nearest related
- Gap = one sentence: what specifically is missing or wrong
- HIGH does not exceed 3 in a normal task. 5+ HIGH → re-check criteria

Final line:

```
Total: {N} HIGH / {M} MED / {K} LOW — {X} gaps, of which {P0} P0 blocks and {P1} P1 blocks.
Waiting for approval → then I pin the block order and ask the work mode.
```

---

## Workflow — 5 phases

Sequential. Cannot start fixing until all 5 phases are completed.

### Step 0 — Check / create the task

`{log_dir}` set → proceed silently. Not set → form slug `{date}-audit-{area-slug}`, show "Creating task: {slug}. Rename?", mkdir, INSERT into `artifacts`. Cannot skip.

**Child task branch:** triggers "create child task" / "next audit stage" / "continuation of {parent}". Form `{parent}-part{N}`, register with `links (from, to, 'part_of')`. Direct mkdir + Write + INSERT bypassing this protocol is prohibited — the `part_of` link won't register and ship-first won't see unclosed chain areas.

### Step 0.5 — Calibrate incoming artifacts

audit-first expects `idea-first-*.md` with type "fix" or "problem". Type differs → propose switching to arch-first. Artifact missing → allowed (manual invocation), skip calibration, proceed with Phase 0.

### Phase 0 — Define the audit area

Do not scan until the area is specified. **Never scan the whole project** — analog of flow-first "going into code without anchors" → 50 LOW gaps, none important. Area given → use as starting point. Not given → ask one specific question.

### Phase 1 — Scan across the 7 planes

Sequential walk. Order matters:

| Order | Plane | Why here |
|---|---|---|
| 1 | Security | Only plane HIGH by default |
| 2 | Integrations architecture | Gaps manifest under load |
| 3 | Data and DB | Data loss irreversible |
| 4 | Error handling | Masks gaps in 1-3 |
| 5 | UI/UX | After backend planes |
| 6 | Observability | Last — doesn't affect correctness |
| 7 | Config in code | Silent gaps, UI+DB "work" but settings not applied |

For each plane: read area files → grep → pin what was found. "Not affected" rule: irrelevant plane → explicit "not applicable" row, don't leave blank.

### Phase 2 — Assemble the gap table

All found gaps → one table. HIGH at top, then MED, then LOW. Assign a block to each HIGH and MED. LOW at user's discretion.

### Phase 3 — Table approval

Show table + summary line → wait for explicit approval.

**Before approval — no code.** Even if the gap is obvious and fix is 2 lines. This is the main rule.

User can: approve → Phase 4; remove row (LOW deferred); change criticality; add missed gap. Each edit → updated table → wait for approval again.

**After approval — register blocks in task_blocks** for each HIGH/MED gap. Sub-blocks use `block_num = N*10 + M`, `parent_block_num = N`.

Append `## Blocks` section to task.md. Output explicit "Registered N blocks: {list}. Launching Skill('flow-first')."

### Phase 3.5 — Batch call to cadence-first

After the INSERT loop and before asking work mode → invoke cadence-first in batch mode so each gap block gets `recommended_cadence` pre-baked. HIGH gaps usually Tier 1 full cycle; LOW often Tier 3 plan-only — cadence-first formalizes this differentiation.

**Why here:** cadence is decided at GENERATION time (rich context — audit area, gap table, criticality), not at EXECUTION time.

On failure → log warning, continue. Blocks execute without pre-baked cadence.

### Final step of Phase 3 — Ask work mode

```
Blocks pinned. How do we work?

1. 🔁 Manual — I run each block, wait for your "ok"
2. 🚀 Autopilot — dev-auto-first takes over
```

Choice 1 → `Skill('flow-first')` for first HIGH block. Choice 2 → `Skill('dev-auto-first')`.

**Save audit-doc.md** to log_dir with the approved gap table. Register in `task_artifacts`. Cannot skip — on session drop, chat table isn't recoverable.

### Phase 4 — Fix per-block

Per-block cycle for each gap in order HIGH → MED → LOW: flow-first (understand landscape) → library-first (ready pattern) → plan-first → execute → ship-first (per-block).

**Block transition rule:** after "go" on ship-first per-block → first action is `Skill(flow-first)` for the next block. Not Read, not grep, not plan-first directly. flow-first cannot be skipped even if "task is obvious".

Each fix = separate commit with clear description of what it closes.

After all fixes → ship-first task-level updates gap table (✅ Fixed / 🔁 Deferred), does final report, sessions, STATUS, push + sync.

---

## Anti-patterns

### ❌ Shovel the whole project without an area

Grep everywhere → 80 lines of noise. Half false positives, other half LOW. Rule: area set before first grep.

### ❌ Fix along with scanning

Found a gap → immediately fix without waiting for remaining planes. Fixing first breaks second you haven't found yet. Rule: scan → table → approval → only then code.

### ❌ Silently skip a plane

"UI isn't relevant" → plane simply not mentioned. User doesn't know: didn't look, or looked and clean? Rule: explicit "not applicable" row for irrelevant planes.

### ❌ Mix audit and fix in one step

"Found and fixed straight away". User didn't see the table, didn't approve priorities. Rule: table shown before any code change. Approval mandatory.

### ❌ Everything is HIGH

Lowering the bar — user stops trusting criticality. Rule: HIGH only for exploitable-without-privileges OR data loss/corruption. 3+ HIGH → re-check criteria.

### ❌ Don't pin LOW in the table

LOW seems insignificant → skip. Six months later LOW is MED, then HIGH, nobody remembers it was known. Rule: all found gaps in the table. Decision what to do with LOW belongs to user.

### ❌ Don't check settings forms

Form saves → agent considers "Config in code" plane clean. But doesn't check whether field is READ in business logic. Rule: for each settings field grep-check reads (not save/update). Written but not read → gap.

### ❌ "go" on next block → plan-first instead of flow-first

After block finished, user answered "go" → agent goes directly to plan-first. Rule: "go" on next block = first action Skill(flow-first). flow-first mandatory for each block without exception.

### ❌ Create child task directly via bash bypassing Step 0

Direct `mkdir` + `Write` + `INSERT INTO artifacts` without the Step 0 child-task branch → task appears without `part_of` link → ship-first doesn't see unclosed siblings on closure. Rule: task creation only via Step 0 branch. Direct tools prohibited.

### ❌ One big fix for the whole table

All gaps in a single commit → impossible to roll back specific fix, impossible to review. Rule: one gap = one commit.

### ❌ Inlining the skill instead of using the Skill() tool

Executed the protocol from memory — outdated version, no accuracy guarantee. Always via `Skill('audit-first')`.

---

## Related skills

- **idea-first** — upstream artifact read in Step 0.5; type "fix"/"problem" → audit-first; other types → arch-first
- **flow-first / library-first / plan-first / ship-first** — per-block execution chain
- **cadence-first** — batch-invoked at Phase 3.5 to pre-bake per-block cadence
- **arch-first** — sibling for feature/product tasks (decomposition instead of gap discovery)

---

## Step 99 — Log invocation

```bash
sqlite3 {routing_db} \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('{slug}', '{N}', 'audit-first', datetime('now'))" 2>/dev/null || true
```
