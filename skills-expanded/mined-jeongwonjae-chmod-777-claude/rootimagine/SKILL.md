---
name: rootimagine
description: Pre-deploy simulation mode. Use when a fix is written but not yet verified — to step-trace the code through normal/edge/failure scenarios, expose what was missed, and require explicit case coverage before commit. Pairs with rootfix.
triggers:
  - 시뮬레이션
  - 시뮬레이션 돌려
  - 시뮬
  - 루트이매진
  - rootimagine
  - root-imagine
  - imagine
  - 확실히 해결한거지
  - 진짜 해결됐는지
  - 검증해줘
  - 검증해봐
  - 시나리오 검증
  - 코드 시뮬
  - 논리적으로 확인
  - dry-run
  - 머릿속으로 돌려봐
---

# rootimagine — Simulation Verification Mode

Writing the fix isn't the end. Mentally (or on paper) run the fix through normal/edge/failure scenarios **before commit** to expose what you missed. "Compiles OK" absolutely does NOT mean "works."

## Activation

Explicit: `/rootimagine`

Auto-triggers:
- "시뮬레이션 돌려"
- "확실히 해결한거지"
- "진짜 해결됐는지"
- "코드 확인해봐"
- "논리적으로 확인"
- "dry-run"
- "머릿속으로 돌려봐"

## Relationship with rootfix

| rootfix | rootimagine |
|---|---|
| Tracks **cause** (WHY×5) | Tracks **effect** (time-step trace) |
| Suggests fix options | Verifies the applied fix |
| Patterns (Drift/Race/...) | Cases (A/B/C/D normal/edge/failure) |
| Pre-commit step | Pre-commit final gate |

Common pair: rootfix to draft → rootimagine to verify → commit.

## 6-Step Simulation

### 1. Build State/Variable Table
List every variable, state, and external resource (cache/DB/event/queue/...) the fix touches:

| Name | Initial | Updated At | Updated By |
|---|---|---|---|
| `_share_card_sent` | False | after yield | SSE generator |
| `_pg.share_card_ready` | unset | finally of side task | _gen_share_card_early |
| `_bg_queue` | empty | each chunk | _bg_generate |

This table is the mental state model. Miss it and the sim is wrong.

### 2. Time-Step Trace (T = time)
For each time point of interest (T=0, T=5, T=10, ...), trace what runs and how variables change.

#### How to pick trace points — any of these is a checkpoint
- `await` / `asyncio.wait_for` / `condition.wait_for` — any yieldable point
- `timeout` expiry — `wait_for` timeout value
- loop iterations — `while True` / `for ...` boundaries
- `event.set()` / `event.is_set()` — completion points of external tasks
- external calls (Bedrock/DB/HTTP) — response arrival (typically ms to tens of seconds)
- user actions — click/leave/refresh/page change
- component mount/unmount (frontend)
- branches (`if/else`) — trace both arms

#### At each time point, record
- **Code line + one-line description** ("line 3040: chunk = await _bg_queue.get() blocked")
- **Every cell of the variable table** (especially the deciding branch variables)
- **What yielded/returned/dispatched** (effect on user view)
- **What other tasks are doing simultaneously** (critical in async)

#### Forced self-check at every branch / await
- During this await, can another task mutate Z so that the next branch chooses differently?
- Did I trace the *other* arm of this branch?
- After this timeout, in what state is the next line invoked?
- While this yield reaches the client, what is the backend doing? (and vice versa)

Example trace:
```
T=0     : line 2944 _gen_share_card_early task started (Bedrock call started)
T=0     : line 2964 _bg_generate task started
T=0.1   : SSE generator entered, line 3027 stat_cards yielded → client view
T=0.1~5 : line 3031 share_card_ready.wait() blocked
         | meanwhile: _gen_share_card_early awaiting Bedrock response
T=5     : line 3031 wait_for TimeoutError → share_card emission skipped → chunks loop
T=5+ε   : line 3041 _bg_queue.get() blocked (no chunk yet)
         | meanwhile: _gen_share_card_early awaiting Bedrock response
T=10    : _gen_share_card_early got Bedrock response → _pg.share_card filled → share_card_ready.set()
         | line 3041 still blocked
T=120   : first chunk arrives → line 3041 unblocks → yield chunk → polling → share_card yielded
         | user: doesn't see share_card until T=120 ← MISSED CASE!
```

If during a trace you find a "wait this is missed" — fix immediately. That is the entire point of the sim.

### 3. Case Enumeration — Pull more than you think
**Principle**: A/B/C/D are the *starting line*, not the finish. For each variable/timing/external resource the code depends on, pull out **dimensions of variation**, then multiply cases by sampling extremes/middles along each dimension. "I only ran the happy path" = immediate fail.

#### Dimension checklist (commonly missed axes)
- **Timing**: fast / right at timeout / slow / never arrives
- **Order**: A first / B first / simultaneous
- **Resource state**: cache hit / miss / stale / reset (after deploy)
- **Network / IO**: normal / slow / disconnect / partial response
- **Concurrency**: single / same user twice / different users simultaneously
- **Input**: normal / empty / malformed / very large
- **Auth**: valid / expired / forged / anonymous
- **Lifecycle**: normal exit / user leaves / refresh / page change
- **External**: external API success / failure / timeout / partial
- **State reset**: initial / leftover from prior call / cross-instance influence

#### Minimum cases (starting line)
**A. Normal (fast path)**: all dependencies satisfied within timeout. Happy path.
**B. Slow path**: async dependency is late but eventually completes. ← **Most fixes miss here**.
**C. Failure**: dependency errors out. Verify fallback behavior.
**D. Extreme**: dependency never completes / external abort / cancel / process kill.

Don't stop here. From the dimension checklist above, pick relevant ones and add cases:
- E. Concurrent invocations (race)
- F. Partial failure (some chunks arrive + cancel)
- G. External resource reset (cache cleared right after deploy)
- H. User input variability (empty form / unicode / emoji / very large)
- ...

**Question to ask yourself**: "Did I write down *every* way this fix could break in someone's hands?" — if you have fewer than 5, push harder.

### 4. State the User-Visible Effect
For each case, what does the user actually see?
- "share_card appears around T=3"
- "1-2 minutes of blank screen, then share_card around T=11"
- "user never sees share_card (fallback kicks in, content batched at the end)"

If you can't write the user-visible effect in plain words, you haven't really traced it.

### 5. Latent Defect Self-Check
- [ ] Any time point where code line Y doesn't execute when it should?
- [ ] Variable Z could hold a stale value due to a race?
- [ ] External resource (cache/DB/event) might be in a reset state?
- [ ] On async cleanup / cancel, is `finally` guaranteed to run?
- [ ] Could the generator hang in a "no chunks/events ever" case?
- [ ] What if two instances run the same code path concurrently?

### 6. Confidence Declaration
- HIGH: all 4+ cases traced end-to-end, no latent defects
- MEDIUM: only some cases simulated, operational verification still required
- LOW: simulation is hard, or external factors dominate → real validation environment needed

**No fake confidence**. If "HIGH" but you skipped cases, it's actually MEDIUM.

### 7. Concerns
Surface things that "won't break right now but need attention." Not just bugs — anything that could become a problem. The purpose is to expose risks before they become incidents.

#### Scope (full coverage)
| Category | Examples |
|---|---|
| **Code Quality** | Tech debt accumulation, scalability limits, maintenance difficulty, test coverage gaps, naming |
| **Operational** | Missing monitoring, incident recovery difficulty, missing alerts, SLA impact, insufficient logging |
| **Business Impact** | User experience degradation, revenue impact, compliance issues, data integrity risk |

#### How to write concerns
- Each concern: **what** + **why it's concerning** + **when it could break**
- Severity tag: `🔴 HIGH` / `🟡 MEDIUM` / `🟢 LOW`
- If you feel "this might be a problem someday..." — write it down. Don't ignore your instinct.
- Overlap with latent defects is OK — here you take a **wider lens**.

Example:
```
🟡 MEDIUM: No backoff in retry logic → could exceed rate limits under external API failure (breaks at 10x traffic)
🔴 HIGH: Errors silently swallowed in this function → impossible to trace root cause during incidents (no monitoring alerts either)
🟢 LOW: Magic numbers in 3 places → not broken now but invites mistakes on next change
```

### 8. Next Actions
After simulation, state clearly "so what now?" If the agent doesn't know what to do next, the simulation was just self-satisfaction.

#### 3-tier classification
| Tier | Criteria | Examples |
|---|---|---|
| **🚨 NOW (Immediate)** | Defects found in simulation. Must fix before commit | "Fix Case B miss", "Add error handling" |
| **📋 NEXT (Follow-up)** | Not this PR, but the very next PR | "Add monitoring dashboard", "Write perf test" |
| **💡 LATER (Optional)** | Nice to have, not urgent. Backlog material | "Refactor", "Docs", "Expand test coverage" |

#### How to write actions
- Each action is **one executable sentence** (vague "needs improvement" forbidden)
- Link to which mode (rootfix/rootclean/rootbuild) when possible
- If any NOW items exist → commit forbidden, apply fix first then re-simulate
- NOW items must be zero before commit is allowed

Example:
```
🚨 NOW (Immediate):
1. Case B: share_card missed when first chunk delayed → add polling outside chunks loop [rootfix]
2. Resource not released in finally after timeout → memory leak possible [rootfix]

📋 NEXT (Follow-up):
1. Add share_card generation latency monitoring alert [rootbuild]
2. Write E2E test for Case D (process kill) scenario [rootbuild]

💡 LATER (Optional):
1. Extract _bg_generate function → currently 87 lines, readability improvement [rootclean]
2. Move magic number timeout 5s to config [rootclean]
```

## Output Format

```
[Simulation — <fix one-liner>]

State table:
| Name | Initial | Updated At | Updated By |
|---|---|---|---|
| ... |

Case A (Normal): T=0 → T=N trace
Case B (Slow):   T=0 → T=N trace
Case C (Failure): T=0 → T=N trace
Case D (Extreme): T=0 → T=N trace

User-visible effect per case:
- A: ...
- B: ...
- C: ...
- D: ...

Latent defects:
- (list if any)

Confidence: HIGH | MEDIUM | LOW
Reason: ...

Concerns:
- 🔴/🟡/🟢 <what> — <why concerning> (<when it breaks>)
- ...

Next Actions:
🚨 NOW (Immediate):
1. <executable instruction> [linked mode]

📋 NEXT (Follow-up):
1. <executable instruction> [linked mode]

💡 LATER (Optional):
1. <executable instruction> [linked mode]
```

## Termination Conditions

Simulation ends → commit/deploy allowed only when ALL of:

- [ ] State/variable table built (every variable the fix touches + external resources)
- [ ] Dimension checklist reviewed (cover every dimension that applies)
- [ ] **At least 5 cases** traced — A/B/C/D + at least one from dimensions
- [ ] User-visible effect declared per case
- [ ] Each await/timeout/branch self-check passed
- [ ] For any miss discovered, an extra fix is applied → that fix is re-simulated (recursive)
- [ ] Latent defects: zero (or explicitly "accepted — reason: ...")
- [ ] Confidence assigned (HIGH/MEDIUM/LOW + reason)
- [ ] If MEDIUM/LOW, operational verification plan specified (which environment, which flow)
- [ ] **Concerns documented** (code quality / operational / business impact — full scope review)
- [ ] **Next Actions classified** (NOW / NEXT / LATER tiers)
- [ ] **NOW items = zero** — any remaining NOW items block commit, fix first

Any unchecked item → simulation incomplete. Commit forbidden. No self-deception.

## Anti-Patterns (forbidden in this mode)

1. **"It compiles, so OK"** — skipping simulation and declaring success
2. **Happy-path-only trace** — skipping B/C/D cases
3. **Self-inflated confidence** — calling it "HIGH" without operational verification
4. **Implicit assumptions** — "chunks will probably arrive early" without stating it
5. **Missing user-visible effect** — wrote what code does, but not what the user sees
6. **Ignoring races** — only one ordering of two tasks considered

## Notes

- Derived from real-world async debugging sessions where fixes were repeatedly applied yet *all of them missed the actual operating environment* — e.g. adding polling inside a chunks loop while the first chunk takes 1-2 minutes to arrive in production (so the polling never runs).
- Pairs with rootfix: fix → simulate → discover missing case → fix again → simulate again → confidence.
- Works in any project. Global skill.
