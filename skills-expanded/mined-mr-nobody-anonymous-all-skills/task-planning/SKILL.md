---
name: task-planning
description: "Use when building task-level autonomy for robots — multi-step missions, task queues, mission interruption/resumption, charging-aware planning, prioritized scheduling, or multi-robot task allocation. Provides PDDL planning concepts, persistent task queue architectures, return-to-dock hysteresis math, auction-based allocation algorithms, and the failure modes that strand robots in the field."
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


# Task Planning and Mission Autonomy

Task planning is the layer above motion planning: deciding *what* the robot does next, not *how* it moves. This is where robots fail embarrassingly in production — a robot that navigates flawlessly but forgets its mission after a reboot, drains its battery 200m from the dock, or deadlocks because two robots claimed the same task. This skill covers the architectures and math that prevent those failures.

## Layering: where task planning sits

```
┌─────────────────────────────────────────────┐
│ Mission layer (this skill)                  │  "deliver item A to room 3,
│  task queue, scheduler, allocator, PDDL     │   then inspect rack 7, then dock"
├─────────────────────────────────────────────┤
│ Behavior layer                              │  behavior trees / state machines
│  (see behavior-trees skill)                 │  executing ONE task
├─────────────────────────────────────────────┤
│ Skill layer                                 │  navigate_to(x,y), pick(obj),
│  Nav2 actions, MoveIt, grippers             │  open_gripper()
├─────────────────────────────────────────────┤
│ Control layer                               │  velocity controllers, PID
└─────────────────────────────────────────────┘
```

Hard rule: **the mission layer never sends velocity commands and never blocks on hardware.** It emits tasks; the behavior layer executes them and reports outcomes. Violating this layering is the #1 source of unrecoverable task-planner state.

---

## 1. PDDL: when you actually need a planner

Most deployed robots do NOT need PDDL — a prioritized queue covers 90% of products. You need symbolic planning when:

- Tasks have **preconditions that other tasks satisfy** (must pick up the key before opening the door).
- The action set is large enough that hand-writing the ordering is error-prone (>~15 interdependent action types).
- Missions are **generated from goals**, not enumerated by an operator ("make all shelves stocked" vs "go to shelf 1, then 2, …").

### PDDL in 60 seconds

A PDDL problem has a **domain** (action schemas with preconditions/effects) and a **problem** (objects, initial state, goal). The planner searches for an action sequence transforming init → goal.

```lisp
;; domain.pddl — minimal mobile manipulation domain
(define (domain warehouse)
  (:requirements :strips :typing)
  (:types robot location item)
  (:predicates
    (at ?r - robot ?l - location)
    (item-at ?i - item ?l - location)
    (holding ?r - robot ?i - item)
    (gripper-free ?r - robot))

  (:action move
    :parameters (?r - robot ?from ?to - location)
    :precondition (at ?r ?from)
    :effect (and (not (at ?r ?from)) (at ?r ?to)))

  (:action pick
    :parameters (?r - robot ?i - item ?l - location)
    :precondition (and (at ?r ?l) (item-at ?i ?l) (gripper-free ?r))
    :effect (and (holding ?r ?i) (not (item-at ?i ?l))
                 (not (gripper-free ?r))))

  (:action place
    :parameters (?r - robot ?i - item ?l - location)
    :precondition (and (at ?r ?l) (holding ?r ?i))
    :effect (and (item-at ?i ?l) (gripper-free ?r)
                 (not (holding ?r ?i)))))
```

```lisp
;; problem.pddl
(define (problem deliver-1)
  (:domain warehouse)
  (:objects rob - robot dock shelfA room3 - location box1 - item)
  (:init (at rob dock) (item-at box1 shelfA) (gripper-free rob))
  (:goal (item-at box1 room3)))
```

Plan output: `(move rob dock shelfA) (pick rob box1 shelfA) (move rob shelfA room3) (place rob box1 room3)`.

### Tooling

- **Fast Downward** — the standard classical planner. Solves problems with thousands of ground actions in milliseconds. `fast-downward.py domain.pddl problem.pddl --search "astar(lmcut())"` for optimal, `--alias lama-first` for fast satisficing.
- **PlanSys2** (`ros2 planning system`) — production ROS 2 integration: maintains the knowledge base, calls a PDDL planner (POPF/TFD), dispatches actions as ROS 2 action clients, supports durative actions and replanning. Use this rather than rolling your own dispatcher.
- **unified-planning** (Python, `pip install unified-planning`) — clean API over multiple planners; good for prototyping domains programmatically.

### PDDL failure modes on real robots

1. **The frame problem in practice**: the planner believes its effects perfectly. Real `pick` fails 5% of the time. You MUST verify postconditions after each action and **replan from observed state** on mismatch — never "continue and hope".
2. **State estimation drift**: the knowledge base says `(at rob shelfA)` but the robot was bumped to a different aisle. Refresh fluents from perception/localization before each planning episode, not just at startup.
3. **Goal impossibility**: a planner returning "no plan" looks identical to a planner crash. Always set a planner timeout (1–5 s for warehouse-scale domains) and have a fallback (report to operator, retry with relaxed goal).
4. **Plan length explosion**: numeric fluents (`:numeric-fluents`) and durative actions blow up search. Keep the symbolic domain coarse; push geometry and timing down to the behavior layer.

**Pattern: plan symbolically, execute reactively.** PDDL produces the task sequence; each task is executed by a behavior tree that handles retries and local recovery. Only escalate to replanning when the behavior layer reports unrecoverable failure.

---

## 2. Task queue architecture (the 90% solution)

For most products, a persistent prioritized queue with explicit task state is correct and sufficient.

### Task lifecycle state machine

```
PENDING ──claim──▶ ACTIVE ──success──▶ DONE
   ▲                 │
   │   requeue       ├──recoverable failure (retries left)──▶ PENDING (retry_count+1)
   │   (preempted)   ├──unrecoverable / retries exhausted──▶ FAILED
   └─────────────────┤
                     └──cancel──▶ CANCELLED
PAUSED ◀──interrupt── ACTIVE     (resumable tasks only)
```

Rules that prevent production bugs:

- Exactly **one task ACTIVE at a time** per robot (per actuator group if you truly have independent subsystems).
- Every transition is **persisted before it is acted on** (write-ahead). If the process dies between "marked ACTIVE" and "started moving", recovery logic sees an ACTIVE task and knows to re-validate it.
- `FAILED` and `CANCELLED` are terminal. Operators re-enqueue a *new* task; never resurrect terminal tasks (audit trail integrity).
- Retry with a cap (typical: 3) and backoff. Distinguish recoverable (path blocked, grasp slipped) from unrecoverable (target location not in map) at the behavior layer — the queue just routes on the reported class.

### Reference implementation (Python, SQLite-backed, ROS 2-friendly)

```python
import sqlite3, json, time, uuid
from dataclasses import dataclass
from enum import Enum

class TaskState(str, Enum):
    PENDING = "PENDING"; ACTIVE = "ACTIVE"; PAUSED = "PAUSED"
    DONE = "DONE"; FAILED = "FAILED"; CANCELLED = "CANCELLED"

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,           -- 'deliver', 'inspect', 'dock', ...
  params TEXT NOT NULL,         -- JSON: goal pose, item id, ...
  state TEXT NOT NULL,
  priority INTEGER NOT NULL,    -- higher = more urgent
  retry_count INTEGER DEFAULT 0,
  max_retries INTEGER DEFAULT 3,
  progress TEXT DEFAULT '{}',   -- JSON checkpoint, see §3
  created_ts REAL, updated_ts REAL,
  deadline_ts REAL              -- NULL = no deadline
);
"""

class TaskQueue:
    def __init__(self, db_path="/var/lib/robot/tasks.db"):
        # WAL mode: survives power loss far better than default journal
        self.db = sqlite3.connect(db_path)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")   # fsync every commit
        self.db.executescript(SCHEMA)

    def enqueue(self, task_type, params, priority=0, deadline_ts=None):
        tid = str(uuid.uuid4())
        now = time.time()
        self.db.execute(
            "INSERT INTO tasks (id,type,params,state,priority,created_ts,"
            "updated_ts,deadline_ts) VALUES (?,?,?,?,?,?,?,?)",
            (tid, task_type, json.dumps(params), TaskState.PENDING,
             priority, now, now, deadline_ts))
        self.db.commit()
        return tid

    def claim_next(self):
        """Atomically promote the best PENDING task to ACTIVE."""
        cur = self.db.execute(
            "SELECT id FROM tasks WHERE state='PENDING' "
            "ORDER BY priority DESC, created_ts ASC LIMIT 1")
        row = cur.fetchone()
        if row is None:
            return None
        tid = row[0]
        # Guard the transition — fails harmlessly if state changed under us
        n = self.db.execute(
            "UPDATE tasks SET state='ACTIVE', updated_ts=? "
            "WHERE id=? AND state='PENDING'", (time.time(), tid)).rowcount
        self.db.commit()
        return tid if n == 1 else None

    def checkpoint(self, tid, progress: dict):
        self.db.execute("UPDATE tasks SET progress=?, updated_ts=? WHERE id=?",
                        (json.dumps(progress), time.time(), tid))
        self.db.commit()

    def complete(self, tid, outcome: TaskState):
        assert outcome in (TaskState.DONE, TaskState.FAILED, TaskState.CANCELLED)
        self.db.execute("UPDATE tasks SET state=?, updated_ts=? WHERE id=?",
                        (outcome, time.time(), tid))
        self.db.commit()

    def report_failure(self, tid, recoverable: bool):
        cur = self.db.execute(
            "SELECT retry_count, max_retries FROM tasks WHERE id=?", (tid,))
        rc, mr = cur.fetchone()
        if recoverable and rc < mr:
            self.db.execute(
                "UPDATE tasks SET state='PENDING', retry_count=?, "
                "updated_ts=? WHERE id=?", (rc + 1, time.time(), tid))
        else:
            self.db.execute(
                "UPDATE tasks SET state='FAILED', updated_ts=? WHERE id=?",
                (time.time(), tid))
        self.db.commit()

    def recover_on_boot(self):
        """Call ONCE at startup, before the executor loop starts.
        Any ACTIVE task means we crashed mid-execution."""
        for (tid,) in self.db.execute(
                "SELECT id FROM tasks WHERE state IN ('ACTIVE','PAUSED')"):
            # Demote to PENDING; the executor re-validates and resumes
            # from the persisted progress checkpoint.
            self.db.execute(
                "UPDATE tasks SET state='PENDING', updated_ts=? WHERE id=?",
                (time.time(), tid))
        self.db.commit()
```

Why SQLite WAL + `synchronous=FULL` and not a JSON file: a JSON file rewritten on every update WILL eventually be corrupted by power loss mid-write, and you will find a robot idle in the field with an unparseable queue. SQLite's WAL gives atomic, durable transitions for free. Do not use `synchronous=OFF` to "speed it up" — the queue does single-digit writes per second; durability costs nothing here.

### Executor loop pattern (ROS 2)

```python
# Runs in the mission node. Behavior execution is delegated to a BT or
# action server — the loop itself never blocks longer than one tick.
def tick(self):
    if self.active_task is None:
        tid = self.queue.claim_next()
        if tid:
            self.active_task = self.start_behavior(tid)   # non-blocking
        return
    status = self.active_task.poll()       # RUNNING / SUCCESS / FAILURE
    if status == "SUCCESS":
        self.queue.complete(self.active_task.tid, TaskState.DONE)
        self.active_task = None
    elif status == "FAILURE":
        self.queue.report_failure(self.active_task.tid,
                                  self.active_task.recoverable)
        self.active_task = None
```

Run `tick()` on a 2–10 Hz timer. Faster buys nothing; slower delays preemption response.

---

## 3. Mission interruption and resumption

Robots get interrupted constantly: e-stop, operator pause, higher-priority task, charging, reboot, software update. A mission system that can't resume is a toy.

### Checkpoint design

Persist progress as a **semantic checkpoint**, not raw executor state. Serialize *what has been accomplished*, never *where in the code you were*.

```json
{
  "phase": "TRANSIT_TO_DROPOFF",
  "waypoints_total": 12,
  "waypoints_done": 7,
  "payload_secured": true,
  "last_confirmed_pose": {"x": 14.2, "y": 3.1, "yaw": 1.57},
  "checkpoint_ts": 1718012345.2
}
```

Bad checkpoint: pickled behavior-tree object, thread state, "line 142 of mission script". These do not survive code upgrades and encode assumptions about the world that are stale after an interruption.

Checkpoint **at semantic boundaries**: after each waypoint reached, after grasp confirmed, after door traversed. Checkpointing at 50 Hz is wasted I/O; checkpointing only at task start means redoing everything.

### Resume protocol (the part everyone gets wrong)

On resume, the world may have changed. Never blindly continue. Run this sequence:

1. **Re-localize**: confirm pose estimate is valid (covariance below threshold; AMCL converged). If not, run a localization recovery before anything else.
2. **Re-validate preconditions for the current phase**: if checkpoint says `payload_secured: true`, *check the gripper/payload sensor*. If the payload is gone, the checkpoint is a lie — fail the task or replan, don't deliver air.
3. **Re-plan the path**: never replay a stored trajectory after interruption. Obstacles moved. Plan fresh from current pose to the next semantic waypoint.
4. **Apply a staleness limit**: if `now - checkpoint_ts > T_stale` (typical 10–30 min for dynamic environments, hours for static), demote the resume to a restart-with-verification: drive to the last confirmed state and re-verify everything.

```python
def resume(self, task):
    p = task.progress
    if time.time() - p["checkpoint_ts"] > self.stale_limit_s:
        return self.restart_with_verification(task)
    if not self.localization_ok():
        if not self.run_localization_recovery():
            return self.fail(task, recoverable=True)
    if p.get("payload_secured") and not self.payload_sensor_confirms():
        return self.fail(task, recoverable=False)  # payload lost — operator
    next_wp = task.waypoints[p["waypoints_done"]]
    return self.navigate_to(next_wp)  # fresh plan, not replayed path
```

### Preemption (interruption by higher-priority task)

- Define which task types are **preemptible** (patrol: yes; mid-grasp manipulation: no — finish the atomic segment first). Mark non-preemptible *segments*, not whole tasks: "navigate" is preemptible, "lift payload" is not.
- On preempt: cancel the behavior at the next safe boundary, write checkpoint, set state PAUSED (or PENDING with progress retained), then claim the urgent task.
- **Priority inversion guard**: cap how long a low-priority task can hold a non-preemptible segment (watchdog, typical 30–120 s); if exceeded, treat as fault.

---

## 4. Prioritized scheduling

### Priority scheme that works in practice

Use a small number of bands, not a continuous score (continuous scores invite tuning wars and are impossible to reason about):

| Band | Value | Examples |
|------|-------|----------|
| EMERGENCY | 100 | e-stop recovery, fire-alarm egress |
| SAFETY | 80 | return-to-dock on critical battery, thermal shutdown park |
| OPERATOR | 60 | direct operator command |
| DEADLINE | 40 | scheduled delivery with due time |
| NORMAL | 20 | standard queue work |
| IDLE | 0 | patrol, opportunistic charging, map refresh |

Within a band, order FIFO (the `created_ts ASC` in `claim_next`). Across bands, strict priority with preemption.

### Starvation and deadlines

Strict priority starves low bands under load. Two fixes, use both:

- **Aging**: `effective_priority = priority + age_minutes * aging_rate`. Typical `aging_rate` = 0.5/min, capped so an aged NORMAL never exceeds SAFETY (cap effective at 59 in the table above).
- **Earliest Deadline First within the DEADLINE band**: among deadline tasks, order by `deadline_ts ASC`, and check feasibility at claim time: `now + estimated_duration + travel_time <= deadline_ts`, else flag to operator immediately rather than failing silently at the deadline.

```sql
-- claim_next with aging (replace the SELECT in §2)
SELECT id FROM tasks WHERE state='PENDING'
ORDER BY MIN(priority + (strftime('%s','now') - created_ts)/60.0 * 0.5, 59)
         DESC,
         COALESCE(deadline_ts, 1e18) ASC,
         created_ts ASC
LIMIT 1;
```

### Travel-aware ordering (batching)

Naive FIFO sends the robot zigzagging across the building. For ≤10 pending tasks of equal band, solve the mini-TSP by brute force or nearest-neighbor with 2-opt — this routinely cuts travel 30–50% in warehouse deployments:

```python
def order_by_travel(tasks, robot_pose, travel_cost):
    """Nearest-neighbor + 2-opt. travel_cost(a,b) should use the
    navigation graph (Nav2 ComputePathToPose length), NOT Euclidean —
    Euclidean lies badly indoors (walls)."""
    route, pos, remaining = [], robot_pose, list(tasks)
    while remaining:
        nxt = min(remaining, key=lambda t: travel_cost(pos, t.location))
        route.append(nxt); pos = nxt.location; remaining.remove(nxt)
    improved = True
    while improved:
        improved = False
        for i in range(len(route) - 1):
            for j in range(i + 2, len(route)):
                if (travel_cost_route(route[:i+1] + route[i+1:j+1][::-1]
                                      + route[j+1:], robot_pose)
                        < travel_cost_route(route, robot_pose)):
                    route[i+1:j+1] = route[i+1:j+1][::-1]
                    improved = True
    return route
```

Only batch within a priority band — never let travel optimization reorder across bands.

---

## 5. Charging-aware planning

The single most common field failure of mobile robots: dead battery away from the dock. The math is simple; the discipline is what's missing.

### Energy feasibility check (run before claiming ANY task)

```
E_needed = E_task + E_return_from_task_end + E_reserve

E_task               = travel_Wh(here → task) + work_Wh(task)
E_return_from_task_end = travel_Wh(task_end → nearest_dock)
E_reserve            = max(0.10 * E_capacity, 15 min of idle draw)
```

Claim the task only if `E_available >= E_needed`. Note the return leg is from the **task end location**, not from here — robots die because the task carried them away from the dock.

Estimate `travel_Wh(a → b)` as `path_length(a,b) / v_avg * P_drive`, with `path_length` from the nav graph. Calibrate `P_drive` (driving power draw, W) empirically: log battery Wh vs odometry over a week; typical differential-drive AMR: 60–150 W driving, 15–40 W idle, plus payload-dependent terms. Re-fit monthly — battery capacity fades ~20% over 500–1000 cycles, and your `E_capacity` constant must track the *current* full-charge capacity, not the nameplate.

### Return-to-dock thresholds with hysteresis

Two thresholds, never one:

```
SOC_go_charge   = 25%   # below this → enqueue SAFETY-band dock task
SOC_resume_work = 80%   # only above this may the robot leave the dock
SOC_critical    = 12%   # below this → abandon current task immediately,
                        # straight-line-priority dock, alert operator
```

Why hysteresis is mandatory: with a single threshold at 25%, the robot docks, charges to 26%, leaves, drives 5 minutes, drops to 24.5%, returns. It oscillates forever, accomplishing nothing and hammering the dock connector. The gap (25 → 80) guarantees each charge session yields a useful work window.

Tuning the numbers:

- `SOC_go_charge` must satisfy: `SOC_go_charge * E_capacity >= max_return_energy + E_reserve`, where `max_return_energy` is the worst-case dock-return from anywhere in the operating area. Compute it: farthest point on the nav graph from any dock. If your facility is large, 25% may be too low — do the math, don't copy the constant.
- `SOC_resume_work`: 80% is a good default for Li-ion — charging slows dramatically above 80% (CC→CV transition), so charging 80→100 takes nearly as long as 20→80. Stopping at 80% maximizes fleet duty cycle. Charge to 100% only on schedule (e.g., overnight) for cell balancing.
- Additionally apply **rate-of-change smoothing**: use SOC filtered over 60 s. Raw SOC from coulomb counters dips transiently under load spikes (acceleration, lift motor) and will false-trigger the threshold.

```python
class ChargingPolicy:
    GO, RESUME, CRIT = 0.25, 0.80, 0.12

    def __init__(self):
        self.charging_mode = False

    def update(self, soc_filtered, queue, robot):
        if soc_filtered <= self.CRIT:
            robot.abort_current_task(checkpoint=True)
            queue.enqueue("dock", {}, priority=80)   # SAFETY band
            self.charging_mode = True
            alert_operator("CRITICAL battery %.0f%%" % (soc_filtered*100))
        elif soc_filtered <= self.GO and not self.charging_mode:
            self.charging_mode = True
            queue.enqueue("dock", {}, priority=80)   # current task may
            # finish first if it passes the feasibility check below
        elif self.charging_mode and soc_filtered >= self.RESUME:
            self.charging_mode = False               # may undock and work

    def may_claim_work(self, soc_filtered):
        return not self.charging_mode
```

### Opportunistic charging

If the queue is empty and SOC < `SOC_resume_work`, dock. An idle robot not charging is wasted capacity. Make "opportunistic dock" an IDLE-band task so any real work preempts it (undock is fast).

### Dock contention (fleets)

N robots, M docks, N > M: treat docks as resources allocated by the same auction mechanism as tasks (§6), with bid = `urgency / travel_time`, urgency = `(SOC_go_charge − SOC)`. A robot at 13% two meters from the dock beats a robot at 24% across the building. Reserve at least one dock for CRITICAL-only if fleet utilization is high.

---

## 6. Multi-robot task allocation (MRTA)

Taxonomy (Gerkey & Matarić): ST-SR-IA — single-task robots, single-robot tasks, instantaneous assignment — is the common case and what this section covers. Anything fancier (coalitions, time-extended scheduling) — start by NOT needing it.

### Architecture decision

| Approach | Use when | Avoid when |
|----------|----------|------------|
| Central dispatcher | Reliable network to all robots; ≤ ~50 robots | Network partitions common |
| Auction (market-based) | Need graceful degradation, heterogeneous robots | — (good default) |
| Fully decentralized consensus (CBBA) | No central node allowed at all | You can run a central auctioneer (simpler) |

Auctions are the sweet spot: near-optimal in practice (single-item sequential auctions are within ~2x of optimal for travel cost; usually much closer), trivially handle heterogeneous robots (each bids its own cost), and degrade gracefully (a silent robot simply doesn't win).

### Sequential single-item auction

```
For each unassigned task t (in priority order):
  1. Auctioneer broadcasts t.
  2. Each eligible robot r computes bid(r, t) and replies within T_bid.
  3. Lowest bid wins; auctioneer sends award; robot ACKs.
  4. No ACK within T_award → award next-best bidder.
```

The bid is a **cost estimate** — lower wins:

```python
def compute_bid(self, task):
    if not self.capable_of(task.type):            return None
    if not self.energy_feasible(task):            return None   # §5 check!
    if self.charging_mode:                        return None
    # Marginal cost: insertion into my current route, not cost-from-idle.
    base = self.route_cost(self.current_route)
    best_insertion = min(
        self.route_cost(insert(self.current_route, task, i))
        for i in range(len(self.current_route) + 1))
    return best_insertion - base
```

**Marginal-cost (insertion) bidding** is the single most important detail: bidding `distance(me, task)` ignores commitments and overloads the nearest robot. Marginal cost makes load balancing emerge automatically.

Parameters that matter:
- `T_bid` = 500 ms–2 s. Too short loses bids on Wi-Fi jitter; too long stalls dispatch. 1 s default.
- Re-auction period: re-run allocation for PENDING (unstarted) tasks every 30–120 s — robot states change (battery, failures). **Never re-auction an ACTIVE task** except on executor failure.
- Award ACK timeout `T_award` = 2 s, 2 retries, then next bidder.

### Failure modes that kill fleets

1. **Double award / double claim**: auctioneer awards, ACK is lost, auctioneer re-awards to robot B, robot A also executes. Fix: award carries a monotonic `allocation_seq`; robots reject awards older than their last-seen seq for that task; auctioneer treats un-ACKed awards as void after `T_award` and explicitly sends CANCEL to the original awardee before re-awarding.
2. **Orphaned tasks on robot death**: a robot wins, then dies. Fix: heartbeat (1 Hz) from each robot to the auctioneer; missing 5 heartbeats → all that robot's non-terminal tasks return to PENDING and re-auction. The dead robot, on recovery, must check with the auctioneer whether it still owns its tasks **before** resuming them.
3. **Auctioneer death**: single point of failure. Fix for small fleets: auctioneer state is just the task table (§2 schema with an extra `assigned_robot` column) in a replicated store, plus a simple leader election (lowest robot ID alive becomes auctioneer). Don't reach for Raft libraries for a 5-robot fleet; do persist the table.
4. **Bid oscillation**: two robots alternately stealing a task on every re-auction because their costs are nearly equal. Fix: switching penalty — incumbent's bid gets a discount (10–20%); reassign only if the challenger is meaningfully better.
5. **Eligibility lies**: a robot bids without running the energy feasibility check, wins, then aborts at 15% battery. Make `energy_feasible` (§5) a hard gate inside `compute_bid` — shown above, because everyone forgets it.

### When to use CBBA instead

Consensus-Based Bundle Algorithm: each robot greedily builds a task bundle, broadcasts bids, and conflicts resolve by max-bid consensus over the mesh network. Use only when no node can be central (military/subterranean comms). Guarantees ≥50% of optimal; convergence in O(N·T) message rounds. Implementations exist but you will likely write your own — keep bundles small (≤5) and you'll be within sight of the sequential-auction quality.

---

## 7. Debugging methodology

When the mission layer misbehaves, follow this order — the bug is almost always state, not logic:

1. **Dump the task table first.** `sqlite3 tasks.db "SELECT id,type,state,priority,retry_count,progress FROM tasks ORDER BY updated_ts DESC LIMIT 20"`. A task stuck ACTIVE with a stale `updated_ts` = executor died without reporting. Tasks ping-ponging PENDING↔ACTIVE with rising `retry_count` = behavior layer failing fast; debug the behavior, not the queue.
2. **Event-log every transition** with cause: `task 7f3a PENDING→ACTIVE (claim_next, soc=0.61)`, `task 7f3a ACTIVE→PENDING (preempted by 9c21 prio=80)`. This log answers 95% of "why did the robot do that?" questions. Without it you are blind.
3. **Replay the decision**: feed logged inputs (SOC, queue snapshot, robot pose) into the scheduler function in a unit test and confirm it reproduces the bad decision. If it doesn't, your logged state differs from the live state — find the unlogged input.
4. **For allocation bugs**, log every bid with its breakdown (`base_cost`, `insertion_cost`, eligibility flags). "Why did robot 3 get that task?" must be answerable from the log alone.
5. **Simulate interruptions in CI**: a test harness that `kill -9`s the mission process at random points and asserts the queue recovers to a consistent state (no task lost, no task duplicated, no ACTIVE survivor) catches the persistence bugs that otherwise surface as a stranded robot at 2 a.m.

### Pre-deployment checklist

- [ ] Queue survives `kill -9` at any point (chaos test in CI)
- [ ] Resume after interruption re-validates preconditions and re-plans paths
- [ ] `SOC_go_charge` verified against worst-case return energy *for this facility's map*
- [ ] Hysteresis gap prevents dock oscillation (soak test: 8 h, count dock events)
- [ ] Energy feasibility gate inside bid computation
- [ ] Heartbeat-based orphan recovery tested by pulling a robot's network cable mid-task
- [ ] Deadline-infeasible tasks alert at claim time, not at the deadline
- [ ] Aging prevents IDLE-band starvation under sustained NORMAL load
- [ ] Every state transition appears in the event log with cause
