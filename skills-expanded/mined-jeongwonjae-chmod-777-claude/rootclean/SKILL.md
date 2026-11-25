---
name: rootclean
description: Refactor-only mode that preserves behavior while removing code smells. Use when user wants to clean up code (not fix bugs, not add features) — duplication, long functions, naming inconsistency, magic numbers. Forces baseline capture, pattern recognition, behavior-preserving transforms, and commit separation before any change.
triggers:
  - 리팩토링
  - 리팩터링
  - 리팩토링해줘
  - refactor
  - 정리해줘
  - 코드 정리
  - 클린업
  - cleanup
  - 단순화
  - 간결하게
  - simplify
  - 가독성
  - 읽기 쉽게
  - 깔끔하게
  - 깨끗하게
  - 중복 제거
  - DRY
  - 매직 넘버
  - magic number
  - 너무 길어
  - 함수가 길어
  - 너무 복잡해
  - 루트클린
  - rootclean
---

# rootclean — Behavior-Preserving Refactoring Mode

Make code better. **But behavior must NEVER change.** If you also want to fix a bug, do it in a separate PR. If you also want to add a feature, definitely a separate PR. One thing at a time.

## Activation

Explicit: `/rootclean`

Auto-triggers:
- "리팩토링", "리팩터링", "refactor"
- "정리해줘", "클린업", "cleanup"
- "단순화", "간결하게", "더 깔끔하게"
- "가독성", "읽기 쉽게"
- "중복 제거", "DRY"
- "매직 넘버", "magic number"
- "함수가 너무 길어", "너무 복잡해"

## What's Different (vs general / rootfix)

| General Mode | rootclean | rootfix |
|---|---|---|
| Behavior may change | **Behavior must be preserved** | Behavior changes (bug fixed) |
| Clean everything at once | **Split into small units** | Trace until root cause found |
| Skip tests | **100% tests must pass** | Add regression tests |
| Mix in one commit | **One transform = one commit** | Execute after option chosen |
| "While I'm here" creep | **Block scope creep** | Identify same pattern elsewhere |

## The Four Code Smells (Python examples)

### 1. Duplication
- **Signal**: Same logic copy-pasted in N places, similar try/except blocks, same dict built directly in multiple functions
- **Python example**:
  ```python
  # BAD: 3 functions with the same validation logic
  def create_user(...): 
      if not email or '@' not in email: raise ValueError(...)
      ...
  def update_user(...):
      if not email or '@' not in email: raise ValueError(...)
      ...
  def invite_user(...):
      if not email or '@' not in email: raise ValueError(...)
      ...
  ```
- **Fix**: Extract Function (`validate_email(email)`), Decorator (`@requires_valid_email`), or Pydantic validator
- **Note**: Rule of Three — 2 duplications is OK, **extract on the third occurrence**

### 2. Long Function / Deep Nesting
- **Signal**: Function 50+ lines, indentation 4+ levels, "what does this function even do" not obvious
- **Python example**:
  ```python
  # BAD: 200-line lambda_handler + 5 levels of nesting
  def lambda_handler(event, context):
      try:
          if event.get('source'):
              if event['source'] == 'aws.events':
                  for record in event.get('Records', []):
                      if record.get('body'):
                          data = json.loads(record['body'])
                          if data.get('action'):
                              # ... 200 more lines
  ```
- **Fix**:
  - **Early Return / Guard Clause**: `if not condition: return` to reduce nesting
  - **Extract Function**: Split by meaning
  - **Strategy/Dispatch**: Replace large if-elif chains with dict mapping
- **Note**: Use linter (`pylint max-args`, `complexity`) thresholds

### 3. Naming / Style Inconsistency
- **Signal**: Same concept named `user_id` / `userId` / `uid` inconsistently, meaningless names like `data` `result` `tmp` `obj`
- **Python example**:
  ```python
  # BAD: inconsistent domain terms
  def fetch_user_data(uid): 
      result = db.query(uid)
      tmp = result.to_dict()
      data = {**tmp, 'extra': ...}
      return data

  # but in another function
  def get_user(userId):
      obj = db.find(userId)
      return obj.serialize()
  ```
- **Fix**:
  - Define a domain glossary (force `user_id`, snake_case)
  - Follow PEP 8 + project conventions
  - Replace `tmp`, `data`, `obj` with meaningful names (`raw_record`, `enriched_user`, etc.)
  - Make intent clear with type hints
- **Note**: Don't rename everything at once → PR explodes. Module-by-module.

### 4. Magic Numbers / Strings
- **Signal**: `0.7`, `86400`, `"abc"`, `30` scattered throughout the code with no explanation
- **Python example**:
  ```python
  # BAD: why 0.7? why 86400?
  if confidence > 0.7:
      retry_in = 86400
      if attempt > 3:
          ...
  ```
- **Fix**:
  - **Named Constants**: `CONFIDENCE_THRESHOLD = 0.7  # >70% means trustworthy`
  - **Enum**: `class RetryDelay: DAILY = 86400`
  - **Configuration**: `.env` / config file for env-specific values
  - **Type alias**: `Seconds = int` for semantic clarity
- **Note**: Same value with different meaning → separate constants

## 6-Step Workflow

### 1. Baseline Capture — Record current behavior
Before refactoring:
- Run all tests (`pytest`) and confirm pass
- If any test fails → **refactoring forbidden**. Fix or skip first.
- If function has no tests → write **characterization test first** (freezes current behavior)
- Capture build/lint state too

```bash
pytest --co -q  # list tests
pytest -x       # confirm all pass once
```

### 2. Smell Identification — Check the four patterns
Identify which patterns are present:
- If **multiple coexist**, prioritize:
  1. Duplication (most dangerous) → changes require N updates
  2. Long Function → hard to understand/test
  3. Naming → cognitive load
  4. Magic Numbers → lost meaning
- **Catalog each instance**. "Here's 1" vs "N across the codebase" matters.

### 3. Scope Decision — Cut into small units
"While I'm here, let me do it all" — absolutely forbidden. One PR =:
- **One pattern** (e.g., this PR is Duplication only)
- **One module** (e.g., only `services/user.py`)
- **Under 1-2 hours** of work
- Future work → record as TODO / issue

Large refactors should be **split into multiple small PRs**. 1000 lines changed = unreviewable + merge conflict hell.

### 4. Apply Transforms — Use safe refactoring patterns

| Smell | Pattern |
|---|---|
| Duplication | Extract Function, Extract Method, Inline Variable |
| Long Function | Extract Function, Replace Nested Conditional with Guard Clause |
| Magic Number | Replace Magic Number with Named Constant, Introduce Configuration |
| Naming | Rename Variable, Rename Function (use IDE refactor tools) |

For each transform:
- **One thing at a time** (no Extract + Rename simultaneously)
- **Test immediately after** (`pytest -x`)
- **Revert immediately if test fails**

### 5. Behavior Verification — Prevent regression
After changes, confirm:
- All unit tests pass
- Integration tests (if any) pass
- Grep all call sites of the changed function → all still work
- Manually verify one real scenario if possible

"I checked my own change" is not verification. **Check every call site** of the changed code.

### 6. Commit Separation — 1 transform = 1 commit
Don't mix transform types in one commit:
- ❌ "refactor: cleanup user service" (50 files, 1000 lines)
- ✅ `refactor: extract validate_email` (1 file, 20 lines)
- ✅ `refactor: replace magic number 86400 with RETRY_DELAY_DAILY` (3 files, 6 lines)

Commit messages should specify:
- Which pattern was cleaned up, how
- No behavior change (No behavior change)
- Test pass confirmed

## Anti-Patterns (Forbidden in this mode)

1. **"While I'm here, also fix the bug"** — Behavior change = exit rootclean, separate PR via rootfix
2. **Refactor without tests** — Write characterization tests first
3. **Massive commit** — 1000 lines at once = unreviewable = merge conflict
4. **Style-only changes labeled as refactor** — Not refactoring, separate "apply lint" PR
5. **"I'll clean up later"** — Never happens. Only the small unit you split out, now.
6. **Introduce new abstractions** — That's building. Cleaning organizes what's already there.

## Output Format

When receiving a refactoring request, answer in this order:

```
[Baseline]
- Tests passing: ✓ / ✗
- Target module / function: <path>
- Current LOC / complexity: <numbers>

[Smells Found]
1. Duplication: <N locations> → <description>
2. Long Function: <function_name> N lines, N levels deep
3. Naming: <inconsistency example>
4. Magic Numbers: <N values>

[Proposal]
This PR: <1 pattern + 1 module> only
Transform: <Extract / Rename / etc.>
Remaining work: noted as TODO (separate PR)

Proceed?
```

## Termination Conditions

Exit rootclean mode only when ALL of:
- Baseline tests pass after changes (100%)
- No behavior change (manual verification or integration test)
- Commits split per transform
- Same pattern elsewhere noted as TODO if any
- No "while I'm here" scope additions

## Notes

- This skill encodes patterns from real-world Python refactoring sessions: duplicated logic, long functions/deep nesting, inconsistent naming, magic numbers.
- Pair with rootfix and rootbuild. rootfix changes behavior (fixes bugs), rootclean preserves behavior (improves quality), rootbuild adds (new features). Don't mix.
- Small fixes can stay in regular conversation. Activate this for medium+ refactors.
- Works in any project. Global skill.
