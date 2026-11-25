---
name: rootscan
description: Systematic bug-hunting mode with logic reasoning. Use when user wants to find bugs before they happen — combines pattern-based detection (fast) with logic reasoning (deep) to find structural defects, design flaws, and edge cases. Forces 2-phase scan, severity rating, and actionable report before any fix.
triggers:
  - 버그 찾아
  - 버그 찾아줘
  - 버그 있는지
  - 버그 검사
  - 버그 스캔
  - 문제 찾아
  - 취약점 찾아
  - 취약점 검사
  - 코드 검사
  - 코드 리뷰
  - 잠재적 버그
  - 숨어있는 버그
  - 안전한지 확인
  - 보안 검사
  - 성능 문제
  - 메모리 누수
  - find bugs
  - scan bugs
  - code scan
  - vulnerability scan
  - security scan
  - performance issues
  - rootscan
  - 루트스캔
---

# rootscan — Logic-Driven Bug Hunting Mode

Don't wait for bugs to bite. Find them before they escape to production. When this skill activates, run 2-phase scan: **Phase 1** (pattern detection) finds known anti-patterns, **Phase 2** (logic reasoning) finds structural defects that only appear when understanding code flow.

## Activation

Explicit: `/rootscan`

Auto-triggers (when these phrases appear in user message):
- "버그 찾아줘", "버그 있는지 확인"
- "취약점 찾아", "보안 검사"
- "코드 검사", "잠재적 버그"
- "성능 문제", "메모리 누수"
- "find bugs", "scan bugs", "vulnerability scan"

## What's Different (vs general code review)

| General Review | rootscan Mode |
|---|---|
| Read code + spot issues | 2-phase: pattern scan (fast) + logic reasoning (deep) |
| Subjective "looks OK" | Severity-rated findings (🔴 HIGH / 🟡 MEDIUM / 🟢 LOW) |
| Mixed findings | Categorized report (Logic / Security / Performance / Type) |
| Text feedback | Actionable items (file:line + trace + fix suggestion) |
| One-pass read | Multi-pass: pattern → logic → cross-file → report |
| Finds known bugs | Finds known bugs **+ structural defects + design flaws** |

## 4-Category Bug Hunt

### Category 1: Logic Bugs 🧩
**What to find**: Edge cases, race conditions, null/undefined handling gaps, off-by-one errors, async coordination issues.

**Patterns to detect**:
- **Null/Undefined**: `obj.prop` without `obj?.prop` or null check, array access without bounds check
- **Edge Cases**: loop with `i < arr.length` but `arr[i+1]` access, division without zero check, string operations without empty check
- **Race Conditions**: multiple `asyncio.create_task` or `Promise.all` with shared state mutation, no lock/event for concurrent access
- **Async Coordination**: `await` inside loop without considering parallelism, missing error handling in async tasks, dangling promises
- **Off-by-One**: `range(len(arr))` then `arr[i+1]`, `slice(0, n)` logic errors
- **Boolean Logic**: complex `if` conditions with mixed `and/or`, De Morgan's law violations, redundant checks

**Detection method**:
1. Grep for risky patterns: `\.\w+\(` without null check, `arr\[.*\+.*\]`, `asyncio.create_task`, `Promise.all`
2. Read functions with >3 branches or >2 levels of nesting
3. Check all async functions for error handling + coordination

**Severity rating**:
- 🔴 HIGH: Null dereference in hot path, race on shared state, async coordination gap
- 🟡 MEDIUM: Missing edge case handling, off-by-one in non-critical path
- 🟢 LOW: Redundant checks, minor boolean logic simplification

---

### Category 2: Security Vulnerabilities 🔒
**What to find**: SQL injection, XSS, command injection, path traversal, authentication bypass, authorization gaps, secrets in code.

**Patterns to detect**:
- **Injection**:
  - SQL: string concatenation in queries (`f"SELECT * FROM {table}"` or `"SELECT * FROM " + table`)
  - Command: `os.system(user_input)`, `subprocess.call` with shell=True + user input
  - Path Traversal: `open(user_path)` without validation, `../` not blocked
  - XSS: HTML output with user input without escaping (`innerHTML = userInput`)
- **Authentication/Authorization**:
  - Missing auth check: endpoints without `@require_auth` decorator or similar
  - JWT: hardcoded secrets, no expiration check, no signature verification
  - Session: session ID in URL, no CSRF token
- **Secrets**:
  - Hardcoded: `password = "..."`, `API_KEY = "..."`, `token = "..."`
  - Logged: `logger.info(f"password: {pw}")`, sensitive data in error messages
- **Cryptography**:
  - Weak hash: MD5, SHA1 for passwords (instead of bcrypt/argon2)
  - ECB mode, hardcoded IV/salt

**Detection method**:
1. Grep for injection patterns: `f".*SELECT.*{`, `os.system`, `subprocess.*shell=True`, `innerHTML`
2. Grep for secrets: `password\s*=\s*["']`, `api_key\s*=`, `token\s*=`, `secret\s*=`
3. Check all route handlers for auth decorators
4. Check crypto usage: `hashlib.md5`, `Cipher.*MODE_ECB`

**Severity rating**:
- 🔴 HIGH: SQL injection, command injection, hardcoded secrets in production code, auth bypass
- 🟡 MEDIUM: Path traversal without validation, weak hash, missing CSRF
- 🟢 LOW: Secrets in test fixtures, verbose error messages

---

### Category 3: Performance Issues ⚡
**What to find**: N+1 queries, memory leaks, infinite loops, O(n²) algorithms, redundant API calls, unindexed DB queries.

**Patterns to detect**:
- **N+1 Query**:
  - Loop with DB query inside: `for item in items: db.query(...)`
  - ORM lazy load in loop: `for user in users: user.profile.name`
- **Memory Leaks**:
  - Unclosed resources: `open(file)` without `with`, `requests.get` without `.close()`
  - Event listeners without cleanup: `addEventListener` without `removeEventListener`
  - Growing cache without eviction: unbounded dict/map used as cache
- **Algorithmic**:
  - Nested loops on same data: `for i in arr: for j in arr:`
  - Linear search in loop: `for item in big_list: if item == x`
  - Repeated sorting: `sorted(arr)` called multiple times on same data
- **Redundant Work**:
  - Same API call in loop: `for id in ids: api.get(id)`
  - Repeated computation: same calculation in loop without memoization

**Detection method**:
1. Grep for N+1: `for.*in.*:.*\.(query|get|fetch)`
2. Grep for unclosed: `open\(` not in `with`, `requests\.(get|post)` without context manager
3. Read nested loops (>2 levels)
4. Check functions with >50 lines for repeated patterns

**Severity rating**:
- 🔴 HIGH: N+1 query in production hot path, memory leak in long-running service
- 🟡 MEDIUM: O(n²) algorithm on medium-size data, unclosed file handle
- 🟢 LOW: Minor redundant computation, non-critical repeated API call

---

### Category 4: Type Safety Holes 🏷️
**What to find**: `any` type abuse, type assertion without validation, runtime type mismatch, missing null checks in typed code.

**Patterns to detect** (TypeScript/Python typed context):
- **Type Escape Hatches**:
  - TypeScript: `as any`, `@ts-ignore`, `// @ts-expect-error` without explanation
  - Python: `cast()` without runtime check, `# type: ignore` without reason
- **Runtime Mismatch**:
  - JSON parsing without validation: `JSON.parse(data)` then direct property access
  - API response without schema check: `response.data.field` without validating structure
  - User input cast: `int(user_input)`, `Number(input)` without try-catch
- **Null Unsafety** (in strict-null-check context):
  - Non-null assertion without check: `obj!.prop`, `obj.prop!` in TypeScript
  - Optional chaining overuse masking real issue: `a?.b?.c?.d?.e` (design smell)
- **Type Declaration Drift**:
  - Interface/type definition doesn't match actual usage
  - Function signature says `X` but returns `X | null` in some paths

**Detection method**:
1. Grep for escape hatches: `as any`, `@ts-ignore`, `cast\(`, `# type: ignore`
2. Grep for non-null assertions: `!\\.`, `\\..*!`
3. Check JSON.parse call sites for validation
4. Run type checker and check for `any` in inferred types

**Severity rating**:
- 🔴 HIGH: `as any` in production code bypassing critical type check, JSON parse without validation in API handler
- 🟡 MEDIUM: `@ts-ignore` without explanation, missing null check in typed code
- 🟢 LOW: Type declaration comment out of sync, harmless `any` in test code

---

## 6-Step Scan Workflow

### Step 1: Scope Definition
- **What to scan**: user specifies file/directory/entire project
- **Focus area**: user can request specific category (e.g., "security only") or all 4
- **Depth**: 
  - **shallow** = entry points only (API handlers, main functions) + pattern scan
  - **deep** = all files + pattern scan + logic reasoning

Ask user if not clear:
```
Scanning scope:
- Files: [which files/directories?]
- Categories: [all 4, or specific ones?]
- Depth: [shallow = pattern scan only, deep = pattern + logic reasoning]
```

**Default**: If user says "버그 찾아줘" without specifying, use **deep scan** on current directory.

---

### Step 2a: Pattern Detection (Phase 1 - Fast)

**Purpose**: Find known anti-patterns via automated checks.

For each category, run the detection method:
- Grep for known patterns
- Read flagged files
- Cross-reference with checklist

**Output format per finding**:
```
[Category] Severity: Issue Title
  File: path/to/file.py:42
  Pattern: [pattern name]
  Code:
    41 | def process(data):
    42 |     result = data.field  # ← no null check
    43 |     return result
  Why risky: [explanation]
  Fix suggestion: [actionable fix]
```

**Time estimate**: ~30 seconds per 1000 LOC

---

### Step 2b: Logic Reasoning (Phase 2 - Deep)

**Purpose**: Find bugs that pattern matching can't catch — structural defects, design flaws, edge cases that only appear when understanding code flow.

**When to run**: Only when depth = **deep**. Skip if shallow.

#### 7-Point Logic Reasoning Checklist

For each critical function (API handlers, core business logic, async coordinators):

##### 1. State Flow Tracing
**Question**: "If I trace all possible state transitions, where does it break?"

Method:
- Identify all mutable state (class vars, DB fields, cache keys, async events)
- Trace state changes through function calls
- Look for paths where state becomes inconsistent

**Example findings**:
```
🔴 HIGH: State inconsistency in order processing
  File: services/order.py:67
  Logic: order.status = 'paid' but order.payment_id is None
  Why risky: Later code assumes payment_id exists when status='paid'
  Trace:
    - Line 45: status set to 'paid'
    - Line 52: payment_id set only if payment_method == 'card'
    - Line 67: returns order (payment_id may be None)
  Fix: Set payment_id before setting status, or add validation
```

##### 2. Auth/Permission Boundary Check
**Question**: "Who can access what, and is it enforced everywhere?"

Method:
- Map all resources (DB rows, files, API data)
- Check if access control is consistent across read/write/delete
- Look for "owner checks" that only check user_id but not resource_id

**Example findings**:
```
🔴 HIGH: Authorization bypass in analysis results
  File: api/analysis.py:34
  Logic: Only checks user_id match, but analysis can be shared
  Why risky: User A shares analysis with User B → both have same user_id in sharing table
            → User C can read if they guess analysis_id
  Boundary: Should check (user_id OR analysis_id in user's shared list)
  Fix: Add analysis ownership/sharing check in middleware
```

##### 3. Edge Case Enumeration
**Question**: "What inputs/states would make this function do something unexpected?"

Method:
- For each function, enumerate input dimensions: empty, zero, null, negative, very large, concurrent
- Check if each edge is handled

**Example findings**:
```
🟡 MEDIUM: Unhandled empty list in batch processor
  File: workers/batch.py:23
  Logic: Assumes items list is non-empty
  Edge cases:
    - items = [] → range(len(items)) = range(0) → loop never runs
    - Line 45: result[0] access → IndexError
  Why risky: Batch queue can send empty list during backpressure
  Fix: Add early return if not items
```

##### 4. Async Coordination Gaps
**Question**: "What happens if two async tasks run this code at the same time?"

Method:
- Find all `asyncio.create_task` / `Promise.all` / background jobs
- Check shared resources (DB, cache, file, state)
- Look for read-modify-write without locks

**Example findings**:
```
🔴 HIGH: Race condition in token refresh
  File: auth/token.py:56
  Logic:
    T=0: Task A reads token (expires_at = T+5)
    T=1: Task B reads token (expires_at = T+5)
    T=2: Task A refreshes → new token written
    T=3: Task B refreshes → overwrites A's token with older one
  Why risky: Token becomes invalid, all requests fail
  Fix: Use lock or atomic compare-and-swap
```

##### 5. Error Propagation Analysis
**Question**: "If step 3 fails, does step 5 know about it?"

Method:
- Trace error paths (try-except, return None, error callbacks)
- Check if errors propagate or get silently swallowed
- Look for "optimistic" code that assumes success

**Example findings**:
```
🟡 MEDIUM: Silent failure in notification sender
  File: notifications/email.py:78
  Logic:
    - send_email() catches all exceptions, logs, returns None
    - Caller doesn't check return value
    - User thinks notification sent, but it failed
  Why risky: Users miss critical alerts (payment failed, account locked)
  Fix: Return success/failure status, or raise exception
```

##### 6. Data Schema Drift Detection
**Question**: "Does code assume a schema that may not be true?"

Method:
- Check API response handling: does code assume fields exist?
- Check DB queries: does code assume row shape matches model?
- Look for dict access `data['field']` without checking key existence

**Example findings**:
```
🔴 HIGH: Missing field handling in external API response
  File: integrations/payment.py:45
  Logic: response.data.transaction_id accessed directly
  Schema risk:
    - External API docs say transaction_id is optional
    - Code assumes it always exists
    - Error: KeyError when payment pending (no transaction_id yet)
  Why risky: Breaks checkout flow
  Fix: Use response.data.get('transaction_id') with fallback
```

##### 7. Implicit Assumptions Hunt
**Question**: "What does this code assume that might not be true?"

Method:
- Read function comments/docstrings for assumptions
- Check "obvious" behavior that's not validated
- Look for magic constants without explanation

**Example findings**:
```
🟡 MEDIUM: Unvalidated assumption about list order
  File: ranking/scorer.py:34
  Logic: Assumes items are sorted by score descending
  Assumption: Caller sorts before passing
  Risk: If caller doesn't sort, top 10 may not be actual top 10
  Evidence: No sorting in this function, no assertion
  Fix: Add assert items == sorted(items, key=...) or sort here
```

---

#### When to flag as finding vs. when to skip

**Flag if**:
- Assumption can be violated in real usage
- Failure mode is data loss / security breach / user-facing error
- Code in critical path (auth, payment, core business logic)

**Skip if**:
- Assumption is guaranteed by framework/library contract
- Only breaks in test scenarios
- Already covered by existing validation layer

---

### Step 3: Severity Triage
Group findings by severity:
- 🔴 **HIGH**: Must fix before merge (blocks PR)
- 🟡 **MEDIUM**: Should fix soon (follow-up ticket)
- 🟢 **LOW**: Optional improvement (backlog)

---

### Step 4: Cross-File Analysis

Some bugs only appear when reading multiple files together:
- **Inconsistent Error Handling**: one file throws, another returns null for same error
- **Shared State Race**: file A writes `_cache[key]`, file B reads it without lock
- **API Contract Drift**: caller expects `{status, data}`, but handler returns `{ok, result}`

Method:
- Identify shared state (global vars, class attributes, DB tables)
- Trace access patterns across files
- Flag inconsistencies

**This step is enhanced by Step 2b logic reasoning** — cross-file issues are often caught during state flow tracing and async coordination checks.

---

### Step 5: Report Generation
**Summary**:
```
🔴 HIGH: N findings (must fix)
🟡 MEDIUM: M findings (should fix)
🟢 LOW: L findings (optional)

Top 3 risks:
1. [most critical finding]
2. [second most critical]
3. [third most critical]
```

**Detailed Findings** (grouped by category → severity):
```
## 🧩 Logic Bugs
### 🔴 HIGH
- [finding 1]
- [finding 2]
### 🟡 MEDIUM
- [finding 3]

## 🔒 Security Vulnerabilities
### 🔴 HIGH
- [finding 4]
...
```

**Actionable Next Steps**:
```
Immediate (before merge):
1. Fix [file:line] - [issue]
2. Fix [file:line] - [issue]

Follow-up (next sprint):
1. Add [test/validation] for [pattern]
2. Refactor [area] to eliminate [risk]

Optional (backlog):
1. Consider [improvement]
```

---

## Output Format

```
[rootscan — <scope>]

Scan Summary:
- Scope: [files/directories]
- Categories: [Logic / Security / Performance / Type]
- Depth: [shallow = pattern only / deep = pattern + logic reasoning]
- Phase 1 (Pattern): N findings
- Phase 2 (Logic): M findings (only if deep scan)
- Total Findings: 🔴 X HIGH / 🟡 Y MEDIUM / 🟢 Z LOW

Top 3 Risks:
1. [most critical]
2. [second most critical]
3. [third most critical]

---

## 🧩 Logic Bugs

### 🔴 HIGH
[findings...]

### 🟡 MEDIUM
[findings...]

### 🟢 LOW
[findings...]

---

## 🔒 Security Vulnerabilities
[same structure...]

---

## ⚡ Performance Issues
[same structure...]

---

## 🏷️ Type Safety Holes
[same structure...]

---

## Next Actions

🚨 Immediate (before merge):
1. [action]
2. [action]

📋 Follow-up (next sprint):
1. [action]

💡 Optional (backlog):
1. [action]

---

Confidence: HIGH | MEDIUM | LOW
Reason: [why this confidence level]
```

---

## Termination Conditions

Scan complete → report delivered when ALL of:

- [ ] Scope clearly defined (files + categories + depth)
- [ ] **Phase 1**: Pattern detection run for all requested categories
- [ ] **Phase 2**: Logic reasoning performed (only if depth = deep)
  - [ ] State flow traced for critical functions
  - [ ] Auth/permission boundaries checked
  - [ ] Edge cases enumerated
  - [ ] Async coordination verified
  - [ ] Error propagation analyzed
  - [ ] Data schema drift checked
  - [ ] Implicit assumptions hunted
- [ ] Each finding has: file:line + severity + fix suggestion (+ trace if from Phase 2)
- [ ] Findings grouped by category → severity → phase
- [ ] Cross-file analysis performed (for deep scan)
- [ ] Top 3 risks identified
- [ ] Next actions classified (Immediate / Follow-up / Optional)
- [ ] Confidence declared (HIGH/MEDIUM/LOW + reason)

Any unchecked item → scan incomplete.

**Confidence rating guide**:
- **HIGH**: Deep scan completed, all 7 logic checks passed, cross-file analysis done
- **MEDIUM**: Pattern scan completed, partial logic reasoning (some checks skipped due to code complexity)
- **LOW**: Shallow scan only, or deep scan blocked by missing context (unclear requirements, external dependencies)

---

## Anti-Patterns (forbidden in this mode)

1. **"Looks OK to me"** — skipping systematic checklist, relying on intuition
2. **Pattern-only when user wants deep** — skipping Phase 2 logic reasoning when depth = deep
3. **Unfocused scan** — reading code without specific pattern/logic check in mind
4. **No severity** — listing findings without priority (user can't triage)
5. **Vague fix** — "improve error handling" instead of "add try-catch at line 42"
6. **False negatives** — missing patterns because grep wasn't run, or missing logic flaws because trace wasn't done
7. **Category mixing** — security + performance in one finding (separate them)
8. **Claiming HIGH confidence without Phase 2** — can't be HIGH if you skipped logic reasoning

---

## Notes

- Derived from real-world code review sessions where critical bugs were missed because review was unfocused or pattern-only.
- **Phase 2 logic reasoning** is the differentiator — finds bugs that static analyzers can't catch.
- Pairs with rootfix: scan → find issue → rootfix → fix root cause.
- Works in any language. Adjust patterns per language (e.g., Python vs TypeScript vs Go).
- Can be run as pre-commit hook (shallow), PR gate (deep), or periodic audit (deep).
- **Time estimate**: shallow ~1 min per 1000 LOC, deep ~5 min per 1000 LOC (depends on complexity).

---

## Example Usage

**User**: "버그 찾아줘 이 API 핸들러에"

**Agent** (rootscan activated):
```
[rootscan — api/handlers/]

Scan Summary:
- Scope: api/handlers/*.py
- Categories: All (Logic, Security, Performance, Type)
- Depth: Deep (pattern + logic reasoning)
- Phase 1 (Pattern): 3 findings
- Phase 2 (Logic): 2 findings
- Total Findings: 🔴 3 HIGH / 🟡 2 MEDIUM / 🟢 1 LOW

Top 3 Risks:
1. Authorization bypass in analysis results (logic reasoning - no pattern match)
2. SQL injection in user_search() - no parameterized query
3. Race condition in async cache update - no lock

---

## 🧩 Logic Bugs

### 🔴 HIGH (Phase 1 - Pattern)
**Race condition in cache update**
  File: api/cache.py:34
  Pattern: Shared state mutation without lock
  Code:
    33 | async def update_cache(key, value):
    34 |     _cache[key] = value  # ← no lock, multiple tasks can race
    35 |     await notify_subscribers(key)
  Why risky: Multiple concurrent calls can interleave, leading to lost updates
  Fix suggestion: Use asyncio.Lock() or single-writer pattern

### 🟡 MEDIUM (Phase 1 - Pattern)
**Missing null check in profile access**
  File: api/user.py:67
  Pattern: Null dereference
  Code:
    66 | user = get_user(id)
    67 | return user.profile.bio  # ← user could be None
  Why risky: If user not found, AttributeError crashes handler
  Fix suggestion: Add `if user is None: return 404` before access

---

## 🔒 Security Vulnerabilities

### 🔴 HIGH (Phase 1 - Pattern)
**SQL injection in search**
  File: api/search.py:23
  Pattern: String concatenation in SQL
  Code:
    22 | query = request.args.get('q')
    23 | sql = f"SELECT * FROM users WHERE name LIKE '%{query}%'"  # ← injection!
    24 | results = db.execute(sql)
  Why risky: Attacker can inject `'; DROP TABLE users; --`
  Fix suggestion: Use parameterized query: `db.execute("... WHERE name LIKE ?", (f"%{query}%",))`

### 🔴 HIGH (Phase 2 - Logic Reasoning)
**Authorization bypass in analysis results**
  File: api/analysis.py:34
  Logic Check: Auth/Permission Boundary
  Code:
    33 | def get_analysis(analysis_id):
    34 |     analysis = db.query(Analysis).filter_by(id=analysis_id).first()
    35 |     if analysis.user_id == current_user.id:
    36 |         return analysis
  Why risky: Only checks user_id match, but analysis can be shared
  Trace:
    - User A creates analysis (owner)
    - User A shares with User B via sharing_table
    - User C guesses analysis_id → Line 34 succeeds
    - Line 35 fails (not owner) → but C already saw analysis in line 34 query
  Boundary violation: Should check (user_id == current OR analysis_id in shared_with_user)
  Fix suggestion: Add sharing check in query filter or middleware

---

## ⚡ Performance Issues

### 🟡 MEDIUM (Phase 1 - Pattern)
**N+1 query in user list**
  File: api/users.py:45
  Pattern: DB query inside loop
  Code:
    44 | for user in users:
    45 |     user.profile = db.query(Profile).filter_by(user_id=user.id).first()  # ← N queries
  Why risky: 1000 users = 1000 DB queries, scales poorly
  Fix suggestion: Use `joinedload(User.profile)` to fetch in one query

---

## 🏷️ Type Safety Holes

### 🟢 LOW (Phase 1 - Pattern)
**Type ignore without reason**
  File: api/utils.py:12
  Pattern: Type escape hatch
  Code:
    11 | def parse(data):
    12 |     return json.loads(data)  # type: ignore
  Why risky: Bypasses type checker, actual issue could be signature mismatch
  Fix suggestion: Add proper return type annotation or explain why ignore is needed

---

## Next Actions

🚨 Immediate (before merge):
1. Fix authorization bypass in api/analysis.py:34 [rootfix]
2. Fix SQL injection in api/search.py:23 [rootfix]
3. Fix race condition in api/cache.py:34 [rootfix]

📋 Follow-up (next sprint):
1. Add integration test for concurrent cache updates [rootbuild]
2. Add sharing matrix test for analysis permissions [rootbuild]
3. Refactor user list to use joinedload [rootclean]

💡 Optional (backlog):
1. Add type validation for JSON.parse calls [rootclean]

---

Confidence: HIGH
Reason: Deep scan completed - all 4 categories + 7 logic checks performed. Phase 2 found authorization bypass that pattern matching missed.
```
