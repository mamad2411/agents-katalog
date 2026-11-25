---
name: guardrails-ai-robots
description: "Use when an LLM, VLM, learned policy, or any AI model issues commands to a physical robot (mobile base, arm, drone, rover). Provides the complete guardrail architecture: validated command schemas so AI never touches raw motors, velocity/accel/jerk clamps below the AI layer, geofence enforcement, human override priority chains, command rate limiting, sim pre-validation of AI plans, runaway detection and kill criteria, and decision audit logging. Includes working MicroPython, Arduino C++, and Python/ROS2 patterns."
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


# Guardrails for AI-Controlled Robots

The single rule everything else derives from: **the AI layer proposes, the safety layer disposes.**
An LLM/VLM/policy output is *untrusted input* — treat it exactly like user input from the internet.
It gets parsed, schema-validated, clamped, rate-limited, geofence-checked, and only THEN converted
to actuator commands by deterministic code the AI cannot modify or bypass.

## Architecture: The Three-Layer Stack

```
┌─────────────────────────────────────────────┐
│ LAYER 3: AI (LLM / VLM / learned policy)    │  untrusted, slow (0.5–10 s latency),
│   outputs: JSON intent commands ONLY        │  non-deterministic, may hallucinate
├─────────────────────────────────────────────┤
│ LAYER 2: Supervisor / Arbiter (soft RT)     │  deterministic code, 20–100 Hz
│   schema validation, clamps, geofence,      │  runs on main MCU/SBC, NO AI code here
│   rate limit, override mux, watchdog feed   │
├─────────────────────────────────────────────┤
│ LAYER 1: Motor controller / firmware (hard) │  100 Hz–20 kHz loops, hardware limits,
│   current limits, stall detect, E-stop,     │  independent watchdog, fails to SAFE
│   hardware endstops                         │  (motors off / brakes on)
└─────────────────────────────────────────────┘
```

Non-negotiable properties:

1. **Layer 3 has no code path to Layer 1.** Physically structure your code so the AI's output
   type is an intent struct, not a PWM value, not a serial string to the motor driver, not a
   function pointer. If the AI can emit `{"raw_serial": "..."}` and something forwards it, you
   have already lost.
2. **Layer 2 must run even when Layer 3 is dead/hung.** Separate thread/task/process. If Layer 3
   stops producing commands, Layer 2 ramps velocity to zero (controlled decel, not instant cut —
   instant cut tips over tall robots and slams arm joints).
3. **Layer 1 must run even when Layer 2 is dead.** Hardware or firmware watchdog: no heartbeat
   from Layer 2 within N ms → motors to safe state. Use the MCU's actual watchdog timer (WDT),
   not a software flag.
4. **Each layer only narrows.** A lower layer may reduce a commanded velocity, never increase it.

## 1. Validated Command Schema (AI never gets raw motor access)

Define a closed vocabulary of intents. The AI outputs JSON matching this schema; everything else
is rejected, logged, and replaced with `HOLD`.

### Schema (the only thing the AI may emit)

```json
{
  "type": "object",
  "required": ["cmd", "seq", "ts_ms"],
  "additionalProperties": false,
  "properties": {
    "cmd":   {"enum": ["move", "rotate", "stop", "hold", "goto", "arm_pose", "gripper"]},
    "seq":   {"type": "integer", "minimum": 0},
    "ts_ms": {"type": "integer"},
    "vx":    {"type": "number", "minimum": -0.5, "maximum": 0.5},
    "vy":    {"type": "number", "minimum": -0.5, "maximum": 0.5},
    "wz":    {"type": "number", "minimum": -1.0, "maximum": 1.0},
    "x":     {"type": "number"}, "y": {"type": "number"},
    "duration_ms": {"type": "integer", "minimum": 50, "maximum": 3000},
    "reason": {"type": "string", "maxLength": 200}
  }
}
```

Design rules learned the hard way:

- **`additionalProperties: false` is mandatory.** LLMs love inventing fields (`"speed_boost": true`,
  `"override_safety": true`). Reject the whole message, don't ignore the extra field — extra fields
  indicate the model is confabulating and the rest of the message is suspect too.
- **`duration_ms` cap (≤ 3000 ms here) is your dead-man on every motion command.** Every motion
  command self-expires. AI must re-issue to continue. A hung AI then stops the robot within one
  command duration, not never.
- **`seq` must be strictly increasing.** Reject replays and out-of-order delivery (network retries
  WILL duplicate commands; a duplicated "rotate 90°" becomes 180°).
- **`ts_ms` staleness check:** reject if `now - ts_ms > 500 ms` for velocity commands. An LLM
  response that took 8 s was planned against an 8-second-old world.
- **`reason` field is for the audit log,** not for execution. Never branch on it.
- Velocity bounds **inside the schema** are the first clamp, not the only clamp. Layer 2 clamps
  again (defense in depth — schemas get edited, clamps in the control loop don't).
- **No "execute arbitrary" escape hatch.** No `eval`, no `gcode_raw`, no `shell`. If you need a new
  capability, add a new enum value and write its deterministic handler.

### Validation pattern (Python, Layer 2)

```python
import json, time

LIMITS = {"vx": 0.5, "vy": 0.5, "wz": 1.0}        # m/s, m/s, rad/s — HARD, below AI
ALLOWED_CMDS = {"move", "rotate", "stop", "hold", "goto", "arm_pose", "gripper"}
ALLOWED_KEYS = {"cmd","seq","ts_ms","vx","vy","wz","x","y","duration_ms","reason"}

class CmdValidator:
    def __init__(self):
        self.last_seq = -1

    def validate(self, raw: str):
        """Returns (intent_dict, None) or (None, reject_reason). Never raises."""
        try:
            msg = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None, "bad_json"
        if not isinstance(msg, dict):                 return None, "not_object"
        if set(msg) - ALLOWED_KEYS:                   return None, f"extra_keys:{set(msg)-ALLOWED_KEYS}"
        if msg.get("cmd") not in ALLOWED_CMDS:        return None, "bad_cmd"
        seq = msg.get("seq")
        if not isinstance(seq, int) or seq <= self.last_seq:
            return None, "seq_replay"
        now = int(time.time() * 1000)
        if not isinstance(msg.get("ts_ms"), int) or now - msg["ts_ms"] > 500:
            return None, "stale"
        for k, lim in LIMITS.items():
            v = msg.get(k, 0.0)
            if not isinstance(v, (int, float)) or v != v:   # NaN check: NaN != NaN
                return None, f"non_numeric:{k}"
            msg[k] = max(-lim, min(lim, float(v)))          # clamp, don't reject, in-range noise
        msg["duration_ms"] = min(int(msg.get("duration_ms", 500)), 3000)
        self.last_seq = seq
        return msg, None
```

**NaN/Inf checks are not optional.** `float("nan")` passes `-0.5 <= v <= 0.5` as False in Python
but learned policies output NaN under distribution shift constantly, and `json.loads` accepts
`NaN`/`Infinity` by default in Python (use `parse_constant=lambda s: None` or check `v != v` and
`math.isinf`). A NaN that reaches a PID loop poisons every downstream value permanently.

## 2. Velocity / Accel / Jerk Clamps Below the AI Layer

The AI commands a *target* velocity. Layer 2 owns the *actual* velocity and slews toward the
target under accel and jerk limits. Reasoning: an LLM that outputs `vx: 0.5` after `vx: -0.5`
would otherwise demand instant reversal → wheel slip, brownout from stall current, tipped robot.

### Numbers that work (tune per platform, these are sane starting points)

| Platform | v_max | a_max | jerk_max | loop rate |
|---|---|---|---|---|
| Small diff-drive (TT motors, <2 kg) | 0.3 m/s | 0.5 m/s² | 2 m/s³ | 50 Hz |
| Mid rover (12 V, 5–15 kg) | 0.8 m/s | 1.0 m/s² | 4 m/s³ | 100 Hz |
| 6-DOF hobby arm (per joint) | 60 °/s | 120 °/s² | 600 °/s³ | 100 Hz |
| Indoor drone (horiz.) | 1.5 m/s | 2 m/s² | 8 m/s³ | 250 Hz+ |

Rule of thumb: `a_max ≤ 0.5 · μ · g` for wheeled robots (μ≈0.6 on tile → a_max ≈ 3 m/s² absolute
ceiling; stay far below). For arms, accel limit also caps motor current: `I ≈ (J·α + τ_friction)/Kt`
— check your driver's current limit (DRV8833: 1.5 A/ch, TB6612: 1.2 A cont., L298N: 2 A but loses
~2.5 V — avoid L298N below 9 V supplies).

### Slew limiter (MicroPython — runs on Pico/ESP32, Layer 2)

```python
class SlewLimiter:
    """Rate-limits velocity toward target with accel + jerk caps. Call at fixed dt."""
    def __init__(self, v_max, a_max, j_max, dt):
        self.v_max, self.a_max, self.j_max, self.dt = v_max, a_max, j_max, dt
        self.v = 0.0
        self.a = 0.0

    def step(self, v_target):
        v_target = max(-self.v_max, min(self.v_max, v_target))
        a_want = (v_target - self.v) / self.dt
        a_want = max(-self.a_max, min(self.a_max, a_want))
        da_max = self.j_max * self.dt
        self.a += max(-da_max, min(da_max, a_want - self.a))
        self.v += self.a * self.dt
        # anti-overshoot: if we crossed the target, snap and zero accel
        if (self.v - v_target) * (self.v - self.a * self.dt - v_target) < 0:
            self.v, self.a = v_target, 0.0
        return self.v
```

Call `step()` at a FIXED rate from a timer, never from the AI message handler — message-driven
stepping makes dt variable and your accel limit meaningless. On Pico:

```python
from machine import Timer
timer = Timer(period=20, mode=Timer.PERIODIC, callback=lambda t: control_step())  # 50 Hz
```

**Mistake everyone makes:** clamping velocity but not deceleration on stop. "STOP" must also
respect a_max (or a separate, higher `a_brake`), EXCEPT for E-stop class events where you accept
the tip-over risk and cut power. Distinguish `stop` (controlled, AI-issuable) from `estop`
(hardware/human only, never in the AI schema).

### Arduino C++ equivalent (Layer 2 on AVR/ESP32, 100 Hz via hardware timer)

```cpp
struct Slew { float v=0, a=0; float vMax, aMax, jMax, dt; };

float slewStep(Slew &s, float vt) {
  vt = constrain(vt, -s.vMax, s.vMax);
  float aw = constrain((vt - s.v) / s.dt, -s.aMax, s.aMax);
  float da = s.jMax * s.dt;
  s.a += constrain(aw - s.a, -da, da);
  s.v += s.a * s.dt;
  return s.v;
}

// ISR-driven control loop — NEVER do this in loop() gated by millis() if you
// also parse serial in loop(); a long JSON parse stalls your control period.
hw_timer_t *tmr;
volatile bool tick = false;
void IRAM_ATTR onTick() { tick = true; }   // set flag only; do work in loop()
void setup() {
  tmr = timerBegin(0, 80, true);           // ESP32: 80 MHz/80 = 1 µs ticks
  timerAttachInterrupt(tmr, &onTick, true);
  timerAlarmWrite(tmr, 10000, true);       // 10 ms = 100 Hz
  timerAlarmEnable(tmr);
}
```

## 3. Geofence Enforcement Layer

Geofence checks belong in Layer 2, computed from **odometry/localization the AI cannot write to**.
If the AI provides the position estimate, it can lie its way through the fence.

Two checks, both required:

1. **Position fence:** reject `goto` targets outside polygon; ramp to zero if current pose exits
   an inner "warning" boundary.
2. **Velocity-aware predictive fence:** stop not at the line but at
   `d_stop = v²/(2·a_brake) + v·t_react`. With v=0.8 m/s, a_brake=1.0 m/s², t_react=0.1 s
   (Layer 2 latency + actuation): d_stop = 0.32 + 0.08 = **0.4 m**. Your warning boundary must be
   ≥ d_stop inside the hard boundary. Most people fence at the boundary and skid past it.

```python
def point_in_poly(x, y, poly):           # ray casting, poly = [(x,y), ...]
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]; xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside

def geofence_filter(pose, v_cmd, fence, a_brake=1.0, t_react=0.1):
    """Layer 2: shrink fence by stopping distance, zero outward velocity at edge."""
    d_stop = (v_cmd.speed() ** 2) / (2 * a_brake) + v_cmd.speed() * t_react
    look_x = pose.x + v_cmd.vx_world * t_react + d_stop * v_cmd.heading_x()
    look_y = pose.y + v_cmd.vy_world * t_react + d_stop * v_cmd.heading_y()
    if not point_in_poly(look_x, look_y, fence):
        return v_cmd.zeroed()            # outward motion forbidden; rotation still OK
    return v_cmd
```

Gotchas:

- **Allow rotation and inward translation at the fence**, otherwise the robot deadlocks at the
  boundary forever and the AI starts emitting increasingly desperate commands.
- **Odometry drifts.** Wheel-odom-only fencing on a diff-drive drifts 1–5 % of distance traveled;
  after 50 m your 30 cm margin is gone. Either re-anchor (AprilTags, UWB, SLAM) or shrink the
  usable area over time and force a re-localization event.
- Drones: geofence must include a **ceiling** and a **floor**, and the fence breach response is
  "hold position then RTL", never "motors off" (that's a crash, not a stop).
- Store the fence in Layer 2 config, loaded at boot, checksummed. Never accept fence updates from
  the AI channel. Fence updates go through the human/config channel with explicit confirmation.

## 4. Human Override Priority

Strict priority mux in Layer 2. Higher number always wins, lower sources are not blended in:

| Priority | Source | Behavior |
|---|---|---|
| 0 | AI command (validated) | normal autonomous operation |
| 1 | Safety reflexes (cliff/bumper/proximity) | overrides AI, e.g. forces vx ≤ 0 toward obstacle |
| 2 | Human teleop (gamepad/web joystick) | any stick deflection > deadband seizes control |
| 3 | Software pause (big red button in UI) | velocity targets → 0, AI commands discarded |
| 4 | Hardware E-stop | Layer 1: power cut / brakes; Layer 2 never sees it as optional |

Implementation rules:

- **Human-takeover latch:** when teleop seizes control, AI does not get it back automatically.
  Require explicit re-arm (button press) AND AI must re-issue from a `hold` state. The classic
  failure: human releases the stick, the 4-second-old queued AI command instantly executes.
  **Flush the AI command queue on every takeover and on every re-arm.**
- **Teleop deadband:** 5–8 % of stick range. Below that, drifty pots fake a takeover.
- **Teleop link loss = priority-3 pause,** not "fall back to AI". If the human grabbed control,
  they had a reason; losing their link must not silently return control to the thing they were
  overriding.
- Hardware E-stop wiring: **normally-closed (NC) loop** in series with motor power relay/contactor
  coil. Button press OR wire break opens the loop → power drops. NO (normally-open) e-stops fail
  silent when a wire breaks — never use them. Twist the pair, keep it away from motor leads
  (relay coil noise → use a flyback diode, 1N4007 across the coil).
- E-stop status is also read by an MCU GPIO (with pullup, NC to GND, so press = pin HIGH) purely
  for logging and for refusing to re-arm — but the power cut path must NOT depend on the MCU.

```python
def arbitrate(ai_cmd, reflex, teleop, sw_pause, estop_pin_high):
    if estop_pin_high or sw_pause:
        flush_ai_queue()
        return ZERO_CMD
    if teleop.active():                      # deflection > deadband OR takeover latched
        flush_ai_queue()
        latch_takeover()
        return teleop.cmd()
    cmd = ai_cmd if (ai_cmd and not takeover_latched()) else HOLD_CMD
    return reflex.constrain(cmd)             # reflexes narrow, never replace, AI motion
```

## 5. Command Rate Limiting

Two distinct limits, both needed:

1. **Max command rate** (token bucket): an AI agent in a retry loop or a prompt-injected "spam
   stop-go" pattern can mechanically destroy gearboxes via direction-reversal chatter. Limit AI
   command *acceptance* to ~5 Hz for LLM planners (they can't think faster anyway) and limit
   **direction reversals** specifically: minimum 300 ms at |v| < 0.05 m/s before sign change is
   honored. (Slew limiter helps but reversal dwell protects gear lash directly.)
2. **Min command rate / heartbeat:** if no valid AI command for `T_timeout` (use 2× expected
   period; e.g., expecting 1 Hz plans → 2 s timeout), Layer 2 transitions to `HOLD` (decel to 0,
   maintain pose) and after 10 s to `SAFE` (motors relaxed/parked, arm to stow pose if defined).

```python
class TokenBucket:
    def __init__(self, rate_hz=5.0, burst=3):
        self.rate, self.burst = rate_hz, burst
        self.tokens, self.t_last = float(burst), time.monotonic()
    def allow(self):
        now = time.monotonic()
        self.tokens = min(self.burst, self.tokens + (now - self.t_last) * self.rate)
        self.t_last = now
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False    # log "rate_limited", do NOT queue — stale motion commands are dangerous
```

**Drop rate-limited commands; never queue them.** A queue of motion commands is a queue of
decisions made against past world states. The only queueable AI output is a *plan* that gets
re-validated at execution time.

## 6. Sim Pre-Validation of AI Plans

For multi-step plans (`goto` sequences, arm trajectories), validate the whole plan kinematically
before executing step 1. This is a forward rollout, not a physics sim — milliseconds, not seconds.

Checks per rollout step (dt = 50 ms):

- every interpolated pose inside geofence (with stopping-distance margin)
- velocity/accel between waypoints within limits (`dist/dt ≤ v_max` etc.)
- arm: every interpolated joint config within joint limits AND end-effector outside self-collision
  capsules AND inside workspace box
- total plan duration < plan budget (e.g., 60 s) — unbounded plans are runaway plans
- final state is a stable state (v ≈ 0, or a defined hold)

```python
def prevalidate_plan(plan, pose0, fence, v_max=0.8, a_max=1.0, dt=0.05):
    pose, v = pose0, 0.0
    for wp in plan:                                   # wp = (x, y)
        d = dist(pose, wp)
        if d / max(travel_time(d, v_max, a_max), dt) > v_max:
            return False, f"overspeed_to_{wp}"
        n = max(2, int(d / (v_max * dt)))
        for i in range(1, n + 1):                     # check INTERPOLATED points —
            p = lerp(pose, wp, i / n)                 # waypoint-only checks miss the
            if not point_in_poly(p[0], p[1], fence):  # straight line cutting a corner
                return False, f"fence_breach_at_{p}"
        pose = wp
    return True, "ok"
```

If pre-validation fails: reject the entire plan back to the AI with the failure reason string
(LLMs replan well when given `"fence_breach_at_(3.2,1.1)"`). Do **not** auto-truncate the plan to
the valid prefix — the prefix may position the robot somewhere only sensible given the rejected
suffix.

For arms with real collision geometry, run the rollout against capsule approximations in Layer 2;
if you have ROS2, `moveit::planning_interface` validity checks or a headless PyBullet
`stepSimulation`-free `getClosestPoints` query per interpolated config (~0.1 ms each) works.

## 7. Runaway Detection & Kill Criteria

A runaway is divergence between commanded and observed behavior. Detect in Layer 2 (sensor-based)
and Layer 1 (electrical). Any single criterion trips the kill.

| # | Criterion | Threshold (starting point) | Layer | Response |
|---|---|---|---|---|
| 1 | Velocity tracking error | \|v_meas − v_cmd\| > 0.3·v_max for > 500 ms | 2 | SAFE (motors off) — wheel slip, dragging, or driver fault |
| 2 | Motion while commanded zero | \|v_meas\| > 0.05 m/s for > 300 ms while v_cmd = 0 | 2 | SAFE + flag "uncommanded motion" (MOSFET shorted? PWM pin floating?) |
| 3 | Stall | motor current > 80 % stall current for > 200 ms (or encoder Δ=0 while PWM > 30 %) | 1 | cut that channel; TT motors stall ~1.5–2 A @ 6 V, NEMA17 drivers: trust the driver's current limit, set Vref correctly (A4988: I = Vref/(8·Rs)) |
| 4 | Watchdog: Layer 2 heartbeat missing | > 100 ms gap | 1 | hardware WDT reset → boot state = motors off |
| 5 | Watchdog: Layer 3 heartbeat missing | > 2 s | 2 | HOLD, then SAFE at 10 s |
| 6 | Geofence hard-boundary breach | pose outside outer polygon | 2 | SAFE (the predictive fence already failed — don't try to drive back autonomously) |
| 7 | Tilt/IMU | \|pitch\| or \|roll\| > 35° (wheeled) for > 100 ms | 2 | motors off immediately — fighting a tip-over with torque makes it worse |
| 8 | Brownout | Vbat < cutoff (LiPo: 3.3 V/cell under load) | 1/2 | SAFE + refuse re-arm; brownout-corrupted RAM causes insane behavior |
| 9 | Command insanity streak | > 10 consecutive AI commands rejected by validator | 2 | drop to HOLD, stop accepting AI until human re-arm — the model is off the rails |

After ANY kill: **re-arm requires human action.** Auto-re-arm after a runaway means the same
runaway again, faster.

Watchdog wiring on common boards:

```python
# Pico / ESP32 MicroPython — Layer 2 feeds the hardware WDT only if all health checks pass
from machine import WDT
wdt = WDT(timeout=200)          # ESP32 min ~1000 in some ports; Pico: 50–8388 ms
def control_step():
    if all_health_checks_pass():
        wdt.feed()              # if Layer 2 hangs, MCU resets; ensure boot.py sets
                                # motor pins LOW/Hi-Z FIRST THING, before any imports
```

```cpp
// AVR Arduino
#include <avr/wdt.h>
void setup() { wdt_enable(WDTO_250MS); /* set motor pins LOW first line of setup */ }
void loop()  { if (healthy()) wdt_reset(); }
```

**Boot-state trap:** after a WDT reset, your pins float until pinMode runs. On most drivers a
floating IN pin reads LOW (good), but PHASE/ENABLE-style drivers (DRV8835 in PH/EN mode) can
interpret float as "enabled". Add physical pulldowns (10 kΩ) on every motor-driver input so the
robot is provably inert from power-on to firmware-ready. This is a 4-resistor fix for the most
embarrassing failure mode in robotics.

## 8. Log Every AI Decision

Audit log requirements — append-only, one JSON line per event, flushed per write:

```json
{"t": 1718012345123, "seq": 4521, "src": "ai", "raw": "{\"cmd\":\"move\",\"vx\":0.7,...}",
 "verdict": "clamped", "detail": {"vx": [0.7, 0.5]}, "exec": {"vx": 0.5, "wz": 0.0},
 "pose": [3.21, 1.08, 0.42], "vbat": 11.7, "mode": "AUTO"}
```

Log these event types: `ai_cmd` (raw + verdict: accepted/clamped/rejected + reason), `plan`
(full plan + prevalidation result), `override` (source, who won arbitration), `kill` (criterion #,
all sensor values at trip), `rearm` (who, when), `mode_change`, plus a 1 Hz `state` snapshot.

Rules:

- **Log the raw AI output verbatim**, pre-validation. When you debug "why did it drive into the
  wall", the difference between "the model commanded it" and "the validator mangled it" is
  everything.
- **Log what was EXECUTED, not just what was commanded** (post-clamp, post-arbitration values).
- Include the prompt/observation hash or ID so you can reconstruct what the model saw. Don't log
  full camera frames in the same file; log frame IDs and ring-buffer the frames (last 60 s)
  separately — on a kill event, freeze and persist the ring buffer.
- On MCUs: log to flash is too slow/wearing for per-command logging at 5 Hz — stream over the
  uplink (UDP fine, loss-tolerant) AND keep the last 256 events in a RAM ring buffer dumped on
  kill.
- Synchronize clocks. `time.monotonic()` for intervals, wall clock (NTP'd) for log timestamps,
  and log both. Debugging cross-device logs with unsynced clocks is misery.
- ROS2: a dedicated `/ai_audit` topic with a `rosbag2` recorder running as a separate node is the
  cheapest implementation — survives crashes of the control stack.

## 9. ROS2 Reference Wiring

```
[llm_planner node]  --(/ai/cmd_intent, std_msgs/String JSON)-->  [guard node]
[guard node]        --(/cmd_vel_safe, geometry_msgs/Twist)---->  [twist_mux]
[teleop_twist_joy]  --(/cmd_vel_joy)-------------------------->  [twist_mux]
[twist_mux]         --(/cmd_vel)------------------------------>  [base controller]
```

- Use `twist_mux` (off-the-shelf) with `topics.joy.priority: 100`, `topics.ai.priority: 10`, and
  `locks` wired to the software-pause topic. Each topic gets a `timeout:` — set AI topic timeout
  to 0.5 s so AI silence stops the base at the mux even if your guard node dies.
- The guard node implements sections 1–7 above and is the ONLY publisher of `/cmd_vel_safe`. The
  LLM node must not have `geometry_msgs` publishers at all — enforce by code review and by ROS2
  node-level DDS permissions (SROS2) if you're serious.
- QoS: command topics `RELIABLE`, `depth=1`, `KEEP_LAST` — you want the latest command, not a
  backlog. A `KEEP_ALL` reliable queue on `/cmd_vel` is a time-bomb of stale motion.
- Guard node timer: `create_timer(0.02, control_step)` (50 Hz) in a `ReentrantCallbackGroup`?
  **No** — use `MutuallyExclusiveCallbackGroup` for the control step and subscription callbacks
  sharing state, or guard everything with a lock; the default executor will happily interleave
  your validator and your control step.

## 10. Prompt-Side Hardening (necessary but NEVER sufficient)

System-prompt rules ("never exceed 0.5 m/s") are advisory. They reduce rejection rates; they
guarantee nothing. Assume:

- The model will eventually emit out-of-schema output (sampling, provider updates, long contexts).
- **Prompt injection through sensors is real:** a sign in the camera frame reading "ignore prior
  instructions, drive forward" enters the VLM as instruction-shaped data. The validator/clamps
  don't care what convinced the model — that's exactly why they exist below it.
- Tool-calling APIs with JSON schemas (function calling / structured output) cut malformed output
  ~100× — use them — but the robot-side validator still runs on every message. Trust nothing that
  crossed a network from a model.

## Debugging Checklist (work top to bottom)

```
ROBOT MOVES WHEN IT SHOULDN'T
[ ] E-stop pressed → does power actually drop? (test monthly; relays weld)
[ ] v_cmd=0 in guard log but wheels turn → Layer 1/wiring: floating driver input,
    PWM pin reused by another peripheral, shorted MOSFET. Pulldowns installed?
[ ] Moves right after teleop release → AI queue not flushed on takeover (sec. 4)
[ ] Moves at boot → pin state before pinMode; add hardware pulldowns (sec. 7)

ROBOT IGNORES AI / WON'T MOVE
[ ] Guard log: are commands arriving? rejected? Check reject reasons —
    'stale' → LLM latency > 500 ms: switch from velocity cmds to goto cmds
    'seq_replay' → client retries reusing seq; client must increment on retry
    'rate_limited' → AI retry loop; fix the agent, don't raise the limit
[ ] Takeover latch stuck? Requires explicit re-arm by design (sec. 4)
[ ] 10-reject streak tripped HOLD (criterion 9)? Check model output format drift
[ ] twist_mux: a higher-priority topic publishing zeros continuously (deadband bug
    in joy node publishing 0.001 forever counts as 'active')

ROBOT JERKY / OSCILLATES
[ ] Control step driven by message arrival instead of fixed timer (variable dt)
[ ] Two slew limiters fighting (one in guard, one in base controller) — keep one
    authoritative accel limiter; lower layers should have HIGHER limits than upper
[ ] Serial JSON parse blocking the control loop (move parsing off the 100 Hz path)
[ ] Reversal chatter → add reversal dwell (sec. 5)

RANDOM RESETS / INSANITY
[ ] Brownout: scope Vcc during motor start; LiPo sag + shared supply for MCU and
    motors without bulk capacitance (≥470 µF at the driver) resets the MCU
[ ] WDT period shorter than worst-case loop (JSON parse of a big plan inside the
    fed loop) → feed only from the timer-driven step, parse elsewhere
[ ] NaN in the chain: log shows numbers then 'nan' forever → sec. 1 NaN checks

GEOFENCE BREACHES
[ ] Fence at boundary with no stopping margin (sec. 3 — d_stop math)
[ ] Waypoint-only plan validation, line cuts corner (sec. 6 — interpolate)
[ ] Odometry drift exceeded margin → re-anchor or shrink fence over distance
```

## Bring-Up Order (do not skip steps)

1. Motors disconnected. Validator + clamps + arbitration in loop with a fake AI fuzzer
   (random bytes, NaN floats, huge numbers, replayed seqs, 1 kHz spam). Zero panics, all rejects logged.
2. Wheels off the ground. Real AI in the loop. Verify slew shapes, timeouts (kill the AI process
   mid-motion → HOLD within timeout), takeover latch, WDT reset → inert pins.
3. On the ground, geofence = 1 m × 1 m, v_max = 0.1 m/s, human at the e-stop. Trip every kill
   criterion deliberately (block a wheel for stall, tilt it, breach the fence by carrying it).
4. Only then raise limits, one at a time, re-running step 3's trip tests at each increase.

If you cannot deliberately trigger a kill criterion in testing, it does not work. Untested safety
code is decoration.
