---
name: functional-safety-standards
description: "Use when designing, coding, or reviewing any robot that operates near humans — cobots, mobile robots, personal care robots, automotive/AGV systems — and you need force/pressure limits, risk assessment methodology, SIL/PL/ASIL targets, or the safety-vs-functional requirements split. Provides ISO 10218-1/-2 and ISO/TS 15066 cobot body-region force/pressure limit tables, ISO 13482 personal care robot categories and hazards, ISO 26262 ASIL determination, IEC 61508 SIL and ISO 13849 PL mapping, risk = severity x exposure x avoidance scoring, safety-rated software patterns (dual-channel, watchdogs, safe-torque-off), and the design mistakes that fail certification audits."
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


# Functional Safety Standards for Robotics

Expert reference for building robots that pass safety assessment and do not hurt people.
Covers ISO 10218 / ISO/TS 15066 (industrial + collaborative robots), ISO 13482 (personal
care robots), ISO 26262 (automotive, ASIL), IEC 61508 (SIL), ISO 13849 (PL), and how to
write code and architecture that a notified body will actually accept.

---

## 0. The One Rule That Governs Everything

**Safety functions must be implemented in safety-rated hardware/channels, NEVER in your
application code.** Your Python/ROS2/MicroPython application is — by definition — not a
safety function. It is QM (quality managed) at best. The safety chain is:

```
E-stop button ──┐
Light curtain ──┤
Safety laser  ──┼──> Safety PLC / safety relay (PLe/SIL3 rated)
Force sensor  ──┤        │
Enabling sw.  ──┘        ├──> STO (Safe Torque Off) input on servo drive
                         └──> Hard contactor on motor power
Application code ────────────> *requests* motion; cannot *guarantee* stopping
```

If your design doc says "the ROS node monitors the lidar and stops the robot when a person
is near" as the **only** protection, it will fail assessment. The node can do that as a
*functional* (productivity) layer, but a certified safety-rated scanner output wired into
a safety controller must exist underneath it.

---

## 1. Standards Map — Which Standard Applies to What

| Robot type | Primary standard | Supporting | Safety metric |
|---|---|---|---|
| Industrial arm (fenced) | ISO 10218-1 (robot), 10218-2 (cell/integration) | ISO 13849-1, IEC 62061 | PL (a–e) or SIL (1–3) |
| Collaborative robot (cobot) | ISO 10218-1/-2 + **ISO/TS 15066** | ISO 13849-1 | PL d Cat 3 typical |
| Personal care robot (home assist, exoskeleton, person carrier) | **ISO 13482** | IEC 61508, ISO 13849 | PL / SIL per hazard |
| Mobile platform / AMR / AGV (industrial) | ISO 3691-4 (driverless trucks), ANSI/RIA R15.08 (AMRs, US) | ISO 13849 | PL d typical for personnel detection |
| Road vehicle / ADAS | **ISO 26262** | SOTIF (ISO 21448) | ASIL (A–D) |
| Medical robot | IEC 60601 series, IEC 62304 (software) | ISO 14971 (risk mgmt) | Software class A/B/C |
| Drones/UAS | SORA methodology (EASA), 14 CFR 107 | — | SAIL levels |
| Generic E/E/PE system | IEC 61508 (the parent of all of the above) | — | SIL 1–4 |

Hierarchy: IEC 61508 is the root. ISO 26262 = 61508 adapted for cars. ISO 13849 =
machinery-sector simplification. ISO 10218/13482 are C-standards (product-specific) that
point at 13849/61508 for the actual integrity requirements.

---

## 2. Risk Assessment: Severity × Exposure × Avoidance

You cannot pick a PL/SIL/ASIL out of the air. It comes from risk assessment. Do this
FIRST, document it, and the rest of the architecture falls out of it.

### 2.1 ISO 13849-1 Risk Graph (PLr determination)

Parameters:
- **S — Severity of injury**: S1 = slight (reversible, bruise, laceration needing first aid);
  S2 = serious (irreversible: amputation, fracture, death)
- **F — Frequency/duration of exposure**: F1 = seldom-to-less-often and/or short exposure
  (rule of thumb: ≤ once per hour, ≤ 1/20 of operating time); F2 = frequent to continuous
- **P — Possibility of avoidance**: P1 = possible under specific conditions (slow robot
  < 250 mm/s, good visibility, room to escape); P2 = scarcely possible (fast motion,
  surprise approach, confined space)

Risk graph result → required Performance Level (PLr):

```
S1 F1 P1 → PL a        S2 F1 P1 → PL c
S1 F1 P2 → PL b        S2 F1 P2 → PL d
S1 F2 P1 → PL b        S2 F2 P1 → PL d
S1 F2 P2 → PL c        S2 F2 P2 → PL e
```

Typical cobot results: emergency stop → PL d. Speed & separation monitoring → PL d.
Power & force limiting function (the force/torque monitoring in the joints) → PL d Cat 3.
Axis position limiting (soft axis limits used as safety) → PL d.

### 2.2 PL ↔ SIL ↔ PFHd mapping

| PL | PFHd (dangerous failures/hour) | ≈ SIL |
|---|---|---|
| a | 10⁻⁵ to <10⁻⁴ | — |
| b | 3×10⁻⁶ to <10⁻⁵ | 1 |
| c | 10⁻⁶ to <3×10⁻⁶ | 1 |
| d | 10⁻⁷ to <10⁻⁶ | 2 |
| e | 10⁻⁸ to <10⁻⁷ | 3 |

PL also requires an architecture **Category**:
- **Cat B/1**: single channel. Max PL c (Cat 1 with well-tried components).
- **Cat 2**: single channel + test/monitoring. Max PL d (rarely used; test rate ≥ 100× demand rate).
- **Cat 3**: dual channel, single fault does not lead to loss of safety function. PL d/e workhorse. **This is why safety I/O is always two wires/contacts.**
- **Cat 4**: dual channel + accumulated fault detection. PL e.

Practical consequence for wiring: an e-stop at PL d Cat 3 = **two NC contacts, two
channels into the safety relay, cross-fault monitoring (pulsed test outputs), and the
relay must detect discrepancy between channels (typ. window 100–500 ms).**

### 2.3 ISO 26262 ASIL determination (intuition)

Parameters: **S** (S0 none → S3 life-threatening/fatal), **E** (E0 incredible → E4 high
probability, >10% of operating time), **C** controllability (C0 controllable in general →
C3 difficult/uncontrollable).

ASIL = lookup(S, E, C). Anchors to memorize:
- S3 + E4 + C3 → **ASIL D** (e.g., unintended full braking at highway speed, unintended steering)
- S3 + E4 + C2 → ASIL C
- S3 + E2 + C3 → ASIL B
- Anything with S0, E0, or C0 → QM (no ASIL)
- Each single-step reduction in any parameter drops one ASIL level.

Examples: airbag inadvertent deploy = ASIL D. Loss of low-beam headlights at night =
ASIL B. Rear-view camera failure = ASIL A/QM. Instrument cluster wrong speed = ASIL B.

**ASIL decomposition**: ASIL D can be split into ASIL B(D) + ASIL B(D) over two
*independent* channels (independence must be proven — no shared power, clock, housing,
or common-cause failure). This is why automotive safety MCUs (TI TMS570, Infineon AURIX
TC3xx, NXP S32K3) have lockstep cores: two cores execute the same code 2 cycles apart and
a comparator traps divergence within nanoseconds.

### 2.4 HRN-style numeric scoring (useful for design reviews)

Risk Priority Number = Severity × Exposure × Avoidance, e.g. each scored 1–5:

| Score | Severity | Exposure | Avoidance |
|---|---|---|---|
| 1 | scratch/bruise | < 1×/month | trivially avoided |
| 2 | first aid injury | weekly | easily avoided |
| 3 | reportable injury (fracture) | daily | possible |
| 4 | permanent disability | hourly | difficult |
| 5 | fatality | continuous | impossible |

RPN ≥ 27 → redesign mandatory (eliminate hazard); 12–26 → engineered safeguard with
PL d+; 6–11 → safeguard PL b/c + warnings; ≤ 5 → administrative controls acceptable.
**Hierarchy of controls is mandatory order**: (1) eliminate by design → (2) safeguard/
engineering control → (3) information for use (warnings/training). You may not jump to
warnings if a design fix is feasible.

---

## 3. ISO/TS 15066 — Cobot Force and Pressure Limits

The core of power & force limiting (PFL) collaboration. Two contact types:

- **Quasi-static contact**: body part clamped between robot and fixed surface. The limit
  values below apply for the full clamp duration (≤ 0.5 s assumed, then must release).
- **Transient contact**: free impact, body part can recoil. Limits = **2× the
  quasi-static values** (pressure and force), contact duration < 50 ms.

### 3.1 Body region limit table (TS 15066 Annex A, the one everyone needs)

Quasi-static limits; transient = 2× force and 2× pressure (except skull/face & no transient contact permitted with skull/forehead in practice):

| Body region | Max pressure (N/cm²) | Max force (N) |
|---|---|---|
| Skull / forehead | 130 | 130 — **transient contact NOT permitted** |
| Face | 65 | 65 — **transient contact NOT permitted** |
| Neck (sides/muscle) | 140 | 150 |
| Neck (front/larynx) | 35 | 35 (treat as no-contact zone in practice) |
| Back / shoulders | 210 | 210 |
| Chest | 140 | 140 |
| Abdomen | 110 | 110 |
| Pelvis | 180 | 180 |
| Upper arm / elbow | 150 | 150 |
| Forearm / wrist | 160 | 160 |
| Hand / finger | 190 (fingertip pad ~300) | 140 |
| Thigh / knee | 220 | 220 |
| Lower leg | 210 | 130 |

Design rule: **identify which body regions can plausibly be contacted in your cell layout
and design to the WORST (lowest) applicable limit.** Tabletop cobot at face height of a
seated operator → face limits (65 N) govern, not hand limits. Standing operator, robot
below shoulder height → chest 140 N typically governs.

### 3.2 Converting limits to a speed limit (the calculation agents get wrong)

Transient contact is energy-limited. TS 15066 model: allowable transfer energy
E = F_max² / (2·k) with body-region spring constant k, and
v_rel,max = F_max / sqrt(μ·k), where μ = reduced mass = (1/m_robot_eff + 1/m_body)⁻¹.

Body-region spring constants (TS 15066): chest k=25 N/mm, abdomen 10, pelvis 25,
upper arm 30, forearm/hand 75, thigh 50, lower leg 60, skull 150.
Effective body masses: chest 40 kg, abdomen 40, pelvis 40, arm 3 (upper) / 2 (forearm),
hand 0.6, leg 75 (thigh) / 75, skull 4.4.

Worked example — cobot moving payload, effective moving mass m_r = 12 kg (≈ M/2 + payload
for an extended arm), hand contact (transient): F_max = 2×140 = 280 N, k = 75 N/mm =
75 000 N/m, m_h = 0.6 kg → μ = (1/12 + 1/0.6)⁻¹ = 0.571 kg →
v_max = 280 / sqrt(0.571 × 75000) = 280 / 207 ≈ **1.35 m/s**.
Same robot, chest contact: F=280, k=25 000, μ=(1/12+1/40)⁻¹=9.23 →
v = 280/sqrt(230 800) ≈ **0.58 m/s**. Chest governs → TCP speed limit 0.5 m/s is the
classic "safe cobot speed" — now you know where it comes from.

**Mistake everyone makes**: using rated payload mass as m_robot. Use *effective mass at
the contact point* = (manipulator moving mass)/2 + payload (TS 15066 simplification), and
remember sharp tooling concentrates pressure — a 140 N force through a 0.5 cm² screwdriver
tip = 280 N/cm² → exceeds every pressure limit. **Pressure usually fails before force.**
Pad/round all surfaces; minimum ~2 cm² contact area design target, no edges < 0.5 mm radius.

### 3.3 The four ISO 10218-2 collaborative methods

1. **Safety-rated monitored stop (SMS)** — robot stops (drives stay energized, SOS state)
   when human enters; resumes when they leave. Needs PL d monitored stop + presence sensing.
2. **Hand guiding** — motion only via hand-guide device with enabling switch (3-position)
   + safety-rated monitored speed.
3. **Speed & separation monitoring (SSM)** — protective separation distance
   S(t) = v_h·(t_r + t_s) + v_r·t_r + B + C + Z_d + Z_r, where v_h = 1.6 m/s walking speed
   (ISO 13855), t_r = sensor+controller reaction, t_s = stop time, B = braking distance,
   C = intrusion distance (850 mm reach allowance if hands undetected), Z = position
   uncertainties. Typical lidar-monitored AMR: t_r ≈ 0.1–0.3 s, full calc lands at 1.2–2 m
   protective fields at 1 m/s.
4. **Power & force limiting (PFL)** — the §3.1 limits, enforced by safety-rated
   force/torque sensing in joints (PL d Cat 3). Only method permitting contact by design.

Validation of PFL is **measured, not calculated**: use a biofidelic measurement device
(GTE CoboSafe / Pilz PRMS — spring + damper matched to body region k, pressure film) at
every plausible contact point/direction. Calculation gets you a design; measurement gets
you a CE file.

---

## 4. ISO 13482 — Personal Care Robots

Scope: non-medical robots in close, often continuous contact with untrained persons.
Three types:
- **Type 1 — Mobile servant robot** (home assistant, delivery-in-building, telepresence)
- **Type 2 — Physical assistant robot** (exoskeletons, restraint-type and non-restraint)
- **Type 3 — Person carrier robot** (mobility chairs, ride-on platforms)

Key differences from industrial standards (these change your design):
- **Users are untrained, including children, elderly, pregnant women, pets.** Avoidance
  parameter P is almost always P2. Exposure F2. → Most S2 hazards land at PL d/e.
- **Contact is the product, not the exception.** You cannot fence; you must limit energy.
- **Specific hazards 13482 forces you to address** (clause 5/6 list — use as checklist):
  battery charging (thermal runaway, charging while in contact with user), robot shape
  (edges < 0.5 mm radius prohibited at contact surfaces), moving parts/hair-entrapment
  (gaps must be < 5 mm or > 25 mm — the finger-probe rule), instability/tip-over (static
  stability ≥ 10° slope typical for Type 1; dynamic stability test with payload),
  travel surfaces (stair-edge detection — cliff sensors are SAFETY functions here),
  incorrect autonomous decisions, localization loss, EMC-induced misbehavior, **emotional
  hazards** (stress from unpredictable motion — required to consider, unique to 13482).
- **Safety-related speed control**: Type 1 robots near people typically limited to
  ≤ 0.5 m/s in proximity, with speed reduction zones. Person carriers: max speed and
  accel limits derived from passenger stability (typ. ≤ 6 km/h indoor, accel ≤ 0.5 m/s²,
  jerk-limited).
- **Protective stop must not itself create a hazard**: a powered exoskeleton doing STO
  mid-stride drops the user. Type 2 robots need a **safe-state strategy other than
  "remove power"** — controlled hold, gravity compensation retained, mechanical
  back-drivability or brakes sized for the user's weight. Document the safe-state
  rationale per hazard; "stop = safe" is an industrial assumption that fails here.
- Cliff/stair detection for Type 1: dual-technology recommended (IR cliff sensors fail on
  black/glossy floors — measure: Sharp GP2Y0A21 returns "far" on matte black carpet).
  Treat cliff detection as PL c/d → two independent sensing channels (e.g., downward IR
  pair + wheel-drop microswitches), either one triggers stop.

---

## 5. SIL / IEC 61508 Essentials That Affect Your Code

| SIL | PFD (low demand) | PFH (high demand/continuous) | HFT required (route 1H, SFF 60–90%) |
|---|---|---|---|
| 1 | 10⁻²–10⁻¹ | 10⁻⁶–10⁻⁵ | 0 |
| 2 | 10⁻³–10⁻² | 10⁻⁷–10⁻⁶ | 0–1 |
| 3 | 10⁻⁴–10⁻³ | 10⁻⁸–10⁻⁷ | 1 |
| 4 | 10⁻⁵–10⁻⁴ | 10⁻⁹–10⁻⁸ | 2 (don't go here; redesign) |

Robot safety functions are **high demand / continuous mode** — use PFH column.
HFT = hardware fault tolerance; HFT 1 = the function survives one fault = dual channel.

Software at SIL 2+ / PL d+ means: certified compiler or compiler qualification kit,
MISRA-C (or equivalent) coding standard, static analysis with zero unjustified findings,
MC/DC or branch coverage targets, no dynamic memory after init, no recursion, bounded
loops, WCET analysis. **You will not certify CPython, a Linux userland process, or a ROS2
node.** Plan accordingly: safety logic lives on a safety PLC (Pilz PNOZ, Sick Flexi,
Siemens F-CPU) or a lockstep MCU with a certified RTOS (SafeRTOS, Zephyr in cert track,
PXROS), and ROS2 talks to it over a *monitored* interface.

---

## 6. Architecture Patterns and Working Code

### 6.1 Reference architecture for a cobot/AMR cell

```
                         ┌──────────────────────────────┐
  Functional layer (QM): │ ROS2 / Python / planner      │  can REQUEST stop,
                         │ publishes /cmd_vel, motion    │  reduce speed, replan
                         └───────────┬──────────────────┘
                                     │ heartbeat + status (RS485/CAN/EtherCAT FSoE)
                         ┌───────────▼──────────────────┐
  Safety layer (PL d):   │ Safety PLC / safety relay     │  e-stop 2ch, scanner OSSD 2ch,
                         │ Cat 3 dual channel            │  enabling switch, door switch
                         └───────┬──────────┬───────────┘
                                 │ STO1/STO2│ K1/K2 contactors (force-guided, monitored
                         ┌───────▼───┐  ┌───▼────────┐    via mirror contacts in feedback loop)
                         │ Servo STO │  │ Motor power │
                         └───────────┘  └────────────┘
```

Wiring table — e-stop into a safety relay (e.g., Pilz PNOZ s4, 24 VDC):

| Signal | From | To | Notes |
|---|---|---|---|
| Test pulse out T0 | Relay S11 | E-stop NC contact 1 | Channel 1, pulsed for cross-short detection |
| Channel 1 in | E-stop contact 1 | Relay S12 | |
| Test pulse out T1 | Relay S21 | E-stop NC contact 2 | Channel 2, different pulse pattern |
| Channel 2 in | E-stop contact 2 | Relay S22 | |
| Reset | Momentary NO button | S34 | **Monitored manual reset** — relay arms on falling edge so a stuck/jumpered button can't auto-reset |
| Safety out 13-14 | Relay | Drive STO_A | 24 V removed = torque off |
| Safety out 23-24 | Relay | Drive STO_B | second channel |
| Feedback loop | K1+K2 NC mirror contacts in series | Y1-Y2 | relay refuses to arm if a contactor welded |

E-stop device rules: red mushroom on yellow background, **NC contacts, positive
(direct) opening action** (look for the ⊖→ arrow symbol on the contact block), latching,
twist/pull release. Never use an NO contact or a GPIO-polled button as the e-stop.
E-stop ≠ protective stop: e-stop is Stop Category 0 or 1 and requires manual reset +
deliberate restart; protective stop (light curtain) may allow automatic re-arm if the
risk assessment permits (it usually doesn't behind a walk-through point).

Stop categories (IEC 60204-1):
- **Cat 0**: immediate power removal (STO). Uncontrolled coast/brake. Longest stopping
  distance for heavy axes — sometimes Cat 1 is *safer*.
- **Cat 1**: controlled deceleration on the drive, THEN power removal (SS1). Standard for
  robot arms. Typical SS1 time window 300–500 ms enforced by the safety relay timer.
- **Cat 2 / SS2 / SOS**: controlled stop, power retained, position safety-monitored.
  Used for safety-rated monitored stop in collaboration.

### 6.2 Functional-layer safety *monitoring* (NOT a substitute for the safety layer)

ROS2 heartbeat + command gating pattern — the functional layer proves liveness to a
hardware watchdog; loss of heartbeat = safety layer drops to safe state:

```python
# ROS2 (rclpy) — functional safety MONITOR pattern. QM code: improves availability and
# adds defense-in-depth. The certified path is scanner->safety PLC->STO underneath this.
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool

SLOW_ZONE_M = 1.5      # from SSM calc, §3.3 — recompute for YOUR t_r and braking
STOP_ZONE_M = 0.7
CMD_TIMEOUT_S = 0.2    # stale /cmd_vel => zero output (deadman on the data path)
SCAN_TIMEOUT_S = 0.3   # stale scan => treat as obstacle at 0 m, NEVER as "clear"

class SafetyGate(Node):
    def __init__(self):
        super().__init__('safety_gate')
        # Sensor QoS must be BEST_EFFORT to match driver; commands RELIABLE.
        self.sub_scan = self.create_subscription(
            LaserScan, '/scan', self.on_scan,
            QoSProfile(depth=1, reliability=ReliabilityPolicy.BEST_EFFORT))
        self.sub_cmd = self.create_subscription(Twist, '/cmd_vel_raw', self.on_cmd, 1)
        self.pub_cmd = self.create_publisher(Twist, '/cmd_vel', 1)
        self.pub_hb  = self.create_publisher(Bool, '/safety_heartbeat', 1)
        self.min_range = 0.0           # pessimistic init: blocked until proven clear
        self.t_scan = self.t_cmd = self.get_clock().now()
        self.last_cmd = Twist()
        self.timer = self.create_timer(0.05, self.tick)   # 20 Hz gate

    def on_scan(self, msg):
        valid = [r for r in msg.ranges if msg.range_min < r < msg.range_max]
        # Empty valid list = sensor blinded/dirty => pessimistic, not "no obstacle"
        self.min_range = min(valid) if valid else 0.0
        self.t_scan = self.get_clock().now()

    def on_cmd(self, msg):
        self.last_cmd = msg
        self.t_cmd = self.get_clock().now()

    def tick(self):
        now = self.get_clock().now()
        scan_fresh = (now - self.t_scan).nanoseconds < SCAN_TIMEOUT_S * 1e9
        cmd_fresh  = (now - self.t_cmd).nanoseconds  < CMD_TIMEOUT_S * 1e9
        out = Twist()
        if scan_fresh and cmd_fresh and self.min_range > STOP_ZONE_M:
            scale = 1.0 if self.min_range > SLOW_ZONE_M else \
                (self.min_range - STOP_ZONE_M) / (SLOW_ZONE_M - STOP_ZONE_M)
            out.linear.x = self.last_cmd.linear.x * scale
            out.angular.z = self.last_cmd.angular.z * scale
        # else: out stays zero — fail silent-to-stop, never coast on last command
        self.pub_cmd.publish(out)
        hb = Bool(); hb.data = scan_fresh        # external HW watchdog also strobed by
        self.pub_hb.publish(hb)                  # the base MCU on receipt (see 6.3)

def main():
    rclpy.init(); rclpy.spin(SafetyGate()); rclpy.shutdown()
```

Rules baked in above that agents routinely violate:
1. **Stale sensor = obstacle, not clear.** Initialize pessimistic.
2. **Stale command = zero velocity**, never "repeat last command".
3. The gate runs on its **own timer**, not inside callbacks, so it fails-to-stop when
   upstream dies.
4. Speed scales down *before* the stop zone (smooth SSM), preventing nuisance Cat 0 stops.

### 6.3 Hardware watchdog + dual-channel input on a microcontroller (MicroPython, RP2040/ESP32)

For hobby/educational robots where a safety PLC is overkill but you still want the
*pattern* right (two channels, discrepancy monitoring, independent watchdog, default-off
actuation):

```python
# MicroPython — dual-channel e-stop read + motor enable with hardware watchdog.
# Wiring: e-stop block with 2x NC contacts.
#   CH_A: 3V3 -> NC contact 1 -> GPIO16 (pull-down). Pressed => contact opens => reads 0.
#   CH_B: 3V3 -> NC contact 2 -> GPIO17 (pull-down). Pressed => reads 0.
#   Healthy (released) state = both HIGH. Broken wire = LOW = SAFE. <- why NC is mandatory.
# Motor enable: GPIO18 -> driver EN, with 10k pull-DOWN on the PCB so MCU reset/boot
#   = motors disabled by hardware, not by code.
from machine import Pin, WDT, Timer
import time

ESTOP_A = Pin(16, Pin.IN, Pin.PULL_DOWN)
ESTOP_B = Pin(17, Pin.IN, Pin.PULL_DOWN)
MOTOR_EN = Pin(18, Pin.OUT, value=0)        # default OFF at boot

wdt = WDT(timeout=200)                       # ms; HW reset if loop hangs.
                                             # On reset MOTOR_EN pull-down kills motors.
DISCREPANCY_MS = 250                         # channels must agree within this window
latched_stop = True                          # require explicit reset after boot
discrep_t0 = None

def estop_active():
    global discrep_t0
    a, b = ESTOP_A.value(), ESTOP_B.value()
    if a == 1 and b == 1:
        discrep_t0 = None
        return False                         # both closed: released
    if a == 0 and b == 0:
        discrep_t0 = None
        return True                          # both open: pressed (or both wires cut)
    # Channels disagree: wiring fault or contact failure. Tolerate only briefly
    # (mechanical contacts don't open simultaneously), then latch a FAULT.
    now = time.ticks_ms()
    if discrep_t0 is None:
        discrep_t0 = now
        return True                          # safe-side while disagreeing
    if time.ticks_diff(now, discrep_t0) > DISCREPANCY_MS:
        fault_latch()                        # permanent until power cycle + repair
    return True

def fault_latch():
    MOTOR_EN.value(0)
    while True:                              # deliberate: only power-cycle clears a
        time.sleep_ms(100)                   # channel-discrepancy FAULT
        wdt.feed()                           # keep WDT fed; we are intentionally parked

RESET_BTN = Pin(19, Pin.IN, Pin.PULL_DOWN)   # momentary NO, monitored manual reset
prev_reset = 0

while True:
    wdt.feed()
    if estop_active():
        latched_stop = True
        MOTOR_EN.value(0)
    else:
        r = RESET_BTN.value()
        if latched_stop and prev_reset == 1 and r == 0:   # FALLING edge arms:
            latched_stop = False                          # stuck/jumpered button can't reset
        prev_reset = r
        MOTOR_EN.value(1 if not latched_stop else 0)
    time.sleep_ms(10)
```

Electrical numbers that matter here: drive contactor/relay coils from a transistor with
flyback diode, never from GPIO (GPIO source limit: RP2040 12 mA max set, ESP32 ~40 mA abs
max, a 24 V contactor coil draws 50–200 mA). Use force-guided relays (e.g., TE SR6,
Panasonic SF-Y) if you want a monitorable feedback contact. Opto-isolate STO inputs;
servo STO inputs are typically 24 V, 5–10 mA per channel, and require BOTH channels low
to remove torque with a plausibility window (~100 ms) enforced inside the drive.

### 6.4 Arduino C++ — Safe Torque Off request + SS1 timing on a drive

```cpp
// SS1 (Stop Category 1) sequencing from a supervisory MCU.
// The DRIVE's certified STO is the safety function; this code only sequences the
// controlled-deceleration request before the safety relay's hard-wired timer fires STO.
// Safety relay (e.g. PNOZ s5) delayed outputs are set to 500 ms: relay drops
// instant outputs (-> our DECEL_REQ interrupt) at t=0 and STO at t=500ms REGARDLESS
// of what this code does. We just make the stop graceful within that window.
const uint8_t PIN_DECEL_REQ = 2;    // from relay instant output, via opto, FALLING = stop
const uint8_t PIN_DAC_SPEED = 9;    // PWM->RC filter -> drive analog speed ref
volatile bool stopRequested = false;
const uint16_t DECEL_MS = 350;      // must finish < 500 ms relay STO timer, margin 150 ms
                                    // => required decel = v_max / 0.35 s; verify drive
                                    // current limit can deliver it WITH max payload.
void onStopReq() { stopRequested = true; }

void setup() {
  pinMode(PIN_DECEL_REQ, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_DECEL_REQ), onStopReq, FALLING);
  analogWrite(PIN_DAC_SPEED, 0);    // power-up at zero speed reference, always
}

void loop() {
  static uint8_t speedCmd = 0;
  if (stopRequested) {
    uint32_t t0 = millis();
    uint8_t v0 = speedCmd;
    while (millis() - t0 < DECEL_MS) {              // linear ramp to zero
      speedCmd = v0 - (uint32_t)v0 * (millis() - t0) / DECEL_MS;
      analogWrite(PIN_DAC_SPEED, speedCmd);
    }
    speedCmd = 0;
    analogWrite(PIN_DAC_SPEED, 0);
    while (true) { /* park; STO lands at t=500ms; manual reset restarts system */ }
  }
  // ... normal operation updates speedCmd ...
  analogWrite(PIN_DAC_SPEED, speedCmd);
}
```

**Timing constraint discipline**: total stop performance = sensor response + logic
response + drive decel + mechanical. Document each. Example budget for SSM at PL d:
scanner OSSD response 60–120 ms (Sick nanoScan3: 70 ms typ) + safety PLC cycle 8–25 ms +
drive SS1 ramp 300 ms + brake engagement 40 ms. That total (≈ 450 ms) and v_h = 1.6 m/s
puts ≥ 0.72 m of the protective distance into human motion alone — never shave C and Z.

---

## 7. Safety vs Functional Requirements Split

Write two separate requirement sets. Mixing them is the #1 documentation failure.

| | Safety requirement | Functional requirement |
|---|---|---|
| Purpose | Prevent harm | Do the job / availability / quality |
| Example | "Torque shall be removed from all axes within 500 ms of e-stop actuation (Stop Cat 1, PL d)" | "The robot shall resume the interrupted pick within 5 s of reset" |
| Implemented in | Safety-rated channel (relay/PLC/lockstep MCU/drive STO) | Application code (QM) |
| Failure response | Fail to SAFE state, latch, manual reset | Retry, degrade, log |
| Verification | Validated + measured per ISO 13849-2 (fault injection: cut each wire, short channels, weld a contactor) | Tested per normal SW QA |
| Change control | Re-assessment + re-validation, signed | Normal code review |

Litmus tests for classifying a requirement:
- "If this fails, can someone be hurt?" → safety. "Just annoyed/blocked?" → functional.
- If the requirement says "detect AND continue operating" it's functional; safety
  requirements end in a defined safe state.
- The functional layer may *duplicate* a safety behavior for availability (slow down
  before the scanner trips) — that duplication is functional, claim no risk reduction
  from it, and say so explicitly in the risk assessment.

Traceability chain a certification auditor walks: Hazard → risk score (S/F/P) → required
PLr/ASIL → safety function spec (what, safe state, response time) → architecture
(category/channels) → component data (B10d, MTTFd, DC, PFHd from datasheets, summed in
SISTEMA or PAScal) → validation test record. Any broken link = finding.

---

## 8. Mistakes Everyone Makes (Pre-Review Checklist)

1. **Software e-stop.** A GUI button or topic named `/emergency_stop` is not an e-stop.
   It may exist as a *protective/functional* stop only; never label it "Emergency Stop".
2. **NO contacts on safety inputs.** Broken wire then reads as "not pressed". All safety
   inputs: NC, positive-opening, dual-channel, pulsed test signals.
3. **Single-channel PL d claim.** Cat 3 means two channels. One reed switch on a door is
   PL c best case.
4. **Auto-reset behind walk-through guards.** A person can stand inside while the curtain
   clears at the boundary. Reset button must be located with full view of the cell,
   outside it, and unreachable from inside.
5. **Forgetting gravity.** STO on a vertical axis = falling axis. Z-axes need a certified
   holding brake, brake-test routine (measure: command 30% torque against closed brake at
   startup, verify zero encoder movement), and SBC (safe brake control) channel.
6. **Pressure ignored, force-only design.** §3.2 — sharp tool exceeds pressure limit at
   half the force limit. Always compute N/cm² at the actual contact geometry.
7. **Using cobot = automatically safe.** A UR10e with a knife-edge gripper or a 0.9 m/s
   trajectory at face height is not a collaborative *application*. TS 15066 assesses the
   application (robot + tool + workpiece + cell), not the robot.
8. **Watchdog fed from a timer interrupt.** Feeds keep coming while the main loop is
   dead. Feed the WDT only from the main control loop after a full healthy iteration,
   ideally with a windowed watchdog (feed too *early* also trips — catches runaway loops).
9. **Heartbeat without sequence numbers.** A switch replaying / a stuck publisher passing
   the same message at rate looks alive. Heartbeat = counter + timeout + (for networks)
   CRC — this is the Black Channel principle behind FSoE/PROFIsafe/CIP-Safety.
10. **Testing only the happy path.** ISO 13849-2 validation = fault injection. Actually
    cut each channel wire, short CH_A to CH_B, short channel to 24 V and to 0 V, stick the
    reset button down, disconnect the encoder, block the brake. Record observed behavior.
11. **MTTFd math on the whole machine.** PL is computed *per safety function* over its
    channel (sensor + logic + actuator subsystems combined per 13849-1 Annex, or just sum
    PFHd of certified subsystems). Don't average unrelated functions.
12. **Muting/blanking as a loophole.** Light-curtain muting needs ≥ 2 independent muting
    sensors, time-limited (typ ≤ 10 s window), direction logic, and muting lamps. "Disable
    the curtain while the pallet passes" via PLC bit = instant audit failure.
13. **Treating SOTIF as covered.** ISO 26262/13849 cover malfunctions. A perception system
    performing *as designed* but insufficient (lidar can't see glass walls, camera blinded
    by low sun) is ISO 21448 territory — list performance limitations as hazards too.
14. **Cliff sensors as functional-only on a stair-capable platform** — on anything that
    can reach a drop > 0.5 m with a person nearby (or carrying one), edge detection is a
    safety function (see §4).
15. **Claiming risk reduction from the QM layer.** The ROS gate in §6.2 reduces *demand
    rate* on the safety system; it contributes **zero** to the PL claim. Write that
    sentence into the safety concept verbatim — assessors look for it.

## 9. Debugging Checklist — Safety Chain Won't Arm / Trips Randomly

- Relay won't arm: feedback loop Y1-Y2 open? (welded contactor mirror contact, or you
  forgot to wire it — bridge ONLY during bench bring-up, never in service).
- Arms then trips immediately: channel discrepancy. Measure both channels with a scope —
  pulsed test outputs mean a multimeter shows ~22–23 V average and lies to you. Look for
  one channel's pulses appearing on the other = cross short = trip by design.
- Random trips on long runs: e-stop wiring run alongside VFD motor cables inducing pulses
  → separate trays/ shielded cable, shield grounded one end at the relay.
- OSSD scanner output trips with nothing visible: dust/condensation on the window (most
  scanners report a window-contamination warning code first — read the diagnostics), or
  reflective floor strip inside the protective field at shallow angle.
- STO "works" but motor coasts forever into the fixture: you needed Stop Cat 1 (SS1), not
  Cat 0 — add the delayed-output timer and the decel sequencing (§6.4).
- Drive faults "STO channel plausibility": the two STO inputs switched > ~100 ms apart —
  one relay output is slow/loaded; drive both channels from the same safety relay output
  group, check wiring lengths and opto delays.
- WDT resets in the field but not the lab: blocking I/O (network/SD/print over USB) in
  the control loop exceeding the timeout under load — budget loop WCET, move I/O off the
  safety-adjacent loop.

---

**Bottom line for code generation**: put the certified stop chain in hardware; make every
software default pessimistic (boot disabled, stale = obstacle, silence = stop); use two
channels and check they agree; derive every speed and distance number from the §2 risk
assessment and §3 tables, and write the safety/functional split down before writing code.
