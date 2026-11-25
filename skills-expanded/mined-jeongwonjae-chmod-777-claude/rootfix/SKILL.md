---
name: rootfix
description: Root-cause-first debugging mode. Use when user wants a real fix (not a band-aid) — when a "fix" keeps coming back, when same code path is built in N places, or when async paths interact in non-obvious ways. Forces 5-Why drilling, drift/race detection, and trade-off-explicit options before any code change.
triggers:
  - 근본
  - 근본적
  - 근본원인
  - 근본 원인
  - 근본해결
  - 근본 해결
  - 근본대책
  - 근본 대책
  - root cause
  - root-cause
  - rootfix
  - 왜 이런거야
  - 왜 자꾸
  - 임시방편 말고
  - 다시 망가지지
  - 또 망가
  - 미봉책
  - 정공법
---

# rootfix — Root-cause Resolution Mode

Don't throw one-off fixes at symptoms. If the same bug returns in different shapes, the root cause wasn't found. When this skill activates, follow the procedure below.

## Activation

Explicit: `/rootfix`

Auto-triggers (when these phrases appear in user message):
- "근본 원인 찾아줘", "근본 해결", "근본 대책"
- "왜 자꾸 이런거야"
- "임시방편 말고"
- "다시 망가지지 않게"
- "정공법으로"
- "또 망가졌어"
- "root cause", "root-cause"

## What's Different (vs general debugging)

| General Mode | rootfix Mode |
|---|---|
| OK if symptom disappears | OK only if same class of bugs cannot recur |
| Patch on first hypothesis | Hypothesis → one more WHY → until true root |
| Commit when it works | Verify **structural defects** (drift / race / multi-store / multi-path) |
| Single option | Both band-aid and root fix, with trade-offs, user picks |
| Code-only change | Verify with real scenario (reproduce → confirm fixed) |

## 6-Step Workflow

### 1. Stop — Block the symptom-patch reflex
- First question: **"Am I just hiding the symptom?"**
- Symptom-patch signals:
  - Recent N commits repeatedly modifying the same area
  - "Temporarily disabled because of X" comments
  - Same scenario recurring in different shapes
  - "Not sure why but this works"
- If 1+ signal present → no general mode, stay in rootfix.

### 2. WHY × 5 — Distinguish nominal vs real root cause
- Problem → why? → nominal reason → **is that nominal really the root?** → one more level → repeat.
- Nominal-cause traps (examples):
  - "Cache is empty" → why? → `cache_set` removed → why? → "to prevent mismatch" → **is that the actual root of cache removal?** → No, the real root is multiple sources for the shared data.
  - "Duplicate history" → why? → 3 save paths → why? → grew over time → **real root** = scattered result-dict builders.
- WHY stops when going deeper hits something un-fixable by code/structure (external system limit, policy, etc.).

### 3. Structural Defect Pattern Checklist
While searching for the root, flag immediately if these patterns appear:

#### Drift (multi-definition pattern)
- Same dict / response / state is built **independently in N places**
- Adding/changing a field requires updating all of them → eventually drifts
- **Fix**: Consolidate into a single builder function. Vary only the call site.

#### Race (parallel task pattern)
- Multiple `asyncio.create_task(...)` floating around
- Shared state (`_pg.share_card`, `_cache`, etc.) — one side writes, another reads
- Ask:
  - Can another coroutine interleave between `await` points?
  - What happens if one side reads the other's result before completion?
  - Does the shared-state access need `Event` / `Lock` / ordering guarantees?
- **Fix**: ready-event + await pattern, or single-writer structure.

#### Multi-Save Path
- Same data can be saved (INSERT/UPDATE) from **multiple paths**
- Time-delayed calls cause duplicates / overwrites
- **Fix**: DB UNIQUE constraint + UPSERT, or converge to a single save path.

#### Stale Fallback
- DB lookup fallback fetches the wrong row (matches only user_id → row from another analysis)
- **Fix**: Add identifier (cache_key, session_id, etc.) to the match condition.

#### Local-Only Vision
- Reading one function and fixing → the same pattern may exist in sibling functions
- **Fix**: `grep` the entire codebase for the pattern, then handle in bulk.

### 4. Option Presentation — Make Trade-offs Explicit
Even with a clear root fix, present **multiple options** first:

```
Option A: Band-aid — 1-line change, applies immediately, misses some cases
Option B: Partial — N-line change, catches most cases, same pattern can recur
Option C: Root fix — migration/refactor, stable, may have downtime
```
For each option, specify:
- Scope of change
- Risk (Scope-risk)
- Cases caught / not caught
- Time to apply

**Forbidden**: Single presentation of "I know the root fix but applied the band-aid only" — that strips the user of trade-off info they might've used to refuse.

### 5. Execute — Minimum Change Principle
After the user picks an option:
- Apply only the selected option's change
- If the same pattern exists elsewhere, explicitly mention it and propose a **separate PR/commit**
- For migrations: clarify the order (DB → code → verify)

### 6. Verify — Reproduce the Actual Scenario
After the change, do one or more of:
- **Local reproduction**: reproduce the scenario via curl/script → confirm it passes
- **Log trace**: monitor production logs for the same pattern over a period
- **Add test**: write a regression test
- **Grep pass**: confirm the same anti-pattern is not left elsewhere

"Compiles = guaranteed behavior" is absolutely NOT true.

## Anti-Patterns (Forbidden in this mode)

1. **"Let's just go with this"** — Single band-aid proposal followed by execution
2. **First hypothesis = conclusion** — Stopping after a single WHY
3. **Compile OK = verified** — Committing without execution verification
4. **Patching the same spot N times** — Re-modifying the same area when bug returns in another shape
5. **Hiding the trade-off** — Not mentioning "I knew a better way but didn't take it"

## Output Format

When receiving a problem report, answer in this order:

```
[Cause Tracing]
Surface cause: <direct cause of visible symptom>
WHY → <one more level>
WHY → <another level>
True root: <structural defect or policy, etc.>
Pattern identified: <Drift / Race / Multi-Save / etc.>

[Options]
A. Band-aid — <scope, caught cases, missed cases>
B. Partial — <scope, trade-offs>
C. Root fix — <scope, trade-offs>

Recommendation: <option + reason>

Proceed?
```

## Termination Conditions

Exit rootfix mode only when ALL of:
- Root cause is named
- User has chosen an option and applied it
- Verification scenario passes (reproduce → fix → no longer reproducible)
- Same-pattern check across the codebase is complete

## Notes

- This skill was derived from real-world debugging sessions where patches kept accumulating without resolving the root cause — avoiding the pattern of patch accumulation → root unresolved → recurrence → bigger patches.
- Works in any project. Global skill.
