---
name: rootbuild
description: New-feature build mode that respects existing patterns and never merges without tests. Use when user wants to add a new feature (not fix bugs, not refactor) — new API endpoint, new module, new functionality. Forces requirement clarification, existing-pattern survey, design proposal, and test-coupled implementation before any code is written.
triggers:
  - 기능 추가
  - 기능 추가해줘
  - 새 기능
  - 신규 기능
  - 새로운 기능
  - 추가해줘
  - 추가하고 싶어
  - 만들고 싶어
  - 구현해줘
  - 구현하고 싶어
  - 빌드해줘
  - build
  - implement
  - add feature
  - new feature
  - 이런 기능
  - 이런거 만들고
  - 루트빌드
  - rootbuild
---

# rootbuild — Pattern-Respecting Build Mode

Add a new feature. **But be a citizen of the existing codebase.** Don't introduce new patterns. Don't merge without tests. Don't bundle multiple features in one PR.

## Activation

Explicit: `/rootbuild`

Auto-triggers:
- "기능 추가", "새 기능", "신규 기능"
- "추가해줘", "구현해줘", "만들어줘"
- "이런 기능 넣어줘"
- "X 같은 거 만들어줘"
- "build", "implement", "add feature"

**Note**: When the user explicitly invokes another skill (e.g., "autopilot으로 만들어줘"), rootbuild stays inactive. autopilot builds from scratch; rootbuild slots into existing code.

## What's Different (vs general / autopilot)

| General Mode | rootbuild | autopilot |
|---|---|---|
| Introduce new patterns freely | **Follow existing patterns** | Design from scratch OK |
| Tests later | **Tests must be paired with code** | Auto QA cycle |
| Bundle multiple features in one PR | **One PR = one feature** | Build big features whole |
| Add dependencies freely | **User approval required** | Auto-add allowed |
| Works = good enough | **Verify no existing breakage** | Multi-perspective review |

## The Two Anti-Patterns (encoded by real experience)

### A. "Ignore existing patterns, introduce new ones"
The most common and most damaging anti-pattern. The #1 reason codebases become inconsistent over time.

**Python signal**:
```python
# BAD: existing code uses FastAPI dependency injection
@app.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == id).first()

# new feature suddenly uses global state
db_connection = create_engine(...)  # module level!

@app.get("/products/{id}")
def get_product(id: int):
    with db_connection.connect() as conn:  # ← ignores existing pattern
        return conn.execute(...).fetchone()
```

**Mitigation**:
1. **Always grep first**: find how similar features are implemented
   - `grep -rn "@app.get" .` (FastAPI pattern)
   - `grep -rn "class.*Service" .` (Service pattern)
2. **Confirm pattern via 3+ examples** before extracting it
3. New code follows that pattern **exactly**
4. If existing pattern is truly bad → exit rootbuild, fix via rootclean first

### B. "Merge without tests"
"I'll add them later" → never happens. Regressions can't be caught.

**Python signal**:
- PR has N new functions, 0 new tests
- Existing `test_*.py` exists, new module missing
- Only "I ran it manually" in PR description

**Mitigation**:
- **One commit = function + test** always paired
- Use pytest fixtures (follow existing patterns)
- Minimum 3 cases:
  - Happy path
  - Edge case (boundary, empty, null)
  - Error path
- Mocks follow project conventions (`unittest.mock` vs `pytest-mock`)

## Python Pattern Checklist

Before adding new feature, check via grep:

| Item | Grep command | Check |
|---|---|---|
| **API pattern** | `grep -rn "@app.\(get\|post\)"` | FastAPI? Flask? Django? |
| **DB access** | `grep -rn "Session\|engine\|cursor"` | SQLAlchemy ORM? Raw SQL? |
| **Auth** | `grep -rn "Depends\|@require\|auth"` | What middleware? |
| **Error handling** | `grep -rn "raise HTTPException\|class.*Error"` | Custom exception? HTTPException? |
| **Logging** | `grep -rn "logger\|logging\|print"` | structlog? standard logging? |
| **Config** | `grep -rn "os.environ\|settings\|Config"` | pydantic-settings? dotenv? |
| **Tests** | `grep -rn "fixture\|conftest"` | pytest fixture location? |
| **Type hints** | `grep -rn ": .*->\|TypedDict"` | How much typing? |
| **async** | `grep -rn "async def\|asyncio"` | sync or async? |
| **Dependencies** | `cat pyproject.toml \| requirements.txt` | Available packages? |

## 6-Step Workflow

### 1. Requirement Clarification — Ask immediately if vague
Preferred workflow: **systematic** (requirements → design → implementation). Never jump to code.

Question priority:
- **What**: exact input/output? (1-2 example data points)
- **Who**: auth needed? permissions?
- **When**: sync? async? batch?
- **How**: part of existing domain or new?
- **On failure**: how to handle? retry? error?

If answers are vague, **ask again, don't guess**. autopilot's deep-interview philosophy.

### 2. Existing Pattern Learning — Force grep
Once requirements are clear, immediately grep:
- Similar feature exists? (if yes, follow its structure exactly)
- API style? DB access? Error handling?
- Where are tests? How?
- New dependency needed? (if yes, check for existing similar package first)

**Confirm via 3+ examples** before extracting a pattern. 1 example might be a fluke.

### 3. Design Proposal — Show before writing code
Show the user:
- **New file location**: `services/notifications.py` (existing `services/` pattern)
- **Function signature**: input/output types
- **Dependency graph**: which existing modules to import?
- **Impact scope**: which existing functions are affected?
- **Pattern match**: "Same structure as existing user_service.py"
- **Test plan**: `test_notifications.py` — happy/edge/error cases

**Never write code without user approval**.

### 4. Incremental Implementation — Inside out
Implementation order:
1. **Types/Schema first**: Pydantic model, TypedDict, dataclass
2. **Tests first (optional)**: write failing test → make it pass
3. **Pure functions first**: I/O-free logic
4. **I/O integration**: DB, API, external calls
5. **Endpoint/Entry point**: HTTP route, CLI command, Lambda handler

**Each step paired with 1+ test**. No "test after everything's done".

### 5. Integration Verification — No breakage
Don't only check the new feature. Verify:
- **All tests**: `pytest` passes all
- **Type check**: `mypy` passes (if used)
- **Lint**: `ruff check` passes
- **Manual check**: new feature 1x + critical existing scenario 1x

```bash
pytest                # all tests
pytest -k new_feature # new feature only
mypy .                # types
ruff check .          # lint
```

### 6. PR Separation — 1 feature = 1 PR
Don't mix in one PR:
- ❌ "feature add + bug fix + refactor"
- ✅ PR 1: feature add only
- ✅ PR 2: bug fix → rootfix
- ✅ PR 3: refactor → rootclean

PR description must include:
- What was added
- Which existing pattern was followed (file path explicit)
- How tests were done
- Dependency additions (if any, with reason)

## Anti-Patterns (Forbidden in this mode)

1. **Write code without grep** — Always grep first
2. **Introduce new patterns** — "This is more modern" rejected. Separate PR via rootclean.
3. **No-test implementation** — "Urgent, just do it" absolutely forbidden
4. **Multiple features in one PR** — "While I'm here" forbidden
5. **Unauthorized dependencies** — New package = explicit user approval
6. **Guess vague requirements** — Ask, don't guess
7. **Manual test = OK** — "I ran it once" ≠ verification

## Output Format

When receiving a feature request, answer in this order:

```
[Requirement Check]
- Input: <type + example>
- Output: <type + example>
- Auth/permissions: <required?>
- On failure: <handling>
(If vague → ask, continue after answer)

[Existing Pattern Survey]
grep results:
- API pattern: <FastAPI Depends, ref services/user.py>
- DB access: <SQLAlchemy session, repositories/ pattern>
- Error handling: <HTTPException used>
- Tests: <pytest fixture in conftest.py>

[Design Proposal]
New file: <path>
Signature: <function/endpoint>
Dependencies: <existing imports only / no new packages>
Impact: <which existing code is affected>
Test plan: <file name + 3 cases>

Proceed?
```

## Termination Conditions

Exit rootbuild mode only when ALL of:
- Requirements unambiguous
- Existing pattern grep done + new code follows it
- Design approved by user
- Tests written alongside code (paired commit)
- All tests + types + lint pass
- PR scope is one feature

## Notes

- This skill encodes anti-patterns observed in Python (Lambda, FastAPI, AI/ML) work: introducing new patterns instead of following existing ones, and merging without tests.
- Preferred workflow: requirements clarification → design → implementation (systematic).
- Pair with rootfix and rootclean. rootfix changes behavior (bug fixes), rootclean preserves behavior (cleanup), rootbuild adds (new features). Don't mix.
- Small features → regular conversation. Activate this for medium+ feature additions (1+ file).
- Bigger greenfield projects → autopilot is better (rootbuild is for slotting into existing code).
- Works in any project. Global skill.
