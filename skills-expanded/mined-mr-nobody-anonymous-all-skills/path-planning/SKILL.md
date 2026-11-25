---
name: path-planning
description: "Use when implementing or debugging robot path planning — A*/Dijkstra/D* Lite on occupancy grids, RRT/RRT* for high-DOF spaces, costmap inflation, global/local planner architecture, path smoothing, or planning frequency budgets. Provides the math, parameter starting values, and failure modes for production-grade planners."
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


# Path Planning

Expert knowledge for grid-based and sampling-based planning on real robots. Covers algorithm selection, admissible heuristics, costmap construction, replanning, smoothing, and the timing budgets that keep a robot from freezing mid-aisle or clipping a shelf corner.

## 0. Mental Model: The Two-Planner Split

Production mobile robots (Nav2, move_base, most AMR stacks) split planning into:

```
                 ┌────────────────────────────────────────────┐
   map + goal →  │ GLOBAL PLANNER (0.5–2 Hz)                  │
                 │ A* / Dijkstra / Theta* on global costmap   │
                 │ Output: coarse path, full map horizon      │
                 └──────────────────┬─────────────────────────┘
                                    │ path (waypoints)
                 ┌──────────────────▼─────────────────────────┐
  sensors      → │ LOCAL PLANNER / CONTROLLER (10–50 Hz)      │
  (rolling       │ DWB / TEB / MPPI / RPP on local costmap    │
   costmap)      │ Output: cmd_vel respecting dynamics        │
                 └────────────────────────────────────────────┘
```

**Why split:** the global planner solves a geometric problem on stale-ish map data; the local planner solves a kinodynamic problem on fresh sensor data. Trying to do both in one planner forces you to either plan kinodynamically over the whole map (too slow) or ignore dynamics (robot can't follow the path).

**Contract between them:**
- Global path must be *feasible enough* — stay outside the inscribed-radius lethal zone so the local planner has room.
- Local planner treats the global path as a reference, not a command. It may deviate within its costmap window (typ. 3–6 m).
- If the local planner can't make progress for N seconds (typ. 5 s), trigger global replan; if that fails, run recovery behaviors (clear costmap, rotate in place, back up).

This skill covers the global side plus the costmap and smoothing layers. Local trajectory control (DWA/TEB/MPPI) is its own discipline; here you only need its *interface requirements*.

## 1. Occupancy Grids and Costmaps

### 1.1 Representation

- Grid resolution: **0.05 m** is the standard for indoor robots (matches typical lidar accuracy and Nav2 defaults). 0.025 m for tight docking maneuvers; 0.1 m for large warehouses (cuts cell count 4x).
- Cell values (Nav2/ROS convention, `uint8`):
  - `0` = FREE
  - `1–252` = increasing cost
  - `253` = INSCRIBED_INFLATED_OBSTACLE (collision if robot center here)
  - `254` = LETHAL_OBSTACLE (actual sensed obstacle)
  - `255` = NO_INFORMATION (unknown)
- Memory: a 100 m × 100 m map at 0.05 m is 2000×2000 = 4M cells = 4 MB per layer. Fine. At 0.01 m it's 100M cells — don't.

### 1.2 Inflation: inscribed vs circumscribed radius

The single most important — and most commonly misconfigured — costmap concept.

- **Inscribed radius** r_in: radius of the largest circle *inside* the robot footprint. If the robot *center* is within r_in of an obstacle, collision is **guaranteed regardless of orientation**. Cells within r_in of a lethal cell get cost 253.
- **Circumscribed radius** r_circ: radius of the smallest circle *containing* the footprint. If the center is farther than r_circ from every obstacle, collision is **impossible regardless of orientation**. Between r_in and r_circ, collision **depends on heading** — a circular-footprint planner must treat this band conservatively or do true footprint (polygon) collision checking.

For a rectangular robot W wide × L long:
```
r_in   = min(W, L) / 2
r_circ = sqrt(W² + L²) / 2
```
Example: 0.6 m × 0.9 m AMR → r_in = 0.30 m, r_circ = 0.541 m.

**Cost decay** outside the inscribed zone (Nav2 inflation layer):
```
cost(d) = 252 * exp(-cost_scaling_factor * (d - r_in))    for d > r_in
```
Starting values:
- `inflation_radius`: **1.5–2.0 × r_circ** (e.g. 1.0 m for the AMR above). Too small → planner hugs walls and the local planner constantly fights obstacle gradients. Too large → corridors narrower than 2×inflation_radius become "blocked" even though the robot fits.
- `cost_scaling_factor`: **3.0** (Nav2 default 10 is aggressive; 3.0 gives smoother gradients that pull paths toward corridor centers).

**Failure mode:** robot fits through a 0.8 m doorway (footprint 0.6 m) but planner says no path. Cause: inflation_radius 1.0 m + high cost near 253 makes both sides' inflation overlap above the planner's lethal threshold. Fix: planner must accept cost ≤ 252 cells (only 253/254 lethal), and verify cost_scaling_factor isn't saturating the doorway. Don't shrink the footprint to "fix" this — that trades a planning failure for a physical collision.

**Failure mode:** robot clips obstacles when rotating in place near walls. Cause: planner used r_in (circular approximation) for a long rectangular robot; in the r_in–r_circ band, orientation matters. Fix: footprint collision checking in the local planner (`footprint` param as polygon, not `robot_radius`), or treat circumscribed cost as lethal in the global planner (`cost_possibly_inscribed = 128` threshold trick in Nav2: lethal if cost ≥ inscribed cost computed for r_circ).

### 1.3 Layered costmaps

Standard layer stack (bottom → top):
1. **Static layer** — from SLAM map. Unknown = 255.
2. **Obstacle/voxel layer** — live sensor marking + raytrace clearing. Key params: `obstacle_max_range` 2.5 m (marking), `raytrace_max_range` 3.0 m (clearing — must be ≥ marking range or ghosts persist), `max_obstacle_height` ≥ robot height.
3. **Inflation layer** — always **last**; it inflates whatever the layers below produced.

**Failure mode (ghost obstacles):** robot stops for an obstacle that's gone. Causes, in order of likelihood: (a) raytrace range < marking range, (b) obstacle was seen by a sensor (e.g. depth cam) that can't see that spot anymore so it never clears — add a clearing-capable sensor or use temporal decay, (c) voxel layer column partially cleared. Mitigation: recovery behavior that clears costmaps; Nav2 `clear_entirely_*` services.

## 2. Graph Search: Dijkstra, A*, D* Lite

### 2.1 Dijkstra

Expands uniformly by cost-from-start g(n). Use when:
- You need cost-to-goal from **everywhere** (e.g. compute once from the goal, then any robot/any start can read off its path — this is how `navfn`'s potential field works, and how multi-robot systems amortize planning).
- No admissible heuristic exists (rare on metric grids).

Complexity O(E log V) with a binary heap. On a 4M-cell grid: ~1–2 s in naive Python, ~30–80 ms in decent C++.

### 2.2 A*

Dijkstra + heuristic. Expands by f(n) = g(n) + h(n).

**Admissibility:** h(n) ≤ true cost to goal, always. Guarantees optimal paths. **Consistency:** h(n) ≤ c(n, n') + h(n') — guarantees you never re-expand a closed node (lets you use a simple closed set).

Correct heuristics per connectivity (grid resolution res, unit cell cost):

| Connectivity | Admissible heuristic |
|---|---|
| 4-connected | Manhattan: `res * (|dx| + |dy|)` |
| 8-connected | **Octile**: `res * (max(|dx|,|dy|) + (√2−1) * min(|dx|,|dy|))` |
| Any-angle (Theta*, Hybrid-A*) | Euclidean: `res * hypot(dx, dy)` |

**The classic bug:** Euclidean heuristic on an 8-connected grid is admissible but *weak* (expands ~2–4x more nodes than octile). Manhattan on an 8-connected grid is **inadmissible** (overestimates diagonals by ~41%) → paths up to 41% longer than optimal, and they look fine in demos so it ships. Use octile.

**Cost function with costmap:** don't just use distance. Standard Nav2-style traversal cost:
```
c(n, n') = dist(n, n') * (1 + cost_factor * costmap(n') / 252)
```
`cost_factor` ≈ 3–10. Higher → paths swing wider around obstacles. Heuristic stays pure-distance (admissible because actual cost ≥ distance).

**Weighted A* (greedy knob):** f = g + w·h with w > 1. Inadmissible but bounded: path ≤ w × optimal. w = 1.5–2.0 cuts expansions 5–20x. Use when the planning budget is tight and 1.5x-optimal paths are acceptable (they usually are — smoothing erases most of the difference).

Reference implementation (the details that matter):

```python
import heapq, math

SQRT2 = math.sqrt(2.0)
LETHAL = 253  # treat inscribed-inflated as lethal too

def octile(dx, dy):
    dx, dy = abs(dx), abs(dy)
    return max(dx, dy) + (SQRT2 - 1.0) * min(dx, dy)

def astar(costmap, start, goal, res=0.05, cost_factor=3.0, w=1.0):
    """costmap: 2D uint8 array. start/goal: (row, col) cells.
    Returns list of cells or None. O((rows*cols) log) worst case."""
    rows, cols = costmap.shape
    if costmap[goal] >= LETHAL:
        return None  # fail fast — don't search 4M cells to discover this
    g = {start: 0.0}
    parent = {start: None}
    openq = [(w * octile(goal[0]-start[0], goal[1]-start[1]), 0.0, start)]
    closed = set()
    NBRS = [(-1,0,1.0),(1,0,1.0),(0,-1,1.0),(0,1,1.0),
            (-1,-1,SQRT2),(-1,1,SQRT2),(1,-1,SQRT2),(1,1,SQRT2)]
    while openq:
        f, gc, n = heapq.heappop(openq)
        if n in closed:            # lazy deletion — cheaper than decrease-key
            continue
        if n == goal:
            path = []
            while n is not None:
                path.append(n); n = parent[n]
            return path[::-1]
        closed.add(n)
        for dr, dc, step in NBRS:
            r, c = n[0]+dr, n[1]+dc
            if not (0 <= r < rows and 0 <= c < cols):
                continue
            cell = costmap[r, c]
            if cell >= LETHAL:
                continue
            # forbid diagonal corner-cutting: both orthogonal cells must be free
            if dr and dc and (costmap[n[0]+dr, n[1]] >= LETHAL
                              or costmap[n[0], n[1]+dc] >= LETHAL):
                continue
            ng = gc + step * (1.0 + cost_factor * cell / 252.0)
            if (r, c) not in g or ng < g[(r, c)] - 1e-9:
                g[(r, c)] = ng
                parent[(r, c)] = n
                h = octile(goal[0]-r, goal[1]-c)
                heapq.heappush(openq, (ng + w * h, ng, (r, c)))
    return None
```

Non-negotiable details encoded above:
1. **Corner-cutting check** — without it, a point-robot path slips diagonally between two lethal cells; a real robot hits the corner.
2. **Lazy deletion** instead of decrease-key — Python's heapq has no decrease-key; pushing duplicates and skipping closed nodes is standard and fast.
3. **Goal-lethal fail-fast** — otherwise an unreachable goal costs a full-grid expansion (your worst-case latency).
4. **Tie-breaking**: pushing `(f, g, node)` breaks f-ties toward higher g (deeper nodes), reducing expansions in corridors. Some prefer `(f, -g)`; either beats no tie-break.

For production: write it in C++ (Nav2's `SmacPlanner2D` / `NavFn` exist — prefer them over rolling your own), or use `std::priority_queue` with the same lazy-deletion trick. Expect 5–50 ms on warehouse-scale maps.

### 2.3 D* Lite — incremental replanning

When the map changes (sensor reveals a blocked aisle), A* from scratch costs the full search again. D* Lite repairs only the affected part of the search tree.

How it works (operationally):
- Searches **backward** from goal to robot, so g-values = cost-to-goal. The robot moving doesn't invalidate the tree — only map *changes* do.
- Maintains two values per node: `g` (current cost-to-goal estimate) and `rhs` (one-step lookahead `min over successors of c + g`). Node is *consistent* when g == rhs. Map change → affected nodes become inconsistent → pushed on priority queue → repaired in order until the robot's node is consistent.
- `km` accumulator compensates for robot motion so heuristic keys stay comparable without reordering the whole queue.

When to use:
- Large maps + frequent small changes + tight replan budget (e.g. planning at the global level every costmap update). Speedup over re-running A*: typically 10–100x for local changes.

When NOT to use:
- Map changes are large/global (D* Lite degenerates to worse-than-A* due to repair overhead).
- Your A* replan already fits the budget (e.g. < 50 ms). **Most indoor robots just re-run A* at 1–2 Hz.** D* Lite's complexity (subtle priority-key bugs, the km term, under/over-consistent cases) is a real maintenance cost — Nav2 itself doesn't use it for this reason. Reach for D* Lite only when profiling proves full replans blow the budget.

Decision table:

| Situation | Choice |
|---|---|
| One-shot plan, known map | A* (octile, w=1) |
| Replan ≤ 2 Hz, map < ~10M cells, C++ | A* from scratch — simplest correct thing |
| Cost-to-goal field needed everywhere / multi-query to one goal | Dijkstra (or backward A* potential field) |
| Huge map, frequent local changes, hard latency bound | D* Lite |
| Tight budget, suboptimality OK | Weighted A* (w = 1.5–2) |
| Need smooth any-angle paths from the search itself | Theta* / SmacPlanner Hybrid-A* (kinematically feasible for car-like) |

## 3. Sampling-Based: RRT and RRT*

Grids die above ~3–4 DOF (cells scale as res^−d). For arms (6–7 DOF), mobile manipulators, and kinodynamic car-like planning, use sampling.

### 3.1 RRT

```
T ← {x_start}
repeat N times:
    x_rand ← sample C-space   (with probability p_goal=0.05–0.10, x_rand = x_goal)
    x_near ← nearest node in T (use a KD-tree; brute force is O(n) per iter → O(n²) total)
    x_new  ← steer(x_near, x_rand, step=η)
    if collision_free(x_near → x_new):       # edge check, not just endpoint!
        T.add(x_new, parent=x_near)
        if dist(x_new, x_goal) < goal_tol and collision_free(x_new → x_goal):
            return extract_path()
```

Parameter starting values:
- **Step size η**: 5–10% of the workspace diagonal; for arms, 0.1–0.3 rad in joint space. Too small → slow growth; too large → edges tunnel through thin obstacles unless your edge checker subdivides.
- **Goal bias**: 0.05–0.10. Higher (0.3+) makes RRT greedy and it stalls against concave obstacles ("bug trap").
- **Edge collision checking**: subdivide at ≤ half the thinnest obstacle dimension, or use a conservative bound (robot max link speed × resolution). Checking only endpoints is the #1 way RRT paths collide on real hardware.
- **Joint-space metric for arms**: weight joints by link inertia/length (proximal joints move more mass): `d(q1,q2) = sqrt(Σ wᵢ (q1ᵢ−q2ᵢ)²)`, w ≈ [3,3,2,1,1,0.5,0.5] for a 7-DOF arm. Unweighted Euclidean makes "nearest" meaningless.

RRT is **probabilistically complete** but the path is jagged and arbitrarily suboptimal. Always post-process (shortcut + smooth, §4).

### 3.2 RRT*

RRT + asymptotic optimality via two changes per iteration:
1. **Choose parent**: among neighbors within radius `r(n) = min(γ (log n / n)^(1/d), η)`, pick the one minimizing cost-to-come to x_new.
2. **Rewire**: for each neighbor, if routing through x_new is cheaper, re-parent it.

γ must satisfy `γ > (2(1 + 1/d))^(1/d) * (μ_free / ζ_d)^(1/d)` (μ_free = free-space volume, ζ_d = unit-ball volume). In practice: compute the theoretical bound from total C-space volume and multiply by 1.5–2.

Costs ~2–5x RRT runtime for the same n. Practical guidance:
- **Informed RRT*** (sample only the ellipsoid with foci start/goal and major axis = current best cost) is a near-free upgrade once a first solution exists — converges far faster.
- For one-shot mobile-robot global planning on a 2D/3D grid, **A* beats RRT*** — it's optimal, deterministic, and faster. RRT* earns its keep at ≥ 5 DOF or with differential constraints (use a steering function that respects them — Dubins/Reeds-Shepp for car-like).
- Industry tooling: **OMPL** (via MoveIt for arms) implements RRT, RRT*, RRTConnect, Informed-RRT*, BIT*. Default to **RRTConnect** for arm point-to-point (bidirectional, very fast, then shortcut the path); RRT*/BIT* when path cost matters.
- **Determinism warning**: sampling planners give a different path every run. For repeatable AMR routes, regulatory test repeatability, or anything an auditor watches, seed the RNG and record the seed — or use a deterministic planner.

## 4. Path Smoothing

Raw grid paths zigzag at 45°/90°; raw RRT paths are jagged. Controllers track smooth paths with less lateral error and less wheel scrub.

### 4.1 Shortcutting (do this first, always)

```python
def shortcut(path, collision_free, iters=100):
    import random
    path = list(path)
    for _ in range(iters):
        if len(path) < 3: break
        i, j = sorted(random.sample(range(len(path)), 2))
        if j - i < 2: continue
        if collision_free(path[i], path[j]):
            path = path[:i+1] + path[j:]
    return path
```
Cheap, removes most suboptimality. The collision check must be the *same conservative footprint check* used by the planner — shortcutting with a point check re-introduces wall clipping.

### 4.2 Gradient smoothing (elastic band style)

Minimize `Σ α‖xᵢ − x̂ᵢ‖² + β‖xᵢ₊₁ − 2xᵢ + xᵢ₋₁‖²` (data term + smoothness term) by gradient descent:

```python
def smooth(path, alpha=0.1, beta=0.3, tol=1e-4, max_iter=500):
    import numpy as np
    p = np.array(path, float); orig = p.copy()
    for _ in range(max_iter):
        grad = alpha * (p - orig)
        grad[1:-1] += beta * (2*p[1:-1] - p[:-2] - p[2:])
        p[1:-1] -= 0.5 * grad[1:-1]        # endpoints fixed
        if np.abs(grad[1:-1]).max() < tol: break
    return p
```
α/β trade fidelity vs smoothness; α=0.1, β=0.3 is a sane start. **Re-validate against the costmap after smoothing** — the smoother happily drags waypoints into inflated cells near inside corners. Either reject moves that increase cell cost above a threshold, or add an obstacle-gradient repulsion term.

### 4.3 Spline fitting

For controllers needing curvature continuity (Pure Pursuit tolerates C¹; MPC and high-speed tracking want C²):
- **Cubic B-spline / quintic spline** through the shortcut path. B-splines don't interpolate control points — they approximate — which is usually fine and inherently smooth; clamp endpoints.
- **Curvature constraint**: ensure max curvature κ_max ≤ tan(δ_max)/L for car-like (wheelbase L, max steer δ), or ≤ v_max-dependent bound for diff-drive comfort. Check κ along the spline (sample at 0.05 m); if violated, insert intermediate waypoints and refit, or fall back to Dubins segments.
- Nav2 ships `SmootherServer` with `ConstrainedSmoother` (costmap-aware, curvature-bounded) — use it before writing your own.

**Failure mode:** smoothed path crosses a doorway diagonally and the robot's circumscribed corner clips the frame. The smoother only checked centerline cells. Fix: validate with the inscribed-cost threshold (253) *plus* orientation-aware footprint check in the narrow band, or simply don't smooth within r_circ of lethal cells.

## 5. Planning Frequency Budgets

Hard numbers that keep robots safe and fluid:

| Loop | Rate | Latency budget | Notes |
|---|---|---|---|
| Global planner | 0.5–2 Hz (or on-demand) | < 200 ms hard, < 50 ms ideal | Blocking > 500 ms = robot visibly stutters at replan boundaries |
| Costmap update | 2–10 Hz (global), 10–20 Hz (local) | < 1 sensor period | Update faster than the local planner reads it |
| Local planner/controller | 10–50 Hz (20 Hz typical) | < 1/rate, hard | Missed ticks → cmd_vel gaps → jerky motion, watchdog stops |
| Safety/E-stop layer | 50–500 Hz | independent of planning | NEVER in the planning process. Lidar safety zones / hardware. |

Rules:
1. **Stopping distance bounds reaction latency.** Worst-case obstacle-to-brake-command latency = sensor period + costmap update + local planner period + control latency. At 1.5 m/s with 0.35 s total latency, the robot travels 0.53 m blind plus braking distance v²/(2a) = 0.56 m at a=2 m/s² → keep ≥ 1.2 m effective sensing margin or slow down. Run this arithmetic for *your* stack; it sets your max speed.
2. **Global planning must not block the control loop.** Separate thread/executor (Nav2: planner and controller servers are separate nodes/lifecycles). The controller keeps following the *old* path until the new one arrives; a planner timeout aborts to recovery, never freezes cmd_vel.
3. **Set an explicit planner timeout** (Nav2 `planner_server` expected frequency warning, or your own deadline ~2× typical solve time). On timeout: return best-effort (weighted A* partial / RRT best-so-far) or fail to recovery — silent overruns are how 1 Hz planners become 0.2 Hz under load and nobody notices until a demo.
4. **Replan triggers** (don't replan blindly every tick): (a) periodic timer, (b) path blocked — new lethal cells on the current path within lookahead, (c) controller progress stall, (d) new goal. Blind 10 Hz global replanning wastes CPU and causes path oscillation between near-equal-cost homotopy classes (robot dithers at a fork). Hysteresis: keep the current path unless the new one is ≥ 5–10% cheaper.

## 6. Debugging Methodology

Symptom-driven, in order of frequency in the field:

1. **"No path found" but a path obviously exists.**
   - Visualize the *costmap the planner actually sees* (RViz costmap topic, not the static map). 90% of cases: goal or start inside inflated/lethal cells (robot parked near a wall; goal clicked inside inflation).
   - Check the lethal threshold the planner uses vs costs present. Check unknown-space policy (`allow_unknown`) — a goal in unexplored space with allow_unknown=false fails correctly but confusingly.
   - Check frames: goal in `map`, planner expecting `map`, TF tree healthy (`ros2 run tf2_tools view_frames`). A 2 m map→odom drift puts the goal inside a wall.

2. **Paths hug walls / cut corners.**
   - inflation_radius too small or cost_scaling_factor too high (cost decays to ~0 just outside r_in, so distance-dominated search slices corners). Lower cost_scaling_factor to 3, raise cost_factor in the traversal cost.

3. **Robot oscillates between two routes.**
   - Equal-cost homotopy classes + frequent replan. Add path hysteresis (§5.4) or a small cost bonus for cells on the previous path.

4. **Planner slow / deadline misses.**
   - Profile expansions, not wall time first: log nodes-expanded per plan. Octile-vs-Euclidean fix or w=1.5 usually gives 5–20x. Then check costmap size — are you planning on the full 500 m map for a 10 m goal? Use a bounded region.
   - Python planner in production: rewrite in C++; the constant factor is 30–100x and it's not optional at scale.

5. **Collision despite "valid" path.**
   - Footprint vs radius mismatch (§1.2), corner-cutting in the search (§2.2), smoother dragging the path (§4.2), or the path is fine and the *local planner* deviated — check which component generated the colliding trajectory before blaming the global planner. Record cmd_vel + local costmap + footprint in a rosbag; replay.

6. **RRT works in sim, fails on robot.**
   - Edge collision resolution too coarse for real (noisier, fatter) obstacles; non-determinism producing occasionally terrible paths — log seeds, add path-cost acceptance threshold + retry.

Tools: RViz/Foxglove (costmap, plan, footprint overlays — always visualize all three together), `ros2 bag` for replay, Nav2 `costmap_filters` for keepout zones (don't hand-edit map PGMs), OMPL benchmark facilities for sampling-planner tuning, `planner_benchmarking` style harness: fixed start/goal set, assert path-found rate, mean cost, p99 latency in CI.

## 7. Reference Stack Choices

| Need | Use |
|---|---|
| Indoor AMR, diff-drive/omni | Nav2: `SmacPlanner2D` or `NavFn` (global) + `MPPI`/`DWB`/`RPP` (local) |
| Car-like / ackermann | Nav2 `SmacPlannerHybrid` (Hybrid-A*, Dubins/Reeds-Shepp motion primitives) |
| 6–7 DOF arm | MoveIt + OMPL: RRTConnect default, BIT*/Informed-RRT* for cost |
| Free-space drone | Grid/ESDF (voxblox/nvblox) + A*/JPS + minimum-snap trajectory opt |
| Lattice/structured warehouse | Pre-built roadmap (PRM/lanes) + Dijkstra; planning becomes graph lookup |

Default rule: **prefer the existing Nav2/OMPL planner with tuned parameters over a custom planner.** Custom planners are justified by a measured limitation (latency, kinematic feasibility, special cost semantics) — not by preference. When you do write one, implement it as a Nav2 planner plugin (`nav2_core::GlobalPlanner`) so costmaps, lifecycle, and recoveries come for free.
