---
name: fault-detection-recovery
description: "Use when a robot must detect, classify, and recover from faults — sensor dropouts, actuator stalls, software hangs, comms loss — or when designing watchdogs, heartbeats, plausibility checks, degraded modes, or chaos tests. Provides fault taxonomy, detection patterns (heartbeat/plausibility/residual), fault→response matrices, auto-recovery vs escalation logic, and working MicroPython, Arduino C++, and ROS 2 code."
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


# Fault Detection & Recovery for Robots

Core principle: **a robot that cannot detect its own faults is a robot that fails silently and dangerously.** Every fault must map to exactly one of: (a) tolerate, (b) degrade, (c) safe-stop, (d) escalate to operator. Never "log and continue" for actuator or safety faults.

## 1. Fault Taxonomy

Classify every conceivable fault into one of four classes. Detection method and response differ per class.

| Class | Examples | Typical detection | Typical latency budget |
|---|---|---|---|
| **Sensor** | stuck-at value, dropout (NaN/timeout), drift, spikes, miscalibration, saturation | plausibility checks, rate-of-change, cross-sensor residual | 1–3 sample periods |
| **Actuator** | motor stall, encoder slip, servo jitter, overcurrent, burned driver, mechanical jam, runaway | current sensing, commanded-vs-measured residual, thermal model | 10–100 ms (stall), <500 ms (thermal) |
| **Software** | task hang, deadlock, memory exhaustion, slow control loop, exception storm, clock skew | watchdog timers, loop-time monitor, heap watermark | 1–2 watchdog periods |
| **Comms** | link dropout (RF/WiFi/CAN), stale data, corruption, bus-off, partial network split | heartbeat timeout, sequence numbers, CRC, CAN error counters | 2–5 heartbeat periods |

### Sub-taxonomy with concrete signatures

**Sensor faults:**
- *Stuck-at*: identical raw value for N samples. An ADC reading EXACTLY the same 12-bit value 50 times in a row is broken (real signals have noise). Threshold: variance < 1 LSB over 50 samples → fault.
- *Dropout*: I2C NACK, SPI all-0xFF or all-0x00, UART timeout. 0xFF on SPI usually means MISO floating (chip absent/unpowered). 0x00 usually means MISO grounded or chip in reset.
- *Drift*: gyro bias walking >0.5 °/s from startup calibration while robot is known-stationary.
- *Spike*: |x[k] − x[k−1]| > physically possible slew. Example: a robot that tops out at 2 m/s cannot show a 5 m position jump between 50 Hz samples.
- *Saturation*: reading pinned at min/max of range (e.g., ±32768 on a ±2g accelerometer means you needed ±8g range, or the sensor is railed).

**Actuator faults:**
- *Stall*: current at/above stall current AND encoder velocity ≈ 0 while PWM duty > ~30%. N20 micro gearmotor: free ~80 mA, stall 0.6–1.6 A. RS-550: free ~1.5 A, stall 80+ A. Detect within 100 ms; sustained stall burns windings in seconds at full voltage.
- *Encoder slip/failure*: PWM > 50% for > 200 ms with zero encoder counts → encoder dead OR motor dead OR wheel off ground. Disambiguate with current: high current = stall, low/free current = encoder fault or drivetrain decoupled.
- *Runaway*: measured velocity opposite in sign to command, or velocity grows with zero command → swapped motor leads, sign error in feedback, or driver short. Hard-stop immediately; PID with inverted feedback diverges in <1 s.
- *Servo fault*: hobby servo drawing > 1 A continuously is jammed against an obstacle or end-stop; it will strip gears or burn out. Detect via INA219/ACS712 on the servo rail.

**Software faults:**
- *Loop overrun*: control loop budgeted 10 ms (100 Hz) takes 25 ms → derivative term of PID computed with wrong dt corrupts control. Always measure actual dt; flag if dt > 1.5× nominal.
- *Heap exhaustion*: MicroPython `gc.mem_free()` < 20 kB on ESP32 → allocation failures imminent in WiFi/SSL stacks.
- *Priority inversion / starvation*: low-rate logger blocking the control task. Symptom: periodic loop-time spikes at the logger's period.

**Comms faults:**
- *Stale data*: packet arrives but contains old state (sender hung between sensor read and transmit). Detect with sender-side monotonic sequence numbers + sender timestamps, not just receiver-side arrival time.
- *CAN bus-off*: TEC ≥ 256 silences the node. Error-passive at TEC ≥ 128 is the early warning — monitor error counters, don't wait for bus-off.
- *WiFi dropout on ESP32*: typical reconnect 2–8 s. Any robot using WiFi for teleop MUST stop motion within 500 ms of last valid command (failsafe timeout), because reconnection is too slow to be in the safety loop.

## 2. Detection Patterns

### 2.1 Heartbeats and watchdogs

Three layers, all of them, always:

1. **Hardware watchdog** (last resort, catches everything including hard faults): MCU WDT resets the chip. ESP32: 1–10 s typical. AVR: `wdt_enable(WDTO_2S)`.
2. **Software watchdog** (task-level): each task pets a flag; a monitor task checks all flags every period.
3. **Comms heartbeat** (inter-device): periodic message with sequence number; receiver times out.

**Numbers that work:**
- Heartbeat rate: 10 Hz (100 ms period) for motion-critical links.
- Timeout: 3 missed beats = 300 ms → stop motors. One missed beat is normal on WiFi/RF; two is suspicious; three is a fault. Single-beat timeout causes constant false trips on 2.4 GHz.
- Hardware WDT: 2–4× the slowest legitimate operation (e.g., 8 s if you do OTA/flash writes, 2 s otherwise).

**MicroPython — ESP32 failsafe receiver (the pattern everyone gets wrong by petting the WDT unconditionally):**

```python
import time
from machine import WDT, Pin, PWM

wdt = WDT(timeout=4000)          # hardware backstop: 4 s
HEARTBEAT_TIMEOUT_MS = 300       # comms failsafe: 3 missed 100ms beats
last_beat = time.ticks_ms()
last_seq = -1
estop_latched = False

def on_packet(seq, cmd):
    """Called from comms RX. Validates freshness via sequence number."""
    global last_beat, last_seq
    if seq <= last_seq and last_seq - seq < 1000:   # allow wraparound
        return                                       # stale/duplicate: ignore
    last_seq = seq
    last_beat = time.ticks_ms()
    apply_command(cmd)

def safety_loop():
    global estop_latched
    while True:
        now = time.ticks_ms()
        comms_ok = time.ticks_diff(now, last_beat) < HEARTBEAT_TIMEOUT_MS
        if not comms_ok and not estop_latched:
            stop_all_motors()          # set PWM duty to 0 AND disable driver EN pin
            estop_latched = True
        if comms_ok and estop_latched:
            # auto-recover ONLY if commanded velocity is currently zero,
            # so the robot doesn't lurch when the link returns
            if current_command_is_zero():
                estop_latched = False
        # CRITICAL: pet the WDT only if the safety loop itself is healthy.
        # If sensors or the control task hang, we WANT the reset.
        if safety_loop_healthy():
            wdt.feed()
        time.sleep_ms(20)              # 50 Hz safety loop
```

**The #1 watchdog mistake:** feeding the WDT in a timer ISR or a dedicated "feeder" task. That makes the WDT useless — the feeder keeps running while your control task is deadlocked. Feed only from the main control/safety loop after verifying it actually did its work.

**Arduino C++ — multi-task software watchdog (single monitor, per-task flags):**

```cpp
// Each task sets its bit each cycle; monitor clears mask and checks next cycle.
#include <avr/wdt.h>

volatile uint8_t taskAlive = 0;
#define TASK_CONTROL  (1 << 0)
#define TASK_SENSORS  (1 << 1)
#define TASK_COMMS    (1 << 2)
const uint8_t ALL_TASKS = TASK_CONTROL | TASK_SENSORS | TASK_COMMS;

uint32_t lastCheck = 0;

void setup() {
  wdt_enable(WDTO_2S);   // hardware backstop
}

void loop() {
  controlTask();   // sets taskAlive |= TASK_CONTROL when it completes a cycle
  sensorTask();    // sets TASK_SENSORS
  commsTask();     // sets TASK_COMMS

  if (millis() - lastCheck >= 500) {            // check at 2 Hz
    lastCheck = millis();
    if ((taskAlive & ALL_TASKS) == ALL_TASKS) {
      wdt_reset();                              // all tasks ran: pet HW WDT
      taskAlive = 0;
    }
    // else: do NOT pet. HW WDT resets us within 2 s. The reset handler
    // (check MCUSR & WDRF in setup) logs the stuck-task mask to EEPROM.
  }
}
```

On reset, read `MCUSR` (AVR) or `esp_reset_reason()` (ESP32, returns `ESP_RST_TASK_WDT` / `ESP_RST_WDT`) to distinguish watchdog reset from power-on — and log it. A robot that watchdog-resets every 30 s "works" in demos and fails in the field.

### 2.2 Plausibility checks (range, rate, cross-checks)

Every sensor reading passes three gates before the control loop may use it:

| Gate | Rule | Example values |
|---|---|---|
| **Range** | min ≤ x ≤ max of physical possibility | battery 3S LiPo: 9.0–12.6 V; ultrasonic HC-SR04: 2–400 cm; IMU temp: −40 to 85 °C |
| **Rate** | \|dx/dt\| ≤ physical slew limit | wheel accel of a 1 kg robot ≤ ~20 m/s²; battery voltage slews < 0.5 V per 10 ms (faster = connector glitch) |
| **Cross** | independent sensors must agree within tolerance | encoder-derived speed vs IMU-integrated speed within 0.3 m/s; dual temperature sensors within 5 °C |

```python
class PlausibilityFilter:
    """Gate one sensor channel. Returns (value, ok). Holds last-good for
    up to max_hold samples, then declares the channel FAULTED."""
    def __init__(self, lo, hi, max_slew_per_s, max_hold=5):
        self.lo, self.hi = lo, hi
        self.max_slew = max_slew_per_s
        self.max_hold = max_hold
        self.last = None
        self.last_t = None
        self.held = 0
        self.faulted = False
        self.stuck_count = 0

    def update(self, x, t_s):
        bad = False
        if x is None or x != x:                      # None or NaN
            bad = True
        elif not (self.lo <= x <= self.hi):
            bad = True
        elif self.last is not None:
            dt = t_s - self.last_t
            if dt > 0 and abs(x - self.last) / dt > self.max_slew:
                bad = True
            if x == self.last:
                self.stuck_count += 1
                if self.stuck_count > 50:            # stuck-at detector
                    bad = True
            else:
                self.stuck_count = 0
        if bad:
            self.held += 1
            if self.held > self.max_hold:
                self.faulted = True
            return self.last, not self.faulted       # hold last-good briefly
        self.last, self.last_t, self.held = x, t_s, 0
        self.faulted = False
        return x, True
```

**Mistakes everyone makes here:**
- Clamping out-of-range values instead of rejecting them. A railed sensor clamped to max range silently drives the controller. Reject, hold-last-good for a few samples, then fault.
- Rate checks using nominal dt instead of measured dt. After a loop overrun, dt doubles and a legitimate change trips a false spike fault.
- No stuck-at detection. The most common real failure of analog sensors (broken wire to ADC pin reads a constant via the pin's parasitic capacitance) passes range AND rate checks forever.
- Filtering before plausibility checking. A low-pass filter smears a 1-sample spike into 10 plausible-looking samples. Check raw, then filter.

### 2.3 Model-based residuals

Compare what the actuator *should* be doing (model) with what sensors *say* it's doing. Residual = |predicted − measured|. Threshold with hysteresis and a persistence counter.

**DC motor stall/health residual (the workhorse):** at steady state, `I ≈ (V_applied − Ke·ω) / R`. You don't need the exact model — learn the nominal current-vs-duty curve at commissioning, then flag deviations.

```cpp
// Arduino C++ — stall + free-spin detection on a brushed DC motor
// Hardware: INA219 on I2C (or ACS712 on A0), quadrature encoder on pins 2/3.
struct MotorHealth {
  float stallCurrentA   = 1.2;   // from motor datasheet (e.g. N20 at 6V)
  float minMovingDuty   = 0.30;  // below this, "no encoder counts" is normal
  uint16_t stallMs      = 100;   // persistence before declaring stall
  uint32_t stallStart   = 0;
  bool stalled          = false;
  bool encoderFault     = false;
};

void checkMotor(MotorHealth &m, float duty, float currentA, float encVelCps) {
  bool stallSig = (fabs(duty) > m.minMovingDuty) &&
                  (currentA > 0.8f * m.stallCurrentA) &&
                  (fabs(encVelCps) < 5.0f);             // counts/sec ~ zero
  if (stallSig) {
    if (m.stallStart == 0) m.stallStart = millis();
    if (millis() - m.stallStart > m.stallMs) m.stalled = true;
  } else {
    m.stallStart = 0;
    // hysteresis: only clear stall after current drops well below threshold
    if (m.stalled && currentA < 0.4f * m.stallCurrentA) m.stalled = false;
  }
  // Encoder fault: driving hard, current LOW (motor spinning free), no counts
  m.encoderFault = (fabs(duty) > 0.5f) &&
                   (currentA < 0.3f * m.stallCurrentA) &&
                   (fabs(encVelCps) < 5.0f);
}
```

**IMU-vs-encoder cross residual (catches wheel slip AND encoder faults):**

```python
# residual between gyro yaw rate and differential-drive kinematic yaw rate
# omega_kin = (v_right - v_left) / track_width
def yaw_residual(gyro_z_rad_s, v_l, v_r, track_m=0.15):
    omega_kin = (v_r - v_l) / track_m
    return abs(gyro_z_rad_s - omega_kin)

# Thresholding: residual > 0.5 rad/s for > 200 ms (10 samples @ 50 Hz)
#   while |commanded turn| is small  -> wheel slip or encoder fault
#   while turning hard               -> probably slip; degrade to gyro-only odom
```

**Residual thresholding rules:**
- Always use persistence (N-of-M): fault if residual exceeds threshold in ≥ 7 of last 10 samples. Single-sample thresholds false-trip on every bump.
- Always use hysteresis: trip at T, clear at 0.5·T. Otherwise the fault flag chatters and your recovery logic oscillates.
- Threshold = 3–5× the residual's standard deviation measured during known-good operation, not a guess. Log residuals during commissioning and compute it.

### 2.4 Comms integrity

- **Sequence numbers**: uint16, increment per packet, wrap allowed. Receiver tracks gaps (loss rate) and rejects duplicates/reordering.
- **CRC**: CRC-16/CCITT minimum on any UART/RF link. XOR checksums miss byte-swap errors. CAN has CRC in hardware; UART has nothing.
- **Stale-data guard**: include sender's `ticks_ms` in the packet; receiver rejects packets older than 2 periods *by sender clock delta*, not arrival time.
- **CAN health**: read TX/RX error counters every second. TEC > 96 → log warning (something is wrong with termination/bitrate). TEC ≥ 128 (error-passive) → degraded mode. Bus-off → comms fault, safe-stop anything that depends on that node.

### 2.5 ROS 2 detection layer

Use lifecycle nodes + `diagnostic_updater` + per-topic deadline QoS. Deadline QoS gives you free heartbeat monitoring.

```python
# ROS 2 (rclpy) — supervisor with deadline-based heartbeat + diagnostics
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from rclpy.duration import Duration
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue

class Supervisor(Node):
    def __init__(self):
        super().__init__('fault_supervisor')
        # Deadline QoS: middleware calls deadline_callback if no msg in 200 ms
        qos = QoSProfile(depth=1, reliability=ReliabilityPolicy.BEST_EFFORT)
        qos.deadline = Duration(seconds=0.2)
        self.scan_ok = False
        self.create_subscription(
            LaserScan, '/scan', self.on_scan, qos,
            event_callbacks=rclpy.qos_event.SubscriptionEventCallbacks(
                deadline=self.on_scan_deadline_missed))
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel_safe', 1)
        self.diag_pub = self.create_publisher(DiagnosticArray, '/diagnostics', 1)
        self.mode = 'NOMINAL'   # NOMINAL | DEGRADED | SAFE_STOP
        self.create_timer(0.05, self.tick)   # 20 Hz supervisor

    def on_scan(self, msg):
        # plausibility: a lidar reporting ALL ranges == range_max is unplugged
        # or staring at the sky; all == range_min is covered/blocked.
        finite = [r for r in msg.ranges
                  if msg.range_min < r < msg.range_max]
        self.scan_ok = len(finite) > 0.1 * len(msg.ranges)

    def on_scan_deadline_missed(self, event):
        self.scan_ok = False

    def tick(self):
        if not self.scan_ok and self.mode == 'NOMINAL':
            self.mode = 'DEGRADED'      # e.g. cap speed, odom-only navigation
        if self.mode == 'SAFE_STOP':
            self.cmd_pub.publish(Twist())   # zeros
        self.publish_diag()

    def publish_diag(self):
        s = DiagnosticStatus()
        s.name, s.hardware_id = 'supervisor', 'base'
        s.level = (DiagnosticStatus.OK if self.mode == 'NOMINAL'
                   else DiagnosticStatus.WARN if self.mode == 'DEGRADED'
                   else DiagnosticStatus.ERROR)
        s.message = self.mode
        s.values = [KeyValue(key='scan_ok', value=str(self.scan_ok))]
        arr = DiagnosticArray()
        arr.header.stamp = self.get_clock().now().to_msg()
        arr.status = [s]
        self.diag_pub.publish(arr)
```

ROS 2 specifics that bite:
- DDS discovery after a node restart takes 1–3 s; design recovery sequences to tolerate this (don't declare the restarted node dead at 500 ms).
- `use_sim_time` mismatch between nodes makes all timestamp-based staleness checks lie. Verify it's consistent across the graph at startup.
- Best-effort QoS on a publisher + reliable on the subscriber = silently no connection. Heartbeat "faults" that are actually QoS mismatches are the most common ROS 2 false alarm. Check with `ros2 topic info -v /topic`.

## 3. Fault → Degraded-Mode Matrix

Write this table for YOUR robot before writing recovery code. Template (differential-drive mobile robot with lidar, IMU, encoders, WiFi teleop):

| Fault | Detection | Immediate action (≤ 1 loop) | Degraded mode | Auto-recovery condition | Escalate if |
|---|---|---|---|---|---|
| Comms heartbeat lost | 300 ms timeout | zero cmd_vel, latch | hold position | link restored AND cmd is zero | > 30 s outage |
| Lidar dropout | deadline 200 ms / all-max ranges | cap speed to 0.1 m/s | encoder+IMU odom only, no autonomous nav | 10 consecutive good scans | > 10 s |
| One encoder dead | residual vs IMU + low current | none (stay moving) | gyro-based heading hold, halve max speed | never auto (hardware) | always — operator |
| Motor stall | current+encoder, 100 ms | PWM to 0 on that motor | — | 3 retry attempts (see §4) | 3 failed retries |
| IMU dropout | I2C NACK ×3 | none | encoder-only odom, disable tilt safety → halve speed | sensor re-init succeeds | 3 failed re-inits |
| Battery < 9.6 V (3S) | range check, 5 s persist | none | limp home at 50% speed, disable aux loads | never (needs charge) | < 9.0 V → safe-stop NOW (over-discharge kills LiPo) |
| Loop overrun > 2× | measured dt | skip derivative term this cycle | reduce logging rate | dt nominal for 1 s | persistent → reboot via WDT |
| Brown-out detected | MCU BOR flag at boot | — | — | — | log + check wiring: usually shared motor/logic supply, add bulk cap ≥ 470 µF + separate regulator |
| Tilt > 30° | IMU accel | motors off (latched) | none | operator only | always |
| MCU watchdog reset | reset-reason register | safe outputs at boot (see §6) | boot into SAFE mode, not NOMINAL | operator or supervisor clears | 2 WDT resets in 5 min → stay down |

Rules for building the matrix:
- **One row per fault, one unambiguous response.** If you find yourself writing "depends", split the row.
- Faults compose: define mode precedence `SAFE_STOP > DEGRADED > NOMINAL`. Multiple simultaneous degradations → take the most conservative action of each affected subsystem, and if ≥ 2 sensor classes are degraded simultaneously, escalate to SAFE_STOP (you no longer have cross-check redundancy).
- Degraded modes must be *tested states*, not emergent behavior. If you've never driven the robot on encoder-only odometry, it's not a degraded mode — it's a hope.

## 4. Auto-Recovery vs Operator Escalation

Decision rule: **auto-recover only faults that are (a) transient by nature, (b) verifiable as cleared, and (c) safe to retry.** Everything else escalates.

| Auto-recover | Escalate to operator |
|---|---|
| Comms blip < 30 s | Any latched safety fault (tilt, e-stop, runaway) |
| Sensor re-init (I2C device reset) | Hardware faults (dead encoder, burned driver) |
| Transient stall (debris) — bounded retries | Repeated faults (same fault 3× in 5 min) |
| Single WDT reset | Two WDT resets in 5 min |
| Loop overrun | Battery critical |

### Bounded retry with backoff (stall recovery)

```python
class StallRecovery:
    """Reverse briefly, then retry forward. Max 3 attempts, then escalate."""
    MAX_ATTEMPTS = 3
    def __init__(self):
        self.attempts = 0
        self.state = 'IDLE'
        self.t0 = 0

    def on_stall(self, now_ms):
        if self.attempts >= self.MAX_ATTEMPTS:
            return 'ESCALATE'           # operator: persistent mechanical jam
        self.attempts += 1
        self.state, self.t0 = 'BACKOFF', now_ms
        return 'RECOVERING'

    def tick(self, now_ms, motor):
        if self.state == 'BACKOFF':
            motor.set_duty(-0.4)        # reverse gently
            if now_ms - self.t0 > 300:  # 300 ms reverse
                self.state, self.t0 = 'COOLDOWN', now_ms
                motor.set_duty(0)
        elif self.state == 'COOLDOWN':
            # let windings cool; stall current heats fast. Backoff doubles.
            if now_ms - self.t0 > 500 * (2 ** self.attempts):
                self.state = 'RETRY'
        elif self.state == 'RETRY':
            self.state = 'IDLE'
            return 'RETRY_NOW'
        return None

    def on_success(self):
        self.attempts = 0               # decay attempts only on verified success
```

Non-negotiables for auto-recovery:
- **Recovery actions are state machines, not blocking sleeps.** `time.sleep(2)` inside a recovery handler freezes the safety loop — the exact thing your watchdog should catch (and will, causing a reset mid-recovery).
- **Verify recovery before declaring it.** After re-initializing an I2C IMU, read WHO_AM_I and one valid sample before clearing the fault. (MPU-6050 WHO_AM_I = 0x68, BNO055 CHIP_ID = 0xA0 at reg 0x00, ICM-20948 = 0xEA.)
- **Latch safety faults.** Tilt, e-stop, and runaway faults clear only by explicit operator action (button, command), never by the condition merely going away — a robot lying on its side reads "level-ish" and would otherwise reactivate its motors.
- **No lurching on link recovery.** Resume motion only after receiving a zero-velocity command post-recovery (operator must "re-arm" by releasing sticks).
- **Crash-loop protection.** Persist a reset counter (RTC memory on ESP32: `machine.RTC().memory()`; EEPROM on AVR). ≥ 2 watchdog resets within 5 min → boot into SAFE mode (comms + diagnostics only, actuators disabled) and wait for operator.

### Escalation must be observable

A robot that safe-stops silently in a corner is a failed escalation. Minimum operator-visible signals, cheapest first:
1. Status LED pattern: solid = nominal, slow blink (1 Hz) = degraded, fast blink (5 Hz) = faulted, off = no power/dead MCU. Use distinct patterns — brightness differences are invisible outdoors.
2. Buzzer: 3 beeps on entering SAFE_STOP. Costs $0.30, saves hours.
3. Telemetry fault word: a uint32 bitmask of active faults in every telemetry packet. The operator UI decodes bits to names. Never send only a boolean "fault=true".
4. Persistent fault log: ring buffer of (timestamp, fault_id, key sensor values at trip) in flash/EEPROM/SD. Post-incident analysis is impossible without the values *at the moment of the trip*.

## 5. Post-Incident Workflow

When a fault occurred in the field, follow this order. Skipping step 1 destroys evidence.

1. **Preserve state before power-cycling.** Dump the fault log, reset-reason register, and last N seconds of telemetry. On ESP32, RTC memory survives soft reset but NOT power cycle — flush to flash in the fault handler if at all possible (but never block the safety loop to do it; queue it).
2. **Reconstruct the timeline.** Order: last nominal telemetry → first anomalous sensor value → detection trip → response action → final state. The gap between "first anomalous value" and "detection trip" is your detection latency; if it's long, your thresholds/persistence are too loose.
3. **Classify**: true fault correctly handled / true fault mishandled / false positive / missed fault (found by damage, not by detector).
4. **Root cause, not proximate cause.** "Motor stalled" is proximate. "Wheel bearing seized because the mount lets grit in" is root. For electrical gremlins, the usual suspects in order: connectors (intermittent crimps), shared grounds (motor current through logic ground return), brown-outs (motor inrush sagging the 3.3 V rail — scope it, a multimeter averages it away), EMI on long unshielded encoder lines (twist them, add 1 nF to ground at the MCU end).
5. **Add or tune a detector.** Every missed fault gets a new detection rule. Every false positive gets a threshold/persistence adjustment — with the change justified by logged residual statistics, not by "felt too sensitive".
6. **Add a regression chaos test** (§7) that reproduces the fault. The incident isn't closed until the injected fault is detected and handled in test.
7. **Update the fault matrix** (§3). The matrix is the living spec; code implements it.

## 6. Safe-State Engineering (what "stop" actually means)

- **Safe outputs at boot, in hardware.** MCU GPIOs float/input during reset and bootloader — a floating EN pin can turn a motor driver ON during the ~1–2 s of boot. Add pull-downs (10 kΩ) on every driver enable/PWM line so the hardware default is OFF, independent of firmware. This is the most common cause of "robot twitches on power-up."
- **Two independent stop paths.** Software path: duty = 0. Hardware path: driver EN/INH pin driven low, or better, a relay/MOSFET on motor power controlled by the safety logic. A latched-up H-bridge ignores PWM; only the power path saves you.
- **Brake vs coast is a design decision.** H-bridge low-side-both-on = brake (use for slopes/arms under gravity); all-off = coast (use when braking torque itself is dangerous, e.g., high-speed wheels). For vertical axes, "stop" requires a mechanical brake or self-locking gearing — torque-off drops the load.
- **E-stop is normally-closed (NC), in series with motor power.** NC so that a broken wire = stop (fail-safe). A software-polled NO button is not an e-stop.
- **Sequenced shutdown:** zero velocity command → wait for measured velocity ≈ 0 (or 500 ms timeout) → disable drivers → log. Cutting driver power at speed dumps regenerative current back into the supply; with a LiPo that's fine, with a bench supply it overvolts the rail (add a TVS or brake resistor if on a PSU).

## 7. Chaos Testing (fault injection)

If you haven't injected the fault, the handler doesn't work. Test in this order: bench with wheels off ground → tethered → free.

**Hardware injection (cheap and brutally effective):**
- Pull the I2C/SPI sensor's power or SDA mid-run (use a toggle switch inline). Expect: dropout detected within max_hold samples, degraded mode entered, no crash, no garbage values reaching control.
- Disconnect one encoder channel. Expect: encoder-fault detection via current residual within 200 ms.
- Grab the wheel (gloves) to force a stall. Expect: PWM cut within 100 ms, bounded retries, escalation after 3.
- Kill the RF link (power off transmitter / `wifi.disconnect()` on the peer). Expect: motion stops within timeout, clean re-arm behavior, no lurch.
- Sag the supply: insert a 1 Ω power resistor in series and command full throttle. Expect: brown-out either ride-through (bulk caps) or detected-and-logged BOR, never silent corruption.

**Software injection — build it in, behind a flag:**

```python
# Fault injection shim — wraps any sensor read. Enabled only when
# CHAOS=1; compiled/configured out in production builds.
import random, time

class ChaosSensor:
    MODES = ('none', 'dropout', 'stuck', 'spike', 'drift', 'latency')
    def __init__(self, real_read):
        self.read_real = real_read
        self.mode = 'none'
        self.stuck_val = None
        self.drift = 0.0

    def read(self):
        x = self.read_real()
        if self.mode == 'dropout':  return None
        if self.mode == 'stuck':
            if self.stuck_val is None: self.stuck_val = x
            return self.stuck_val
        if self.mode == 'spike' and random.random() < 0.02:
            return x * 10
        if self.mode == 'drift':
            self.drift += 0.001
            return x + self.drift
        if self.mode == 'latency':
            time.sleep_ms(15)            # simulate a slow bus transaction
            return x
        return x
```

**ROS 2 chaos:** kill nodes (`ros2 lifecycle set /node shutdown`, or plain `kill -9`), delay topics (republish through a node with `sleep`), drop messages (relay that forwards 70%), corrupt clocks (publish skewed `/clock` in sim). Verify the supervisor's diagnostics reflect each injection and `/cmd_vel_safe` stays sane.

**Chaos test acceptance criteria — for every row of the fault matrix:**
1. Detected within the stated latency budget.
2. Stated immediate action occurred (verify via telemetry log, not eyeballs).
3. Correct mode entered; mode visible on LED/telemetry.
4. Auto-recovery happened iff the matrix says so, with no lurch.
5. Fault logged with timestamp and trip values.
6. System never emitted garbage actuator commands during the transition (log commanded duty around the event and inspect).

Run the full injection suite after ANY change to the safety loop, thresholds, or comms stack. Keep it as a checklist script.

## 8. Debugging Checklist (fault system misbehaving)

**False positives (faults that aren't real):**
- [ ] Persistence counter present? Single-sample thresholds trip on noise.
- [ ] Hysteresis on clear? Chattering fault flags look like repeated faults.
- [ ] Using measured dt in rate checks? Loop jitter + nominal dt = false spikes.
- [ ] Heartbeat timeout ≥ 3 periods? 1-period timeouts false-trip on WiFi/RF constantly.
- [ ] ROS 2: QoS compatible (`ros2 topic info -v`)? Reliability/durability mismatch = silent non-connection misdiagnosed as dead node.
- [ ] Threshold derived from logged good-run statistics (3–5σ) or guessed?
- [ ] Sensor shares I2C bus with a slow device (e.g., OLED display)? Display refresh blocking the bus mimics sensor dropout. Move display to second bus or update it less often.

**Missed faults (damage found, detector silent):**
- [ ] Stuck-at detector present on every analog channel?
- [ ] Plausibility checks on RAW values, before filtering?
- [ ] Current sensing actually wired on the actuator that failed?
- [ ] WDT fed from the real control loop, not an ISR/feeder task?
- [ ] Fault checked in all modes? (Common: stall detection only ran in autonomous mode, robot burned a motor in teleop.)

**Recovery misbehaving:**
- [ ] Recovery handler non-blocking? Blocking recovery starves the safety loop.
- [ ] Retry counter bounded AND only reset on *verified* success?
- [ ] Safety faults latched? Re-arm requires explicit operator action?
- [ ] Reset-reason checked at boot, crash-loop counter persisted?
- [ ] Pull-downs on driver EN/PWM pins (no boot twitch)?
- [ ] Mode precedence enforced when multiple faults are active?

**Comms faults:**
- [ ] CRC on every UART/RF packet (not XOR)?
- [ ] Sequence numbers — duplicates/stale rejected?
- [ ] Staleness judged by sender timestamp, not arrival time?
- [ ] CAN: 120 Ω termination at BOTH physical ends (measure ~60 Ω across CANH–CANL, power off)? Error counters monitored before bus-off?

## 9. Minimal Viable Fault System (if you build nothing else)

For any robot with motors, ship at minimum:
1. Hardware WDT (2–4 s), fed from the main loop only after verifying loop health.
2. Comms failsafe: motors stop within 300 ms of last valid command.
3. Per-motor stall detection: current + encoder (or current + time-at-full-duty if no encoder: full duty > 2 s with no progress = treat as stall).
4. Battery undervoltage: degrade at 3.5 V/cell, hard-stop at 3.2 V/cell (LiPo, under load).
5. Pull-downs on all driver enable pins; NC e-stop in the motor power path.
6. Reset-reason logging + fault bitmask in telemetry.

This covers ~80% of field failures (comms loss, stalls, dead batteries, firmware hangs) with ~150 lines of code and two resistors.
