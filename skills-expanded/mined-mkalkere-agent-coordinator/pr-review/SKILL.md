---
name: pr-review
version: 2.0.0
standalone: true
description: Review pull requests for code quality, security, and correctness
uses:
  - development/git
  - core/memory
  - core/repo-intelligence
requires:
  tools: [git, gh]
  env: []
security:
  risk_level: write
  capabilities:
    - git:read
    - github:pr:read
    - github:pr:comment
  requires_approval: false
---

# PR Review (Reviewer Agent)

Thorough code review for pull requests. Handles the full review process
including context loading, analysis, inline commenting, and verdict submission.

**Standalone**: This skill works without agent-coordinator. Steps marked
*(framework only)* can be skipped when running standalone in Claude Code.

## Two-Round Review Protocol

Every PR gets TWO independent review passes. Only publish a verdict after both.

**Round 1 — Code Reviewer**: Run `references/checklist.md` CRITICAL tier.
Focus on correctness, security, test coverage, design consistency.

**Round 2 — Silent Failure Hunter**: Re-read the FULL diff with a different
mental model. Hunt for what Round 1 missed: swallowed exceptions, race
conditions, data loss on edge inputs, missing error paths, state not cleaned up.
Prefix all Round 2 findings with `[R2]`.

**Verdict rules**:
- Either round finds blocking issues → `review_changes_requested`
- Both rounds clean → `review_approved`
- NEVER post conflicting verdicts on the same commit

## Subagent Review (when Agent tool is available)

When the Agent tool is available (SDK wrapper or interactive mode), spawn
specialized subagents for each round instead of doing both yourself:

```
Agent(description="Code reviewer", prompt="Review PR #{pr_number}. Run checklist CRITICAL tier. Return findings.")
Agent(description="Silent failure hunter", prompt="Hunt for silent failures in PR #{pr_number}. Prefix findings with [R2].")
```

Launch both in parallel for faster reviews. Combine their findings for the verdict.

**Optional third agent for large diffs (200+ lines):**
```
Agent(description="Security auditor", prompt="Security audit PR #{pr_number}. Check OWASP top 10, auth bypass, injection.")
```

## Auto-Scale Review Depth

Scale review effort based on diff size:

| Diff Size | Review Depth |
|---|---|
| < 50 lines | Single-pass checklist (no subagents) |
| 50-199 lines | Two rounds (code reviewer + silent failure hunter) |
| 200+ lines | Three rounds (+ security auditor subagent) |
| 500+ lines | Flag for split — PR may be too large for effective review |

To check diff size: `gh pr diff {pr_number} --stat | tail -1`

## Fix-First Heuristic

Auto-fix mechanical issues. Ask only for judgment calls.

| Auto-fixable (commit directly) | NOT auto-fixable (report as finding) |
|---|---|
| Dead imports / unused variables | Security design decisions |
| Formatting / whitespace | Architecture changes |
| Typos in comments | API contract changes |
| Stale comments that don't match code | Performance trade-offs |
| Missing type annotations | Business logic changes |

When auto-fixing: create a fixup commit on the PR branch, push, note in review comment.

## Completion States

- **DONE**: Both rounds complete, verdict posted, bus message published
- **DONE_WITH_CONCERNS**: Approved with non-blocking observations noted
- **BLOCKED**: Cannot review (PR not found, branch deleted, auth failure)
- **NEEDS_CONTEXT**: Need clarification from developer before completing

**Platform note**: Uses GitHub (`gh` CLI). The review methodology is
platform-agnostic; only the tool commands are GitHub-specific.

## Scope Drift Detection

Before reviewing code quality, check if the PR does what it claims:

1. Read the PR title and description
2. Read the linked issue (if any)
3. Compare the actual diff against the stated intent
4. Flag if files are modified that aren't mentioned in the PR description
5. Flag if the PR description mentions changes not present in the diff

Scope drift is a **HIGH** finding — it means either the PR is incomplete or
contains unintended changes.

## STOP — Read This Entire Skill Before Starting

Do NOT begin reviewing until you have read every section below.
Each section has a purpose. The lifecycle steps at the end (Section 6) are
MANDATORY — skipping them leaves the task in limbo and the developer
is never notified of your verdict.

## Rationalizations to Reject

If you catch yourself thinking any of these, STOP. These are the shortcuts that
lead to rubber-stamp reviews. Every one has caused a real bug to ship.

| Rationalization | Why It's Wrong | Required Action |
|---|---|---|
| "Small PR, quick review" | Heartbleed was a 2-line change. Size ≠ risk. | Full methodology, every step. |
| "This pattern looks safe, I've seen it before" | Each context has different callers, state, and trust boundaries. | Verify THIS specific instance. |
| "The tests pass, so it's correct" | Tests only cover what the developer thought to test. Missing tests are invisible. | Check what's NOT tested. |
| "I'll flag it as Medium, not blocking" | If it causes data loss or silent failure in production, it's Critical regardless of how minor the code change looks. | Assess actual production impact, not code-change size. |
| "The developer probably thought about this" | You are the safety net. If you assume the developer handled it, nobody checked. | Verify explicitly — read the code path. |
| "This is just a UI change, low risk" | DOM state bugs, XSS, error swallowing, and accessibility failures all live in UI code. | Apply full checklist including Silent Failure Hunting. |
| "Skipping full verification for efficiency" | Partial analysis is worse than no analysis — it creates false confidence. | Complete every applicable checklist item. |
| "Similar code elsewhere does this" | Similar code elsewhere may also be buggy. Don't inherit assumptions. | Verify independently. |
| "Just a refactor, no security impact" | Refactors break invariants. Changed code paths need the same scrutiny as new code. | Analyze as HIGH risk until proven LOW. |
| "It's documented in the README" | Developers don't read docs under deadline pressure. Security must be enforced in code, not docs. | Verify the code enforces the documented behavior. |

## BEFORE YOU START — Read references/

> **MANDATORY**: Read BOTH files in `references/` before starting:
> 1. `references/common-misses.md` — 7 patterns reviewers consistently miss
> 2. `references/checklist.md` — structured 2-tier checklist (CRITICAL + INFORMATIONAL)
>
> If you skip these, you WILL miss real bugs.

## Critical Reminders (DO NOT LOSE THESE)

These are the most commonly skipped steps. If your context window is running low,
prioritize these over adding more inline comments:

1. **Read `references/common-misses.md` AND `references/checklist.md`** — the patterns and checks you're most likely to miss
2. **Run BOTH review rounds** — Round 1 (code review) then Round 2 (silent failure hunt)
3. **Post inline comments** via `gh api` (Section 6) — a summary-only review is INCOMPLETE
3. **Update task status** via coordinator (Section 8) — or the developer is never notified
4. **Publish bus notification** (Section 8) — or the system doesn't know the review happened

## Execution Model

This is a **builtin skill** with per-tool handlers. When `pr_diff` is invoked,
the executor runs `gh pr diff`. When `pr_comment` is invoked, the executor posts
the review comment. The agent applies the methodology between tool calls.

## When to Use

- When a `pr_created` message arrives on the bus
- When a `review_request` message arrives (developer addressed comments)
- When manually requested to review a PR

## Task Ownership (MANDATORY FIRST STEP)

Before reviewing, claim the task so other reviewers don't duplicate work:

```bash
COORDINATOR="${AC_COORDINATOR_URL:-http://localhost:9889}"
TASK_ID="{task_id}"  # from the bus message payload
AGENT_NAME="{your-agent-name}"

# Claim the task (JSON body, not query param)
curl -s -X POST "${COORDINATOR}/tasks/${TASK_ID}/claim" \
  -H "Content-Type: application/json" \
  -d "{\"agent_id\": \"${AGENT_NAME}\"}"
# Expected: {"task_id": N, "claimed": true, ...}
# If 409 → another reviewer already claimed it. STOP — do not review.
```

> **Checkpoint**: `curl -s "${COORDINATOR}/tasks/${TASK_ID}"` shows
> `agent_id` is your name.

## Methodology

### 1. Load Repository Context

Before reviewing, use the **query_repo_context** tool to load intelligence:
- Repository patterns and conventions
- Known issues in the codebase
- File relationships (test mappings)
- Previous review trajectories for related files

### 2. Fetch PR Information

**CRITICAL — Resolve PR Number First**: Issue numbers and PR numbers are DIFFERENT namespaces.
A bus message with `issue_id: 473` may correspond to PR `#474`. Never assume they are the same.
Never look at local branches to find the PR. Always use `gh` to resolve the actual PR number.

**If the bus message contains `pr_number`**: use it directly.

**If the bus message contains only `issue_id`** (no `pr_number`):

```bash
# Method 1: Search by linked issue (most reliable)
gh pr list --state open --search "closes:#<issue_id>" --json number,title,headRefName

# Method 2: Match branch name pattern (e.g. fix/<issue_id>-description)
gh pr list --state open --json number,title,headRefName | grep "<issue_id>"

# Method 3: List all open PRs and inspect
gh pr list --state open --json number,title,headRefName,url
```

Verify the resolved PR number before proceeding:

```bash
gh pr view <pr_number> --json number,title,state,body
```

> **Checkpoint**: You have a confirmed integer PR number. Write it down — every subsequent
> step uses this number. If you cannot resolve it, STOP and notify via bus before proceeding.

Use the **pr_diff** tool to get the full diff. Also use **feedback_fetch**
to check existing comments and CI status. Gather:
- PR title, description, and linked issues
- Full diff of all changed files
- CI check status
- File list with additions/deletions count
- Check for open PRs that touch overlapping files: `gh pr list --state open`

### 3. Design Review (EVALUATE FIRST)

Before diving into code details, assess the overall design. This is the most
important review dimension — if the design is wrong, code quality doesn't matter.

- **Approach**: Is the overall approach sound? Could a simpler solution work?
- **Placement**: Does this change belong in this module, or should it be in a
  different component or library?
- **Abstraction**: Is the abstraction level appropriate? Not over-engineered,
  not too concrete?
- **Complexity**: Is the change more complex than necessary? Will future
  developers understand this code without extensive context?
- **Scope**: Is the PR focused on one concern, or does it mix unrelated changes?
  Large PRs mixing concerns should be flagged for splitting.

**PR Splittability Assessment** (flag if ANY apply):
- PR touches 3+ unrelated subsystems (e.g., API + dashboard + config)
- PR mixes a refactor with a behavior change — reviewers can't tell which
  diffs are "just cleanup" vs "functional change"
- PR adds a feature AND fixes an unrelated bug — if the bug fix is reverted,
  the feature shouldn't break (and vice versa)
- Diff exceeds ~400 lines — large PRs get superficial review. Flag as **Medium**:
  "Consider splitting this PR for more thorough review"

**Anti-Over-Engineering Check** (LLM-generated code is especially prone to these):

You are an LLM reviewing code likely written by an LLM. Both of you share the
same tendencies. Actively watch for these and flag them:

- **Premature abstraction**: Helper/utility created for a single call site.
  Three similar lines of code is better than a premature abstraction.
  Flag as **Medium**: "This helper has one caller — inline it."
- **Unnecessary error handling**: Try/catch for scenarios that cannot happen
  given the function's callers. Trust internal code and framework guarantees.
  Only validate at system boundaries (user input, external APIs).
  (Exception: catches on I/O, network, and DB paths are always in scope —
  see Silent Failure Hunting in Section 4A.)
- **Drive-by cleanup**: Bug fix PR that also renames variables, adds docstrings,
  or reorganizes imports in unrelated files. Flag as **Medium**: "Separate cleanup
  from behavior changes — mix makes the diff unreadable."
- **Feature flags for internal code**: Backwards-compatibility shims, re-exports,
  or `_deprecated_` wrappers when the code is internal and can just be changed.
- **Over-documented obvious code**: Comments that restate what the code does
  (`# increment counter` above `counter += 1`). Good comments explain *why*.
- **Unnecessary configurability**: Making things configurable that have exactly
  one correct value in this system. YAGNI applies.

> **Checkpoint**: You can articulate in one sentence what this PR does and
> why the chosen approach is (or isn't) the right one.

### 3.5. Functional Flow Verification

Before reviewing individual files, trace the complete functional flow of the change:

- **Trigger**: What initiates this code path? (HTTP request, bus message, timer, CLI command)
- **Processing**: What transformations/logic happen? Are there intermediate states?
- **Side effects**: What external state changes? (DB writes, file creation, bus messages, API calls)
- **Output**: What does the caller receive? Is the contract clear?
- **Error path**: When things go wrong, what happens at each stage? Is cleanup complete?

Map the flow end-to-end before diving into line-by-line review. This catches
architectural issues that per-file review misses (e.g., a function that writes
to disk but has no cleanup on failure, or a bus message published before the
DB transaction commits).

> **Checkpoint**: You can draw the flow: trigger → processing → side effects → output,
> and you know what happens on the error path at each stage.

### 4A. Universal Checklist

For each file, run this checklist. These items apply to **every** review regardless
of reviewer specialization.

**Security** (OWASP-aligned, always check first):
- No hardcoded secrets, credentials, or API keys
- Input validation on all user-provided data
- SQL injection prevention (parameterized queries only)
- XSS prevention (output encoding/escaping)
- Authentication/authorization checks present and correct
- Sensitive data not logged or exposed in error messages
- Security misconfiguration: no debug flags, no permissive CORS with credentials,
  no default passwords
- Dependency changes: new/changed packages checked for known CVEs
- Cryptographic choices: no weak algorithms (MD5, SHA1 for security), proper key management
- Error handling: exceptions don't expose stack traces or internal state to callers
- Deserialization: untrusted data not deserialized without validation

**Correctness**:
- Code does what it claims
- Edge cases handled (null, empty, boundary values)
- Error handling appropriate (not swallowing exceptions silently)
- No logic errors or off-by-one mistakes
- No falsy value confusion — `if value:` must not lose 0, False, [], {}; use
  `if value is not None:` or `isinstance()` checks when the value domain includes falsies
- Preconditions verified — resource creation functions return whether they actually created
  vs. reused; config resolution paths all actually resolve, not just conditional branches
- Guards protect against missing directories: `Path.unlink(missing_ok=True)` only suppresses
  file-not-found, NOT parent-dir-deleted — check `parent.is_dir()` first
- State machine transitions validated — check that status changes follow allowed transitions
  and handle invalid/duplicate transitions gracefully

**Silent Failure Hunting** (MANDATORY — this catches the bugs that pass all other checks):

For EVERY error handling path in the diff — `try/catch`, `except`, `if err`, `.catch()`,
return codes, exit codes — ask: "What happens when this fails? Does the user know?
Does the developer have breadcrumbs to debug it?"

Quick scan for these high-signal antipatterns by domain (section 4B `error-path-analysis`
has full details, fix guidance, and additional items beyond this summary).
**Skip language sections not present in the PR diff** — e.g., if the PR is Python-only,
skip the Go/Rust/Java/JS sections:

*Any language:*
- Generic catch-all swallowing errors without logging (**High**)
- Discarded error variable — `catch (_)` / `except Exception` with no logging (**High/Medium**)
- Transient state (DOM, in-memory dict, worktree files) lost on recreation (**Critical**)
- Destructive action followed by fallible logging outside transaction (**Critical**)
- Retry without idempotency on non-idempotent operations (**High**)

*Web/Frontend (JS/TS):*
- `res.ok ? data : []` — server errors look like empty data (**Critical**)
- `response.json().catch(() => response.text())` — body stream consumed twice (**High**)
- Buttons triggering API calls without disable-during-request (**Medium**)

*Python/Backend:*
- Bare `except:` — swallows everything including KeyboardInterrupt/SystemExit (**Critical**)
- `except Exception: pass` — swallows all application errors silently (**High**)
- `subprocess.run()` without `check=True` and no manual returncode check (**High**)
- `requests.get()`/`httpx.get()` without `timeout=` — hangs forever on unresponsive server (**High**)
- SQLAlchemy session not committed/rolled-back — auto-rollback on `session.close()` (**High**)
- `async for` / `async with` resource not cleaned up on `CancelledError` (**High**)

*CLI/Infrastructure:*
- Process exit code ignored — `os.system()` or subprocess return value unchecked (**High**)
- Signal handler that doesn't clean up resources (PID files, locks, temp dirs) (**Medium**)
- File lock not released on crash — no `finally` or context manager (**High**)

*Go:*
- `result, _ := doSomething()` — error return discarded (**High**)
- `go func()` without context/cancellation — goroutine leak (**High**)
- `defer f.Close()` before nil check on `f` — panic on error (**High**)

*Rust:*
- `.unwrap()` in non-test library code — panic with no recovery (**High**)
- `let _ = fallible_fn()` — `#[must_use]` Result silently discarded (**High**)

*Java/Kotlin:*
- `catch (Exception e) { /* ignore */ }` — especially swallowed InterruptedException (**High**)
- InputStream/Connection opened without try-with-resources (**High**)

*Database/Data:*
- Migration that silently drops/renames column without data preservation (**Critical**)
- Transaction not committed before response sent — client sees success, DB has nothing (**Critical**)
- Bulk operation with no progress checkpoint — crash at 99% restarts from 0% (**Medium**)

*Configuration/YAML/JSON:*
- YAML `yes`/`no`/`on`/`off` parsed as boolean instead of string (**Medium**)
- Missing required config field silently defaults to zero/empty (**Medium**)

> Note: These apply to catches on **reachable error paths** (I/O, network, disk, DB).
> If a catch guards pure logic with provably constrained inputs, it may be unnecessary —
> see the Anti-Over-Engineering Check (Section 3) resolution rule.

**PR Description Verification** (MANDATORY):
- Read the PR title and description/body carefully
- For each claimed feature or fix, verify the code actually implements it
- If the description says "X is shown when Y happens," find the code that does it
- If a claimed feature is missing from the code, flag as **High** ("PR description
  claims X but code does not implement it")
- Check that the PR scope matches the description — no undocumented drive-by changes

**Performance**:
- No N+1 query patterns
- No blocking operations in async code — `subprocess.Popen`, `open()`, `mkdir()`, and
  file locks in `async def` or FastAPI routes MUST use `asyncio.to_thread()`
- `time.sleep()` > 1 second should use `time.monotonic()` loop for interruptibility
- Regex and expensive lookups compiled once at module level, not per-call
- Large data handled efficiently (streaming, pagination)
- No regressions on hot paths — if the change touches frequently-called code,
  consider the performance impact

**Testing**:
- New code has tests that exercise the actual code (not just mocked logic)
- Tests cover edge cases and error scenarios
- Tests are meaningful (not just for coverage numbers)
- Tests call real methods, not re-implementations of production logic
- Failure paths tested — not just happy path
- Timeout/concurrency scenarios considered where applicable
- Mocks validate behavior, not implementation details

**AI-Generated Code Patterns** (LLM-written code has predictable failure modes):

Code generated by LLMs (including this project's agents) fails in specific,
predictable ways. Check explicitly for these:

1. **Hallucinated APIs**: Function calls, method names, or parameters that don't
   exist in the library being used. Verify every imported function and method call
   against the actual library API. Flag as **Critical**.
2. **Plausible-but-wrong logic**: Code that reads correctly but has subtle logic
   errors — e.g., inverted condition, off-by-one in range, wrong variable in
   comparison. LLMs produce code that "looks right" more than it "is right."
   Flag as **High** when found.
3. **Outdated library usage**: Using deprecated APIs, old syntax, or patterns from
   older library versions. LLMs train on historical code. Verify against current
   library docs. Flag as **Medium**.
4. **Missing context dependencies**: Code that works in isolation but fails because
   it doesn't account for surrounding state — e.g., assumes a variable is set by
   a caller, relies on initialization order, or misses a required import.
   Flag as **High**.
5. **Copy-paste drift**: Two or more similar code blocks that should be identical
   but have small differences (different variable names, missing a line). LLMs
   generate each block independently. Flag as **Medium**.

Note: Unnecessary error handling for impossible cases is covered under
Anti-Over-Engineering Check (Section 3). Do not duplicate findings here.

**Observability** (can you debug this in production?):
- Critical operations (auth, task state changes, destructive actions) produce log
  entries with enough context to reconstruct what happened
- Error paths log the error object/message, not just "an error occurred"
- No `console.log` or `print()` debugging left in production code paths
- If the change adds a new background process, timer, or polling loop — is there
  a way to tell if it's running, stuck, or failed? (health endpoint, log, metric)
- Audit-critical operations (delete, permission change) have non-optional logging
  that cannot be silently skipped

**Framework Compliance** (MANDATORY for this project):
- **Templates first**: If `.os/` files were modified, were `src/os/templates/` updated FIRST
  and synced? Direct `.os/` edits without template changes are a **Critical** issue.
- **Both execution paths**: If `claude_wrapper.py` was changed, does `agent_runner.py`
  need the same change (or vice versa)? If only one path was changed, verify the PR
  description explains WHY the other path is unaffected.
- **No developer memory leaks**: `.os/agents/*/memory/` files from the PR AUTHOR should NOT
  be in the PR diff — these are local agent state, not project code. Flag as **Medium** if present.
  Exception: reviewer's own memory commits intentionally added to the branch are expected.

**Documentation**:
- Public APIs documented
- Complex logic has comments explaining why, not what

### 4B. Review-Profile Dimensions (from identity.yaml)

Before starting this section, check your `review_focus` from identity.yaml.
Apply ONLY the dimension checklists that match your focus tags. Skip the rest.

If you do not have a `review_focus` list, apply ALL dimension checklists below.

When submitting your review via `pr_comment`, you MUST include a `review_checklist`
parameter — a JSON object where each key is one of your `review_focus` tags and
each value is `"checked"`, `"not_applicable"`, or `"skipped_with_reason:..."`.
The tool will reject your review if any focus area is missing.

---

#### `async-correctness`
- No blocking I/O in async functions — `subprocess.Popen`, `open()`, `os.mkdir()`,
  file locks in `async def` MUST use `asyncio.to_thread()`
- Task cancellation handled — `asyncio.shield()` used where needed, cleanup runs on cancel
- No fake async — functions that are `async def` but never `await` are misleading
- Lock contention checked — `asyncio.Lock` held across await points minimized
- `time.sleep()` never used in async code — use `asyncio.sleep()` instead

#### `platform-safety`
- **Unix process groups**: `os.killpg(pid, sig)` MUST verify `os.getpgid(pid) == pid`
  first — killing a non-leader's group kills the parent process (server)
- **Windows file ops**: `Path.replace()` and `os.rename()` fail with PermissionError when
  destination is open — provide fallback to direct write
- **Windows file close**: `fh.close()` can raise PermissionError under contention —
  wrap cleanup in try/except
- **Cross-platform paths**: Use `Path` objects, not string concatenation with `/`
- **Shell quoting**: Use `shlex.quote()` for Unix, avoid `shell=True` on both platforms
- If code touches processes, pipes, or file locks: verify both Windows and Unix paths tested

#### `resource-lifecycle`
- Process cleanup: every `subprocess.Popen` has a corresponding kill/wait path on error
- File handles: every `open()` uses `with` or has explicit `close()` in `finally`
- Async tasks: every `asyncio.create_task()` is awaited or tracked for cancellation
- Unbounded buffers: no list/dict that grows without bound in a long-running process
- Temp files: every `tempfile.mkstemp` or `NamedTemporaryFile` has cleanup in `finally`

#### `concurrency-safety`
- TOCTOU prevention: check-then-act patterns use atomic operations or locks
- Atomic operations: `INSERT...SELECT` for DB claims, `os.rename` for file swaps
- Lock ordering: if multiple locks are acquired, order is consistent to prevent deadlock
- Shared mutable state: global/class-level dicts/lists protected by locks or are thread-local
- Signal safety: signal handlers do minimal work (set a flag, not I/O)

#### `state-machine-integrity`
- Transition validation: status changes follow allowed transitions (e.g., `idle→working→done`)
- Idempotency: repeated transitions to same state are safe (no double-counting, no errors)
- Crash recovery: if process dies mid-transition, state is recoverable on restart
- Concurrent transitions: two agents can't race to claim the same state change

#### `data-integrity`
- Falsy value confusion: `if value:` doesn't silently lose `0`, `False`, `""`, `[]`, `{}`
- Path traversal: user-provided file paths validated against workspace root
- Schema validation: external data (bus messages, API input) validated before use
- Serialization roundtrip: data survives JSON/YAML encode→decode without loss
- Type coercion: no silent `str(None)` producing `"None"` strings in data

#### `defensive-coding`
- Precondition guards: functions validate inputs before proceeding (fail fast)
- Fallback chains: when primary path fails, fallback exists and is tested
- Partial-state cleanup: if a multi-step operation fails midway, partial results are cleaned up
- Sentinel values: no magic strings (`"unknown"`, `"none"`) where `None` or enum should be used

#### `cross-module-impact`
- Caller tracing: for every changed function, `grep` all callers — do they still work?
- Config keys: renamed/removed config keys checked against all consumers
- Bus schemas: changed message payloads checked against all subscribers
- API contracts: changed HTTP endpoints checked against all clients
- Import changes: renamed/moved modules checked against all importers

#### `unbounded-growth`
- Buffer caps: in-memory collections have maximum size limits
- JSONL rotation: append-only log files have rotation or size limits
- DLQ limits: dead-letter queues don't grow forever
- Dedup set bounds: deduplication sets are bounded or periodically cleaned
- Connection pools: pool sizes are configured, not unlimited

#### `error-path-analysis`
This is the authoritative checklist for error-path bugs. Section 4A's Silent Failure
Hunting is a quick-scan summary — this section has the full details and fix guidance.
Trace each error path through callers, not just the immediate diff.
**Read only the "Any language" section plus sections matching the PR's languages.**
Skip language sections not present in the diff to conserve context window.

**Any language / cross-cutting:**

- **Generic catch-all swallowing**: `.catch(() => genericMsg)`, `catch(e) { showGeneric() }`,
  `except Exception: return default` where the error is never logged or surfaced. Every
  catch must log the error and show specifics. Flag as **High**.
- **Discarded error variable**: `catch (_) {}`, `catch {}`, `except Exception:` with the
  error deliberately unnamed/unused. Flag as **High** if the catch body does not clearly
  indicate intentional handling. Flag as **Medium** if the catch body handles the case
  correctly but does not log for debugging. Fix: name it, log it.
- **Transient state not surviving recreation**: State stored in a transient container
  (DOM elements, in-memory dict, context window, worktree-local files) is silently lost
  when the container is recreated (re-render, process restart, worktree cleanup). Check
  for this in any code that stores state — not just UI code. Flag as **Critical**.
  Fix: store state in a durable location and restore after recreation.
- **Destructive-then-fallible-log**: Destructive action (DELETE, DROP, overwrite) followed
  by audit logging outside the same transaction. If logging fails, user sees 500 but data
  is already gone. Fix: wrap post-destruction logging in try-except, or move inside
  transaction. Flag as **Critical**.
- **Retry without idempotency**: Code that retries a failed request on non-idempotent
  operations (POST, DELETE) can cause duplicates. Verify idempotency or use idempotency
  keys before adding retry logic. Flag as **High**.
- **Error caught at wrong level**: Error caught and handled locally when it should
  propagate to a higher-level handler with more context. E.g., data layer catches a
  connection error and returns `None` — API handler returns 200 with empty data, never
  knowing the DB is down. Flag as **High**. Check whether the caller distinguishes
  "no data" from "error fetching data." If the caller handles the `None`/default as an
  error condition, the local catch may be intentional — only flag when the error is truly
  swallowed and the caller cannot distinguish failure from empty.
  Fix: let the error propagate; handle where the user gets actionable feedback.
- **Optional chaining hiding failures**: `obj?.prop?.method()` silently produces `undefined`
  when `obj` is unexpectedly null. In Python: `getattr(obj, 'prop', None)`. If the value
  should always exist, optional chaining masks the bug. Flag as **High** if the value
  is required by downstream logic (silent `undefined` propagates). Flag as **Medium** if
  the value is sometimes-absent by design.
  Fix: explicit null check with error for required values; `?.` only for genuinely optional.
- **Fallback to mock/stub in production**: Production code falls back to a mock, stub,
  or in-memory implementation when the real service is unavailable. Hides outages,
  produces silently wrong data. Flag as **Critical**.
  Fix: fail visibly when a required service is down; fake fallbacks belong only in tests.
- **Retry exhaustion without notification**: Retry loop exhausts all attempts, then
  silently returns a default or empty result. User never knows. Flag as **High**.
  Fix: after exhausting retries, surface the last error with retry count.

**Web/Frontend (JS/TS):**

- **Fetch/HTTP error masking**: `res.ok ? data : []` or `res.ok ? data : {}` makes server
  errors (500, 502, 404) indistinguishable from "no data." User sees empty list, assumes
  nothing exists. Every fetch must have a distinct error state with HTTP status shown.
  Flag as **Critical**.
- **Body stream double-consumption**: `response.json().catch(() => response.text())`.
  In browser Fetch, calling `.json()` consumes the ReadableStream body. If `.json()`
  rejects, a subsequent `.text()` resolves to empty string because the stream is drained.
  (Node.js undici may differ.) Flag as **High**.
  Fix: `const text = await response.text(); const data = JSON.parse(text);`
- **Success-path silent fallback**: `try { data = await res.json() } catch { data = {} }` —
  parse failure on a success response silently produces empty data. Downstream code gets
  `undefined` for expected fields. At minimum: `console.warn`. Flag as **Medium**.
- **No double-click protection**: Buttons triggering API calls (send, delete, create) without
  disable-during-request allow duplicate operations. Flag as **Medium**.
  Fix: disable in handler, re-enable in `finally`.

**Python/Backend:**

- **Bare except swallowing**: Bare `except:` catches everything including `BaseException`
  subclasses (`KeyboardInterrupt`, `SystemExit`, `CancelledError` in Python 3.9+) — the
  process cannot be interrupted. Flag as **Critical**.
  `except Exception: pass` does NOT catch `KeyboardInterrupt`/`SystemExit` but still
  silently swallows all application errors. Flag as **High**.
  Fix: catch specific exceptions, or at minimum `except Exception as e: logger.error(e)`.
- **Subprocess exit code ignored**: `subprocess.run()` or `os.system()` without
  `check=True` and no manual `returncode` check. The command fails, the code continues
  as if it succeeded. Flag as **High**.
  Fix: use `subprocess.run(..., check=True)` or check `result.returncode != 0`.
- **HTTP request without timeout**: `requests.get(url)` or `httpx.get(url)` without
  `timeout=` parameter. Hangs forever if the server is unresponsive. In async code,
  `asyncio.wait_for()` or `httpx.AsyncClient(timeout=...)`. Flag as **High**.
  Fix: always set explicit timeout. Default to 30s for API calls, 5s for health checks.
- **SQLAlchemy session not committed**: Changes made via `session.add()` / `session.execute()`
  but `session.commit()` missing or only in the happy path. On exception, `session.close()`
  auto-rolls-back and changes are silently lost. Flag as **High**.
  Fix: use `with session.begin():` context manager or explicit commit in `try` + rollback
  in `except`.
- **Async cancellation not handled**: `async with` or `async for` resource cleanup skipped
  when `asyncio.CancelledError` propagates. The resource (file handle, DB connection,
  subprocess) leaks. Flag as **High**.
  Fix: use `try/finally` or ensure `__aexit__` handles cancellation.
- **`logging.exception()` outside except block**: Calling `logging.exception()` outside
  an `except` block produces "NoneType" in the traceback. Flag as **Medium**.
  Fix: use `logging.error()` with explicit exception, or only call `.exception()` in except.

**CLI/Infrastructure:**

- **Process exit code ignored**: `os.system(cmd)` return value unchecked, or `subprocess.call()`
  result discarded. Script reports success when the underlying command failed.
  Flag as **High**. Fix: check return code, propagate non-zero as error.
- **Signal handler doesn't clean up**: SIGTERM/SIGINT handler that sets a flag or logs
  but doesn't release locks, remove PID files, close DB connections, or clean temp dirs.
  On container shutdown, resources are orphaned. Flag as **Medium**.
  Fix: register cleanup in `atexit` AND signal handlers, or use context managers.
- **File lock not released on crash**: Lock acquired via `fcntl.flock()` or `msvcrt.locking()`
  without `try/finally` or context manager. Process crash = permanent lock.
  Flag as **High**. Fix: use `with` statement or `finally` block. Consider lease-based
  locks with expiry for distributed systems.
- **PID file stale after crash**: PID file written on start but not removed on abnormal
  exit. Next startup sees stale PID, refuses to start or kills wrong process.
  Flag as **Medium**. Fix: validate PID is still alive before trusting PID file.

**Database/Data:**

- **Migration drops/renames without preservation**: `ALTER TABLE DROP COLUMN` or
  `ALTER TABLE RENAME COLUMN` without a data migration step. Existing data is silently
  lost or inaccessible. Flag as **Critical**.
  Fix: add data migration, or use add-new → migrate-data → drop-old pattern.
- **Transaction not committed before response**: API endpoint sends success response
  before DB transaction commits. Client sees 200, but if commit fails, DB has nothing.
  Flag as **Critical**. Fix: commit before sending response, or use DB-level confirmation.
- **Bulk operation without progress checkpoint**: Processing 10K records in a single
  transaction. Crash at 99% restarts from 0%. Flag as **Medium**.
  Fix: batch with periodic commits and resumable cursor/offset.
- **Schema assumption without validation**: Code assumes a column, table, or index exists
  without checking. Works in dev (migrations ran), fails in production (migration pending).
  Flag as **Medium**. Fix: add migration version check, or use safe `IF EXISTS` patterns.
- **Concurrent write without conflict resolution**: Two writers update the same row.
  Last-write-wins silently overwrites the first writer's changes. Flag as **High**.
  Fix: optimistic locking (version column), or `UPDATE ... WHERE version = expected`.

**Go:**

- **Unchecked error return**: `result, _ := doSomething()` or `doSomething()` without
  capturing the error return. The function fails, the code continues with zero-value `result`.
  Flag as **High** when the function performs I/O or has runtime-dependent failure modes.
  If the error is provably impossible for the given inputs (e.g., `strconv.Atoi` on a
  compile-time constant), the discard may be intentional — verify before flagging.
  Fix: `result, err := doSomething(); if err != nil { return err }`.
- **Goroutine leak**: `go func()` launched without cancellation path — if the goroutine
  blocks on a channel or I/O, it never exits. Flag as **High**.
  Fix: pass `context.Context`, select on `ctx.Done()`.
- **Deferred close after error check**: `f, err := os.Open(...); defer f.Close()` before
  checking `err`. If `err != nil`, `f` is nil and `defer f.Close()` panics.
  Flag as **High**. Fix: defer after the nil check.
- **nil map/slice write**: Writing to a nil map panics. Writing to a nil slice via index
  panics (append is safe). Flag as **High** if map is not initialized before write.

**Rust:**

- **Unwrap in library code**: `.unwrap()` or `.expect()` in non-test, non-main code.
  Panics crash the caller with no recovery. Flag as **High** when the `Result`/`Option`
  depends on runtime input. Unwrapping a value just validated by a match/if-let or
  produced by an infallible path is idiomatic — verify before flagging.
  Fix: return `Result<T, E>` and use `?` operator.
- **Ignoring Result**: `let _ = fallible_fn();` — the `#[must_use]` warning is suppressed
  and the error is silently discarded. Flag as **High** if the function has side effects.
- **Unbounded collect**: `.collect::<Vec<_>>()` on an iterator of unknown size — OOM on
  large inputs. Flag as **Medium**. Fix: use bounded buffer or streaming.

**Java/Kotlin:**

- **Checked exception swallowed**: `catch (Exception e) { /* ignore */ }` — especially
  `InterruptedException` which clears the interrupt flag silently. Flag as **High**.
  Fix: re-throw, or at minimum `Thread.currentThread().interrupt()` for InterruptedException.
- **Resource not closed**: `InputStream`, `Connection`, `PreparedStatement` opened without
  try-with-resources. Leaked on exception. Flag as **High**.
  Fix: use try-with-resources (`try (var rs = ...)`) or Kotlin's `.use {}`.
- **Nullable platform type**: Kotlin calling Java method that returns `@Nullable` without
  null check. Compiles fine, NPE at runtime. Flag as **High**.

**Configuration/YAML/JSON:**

- **Type coercion surprise**: YAML `yes`/`no`/`on`/`off` parsed as boolean, not string.
  `port: 8080` parsed as int, `port: 08080` parsed as octal (some parsers). Norway
  country code `NO` parsed as `false`. Flag as **Medium**.
  Fix: quote strings in YAML, use explicit types, validate after parse.
- **Missing required field with silent default**: Config schema allows missing fields that
  silently default to empty/zero. App runs in degraded mode with no warning.
  Flag as **Medium**. Fix: validate required fields at startup, fail fast.
- **Environment variable not set**: `os.environ['KEY']` or `env::var('KEY').unwrap()` without
  fallback — crashes on missing env. But `os.getenv('KEY', '')` silently uses empty string.
  Flag as **Medium**. Fix: validate env vars at startup, fail with descriptive error.

#### `test-depth`
- Failure paths tested: not just happy path — error branches exercised
- Timeout values: tests don't use `time.sleep(10)` — use short timeouts or mocks
- Concurrency tested: race conditions exercised with thread/async interleaving
- Mock quality: mocks validate behavior contracts, not implementation details
- Integration coverage: at least one test exercises the real code path (not all mocked)

#### `type-design`
When a PR introduces or modifies types (classes, dataclasses, Pydantic models, TypedDict,
interfaces, structs). If you flag a construction validation issue here, do not also flag
it under `error-path-analysis` or `insecure-defaults` — one finding per root cause.

- **Anemic domain models**: Types with only data fields and no behavior. Business logic
  lives in external functions that manipulate the type's internals. The type cannot
  enforce its own invariants. Flag as **Medium**.
  Exception: DTOs, API schemas (Pydantic BaseModel, TypedDict for serialization), and
  database row types are intentionally data-only. Only flag types that represent domain
  entities with invariants (e.g., `Task`, `Agent`, `Decision`).
  Fix: move validation and state-change logic into methods on the type.
- **Mutable internals exposed**: Type exposes mutable collections (lists, dicts, sets)
  via properties or public fields. External code can modify internal state without going
  through validation. Flag as **High**.
  Fix: return copies or read-only views. Use `@property` with defensive copying.
- **Invariants enforced only by documentation**: Comments say "must be positive" or
  "cannot be empty" but the constructor accepts any value. Flag as **Medium**.
  Fix: validate in `__init__` / constructor. Make illegal states unrepresentable.
- **Missing construction validation**: `__init__` or factory accepts raw user input
  without validating constraints. Invalid instances circulate through the system.
  Flag as **High**. Fix: validate at construction, raise on invalid input.
- **Inconsistent mutation guards**: Some setters validate but others don't. Some
  methods check preconditions but others assume valid state. Flag as **Medium**.
  Fix: all mutation paths must enforce the same invariants.
- **Type exposes implementation details**: Internal representation (e.g., underlying dict
  structure, SQL column names, wire format) leaks through the public API. Changing the
  implementation breaks all consumers. Flag as **Medium**.

#### `adversary-modeling`
For security-relevant code (auth, API endpoints, config, user input, permissions),
consider three adversary types (adapted from Trail of Bits' sharp-edges methodology):

1. **The Scoundrel** (malicious actor — attacker controlling input or config):
   - Can they disable security via configuration? (`verify_ssl: false`, `auth: off`)
   - Can they downgrade algorithms or bypass validation?
   - Can they inject malicious values through any input the code trusts?
   - Can they forge/replay tokens, sessions, or messages?

2. **The Lazy Developer** (copy-pastes examples, skips docs, deadline pressure):
   - Will the first example they find in the codebase be secure?
   - Is the path of least resistance the secure path?
   - If they forget a step (validation, cleanup, lock release), does the system
     fail safely or fail open?
   - Do error messages guide toward secure usage?

3. **The Confused Developer** (misunderstands the API contract):
   - Can they swap parameters without type errors? (e.g., `(key, nonce)` vs `(nonce, key)`)
   - Can they use the wrong enum variant or status string?
   - Are failure modes obvious or silent?
   - Does `0`, `""`, `null`, or `[]` for a security parameter disable the check?

Flag findings with the adversary type: "**High [Scoundrel]**: attacker can set
`timeout=0` to bypass rate limiting."

#### `insecure-defaults`
Adapted from Trail of Bits' insecure-defaults skill. Check for fail-open patterns:

- **Fallback secrets**: `env.get('SECRET') or 'default-key'` — app runs with weak
  secret if env var missing. Flag as **Critical** if it reaches auth/crypto paths.
- **Fail-open guards**: `if not config.get('auth_required'): pass` — missing config
  disables security instead of enforcing it. Secure default = deny.
- **Dangerous zero values**: What happens with `timeout=0`, `max_retries=0`,
  `rate_limit=0`? Does `0` mean "infinite" or "disabled" or "immediate"?
- **Boolean security flags**: `debug=True`, `skip_validation=True`,
  `allow_all_origins=True` — if the default is the insecure value, flag as **High**.
- **Hardcoded credentials in non-test code**: Any literal password, API key, or
  token outside of `test/`, `__tests__/`, or `.example` files. Flag as **Critical**.
- **Permissive CORS with credentials**: `Access-Control-Allow-Origin: *` combined
  with `credentials: true`. Flag as **Critical**.

### 4C. Confidence Scoring (MANDATORY for every finding)

Every finding you report MUST include a confidence score. This prevents false
positives from wasting the developer's time and ensures Critical findings are
backed by evidence, not pattern-matching hunches.

**Scale (0–100)**:

| Score | Meaning | Evidence Required |
|-------|---------|-------------------|
| 90–100 | **Certain** — you traced the data flow and confirmed the bug | Full code path traced, specific trigger described |
| 70–89 | **High confidence** — code clearly has the issue but you haven't traced every caller | Issue visible in diff, checked immediate context |
| 50–69 | **Moderate** — pattern matches a known antipattern but context might make it safe | Pattern identified, but mitigating code may exist elsewhere |
| 30–49 | **Low** — suspicious but could be intentional or guarded upstream | Flagging for developer to confirm, not asserting a bug |
| 0–29 | **Speculative** — do NOT report these | Suppress — not enough evidence |

**Filtering rules**:
- **Critical/High severity**: Only report if confidence ≥ 70
- **Medium severity**: Only report if confidence ≥ 50
- **Low/Nit**: Only report if confidence ≥ 50 (avoid noise)
- If you cannot reach the confidence threshold, investigate deeper before reporting.
  Read the surrounding code, trace the callers, check for upstream guards.
- **Never pad your review** with low-confidence findings to look thorough.
  Five high-confidence findings are worth more than twenty speculative ones.
- **ESCAPE HATCH — never suppress potential Critical findings**: If the potential
  impact is Critical (data loss, security vulnerability, silent corruption) but you
  cannot reach the 70 confidence threshold due to context limits or code complexity,
  report it anyway with an explicit "unverified" tag. Use the format:
  `**Critical [confidence: 55, unverified]**: ... — needs developer confirmation.`
  A false positive on a Critical issue wastes 5 minutes of developer time. A false
  negative on a Critical issue ships a security vulnerability. The cost is asymmetric.

Include the score in each inline comment: `**High [confidence: 85]**: ...`

### 4D. Finding Verification (for Critical/High findings)

Before reporting any **Critical** or **High** finding, verify it is a true positive —
not just pattern matching. For findings reported via the 4C escape hatch (`[unverified]`),
complete as many verification steps as possible and document which steps you could not
complete. The `[unverified]` tag signals that full verification was not achievable.

**For each Critical/High finding, answer these questions:**

1. **Restate the bug precisely**: "In `file.py:42`, when X happens, Y occurs
   because Z." If you can't restate it clearly, it's probably not real.
2. **Trace the data flow**: Follow the vulnerable input from source to sink.
   Is there validation, sanitization, or a guard upstream that prevents the issue?
3. **Check the callers**: Who calls this code? Do the callers constrain the input
   in a way that makes the bug unreachable?
4. **Find a concrete trigger**: Describe the exact request, input, or sequence
   that triggers the bug. If you can't construct a trigger, downgrade confidence.
5. **Devil's advocate**: Argue the opposite — why might this code be correct?
   What would the developer say in defense? If the defense is strong, downgrade.

**Rationalizations to reject** (from Trail of Bits):

| Rationalization | Why It's Wrong |
|---|---|
| "This pattern looks dangerous, so it's a vulnerability" | Pattern recognition is not analysis. Complete data flow tracing first. |
| "Similar code was vulnerable elsewhere" | Each context has different validation, callers, and protections. |
| "This is clearly critical" | LLMs are biased toward seeing bugs and overrating severity. Prove it. |
| "Skipping verification for efficiency" | Unverified findings waste more time than thorough analysis. |

If a finding survives verification, include the evidence in your comment:
"**Critical [confidence: 92]**: `deleteTask` at line 47 — when server returns 500,
`response.json()` consumes the body stream. The subsequent `.text()` fallback returns
empty string. Traced: no upstream guard exists. Trigger: any 500 from `/tasks/{id}`."

### 5. End-to-End Impact Analysis (DO NOT SKIP)

**This is what separates a good review from a superficial one.**
Do NOT just review the diff in isolation. Assess system-wide impact:

**Dependency tracing** (concrete techniques):
- For each changed function/class/API, search for ALL callers in the codebase:
  `grep -rn "function_name" --include="*.py"` or use `query_repo_context`
- Verify callers still work correctly with the new behavior
- Check if changed function signatures, return types, or error behavior break consumers
- Read the full function/class around a change, not just the changed lines

**Integration points**:
- Does this PR change any API contracts (HTTP endpoints, message schemas, config formats)?
- Are there other services, agents, or scripts that depend on the changed interfaces?
- If a message type or bus channel name changed, check ALL publishers and subscribers:
  `grep -rn "bus_publish\|publishes\|listens_to" --include="*.py" --include="*.yaml"`
- If a config key changed, check all consumers:
  `grep -rn "config_key_name" --include="*.py" --include="*.yaml"`

**Backward compatibility**:
- Can the system run with a mix of old and new code during deployment?
- Are database migrations needed? Are they reversible?
- Do config files need updates? Will old configs still work?
- Are existing API consumers broken by this change?

**Cross-PR conflicts**:
- Check open PRs for overlapping file changes
- Flag potential merge conflicts or semantic conflicts with in-flight work

> **Checkpoint**: For each changed file, you can explain what OTHER code
> in the repository is affected by this change and why it is safe.

### 5.5. Removal Candidates (check during review, report in summary)

While reviewing, watch for code that should be removed. LLM-generated PRs
frequently add new code paths without cleaning up the old ones they replace.

- **Dead code**: Functions, classes, or imports in the diff's files that are no
  longer called after this PR's changes. Use `grep` to verify zero callers.
- **Superseded logic**: Old implementation kept alongside new (e.g., both
  `fetchData()` and `fetchDataV2()` exist, but only V2 is called).
- **Feature-flagged-off code**: Code behind a flag that has been permanently
  off. If the PR doesn't clean it up, flag as **Low**: "Consider removing
  dead feature flag `X` and its code path."
- **Redundant fallbacks**: New code adds proper error handling, but the old
  `catch(() => [])` fallback is left in place. The fallback now masks the
  new error handling. Flag as **Medium**.

Report removal candidates in the review summary section, not as blocking issues
(unless the dead code creates confusion or maintenance burden). Use the format:
"**Removal candidate**: `functionName` in `file.py` — zero callers after this PR."

### 6. Post Inline Comments (MANDATORY — DO NOT SKIP)

**You MUST post inline comments on specific lines where issues exist.**
A single consolidated summary comment is NOT sufficient. Each issue MUST be
tied to the exact file and line where it occurs. Only post a summary comment
AFTER all inline comments are submitted.

Every file in the diff must be EXAMINED. For files with no issues, note them
in the summary section — do not post noise comments just to fill a checkbox.

Use the GitHub reviews API to submit a single review with inline comments:

```bash
# Get HEAD commit SHA and repo info
HEAD_SHA=$(gh api repos/{owner}/{repo}/pulls/{number} --jq '.head.sha')
```

Build a review JSON payload with a `comments` array. Each comment needs:
- `path`: file path from the diff
- `position`: line number within the diff hunk (not the file line number)
- `body`: review comment with severity label and analysis

```bash
# Submit review with inline comments in a single API call
gh api repos/{owner}/{repo}/pulls/{number}/reviews \
  --method POST \
  -f event="COMMENT" \
  -f body="Summary of review" \
  --input payload.json
```

Where `payload.json` contains:
```json
{
  "event": "COMMENT",
  "body": "## Review Summary\n...",
  "comments": [
    {"path": "src/file.py", "position": 42, "body": "**High**: Issue description..."}
  ]
}
```

For each inline comment include:
- **Severity label**: Critical, High, Medium, Low, Nit (non-blocking style)
- **Clear description** of the problem
- **Specific fix suggestion** — code snippet or approach, not just "fix this"
- **Constructive tone** — comment on the code, never the developer.
  Use "this line" or "we should" rather than "you did"
- **Impact scope** — does this issue affect just this file or propagate elsewhere?

**VERIFICATION GATE**: Before proceeding to Step 7, confirm:
- [ ] You posted at least one inline comment via `gh api` (not just `gh pr review`)
- [ ] Each inline comment references a specific file path and line
- If you have zero inline comments, you MUST go back and add them.
  A review with only a summary comment is INCOMPLETE and will be rejected.

### 7. Submit Review Verdict

Use the **pr_comment** tool to submit the final verdict:
- If critical or high issues: `event="request-changes"` with summary
- If only medium/low issues: `event="comment"` with summary
- If no issues: `event="approve"` with summary of what was checked

**MANDATORY**: If your identity.yaml defines `review_focus`, you MUST include a
`review_checklist` parameter when calling `pr_comment`. This is a JSON object mapping
each of your focus tags to its status:

```json
{
  "review_checklist": {
    "async-correctness": "checked",
    "platform-safety": "checked",
    "defensive-coding": "not_applicable",
    "data-integrity": "checked",
    "cross-module-impact": "skipped_with_reason: no cross-module changes in this PR"
  }
}
```

The tool will **reject** your review if any focus area is missing from the checklist.

### 8. Update Task Status and Publish Results (MANDATORY — DO NOT SKIP)

**This is the most commonly skipped step. If you skip it, the developer
is never notified and the task stays in review limbo.**

```bash
COORDINATOR="${AC_COORDINATOR_URL:-http://localhost:9889}"
TASK_ID="{task_id}"
AGENT_NAME="{your-agent-name}"

# If approving:
curl -s -X POST "${COORDINATOR}/tasks/${TASK_ID}/status?new_status=approved&agent_id=${AGENT_NAME}"

# If requesting changes:
curl -s -X POST "${COORDINATOR}/tasks/${TASK_ID}/status?new_status=changes_requested&agent_id=${AGENT_NAME}"
```

**Publish to bus** (use the `bus_publish` MCP tool):

If approving:
```json
{
  "channel": "work",
  "type": "review_approved",
  "message": {
    "pr_number": "{pr_number}",
    "task_id": "{task_id}",
    "verdict": "approved",
    "summary": "{brief summary of review}",
    "reviewer": "{your-agent-name}"
  }
}
```

If requesting changes:
```json
{
  "channel": "work",
  "type": "review_completed",
  "message": {
    "pr_number": "{pr_number}",
    "task_id": "{task_id}",
    "verdict": "changes_requested",
    "summary": "{brief summary of issues}",
    "reviewer": "{your-agent-name}"
  }
}
```

Update repo intelligence:
1. Create review trajectory for the files reviewed
2. Update known issues if new ones found

### Memory Commit — On the Reviewed Branch (NOT a Separate PR)

After updating your memory files, commit them to the **reviewed PR's branch** so
they ship with that PR merge. **NEVER create a separate PR for reviewer memory updates.**
Separate memory PRs conflict with main and create noise.

```bash
# Get the reviewed PR's branch name
BRANCH=$(gh pr view {pr_number} --json headRefName --jq '.headRefName')

# Checkout the branch, commit memory, push
git fetch origin
git checkout "$BRANCH"
git add .os/agents/reviewer/memory/
git commit -m "chore(reviewer): update memory with PR #{pr_number} review notes"
git push origin "$BRANCH"

# Return to your working branch
git checkout main
```

**If the PR is already merged** (branch deleted): create a short-lived feature branch,
commit memory there, and push. The coordinator will handle it. Do NOT push directly to main.

```bash
git checkout main && git pull
git checkout -b chore/reviewer-memory-pr{pr_number}
git add .os/agents/reviewer/memory/
git commit -m "chore(reviewer): update memory with PR #{pr_number} review notes"
git push origin chore/reviewer-memory-pr{pr_number}
```

> **Checkpoint**: Memory is committed. No new PR was created for the memory update.

> **Checkpoint**: Task status is `approved` or `changes_requested`.
> A `review_approved` or `review_completed` message exists on the work channel.

## Output Format

```
## PR Review: #[N] — [Title]

### Verdict: [Approved / Changes Requested]

### Design Assessment
[Is the overall approach sound? One paragraph.]

### End-to-End Impact
[What other code/systems are affected by this change? Any backward compat concerns?]

### Statistics
- Critical: [count]
- High: [count]
- Medium: [count]
- Low: [count]
- Total comments: [count]

### Critical Issues
1. [file:line] — [description] — [impact on callers/system]

### High Priority
1. [file:line] — [description] — [impact on callers/system]

### Summary
- Design: [sound / N concerns]
- Security: [pass / N issues]
- Correctness: [pass / N issues]
- Performance: [pass / N issues]
- Testing: [pass / N issues]
- Backward Compatibility: [safe / N concerns]

### Recommendation
[Approve / Request changes — specific actions needed]
```

## Self-Audit (Before Submitting Verdict)

Before posting your review, verify you completed every review dimension:

```
SELF-AUDIT (Universal):
- [ ] Functional flow: I traced trigger → processing → side effects → output → error path
- [ ] Design: I assessed the overall approach, not just code details
- [ ] Security: I ran the full OWASP-aligned checklist (11 items)
- [ ] Impact: I traced callers/consumers for every changed function/API
- [ ] Backward compat: I checked if existing consumers break
- [ ] Cross-PR: I checked for conflicting open PRs
- [ ] Framework: Templates updated before .os/? Both execution paths checked?
- [ ] No DEVELOPER memory files (.os/agents/*/memory/) leaked into the PR? (Reviewer's own memory commits are intentional — not a leak.)
- [ ] Lifecycle: I will update task status AND publish bus notification

SELF-AUDIT (Review Profile — one per review_focus tag):
- [ ] Each review_focus tag from my identity.yaml has been checked
- [ ] review_checklist JSON object is complete with all focus tags
- [ ] No focus tag left unaddressed (use "not_applicable" if genuinely N/A)
```

If any box is unchecked, go back and complete it before submitting.

## Quality Criteria

- [ ] Design assessment completed — overall approach evaluated
- [ ] All changed files examined (not just the first few)
- [ ] Full security checklist completed (OWASP-aligned, 11 items)
- [ ] End-to-end impact assessed — callers traced, API contracts checked
- [ ] Backward compatibility verified for changed interfaces
- [ ] Issues categorized by actual severity (not inflated)
- [ ] Inline comments include specific fix suggestions with code
- [ ] Review tone is constructive — comments on code, not developer
- [ ] Summary includes design assessment and impact analysis
- [ ] Repository intelligence updated after review
- [ ] Task status updated via coordinator API
- [ ] Bus notification published with correct message type

## Common Mistakes

- **Reviewing only the diff, not the context** — Consequence: miss regressions in callers, break integration points, approve changes that look correct in isolation but fail system-wide.
  **Fix**: Read the full function/class around each change. Search for callers with grep. Check API consumers.

- **Skipping design review** — Consequence: approve a fundamentally wrong approach that passes all code-level checks. Harder to fix later.
  **Fix**: Always start with Section 3 (Design Review). Ask: "Is this the right approach?"

- **Superficial review** — Consequence: bugs and security issues reach production.
  **Fix**: Go deep on every file. Check logic, security, edge cases.

- **Severity inflation** — Consequence: developers learn to ignore your reviews.
  **Fix**: Reserve Critical for security vulns and data loss. Style nits are "Nit:" prefix.

- **No fix suggestions** — Consequence: developer doesn't know how to fix the issue.
  **Fix**: Always include a specific code suggestion or approach.

- **Skipping security checklist** — Consequence: vulnerabilities sneak through.
  **Fix**: Run the full 11-item security checklist for every PR, even small ones.

- **Not checking backward compatibility** — Consequence: deployed change breaks existing API consumers, config files, or dependent agents.
  **Fix**: For every changed interface, ask "who calls this?" and "will they break?"

- **Not loading repo context** — Consequence: miss context-specific issues.
  **Fix**: Use `query_repo_context` before starting the review.

- **Wrong bus type on completion** — Consequence: developer handles `review_completed` (changes requested) differently from `review_approved`. Wrong type = wrong developer action.
  **Fix**: Use `review_approved` for approvals, `review_completed` for changes requested.

- **Not updating task status** — Consequence: task stays in `review` forever. Developer never gets notified. Task lifecycle is broken.
  **Fix**: Always call `POST /tasks/{task_id}/status` with `approved` or `changes_requested`.

- **Creating a separate PR for reviewer memory updates** — Consequence: separate `chore(reviewer): update memory` PRs conflict with main and accumulate, requiring manual cleanup.
  **Fix**: Commit memory to the reviewed PR's branch BEFORE submitting the verdict (see Section 8 Memory Commit step). If the branch is already merged, create a short-lived `chore/reviewer-memory-pr{N}` branch and push — never push directly to main.

## Completion

A PR review is complete when ALL of these are true:
- [ ] Design assessed — overall approach is sound (or issues flagged)
- [ ] All changed files reviewed against the full checklist
- [ ] End-to-end impact assessed — callers traced, backward compat verified
- [ ] Inline comments posted for substantive issues found
- [ ] Summary review submitted with correct verdict
- [ ] Repository intelligence updated (trajectory, known issues)
- [ ] Memory committed to reviewed PR's branch (or to a chore/reviewer-memory-prN branch if already merged) — NOT a separate PR and NOT directly to main
- [ ] Task status updated (`approved` or `changes_requested`)
- [ ] Bus notification published with correct message type
