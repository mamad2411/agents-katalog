---
name: state-machines-pro
description: "Use when designing, implementing, or debugging robot behavior coordination with finite state machines — task sequencing, mission executives, mode managers, error recovery flows, or when choosing between SMACH/yasmin/hand-rolled FSMs in ROS2. Provides production patterns for hierarchical FSMs, entry/exit actions, transition guards, event-driven vs polled execution, explicit error-state modeling, state timeouts, and state-history logging."
category: robotics
domain: robotics
subdomain: general
version: 1.0.0
license: MIT
risk: low
source:
  repository: "rahulbachina/robotics-skills"
  commit: "e69d9828fb"
  imported_at: "2026-09-20"
  license: "MIT"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---


# Production State Machines for Robot Behavior

State machines coordinate everything above the control loop: docking sequences, pick-and-place missions, charging behavior, error recovery, operational modes. Most robot field failures that are not hardware are *behavioral*: the robot gets stuck in a state, transitions on a stale event, or enters a state nobody modeled. This skill encodes the patterns that prevent that.

## Core Principles (non-negotiable in production)

1. **Every state needs an error exit.** A state with no failure transition is a trap. If you cannot name what happens when this state fails, the design is incomplete.
2. **Every state needs a timeout** (or an explicit, documented reason it cannot have one). Robots block on hardware; hardware lies.
3. **Transitions fire on events, guarded by conditions.** Never encode "wait until X" as a busy spin inside a state's execute body without a timeout and an abort path.
4. **State machines must be observable.** If you cannot answer "what state was the robot in at 14:32:07 and why did it transition?", you cannot debug field reports.
5. **One source of truth for the current state.** No mirrored state variables in other nodes — publish state, never duplicate the machine.
6. **Transitions are atomic.** Exit actions of the old state complete before entry actions of the new state begin. No work runs "between" states.

## Anatomy of a Production State

Each state has, explicitly:

| Element | Purpose | Common bug if missing |
|---|---|---|
| `on_entry()` | One-shot setup: start timers, send goal, enable hardware | Re-sending goals every tick |
| `execute()` / event handlers | The state's ongoing logic | — |
| `on_exit()` | Cleanup: cancel goals, stop motion, release resources | Motors still commanded after transition |
| Guards | Predicates that must hold for a transition to fire | Transitioning on stale/invalid data |
| Timeout | Max dwell time → error transition | Robot frozen forever waiting on a dead sensor |
| Error outcome | Named failure transition | Unhandled exceptions kill the executive |

**Critical rule: `on_exit()` must be safe to call from any point in the state's lifetime**, including immediately after entry (preemption can arrive at any time). `on_exit()` is where you cancel action goals and command zero velocity. If you only stop the robot in the "happy path" transition, a preempt mid-`NAVIGATE` leaves the base driving.

## Flat FSM Skeleton (Python, the pattern to generate)

This is the minimal correct shape. Note: event queue, per-state timeout, entry/exit, guarded transitions, history log.

```python
import time, queue, logging, dataclasses
from enum import Enum, auto
from typing import Callable, Optional

log = logging.getLogger("fsm")

@dataclasses.dataclass(frozen=True)
class Event:
    name: str
    data: dict = dataclasses.field(default_factory=dict)
    stamp: float = dataclasses.field(default_factory=time.monotonic)

class State:
    name = "BASE"
    timeout_s: Optional[float] = 30.0     # default: every state times out

    def on_entry(self, ctx): pass
    def on_exit(self, ctx): pass          # MUST be idempotent & safe anytime
    def handle(self, ctx, ev: Event) -> Optional[str]:
        """Return next state name, or None to stay."""
        return None
    def on_timeout(self, ctx) -> str:
        """Every state defines its timeout exit. Default: error."""
        return "ERROR"

@dataclasses.dataclass
class TransitionRecord:
    stamp: float; src: str; dst: str; cause: str

class Machine:
    def __init__(self, states: dict[str, State], initial: str, ctx):
        self.states = states
        self.ctx = ctx
        self.events: queue.Queue[Event] = queue.Queue(maxsize=64)
        self.history: list[TransitionRecord] = []
        self.current = initial
        self._entered_at = time.monotonic()
        self.states[initial].on_entry(ctx)
        log.info("FSM start in %s", initial)

    def post(self, ev: Event):
        try:
            self.events.put_nowait(ev)
        except queue.Full:
            # NEVER silently drop — full queue means a consumer stall
            log.error("event queue full, dropping %s", ev.name)

    def _transition(self, dst: str, cause: str):
        src = self.current
        self.states[src].on_exit(self.ctx)          # exit FIRST, atomically
        rec = TransitionRecord(time.monotonic(), src, dst, cause)
        self.history.append(rec)
        log.info("FSM %s -> %s (%s)", src, dst, cause)
        self.current = dst
        self._entered_at = time.monotonic()
        self.states[dst].on_entry(self.ctx)

    def spin_once(self, block_s: float = 0.05):
        st = self.states[self.current]
        # 1. timeout check
        if st.timeout_s is not None and \
           time.monotonic() - self._entered_at > st.timeout_s:
            self._transition(st.on_timeout(self.ctx), "TIMEOUT")
            return
        # 2. drain one event
        try:
            ev = self.events.get(timeout=block_s)
        except queue.Empty:
            return
        # 3. stale-event guard: events older than entry to current state
        #    usually belong to the previous state — handle deliberately.
        if ev.stamp < self._entered_at:
            log.warning("stale event %s ignored in %s", ev.name, self.current)
            return
        nxt = st.handle(self.ctx, ev)
        if nxt is not None and nxt != self.current:
            self._transition(nxt, ev.name)
```

Things baked into this skeleton that AI-generated FSMs routinely get wrong:

- **Stale-event rejection.** An action result from the *previous* state arriving after transition must not drive the *new* state. Timestamp events; drop or explicitly route anything stamped before state entry.
- **Bounded queue with loud failure.** Unbounded queues hide stalls until memory dies; silent drops hide lost events. Bound it, log drops as errors.
- **`time.monotonic()`, never `time.time()`** for dwell timing — wall clock jumps (NTP, sim time) corrupt timeouts.
- **Exit-before-entry ordering** in `_transition`.

## Hierarchical FSMs (HSM): when and how

Use hierarchy when ≥2 of these hold:

- Multiple states share the same response to an event (e.g., `ESTOP_PRESSED` from anywhere → `SAFE_STOP`).
- A behavior decomposes into a sequence with its own internal failures (e.g., `DOCKING` = `APPROACH → ALIGN → CONTACT → LATCH`).
- You have >10–12 flat states. Flat machines beyond that size become transition spaghetti; transition count grows roughly O(states × events).

### HSM semantics that matter

1. **Event bubbling:** a substate that does not handle an event defers to its parent. This is how you write `ESTOP` handling *once* on the root state instead of N times. This is the single biggest payoff of HSMs.
2. **Entry/exit chains:** transitioning from `DOCKING.ALIGN` to `IDLE` runs `ALIGN.on_exit()` then `DOCKING.on_exit()` then `IDLE.on_entry()`. Exit innermost-first, enter outermost-first. Get this order wrong and parent cleanup runs before child cleanup (e.g., you power down the docking sensor while the alignment controller still reads it).
3. **Initial substates:** entering a composite state enters its designated initial substate. Decide explicitly whether re-entry resumes (**history pseudostate** — resume `ALIGN` where you left off) or restarts (`APPROACH` from scratch). For physical processes, **restart is almost always safer**: the world moved while you were in `ERROR_RECOVERY`. Use history only for pause/resume of stateless progress (e.g., a patrol route index), and persist the history variable explicitly.
4. **Composite-state outcomes:** a sub-machine terminates with a named outcome (`succeeded`/`failed`/`preempted`); the parent maps outcomes to its own transitions. Never let a child transition directly to a sibling of its parent — that breaks encapsulation and makes the child unreusable.

### Reference architecture: 3-layer mission executive

```
ROOT
├── BOOT            (self-test; → IDLE | FAULT)
├── IDLE            (await mission; heartbeat checks)
├── MISSION  [composite]
│   ├── NAV_TO_PICK     → PICK
│   ├── PICK [composite]
│   │   ├── PERCEIVE → PLAN_GRASP → EXECUTE_GRASP → VERIFY_GRASP
│   │   └── (any failure) → outcome: pick_failed
│   ├── NAV_TO_PLACE    → PLACE
│   └── PLACE [composite] ...
│   outcomes: succeeded → IDLE, *_failed → RECOVERY
├── RECOVERY [composite]
│   ├── CLASSIFY_FAULT → RETRY | REPOSITION | CALL_OPERATOR
│   └── retry budget exhausted → outcome: unrecoverable → FAULT
├── FAULT           (motion stopped, awaiting operator; NO timeout — documented)
└── SAFE_STOP       (reachable from EVERY state via root handler on ESTOP/comms-loss)
```

Design notes:
- `SAFE_STOP` and `FAULT` are root-level, reached by bubbled events. They are the only states allowed `timeout_s = None`, and that exemption is documented in code.
- `RECOVERY` carries a **retry budget in context** (e.g., `ctx.retries["pick"]`, start at 3). Decrement on entry to retry; on zero, escalate. Unbudgeted retry loops are the #1 cause of robots oscillating forever in the field (`PICK → fail → RETRY → PICK → ...`).
- Fault classification is its own state — do not branch on error strings inside transitions.

## Event Queue vs Polling

| | Event-driven (queue) | Polled (tick + condition checks) |
|---|---|---|
| Latency | Reacts immediately | Bounded by tick rate |
| Edge events (button press, action result) | Natural | Easy to miss between ticks |
| Level conditions (battery < 20%, pose within tolerance) | Awkward — needs edge detection upstream | Natural |
| Determinism / testability | Re-playable event log = perfect replays | Depends on sensor mocks |
| Failure mode | Queue overflow, stale events, event storms | Missed edges, tick-rate coupling |

**Production answer: hybrid.** Run a tick (10–50 Hz is typical for an executive; the FSM is not a control loop — do not run it at 1 kHz) that (a) drains the event queue and (b) evaluates level-condition guards. Discrete facts (action results, operator commands, e-stop) come in as events; continuous facts (battery, pose error, force threshold) are read fresh from context at evaluation time — **never cache continuous values inside events**, they are stale by the time they are handled.

Event storm protection: coalesce repeated identical events (a chattering bumper switch can post 200 `BUMP` events in a second — debounce at the source, and de-duplicate consecutive identical events in the queue).

## Transition Guards

A guard is a pure predicate over context evaluated at transition time. Rules:

- **Guards must be side-effect free.** A guard that commands hardware or mutates context creates untestable, order-dependent behavior. Side effects belong in entry/exit actions.
- **Guards must be fast** (<1 ms). A guard that calls a service blocks the executive. If a transition needs a slow check (e.g., "is the path clear?"), make the check a *state* (`CHECK_PATH`) that posts an event.
- **Guard on data validity, not just value.** `battery_pct < 20` is wrong if the BMS dropped out and `battery_pct` is 5 minutes old. Correct guard: `(now - battery_stamp < 2.0) and battery_pct < 20`; and a *separate* transition for stale data → `SENSOR_FAULT`. Stale-data-treated-as-fresh has driven robots off docks.
- When multiple guarded transitions can fire on the same event, define priority explicitly (ordered list). Safety transitions first, always.

```python
# Guard pattern: validity + value, with explicit priority ordering
TRANSITIONS = [  # evaluated in order; first match wins
    ("ANY",      lambda c: c.estop,                                  "SAFE_STOP"),
    ("NAVIGATE", lambda c: c.now() - c.battery_stamp > 2.0,          "SENSOR_FAULT"),
    ("NAVIGATE", lambda c: c.battery_pct < 15.0,                     "GO_CHARGE"),
    ("NAVIGATE", lambda c: c.goal_reached(),                         "ARRIVED"),
]
```

## State Timeouts — patterns and starting values

Every timeout needs three decisions: duration, what it means, where it goes.

| State type | Starting timeout | Timeout meaning | Timeout target |
|---|---|---|---|
| Hardware enable / homing | 10–30 s | Hardware fault | `FAULT` |
| Navigation to goal | `2.5 × (dist / nominal_speed)` + 10 s, recomputed on entry | Stuck / planner failure | `RECOVERY` |
| Grasp / manipulation primitive | 2–3× nominal execution time | Mechanical jam or perception error | `RECOVERY` |
| Waiting for operator | 5–15 min | Escalate notification | stay, re-alert (timeout resets) |
| Action-server result wait | server's own timeout + 5 s margin | Server hung | cancel goal → `RECOVERY` |
| `FAULT`, `SAFE_STOP` | none (documented) | — | — |

Patterns:
- **Dynamic timeouts**: compute in `on_entry()` from the goal (distance-based for nav). A fixed 60 s nav timeout is wrong for both a 2 m hop and a 200 m traverse.
- **Watchdog vs deadline**: a *deadline* is total dwell time; a *watchdog* resets on progress (e.g., reset while distance-to-goal is decreasing). Use watchdogs for long states where progress is measurable — they catch "stuck" in 5 s instead of 300 s.
- **Timeout escalation ladder**: first timeout → retry/recovery; second consecutive timeout of the same state → escalate (don't retry the same thing forever). Track consecutive-timeout count per state in context.
- On timeout, `on_exit()` still runs — this is where the in-flight action goal gets cancelled. Verify the cancel completed (or hard-stop) before commanding the next behavior; two active goals on one controller is undefined behavior.

## ROS2: SMACH vs yasmin vs hand-rolled vs BTs

- **SMACH** (`executive_smach`, ROS2 port): mature concepts (Concurrence, Sequence, hierarchical containers, `smach_viewer`-style introspection), Python-only, callback-style API showing its age. Fine for prototypes and labs.
- **yasmin** ("Yet Another State MachINe"): modern ROS2-native, Python *and* C++, built-in action/service client states (`ActionState`, `ServiceState`, `MonitorState`), blackboard, web/`yasmin_viewer` introspection, simpler API than SMACH. **Default recommendation for new ROS2 work.**
- **Hand-rolled** (skeleton above): when you need exact control over timing/preemption/logging, or no extra deps. Cost: you must implement introspection and the action-state plumbing yourself, correctly.
- **Behavior trees** (BehaviorTree.CPP / py_trees): prefer over FSMs when behavior is heavily *reactive* (conditions constantly re-checked, e.g., Nav2-style) or when non-engineers must author behaviors. Prefer FSMs when behavior is fundamentally *sequential with modal phases* and you need explicit, auditable transitions. Mixing is legitimate: FSM at mission level, BTs inside states (this is the Nav2 architecture inverted — Nav2 itself uses a BT with FSM-like recovery branches).

### yasmin pattern (the shape to generate for ROS2)

```python
import yasmin
from yasmin import StateMachine, Blackboard
from yasmin_ros import ActionState
from yasmin_ros.basic_outcomes import SUCCEED, ABORT, CANCEL, TIMEOUT
from nav2_msgs.action import NavigateToPose

class NavToPose(ActionState):
    def __init__(self):
        super().__init__(
            NavigateToPose, "/navigate_to_pose",
            create_goal_handler=self._goal_cb,
            outcomes=None,            # SUCCEED / ABORT / CANCEL
            timeout=120.0,            # yasmin adds TIMEOUT outcome
        )
    def _goal_cb(self, blackboard: Blackboard) -> NavigateToPose.Goal:
        g = NavigateToPose.Goal()
        g.pose = blackboard["target_pose"]
        return g

sm = StateMachine(outcomes=["mission_done", "mission_failed"])
sm.add_state("NAV_TO_PICK", NavToPose(), transitions={
    SUCCEED: "PICK",
    ABORT:   "RECOVERY",      # every ROS outcome mapped — no defaults
    CANCEL:  "mission_failed",
    TIMEOUT: "RECOVERY",
})
# ... add PICK (nested StateMachine), RECOVERY, etc.
yasmin.YasminViewerPub("mission_executive", sm)   # live introspection
```

Rules when generating SMACH/yasmin code:
- **Map every outcome** of every state, including `CANCEL`/`preempted` and `TIMEOUT`. Unmapped outcomes raise at construction (SMACH) or runtime — and a forgotten `ABORT` mapping is a robot that silently stops mid-mission.
- Blackboard keys: define them in one constants module; typo'd blackboard keys are runtime KeyErrors deep in a mission. Validate required keys in a `BOOT`/`VALIDATE` state, not lazily.
- Preemption: yasmin `ActionState` cancels the ROS action on state cancel; in hand-rolled code you must send `cancel_goal_async()` AND wait for the cancel response in `on_exit()` before declaring the state exited.
- Executive node: run the FSM in its own node with a `MultiThreadedExecutor` (or dedicated callback groups) so action feedback callbacks don't deadlock against the FSM's blocking waits. Single-threaded executor + blocking `ActionState` = classic ROS2 deadlock.

## Modeling Error States Explicitly

Anti-pattern: one global `ERROR` state. It destroys information — you arrive there from 15 places with 15 different recovery needs.

Production pattern:

1. **Typed fault context.** On any failure transition, write `ctx.fault = Fault(code, source_state, detail, stamp)` before transitioning. The recovery state reads it.
2. **`RECOVERY` is a composite state** with a `CLASSIFY` initial substate that switches on `fault.code`:
   - *Transient* (nav timeout, grasp slip, perception miss) → bounded retry, possibly with perturbation (re-perceive from new viewpoint, re-plan with inflated costmap).
   - *Degraded* (one sensor down, redundancy available) → reconfigure and continue with reduced capability + operator notification.
   - *Hard* (motor fault, e-stop, comms loss, self-test fail) → `FAULT`/`SAFE_STOP`, motion inhibited, operator required.
3. **Recovery actions are themselves states** with timeouts and error exits (recovery can fail too — `RECOVERY` failing must not transition back into `RECOVERY`; it escalates).
4. **Safety inversion rule:** entry into any error/fault state must *first* establish a safe actuator condition (zero velocity, gravity-compensated or braked arm, gripper hold-or-release per payload policy) *before* any diagnosis or logging. Safety in `on_entry()` first line, not after the log statement.
5. Distinguish **`FAULT`** (software-managed stop, recoverable by operator command → re-run `BOOT` self-test, never jump straight back to `MISSION`) from **`ESTOP`** (hardware safety chain; software merely observes it; exit requires physical reset then re-homing).

## Visualizing and Logging State History

You need three artifacts:

1. **Live state topic.** Publish `current_state` (full hierarchical path, e.g., `MISSION/PICK/VERIFY_GRASP`) on every transition AND latched/periodically at ~1 Hz (late-joining tools need it). In ROS2: a `String` or custom msg on `/executive/state`, plus yasmin_viewer / SMACH introspection server if using those libs.
2. **Transition log.** Structured, one record per transition: `{stamp, src, dst, cause_event, guard_results, fault_code?, dwell_s}`. Log dwell time of the exited state — dwell-time histograms are how you discover that `ALIGN` occasionally takes 40 s before it ever times out in front of a customer. Emit to rosbag (record `/executive/state` and `/executive/transitions`) and to plain log.
3. **Static diagram from code.** Generate Graphviz/PlantUML *from the transition table* (never hand-maintain a diagram — it will lie within a month):

```python
def to_dot(machine) -> str:
    lines = ["digraph fsm {", '  rankdir=LR;']
    for (src, _guard, dst) in machine.transition_table:
        lines.append(f'  "{src}" -> "{dst}";')
    for name, st in machine.states.items():
        if st.timeout_s is not None:
            lines.append(f'  "{name}" -> "{st.on_timeout_target}" [style=dashed,label="t>{st.timeout_s}s"];')
    lines.append("}")
    return "\n".join(lines)
```

Review the rendered diagram for: states with no error exit (dead ends), states unreachable from `BOOT`, and missing dashed timeout edges. This visual audit catches design holes faster than code review.

## Debugging Methodology

When a robot "got stuck" or "did something weird":

1. **Pull the transition log first.** Identify the state at the incident time and the last transition cause. 80% of behavior bugs are visible here without touching code.
2. **Check dwell time vs timeout.** Stuck = dwell exceeded expectation. Either the timeout was missing/too long, or the timeout fired but recovery looped (look for `A → RECOVERY → A → RECOVERY` cycles in the log — retry budget bug).
3. **Check for stale events.** A transition whose cause-event timestamp predates the source state's entry is a routing/staleness bug.
4. **Replay.** With an event-driven core, feed the recorded event log into the FSM in a unit test and reproduce the exact transition sequence deterministically. Build this replay harness on day one; it converts every field incident into a regression test.
5. **For Heisenbugs in transitions:** look for side effects in guards, non-idempotent `on_exit()`, or callbacks mutating context from another thread without the FSM's lock. The FSM core should be single-threaded; all external inputs enter via the queue (thread-safe boundary) — if any other code path mutates `ctx`, that is the bug until proven otherwise.

## Testing Requirements

- **Transition-table coverage:** a parameterized test asserting every (state, event) pair either transitions, is explicitly ignored, or bubbles — no accidental swallows.
- **Timeout tests with fake clock:** inject a controllable monotonic source; never `sleep()` in FSM tests.
- **Preemption tests:** post a preempt/e-stop event during *every* state and assert (a) `SAFE_STOP` is reached, (b) `on_exit()` cancelled the in-flight goal (assert on a mock action client).
- **Retry-budget exhaustion:** force N consecutive failures, assert escalation, not an infinite loop.
- **Fuzz the event queue:** random valid event sequences for 10k steps; assert no unhandled exception, no unknown state, queue never overflows at nominal rates.

## Quick Anti-Pattern Checklist (reject generated code containing these)

- State with no failure/timeout transition (except documented `FAULT`/`SAFE_STOP`).
- `while not done:` spin inside a state body with no timeout and no preempt check.
- Goal sent in `execute()`/tick instead of `on_entry()` (re-sends every tick).
- `on_exit()` missing goal cancellation / zero-velocity command for motion states.
- Guards with side effects, service calls, or sleeps.
- Global `ERROR` state with no fault context.
- Retry loops without a budget counter.
- `time.time()` for dwell/timeout measurement.
- Hand-drawn state diagram not generated from the transition table.
- State duplicated/mirrored in another node instead of subscribed.
