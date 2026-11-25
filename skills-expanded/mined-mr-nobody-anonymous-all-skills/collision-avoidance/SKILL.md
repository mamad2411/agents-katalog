---
name: collision-avoidance
description: "Use when implementing obstacle avoidance, protective stop zones, velocity scaling, contact detection, or safety layers on a mobile robot or manipulator. Provides layered collision-avoidance architecture: lidar stop/slow zones with exact timing budgets, proximity-based velocity scaling math, current-based contact detection thresholds, costmap vs reactive (VFH, potential fields) layer selection, blind-zone mitigation, constant-velocity obstacle prediction, and soft-target test protocols with working ROS2/Python, Arduino C++, and MicroPython code."
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


# Layered Collision Avoidance

## The Non-Negotiable Architecture

Collision avoidance is NEVER one algorithm. It is a stack of independent layers, each
with its own sensor, its own latency budget, and its own authority. A higher layer
failing must never disable a lower layer.

```
Layer 4  PLANNER        global costmap, A*/Dijkstra      100–1000 ms cycle   "go around"
Layer 3  LOCAL AVOID    VFH / DWA / potential fields     50–100 ms cycle     "steer away"
Layer 2  SLOW ZONE      velocity scaling by proximity    20–50 ms cycle      "slow down"
Layer 1  PROTECTIVE STOP lidar/sonar hard stop zone      ≤10 ms reaction     "STOP NOW"
Layer 0  CONTACT        motor current / bumper switch    ≤5 ms reaction      "already hit — kill torque"
```

Rules that must hold in code:
- Layer 1 and 0 run in their own loop/ISR/thread, NOT inside the planner callback.
- Each layer can only REDUCE the commanded speed coming from above, never increase it.
  Implement as `v_out = min(v_planner, v_scaled, v_stop)`.
- A watchdog: if any layer's sensor data is older than 2× its expected period → treat as
  obstacle-at-zero-distance (fail-safe, not fail-silent).
- E-stop and Layer 0 should cut motor power in hardware (relay/MOSFET on driver enable
  pin), not just set PWM to 0 in software.

## Stop-Distance Math (do this before writing any code)

Total stopping distance:

```
d_stop = v * (t_sense + t_compute + t_actuate) + v² / (2 * a_brake)
```

Typical real numbers for a small differential-drive robot:

| Term | Typical value | Notes |
|---|---|---|
| t_sense (RPLIDAR A1 @ 5.5 Hz) | up to 182 ms | full-rotation latency — the killer term |
| t_sense (RPLIDAR A1 @ 10 Hz) | up to 100 ms | run it at 10 Hz, always |
| t_sense (HC-SR04 sonar) | ~30 ms per ping | 38 ms timeout if no echo |
| t_sense (VL53L1X ToF) | 33 ms (default timing budget) | can be 20 ms in short-range mode |
| t_compute | 1–20 ms | keep Layer 1 under 5 ms |
| t_actuate (motor driver + inertia) | 50–150 ms | measure it, don't guess |
| a_brake (rubber wheels, hard floor) | 1–3 m/s² | 0.5 m/s² on smooth tile, derate! |

Worked example: v = 0.5 m/s, total latency 250 ms, a_brake = 1.5 m/s²:
`d_stop = 0.5*0.25 + 0.25/(3.0) = 0.125 + 0.083 = 0.21 m`
→ Protective stop zone must be ≥ 0.21 m **plus** robot half-width margin **plus**
sensor noise margin (3σ of range noise, ~±30 mm for cheap lidar). Use 0.35 m.

**The mistake everyone makes:** setting the stop zone from the braking term only and
forgetting sensor latency. At 1 m/s a 5.5 Hz lidar can eat 18 cm before the robot even
*knows* there is an obstacle.

## Zone Definition (industrial pattern, scaled down)

Three concentric zones, evaluated every scan:

```
STOP zone   : d < d_stop_margin            → v_cmd = 0, latch until clear for 500 ms
SLOW zone   : d_stop < d < d_slow          → v_cmd scaled (see below)
FREE zone   : d > d_slow                   → full planner speed
```

Latch the stop: if you un-stop the instant the reading clears, sensor noise at the zone
boundary makes the robot stutter-charge at the obstacle. Require N consecutive clear
scans (e.g., 5 scans @ 10 Hz = 500 ms) before releasing.

Zones must be SPEED-DEPENDENT. Either compute `d_stop` from current v each cycle, or
use 2–3 discrete speed bands with pre-computed zones (industrial safety lidars like the
SICK S300 do exactly this with "field sets" switched by speed).

### Angular gating

Only ranges within the collision corridor matter:

```python
# half-width corridor check, robot width W, lateral clearance c
# point at (r, theta) in robot frame, robot moving +x
x = r * cos(theta); y = r * sin(theta)
in_corridor = (x > 0) and (abs(y) < W/2 + c)
```

When turning, sweep the corridor: check the area the robot will OCCUPY along the arc,
not just straight ahead. Cheap approximation: widen `c` proportionally to |ω|:
`c_eff = c + k * abs(omega)` with k ≈ 0.3 m·s/rad for small robots.

## Velocity Scaling (Layer 2)

Linear ramp between zones — simple, monotonic, no oscillation:

```python
def scale_speed(d_min, v_request, D_STOP=0.35, D_SLOW=1.0, V_MIN=0.05):
    if d_min <= D_STOP:
        return 0.0
    if d_min >= D_SLOW:
        return v_request
    frac = (d_min - D_STOP) / (D_SLOW - D_STOP)   # 0..1
    return max(V_MIN, v_request * frac)
```

Better: speed-limit so the robot can ALWAYS stop within current clearance
(this is the ISO/TS 15066 SSM idea applied to mobile robots):

```python
import math
def safe_speed_limit(d_clear, a_brake=1.5, t_latency=0.25):
    # solve v*t + v^2/(2a) = d_clear  for v
    disc = (a_brake*t_latency)**2 + 2*a_brake*d_clear
    return max(0.0, -a_brake*t_latency + math.sqrt(disc))
```

Apply `v_cmd = min(v_planner, safe_speed_limit(d_min))`. This single function replaces
hand-tuned zone tables and is provably conservative if a_brake and t_latency are honest.

**Mistake:** scaling angular velocity ω by the same factor. Don't. Killing ω near
obstacles removes the robot's ability to turn AWAY. Scale linear v only; clamp ω to a
modest max (e.g., 1.0 rad/s) independently.

## Layer 1: Protective Stop — ROS2 Implementation

Standalone node. Subscribes to `/scan` and the planner's `/cmd_vel_raw`, publishes
`/cmd_vel`. Nothing else in the system publishes `/cmd_vel` directly.

```python
#!/usr/bin/env python3
import math, rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ProtectiveStop(Node):
    def __init__(self):
        super().__init__('protective_stop')
        self.D_STOP, self.D_SLOW = 0.35, 1.00
        self.W_CORRIDOR = 0.45        # robot width 0.35 + 0.10 clearance
        self.CLEAR_SCANS = 5
        self.SCAN_TIMEOUT = 0.3       # s; 10 Hz lidar → 3 missed scans = fault
        self.d_min = 0.0              # fail-safe: no data = obstacle at 0
        self.clear_count = 0
        self.stopped = True
        self.last_scan_t = 0.0
        qos = QoSProfile(depth=1, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.create_subscription(LaserScan, 'scan', self.on_scan, qos)
        self.create_subscription(Twist, 'cmd_vel_raw', self.on_cmd, 10)
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.create_timer(0.05, self.watchdog)            # 20 Hz

    def on_scan(self, msg):
        self.last_scan_t = self.get_clock().now().nanoseconds * 1e-9
        d = float('inf')
        ang = msg.angle_min
        for r in msg.ranges:
            if msg.range_min < r < msg.range_max:         # reject 0.0 and inf garbage
                x = r * math.cos(ang); y = r * math.sin(ang)
                if x > 0.0 and abs(y) < self.W_CORRIDOR / 2:
                    d = min(d, r)
            ang += msg.angle_increment
        self.d_min = d
        if d <= self.D_STOP:
            self.stopped = True; self.clear_count = 0
        elif self.stopped:
            self.clear_count += 1
            if self.clear_count >= self.CLEAR_SCANS:
                self.stopped = False                       # latched release

    def watchdog(self):
        now = self.get_clock().now().nanoseconds * 1e-9
        if now - self.last_scan_t > self.SCAN_TIMEOUT:
            self.stopped = True                            # stale data = STOP
            self.d_min = 0.0

    def on_cmd(self, msg):
        out = Twist()
        if not self.stopped:
            frac = min(1.0, max(0.0,
                (self.d_min - self.D_STOP) / (self.D_SLOW - self.D_STOP)))
            out.linear.x  = max(0.0, msg.linear.x) * frac if msg.linear.x > 0 \
                            else msg.linear.x              # never block reversing away
            out.angular.z = msg.angular.z
        self.pub.publish(out)

def main():
    rclpy.init(); rclpy.spin(ProtectiveStop()); rclpy.shutdown()
```

Key details baked in: BEST_EFFORT QoS (sensor data — RELIABLE causes queue lag),
fail-safe init (`d_min = 0`, `stopped = True`), stale-scan watchdog, latched release,
reverse motion never blocked by a FRONT lidar (the #1 way robots get permanently wedged).

## Layer 1 on a Microcontroller (MicroPython, HC-SR04 + N20 motors)

```python
from machine import Pin, PWM, time_pulse_us, Timer
import time

TRIG = Pin(5, Pin.OUT); ECHO = Pin(18, Pin.IN)
# HC-SR04: 5V device. ECHO is 5V out — divider 1k/2k to 3.3V MCU pin or you cook it.
# TRIG accepts 3.3V high fine. Vcc=5V, GND common with MCU. Current draw 15 mA.

D_STOP_MM, D_SLOW_MM = 200, 600
speed_scale = 0.0          # written by sensor loop, read by drive code

def read_mm():
    TRIG.value(0); time.sleep_us(2)
    TRIG.value(1); time.sleep_us(10); TRIG.value(0)
    t = time_pulse_us(ECHO, 1, 30000)      # 30 ms timeout ≈ 5 m
    if t < 0:
        return None                        # timeout/no echo — treat as FAR? NO:
    return t * 343 // 2000                 # us → mm  (speed of sound 343 m/s)

def sensor_tick(_):
    global speed_scale
    d = read_mm()
    if d is None:
        # Ambiguity: timeout = nothing in range OR soft obstacle absorbed echo.
        # For a hobby robot moving <0.3 m/s treating timeout as clear is the
        # usual choice — but log it, and pair sonar with a bumper (Layer 0).
        speed_scale = 1.0
        return
    if d <= D_STOP_MM:
        speed_scale = 0.0
    elif d >= D_SLOW_MM:
        speed_scale = 1.0
    else:
        speed_scale = (d - D_STOP_MM) / (D_SLOW_MM - D_STOP_MM)

Timer(0).init(period=60, mode=Timer.PERIODIC, callback=sensor_tick)
# 60 ms ≥ HC-SR04 recommended ping interval; faster causes echo cross-talk.

# In the drive loop:  pwm_duty = int(base_duty * speed_scale)
```

HC-SR04 hard limits to respect: 15° effective cone, blind below ~20 mm, unreliable on
soft/angled surfaces (foam, cloth, surfaces >45° off-normal reflect echo away → looks
CLEAR). Sonar alone is not a safety sensor; it is a slow-zone sensor.

## Layer 0: Current-Based Contact Detection

A stalled DC motor draws stall current (often 5–10× free-run). A collision is a
partial stall. Sense it with a low-side shunt or hall sensor:

| Sensor | Range | Output | Notes |
|---|---|---|---|
| ACS712-05B | ±5 A | 185 mV/A, Vcc/2 @ 0 A | noisy ±80 mA; fine for >0.5 A motors |
| INA219 (I2C, addr 0x40) | ±3.2 A w/ 0.1 Ω | 12-bit, 1 ms conv | cleanest for hobby use |
| Shunt 0.1 Ω + ADC | per design | V=I·0.1 | add RC filter 1k/1 µF, fc≈160 Hz |

Algorithm — threshold on a FILTERED current with an INRUSH MASK:

```cpp
// Arduino C++, INA219, runs in 1 kHz-ish loop
#include <Adafruit_INA219.h>
Adafruit_INA219 ina;                 // SDA/SCL, 3.3 or 5 V, addr 0x40

float i_filt = 0;
const float ALPHA = 0.05f;           // ~20-sample EMA @1 kHz → ~20 ms lag
const float I_TRIP = 1.8f;           // A; set = 1.5 × max normal driving current
const uint16_t INRUSH_MS = 300;      // ignore startup spike
uint32_t t_motor_on = 0;
const int EN_PIN = 7;                // driver enable — hardware kill

void loop() {
  float i = ina.getCurrent_mA() / 1000.0f;
  i_filt += ALPHA * (i - i_filt);
  bool armed = (millis() - t_motor_on) > INRUSH_MS;
  if (armed && i_filt > I_TRIP) {
    digitalWrite(EN_PIN, LOW);       // kill torque in <1 ms
    // then: back off 5 cm at 30% speed, re-plan. Do NOT just retry forward.
  }
}
```

Calibration procedure (do this, don't guess):
1. Log i_filt while driving normally on the worst surface (carpet) — note max, call it I_drive.
2. Hold the robot against a wall at normal speed for 1 s — note plateau, I_stall_partial.
3. Set `I_TRIP = I_drive + 0.4 * (I_stall_partial - I_drive)`. Verify no false trips
   over 10 min of normal driving, and trip time < 200 ms on a held-wheel test.

**Mistakes everyone makes:** (a) no inrush mask → trips at every start;
(b) raw unfiltered ADC → PWM ripple aliasing causes random trips — sample synchronized
to PWM or filter below PWM frequency; (c) tripping but leaving PWM running ("speed 0"
through the planner takes 100+ ms — pull the enable pin); (d) putting the shunt on the
motor lead instead of the supply on a locked-antiphase driver, reading garbage.

For manipulators: same idea per joint; threshold on |τ_measured − τ_model| if you have
a dynamics model, else on dI/dt (collision = current step >0.5 A in <50 ms, far faster
than any commanded accel).

## Layer 3: Costmap vs Reactive — Which and When

| Property | Costmap + local planner (Nav2 DWB/MPPI) | Reactive (VFH, potential fields) |
|---|---|---|
| Needs localization | yes (TF map→base) | no — works in robot frame |
| Memory of obstacles | yes (marking/clearing) | none — current scan only |
| Local-minimum traps | planner replans around | gets stuck in U-shapes |
| Compute | moderate–high | trivial (<1 ms) |
| Failure mode | stale costmap ghosts | oscillation between obstacles |
| Use as | Layer 3–4 | Layer 3 on MCU-class robots, or escape behavior |

Use BOTH on bigger robots: costmap planner for routing, reactive check as a final gate.
On Nav2, the relevant knobs:

```yaml
local_costmap:
  inflation_layer:
    inflation_radius: 0.55          # ≥ robot radius + d_stop
    cost_scaling_factor: 3.0        # higher = costs drop faster from obstacle
  obstacle_layer:
    observation_sources: scan
    scan: {marking: true, clearing: true, obstacle_max_range: 2.5,
           raytrace_max_range: 3.0}
```

`raytrace_max_range` MUST exceed `obstacle_max_range` or cleared cells beyond marking
range leave permanent ghosts. Ghost obstacles after a person walks away = clearing
misconfigured or the lidar can't see through the cell (raise `inflation` patience, or
enable `voxel_layer` with `unknown_threshold` for 3D).

### Minimal VFH (vector field histogram) — fits on an MCU

```python
import math
def vfh_steer(ranges, angle_min, angle_inc, target_bearing,
              d_max=1.5, sector_deg=5, thresh=0.6):
    n = int(360 / sector_deg)
    hist = [0.0] * n
    a = angle_min
    for r in ranges:
        if 0.05 < r < d_max:
            s = int(math.degrees(a) % 360 / sector_deg)
            hist[s] += (d_max - r) / d_max          # closer = bigger magnitude
        a += angle_inc
    # candidate sectors: histogram below threshold
    best, best_cost = None, 1e9
    for s in range(n):
        if hist[s] < thresh:
            bearing = math.radians(s * sector_deg + sector_deg/2)
            diff = math.atan2(math.sin(bearing-target_bearing),
                              math.cos(bearing-target_bearing))
            if abs(diff) < best_cost:
                best, best_cost = bearing, abs(diff)
    return best          # None = no free sector → stop, rotate in place, retry
```

Add hysteresis on the chosen sector (stick with previous choice unless a sector ≥2
sectors better appears) or the robot oscillates in doorways.

Potential fields: only use with (a) capped repulsive force, (b) added damping term
proportional to −v, (c) random escape kick on local-minimum detection (‖F_total‖ < ε
while goal not reached). Otherwise it's a demo, not a robot.

## Blind Zones — Enumerate Then Mitigate

Every sensor suite has them. Write the list down for YOUR robot:

1. **Lidar plane gaps**: a 2D lidar at 20 cm height misses table edges, low kerbs,
   overhanging shelves, and feet-below/torso-above geometry. Mitigation: 1–2 downward
   ToF sensors (VL53L1X) for cliff + low obstacle, one upward/forward for overhangs.
2. **Lidar minimum range**: RPLIDAR A1 min range 0.15 m — anything closer is invisible
   AND often reported as 0 (which naive code treats as "invalid → ignore" → robot
   grinds into the box it's touching). Treat r < range_min as UNKNOWN-NEAR, not clear.
3. **Behind the robot**: front-only sensing + reverse motion = unprotected. Either
   never reverse faster than 0.1 m/s, or add rear sonar/bumper.
4. **Glass and matte black**: lidar returns nothing (glass) or weak/short (black felt).
   Sonar SEES glass — this is the classic lidar+sonar complementarity. Fuse with
   per-cell min(): obstacle if EITHER sensor says so.
5. **Dynamic blind time**: between scans, a person walking at 1.5 m/s moves 15 cm per
   10 Hz scan. That's what the prediction layer below is for.
6. **Self-occlusion**: cables, masts, grippers in the scan → permanent phantom stop.
   Filter a static angular mask: `if angle in SELF_MASK: skip`. Measure the mask
   empirically with the robot in open space.

## Constant-Velocity Obstacle Prediction

Cheapest useful dynamic-obstacle model. Cluster scan points, track cluster centroids
across frames, assume each keeps its velocity, and check time-to-collision (TTC):

```python
import math

def ttc_and_miss(p_rel, v_rel, robot_radius=0.25, obst_radius=0.25):
    """p_rel, v_rel: obstacle position/velocity RELATIVE to robot (robot frame).
       Returns (ttc seconds or None, miss distance m)."""
    R = robot_radius + obst_radius
    px, py = p_rel; vx, vy = v_rel
    v2 = vx*vx + vy*vy
    if v2 < 1e-6:
        d = math.hypot(px, py)
        return (None, d - R)
    t_cpa = -(px*vx + py*vy) / v2                 # time of closest approach
    if t_cpa < 0:
        return (None, math.hypot(px, py) - R)     # moving apart
    d_cpa = math.hypot(px + vx*t_cpa, py + vy*t_cpa)
    if d_cpa >= R:
        return (None, d_cpa - R)
    # solve |p + v t| = R for the earlier root
    disc = math.sqrt(R*R - d_cpa*d_cpa) / math.sqrt(v2)
    return (max(0.0, t_cpa - disc), 0.0)

# Policy:  ttc < 2.0 s → enter SLOW;  ttc < t_stop_capability → STOP.
```

Tracking pipeline minimum: euclidean clustering (gap > 0.2 m splits clusters),
nearest-neighbor association frame-to-frame (gate at 0.5 m), centroid velocity =
EMA of frame-to-frame displacement / dt (alpha ≈ 0.3; raw differencing of lidar
centroids is hopelessly noisy). Drop tracks unseen for 3 frames. Remember the
robot's own motion: `v_rel = v_obstacle_world − v_robot_world`; if you skip ego-motion
compensation, every wall "approaches" at robot speed and TTC fires constantly.

CV prediction is valid ~1–2 s ahead for walking humans. Don't extrapolate further;
inflate predicted position uncertainty linearly with horizon (σ ≈ 0.3 m/s · t) and
test the inflated circle.

## Wiring Quick Reference

| Device | V | Current | Interface | Gotchas |
|---|---|---|---|---|
| RPLIDAR A1/A2 | 5 V | 400–600 mA (motor spin-up 1 A) | UART 115200/256000 8N1 | Separate 5 V rail; USB hub brownout = scan dropouts. TX/RX are 3.3 V logic. |
| HC-SR04 | 5 V | 15 mA | TRIG in / ECHO out | ECHO is 5 V — divider to 3.3 V MCU |
| VL53L1X | 2.6–3.5 V | 18 mA avg | I2C 0x29, 400 kHz | All share 0x29 — XSHUT pins to re-address at boot, one at a time |
| INA219 | 3–5.5 V | 1 mA | I2C 0x40–0x4F (A0/A1) | Shunt in series with LOAD high side |
| ACS712 | 5 V | 10 mA | Analog, Vcc/2 center | 5 V analog out → divider for 3.3 V ADC |
| Bumper microswitch | any | — | GPIO + pullup | Use NC contact: wire break = trip = fail-safe |
| Motor driver EN (TB6612/DRV8833) | 3.3/5 V | — | GPIO | This is your hardware kill line — route from safety MCU/relay, pull-DOWN resistor so floating = disabled |

Power architecture rule: lidar + motors on the battery rail through separate
regulators; logic MCU on its own 3.3/5 V regulator. Shared rail = lidar resets during
motor stall = blind robot at the worst possible moment.

## Soft-Target Test Protocol

Never validate collision behavior on people, pets, or walls first. Sequence:

1. **Bench, wheels-up**: verify stop latching, watchdog (unplug lidar mid-run → must
   stop within SCAN_TIMEOUT), and that `/cmd_vel` is zero when stopped. Pass = scope
   or log shows v_cmd → 0 within budget.
2. **Static soft target**: cardboard box (lidar-friendly) at known distances. Approach
   at 0.25 / 0.5 / max speed. Measure actual stop gap with tape measure, 5 reps per
   speed. Pass = gap > 0 every rep AND gap variance < 5 cm.
3. **Hostile-surface targets**: matte-black foam board, clear acrylic sheet, a chair
   (thin legs). These find your sensor lies. Expect failures; that's the point —
   document which Layer caught it (often Layer 0).
4. **Dynamic target**: foam cylinder on a string or a second small robot crossing the
   path at 0.5–1.5 m/s, perpendicular and head-on. Pass = no contact at crossing
   speeds up to your CV-prediction design limit.
5. **Contact test**: drive into a suspended foam block at low speed with Layer 1
   DISABLED (flag, logged). Pass = current trip kills torque < 200 ms, retreat
   executes, contact force on a kitchen scale behind the foam < your limit
   (ISO/TS 15066 quasi-static hand limit is 140 N — stay far under for kid-adjacent
   robots; target < 30 N).
6. **Endurance**: 30 min random wander in a cluttered pen. Pass = zero contacts,
   zero false-stop lockups (stopped > 10 s with clear path).

Log everything per run: timestamped d_min, v_cmd, layer that triggered, currents.
A collision-avoidance system without logs cannot be debugged after the one failure
that matters.

## Debugging Checklist

Robot doesn't stop:
- [ ] Is the safety node actually in the cmd_vel chain? `ros2 topic info /cmd_vel` —
      exactly ONE publisher allowed.
- [ ] Print d_min live. Is the obstacle inside range_min (invisible)? In the self-mask?
- [ ] Are invalid ranges (0.0 / inf / NaN) being skipped as "clear"? They must not be.
- [ ] Latency: timestamp scan→cmd path. >100 ms means your stop zone math is void.
- [ ] QoS mismatch (RELIABLE sub on BEST_EFFORT lidar pub = silent no-data).

Robot stops constantly / falsely:
- [ ] Self-occlusion (mast, cable, gripper in scan) — plot a polar scan in open space.
- [ ] Sonar cross-talk (two HC-SR04 pinging together) — interleave pings ≥30 ms apart.
- [ ] Floor returns: lidar tilted down 1–2° sees floor at 2–3 m as a wall. Shim it
      level; verify with a flat-wall scan.
- [ ] Sun/IR interference on ToF sensors near windows.
- [ ] Stop zone larger than corridor/doorway the robot must pass — check corridor
      width vs W_CORRIDOR + 2·d_stop.

Robot stutters at zone boundary:
- [ ] Missing release latch / hysteresis (need D_release > D_stop by ≥ 3σ noise).

Current trip misbehaving:
- [ ] False trips at start = no inrush mask. At speed changes = filter too fast.
- [ ] Missed collisions = threshold from free-run not carpet-run; or filtered so slow
      the robot pushes for a second first. EMA lag and trip threshold trade off —
      verify trip time on a held-wheel test, not on math.

Gets stuck oscillating between obstacles:
- [ ] Reactive layer with no hysteresis or no memory — add sector stickiness, or a
      "committed maneuver" timer (hold chosen direction ≥ 1 s unless STOP fires).

Wedged in a corner forever:
- [ ] Recovery ladder missing. Implement: stop → rotate-scan ±90° → reverse 10 cm →
      rotate 180° → declare stuck and alert. Each rung only if the previous failed,
      each protected by the same Layer 0/1.
