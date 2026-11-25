---
name: power-management
description: "Use when designing or debugging power systems for robots — battery chemistry selection (NiMH/LiPo/18650), brownout prevention on motor start, regulator choice (buck vs LDO), battery voltage sensing, low-battery behaviors, and TP4056 charging circuits. Provides exact wiring tables, voltage/current budgets, capacitor sizing, ADC divider math, and working MicroPython/Arduino code for battery monitoring and graceful degradation."
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


# Robot Power Management

Power is the #1 cause of "random" robot failures. A robot that resets when motors start, an ESP32 that boot-loops, a Pi that corrupts its SD card — these are power problems, not software bugs. This skill makes the power system correct **before** debugging code.

## 0. The One Rule

**Logic and motors NEVER share a regulator output.** They may share a battery, but the path splits at the battery terminals:

```
Battery (+) ──┬──> Motor driver VIN (direct, thick wire, short)
              └──> Buck/LDO ──> MCU 3.3V/5V rail
Battery (−) ──┬──> Motor driver GND
              └──> MCU GND          <-- star ground at battery, NOT daisy-chained
```

If you remember nothing else: separate rails, star ground, bulk capacitance at the motor driver.

---

## 1. Battery Chemistry Selection

| Property | 4×AA NiMH | 2S LiPo | 2×18650 (2S) | 6×AA Alkaline |
|---|---|---|---|---|
| Nominal voltage | 4.8 V | 7.4 V | 7.2–7.4 V | 9 V |
| Full charge | 5.6 V (1.4 V/cell) | 8.4 V | 8.4 V | 9.6 V |
| Empty (cutoff) | 4.0 V (1.0 V/cell) | 6.4 V (3.2 V/cell) | 6.0 V (3.0 V/cell) | 5.4 V |
| Capacity (typical) | 2000–2500 mAh | 1000–5000 mAh | 2500–3500 mAh/cell | ~1500 mAh under load |
| Max continuous discharge | ~2C (4–5 A) | 20C+ (huge) | ~2C protected, 10C+ unprotected high-drain | <1 A (sags badly) |
| Internal resistance | ~30 mΩ/cell | ~5–15 mΩ | ~20–40 mΩ (protected) | 150–300 mΩ/cell |
| Charging complexity | Easy (dumb chargers OK) | Needs balance charger, fire risk | TP4056 per cell or 2S BMS | Not rechargeable |
| Abuse tolerance | Excellent | Poor (puncture = fire) | Good (steel can) | Fine |
| Kid/classroom safe | **Yes** | No (supervised only) | Mostly | Yes but wasteful |

**Decision rules:**
- **Classroom / kids / first robot:** 4×AA or 6×AA NiMH. Survives shorts, reverse insertion (with holder diode), drops. Worst case: warm battery.
- **Need torque or speed (drive motors > 1 A each):** 2S LiPo with a proper XT60/JST connector and a low-voltage alarm. Never charge unattended.
- **Long runtime, rebuildable packs:** 18650s in holders. Buy **protected** cells for beginners (built-in over-discharge cutoff ~2.5 V), **unprotected high-drain** (Molicel P28A, Samsung 25R) only if a BMS board is in circuit.
- **Never** power motors from a 9V PP3 block battery. Its internal resistance (~2 Ω) collapses to <6 V under a 500 mA motor load. This is the most common beginner mistake.
- **Never** run a Raspberry Pi from AA alkalines through a linear regulator — a Pi 4 needs 5 V / 3 A peaks; only a buck from 2S+ or a quality USB power bank works.

**Voltage matching to motors:**
- "TT" yellow gearmotors: 3–6 V. Run from 4×NiMH (4.8 V) direct, or 2S LiPo **through the driver's voltage drop** (L298N drops ~2.6 V, conveniently landing 8.4 V → ~5.8 V — the only good thing about an L298N).
- N20 micro gearmotors: check the label, commonly 6 V or 12 V variants.
- Sensors/servos (SG90): 4.8–6 V. From 2S LiPo, use a separate 5 V buck rated ≥3 A; one stalled SG90 draws ~700 mA, an MG996R draws ~2.5 A stalled.

**Capacity math:** runtime_h = capacity_Ah ÷ average_current_A × 0.8 (the 0.8 covers voltage sag and the unusable tail). A 2000 mAh pack driving 2 motors at 400 mA each + 200 mA logic ≈ 2.0 ÷ 1.0 × 0.8 = **1.6 hours**.

---

## 2. Brownout on Motor Start — Cause and Cure

**Symptom:** robot resets / ESP32 prints `Brownout detector was triggered` / Pi shows lightning bolt / Bluetooth disconnects — exactly when motors start or reverse.

**Cause:** a DC motor at standstill is just its winding resistance. Inrush = V/R. A 6 V TT motor with 3 Ω winding pulls **2 A for ~50 ms** at start, 4–6× its running current. Reversing direction at speed pulls up to 2× stall current. This current spike × battery internal resistance + wire resistance = a voltage notch on the shared rail. MCU brownout thresholds: ESP32 ≈ 2.43 V on 3.3 V rail (default), ATmega328P BOD typically 2.7 V, Pi flags under-voltage below 4.63 V.

**The fix stack (apply ALL of these, in order of importance):**

1. **Separate rails** (Section 0). The motor spike then sags the battery, but the buck regulating logic rides through if its input stays above dropout.
2. **Bulk capacitor at motor driver VIN:** **1000 µF electrolytic, voltage rating ≥ 2× battery voltage** (so 16 V for 2S LiPo, 10 V minimum for 4×AA). Place within 5 cm of the driver's power pins. It supplies the inrush locally instead of yanking the rail.
3. **Bulk capacitor at MCU regulator input:** 470–1000 µF. Plus the standard 100 nF ceramic at every IC's VCC pin.
4. **Motor noise suppression:** 100 nF ceramic soldered **across each motor's terminals**, plus optionally 100 nF from each terminal to the motor can. Kills brush-noise resets and I2C corruption.
5. **Soft-start in software:** ramp PWM instead of 0→100%:

```python
# MicroPython — soft start, ~200 ms ramp, eliminates inrush spike
from machine import Pin, PWM
import time

pwm = PWM(Pin(14), freq=1000)

def set_motor(target_duty_u16, step=2048, delay_ms=10):
    current = pwm.duty_u16()
    if target_duty_u16 > current:
        for d in range(current, target_duty_u16, step):
            pwm.duty_u16(d)
            time.sleep_ms(delay_ms)
    pwm.duty_u16(target_duty_u16)

set_motor(65535)  # full speed via ramp, not a step
```

```cpp
// Arduino — same idea
void setMotorSoft(uint8_t pin, uint8_t target) {
  static uint8_t current = 0;
  while (current != target) {
    current += (target > current) ? 1 : -1;
    analogWrite(pin, current);
    delay(2);              // 0->255 in ~510 ms; use delay(1) for faster ramp
  }
}
```

6. **Direction-change guard:** never flip H-bridge direction at full PWM. Ramp to 0, wait 50 ms (back-EMF decay), then ramp the other way. Instant reversal ≈ 2× stall current and is the #1 H-bridge killer.
7. **Wire gauge and length:** motor power wires ≥ 22 AWG for ≤ 2 A, ≥ 18 AWG for ≤ 6 A, as short as practical. Breadboard rails and DuPont jumpers are good for ~500 mA max — motor current through a breadboard **will** brown out and may melt the rail. Solder or use screw terminals for motor power.

**ESP32-specific:** if brownouts persist during WiFi TX (WiFi bursts ~400 mA), add 470 µF directly across ESP32 3V3/GND and ensure the 3.3 V regulator is ≥ 600 mA (the AMS1117 on most dev boards is marginal from 5 V USB through a diode). Do NOT "fix" it by disabling the brownout detector (`CONFIG_ESP_BROWNOUT_DET=n`) — that converts clean resets into flash corruption.

---

## 3. Buck vs LDO vs Boost

| | LDO (AMS1117, MCP1700) | Buck (MP1584, LM2596, TPS54331) | Boost (MT3608) |
|---|---|---|---|
| Efficiency | V_out/V_in (7.4→3.3 V = **45%**, rest is heat) | 85–95% | 80–93% |
| Noise | Very low — good for ADC/analog | Switching ripple 10–50 mV @ 100 kHz–1.5 MHz | Worse ripple |
| Dropout | AMS1117: 1.1 V; MCP1700: 0.18 V | Needs V_in ≥ V_out + ~1.5 V typically | V_in < V_out |
| Max current | AMS1117: 800 mA (with heatsinking) | MP1584: 3 A; LM2596: 2 A real-world | MT3608: ~1 A out at low boost ratio |

**Rules:**
- Battery → 5 V or 3.3 V logic rail: **buck**, always, if V_in − V_out > 2 V or current > 200 mA. Heat math for an LDO: P = (V_in − V_out) × I. From 2S (7.4 V) to 5 V at 1 A = 2.4 W — an AMS1117 in SOT-223 hits thermal shutdown at ~1.5 W without a big copper pour.
- Quiet rail for analog sensors / ADC reference: buck to an intermediate voltage, then **LDO** for the last 0.5–1 V (e.g. buck to 4.0 V → MCP1700-3.3 → clean 3.3 V).
- Single Li-ion cell (3.0–4.2 V) → 3.3 V: this straddles 3.3 V, so use a **buck-boost** (TPS63020) or accept an LDO with low dropout (MCP1700, works until cell hits ~3.5 V — wastes the bottom 20% of capacity).
- 5 V servos from 1S Li-ion: MT3608 boost works but budget 2× input current (5 V × 1 A out ≈ 3.7 V × 1.6 A in). One MT3608 per 2 servos max.
- Cheap MP1584/LM2596 modules: **set the output voltage with a multimeter BEFORE connecting the load.** They ship at random voltages, often 12+ V. Many a 3.3 V MCU has died this way. Add a drop of nail polish on the trimpot after setting.
- LM2596 modules from AliExpress are frequently fake (relabeled, 500 mA real limit, wrong switching frequency). MP1584 and genuine TI/Pololu modules are more reliable.

---

## 4. Battery Voltage Sensing (the divider everyone gets wrong)

ADC pins tolerate max 3.3 V (ESP32, Pico) or 5 V (Uno). Battery is higher → divide it down.

**Divider design:**

```
V_bat ──[ R1 ]──┬──[ R2 ]── GND
                └──> ADC pin
                └──[ 100 nF ]── GND   (noise filter, mandatory)
V_adc = V_bat × R2 / (R1 + R2)
```

| Battery | Max V | Target ADC | R1 | R2 | Ratio | Drain |
|---|---|---|---|---|---|---|
| 2S LiPo | 8.4 V | ≤3.0 V (ESP32 sweet spot) | 100 kΩ | 47 kΩ | 0.320 → 2.69 V max | 57 µA |
| 2S LiPo | 8.4 V | ≤3.3 V (Pico) | 68 kΩ | 33 kΩ | 0.327 → 2.74 V | 83 µA |
| 4×NiMH | 5.6 V | ≤3.3 V | 33 kΩ | 33 kΩ | 0.5 → 2.8 V | 85 µA |
| 3S LiPo | 12.6 V | ≤3.3 V | 100 kΩ | 33 kΩ | 0.248 → 3.13 V | 95 µA |
| 1S Li-ion | 4.2 V | ≤3.3 V | 100 kΩ | 220 kΩ | 0.687 → 2.89 V | 13 µA |

**Critical gotchas:**
- **ESP32 ADC is nonlinear and reads garbage above ~3.1 V and below ~0.1 V.** Use 11 dB attenuation and keep the divider output under 2.9 V. Calibrate against a multimeter — raw ESP32 ADC error is ±6%; with `esp_adc_cal` / MicroPython `ADC.read_uv()` (S2/S3/C3) it drops to ~±1%.
- **High divider impedance vs ADC sampling:** the ESP32/Pico ADC sample cap needs a source impedance < ~10 kΩ for accurate single reads. With a 100k/47k divider (Thevenin ≈ 32 kΩ), the 100 nF cap across R2 fixes this — it holds the voltage during sampling. Without the cap, readings sit 5–10% low and jump around.
- **Divider drains the battery forever**, even when "off". 57 µA kills a 2000 mAh pack in ~4 months. For products: high-side P-MOSFET switch on the divider, or use ≥1 MΩ total (with the cap, mandatory) accepting slower response.
- Read **under load and averaged** — battery voltage during a motor pulse is not state-of-charge:

```python
# MicroPython (ESP32) — calibrated battery read
from machine import ADC, Pin
import time

adc = ADC(Pin(34))                  # input-only pin, good for ADC
adc.atten(ADC.ATTN_11DB)            # full-scale ~3.1 V usable

DIVIDER = (100 + 47) / 47           # = 3.128
CAL = 1.000                          # multimeter_V / reported_V, set once

def battery_voltage(samples=16):
    total = 0
    for _ in range(samples):
        total += adc.read_uv()       # factory-calibrated on S2/S3/C3; on classic
        time.sleep_ms(2)             # ESP32 falls back to nominal — calibrate!
    return (total / samples) / 1_000_000 * DIVIDER * CAL
```

```cpp
// Arduino Uno (5 V tolerant ADC, 2S LiPo via 100k/47k)
const float DIVIDER = (100.0 + 47.0) / 47.0;
float batteryVoltage() {
  long sum = 0;
  for (int i = 0; i < 16; i++) { sum += analogRead(A0); delay(2); }
  return (sum / 16.0) * (5.0 / 1023.0) * DIVIDER;  // measure your real 5V rail;
}                                                   // USB "5V" is often 4.6-4.9V!
```

**Uno AREF trap:** `5.0/1023.0` assumes a true 5.000 V rail. On USB power the rail is 4.6–4.9 V → 5% error. Either measure VCC with a meter and hardcode it, or use the internal 1.1 V bandgap trick to compute VCC at runtime.

**Voltage → state-of-charge (resting, per Li-ion cell):** 4.20 V = 100%, 4.00 V = ~85%, 3.85 V = ~65%, 3.75 V = ~45%, 3.65 V = ~25%, 3.50 V = ~10%, 3.30 V = ~0% usable. Under load subtract I × R_int (~50 mV/A for a healthy cell). NiMH is flat (1.25–1.2 V) for 80% of discharge — voltage is a poor SoC indicator; just alarm at 1.1 V/cell.

---

## 5. Low-Battery Behaviors (limp home, save state)

A robot must never just die. Implement a 3-threshold state machine. Thresholds for **2S LiPo, measured under typical load** (subtract ~0.2 V from resting values):

| State | Threshold (2S) | Per Li-ion cell | 4×NiMH | Behavior |
|---|---|---|---|---|
| NORMAL | > 7.0 V | > 3.5 V | > 4.6 V | Full performance |
| LOW | ≤ 7.0 V | ≤ 3.5 V | ≤ 4.6 V | Warn (LED blink / beep), cap motor PWM at 60%, disable non-essential loads (camera LEDs, speaker) |
| CRITICAL | ≤ 6.6 V | ≤ 3.3 V | ≤ 4.2 V | **Limp home:** 30% PWM, return to base / stop in safe pose, save state to flash |
| CUTOFF | ≤ 6.4 V | ≤ 3.2 V | ≤ 4.0 V | Motors OFF, deep sleep or full shutdown. Going lower permanently damages Li-ion |

**Implementation rules:**
- **Hysteresis + debounce:** a motor surge dips voltage transiently. Only change state if the (averaged) reading stays below threshold for ≥ 3 s, and require +0.2 V above threshold to go back up. Without this the robot oscillates between states.
- **Latch CRITICAL and CUTOFF** — once entered, never auto-recover (voltage rebounds when load drops; that's not a charged battery).
- **Save state BEFORE cutting motors** if state matters (odometry pose, task progress): flash writes need ~20–100 ms and must finish while power is solid.

```python
# MicroPython — battery state machine with debounce + hysteresis
import time, json

NORMAL, LOW, CRITICAL, CUTOFF = 0, 1, 2, 3
THRESH = [99.0, 7.0, 6.6, 6.4]        # entry thresholds (V), index = state
HYST = 0.2
DEBOUNCE_MS = 3000

class BatteryMonitor:
    def __init__(self, read_v):
        self.read_v = read_v
        self.state = NORMAL
        self.avg = read_v()
        self._below_since = None

    def update(self):
        self.avg = 0.9 * self.avg + 0.1 * self.read_v()   # EMA smoothing
        nxt = self.state + 1
        if nxt <= CUTOFF and self.avg < THRESH[nxt]:
            if self._below_since is None:
                self._below_since = time.ticks_ms()
            elif time.ticks_diff(time.ticks_ms(), self._below_since) > DEBOUNCE_MS:
                self.state = nxt                            # latches: only moves down
                self._below_since = None
                self.on_state_change(nxt)
        elif self.state == LOW and self.avg > THRESH[LOW] + HYST:
            self.state = NORMAL                             # only LOW may recover
            self._below_since = None
        else:
            self._below_since = None

    def on_state_change(self, s):
        if s == LOW:
            set_max_pwm(0.6); start_warning_blink()
        elif s == CRITICAL:
            save_state()                                    # FIRST, while power is good
            set_max_pwm(0.3); begin_return_to_base()
        elif s == CUTOFF:
            motors_off()
            import machine
            machine.deepsleep()                             # µA-level draw

def save_state():
    with open('/state.json', 'w') as f:
        json.dump({'pose': get_pose(), 'task': get_task_progress()}, f)
        f.flush()
    # call in main loop: monitor.update() every ~100 ms
```

- **PWM cap, not speed cap:** in LOW/CRITICAL, clamp the duty cycle command (`duty = min(duty, max_pwm * 65535)`). This bounds current draw, flattens the sag, and buys real runtime.
- **ESP32 deep sleep ≈ 10 µA**, but the dev board's USB-UART chip + power LED add 1–10 mA. For real shutdown, control system power with a high-side P-MOSFET latch the MCU can release (soft power switch).
- **ROS2 pattern:** publish `sensor_msgs/BatteryState` at 1 Hz from the base node; a lifecycle manager node subscribes and transitions navigation to a `dock` behavior at CRITICAL via the Nav2 behavior tree (`BatteryCharging`/`IsBatteryLow` BT condition nodes exist in `nav2_behavior_tree` — set `min_battery: 0.25` on `IsBatteryLow` and remap `battery_topic`).

---

## 6. TP4056 Charging (1S Li-ion / LiPo)

The ubiquitous $1 module. Two variants exist — this matters:

- **Plain TP4056** (one chip): charger only. NO over-discharge or short protection.
- **TP4056 + DW01A + FS8205** (three chips, usually 6 pads: IN±, BAT±, OUT±): adds over-discharge cutoff (2.4 V — note: **lower than the 3.0 V you should use**, it's a last resort, not a fuel gauge), overcurrent (~3 A), and short protection. **Always buy this version.** Identify it by the OUT+/OUT− pads and the two extra chips.

**Wiring (protected version):**

| Pad | Connect to |
|---|---|
| IN+ / IN− (or USB-C/micro) | 5 V charge source, ≥ 1 A capable |
| B+ / B− | Battery terminals directly, short leads |
| OUT+ / OUT− | Robot load (through DW01 protection FETs) |

**Setting charge current:** R_prog on pin 2. Default 1.2 kΩ = 1 A. I_chg ≈ 1200/R_prog (A). For small cells charge at ≤ 1C: a 500 mAh cell needs R_prog = 2.4 kΩ (replace the 1.2 kΩ 0805 resistor) → 500 mA. Charging a 400 mAh cell at the default 1 A will overheat and swell it.

**Charge profile:** CC at I_set until 4.2 V, then CV taper; terminates at I_set/10. Red LED = charging, blue/green = done.

**The load-sharing trap (most important TP4056 gotcha):** powering the robot from OUT± **while charging** confuses termination — the chip sees load current as charge current, never terminates, and the cell sits at 4.2 V being micro-cycled (kills cells in months, mild fire risk). Fixes, in order of correctness:

1. **Proper load-sharing circuit** (do this for products): P-MOSFET (e.g. DMG3415, AO3401) + Schottky (SS34). When USB present, load runs from USB via the Schottky and the MOSFET disconnects the battery from the load; battery charges undisturbed. Gate to USB 5 V, source to BAT+, drain to load, Schottky from USB 5 V to load:

```
USB5V ──┬─────────|>|── (SS34) ──┬──> LOAD+
        │                        │
        └── gate ─┐              │
BAT+ ── source ──[P-FET]── drain ┘
(gate pulled to GND via 100 kΩ so FET is ON when no USB)
```
2. **Switch:** physically disconnect load while charging (fine for hobby robots).
3. Accept it for toys that are rarely left plugged in — but know the trade.

**More TP4056 rules:**
- One module per cell. **Never** charge a 2S pack with one TP4056, and never with two TP4056s sharing a ground (their grounds are at different pack potentials — instant short through USB grounds). For 2S use a dedicated 2S charger/BMS (e.g. 2S 8.4 V CC/CV module + balance board, or HX-2S-JH3 BMS + 8.4 V supply).
- Input must be 4.5–5.5 V. 9 V or 12 V input kills the chip (abs max ~8 V).
- Thermal: at 1 A with a 3.0 V cell the chip dissipates ~2 W and thermally throttles (this is normal, charge just slows). Don't enclose it in foam.
- The DW01's 2.4 V cutoff returns ~150 µA leakage; a robot left "off" on protection cutoff for weeks will deep-discharge the cell below recovery (< 2.0 V = do not recharge, recycle the cell).

---

## 7. Current Budget Worksheet (do this before choosing anything)

Sum the **worst case**, not typical:

| Load | Typical | Worst case (use this) |
|---|---|---|
| ESP32 | 80 mA | 500 mA (WiFi TX burst) |
| Pi Pico / Pico W | 25 / 45 mA | 100 mA |
| Raspberry Pi 4 | 600 mA | 3 A (boot + USB peripherals) |
| Raspberry Pi 5 | 800 mA | 5 A |
| TT gearmotor (6 V) | 150–250 mA | 1.5–2 A stall, ×2 on reversal |
| N20 (6 V HP) | 100 mA | 1.6 A stall |
| SG90 servo | 100–250 mA moving | 700 mA stall |
| MG996R servo | 500 mA | 2.5 A stall |
| NeoPixel (each) | 20 mA | 60 mA (full white) |
| HC-SR04 | 15 mA | 15 mA |
| OLED 128×64 | 20 mA | 30 mA |
| Camera (OV2640 on ESP32-CAM) | 120 mA | 300 mA |

Rules: regulator continuous rating ≥ 1.5× summed worst case. Motor driver continuous rating ≥ per-motor stall current (not running current!) — an L298N (2 A peak/channel, ~1 A continuous real-world) driving a motor with 2.5 A stall will die at the first wheel jam. Prefer TB6612FNG (1.2 A cont / 3.2 A peak, 90%+ efficient) or DRV8833 (1.5 A) over L298N in every new design — the L298N's 2.6 V drop also steals a third of a 6 V battery.

---

## 8. Debugging Checklist — "my robot resets / acts weird"

Work top to bottom; each step takes < 2 min:

1. **Multimeter on the logic rail, robot running motors.** Min/max capture if the meter has it. 3.3 V rail dipping below 3.0 V or 5 V below 4.7 V = brownout confirmed. No meter? Blink test: LED on a GPIO at 2 Hz from `setup()`/boot — if the blink pattern restarts when motors kick, the MCU is resetting.
2. **Check ground topology.** One continuous ground daisy-chain through a breadboard = motor return current flows through logic ground = ground bounce. Rewire to star ground at the battery.
3. **Look for shared regulator.** Servos or motors on the MCU board's 5 V pin? That pin can source ~500 mA through a polyfuse/diode at best. Move them to battery/buck direct.
4. **Measure battery under load.** Resting 8.1 V but 6.2 V under load = tired pack or high-resistance connection (oxidized AA holder springs are notorious — measure across each junction; > 0.1 V drop at any junction = fix it).
5. **Add/verify capacitors:** 1000 µF at motor driver VIN, 470 µF at regulator input, 100 nF at each IC, 100 nF across each motor. Electrolytic polarity matters — backwards = vents/explodes.
6. **Check the buck module output with a scope or meter** while motors run: ripple > 150 mV pk-pk on logic rail = bad/fake module or insufficient output cap; add 220 µF + 10 µF ceramic at output.
7. **ESP32 only:** `esptool.py` reset reason / `machine.reset_cause()` / Arduino `esp_reset_reason()`. `BROWNOUT_RESET` (or cause 4 in some ports) confirms power; `TG0WDT`/WDT points to software instead — stop blaming power.
8. **USB cable test:** programming over a thin USB cable while running motors? Cheap cables have 0.5 Ω+ round-trip; the board may run fine on battery and brown out on USB. Test on battery before debugging "the bug".
9. **Thermal:** touch (carefully) the regulator after 2 min. Too hot to hold = it's in thermal foldback and the rail is sagging cyclically (symptom: robot works for N minutes then degrades). Recompute Section 3 heat math.
10. **I2C/sensor corruption without resets** = motor brush noise. Add motor caps (step 5), shorten and twist motor leads, route them away from I2C lines, drop I2C to 100 kHz, add 2.2 kΩ pullups (not 10 kΩ).

## 9. Mistakes Everyone Makes (final scan list)

- 9V PP3 block powering motors. Never works. (§1)
- Logic and motors on one regulator. (§0)
- L298N chosen in 2026. Use TB6612FNG/DRV8833. (§7)
- Buck module connected before setting its trimpot. (§3)
- LDO from 7.4 V → 3.3 V at 500 mA = 2 W heater = thermal shutdown. (§3)
- Voltage divider output > 3.1 V on ESP32 ADC, no filter cap, no calibration. (§4)
- Battery thresholds without debounce/hysteresis → state thrashing. (§5)
- Plain TP4056 (no DW01) on an unprotected cell, or load attached during charge with no load-sharing circuit. (§6)
- Two TP4056s "making a 2S charger". Instant short via shared USB ground. (§6)
- Stall current ignored; driver sized to running current. (§7)
- Motor power through breadboard rails / DuPont jumpers. (§2)
- Instant direction reversal at full PWM. (§2)
- Disabling the ESP32 brownout detector instead of fixing power. (§2)
