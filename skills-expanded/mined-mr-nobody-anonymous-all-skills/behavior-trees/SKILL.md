---
name: behavior-trees
description: "Use when designing robot task logic, mission sequencing, or replacing a finite state machine that has become unmaintainable. Provides expert knowledge of behavior trees: node semantics (sequence/fallback/parallel/decorators), tick-based execution, BehaviorTree.CPP v4 and py_trees/py_trees_ros patterns, blackboard data flow, ROS2 action integration, interruptibility/reactivity design, and the antipatterns (blocking ticks, conditions with side effects, blackboard abuse) that break BTs in production."
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


# Behavior Trees for Robot Task Logic

## Why BTs beat FSMs at scale

An FSM with N states and M transitions per state has O(N×M) edges to maintain. Adding one
state ("low battery → go charge") means touching *every* existing state to add an exit
transition. A BT expresses the same thing with **one reactive fallback at the root** —
zero changes to existing behavior.

| Property | FSM | Behavior Tree |
|---|---|---|
| Adding a global interrupt (e-stop, low battery) | Edit every state | Add 1 condition node high in tree |
| Reusing a sub-behavior ("dock") | Copy states + rewire transitions | Subtree reference, drop in anywhere |
| Execution model | Event-driven, transitions fire once | **Tick-driven**, root ticked at fixed rate (10–100 Hz typical) |
| Where is "current state"? | Explicit state variable | Implicit — the set of RUNNING nodes |
| Failure handling | Explicit error states everywhere | FAILURE propagates up, fallback catches it |
| Readability at 50+ behaviors | Spaghetti diagram | Still a readable tree |

Rule of thumb: **≤5 states and no shared interrupts → FSM is fine** (it's simpler).
Anything with retries, recovery behaviors, priority interrupts, or reuse → BT.

The key mental shift: a BT does not "transition". Every tick, control flow re-evaluates
**from the root down**. Reactivity falls out of node ordering, not transition tables.

## Node semantics — exact rules

Every node returns one of exactly three statuses per tick: `SUCCESS`, `FAILURE`, `RUNNING`.
(BehaviorTree.CPP also has `SKIPPED` for pre-conditions — ignore until needed.)

### Sequence (`->`) — "do A then B then C"
- Ticks children left to right.
- Child returns FAILURE → sequence returns FAILURE immediately, **resets** (next tick restarts at child 0... depending on variant, see below).
- Child returns RUNNING → sequence returns RUNNING.
- All children SUCCESS → SUCCESS.

Three variants in BehaviorTree.CPP — picking the wrong one is the #1 source of BT bugs:

| Variant | On child RUNNING, next tick resumes at | On child FAILURE | Use for |
|---|---|---|---|
| `Sequence` | same child (memory) | restart from child 0 | default plain sequencing |
| `ReactiveSequence` | **child 0 — re-ticks all earlier children** | restart from child 0 | guard conditions that must stay true (e.g. `IsPathClear -> FollowPath`) |
| `SequenceWithMemory` | same child | **resume at the failed child** (doesn't re-run succeeded ones) | one-shot mission steps you must not repeat (e.g. `PickObject`) |

py_trees equivalent: `Sequence(memory=True)` ≈ `Sequence`; `Sequence(memory=False)` ≈ `ReactiveSequence`.

### Fallback / Selector (`?`) — "try A, else B, else C"
- Child SUCCESS → fallback returns SUCCESS immediately.
- Child FAILURE → tick next child.
- All fail → FAILURE.
- `ReactiveFallback`: while a child is RUNNING, earlier (higher-priority) children are
  re-ticked every tick — this is how you implement **priority interruption**:

```
ReactiveFallback
├── BatteryOK?          # condition: returns SUCCESS while battery fine
└── GoCharge            # only runs when BatteryOK fails... wait, NO — see antipattern #4
```

Careful — fallback runs the *next* child when the previous **fails**. So the pattern above
is wrong as a "charge when low" trigger written naively; the correct idiom is:

```
ReactiveFallback                     # "ensure battery handled, else do mission"
├── Sequence
│   ├── BatteryLow?                  # SUCCESS when battery IS low
│   └── GoChargeAndWaitFull
└── DoMission
```
No — also wrong: if battery is fine, `BatteryLow?` FAILS → sequence FAILS → mission runs. Good.
If battery is low → charge subtree runs, mission is preempted (ReactiveFallback re-ticks child 0
every tick while DoMission is RUNNING). This is the canonical reactive-interrupt pattern.
Write it exactly this way.

### Parallel
- Ticks ALL children every tick.
- BehaviorTree.CPP: `Parallel` with `success_count`/`failure_count` thresholds
  (`success_count=-1` means "all"). py_trees: `Parallel(policy=SuccessOnAll | SuccessOnOne)`.
- Use for: monitoring while acting (`MonitorCollision || FollowPath`), driving + speaking.
- Do NOT use for true concurrency of blocking work — BT ticks are single-threaded;
  children must each return quickly (RUNNING) and do work asynchronously.

### Decorators (single child)
| Decorator | Behavior | Typical robot use |
|---|---|---|
| `Inverter` | SUCCESS↔FAILURE (RUNNING passes through) | turn `ObstacleDetected` into a guard |
| `RetryUntilSuccessful(N)` | re-tick child up to N times on FAILURE | flaky grasp, `num_attempts=3` |
| `Repeat(N)` | re-tick child N times on SUCCESS | patrol loop |
| `Timeout(ms)` | FAILURE if child RUNNING longer than ms | cap navigation at 30000 ms |
| `ForceSuccess` / `ForceFailure` | override child result | optional steps ("try to announce, don't care if TTS fails") |
| `KeepRunningUntilFailure` | converts SUCCESS to RUNNING | continuous monitors |
| `Delay(ms)` | wait before ticking child | settle time after docking |
| py_trees `EternalGuard` | re-evaluates condition every tick, halts child on fail | hardware interlocks |

### Conditions vs Actions
- **Condition**: returns SUCCESS/FAILURE *instantly*, never RUNNING, never changes the world.
- **Action**: may return RUNNING across many ticks; does the work.
If you can't classify a node as one of these, your design is wrong.

## Tick rate and timing constraints

- Root tick rate: **10 Hz is the standard default** (Nav2 uses 10 Hz, `bt_loop_duration: 10ms`
  internally with 100 ms outer loop). Manipulation trees often run 50–100 Hz.
- **Hard rule: one full tree tick must complete in well under the tick period.**
  At 10 Hz that's <<100 ms; budget <10 ms for tree traversal itself. Any node tick that
  blocks (sleep, service call wait, `rclpy.spin_until_future_complete`) freezes the entire
  tree — no interrupts, no monitors, nothing runs. This is the single most common BT bug.
- Long work pattern: on first tick, *start* async work (send ROS2 action goal, launch thread,
  set non-blocking I/O); on subsequent ticks, *poll* and return RUNNING until done.
- Reactivity latency = tick period. A guard checked via ReactiveSequence at 10 Hz reacts
  within 100 ms worst case. If you need <10 ms reaction (collision stop), do it in the
  controller layer, not the BT — BTs are for *task* logic, not safety loops.

## BehaviorTree.CPP v4 (C++ / ROS2, used by Nav2)

### Minimal correct custom nodes

```cpp
#include <behaviortree_cpp/bt_factory.h>
using namespace BT;

// CONDITION — instant, side-effect free
class IsBatteryLow : public ConditionNode {
public:
  IsBatteryLow(const std::string& name, const NodeConfig& cfg)
    : ConditionNode(name, cfg) {}
  static PortsList providedPorts() {
    return { InputPort<double>("threshold", 0.2, "fraction 0-1") };
  }
  NodeStatus tick() override {
    double thr = getInput<double>("threshold").value();
    // read from cached subscriber value — NEVER call a service here
    return (g_battery_fraction.load() < thr) ? NodeStatus::SUCCESS
                                             : NodeStatus::FAILURE;
  }
};

// ASYNC ACTION — StatefulActionNode gives you onStart/onRunning/onHalted
class MoveToPose : public StatefulActionNode {
public:
  MoveToPose(const std::string& name, const NodeConfig& cfg)
    : StatefulActionNode(name, cfg) {}
  static PortsList providedPorts() {
    return { InputPort<Pose2D>("goal") };
  }
  NodeStatus onStart() override {
    auto goal = getInput<Pose2D>("goal");
    if (!goal) { throw RuntimeError("missing goal: ", goal.error()); }
    sendNavGoalAsync(goal.value());        // non-blocking
    return NodeStatus::RUNNING;
  }
  NodeStatus onRunning() override {        // called each tick while RUNNING
    switch (pollNavResult()) {
      case Nav::SUCCEEDED: return NodeStatus::SUCCESS;
      case Nav::FAILED:    return NodeStatus::FAILURE;
      default:             return NodeStatus::RUNNING;
    }
  }
  void onHalted() override {               // PREEMPTION — must cancel real work
    cancelNavGoal();                       // forgetting this = robot keeps driving
  }
};
```

`onHalted()` is called when a higher-priority branch takes over (e.g. ReactiveFallback
switches children). **If onHalted doesn't cancel the underlying action goal, the robot
continues executing the old command while the tree thinks it stopped.** This causes the
classic "robot drives to two goals at once" bug.

### Registering and running

```cpp
BehaviorTreeFactory factory;
factory.registerNodeType<IsBatteryLow>("IsBatteryLow");
factory.registerNodeType<MoveToPose>("MoveToPose");
auto tree = factory.createTreeFromFile("mission.xml");

// Correct tick loop — do NOT use tickWhileRunning() if you need a fixed rate
while (rclcpp::ok()) {
  tree.tickOnce();                          // v4 API (v3 was tickRoot())
  std::this_thread::sleep_for(100ms);       // 10 Hz
}
```

### XML tree (v4: `BTCPP_format="4"`)

```xml
<root BTCPP_format="4" main_tree_to_execute="Mission">
  <BehaviorTree ID="Mission">
    <ReactiveFallback>
      <Sequence name="charge_if_needed">
        <IsBatteryLow threshold="0.25"/>
        <SubTree ID="GoCharge"/>
      </Sequence>
      <SequenceWithMemory name="patrol">
        <MoveToPose goal="{wp1}"/>
        <MoveToPose goal="{wp2}"/>
        <RetryUntilSuccessful num_attempts="3">
          <MoveToPose goal="{dock_approach}"/>
        </RetryUntilSuccessful>
      </SequenceWithMemory>
    </ReactiveFallback>
  </BehaviorTree>

  <BehaviorTree ID="GoCharge">
    <Sequence>
      <MoveToPose goal="{charger_pose}"/>
      <Timeout msec="600000">
        <WaitUntilCharged level="0.9"/>
      </Timeout>
    </Sequence>
  </BehaviorTree>
</root>
```

`{wp1}` syntax = blackboard pointer. SubTrees get an **isolated blackboard**; remap
explicitly: `<SubTree ID="GoCharge" charger_pose="{charger_pose}"/>` or use
`_autoremap="true"` (v4) — prefer explicit remapping, autoremap hides coupling.

### Nav2 integration notes
- Nav2's `bt_navigator` loads BT XML per navigation request; custom nodes ship as plugins
  (`nav2_behavior_tree::BtActionNode<ActionT>` base class wraps a ROS2 action client with
  correct async semantics — inherit from it instead of hand-rolling).
- Register plugin in `bt_navigator` params: `plugin_lib_names: [my_bt_nodes]`.
- Nav2 BT nodes communicate via the blackboard keys `goal`, `goals`, `path`, `node`
  (the rclcpp node ptr) — read Nav2's `navigate_to_pose_w_replanning_and_recovery.xml`
  before writing your own; it's the canonical recovery-pattern reference.

## py_trees + py_trees_ros (Python / ROS2)

```python
import py_trees
import py_trees_ros
from nav2_msgs.action import NavigateToPose

class BatteryLow(py_trees.behaviour.Behaviour):
    """Condition: reads blackboard, no side effects, never RUNNING."""
    def __init__(self, name="BatteryLow?", threshold=0.25):
        super().__init__(name)
        self.threshold = threshold
        self.bb = self.attach_blackboard_client()
        self.bb.register_key("battery_pct", access=py_trees.common.Access.READ)

    def update(self):
        try:
            low = self.bb.battery_pct < self.threshold
        except KeyError:                       # sensor not published yet
            return py_trees.common.Status.FAILURE
        return (py_trees.common.Status.SUCCESS if low
                else py_trees.common.Status.FAILURE)


def make_root():
    root = py_trees.composites.Selector("Root", memory=False)  # reactive fallback

    charge = py_trees.composites.Sequence("ChargeIfNeeded", memory=False)
    charge.add_children([
        BatteryLow(),
        py_trees_ros.actions.ActionClient(          # wraps ROS2 action correctly:
            name="GoToCharger",                     # async send, RUNNING while active,
            action_type=NavigateToPose,             # cancels goal on halt/preempt
            action_name="navigate_to_pose",
            action_goal=charger_goal(),
        ),
    ])

    mission = py_trees.composites.Sequence("Mission", memory=True)
    mission.add_children([nav_action("WP1", wp1), nav_action("WP2", wp2)])

    root.add_children([charge, mission])
    return root


# Data ingress: subscriber -> blackboard, the py_trees_ros idiom
def make_data2bb():
    return py_trees_ros.battery.ToBlackboard(
        name="Battery2BB", topic_name="/battery_state",
        qos_profile=py_trees_ros.utilities.qos_profile_unlatched(),
        threshold=0.25,
    )

# Tree setup + tick at 10 Hz
tree = py_trees_ros.trees.BehaviourTree(root=make_root(), unicode_tree_debug=True)
tree.setup(node_name="mission_bt", timeout=15.0)
tree.tick_tock(period_ms=100)                       # 10 Hz; rclpy spun internally
```

py_trees specifics that bite people:
- `memory=False` on Selector/Sequence = reactive (re-tick from first child each tick);
  `memory=True` = resume at running child. **Default differs between composites across
  versions — always pass it explicitly.**
- `update()` is your tick. `initialise()` is called when the node goes from non-RUNNING
  to ticked (≈ onStart). `terminate(new_status)` is called on halt/completion (≈ onHalted) —
  cancel goals there.
- Standard pattern: a top-level `Parallel` with a "Topics2BB" branch (all subscribers→
  blackboard) and the "Tasks" branch. Data ingress happens every tick before logic runs:

```python
root = py_trees.composites.Parallel(
    "TopLevel",
    policy=py_trees.common.ParallelPolicy.SuccessOnAll(synchronise=False))
root.add_children([topics2bb, tasks])
```

## Blackboard data flow — rules

The blackboard is shared key/value memory. It is also the easiest way to ruin a BT.

1. **Declare ports** (BT.CPP) / **register keys with access mode** (py_trees). Undeclared
   access works in py_trees ≥2.0 only if you attach a client — use READ/WRITE declarations
   so `py_trees.display.unicode_blackboard()` shows the real dataflow.
2. **Writer/reader discipline**: each key has exactly ONE writer node (or one ingress
   subscriber). Multiple writers = race decided by tick order = heisenbug.
3. **Namespace per subtree** (BT.CPP does this automatically; in py_trees use key
   namespaces like `/mission/target_pose`).
4. Pass data via ports, not globals. In BT.CPP XML, `{key}` on an output port of one node
   and input port of another is the contract: `<ComputeGrasp target="{object_pose}" grasp="{grasp_pose}"/>` → `<ExecuteGrasp grasp="{grasp_pose}"/>`.
5. Stale-data guard: stamp blackboard entries (`(value, time)`), and have conditions FAIL
   if data older than N ms. A BT happily acts on a 40-second-old obstacle reading otherwise.

## Interruptibility / preemption design

The whole point of BTs. Recipe:

1. Order children of a **ReactiveFallback** by priority: safety > battery > user-commands > mission.
2. Each priority branch starts with a **condition** ("is this branch needed?"), so it FAILS
   fast when not applicable and the tick falls through to lower priority.
3. Every Action node MUST implement halt/terminate to **cancel its underlying goal**.
4. Long mission steps that must not repeat go under `SequenceWithMemory` /
   `Sequence(memory=True)` so that after an interruption + recovery, the mission resumes
   where it left off instead of restarting.
5. Test preemption explicitly: publish the interrupt mid-action and verify (a) old action
   goal got a cancel request, (b) tree shows old branch halted, (c) on interrupt clearing,
   mission resumes at correct child.

## Antipatterns — the mistakes everyone makes

1. **Blocking inside tick().** `rclpy.spin_until_future_complete`, `time.sleep`,
   synchronous service calls, `action_client.send_goal()` (sync version). The whole tree
   freezes; reactive guards stop guarding. Fix: async send + poll, or use
   `py_trees_ros.actions.ActionClient` / `BtActionNode` which do it correctly.
2. **Conditions with side effects.** A `IsDoorOpen` condition that *also* sends the
   open-door command. Reactive composites re-tick conditions every tick (10 Hz) → the
   command spams 10× per second, and tree semantics become unreadable. Conditions read;
   actions write. No exceptions.
3. **Wrong sequence variant.** Plain `Sequence` around `ApproachObject -> Grasp -> Retreat`
   with a reactive parent: after preemption it restarts at `ApproachObject` even though
   the object is already grasped → robot re-grasps air. Use `SequenceWithMemory`.
   Conversely, `SequenceWithMemory` for `IsPathClear -> Drive` never re-checks the guard. Use `ReactiveSequence`.
4. **Inverted-condition fallbacks.** Writing `Fallback(BatteryOK?, GoCharge)` — this *works*
   but reads as "battery ok OR charge", and the moment someone adds a third child the
   semantics break. Prefer `Fallback(Sequence(BatteryLow?, GoCharge), Mission)`.
5. **Blackboard as global soup.** 60 keys, every node reads/writes everything, behavior
   depends on tick order. Enforce one-writer rule and port declarations.
6. **No halt implementation.** Default `onHalted()`/`terminate()` does nothing → preempted
   nav goals keep executing. Always cancel.
7. **Using the BT as a control loop.** PID, trajectory following, collision reflexes do not
   belong in 10 Hz tree ticks. BT decides *what* to do; controllers (100 Hz–1 kHz) decide *how*.
8. **Deep trees for sequential scripts.** If your "tree" is one 14-child Sequence with no
   fallbacks, you didn't need a BT. That's a script — fine, but don't add the framework tax.
9. **RUNNING leaks from conditions.** A condition returning RUNNING stalls Reactive
   composites in surprising ways. Conditions return SUCCESS/FAILURE only.
10. **Parallel for blocking children.** Parallel ticks children sequentially in one thread.
    Two children that each block 80 ms = 160 ms tick at "10 Hz". Children must be async.
11. **Restart-vs-resume confusion after FAILURE.** Plain `Sequence` in BT.CPP restarts from
    child 0 after FAILURE; `SequenceWithMemory` resumes at the failed child on the next tick
    *if re-ticked* — wrap in `RetryUntilSuccessful` deliberately, don't rely on parent retick accidents.

## Debugging checklist

Work top to bottom:

1. **Visualize live.** BT.CPP: Groot2 (`tree.subscribeToGrootMonitor` /
   `BT::Groot2Publisher pub(tree, 1667);` then connect Groot2 to port 1667).
   py_trees_ros: `py-trees-tree-watcher` CLI or `py_trees_ros_viewer` (Qt). Watching the
   RUNNING path in real time finds 80% of bugs instantly.
2. **Print the tree + blackboard each tick** while developing:
   `py_trees.display.unicode_tree(root, show_status=True)` and
   `py_trees.display.unicode_blackboard()`. BT.CPP: `BT::printTreeRecursively(tree.rootNode())`
   plus `StdCoutLogger logger(tree);` for per-node status transitions.
3. **Tick by hand.** Don't run at 10 Hz while debugging logic — call
   `tree.tickOnce()` / `root.tick_once()` in a REPL/test and inspect status after each tick.
4. **Measure tick duration.** Wrap the tick in a timer; alert if > 20% of period. A slowly
   growing tick time means someone added a blocking call.
5. **Symptom → cause table:**

| Symptom | Likely cause |
|---|---|
| Tree stuck RUNNING, nothing reacts | blocking call inside a tick (antipattern 1) |
| Interrupt branch never fires | parent is non-reactive (`Sequence`/`Fallback` with memory) |
| Action repeats / spams commands | condition with side effect, or reactive parent re-ticking an action that returns SUCCESS instantly |
| Robot keeps moving after preemption | missing halt/terminate cancel (antipattern 6) |
| Mission restarts from beginning after recovery | plain Sequence where SequenceWithMemory needed |
| Works in isolation, fails in full tree | blackboard key collision / multiple writers |
| First tick fails, second succeeds | reading blackboard key before ingress branch populated it — gate with a "data fresh?" condition |
| Nondeterministic branch choice | two writers racing on one key; or unstamped stale data |
6. **Unit-test nodes off-robot.** Both frameworks let you tick a single node with a mock
   blackboard. Test the SUCCESS, FAILURE, RUNNING→SUCCESS, and RUNNING→halt paths — four
   tests per action node, minimum.
7. **Log status *transitions*, not statuses.** 10 Hz × 50 nodes = noise. BT.CPP
   `TreeObserver`/`StdCoutLogger` and py_trees' `post_tick_handler` with a status-change
   filter give readable traces.

## Quick design procedure for a new robot behavior

1. List interrupts by priority (e-stop handled below BT; then battery, user cancel, ...).
2. Root = ReactiveFallback ordered by that priority; each branch = `Sequence(Condition, Handler)`.
3. Lowest-priority child = the mission, usually `SequenceWithMemory` of steps.
4. Wrap flaky steps in `RetryUntilSuccessful(n)`, unbounded steps in `Timeout(ms)`.
5. Data ingress: subscribers → blackboard at tree top (py_trees Parallel idiom) or cached
   atomics (BT.CPP). One writer per key.
6. Implement halt/terminate with real cancellation for every action.
7. Tick at 10 Hz; verify max tick time < 10 ms; test each preemption path by hand.
