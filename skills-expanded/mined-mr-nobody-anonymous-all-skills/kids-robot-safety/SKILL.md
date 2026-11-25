---
name: kids-robot-safety
description: "Use when designing, coding, or reviewing any robot that children (under 14) will touch, hold, or operate — toys, classroom kits, STEM products, hand-held bots. Provides safety engineering expertise: pinch-point elimination, LiPo vs NiMH battery decisions, EN71/CPSIA small-parts compliance awareness, motor torque/force limits for hand-held robots, firmware emergency-stop patterns (watchdog + hardware kill), and touchable-voltage limits."
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


# Kids Robot Safety Engineering

Safety for children's robots is not a feature — it is a set of hard constraints that must be designed in from the first line of firmware and the first CAD sketch. Retrofitting safety fails. This skill encodes the constraints, the numbers, and the firmware patterns.

**Core principle: a child WILL do the worst possible thing with the robot.** They will put it in their mouth, stick a finger in the gearbox while it runs, drop it in the bath, charge it under a pillow, and press every button simultaneously. Design for that child, not the well-behaved one in the marketing video.

---

## 1. Battery Chemistry: The Single Biggest Decision

### Decision table

| Chemistry | Kids product verdict | Why |
|---|---|---|
| **NiMH (AA/AAA cells)** | **PREFERRED for under-8 and any product parents charge** | Thermally tolerant, no fire on puncture, no protection circuit needed, user-replaceable, ships without UN38.3 lithium paperwork hassle |
| **LiPo pouch with protection PCB + JST-PH** | Acceptable for 8+ supervised kits, ONLY with protection circuit integral to cell | Energy density; but fire risk on puncture/overcharge |
| **Bare LiPo pouch (no PCM), hobby-style with XT30/XT60** | **NEVER in a kids product** | Single overdischarge/puncture = fire. Hobby connectors invite reverse insertion |
| **18650 cylindrical Li-ion, protected, non-removable** | Acceptable for 10+ if non-user-accessible (screwed compartment) | Steel can resists puncture; but loose 18650s are a swallow/short hazard — never user-swappable |
| **Coin/button cells (CR2032 etc.)** | Avoid entirely if possible | Ingestion = esophageal burn, can be fatal in 2 hours. If unavoidable: screw-secured compartment is a LEGAL requirement (IEC 62115, "reasonably foreseeable abuse" tests) |

### LiPo rules if you must use one

- **Protection circuit (PCM) must be on the cell itself**, not on your PCB. Specify cells with integrated PCM: overcharge cutoff ≤ 4.25 V, overdischarge cutoff ≥ 2.5 V (prefer 2.8 V), overcurrent cutoff sized to ~2–3× your max draw, short-circuit protection.
- **Charge at ≤ 0.5C for kids products** (e.g., 250 mA for a 500 mAh cell). 1C is the hobby norm; halve it. Slower charge = cooler cell = wider safety margin.
- **Charger IC, not a wall wart**: use a proper CC/CV linear charger — MCP73831 (≤500 mA), TP4056 *with* the DW01A+FS8205 protection companion board (the bare TP4056 board WITHOUT protection is the one that burns houses down — verify the board has 6 ICs/2 chips not 1), or BQ24074 for power-path designs.
  - Set charge current via PROG resistor: MCP73831 `I_chg = 1000V/R_prog` → 4.7 kΩ ≈ 213 mA. TP4056 `I_chg = 1200/R_prog (A)` → 5 kΩ ≈ 240 mA.
- **NTC thermistor**: if the cell has a 3-wire JST with NTC, USE IT (BQ2407x supports TS pin; charge inhibited outside 0–45 °C). Charging a cold (<0 °C) LiPo plates lithium metal → internal short weeks later.
- **Never charge unattended** must appear in the manual, but don't rely on it — design so an unattended charge is still safe: charge-current limit, charge timer (most charger ICs have a safety timer ~4–10 h; do not disable it), no charging while motors can run (power-path or firmware lockout).
- **Mechanical**: cell in a rigid compartment, no sharp PCB corners or screw tips facing the pouch, foam pad, wires strain-relieved. A swollen cell must have somewhere to swell (10–15% thickness headroom) without pressing on anything sharp.
- **Connector**: JST-PH 2.0 mm, polarized. Never barrel jacks or pin headers for battery — kids reverse them.

### NiMH design notes

- 4×AA NiMH = 4.8 V nominal (5.4 V fresh off charge, 4.0 V depleted). Design your regulator for the 4.0–5.6 V window. An ESP32 (3.3 V) on 4×AA NiMH via an MCP1700-3302 LDO works across the whole curve.
- Low-battery cutoff in firmware at ~1.0 V/cell (4.0 V for 4S) — NiMH tolerates overdischarge far better than LiPo but reversal of the weakest cell still kills it.
- Alkaline compatibility: if the compartment fits alkalines (6.0 V for 4×AA), your input range must handle 6.4 V fresh, or print "NiMH only" AND clamp anyway. Kids' parents will insert alkalines.

---

## 2. Voltage and Current Exposure Limits

Numbers an agent must know when reviewing a kids-robot schematic:

- **Touchable conductor limit (toy standards, IEC 62115): 24 V DC max** between any two simultaneously touchable parts. In practice kids robots run 3–12 V — fine. The hazard is never electrocution at these voltages; it is **burns and fire** from shorted batteries.
- **A 2S LiPo shorted through a paperclip delivers 20–60 A.** Every battery output needs a fuse or polyfuse. Use a PTC resettable fuse (polyfuse) rated ~1.5–2× max normal draw, e.g., MF-R110 (1.1 A hold) for a small bot. It must be BEFORE the switch and any user-accessible contacts.
- **No exposed PCB traces or test pads carrying battery voltage** in any area a child can touch — saliva + battery voltage = electrolytic corrosion and localized heating. Conformal coat or enclose.
- **USB charging port**: USB-C with 5.1 kΩ CC pull-downs (so dumb C-to-C cables work). The port is the one connector kids will jam things into — recess it, and the polyfuse upstream covers a shorted port.
- **Surface temperature limits** (IEC 62115 / EN 71-1 informed): touchable metal ≤ 45 °C above… practically: design so no touchable surface exceeds **~48 °C absolute** during stall or charge. Motor cans and charger ICs are the usual offenders. If a motor can stall against a kid's hand, the can must not be directly touchable or must be thermally limited in firmware (see §5).

---

## 3. Pinch Points and Mechanical Hazards

### The pinch-point rule of thumb

A child's finger is modeled as a **5.6 mm probe (small finger of a young child)**; toy standards use accessibility probes. The engineering translation:

- **Any gap that is between 5 mm and 12 mm and can CLOSE under power is a pinch point.** Gaps < 5 mm: finger can't enter. Gaps > 12 mm (and not closing below 12 mm): finger fits loosely and isn't trapped (for small kids' fingers; for hinged panels and larger products treat 5–25 mm as the danger band).
- Gear trains: **fully enclose every gear mesh.** A cover with ventilation slots must keep slots < 5 mm wide near moving parts. Kids defeat snap-fit covers — use screws (which also satisfies battery-compartment rules).
- Wheel-to-chassis gaps: keep < 5 mm or > 12 mm. The classic failure: a 8 mm gap between a driven wheel and the body that swallows a fingertip.
- Servo horns and rotating arms: shroud the root of the arm where it sweeps past the body — that's where the scissor action is. The arm tip is rarely the hazard; the **closing angle near the pivot** is.
- Hinged lids/joints: required by EN 71-1 to not have a 5–12 mm gap at any point in travel.
- **Spring-loaded or elastic-driven mechanisms** store energy even when power is off. A wound-up gripper releasing on a finger needs the same analysis as a powered one.

### Sharp edges and points

- EN 71-1 has specific sharp-edge (tape test) and sharp-point tests. Engineering translation: **all accessible edges radiused ≥ 0.5 mm**, no accessible burrs, no exposed screw tips, PCB edges not accessible (V-score burrs are sharp). 3D-printed parts: FDM layer edges pass, but support-removal scars can fail — design to avoid supports on touchable faces.
- Antennas/wires that protrude: must not be rigid sharp points; whip antennas in kids products are banned in practice.

---

## 4. Small Parts: EN 71 / CPSIA Awareness

The agent is not a compliance lab, but must not design products that obviously fail:

- **Small-parts cylinder (16 CFR 1501 / EN 71-1)**: 31.7 mm diameter × 57.1 mm deep truncated cylinder. **Any component that fits entirely inside it is a choking hazard for under-3s and is banned in under-3 products, and triggers warning labels for 3–6.** This includes anything that can detach under the standardized abuse tests (drop, torque, tension ~70 N pull on graspable parts).
- Practical consequences:
  - Wheels, servo horns, sensor modules, battery doors, knobs: must survive a **70 N pull and 0.34 N·m torque** without detaching, or must be too big for the cylinder.
  - **Screws over snap-fits** for anything load-bearing or graspable.
  - LEGO-style kits with small pieces are fine for 6+ with the choking-hazard warning; they are NOT fine marketed to under-3.
- **Magnets**: if two+ small magnets (or one magnet + ferromagnetic part) can be swallowed, intestinal pinching is potentially fatal. EN 71-1 magnet flux index limit: **< 50 kG²·mm² for any swallowable magnet**. Practically: NO loose neodymium magnets in kids robots. Glue is not retention — use mechanical capture (overmold, screwed pocket).
- **CPSIA (US)**: lead < 100 ppm in any accessible substrate, phthalate limits in plasticized parts, mandatory third-party testing (CPC certificate) for children's products. Design impact: specify **lead-free HASL or ENIG PCBs**, RoHS components, and phthalate-free TPU/PVC. "RoHS compliant" BOM ≠ CPSIA tested, but it's the right starting spec.
- **Cords/straps**: any cord > 220 mm on an under-3 toy is a strangulation finding. Tethered controllers for young kids: keep cords short or go wireless.
- **Sound**: continuous sound at the ear ≤ ~85 dB(A) for close-to-ear toys (EN 71-1 acoustics). Cap your buzzer/speaker drive in firmware; a piezo at full MCU PWM can exceed 90 dB at 5 cm.

---

## 5. Motor Torque and Force Limits for Hand-Held Robots

A robot a child holds while it moves (gripper bots, walking bots held in hand, RC cars picked up while driving) must be force-limited.

### Numbers

- **Skin pinch pain threshold ~ 10–25 N over a fingertip-sized area; injury (skin break/crush) risk climbs steeply above ~50 N** on a small contact area. Collaborative-robot standards (ISO/TS 15066) use body-region force/pressure limits; for kids, design to a **fraction**: target **< 15 N max static force at any pinch or grip point, < 25 N transient**.
- Convert torque to force: `F = τ / r`. A gripper with 2 N·m at the jaw pivot and a 2 cm jaw length exerts **100 N at the jaw tip** — wildly unsafe. The popular MG996R servo (~1.1 N·m at 6 V) on a 3 cm gripper jaw = ~37 N. Still too much for a kid's finger placed at the jaw root (1 cm → 110 N).
- **Choose weak actuators on purpose**: SG90/MG90S class servos (~0.2 N·m at 5 V) on ≥3 cm arms (≤ ~6.5 N tip force) are inherently finger-safe. N20 geared motors: pick the LOW gear-ratio (high-speed, low-torque) variants for anything that can grip or close; a 1000:1 N20 can exceed 0.5 N·m and strip skin.
- **Wheeled bots**: limit is not torque but kinetic energy and entrapment. < 0.5 m/s and < 500 g for tabletop kids bots keeps impact energy trivial (< 0.07 J). Hair entanglement in wheels/axles: shroud axle ends; long hair wraps around any exposed spinning shaft in seconds.

### Firmware force limiting (works even without a force sensor)

Current is a torque proxy: `τ ∝ I` for DC motors. Limit current in firmware:

```cpp
// Arduino C++ — current-limited gripper close (ACS712-05 or INA219 on motor)
// DRV8833: sense via aISEN resistor, or use driver with built-in current limit
const float CURRENT_LIMIT_A = 0.35;   // tuned: corresponds to ~8 N at jaw tip
const uint16_t GRIP_TIMEOUT_MS = 1500;

bool closeGripper() {
  uint32_t t0 = millis();
  motorForward(GRIP_PWM);             // e.g. 60% duty, never 100%
  while (millis() - t0 < GRIP_TIMEOUT_MS) {
    float i = readMotorCurrentA();
    if (i > CURRENT_LIMIT_A) {        // object (or finger) met resistance
      motorBrakeThenHold(HOLD_PWM);   // drop to low holding duty (~25%)
      return true;
    }
    delay(5);
  }
  motorCoast();                        // timeout: never leave motor stalled
  return false;
}
```

```python
# MicroPython (ESP32 / Pico) — stall + thermal protection for any kids-bot motor
import time
from machine import Pin, PWM, ADC

PWM_MAX = 40000          # cap duty at ~60% of 65535: hard ceiling on torque
STALL_CURRENT = 0.35     # amps
STALL_TRIP_MS = 300      # current may spike on start; require sustained stall
THERMAL_BUDGET = 5.0     # amp-seconds of over-limit before forced cooldown

class SafeMotor:
    def __init__(self, pwm_pin, dir_pin, isense_adc):
        self.pwm = PWM(Pin(pwm_pin), freq=20000)  # 20 kHz: inaudible, kid-friendly
        self.dir = Pin(dir_pin, Pin.OUT)
        self.isense = ADC(Pin(isense_adc))
        self.over_since = None
        self.heat = 0.0
        self.last = time.ticks_ms()

    def current_a(self):
        # ACS712-05: 185 mV/A, midpoint ~ Vcc/2 -> calibrate offset at boot, motor off
        return abs(self.isense.read_uv() / 1e6 - self.offset_v) / 0.185

    def drive(self, duty):                 # duty: -1.0 .. 1.0
        now = time.ticks_ms()
        dt = time.ticks_diff(now, self.last) / 1000
        self.last = now
        i = self.current_a()
        # leaky thermal integrator: heats when over limit, cools when under
        self.heat = max(0.0, self.heat + (i - STALL_CURRENT) * dt)
        if self.heat > THERMAL_BUDGET:
            self.pwm.duty_u16(0)           # forced cooldown; caller must back off
            return False
        if i > STALL_CURRENT:
            if self.over_since is None:
                self.over_since = now
            elif time.ticks_diff(now, self.over_since) > STALL_TRIP_MS:
                self.pwm.duty_u16(0)       # sustained stall: cut power
                return False
        else:
            self.over_since = None
        self.dir.value(1 if duty >= 0 else 0)
        self.pwm.duty_u16(min(int(abs(duty) * 65535), PWM_MAX))
        return True
```

Key points encoded above that everyone gets wrong:
1. **Cap PWM duty in one place** (a constant), never trust call sites to pass safe values.
2. **Debounce stall detection** (start-up inrush is 3–5× run current for ~100 ms; instant trip = bot that never moves).
3. **Thermal integrator, not just instantaneous trip** — repeated near-limit stalls cook small motors and make touchable surfaces exceed 48 °C.
4. **Never leave a motor energized at stall** after a timeout. Coast or brake, don't hold full duty.
5. 20 kHz PWM: sub-20 kHz whine is unpleasant and some kids (and dogs) find audible PWM distressing.

---

## 6. Emergency Stop: Firmware Patterns

A kids robot needs THREE independent stop layers. Any one alone is insufficient.

### Layer 1 — Hardware kill (no firmware involved)

A physical switch or button that interrupts motor power **electrically**, not via GPIO. Slide switch in the battery line (after fuse) is the minimum. For bots with a gripper or blade-adjacent anything: a **big red latching mushroom button in series with the motor driver's VM supply** (logic can stay powered so state isn't lost). Firmware cannot be trusted to stop a robot whose firmware has crashed — that is the whole point of this layer.

### Layer 2 — Watchdog + heartbeat

```cpp
// Arduino C++ (AVR/ESP32) — watchdog ensures a hung loop can't leave motors on
#include <esp_task_wdt.h>            // ESP32
void setup() {
  // CRITICAL ORDER: force motors off BEFORE anything that can hang (WiFi, sensors)
  pinMode(MOTOR_EN, OUTPUT);
  digitalWrite(MOTOR_EN, LOW);       // motors default OFF at boot/reset
  esp_task_wdt_init(2, true);        // 2 s timeout, panic->reset
  esp_task_wdt_add(NULL);
  // ... now init radio/sensors
}
void loop() {
  esp_task_wdt_reset();              // ONLY place the watchdog is fed
  // ...
}
```

Watchdog rules:
- **Feed the watchdog in exactly one place**, at the top of the main loop. Feeding it inside helper functions or ISRs defeats it (a hung subloop that contains a feed never trips).
- **Motor outputs must default OFF on reset.** On AVR, GPIO floats at reset — your motor driver's enable pin needs an external **pull-down resistor (10 kΩ)** so a watchdog reset (or flashing!) physically disables motors during the boot window. This resistor is the most-omitted safety component in hobby designs.
- Use a driver with an active-high enable (DRV8833 nSLEEP needs pull-DOWN; TB6612 STBY needs pull-DOWN) so the unpowered/floating state = motors dead.

### Layer 3 — Command timeout (dead-man's switch for remote control)

```python
# MicroPython — RC/BLE-controlled bot: stop if commands cease
CMD_TIMEOUT_MS = 300     # 300 ms: snappy enough that a dropped phone = instant stop

last_cmd = time.ticks_ms()

def on_command(packet):
    global last_cmd
    last_cmd = time.ticks_ms()
    apply_drive(packet)

def safety_tick():       # call every loop iteration
    if time.ticks_diff(time.ticks_ms(), last_cmd) > CMD_TIMEOUT_MS:
        all_motors_off()        # coast, not brake, for drive wheels
        set_state(STOPPED)      # require explicit resume command, not auto-resume
```

- **300 ms timeout** for BLE/WiFi-controlled kids bots. 1 s feels like the robot "ran away" after the app crashed.
- **Latch the stop**: after a timeout stop, require a deliberate resume action (button press in app). Auto-resume on next packet means a bot that lurches the instant the connection flickers back.
- E-stop state machine: `RUN → STOPPED` on (button, timeout, stall-trip, low battery, overtemp). `STOPPED → RUN` only via explicit user action AND all fault conditions cleared.
- **The soft e-stop button GPIO needs an interrupt, not polling-only**, and the ISR sets a flag that the main loop AND the motor functions both check. Belt and suspenders: motor drive functions early-return if `estop_flag` is set, so a logic bug elsewhere can't drive through a stop.

### Low-battery behavior

Cut motors at the cell-protection threshold MINUS margin (LiPo: stop motors at 3.3 V/cell, warn at 3.5 V) so the protection PCM is never your routine cutoff — it's the backstop. A kids bot that dies abruptly is fine; a LiPo repeatedly ridden down to PCM cutoff (2.5 V) swells within months.

---

## 7. The Five Mistakes Everyone Makes

1. **Bare TP4056 module (no DW01A protection) + unprotected LiPo pouch.** The two cheapest parts on AliExpress combine into a fire. Verify the protection ICs exist, or spec a protected cell.
2. **No pull-down on the motor-driver enable pin.** Motors twitch or run during boot, flashing, and watchdog resets — exactly when firmware can't stop them.
3. **Gripper/arm torque calculated never, jaw force = servo torque ÷ 2 cm.** Run the `F = τ/r` math at the WORST point (closest to pivot a finger fits), not the jaw tip.
4. **Watchdog fed in multiple places / inside the radio callback.** A wedged main loop with a live BLE stack keeps feeding the dog while motors run open-loop.
5. **Snap-fit battery door + AAA cells small enough for the choke cylinder.** Battery compartments on kids products need a screw or two independent simultaneous motions (IEC 62115 / EN 62115). A coin cell behind a snap fit is a recall.

---

## 8. Pre-Ship Review Checklist

Run this against any kids-robot design/firmware before calling it done:

**Battery**
- [ ] Chemistry justified (NiMH default; LiPo only with integral PCM, ≤0.5C charge, charger safety timer on)
- [ ] Polyfuse on battery output, before switch
- [ ] Battery compartment screw-secured; cells not swallowable OR not user-accessible
- [ ] Low-battery firmware cutoff above PCM threshold; charging lockout vs motor run

**Mechanical**
- [ ] No closing gaps in the 5–12 mm band anywhere in any mechanism's travel
- [ ] All gear meshes enclosed, vent slots < 5 mm near moving parts
- [ ] Graspable parts survive 70 N pull / 0.34 N·m torque or are larger than the small-parts cylinder
- [ ] No swallowable magnets; magnets mechanically captured
- [ ] Accessible edges radiused, no exposed screw tips/PCB edges
- [ ] No exposed spinning shafts (hair entanglement)

**Electrical**
- [ ] All touchable conductors ≤ 24 V (trivially true) and no exposed battery-voltage traces/pads
- [ ] Touchable surfaces < 48 °C under stall and charge (measure, don't assume)
- [ ] USB port recessed, CC pull-downs present, upstream polyfuse covers it

**Firmware**
- [ ] PWM duty hard cap in one constant; jaw/arm force ≤ 15 N at worst-case finger position
- [ ] Stall detection with inrush debounce + thermal integrator; stalled motor never held energized
- [ ] Watchdog: single feed point, 1–2 s timeout, motors default OFF through reset (external pull-down verified)
- [ ] Command timeout ≤ 300 ms for remote control; stop is latched, resume is explicit
- [ ] E-stop flag checked inside motor-drive functions, not only the main loop
- [ ] Speaker/buzzer output capped (≤ ~85 dB(A) close to ear)

**Regulatory awareness (flag for the compliance lab, don't self-certify)**
- [ ] Age grading decided and consistent with small parts / magnets / cords
- [ ] BOM is RoHS / lead-free; plastics phthalate-free spec
- [ ] EN 71-1/-2/-3 + EN 62115 (EU) or ASTM F963 + CPSIA + 16 CFR 1501 (US) testing planned; CPC/DoC paperwork on the launch checklist
