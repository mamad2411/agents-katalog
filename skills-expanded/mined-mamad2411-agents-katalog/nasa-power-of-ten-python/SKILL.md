---
name: nasa-power-of-ten-python
description: >
  Audit Python, FastAPI, or long-running service code against a 12-rule
  reliability discipline adapted from NASA JPL's Power of Ten rules and extended
  for AI-generated code. Use whenever a user asks to review, audit, or refactor
  code for reliability, production safety, or correctness -- especially for
  FastAPI services, background workers, daemons, or any long-running process.
  Trigger even when the user says things like "my code has silent failures",
  "I have a memory leak", "improve code quality", "make this more robust",
  "is this safe to ship", "audit this", or "review this for production".
  Produces a severity-ranked findings report with a rule-by-rule summary and a
  ship / do-not-ship verdict.
---

# NASA JPL Power of Ten — 12-Rule Audit for Python & AI-Assisted Code

**Category:** Code Quality | Reliability | Python Best Practices
**Skill Level:** Advanced

**Sources.** The rules descend from Gerard Holzmann's
[Power of Ten — Rules for Developing Safety Critical Code](https://spinroot.com/gerard/pdf/P10.pdf)
(NASA/JPL, 2006). The 12-rule audit structure, severity taxonomy, and rules 10–12
are adapted from [LordMoMA/AI_skills](https://github.com/LordMoMA/AI_skills),
extended for LLM-generated code. The Python/FastAPI translations and worked
examples are this repository's contribution.

---

## Overview

NASA's JPL applies the Power of Ten rules to C programs running on Mars rovers —
software where a single bug cannot be patched after launch. The core insight is
that **rules which remove entire classes of bugs are more valuable than rules
that catch individual bugs**.

Applied to Python/FastAPI, these rules surface hidden failures, prevent resource
exhaustion, and make code dramatically easier to review and test. This is not
about risk parity with spacecraft software. It is about borrowing a proven *way
of thinking* that pays off at any scale.

**Read the actual code.** Do not audit from filenames, diffs, or assumptions.

---

## The 12 Rules (Quick Reference)

| # | Rule | Intent | Python / FastAPI Translation |
|---|------|--------|------------------------------|
| 1 | Keep it linear | No `goto`, no unbounded recursion | No nesting >2 deep; no exception-driven flow; no bare `except` |
| 2 | Bound every loop | Every loop provably terminates | `while` gets an enforceable cap or timeout; retry/poll/crawl loops are 🔴 |
| 3 | Know what you own | Every resource closed on every path | `with` / `async with` everywhere; bounded growth in long-lived structures |
| 4 | One function, one job | ≤ 60 lines, one responsibility | Route handlers delegate; no function describable only with "and" |
| 5 | State your assumptions | Assert invariants in code | Replace `assert` with `if`/`raise` that survives `-O`; validate at trust boundaries |
| 6 | Never swallow errors | Every failure surfaces | No `except: pass`, empty catches, ignored return codes, discarded `err` |
| 7 | Narrow your state | Scope state as tightly as possible | No module globals, wide mutable state, or class-level passthrough |
| 8 | Surface your side effects | I/O visible at the call site | Do not hide network/DB/disk writes in innocuously-named helpers |
| 9 | One layer of magic | Nothing obscures what runs | Stacked decorators, middleware chains, dynamic dispatch, callback pyramids |
| 10 | Warnings are errors | Static analysis must block | Linter/typechecker must be exit-code-failing in CI, not advisory |
| 11 | Read every line | No unreviewed AI artifacts | Dead code, commented-out "just in case", `data`/`result`/`temp` in critical paths |
| 12 | Tests first | Production code has a failure-mode test | New behaviour ships with a test covering at least one failure |

---

## Severity

Use these tags on every finding. Do not invent tags.

- 🔴 **Critical** — silent data loss, resource leak, swallowed error, unbounded loop in a production path
- 🟠 **High** — likely bug, missing invariant check, side-effect surprise
- 🟡 **Medium** — maintainability hazard, comprehension cost
- 🟢 **Low** — style / clarity nit
- ℹ️ **Info** — observation or good practice noted

---

## Detailed Rules

### Rule 1: Keep it linear

**Original purpose.** Eliminate `goto`, `setjmp`/`longjmp`, and unbounded recursion. When control flow is complex you cannot confidently trace what the program will do.

**Python / FastAPI.** Python has no `goto`, but the equivalent traps exist: nesting more than two levels deep, recursion without an explicit base-case bound, and — most commonly — using broad `except` clauses to redirect execution. The last is Python's `goto`: it makes the real path invisible.

**❌ Violates**
```python
def get_user(user_id):
    try:
        return db.query(User).filter(User.id == user_id).first()
    except:
        return None
```

**✅ Follows**
```python
def get_user(user_id):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        logger.warning("User not found", extra={"user_id": user_id})
    return user
```

> Reported impact: removing bare `except` blocks in one codebase exposed two production bugs that had been silently failing for months.

---

### Rule 2: Bound every loop

**Original purpose.** Every loop must have a provable maximum iteration count. An unbounded loop can freeze a system with no recovery path.

**Python / FastAPI.** `while` loops without explicit termination are the primary offender. Polling, retry, and crawl loops are 🔴 by default: a task flag that never flips, a queue that never drains, and the loop runs until the process dies.

**❌ Violates**
```python
while not task_complete:
    process_next_item()
    time.sleep(1)
```

**✅ Follows**
```python
MAX_ATTEMPTS = 300
for attempt in range(MAX_ATTEMPTS):
    if task_complete:
        break
    process_next_item()
    time.sleep(1)
else:
    logger.error("Task did not complete within timeout")
    raise TaskTimeoutError("Exceeded maximum attempts")
```

For genuinely continuous workers, bound by wall-clock instead of iteration count — an unbounded `asyncio` consumer should carry a heartbeat and a shutdown deadline, not a counter.

> Reported impact: three unbounded `while` loops in background workers were found that would have consumed all server memory under specific failure conditions.

---

### Rule 3: Know what you own

**Original purpose.** No `malloc` after initialization. In fixed-RAM embedded systems, unbounded allocation causes unpredictable failure.

**Python / FastAPI.** Two distinct failures live here. First, **resource leaks**: every opened resource — file handle, DB connection, lock, socket, subscription — must be released on every exit path, including the error path. Second, **unbounded growth** in long-lived structures.

**❌ Violates**
```python
class EventProcessor:
    def __init__(self):
        self.processed_events = []          # grows forever

    def process(self, event):
        result = handle_event(event)
        self.processed_events.append(result)
        return result


def load_rows(conn):
    cur = conn.cursor()
    cur.execute("SELECT ...")
    return cur.fetchall()                    # cursor never closed
```

**✅ Follows**
```python
from collections import deque

class EventProcessor:
    def __init__(self, max_history=1000):
        self.processed_events = deque(maxlen=max_history)   # bounded by design


def load_rows(conn):
    with conn.cursor() as cur:              # closed on every path
        cur.execute("SELECT ...")
        return cur.fetchall()
```

> **Scope note.** Unlike embedded systems, web apps legitimately use dynamic memory per request. This rule targets **long-lived, accumulating** structures and unclosed resources — not normal per-request allocation.

> Reported impact: unbounded instance-variable lists were the direct root cause of a confirmed memory leak in a long-running background process.

---

### Rule 4: One function, one job

**Original purpose.** No function longer than one printed page (~60 lines). A single clear responsibility is easier to verify, test, and reason about.

**Python / FastAPI.** FastAPI route handlers are the most common violation. A handler that validates a user, checks a balance, writes the DB, sends email, and updates inventory is doing six jobs — six failure modes, six places where error handling can be silently omitted.

**❌ Violates**
```python
@app.post("/orders")
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.id == order.user_id))
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.balance < order.total:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    new_order = Order(**order.dict())
    db.add(new_order)
    user.balance -= order.total
    await db.commit()
    await send_confirmation_email(user.email, new_order.id)
    await update_inventory(order.items)
    return new_order
```

**✅ Follows**
```python
@app.post("/orders")
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    user = await get_verified_user(db, order.user_id)
    await verify_sufficient_balance(user, order.total)
    new_order = await save_order(db, order, user)
    await post_order_tasks(user, new_order, order.items)
    return new_order
```

> Reported impact: splitting four multi-responsibility handlers revealed two missing error-handling paths that were unreachable in the monolithic version.

---

### Rule 5: State your assumptions

**Original purpose.** Assert that every condition you believe to be true actually is. If an assertion fails, your model of the code did not anticipate reality.

**Python / FastAPI.** Python's `assert` is **silently disabled** under `-O`, giving false confidence in exactly the environments where you need it. The correct equivalent is explicit guards that always run, plus validation at trust boundaries (Pydantic models for API input, type checks at module edges).

**❌ Violates**
```python
def calculate_discount(amount, rate):
    assert amount > 0, "Amount must be positive"
    assert 0 <= rate <= 1, "Rate must be between 0 and 1"
    return amount * rate
```

**✅ Follows**
```python
def calculate_discount(amount: float, rate: float) -> float:
    if amount <= 0:
        raise ValueError(f"Amount must be positive, got {amount}")
    if not 0 <= rate <= 1:
        raise ValueError(f"Rate must be between 0 and 1, got {rate}")
    return amount * rate
```

> Reported impact: adding explicit checks to internal utilities caught three cases of incorrect data being silently passed between functions.

---

### Rule 6: Never swallow errors

**Original purpose.** Every failure must be handled explicitly. Silent failure is worse than a crash, because the system keeps running on wrong data.

**Python / FastAPI.** This is the highest-yield rule in Python, and the most commonly violated. `except: pass`, empty `except` blocks, ignored return codes from `subprocess`/`os`, and discarded `err` values from Go-style callback APIs all produce code that looks correct and is not.

**❌ Violates**
```python
try:
    result = process_payment(order)
except Exception:
    pass                      # failure is invisible forever

try:
    cleanup()
except:                      # bare, catches KeyboardInterrupt too
    pass

subprocess.run(["migrate"], check=False)   # exit code discarded
```

**✅ Follows**
```python
try:
    result = process_payment(order)
except PaymentDeclined as exc:
    logger.warning("Payment declined", extra={"order_id": order.id, "reason": str(exc)})
    raise
except Exception:
    logger.exception("Unexpected payment failure", extra={"order_id": order.id})
    raise

try:
    cleanup()
except Exception:
    logger.exception("Cleanup failed")

proc = subprocess.run(["migrate"], check=False, capture_output=True, text=True)
if proc.returncode != 0:
    raise MigrationError(f"migrate failed ({proc.returncode}): {proc.stderr}")
```

> Severity floor: swallowed errors in a production path are 🔴 even when the code looks clean.

---

### Rule 7: Narrow your state

**Original purpose.** Keep data objects scoped as tightly as the compiler allows. Shared mutable state is the root of a large share of concurrency bugs.

**Python / FastAPI.** Module-level globals, class-level mutable attributes used as passthrough, and caches with no invalidation policy. Under ASGI, module globals are also shared across concurrent tasks, so a race is not hypothetical.

**❌ Violates**
```python
CURRENT_USER = None           # module global, shared across tasks
_CACHE = {}

def get_user(uid):
    if uid in _CACHE:         # unbounded, never invalidated, not thread-safe
        return _CACHE[uid]
    user = fetch(uid)
    _CACHE[uid] = user
    return user
```

**✅ Follows**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)     # bounded, explicit, has invalidation semantics
def get_user(uid: str) -> User:
    return fetch(uid)


async def current_user(request: Request) -> User:
    return request.state.user     # per-request scope
```

---

### Rule 8: Surface your side effects

**Original purpose.** I/O and mutation should be visible where they happen, not hidden inside a helper whose name does not promise them.

**Python / FastAPI.** A function called `build_order()` that also writes to the database, sends an email, and decrements inventory will be called from somewhere that believes it is pure. The bug surfaces three files away.

**❌ Violates**
```python
def build_order(items):
    order = Order(items=items)
    db.add(order)
    db.commit()                  # writes, undeclared
    send_email(order)            # network, undeclared
    return order
```

**✅ Follows**
```python
def build_order(items) -> Order:          # pure
    return Order(items=items)


async def persist_and_notify(order: Order) -> None:
    """Writes the order and sends confirmation."""
    db.add(order)
    await db.commit()
    await send_email(order)
```

Name the side effect in the function name or the docstring. If the docstring needs a paragraph to mention the database, that is the smell.

---

### Rule 9: One layer of magic

**Original purpose.** Restrict indirection. Stacked decorators and dynamic dispatch obscure what actually executes, which defeats review and debugging.

**Python / FastAPI.** Stacked decorators, deep middleware chains, metaclass magic, dynamic `__getattr__` dispatch, and callback pyramids. Every layer is a hop you must trace during an incident.

**❌ Violates**
```python
@app.post("/orders")
@require_auth
@rate_limit(100)
@validate_schema(OrderCreate)
@retry(3)
@log_requests
@timed
async def create_order(order):     # six layers before the body
    ...
```

**✅ Follows**
```python
async def create_order(request: Request, db: AsyncSession = Depends(get_db)):
    payload = OrderCreate.model_validate(await request.json())
    return await handle_order(payload, db)
```

Cross-cutting concerns belong in one dependency or one middleware — not stacked five deep.

---

### Rule 10: Warnings are errors

**Original purpose.** Static analysis must be authoritative. Advisory tooling is decoration.

**Python / FastAPI.** Check that the linter and type checker are configured *and enforcing*. A `ruff` or `mypy` block in `pyproject.toml` that CI runs without `--exit-zero` and without a failure threshold does nothing.

**What to verify**
- Does CI run the linter on every commit, or only on `main`?
- Is the exit code checked, or is the output informational?
- Is `mypy`/`pyright` non-optional in CI, and does the config fail on error?
- Are tests actually gated (`--exitfirst`, coverage floor) or just reported?

**❌ Violates**
```yaml
- run: uv run ruff check . || echo "lint issues found"   # always passes
- run: uv run mypy src/ --ignore-errors                 # advisory only
```

**✅ Follows**
```yaml
- run: uv run ruff check --exit-zero=false .
- run: uv run mypy --strict src/
- run: uv run pytest --cov=src --cov-fail-under=80 -x
```

Missing configuration is 🟠. Configuration that does not block is 🟠.

---

### Rule 11: Read every line

**Original purpose.** Not from NASA — added for LLM-generated code. Generated code arrives plausible and unreviewed, and reviewers skim it because it reads well.

**Python / FastAPI.** The tells:

- Dead code and unused imports left from an earlier draft
- Commented-out blocks kept "just in case"
- Over-defensive `try/except` wrapping trivial operations
- Generic names — `data`, `result`, `temp`, `val`, `obj` — on critical paths
- Comment density that describes *what* rather than *why*
- Docstrings that restate the function name

**❌ Violates**
```python
def process(payload):
    # old approach, keeping for reference
    # return payload.map(lambda x: x.strip())

    tmp = data          # what is `data`?
    result = transform(tmp)
    return result
```

**✅ Follows**
```python
def process(raw_payload: dict) -> list[ChargeRecord]:
    """Convert a raw Stripe payload into charge records.

    Strips zero-amount entries, which Stripe emits for refunded invoices.
    """
    charges = [ChargeRecord.from_stripe(c) for c in raw_payload["charges"]]
    return [c for c in charges if c.amount_cents > 0]
```

---

### Rule 12: Tests first

**Original purpose.** Added for AI-assisted development. Code that was generated faster than it was understood needs an executable statement of intent.

**Python / FastAPI.** New or changed production behaviour ships with a test that covers **at least one failure mode**. A test that only exercises the happy path documents nothing about what the function is for.

**What to verify**
- Does the change have a corresponding test?
- Does at least one test assert the error branch?
- Are the failure modes from Rules 2, 5, and 6 (timeout, invalid input, swallowed error) covered?

**❌ Violates**
```python
def test_discount():
    assert calculate_discount(100, 0.1) == 10     # happy path only

# no test for calculate_discount(-1, 0.1) -> ValueError
```

**✅ Follows**
```python
def test_discount_happy_path():
    assert calculate_discount(100, 0.1) == 10


def test_discount_rejects_non_positive_amount():
    with pytest.raises(ValueError, match="Amount must be positive"):
        calculate_discount(-1, 0.1)


def test_discount_rejects_out_of_range_rate():
    with pytest.raises(ValueError, match="Rate must be between 0 and 1"):
        calculate_discount(100, 1.5)
```

If a change is config-, docs-, or types-only, mark Rule 12 N/A rather than inventing a finding.

---

## Audit Procedure

1. **Establish scope.** If the user named a target (file, directory, glob, `staged`, `branch`), use it. Otherwise:
   - git repo with staged changes → audit `git diff --cached`
   - on a non-default branch → audit `git diff <default-branch>...HEAD`
   - otherwise → **ask the user what to audit. Do not guess.**
2. **Read the actual files.** Never audit from filenames or the diff alone.
3. **Walk the 12 rules in order.** Record findings with `file:line` and the offending snippet quoted.
4. **Assign severity** from the taxonomy above.
5. **Report** using the output contract below.

### Guidelines

- **Be specific.** "This function is too long" is useless. "`handle_request` at `api.py:240` is 142 lines and mixes auth, validation, and persistence — split into three" is useful.
- **Cite line numbers** from the actual file, not from a diff hunk header.
- **Do not invent violations.** If the code is clean for a rule, say so in the summary table.
- **Do not flag stylistic preference as a violation.** Every finding traces to one of the 12 rules.
- **Skip generated code, vendored dependencies, and migrations** unless the user explicitly includes them.

---

## Output Contract

Print to the terminal. Do not write a file unless asked.

```
# NASA Power-of-Ten Audit

**Target:** <what was audited>
**Files reviewed:** N

## Findings

### 🔴 Critical (N)
- `path/to/file.ext:LINE` — Rule N (name) — one-line issue
  ```lang
  offending snippet
  ```
  **Fix:** concrete suggestion.

### 🟠 High (N)
### 🟡 Medium (N)

## Rule-by-rule Summary

| Rule | Status |
|------|--------|
| 1. Keep it linear | ✅ / N violations |
| 2. Bound every loop | ... |

## Verdict

One paragraph: is this safe to ship, and what must change first?
```

---

## Limitations

Not every rule translates equally to web application context. Do not apply them mechanically.

| Rule | Limitation |
|------|------------|
| 3. Know what you own | Web apps legitimately allocate per request. Apply only to long-lived accumulating structures and unclosed resources. |
| 1. Keep it linear | Python carries a recursion limit already; most web code cannot stack-overflow. Recursion without an explicit base-case bound is still worth flagging. |
| 2. Bound every loop | Some workers legitimately run indefinitely. Bound by wall-clock or heartbeat, not iteration count. |
| 5. State your assumptions | Over-validating internal invariants adds cost without safety. Concentrate on trust boundaries. |
| 9. One layer of magic | Framework-mandated indirection is not a finding. Flag indirection you introduced. |
| 10. Warnings are errors | A repo with no type checker at all is a judgement call — report it as info, not as a blocker. |
| 12. Tests first | Absence of tests on legacy code is context, not a violation. Apply to changed code. |

**The value is not mechanical compliance.** It is understanding *why* each rule
exists and applying that reasoning to your system's actual risk profile.

---

## Example Usage

### Example 1 — Whole-repo reliability audit

> "Review this FastAPI background worker for reliability issues."

The agent establishes scope (asks, or uses staged changes), reads the file, walks
all 12 rules, finds a bare `except` at line 23 (Rule 1) and an unbounded
`while True` at line 41 (Rule 2), emits both as 🟠, produces the rule-by-rule
table marking the clean rules ✅, and returns a verdict.

### Example 2 — Targeted diagnosis

> "I have a memory leak somewhere in my event processor class."

The agent scans for long-lived instance variables (Rule 3), finds an unbounded
list accumulating processed events, proposes `deque(maxlen=1000)`, and notes the
same code also drops `cur.close()` on an error path.

### Example 3 — Pre-merge gate

> "Is this safe to ship?"

The agent runs all 12 rules, includes Rule 10 by checking whether CI actually
enforces lint and types rather than merely running them, and returns a verdict
paragraph naming the specific blocking findings.