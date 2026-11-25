---
name: writing-bench-task-judge
description: Use when writing or modifying `check_goals()` / `get_answer()` / App `check_*` methods in `bench_env/task/`, or when reviewing a draft task's judge correctness. Triggers include adding a new task, editing a judge method, or diagnosing a judge false-positive/negative.
---

# Writing bench_env Task Judges

## Overview

A judge decides whether the Agent completed the task. Two failure modes dominate:

- **Soundness hole** — an obviously wrong path is judged `passed=True` (keyword hit, unstable trace field).
- **Completeness hole** — a reasonable completion path is judged `passed=False` (bound to specific wording or UI step).

Neither is caught by type checks — both are caught by applying the **CRUD model** rigorously.

**Authoritative refs:**
- `bench_env/docs/task/TASK_AUTHORING_GUIDE.md` — task design + CRUD judge model (read §2 in full)
- `bench_env/docs/task/TASK_CODE_SPEC.md` — code rules (file responsibilities, naming, defensive-coding ban, time APIs, CriteriaTask)
- `bench_env/docs/REFERENCE.md` — `JudgeInput` / `JudgeResult` field & `expected_changes` path syntax lookup
- `bench_env/docs/task/GROUNDED_MODE.md` — only if task uses `answer_fields` / grounded eval

## Step 1 — Classify the task as CRUD

Before writing any check, name the operation out loud:

| Operation | Triggering verbs | Required check strategy |
|---|---|---|
| **Create** (增) | 添加/创建/发送/收藏/点赞/新建 | **diff**: init vs current, match in new items |
| **Delete** (删) | 删除/移除/取消/取关/下架 | **diff**: target id in `init_ids - curr_ids` |
| **Modify** (改) | 修改/切换/改名/设置为/拨动 | **lookup in current**; use **init** to resolve identity |
| **Query** (查) | 告诉我/是多少/哪个/什么时候 | **read from init**, compare to `input.answer` |

**Each CRUD type has ONE correct strategy — not a choice.** Using lookup-on-current for Delete/Create creates false positives (sampler bug → passes as Agent action).

## Step 2 — Survey the App module for reusable abstractions

**Before writing any judge, Read `app.py` end-to-end with the Read tool** (split into sections only if the file exceeds the tool's limit). Scan every `def` line plus its docstring / leading comment, plus any module-level helper functions above the class. **Do not substitute `grep` for this.** Grep silently misses:

- module-level helpers (`_note_text`, `_pick_keywords_from_note`) that sit above the class
- `@staticmethod` / `@property` / `@classmethod` methods that your prefix guess won't anticipate
- helpers whose names don't follow the shape you grepped for (`latest_note_by_title` is a find-by-name primitive but doesn't start with `find_`; `visible_notes` is a filtered view but doesn't start with `filtered_`)
- `_xxx` private methods that contain logic you could extract

Reading the file end-to-end is cheap (one tool call for a few hundred lines). Missing a helper and duplicating it is expensive — the duplicate anchors every future author to the wrong template, and the trap rationale that belonged on the App method ends up lost. After `app.py`, skim `tasks.py` as well: existing tasks show you the canonical call shape to mirror.

As you read, classify each method against `TASK_AUTHORING_GUIDE.md` §2.1 "Three-tier App helpers" (that section is the backbone; re-read it if rusty). The table below is a fast-lookup of the layers a judge most often needs — use it as a mental checklist while scanning, not as a grep target list:

| Layer | Typical shape | Judge uses it for |
|---|---|---|
| Find / lookup | `find_X_by_id`, `find_X_by_text`, `latest_X_by_Y` | Identity resolution in Modify / Delete (on `init`) |
| Diff primitives | `new_X()`, `removed_X_ids()`, `changed_X_ids()` | Create / Delete strategy |
| Filtered views | `visible_notes`, `incomplete_todos`, `private_notes` | Sampler candidates, post-condition subsets |
| Semantic labels | `reminder_time_labels`, `date_match_labels` | Answer-text matching |
| **Existing `check_*`** | `check_todo_deleted`, `check_latest_contains` | **Call directly — and read its docstring to inherit the invariant it encodes** |

Decision once you've surveyed:

1. An existing `check_*` covers your goal → call it from `check_goals`.
2. A lower-layer primitive exists (e.g. `removed_X_ids()`) but no `check_*` wraps it → **add a new `check_*` method** in the same file, following the surrounding naming convention (`check_<noun>_<verb-past>` or `check_<noun>_<adjective>`), call it from `check_goals`.
3. Nothing exists → **add both the primitive and the `check_*`** to `app.py`, then call the `check_*` from `check_goals`.

**Don't inline set-ops, id diffs, or find-by loops in `check_goals`.** Doing so:

- duplicates logic that already exists or will exist
- hides the *reason* the check is correct (e.g. "why id-diff, not text lookup" — the trap rationale lives in the App method's docstring, not in every task that uses it)
- anchors the next author to a bad template, because they'll copy the most recent task

Concrete counter-example (what NOT to do):

```python
# ❌ inline logic in check_goals — duplicates what should be an App method
def check_goals(self, input):
    notes = Notes(input.apps["notes"], init=input.apps_init["notes"])
    init_target = notes.init.find_todo_by_text(self.p.todo_text)
    target_id = str((init_target or {}).get("id") or "")
    current_ids = {str(t.get("id") or "") for t in notes.todos}
    removed = bool(target_id) and target_id not in current_ids
    return [{"field": "todo_deleted", "expected": self.p.todo_text,
             "actual": None if removed else self.p.todo_text, "passed": removed}]

# ✅ push to Notes.check_todo_deleted(text), call it here
def check_goals(self, input):
    notes = Notes(input.apps["notes"], init=input.apps_init["notes"])
    return [notes.check_todo_deleted(self.p.todo_text)]
```

## Step 3 — Enforce the init/current rule

| Use | Which state | Why |
|---|---|---|
| Resolve target identity for modify/delete | **init** | Current may have been changed; init can't lie |
| Verify the modification result | **current** | You're checking what the Agent produced |
| Diff for create/delete | **both** | You need both ends of the delta |
| Read expected answer for Query | **init** | Ground truth is frozen at setup time |

```python
# ✅ Modify: init resolves identity, current verifies result
init_alarm = self.init.find_alarm_by_time(h, m)
assert init_alarm is not None  # sampler contract
alarm = self.find_alarm_by_id(init_alarm["id"])  # current
```

## Step 4 — Sampler contract asserts (only where upstream is silent)

Add `assert` in an App `check_*` method **only when** the target's presence in `init` isn't already enforced upstream **and** the natural failure mode would be silent `passed=False`. The purpose is attribution: route sampler bugs to `judge_error` instead of `passed=False`. If upstream already raises, a `check_*`-level assert re-validates the same premise and **violates `TASK_CODE_SPEC.md` §5 "No defensive coding"**.

**Upstream is already enforced** (skip the assert — it's defensive coding):

- **Sampler `raise`s on no candidate** — the canonical pattern: `_sample_X` reads `env_state`, picks a candidate, `raise ValueError` if none. By the time `check_*` runs, the target is guaranteed to be in `init`. Re-asserting is double-validation.
- **Data method raises on not-found** (`find_contact_wxid(name)` → `ValueError`) — premise already enforced by the lookup itself.
- **Query** / **direct leaf access** — natural dereference (`alarm["note"]`, `self.get("settings.darkMode")`) raises KeyError/TypeError → already `judge_error`.
- **`target is None` is a legitimate Agent failure mode** — e.g. Agent deleted the alarm it was supposed to modify → `alarm is None → passed=False` is correct per `TASK_AUTHORING_GUIDE.md` §2.5 "Modify".

**Add assert** when upstream is silent or absent (sampler bug would be silently absorbed into `passed=False`):

- **Legacy silent-fallback sampler** — older sampler that returns a default instead of raising when no candidate.
- **Hardcoded `default` param with no `sampler:` binding** — CLI overrides, smoke tests, suites that don't sample this field. No upstream guarantee exists.
- **Externally-injected params** — cross-app contracts, harness-level inputs, params whose provenance lives outside the suite.

```python
# ✅ Sampler raises on no candidate → no assert; target is guaranteed in init
# (e.g. Notes._sample_incomplete_todo raises ValueError if no candidate)
def check_todo_deleted(self, text):
    init_todo = self.init.find_todo_by_text(text)  # guaranteed non-None by sampler
    target_id = str(init_todo["id"])
    return {...}

# ✅ No sampler binding for `alarm_id` → param may come from CLI/default → assert
def check_deleted_alarm(self, alarm_id):
    assert self.init.find_alarm_by_id(alarm_id) is not None, (
        f"Upstream bug: alarm {alarm_id} not in init"
    )
    removed = self.removed_alarm_ids()
    return {"field": "alarm_deleted", "expected": alarm_id,
            "actual": sorted(removed), "passed": str(alarm_id) in removed}
```

**Quick decision**: trace where the target id/text came from. If the path is `env_state → _sample_X (raises on empty) → params.X → check_*`, the assert is redundant. If the path is `default = "..." → params.X → check_*` or anything involving user-supplied / hardcoded values, keep the assert.

**Asserts live in App `check_*` methods, not in `tasks.py`'s `check_goals()`.**

## Step 5 — Declarative first, `check_goals` last (TASK_AUTHORING_GUIDE §4.2)

Decision order when writing a task:

1. Can it be `answer = ".path"` / `answer = ".path[field={param}].x"`? → use it.
2. Can it be `criteria = {"key": "{param}"}`? → use it.
3. Only if neither fits, write `get_answer()` / `check_goals()`.

```python
# ❌ Over-written
def get_answer(self, input):
    for p in Railway12306(input.apps["railway12306"]).passengers:
        if p["isDefault"]:
            return p["name"]

# ✅ One line
answer = ".passengers[isDefault=True].name"
```

## Step 6 — Soundness + completeness self-audit (TASK_AUTHORING_GUIDE §2.7 "Reliability requirements")

Before committing, walk through:

| Question | Red flag |
|---|---|
| Does this check pass when a broad keyword appears but the goal wasn't met? | Bound to keywords like "计划"/"推荐" |
| Does it bind to one specific UI path's incidental step? | Using current-route checkpoints Agent can skip |
| Does it rely on unstable trace fields (`lastAccess`, `currentlySelected`, `recentlyViewed`)? | These get overwritten by subsequent actions |
| Does it force one specific wording / title / format? | Won't tolerate合理改写 |
| Does it fail合理替代路径? | Over-tight completeness |
| **If Agent hits the target *and also* mutates unrelated state (deletes another row, flips an unrelated flag), does anything fail the task?** | **No side-effect fence** — `expected_changes` is too broad and no conservation `check_*` backs it up |

If any answer is "yes," rework the check — either strengthen evidence (for soundness) or broaden acceptance (for completeness).

### Side-effect fence: precise `expected_changes` first, conservation check second

`expected_changes` (see `bench_env/docs/REFERENCE.md` "expected_changes path syntax") is the framework's automatic diff gate — any path outside it fails the task regardless of `check_goals`. Narrow it before you reach for a hand-written conservation check:

- **`CriteriaTask`** auto-derives `expected_changes` from `criteria` keys — usually no declaration needed.
- **Precise paths** let the framework do the whole conservation job:
  - `expected_changes = ["todos[id={todo_id}]"]` — only this todo may change; Agent deleting a *different* todo fails automatically.
  - `expected_changes = ["moments[+1]"]` — exactly one new moment may appear; adding two fails automatically.
  - `expected_changes = ["contacts[name={contact}].isBlacklisted"]` — only this contact's blacklist flag may change; editing their name fails automatically.
- Only when `expected_changes` **genuinely can't** be narrowed do you need a conservation `check_*`:
  - Batch deletes across a whole partition (`DeleteAllCompletedTodos` must delete an unknown-at-design-time set of ids) — pair `check_X_all_deleted` with `check_other_partition_preserved`.
  - The target id isn't exposed as a Task param, only its text/name is — precise path `[id={id}]` not available.
  - Multi-path Create/Modify where declaring every touched path would be brittle.

**Rule of thumb:** if you're about to add `check_other_X_preserved(exclude_text=self.p.x)` to a single-target Delete, first check whether sampler exposes the target id and whether `expected_changes = ["xs[id={x_id}]"]` would eliminate the check entirely. Framework-level fences beat hand-written ones — they're declarative, typechecked against the diff engine, and can't be forgotten by the next author.

## Step 7 — check_goals return format (TASK_AUTHORING_GUIDE §2.4 "Check methods")

Every check dict **must** have exactly `field` / `expected` / `actual` / `passed`. Framework raises `ValueError` on missing `passed`.

```python
# ❌ wrong shape
return [{"name": "route", "ok": True, "detail": {...}}]

# ✅ canonical shape, with diagnostic expected/actual
return [{"field": "newPendingOrder",
         "expected": "上海→南京 2026-03-21 G7002 二等 ×1 (赵宇轩)",
         "actual": "未创建新订单",
         "passed": False}]
```

**One check = one semantic goal.** Don't split "buy a correct ticket" into 5 field-level checks — that inflates `progress` and loses global diagnostic value. Do use multiple checks when there are independent goals.

**`expected`/`actual` must be human-readable.** `expected=True, actual=None` tells nobody anything.

## Step 8 — Use `input.apps` / `input.apps_init` directly (TASK_CODE_SPEC §5 "No defensive coding")

```python
# ✅
wechat = Wechat(input.apps["wechat"], init=input.apps_init["wechat"])

# ❌ defensive — masks config bugs
wechat = Wechat(input.apps.get("wechat", {}), init=(input.apps_init or {}).get("wechat"))
```

No `or {}`, no `.get("xxx", {})`, no `try/except` on data access. Data missing → exception → `judge_error`.

## Red-flag self-check (scan before submitting)

- [ ] Named the CRUD type; picked the required strategy
- [ ] Read the suite's `app.py` end-to-end with the Read tool (**not grepped** — grep misses module-level helpers, decorated methods, and anything whose name doesn't match the prefix you guessed); classified each helper into its layer (find / diff / filtered-view / check / answer) and reused or extended existing ones instead of inlining set-ops / diffs in `check_goals`. Also skimmed `tasks.py` for the canonical call shape.
- [ ] init vs current used per the rule table
- [ ] Sampler contract `assert` present in Create/Delete/Modify `check_*` methods **only when** upstream is silent (legacy fallback sampler, hardcoded default without `sampler:`, external input); **skipped** when upstream already `raise`s (canonical `_sample_X` pattern) to avoid violating TASK_CODE_SPEC §5 (no defensive coding); **never** added blindly to query / leaf-access checks
- [ ] Tried `answer=` / `criteria=` first; only wrote `check_goals` if declarative couldn't express it
- [ ] Soundness audit: no broad-keyword pass, no unstable trace field, no path-specific step
- [ ] Completeness audit: no forced wording / title / format
- [ ] Side-effect fence: `expected_changes` narrowed to precise paths (`[id={x}]` / `[+N]` / `[field=v].sub`) where possible; conservation `check_*` added **only** when the framework fence genuinely can't express the scope
- [ ] Check dicts use `field/expected/actual/passed`; `expected`/`actual` human-readable
- [ ] One check per semantic goal
- [ ] No defensive `or {}` / `.get()` on `input.apps*`
- [ ] Time/duration fields use `match_time` / `match_duration` (see `GROUNDED_MODE.md` §4.3 "Matchers"), not `match_value`
- [ ] Date answers use `date_match_labels(date, input.os)` with os_state for relative labels
- [ ] If using grounded eval: read `GROUNDED_MODE.md` §3-4

## Rationalization table

| Excuse | Reality |
|---|---|
| "lookup on current is simpler than diff" | For Create/Delete it creates silent false positives on sampler bugs. Use diff. |
| "The existing task Foo uses lookup, so mine can too" | Then Foo has the same bug. File it, don't propagate it. |
| "Assert is defensive; the spec bans defensive code" | Wrong: asserts enforce **upstream contracts** so failures route to `judge_error`, not `passed=False`. Defensive = `or {}` / `try/except` on downstream data. |
| "Every check method should have an assert for consistency" | No — blanket asserts add noise and violate TASK_CODE_SPEC §5 (no defensive coding). Skip assert when upstream already enforces the premise: (1) sampler that `raise`s on no candidate, (2) data methods that raise on not-found, (3) query / leaf-access paths where natural dereference raises. Add assert only when upstream is silent (legacy silent-fallback sampler, hardcoded default without `sampler:`, external input). |
| "One check per field gives better progress granularity" | TASK_AUTHORING_GUIDE §2.4 — one semantic goal = one check. Field-level splits inflate progress on partial wrong answers. |
| "`check_goals` is the natural place for checks" | TASK_AUTHORING_GUIDE §4.2 — try `answer=` / `criteria=` first. `check_goals` is last resort. |
| "My judge is simple enough to inline in `check_goals`" | Inline set-ops / id diffs duplicate existing App abstractions, hide the trap rationale (e.g. "why id-diff, not text lookup"), and anchor the next author to your bad template. If the pattern belongs anywhere, it belongs on the App class next to its siblings. |
| "No existing `check_*` covers this exact case, so I'll write it in the task" | That's the signal to **add** a new `check_*` on the App class, not to inline. Step 2. |
| "Grep for `find_\|new_\|check_` is faster than reading the whole `app.py`" | Grep misses module-level helpers, `@staticmethod` / `@property` methods, and anything whose name doesn't match your prefix guess (e.g. `latest_note_by_title`, `visible_notes`). A single Read call on a few-hundred-line file is cheap; a duplicated helper poisons every future task that copies yours. |
| "I'll add `check_other_X_preserved` to lock down side-effects" | First try `expected_changes = ["Xs[id={x_id}]"]` — if the target id is in params, the framework fences scope for free. Hand-written conservation checks are for cases where the framework genuinely can't express the scope (batch deletes over an unknown set, target addressable only by text, etc.). |
