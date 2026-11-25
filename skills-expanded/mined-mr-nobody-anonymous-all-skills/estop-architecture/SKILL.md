---
name: estop-architecture
description: "Use when designing or reviewing emergency stop systems for robots, CNC machines, mobile platforms, or any machine with hazardous motion. Provides IEC 60204-1 stop category selection (0/1/2), hardware E-stop chain design (software E-stop is NOT a safety function), dual-channel monitoring with safety relays, motor contactor cut wiring, latching+reset state machines, and wireless E-stop heartbeat patterns with exact wiring tables, timing constraints, and working MicroPython/Arduino/ROS2 code."
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


# E-Stop Architecture

## The One Rule That Overrides Everything

**The E-stop chain must remove hazardous energy WITHOUT any microcontroller, firmware, OS, or network in the path.** Software may *observe* the E-stop state, *report* it, and *manage recovery*, but the actual power cut goes: E-stop button → safety relay → contactor → motor power. If your design requires code to execute for the robot to stop, it is broken. Period.

Corollaries:
- A GUI "STOP" button is a *functional stop*, not an emergency stop. Keep it, but never count it toward safety.
- An E-stop wired to a GPIO pin that triggers `motor.stop()` in an ISR is a functional stop. The MCU can be hung, brown-out latched, or stuck in a flash-write critical section.
- PWM disable via firmware is not a safety stop. Cut the power stage.

## IEC 60204-1 Stop Categories

| Category | Definition | How energy is removed | Use when |
|----------|-----------|----------------------|----------|
| **Cat 0** | Uncontrolled stop — immediate removal of power to actuators | Contactor drops out instantly; motor coasts or mechanical brake engages | Small robots, low inertia, anywhere a coast-down is safe. Default choice. |
| **Cat 1** | Controlled stop — power available to brake, THEN power removed | Drive performs controlled deceleration; time-delay safety relay drops contactor after T (typ. 0.5–5 s) | High inertia (heavy arms, spindles, vertical axes with gravity loads) where free coast is MORE dangerous than powered braking |
| **Cat 2** | Controlled stop with power LEFT ON (standstill monitoring) | Drive holds position under power (e.g., SS2/SOS in servo drives) | NOT permitted for emergency stop. Only for operational/protective stops. |

**Emergency stop must be Category 0 or 1 (IEC 60204-1 §9.2.3.4.2). Never Category 2.**

Cat 1 implementation detail: use a time-delay safety relay (e.g., Pilz PNOZ s5, two delayed contact sets) or a safety relay with both instantaneous and delayed outputs. Instantaneous output → drive's "controlled stop" input (STO stays enabled, drive ramps down). Delayed output (set to ramp time + margin) → contactor coil / STO. The delay is a hard upper bound: even if the drive fails to decelerate, power dies at T.

Vertical/gravity axes: Cat 0 on a vertical axis means the load falls unless you have a spring-applied, power-released brake. Wire the brake coil through the SAME contactor that cuts motor power — power loss = brake engaged. Never control the safety brake from firmware alone.

## Performance Levels (quick selection)

| Risk | Standard target | Architecture |
|------|----------------|--------------|
| Hobby bench robot, <10 W motors, no one inside envelope | Single channel acceptable (still hardware chain) | 1 NC contact → relay/contactor |
| Workshop CNC, 3D printer with heaters, small cobot | PLd / SIL 2 typical | Dual channel + safety relay with cross-monitoring |
| Industrial robot cell, AGV among people | PLe / SIL 3 | Dual channel, certified safety relay or safety PLC, monitored contactors (mirror contacts), regular proof tests |

Risk assessment per ISO 12100; PL determination per ISO 13849-1. If people share space with >80 W of moving robot, do not ship a single-channel design.

## E-Stop Button Hardware

- **Must be**: red mushroom head, yellow background, twist-or-pull-to-release, **latching** (stays pressed until deliberately released), direct-opening NC contacts (look for the ⊖→ arrow symbol, IEC 60947-5-1 Annex K).
- **NC (normally closed) contacts, always.** Wire break = open circuit = stop. NO contacts fail silent on a broken wire — never use them for the stop function.
- Typical parts: Schneider XB4BS8445, IDEC XW1E, Eaton M22-PV. Get the 2-NC contact block version for dual channel (e.g., ZBE-102 ×2 or 1NC+1NC block).
- Mount within reach of every operator position; ≤ 600 mm reach, unobstructed, not behind doors.
- Multiple E-stops: wire all NC contacts **in series** per channel. Any one pressed opens the chain.

## Reference Wiring — Dual-Channel with Safety Relay

Example with Pilz PNOZ X3 / PNOZ s4 / Schmersal SRB301 class device (terminal names vary; pattern identical):

| Terminal | Connect to | Purpose |
|----------|-----------|---------|
| A1 | +24 VDC | Relay supply |
| A2 | 0 V | Relay supply return |
| S11 | E-stop channel 1 contact in | Test pulse source CH1 |
| S12 | E-stop channel 1 contact out | Monitored input CH1 |
| S21 | E-stop channel 2 contact in | Test pulse source CH2 |
| S22 | E-stop channel 2 contact out | Monitored input CH2 |
| S33–S34 | Reset button (NO, momentary) in series with contactor mirror contacts (K1 NC aux + K2 NC aux) | Monitored manual reset + external device monitoring (EDM) |
| 13–14 | Safety output 1 → contactor K1 coil | Cuts motor power |
| 23–24 | Safety output 2 → contactor K2 coil | Redundant cut |
| 33–34 or 41–42 | Aux/signal contact → MCU GPIO or PLC input | Status ONLY — never in the safety path |

Power path (three-phase example):

```
L1/L2/L3 ──► K1 main contacts ──► K2 main contacts ──► VFD/servo drive ──► motor
                 (in series — either contactor opening kills power)
```

DC robots: same pattern with DC-rated contactors (mind DC arc ratings — a contactor rated 20 A AC may only break 1–2 A at 48 VDC inductive; use DC-rated, e.g., Albright SW80, TE EV200, Gigavac GX series for battery packs).

**Why two contactors in series**: a single contactor can weld closed. Two in series with mirror-contact monitoring (the K1/K2 NC aux contacts in the reset loop) means a welded contactor blocks the next reset — the fault is *detected*, not just tolerated.

**Why dual channel on the button**: detects a single shorted wire or stuck contact. The safety relay sends distinct test pulses down S11→S12 and S21→S22; a cross-short between channels or a short to 24 V is detected within the relay's discrepancy window (typically channels must agree within ~0.5 s).

Contactor coil suppression: put a varistor or RC snubber across AC coils, a flyback diode (or better, diode + zener for faster drop-out) across DC coils. Bare flyback diode alone slows contactor opening by 2–5×; if drop-out time matters for your stop distance, use diode+zener (e.g., 1N4007 + 24 V zener) or a varistor.

## STO (Safe Torque Off) on Servo/Stepper Drives

Modern servo drives and many VFDs expose STO inputs (two channels, typically STO1/STO2 + common, 24 V = torque enabled, 0 V = torque removed). STO removes gate drive to the power stage in hardware — it IS a valid safety function (usually SIL 3 / PLe capable on certified drives).

- Wire safety relay outputs 13-14 / 23-24 to STO1 / STO2 instead of (or in addition to) a contactor.
- STO = Category 0 (motor coasts). For Cat 1, use drive's SS1 function or the time-delay relay pattern above.
- **STO does not isolate**: bus voltage is still present on drive terminals. For lockout/tagout you still need a disconnect.
- Cheap hobby drives ("STO" on a $40 stepper driver) are usually just an enable pin into a microcontroller — read the manual; if it's not a certified hardware channel, treat it as functional only and keep the contactor.

## Latching + Reset State Machine

Required behavior (IEC 60204-1): after E-stop actuation, the stop condition **latches** until (a) the button is manually unlatched AND (b) a separate deliberate reset action occurs. Releasing the button must NEVER restart motion by itself.

```
            button pressed (any time, any state)
  ┌───────────────────────────────────────────────┐
  ▼                                               │
ESTOP_ACTIVE ──button released──► RESET_REQUIRED ─┘
  ▲                                   │ reset btn pressed AND released
  │                                   ▼            (monitored: rising
  │                              SAFE_IDLE          edge on RELEASE)
  │                                   │ operator commands enable
  │                                   ▼
  └──────────────────────────────  RUNNING
```

Key rules:
1. Reset is **edge-triggered on release** of the reset button (monitored reset). A reset button stuck/jammed closed must not auto-reset — this is why safety relays monitor the S33-S34 loop for an open→close→open sequence.
2. Reset transitions to SAFE_IDLE (power available, motion disabled). A *separate* start/enable command begins motion. Reset ≠ restart.
3. The hardware safety relay implements this latch electrically. Firmware mirrors it for state reporting and to gate software-side enables — both latches must agree before motion.

## Firmware Patterns

### MicroPython (RP2040/ESP32) — monitoring + software-side latch

The MCU reads the safety relay's auxiliary contact. It does not implement the stop.

```python
from machine import Pin, Timer
import time

# Aux contact of safety relay: closed (low w/ pullup... see note) = chain healthy.
# Wire aux NC->GPIO->GND with internal pullup: chain OK = pin LOW.
# Open chain (estop) = pin HIGH. Broken wire also reads HIGH = fail safe.
ESTOP_OK = Pin(16, Pin.IN, Pin.PULL_UP)      # 0 = chain closed (OK)
RESET_BTN = Pin(17, Pin.IN, Pin.PULL_UP)     # 0 = pressed
MOTION_ENABLE = Pin(18, Pin.OUT, value=0)    # software enable to drive (functional only)

STATE_ESTOP, STATE_RESET_REQ, STATE_SAFE_IDLE, STATE_RUNNING = range(4)
state = STATE_ESTOP                          # ALWAYS boot into safe state

_db_count = 0
_db_val = 1

def debounced_estop_active():
    # call at 1 kHz; require 20 consecutive identical samples (20 ms)
    global _db_count, _db_val
    raw = ESTOP_OK.value()
    if raw == _db_val:
        _db_count = min(_db_count + 1, 20)
    else:
        _db_val = raw
        _db_count = 0
    return _db_val == 1 and _db_count >= 20   # HIGH = chain open = e-stop

_reset_prev = 1
def reset_released_edge():
    global _reset_prev
    cur = RESET_BTN.value()
    edge = (_reset_prev == 0 and cur == 1)    # released (rising) edge
    _reset_prev = cur
    return edge

def tick(t):
    global state
    estop = debounced_estop_active()
    if estop:                                 # dominant: from ANY state
        MOTION_ENABLE.value(0)
        state = STATE_ESTOP
        return
    if state == STATE_ESTOP:
        state = STATE_RESET_REQ               # chain closed again; await reset
    elif state == STATE_RESET_REQ:
        if reset_released_edge():
            state = STATE_SAFE_IDLE
    elif state == STATE_SAFE_IDLE:
        pass                                  # main app calls request_run()
    elif state == STATE_RUNNING:
        MOTION_ENABLE.value(1)

def request_run():
    global state
    if state == STATE_SAFE_IDLE:
        state = STATE_RUNNING
        return True
    return False

Timer(period=1, mode=Timer.PERIODIC, callback=tick)   # 1 kHz
```

Notes:
- Boot state is ESTOP. Power-on never enables motion.
- Debounce 10–30 ms. Mushroom E-stop contacts bounce; safety relays handle this internally but your aux-contact read does not.
- ESP32: avoid GPIO 0/2/12/15 for safety-adjacent IO (boot-strap pins glitch at reset). RP2040 GPIOs are clean at boot (inputs, no pull) — still verify your level conventions hold during reset.

### Arduino C++ — same pattern, plus watchdog

```cpp
#include <avr/wdt.h>

const uint8_t PIN_ESTOP_OK   = 2;   // aux NC contact -> GND, INPUT_PULLUP; LOW = OK
const uint8_t PIN_RESET_BTN  = 3;   // NO momentary -> GND, INPUT_PULLUP
const uint8_t PIN_MOTION_EN  = 4;   // to drive enable (functional layer only)

enum State : uint8_t { ESTOP, RESET_REQ, SAFE_IDLE, RUNNING };
volatile State state = ESTOP;

bool estopActive() {                 // debounced, 1 kHz calls, 20 ms window
  static uint8_t cnt = 0; static bool val = true;
  bool raw = digitalRead(PIN_ESTOP_OK) == HIGH;   // HIGH = chain open
  if (raw == val) { if (cnt < 20) cnt++; }
  else { val = raw; cnt = 0; }
  return val && cnt >= 20;
}

bool resetReleasedEdge() {
  static bool prev = HIGH;
  bool cur = digitalRead(PIN_RESET_BTN);
  bool edge = (prev == LOW && cur == HIGH);
  prev = cur;
  return edge;
}

void setup() {
  pinMode(PIN_ESTOP_OK, INPUT_PULLUP);
  pinMode(PIN_RESET_BTN, INPUT_PULLUP);
  pinMode(PIN_MOTION_EN, OUTPUT);
  digitalWrite(PIN_MOTION_EN, LOW);  // safe at boot, BEFORE anything else
  wdt_enable(WDTO_60MS);             // hung firmware -> reset -> boots safe
}

void loop() {
  static uint32_t last = 0;
  if (millis() - last >= 1) {        // ~1 kHz state machine
    last = millis();
    if (estopActive()) { digitalWrite(PIN_MOTION_EN, LOW); state = ESTOP; }
    else switch (state) {
      case ESTOP:     state = RESET_REQ; break;
      case RESET_REQ: if (resetReleasedEdge()) state = SAFE_IDLE; break;
      case SAFE_IDLE: /* await start command (serial/button) */ break;
      case RUNNING:   digitalWrite(PIN_MOTION_EN, HIGH); break;
    }
    wdt_reset();
  }
}
```

AVR gotcha: pins are inputs (Hi-Z) during reset/bootloader (~2 s on Uno). If the drive's enable input floats high during that window, the motor can twitch at boot. Fix in hardware: 10 kΩ pulldown on the enable line so it defaults to disabled. This rule generalizes: **every enable line gets a hardware pull to the safe state.**

### ROS 2 — E-stop status topic + software functional stop

```python
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from std_msgs.msg import Bool

class EstopMonitor(Node):
    """Publishes hardware E-stop state read via GPIO/CAN. Subscribers
    (controllers) must treat estop=True OR topic timeout as STOP."""
    def __init__(self):
        super().__init__('estop_monitor')
        qos = QoSProfile(depth=1,
                         reliability=ReliabilityPolicy.RELIABLE,
                         durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self.pub = self.create_publisher(Bool, '/estop_active', qos)
        self.timer = self.create_timer(0.02, self.tick)   # 50 Hz
    def tick(self):
        msg = Bool()
        msg.data = read_estop_gpio()    # your HW read
        self.pub.publish(msg)
```

Controller side rules:
- Subscribe with a **deadline/timeout**: if no `/estop_active` message in 100 ms, treat as E-stop. Absence of "OK" = stop. Never the inverse.
- `TRANSIENT_LOCAL` durability so late-joining controllers immediately get the latest state.
- This entire layer is functional. The hardware chain (safety relay → STO/contactor) is what actually protects people; the ROS layer prevents controllers from fighting the disabled drives and manages graceful recovery.

## Wireless E-Stop (mobile robots, AGVs)

Wireless links FAIL SILENT. Therefore the safe-state logic must be **heartbeat-based**: the robot stops when it stops *hearing* "all clear," not when it hears "stop."

Architecture:
- Transmitter (operator pendant) sends an authenticated heartbeat at fixed rate, e.g., every 50 ms, containing a monotonically increasing sequence number.
- Receiver on robot: dedicated MCU whose relay output holds the safety chain closed ONLY while heartbeats arrive. Heartbeat timeout → relay opens → same hardware chain as the wired button.
- Timeout budget: industrial wireless E-stops (e.g., Fort/HRI, Tyro, Autec) use 100–500 ms. Pick: `timeout ≥ 3 × heartbeat_period` to ride through single packet loss; total stop time = timeout + relay drop (10–30 ms) + contactor drop (15–50 ms) + mechanical stop distance. Verify the worst-case stopping distance at max speed is acceptable.
- The pendant's red button does both: stops sending heartbeats AND sends an explicit STOP packet (belt and suspenders — the explicit packet gives you the fast path, the timeout gives you the guaranteed path).
- Sequence numbers + MAC/auth prevent replay (an attacker or a reflection replaying old "OK" frames). At minimum: rolling counter, reject ≤ last seen.

Receiver pattern (MicroPython, ESP-NOW or LoRa or nRF24 — transport-agnostic):

```python
import time
from machine import Pin, Timer

CHAIN_HOLD = Pin(15, Pin.OUT, value=0)   # drives opto/relay holding safety chain
                                          # de-energized = chain OPEN = stop (fail safe)
HEARTBEAT_TIMEOUT_MS = 150                # 3 x 50 ms send period
last_hb = 0                               # ticks_ms of last valid heartbeat
last_seq = -1

def on_packet(payload):                   # called from radio RX callback
    global last_hb, last_seq
    seq, is_stop, mac_ok = parse_and_auth(payload)
    if not mac_ok or seq <= last_seq:
        return                            # bad auth or replay: IGNORE (not "stop",
    last_seq = seq                        #  ignore — timeout handles real loss)
    if is_stop:
        last_hb = 0                       # force immediate timeout
    else:
        last_hb = time.ticks_ms()

def supervisor(t):                        # 100 Hz
    fresh = last_hb and time.ticks_diff(time.ticks_ms(), last_hb) < HEARTBEAT_TIMEOUT_MS
    CHAIN_HOLD.value(1 if fresh else 0)

Timer(period=10, mode=Timer.PERIODIC, callback=supervisor)
```

Critical detail: `CHAIN_HOLD` energized = run. MCU crash, brownout, or radio task hang → pin returns low / watchdog resets → chain opens. Add the MCU watchdog (`machine.WDT(timeout=200)`) fed only from the supervisor timer. And the wired E-stop on the robot chassis remains in series with this relay — wireless is an *additional* stop input, never a replacement for the onboard button.

Latency reality check: WiFi/ESP-NOW typical RTT 2–20 ms but tail latencies during interference can exceed your timeout — that's fine (robot stops, operator resets), it fails toward safe. What's NOT fine is raising the timeout to 2 s to "fix nuisance stops." Fix the RF link (channel, antenna, power), not the safety parameter.

## Timing Budget (Cat 0 chain, worst case)

| Stage | Typical | Notes |
|-------|---------|-------|
| Button actuation → contact open | < 5 ms | Direct-opening action |
| Safety relay response | 10–30 ms | Datasheet "response time" |
| Contactor drop-out | 15–50 ms | Slower with bare flyback diode on DC coils |
| Drive discharge / motor torque decay | 1–50 ms | STO gate-kill is ~ms; bus caps hold voltage but no torque |
| **Electrical total** | **30–135 ms** | |
| Mechanical coast/brake distance | dominant | Measure it. This sets your safety distances (ISO 13855). |

Safety distance formula (ISO 13855): `S = K × T + C`, where K = 1600 mm/s (walking approach), T = total stop time in seconds, C = intrusion allowance. A 200 ms total stop time ⇒ E-stop alone doesn't protect anyone closer than ~320 mm + C; that's what guards and light curtains are for. E-stop is a *complementary* protective measure, not the primary safeguard.

## The Mistakes Everyone Makes

1. **Software-only E-stop.** GPIO → ISR → `disableMotors()`. Covered above; it's the #1 failure. Hardware chain or it doesn't count.
2. **NO contacts instead of NC.** Broken wire = E-stop silently dead. NC + monitoring: broken wire = stop. Always NC.
3. **E-stop in series with the logic supply instead of motor power.** Cutting 5 V to the MCU while the motor driver stays powered can leave outputs floating → motors run away. Cut the *power stage*, keep logic alive for diagnostics.
4. **Auto-restart on button release.** Twist-release of the mushroom must land in RESET_REQUIRED, never RUNNING. Verified by test: press E-stop mid-motion, release it — nothing may move until reset + start.
5. **Reset button that's level-triggered.** Jammed reset button = auto-reset after every E-stop. Edge-on-release, monitored.
6. **Single contactor, no monitoring.** Contactors weld. Use two in series + mirror (NC aux) contacts in the reset loop, or a drive with certified STO.
7. **Relay module "active high = stop."** Hobby relay boards often energize to open the load. Energy must flow to PERMIT motion (energize-to-run); loss of power anywhere = stop. Check every stage: button, relay coil, contactor coil, STO inputs, brake coil.
8. **Sharing the E-stop signal as a data input only.** Routing the chain through a PLC/MCU input and back out a PLC output puts software in the path. Aux contacts INTO the controller: yes. Chain THROUGH the controller: no (unless it's a certified safety PLC running certified safety logic).
9. **Forgetting stored energy.** Bus capacitors (drives hold >60 V for seconds–minutes), gravity loads, spinning flywheels, pneumatic pressure. E-stop cuts the source; you also need bleed resistors, mechanical brakes, and dump valves per the energy type.
10. **Wireless E-stop with "stop on STOP packet" logic.** Packet loss = no stop. Must be heartbeat-timeout (stop on silence).
11. **E-stop used as the routine on/off switch.** Wears the contacts, normalizes the action, and contactors breaking full load current daily will weld sooner. Provide a separate operational stop.
12. **No periodic test.** Direct-opening contacts and welded contactors are only detected if exercised. Test the full chain (press button, verify motor power actually dead at the terminals) at least monthly; log it.
13. **Floating enable lines at boot.** Pull every drive-enable to the disabled state in hardware (10 kΩ). MCU resets, bootloaders, and flash programming all leave pins Hi-Z.
14. **24 V supply shared and undersized.** Safety relay (50–150 mA) + two contactor coils (100–500 mA each, with 5–10× inrush on some) browning out the rail during pickup → chattering contactors. Budget the 24 V rail; separate the safety supply from noisy actuator loads.

## Debugging Checklist

Safety relay won't reset:
- [ ] Both channels closed? Measure S11–S12 and S21–S22 continuity with E-stop released.
- [ ] Channel discrepancy: did one channel close > ~0.5 s after the other (dirty contact)? Cycle the button firmly.
- [ ] EDM loop open: a contactor failed to drop (welded) so its NC mirror contact in S33–S34 is open. Check K1/K2 aux continuity with coils de-energized.
- [ ] Reset is monitored type but you wired a maintained switch — must be momentary NO.
- [ ] Cross-fault detected (channel shorted to 24 V or to other channel): relay latches fault, needs power cycle on many models. Megger/check the field wiring.
- [ ] A1–A2 actually at 24 V under load? Measure during reset attempt, not idle.

Nuisance trips:
- [ ] Contact bounce/vibration on the button or its terminals (loose screw terminals are the classic). Torque to spec.
- [ ] EMI from contactor coil switching coupling into channel wiring — add coil suppression, separate safety wiring from motor cables (>100 mm or crossed at 90°).
- [ ] Shared 0 V bouncing: motor return current through the safety relay's ground path. Star-ground at the supply.
- [ ] Wireless: log heartbeat inter-arrival times; if p99 > timeout/2, fix RF before anything else.

Motor doesn't stop on E-stop test:
- [ ] Measure voltage at motor/drive INPUT terminals with button pressed. If present: contactor welded or chain miswired (relay output bypassed?).
- [ ] STO wired to a non-certified "enable" pin that firmware can override?
- [ ] Drive bus caps: torque should die instantly even though bus voltage persists. If shaft still has torque, STO isn't actually opening both channels.

Commissioning test procedure (run all, every install):
1. Press each E-stop individually → verify motor power dead at terminals, status reported to controller, relay LEDs show channel state.
2. Release button → verify NOTHING restarts; state = reset-required.
3. Reset → verify motion still doesn't start until explicit start command.
4. Press E-stop DURING motion at max speed → measure stop time/distance, compare to budget.
5. Pull one channel wire (simulate break) → must stop or refuse reset.
6. Short the two channels together → relay must detect and refuse reset.
7. Power-cycle mid-run → must boot into safe state, no motion blip (scope the enable line through boot).
8. Wireless: kill the pendant battery mid-run → robot stops within timeout.

## Minimal BOMs

Bench robot (single channel, hardware chain, < 48 V / < 10 A):
- E-stop button 1NC (IDEC XW1E-BV411MR, ~$15)
- DC-rated relay or contactor sized 1.5× motor stall current, coil energize-to-run
- Flyback suppression on coil; 10 kΩ pulldowns on all enables
- MCU monitors aux contact only

Workshop machine / cobot cell (PLd target):
- E-stop 2NC (Schneider XB4BS8445 + contact blocks)
- Safety relay (Pilz PNOZ s4 ~$200, Schmersal SRB301MC, or Banner SR-IM-9A)
- 2× contactors with mirror contacts (Schneider LC1D + LADN aux, Siemens 3RT + 3RH)
- Monitored reset button (NO momentary, blue or white — not red)
- For Cat 1: PNOZ s5 (delayed outputs) or drive SS1 + delayed channel
