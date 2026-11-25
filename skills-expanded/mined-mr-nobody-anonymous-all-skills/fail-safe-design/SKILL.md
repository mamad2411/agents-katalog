---
name: fail-safe-design
description: "Use when designing or reviewing robot firmware/software that must fail safely — watchdogs, command timeouts, actuator safe states, sensor plausibility, startup self-test, brownout persistence. Provides exact timing budgets, register-level WDT setup for AVR/ESP32/STM32, deadman patterns for MicroPython/Arduino/ROS2, per-actuator safe-state tables, and the failure modes that injure people or destroy hardware when missed."
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


# Fail-Safe Design for Robots

The core principle: **a robot must be safe when the software is wrong, not just when it is right.** Every fail-safe layer assumes the layer above it has already failed. Design order: (1) what happens when power dies, (2) what happens when the MCU hangs, (3) what happens when commands stop arriving, (4) what happens when a sensor lies, (5) only then — normal operation.

## 1. The Layered Fail-Safe Stack

```
Layer 0  Hardware: E-stop relay, fuses, current-limited supply, mechanical end stops
Layer 1  Hardware watchdog (independent oscillator) → MCU reset
Layer 2  Task/loop monitors (software watchdog per task) → safe-state then reset
Layer 3  Command deadman timeout (100–200 ms) → actuators to safe state
Layer 4  Sensor plausibility (range/rate/cross checks) → degrade or stop
Layer 5  Startup self-test → refuse to arm if anything fails
```

Rule: **each layer must not depend on any higher layer working.** The HW watchdog must run from its own clock (it does on ESP32 RTC_WDT, AVR WDT 128 kHz ULP osc, STM32 IWDG LSI ~32 kHz). The E-stop must be a physical relay/contactor in the motor power path, never a GPIO read by software.

### E-stop wiring (Layer 0) — normally-closed loop

| Signal | Wiring | Why |
|---|---|---|
| E-stop button | NC contacts in series with motor contactor coil | Broken wire = stop (fail-open is fail-safe) |
| Contactor coil | 12/24 V through E-stop loop; MCU enables via low-side MOSFET *in series*, never in parallel | Both software AND human must agree to enable |
| MCU enable pin | External pull-down 10 kΩ | MCU in reset/brownout = pin floats low = motors off |
| Motor power | Through contactor main contacts, fused at 1.5× stall current | Software cannot override |

Mistake everyone makes: wiring E-stop to an MCU input and handling it in software. That is a *status input*, not an E-stop. The button must physically break motor power.

## 2. Hardware Watchdog (Layer 1)

### Timing budget

| Loop type | Loop period | WDT timeout | Feed point |
|---|---|---|---|
| Motor control (PID) | 1–10 ms | 50–100 ms | End of control loop, AFTER outputs written |
| Mobile robot main loop | 10–50 ms | 200–500 ms | End of main loop |
| Slow supervisor (telemetry) | 100–1000 ms | 2–8 s | After all health checks pass |

Rules:
- Timeout = 5–10× worst-case loop period. Tighter trips on legitimate jitter (WiFi stack, GC in MicroPython); looser leaves actuators live too long. A robot at 1 m/s travels 10 cm per 100 ms — size the timeout from stopping distance, not convenience.
- **Feed in exactly ONE place**, at the end of the main loop, only after verifying the loop actually did its work. Never feed in a timer ISR — an ISR keeps running when main code is hung, which defeats the entire watchdog. This is the single most common watchdog mistake.
- Never feed inside a `while` wait loop ("feed so it doesn't reset while I wait for the sensor"). If a sensor wait can exceed the WDT period, your architecture is wrong — make it non-blocking.
- On reset, READ the reset cause and refuse to auto-arm after a WDT reset (require explicit re-arm or log + count; 3 WDT resets in 60 s → lockout).

### ESP32 (MicroPython)

```python
from machine import WDT, reset_cause, WDT_RESET
import machine

# Check why we booted BEFORE enabling anything
if machine.reset_cause() == machine.WDT_RESET:
    boot_count = read_wdt_counter() + 1          # persisted, see §7
    write_wdt_counter(boot_count)
    if boot_count >= 3:
        enter_lockout_mode()                      # LEDs blink error, motors never armed
else:
    write_wdt_counter(0)

wdt = WDT(timeout=200)   # ms; min 1000 ms on some ports — check; ESP32 port allows lower via TWDT

while True:
    t0 = time.ticks_ms()
    run_control_loop()        # read sensors, compute, write actuators
    if loop_healthy():        # all subtasks reported in (see §3)
        wdt.feed()
    # if not healthy: do NOT feed → HW reset in <=200 ms
    # pace the loop
    dt = time.ticks_diff(time.ticks_ms(), t0)
    time.sleep_ms(max(0, 10 - dt))
```

Note: MicroPython `WDT` cannot be disabled once started (by design). On the ESP32 there are actually three watchdogs: RTC_WDT (bootloader), TWDT (task WDT, what `machine.WDT` uses), and INT_WDT. The TWDT default panics rather than resets in ESP-IDF — in Arduino/IDF C++ configure it explicitly:

### ESP32 (Arduino C++ / ESP-IDF)

```cpp
#include "esp_task_wdt.h"

void setup() {
  esp_task_wdt_config_t cfg = {
    .timeout_ms = 200,
    .idle_core_mask = 0,          // don't watch idle tasks
    .trigger_panic = true,        // panic → reset, gets reset reason ESP_RST_TASK_WDT
  };
  esp_task_wdt_reconfigure(&cfg); // (init already done by Arduino core)
  esp_task_wdt_add(NULL);         // subscribe current task (loopTask)

  esp_reset_reason_t r = esp_reset_reason();
  if (r == ESP_RST_TASK_WDT || r == ESP_RST_WDT || r == ESP_RST_BROWNOUT) {
    handle_unclean_boot(r);       // do not auto-arm
  }
}

void loop() {
  run_control_loop();
  if (loop_healthy()) esp_task_wdt_reset();
}
```

### AVR (Arduino Uno/Nano/Mega)

```cpp
#include <avr/wdt.h>

// CRITICAL on old bootloaders (Nano w/ ATmegaBOOT): WDT stays enabled at 15 ms
// after reset → infinite reset loop. Disable ASAP in early init:
void wdt_first_thing(void) __attribute__((naked, used, section(".init3")));
void wdt_first_thing(void) {
  MCUSR = 0;            // must clear WDRF before WDT can be disabled
  wdt_disable();
}
// (Optiboot handles this for you; ATmegaBOOT does not. Know your bootloader.)

void setup() {
  // ... self-test (§6) ...
  wdt_enable(WDTO_120MS);   // options: 15,30,60,120,250,500MS, 1,2,4,8S
}

void loop() {
  run_control_loop();
  if (loop_healthy()) wdt_reset();
}
```

AVR gotcha: `wdt_enable()` timeouts are from a 128 kHz oscillator with ±10% tolerance and Vcc/temperature drift — never design a 100 ms loop against `WDTO_120MS`; use `WDTO_250MS` or restructure.

### STM32 (IWDG)

```c
// IWDG: independent LSI clock (~32 kHz ±~47% across temp on F1! F4 is tighter).
// Cannot be stopped once started except by reset. Freeze in debug:
__HAL_DBGMCU_FREEZE_IWDG();

IWDG_HandleTypeDef hiwdg = {
  .Instance = IWDG,
  .Init = { .Prescaler = IWDG_PRESCALER_32,   // 32 kHz/32 = 1 kHz tick
            .Reload = 200 }                    // ≈200 ms
};
HAL_IWDG_Init(&hiwdg);
// feed: HAL_IWDG_Refresh(&hiwdg);
// reset cause: __HAL_RCC_GET_FLAG(RCC_FLAG_IWDGRST); then __HAL_RCC_CLEAR_RESET_FLAGS();
```

Use WWDG (window watchdog) in addition if you must also catch *too-fast* loops (runaway that skips work but still feeds). Window watchdogs catch the "ISR feeds the dog" failure class.

## 3. Task Monitors / Software Watchdog (Layer 2)

The HW WDT only proves the main loop spins. It does NOT prove the IMU task, the comms task, or the motor task did anything. Pattern: each task sets a flag/timestamp; the main loop checks ALL of them before feeding.

```python
# MicroPython — checkin table pattern
import time

class TaskMonitor:
    def __init__(self):
        self.tasks = {}          # name -> (deadline_ms, last_checkin)

    def register(self, name, deadline_ms):
        self.tasks[name] = [deadline_ms, time.ticks_ms()]

    def checkin(self, name):
        self.tasks[name][1] = time.ticks_ms()

    def all_alive(self):
        now = time.ticks_ms()
        for name, (deadline, last) in self.tasks.items():
            if time.ticks_diff(now, last) > deadline:
                log("TASK DEAD:", name)
                return False
        return True

mon = TaskMonitor()
mon.register("imu",   50)    # IMU must read every 50 ms
mon.register("cmd",  200)    # command receiver, see §5
mon.register("motor", 20)

# in each task / handler:  mon.checkin("imu")
# in main loop:            if mon.all_alive(): wdt.feed()
#                          else: safe_state_all(); (don't feed → HW reset)
```

Sequence on task failure: **safe-state the actuators FIRST, then stop feeding.** Letting the WDT reset with motors still commanded means motors run at last PWM for the full WDT timeout + reset + reboot time (easily 500 ms–2 s). Always:

```python
if not mon.all_alive():
    safe_state_all()      # immediate, takes <1 ms
    while True: pass      # spin until HW WDT resets us
```

ROS 2 equivalent: each node publishes a heartbeat or use lifecycle nodes + `diagnostic_updater`; a safety node subscribes with a deadline QoS and drops the enable line via hardware on `DEADLINE_MISSED`:

```python
qos = QoSProfile(depth=1,
                 deadline=Duration(seconds=0.2),
                 reliability=ReliabilityPolicy.RELIABLE)
self.sub = self.create_subscription(Twist, 'cmd_vel', self.cb, qos,
              event_callbacks=SubscriptionEventCallbacks(
                  deadline=self.on_deadline_missed))
```

Don't reinvent this in ROS 2 — deadline QoS exists precisely for deadman detection, and it triggers even when zero messages ever arrive (a plain "check timestamp of last msg" misses the never-connected case if you initialize the timestamp to now).

## 4. Per-Actuator Safe State (the brake/coast/hold decision)

"Stop the motors" is not one thing. Choosing wrong is itself a hazard.

| Actuator | Safe state | How | Why / hazard if wrong |
|---|---|---|---|
| Drive motors (wheeled, flat ground) | **Brake** (short windings) | H-bridge: both low-side ON (or both high). PWM=0 + IN1=IN2=LOW on DRV8833/TB6612 = coast; IN1=IN2=HIGH = brake. Check YOUR driver's table. | Coast on a slope = robot rolls away |
| Drive motors (high speed >2 m/s) | Coast, then brake below threshold | Ramp or speed-gated brake | Hard brake at speed = tip-over, wheel lock skid |
| Hobby servo (arm joint, gripper) | **Hold** last position, then ramp to safe pose | Keep sending last pulse; do NOT stop PWM | Cutting servo PWM = goes limp = arm falls on someone. But a stalled/obstructed servo held forever overheats — ramp to rest pose within ~2 s |
| Servo (continuous rotation) | Stop pulse = 1500 µs exactly | Calibrate; many stop at 1480–1520 µs | "No signal" ≠ stop on some CR servos — they hold last speed |
| BLDC via ESC (drone) | **Motors OFF / disarm** | Send min throttle (1000 µs) or ESC disarm | A drone must never "hold" — it must stop props. Failsafe-RTL is flight-controller territory, not yours |
| BLDC via ESC (e-bike/rover) | Coast (throttle 0), never disarm mid-motion | 1500 µs neutral for bidirectional ESCs | Disarm at speed = loss of regen/brake control |
| Stepper (gantry, no gravity load) | De-energize (driver ENABLE off) | EN pin high (active-low on A4988/DRV8825/TMC) | Holding current cooks steppers + drivers in a fault state |
| Stepper (Z-axis, gravity load) | Keep energized at reduced current, or mechanical brake | TMC: reduce IHOLD; or spring-applied brake | De-energize = Z crashes down |
| Linear actuator w/ lead screw | De-energize (self-locking) | Most ACME lead screws back-drive < few % efficiency | Free — use this; it's the only truly passive hold |
| Pneumatic | Vent (3/2 NC valve) or hold (5/3 closed-center) — application dependent | Choose valve type at design time | Venting a vertical cylinder drops the load; holding traps energy for maintenance staff |
| Heater | OFF, always | Relay/SSR open, fail-open thermal fuse in series | No exceptions |
| Gripper holding a load | **Hold** | Maintain grip force | Opening = drops the payload (possibly on a hand) |

Implementation rule: write `safe_state()` per actuator as the FIRST function in each driver module, callable from any context (no allocation, no locks, no I2C transactions that can block — if the actuator is on an I2C GPIO expander, you've designed wrong; enable lines belong on direct GPIO).

```cpp
// Arduino — TB6612FNG drive pair, brake safe-state
void drive_safe_state() {
  // brake: both inputs HIGH, PWM full
  digitalWrite(AIN1, HIGH); digitalWrite(AIN2, HIGH); analogWrite(PWMA, 255);
  digitalWrite(BIN1, HIGH); digitalWrite(BIN2, HIGH); analogWrite(PWMB, 255);
  digitalWrite(STBY, HIGH);   // STBY low would coast — keep high for brake
}
```

GPIO power-up state matters: on reset, MCU pins float as inputs until your code runs (tens of ms on ESP32, longer with bootloader delays). **Every motor driver enable/PWM line needs an external pull resistor that selects the safe state** (e.g., 10 kΩ pull-down on PWM and enable). ESP32 strapping pins (0, 2, 5, 12, 15) glitch at boot — never put a motor enable on them. AVR pins are inputs (hi-Z) after reset; ESP32 GPIO1/3 are UART and will toggle during boot logging.

## 5. Command Deadman Timeout (Layer 3)

Every remotely commanded robot stops when commands stop. **Timeout: 100–200 ms** for ground robots at human-interaction speed; scale by stopping distance: `timeout ≤ (allowed_overrun_m / max_speed_mps) − actuator_stop_latency`.

| Link | Typical cmd rate | Recommended timeout |
|---|---|---|
| Local UART/RC PWM | 50 Hz (20 ms) | 100 ms (5 missed frames) |
| WiFi UDP teleop | 20–50 Hz | 150–200 ms |
| BLE | 10–20 Hz | 250–300 ms (connection interval jitter) |
| ROS 2 /cmd_vel over WiFi | 10–30 Hz | 200 ms (deadline QoS) |

Rules:
- Timeout on **command messages**, not on the TCP connection. TCP stays "connected" for minutes after WiFi drops (until keepalive). UDP + sequence numbers + timestamps beats TCP for teleop precisely because silence is detectable.
- The sender must stream commands continuously (even "same as before"), so silence is unambiguous. A protocol where "no message = keep doing last thing" cannot have a deadman.
- Reject stale/reordered packets: include a `seq` (uint16, wrap-aware compare) and drop `seq <= last_seq` (mod 65536, window 32768).
- On timeout: go to safe state AND require fresh non-zero-age command to resume. Do not latch into estop requiring reboot (operators will hate it and bypass it) — auto-resume on command resumption is fine for velocity-class commands; require explicit re-arm for anything energetic.
- Zero-velocity is not safe-state. Apply the §4 table (brake vs coast), don't just command 0 and hope.

```python
# MicroPython — UDP teleop receiver with deadman
import socket, struct, time

CMD_TIMEOUT_MS = 150
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 4210))
sock.setblocking(False)

last_cmd_ms = -CMD_TIMEOUT_MS      # start EXPIRED — no motion until first cmd
last_seq = -1
vx = wz = 0.0

def poll_commands():
    global last_cmd_ms, last_seq, vx, wz
    while True:                     # drain socket, keep newest
        try:
            pkt, _ = sock.recvfrom(64)
        except OSError:
            break                   # EAGAIN — empty
        if len(pkt) != 12: continue
        seq, nvx, nwz = struct.unpack('<Hxxff', pkt)
        if last_seq >= 0 and ((seq - last_seq) & 0xFFFF) > 0x7FFF:
            continue                # stale/reordered
        last_seq = seq
        vx, wz = nvx, nwz
        last_cmd_ms = time.ticks_ms()
        mon.checkin("cmd")

def control_step():
    if time.ticks_diff(time.ticks_ms(), last_cmd_ms) > CMD_TIMEOUT_MS:
        drive_safe_state()          # brake (per §4)
        return
    drive_set(clamp(vx, -VX_MAX, VX_MAX), clamp(wz, -WZ_MAX, WZ_MAX))
```

Critical detail: initialize `last_cmd_ms` to *expired*, not `now`. Initializing to boot time gives the robot a free 150 ms window to act on garbage at startup.

ROS 2: prefer deadline QoS (§3 snippet) plus a `twist_mux` with a timeout per source, or `joy_teleop`'s built-in deadman button. The deadman BUTTON (operator must hold a button for motion) is a separate, additive mechanism — implement it on the *sender*, and have the sender stream zero-velocity (not silence) when released, so you can distinguish "operator released" from "link dead".

## 6. Startup Self-Test (Layer 5)

Refuse to arm unless ALL pass. Order matters — test the safety mechanisms before the things they protect.

```
POST sequence (target < 3 s total):
 1. Reset-cause check        → WDT/brownout reset? apply policy (§2, §7)
 2. Supply rail check        → ADC on Vbat through divider; reject < cell_min
                               (3.3 V/cell LiPo load-sag floor; 3.5 V resting)
 3. Watchdog test (optional, first-boot/factory only): deliberately hang,
    verify reset occurs, set "wdt-verified" flag in NVS
 4. Sensor presence          → I2C: probe addresses (expect ACK); SPI: read
                               WHO_AM_I (MPU6050: 0x75→0x68; BNO055 CHIP_ID:
                               0x00→0xA0; BMI160: 0x00→0xD1)
 5. Sensor sanity            → IMU stationary: |accel| = 9.81 ±1.5 m/s²,
                               |gyro| < 3 °/s; if violated: robot moving or
                               sensor broken — either way don't arm
 6. Encoder/motor loopback   → pulse motor 5% PWM for 50 ms, expect encoder
                               counts ≠ 0 and correct sign. Catches swapped
                               wiring, dead driver, jammed mech. SKIP on
                               robots where any motion at boot is hazardous.
 7. E-stop circuit check     → read E-stop status input: must be RELEASED;
                               if your contactor has an aux contact, verify
                               it opens when enable is dropped
 8. Comms check              → link up + first valid command structure seen
                               (do not require this for autonomous robots)
 9. ARM                      → only now energize the enable line
```

Failures: blink count on status LED + log over serial + (if comms up) telemetry message naming the failed step. A robot that fails POST silently gets power-cycled in frustration until someone bypasses the test.

```cpp
// Arduino — I2C presence + WHO_AM_I pattern
bool check_imu() {
  Wire.beginTransmission(0x68);
  if (Wire.endTransmission() != 0) return fail("IMU no ACK");
  Wire.beginTransmission(0x68); Wire.write(0x75); Wire.endTransmission(false);
  Wire.requestFrom(0x68, 1);
  if (!Wire.available() || Wire.read() != 0x68) return fail("IMU bad WHO_AM_I");
  return true;
}
```

Also set `Wire.setWireTimeout(3000, true)` (AVR core ≥1.8.13) or equivalent — a stuck I2C slave holding SDA low otherwise hangs `endTransmission()` forever, and you learn why the HW WDT was Layer 1. Bus recovery: clock SCL manually 9 times with SDA released, then STOP.

## 7. Sensor Plausibility (Layer 4)

Three checks per sensor, cheap and ordered:

**Range check** — physically possible values:

| Sensor | Valid range | Reject also |
|---|---|---|
| MPU6050 accel (±2g cfg) | ±19.6 m/s² | exactly 0x0000 or 0xFFFF raw (bus failure reads) |
| Gyro (±250 °/s cfg) | ±250 °/s | constant nonzero at rest > 5 °/s (bias broke) |
| HC-SR04 ultrasonic | 0.02–4.0 m | timeout (no echo) ≠ "4 m clear" — it's UNKNOWN |
| VL53L0X ToF | 0.03–2.0 m | status ≠ 0 in result struct (signal/sigma fail) |
| Wheel encoder velocity | ≤ motor free speed × wheel circ. | — |
| NTC thermistor | −20…+120 °C | open (ADC≈max) or short (ADC≈0) — broken wire |
| Battery ADC | 2.5–4.35 V/cell | step > 0.5 V between reads (divider fault) |

**Rate check** — max physical change per sample: `|x[k] − x[k−1]| ≤ max_slew × dt`. A 1 kg robot can't change velocity 5 m/s in 10 ms. Temperature can't move 10 °C in 100 ms. Trip → discard the SAMPLE (hold last good), not the sensor; trip N=5 consecutive → declare sensor failed.

**Cross check** — independent sources must agree:
- Encoder velocity vs integrated IMU accel: disagree > threshold for > 300 ms → wheels slipping OR encoder failed OR robot picked up. All three mean: stop.
- Commanded PWM vs measured current: PWM 80%, current ≈ 0 → open motor wire. PWM 0, current > 0.5 A → shorted driver FET (this one is on FIRE-path: kill the contactor, not just PWM).
- Left vs right range sensor overlap region; dual thermistors on one heater (±5 °C agreement).
- Stall detection: commanded speed > 0.2 m/s, encoder counts = 0 for 500 ms → stalled. Cut drive; current limit alone lets a stalled motor cook at exactly the limit.

```python
class PlausibleSensor:
    def __init__(self, lo, hi, max_slew_per_s, max_strikes=5):
        self.lo, self.hi, self.slew = lo, hi, max_slew_per_s
        self.max_strikes = max_strikes
        self.strikes = 0
        self.last = None
        self.last_t = None
        self.failed = False

    def update(self, x, t_ms):
        if self.failed: return None
        ok = self.lo <= x <= self.hi
        if ok and self.last is not None:
            dt = time.ticks_diff(t_ms, self.last_t) / 1000
            ok = abs(x - self.last) <= self.slew * dt + 1e-9
        if ok:
            self.strikes = 0
            self.last, self.last_t = x, t_ms
            return x
        self.strikes += 1
        if self.strikes >= self.max_strikes:
            self.failed = True            # latched until re-POST
        return self.last                  # hold last good value
```

Policy on sensor failure: **degrade by capability, don't binary-stop everything.** Range sensor dead → speed cap to creep (0.1 m/s) if bump sensors still work, else stop. IMU dead on a balancing robot → that IS the stop. Encode the policy as a table, not scattered ifs.

The mistake everyone makes: filtering before checking. Run plausibility on RAW samples. A complementary/Kalman filter fed one 0xFFFF glitch smears it over seconds and the rate check downstream never fires.

## 8. Brownout-Safe Persistence

Brownout corrupts flash writes; flash writes during brownout corrupt entire sectors. The two interact: your "log the fault then die" code is the thing most likely to run during a brownout.

- **Enable the brownout detector** and set it ABOVE the flash-write minimum: AVR fuse BOD 4.3 V for 5 V boards (default is often disabled!); ESP32 default ~2.43 V is too low for SD writes — config to 2.8 V+ (`CONFIG_ESP_BROWNOUT_DET_LVL`); STM32 PVD interrupt at ~2.9 V gives you an early-warning window before BOR at 2.7 V.
- **Order of operations in the PVD/early-warning ISR:** kill motor enable (biggest load — buys you milliseconds of hold-up), THEN write the crash record. Bulk capacitance: 1000 µF on the logic rail ≈ tens of ms hold-up at MCU-only load.
- **Separate logic and motor supplies** or at minimum a diode + bulk cap island for the MCU. Motor stall transient sagging Vcc → MCU brownout-resets → GPIO float → motors re-energize → sag again: the classic brownout boot-loop. The pull-downs from §4 are what break this loop.
- **Persist with atomicity**: two slots + sequence number + CRC. Write slot A, then B alternately; on boot take the slot with valid CRC and higher seq. Never overwrite your only copy.

```python
# MicroPython ESP32 — double-buffered NVS record
from esp32 import NVS
import struct

nvs = NVS("failsafe")

def save_record(wdt_count, fault_code):
    seq = (load_record()[0] if load_record() else 0) + 1
    blob = struct.pack('<IHH', seq, wdt_count, fault_code)
    crc = simple_crc16(blob)
    slot = "rec_a" if seq % 2 else "rec_b"
    nvs.set_blob(slot, blob + struct.pack('<H', crc))
    nvs.commit()                  # commit() is the actual flash write

def load_record():
    best = None
    for slot in ("rec_a", "rec_b"):
        try:
            buf = bytearray(10); nvs.get_blob(slot, buf)
        except OSError:
            continue
        seq, wdt, fault = struct.unpack('<IHH', buf[:8])
        if struct.unpack('<H', buf[8:])[0] == simple_crc16(buf[:8]):
            if best is None or seq > best[0]:
                best = (seq, wdt, fault)
    return best
```

- **Wear**: NVS/EEPROM endurance ~100k cycles (AVR EEPROM 100k, ESP32 NVS wear-levels across its partition). Writing a counter every loop at 100 Hz kills it in 17 minutes of cumulative writes. Write on EVENT (fault, state change), never on tick. For an odometer-style counter, RAM-accumulate and flush every N units or on PVD warning.
- The WDT-reset counter from §2 belongs here. Also persist: last fault code, last sensor-failed bitmap, total runtime. That record is the only witness when you're debugging a field unit that "just resets sometimes".
- AVR-specific: `EEPROM.update()` not `.write()` (skips identical bytes); EEPROM corruption address 0 is folklore-real on brownout — don't use address 0, or guard with BOD properly enabled.

## 9. Debugging Checklist — "the robot did something scary"

Work the list in order; each item is a 5-minute check.

1. **Reset counters**: read the persisted WDT/brownout counters (§8). Nonzero brownout count → power problem, stop looking at software.
2. **Scope the enable line at power-on**: any pulse > 1 µs on motor enable during boot = missing pull-down or strapping-pin conflict (§4).
3. **Pull the command sender's plug mid-motion**: robot must reach safe state within `CMD_TIMEOUT + 50 ms`. Time it with slow-mo phone video (240 fps = 4 ms resolution). If it keeps going: deadman is on the wrong layer (TCP?) or `last_cmd_ms` init bug (§5).
4. **Hang the main loop deliberately** (`while(1);` behind a test command): WDT must reset within its timeout AND the robot must not auto-rearm. If motors stay energized during the reset window → §3 ordering bug (safe-state before starving the dog).
5. **Disconnect each sensor live** (one at a time): plausibility layer must catch it in < 5 samples, robot degrades per policy. If the loop instead freezes → blocking I2C read without bus timeout (§6).
6. **Stall a wheel by hand** (gloves, low PWM): stall detect must cut drive in < 500 ms. Measure motor current — if it sits at the limiter value indefinitely, you have a heater, not a robot.
7. **Brownout test**: bench supply, ramp Vin down slowly through the BOD threshold and back up, 10 cycles. Robot must end every cycle in safe state with intact NVS. Then do it fast (yank power during a flash write loop).
8. **Check the feed sites**: `grep -rn "wdt.feed\|wdt_reset\|IWDG_Refresh" src/` — more than one hit outside the main loop is a finding. Any hit inside an ISR is a bug, full stop.
9. **Timing audit**: log loop dt max over 10 minutes including WiFi reconnect events. If `dt_max > WDT_timeout / 2`, you will get field resets that never reproduce on the bench.
10. **E-stop while driving**: physical button, full speed. Must stop mechanically (Layer 0) even with the MCU held in reset (jumper the reset pin to prove it).

## 10. Anti-Patterns (seen constantly, all wrong)

- Feeding the watchdog in a timer ISR or a FreeRTOS high-priority task that "always runs". The watchdog now proves only that the scheduler ticks.
- `try: ... except: pass` around the control loop in MicroPython. The exception you swallowed was the IMU bus dying; you're now integrating zeros into the Kalman filter.
- One global `ESTOP` boolean checked "everywhere". Race-prone, misses ISR paths, and software-only. Safe-state must be a function that forces hardware, called from a single supervisor.
- Deadman that resumes with the stale pre-timeout command instead of requiring a fresh one.
- Self-test that runs motors on a robot sitting on a workbench shelf. Gate motion tests on a "bench mode" jumper or wheels-off detection.
- `delay(500)` anywhere in a system with a 200 ms watchdog (works in the demo, resets in the field when two delays stack).
- Treating ultrasonic timeout as "max range, path clear". No echo means unknown; soft surfaces and angled walls eat pings.
- Calibrating the safe state at full battery only. Brake chopping duty, servo hold torque, and BOD margins all shift across the discharge curve — test at cell_min too.
- Logging to SD/flash inside the fault path without checking supply voltage first (§8).
- Believing the spec: AVR WDT ±10%, STM32F1 LSI 30–60 kHz, hobby ESC arming sequences vary by firmware. Measure your actual timeout with a scope once per design.

## Quick Reference Card

```
WDT timeout          = 5–10 × loop period (motor loops: 50–100 ms)
Feed location        = ONE place, end of main loop, after health checks, NEVER in ISR
Cmd deadman          = 100–200 ms; init expired; reject stale seq; brake per actuator table
Safe states          : drive=brake | servo arm=hold→ramp | ESC drone=disarm |
                       stepper(Z)=hold reduced current | heater=OFF | gripper=HOLD
Pull-downs           = every enable/PWM line, 10 kΩ, selects safe state at boot/reset
POST order           = reset-cause → battery → sensors WHO_AM_I → sanity → loopback → arm
Plausibility         = range → rate → cross, on RAW data, 5-strike latch, degrade by table
Persistence          = double-slot + seq + CRC, write on event not tick, BOD above flash-min
WDT-reset policy     = no auto-arm; 3 resets / 60 s → lockout
E-stop               = NC loop breaking motor power physically; MCU enable in SERIES
```
