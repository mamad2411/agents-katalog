---
name: dc-motors-l298n
description: "Use when driving brushed DC motors with an L298N dual H-bridge module (the red board with the big heatsink). Covers the voltage-drop trap that makes motors crawl, the 5V-EN jumper rules that brick boards, IN1/IN2/ENA truth tables, PWM frequency selection, stall-current sizing, and correct MicroPython/Arduino code patterns."
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


# DC Motors with the L298N Dual H-Bridge

The L298N is the most common motor driver in hobby robotics and the most misunderstood. It is a 1990s-era BJT (Darlington) H-bridge, NOT a MOSFET driver. That single fact explains almost every problem people have with it. Read the voltage-drop section before writing any code or recommending any battery.

## The #1 Trap: Voltage Drop (1.4–2.6 V is GONE before the motor sees anything)

The L298N's Darlington output stages drop voltage like diodes, not like MOSFET switches:

| Load current | Typical total drop (high+low side) | Worst case |
|---|---|---|
| 0.5 A | ~1.8 V | 2.5 V |
| 1.0 A | ~2.3 V | 3.2 V |
| 2.0 A | ~3.2 V | 4.9 V |

Practical consequences:

- **6V battery pack (4×AA) → motors see ~4.2–4.6 V.** "TT" yellow gearmotors rated 3–6 V will run, but slowly and with weak torque. Under load (robot on carpet) AA voltage sags further and the robot stalls.
- **Two 3.7V Li-ion (7.4 V nominal) → motors see ~5.0–5.6 V.** This is the correct pairing for 6V motors. **Size the battery UP to compensate for the drop — this is the rule.**
- **9V PP3 smoke-alarm battery → never.** It cannot source even 500 mA without collapsing. It is the most common cause of "robot resets when motors start."
- For 12V motors, supply 12 V and accept ~9.5–10.5 V at the motor, or use a 3S LiPo (11.1–12.6 V).

If the user/agent needs efficiency or is stuck with a low-voltage pack (e.g., 2×AA, single Li-ion, USB power bank), **recommend a TB6612FNG or DRV8833 instead** — those are MOSFET drivers with ~0.1–0.3 V drop. The L298N is only the right choice when it's what's physically on the bench.

## Power Wiring and the 5V-EN Jumper (this is where boards get bricked)

The blue screw terminal block has three positions: **+12V (VS, motor supply) | GND | +5V**. There is a jumper near it labelled **5V-EN** that connects an onboard 78M05 linear regulator.

**Jumper rules — memorize these:**

| Motor supply VS | 5V-EN jumper | +5V terminal usage |
|---|---|---|
| 7 V – 12 V | **ON** | Is an OUTPUT. You may power the MCU from it (≤ ~300 mA spare, regulator is linear and gets hot). |
| > 12 V (up to 35 V) | **OFF** (remove it) | Must FEED 5 V IN from an external source (the logic side needs it). Leaving the jumper on above ~12–16 V cooks the 78M05. |
| < 7 V | ON, but regulator output sags | Onboard 5 V becomes unreliable below ~7 V VS; power logic externally and treat +5V terminal as unused. |

**Never** feed external 5 V into the +5V terminal while the jumper is ON — you are back-driving the regulator output and one of the two 5 V sources loses.

**Common ground is non-negotiable.** The motor battery GND, the L298N GND, and the MCU GND must all be connected. PWM and direction signals are referenced to ground; without a shared ground the motor does nothing, twitches randomly, or half-works (the classic symptom: works when USB is plugged in, dies on battery). Run a dedicated wire MCU GND → L298N GND.

**Why separate supplies at all:** motor inrush/stall current causes supply sag and brush noise causes voltage spikes. Sharing the MCU's 5 V rail with motors causes brownout resets the moment the motors start. Motors get their own battery (or at minimum their own regulator + bulk capacitor); only ground is shared. Add a 470–1000 µF electrolytic across VS/GND at the driver if resets persist — many L298N clone boards only have a tiny 100 nF there.

## Pin Map (typical 2-motor robot)

| L298N pin | Connect to | Notes |
|---|---|---|
| ENA | MCU PWM pin (e.g., ESP32 GPIO25, Arduino D9) | Remove the black jumper cap first! Cap = permanently full speed. |
| IN1 | MCU GPIO (e.g., GPIO26 / D8) | Direction bit A1 |
| IN2 | MCU GPIO (e.g., GPIO27 / D7) | Direction bit A2 |
| IN3 | MCU GPIO (e.g., GPIO14 / D5) | Direction bit B1 |
| IN4 | MCU GPIO (e.g., GPIO12 / D4) | Direction bit B2 |
| ENB | MCU PWM pin (e.g., GPIO13 / D6) | Remove jumper cap |
| OUT1/OUT2 | Motor A terminals | Swap wires to reverse "forward" |
| OUT3/OUT4 | Motor B terminals | |
| +12V (VS) | Battery + (7.4 V Li-ion typical) | |
| GND | Battery − AND MCU GND | Two wires into one terminal is fine |
| +5V | MCU VIN/5V only if jumper ON and VS 7–12 V | Or leave unconnected |

Logic-high threshold is ~2.3 V, so **3.3 V MCUs (ESP32, Pico, ESP8266) drive it fine** — no level shifter needed. (The board is 5 V-tolerant input, not 5 V-requiring.)

ESP32 note: avoid GPIO 0, 2, 12, 15 for driver inputs if possible — they are boot-strapping pins; a driver input holding them at the wrong level can stop the ESP32 booting, and they glitch motors at reset. GPIO 12 in the table above works but expect a brief twitch at boot; prefer 25/26/27/32/33.

## IN1/IN2/ENA Truth Table (per channel)

| ENA | IN1 | IN2 | Result |
|---|---|---|---|
| PWM/HIGH | HIGH | LOW | Forward at PWM duty |
| PWM/HIGH | LOW | HIGH | Reverse at PWM duty |
| HIGH | LOW | LOW | **Brake** (both terminals shorted low — motor stops hard) |
| HIGH | HIGH | HIGH | **Brake** (shorted high) |
| LOW | X | X | **Coast** (outputs float — motor freewheels) |

Two distinct "stop" behaviors. Brake stops a robot in centimeters; coast lets it roll. For drive wheels you usually want brake; for a spinning flywheel you want coast. Choose deliberately — codebases that only ever set ENA=0 have robots that drift downhill.

**Alternative PWM scheme:** tie ENA HIGH (leave the jumper cap on) and PWM one of IN1/IN2 while holding the other LOW (sign-magnitude on the IN pins). This works and frees a PWM channel, but during PWM-off time the motor is in brake mode rather than coast (slow-decay), giving more linear low-speed response. Either scheme is valid; the ENA-PWM scheme is more common in tutorials, the IN-PWM scheme gives better low-speed control.

## PWM Frequency: 1–2 kHz Sweet Spot

- **Below ~200 Hz:** motor cogs/vibrates, control is jerky.
- **490 Hz / 980 Hz (Arduino `analogWrite` defaults):** works, audibly whines, acceptable.
- **1–2 kHz: the sweet spot for the L298N.** Smooth control, whine tolerable, switching losses negligible.
- **Above ~5 kHz:** the L298N's slow BJT switching (rise/fall in the µs range) means real switching losses, more heat, and *less* torque at a given duty. Do NOT use 20 kHz "inaudible" PWM with an L298N — that advice is for MOSFET drivers. The datasheet limit is 40 kHz; practical limit is ~10 kHz, optimum 1–2 kHz.
- On ESP32 (`PWM(freq=...)` or LEDC) and Pico, set 1000–2000 Hz explicitly. On classic Arduino, the default is fine; changing Timer0's prescaler breaks `millis()` — change Timer1/Timer2 pins instead if you must.

**Minimum effective duty:** brushed gearmotors through an L298N typically don't move below ~30–40 % duty (static friction + voltage drop). Map your speed range from `min_duty` to 100 %, not 0 to 100 %. Kick-start trick: pulse 100 % for 50 ms, then drop to the target duty — this gets reliable low-speed starts.

## Stall Current vs Running Current — How to Size Everything

Three currents matter; measure or look up all three:

1. **Free-run current** — motor spinning, no load. TT gearmotor: ~120–200 mA.
2. **Loaded running current** — robot actually driving. Typically 2–4× free-run.
3. **Stall current** — shaft locked. **Measure it: stall ≈ V_supply / R_winding.** Measure winding resistance with a multimeter across the motor terminals (nudge the shaft, take the lowest stable reading; readings vary with brush position). A TT motor with ~2 Ω at 6 V → ~3 A stall. Every motor start is a momentary stall — the inrush IS the stall current.

L298N limits: **2 A continuous per channel, 3 A peak** (datasheet, with heatsinking). Clone boards with the small bolt-on heatsink realistically handle **~1–1.5 A continuous** before thermal shutdown (the chip has internal thermal protection — symptom: motors mysteriously stop after 30–90 s, then work again after cooling).

Sizing rules:
- Motor **stall current must be < 3 A** or the driver enters current/thermal limiting on every hard start.
- Continuous loaded current should be **< 1.5 A per channel** for reliability.
- Battery must source **both motors' stall current simultaneously** (robot pushed against a wall = 2× stall). For two TT motors: budget ≥ 4–6 A burst. AA alkalines cannot do this; NiMH AA barely; Li-ion 18650 and LiPo can.
- Fuse the battery line at ~1.5× combined loaded current if you want survivable wiring mistakes.

## Flyback Protection: Already Included

The standard red L298N module has **eight discrete flyback diodes** (usually 1N4007 or Schottky) already on the board around the chip. Do **not** add external flyback diodes to the module — that advice applies to the bare L298N IC (which has none built in), not the module. What you SHOULD still add for noisy motors: a 100 nF ceramic capacitor soldered directly across each motor's terminals (and optionally terminal-to-can) to suppress brush noise that corrupts ADC readings and resets MCUs.

## MicroPython (ESP32 / Pico) — Known-Good Pattern

```python
from machine import Pin, PWM

PWM_FREQ = 1000  # 1 kHz — L298N sweet spot

class L298NMotor:
    def __init__(self, in1_pin, in2_pin, en_pin):
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        self.pwm = PWM(Pin(en_pin), freq=PWM_FREQ, duty_u16=0)

    def drive(self, speed):
        """speed: -100..100. Negative = reverse. 0 = brake."""
        speed = max(-100, min(100, speed))
        if speed > 0:
            self.in1.value(1); self.in2.value(0)
        elif speed < 0:
            self.in1.value(0); self.in2.value(1)
        else:
            self.in1.value(0); self.in2.value(0)  # brake (EN high) — see coast()
        # Map 1..100% to 35..100% duty: motors don't move below ~35%
        d = abs(speed)
        duty = 0 if d == 0 else int((35 + d * 0.65) / 100 * 65535)
        self.pwm.duty_u16(duty if d else 65535)  # full EN for hard brake at 0

    def coast(self):
        self.pwm.duty_u16(0)  # EN low → outputs float → freewheel

# ESP32 wiring example (avoid boot-strap pins 0/2/12/15)
left  = L298NMotor(in1_pin=26, in2_pin=27, en_pin=25)
right = L298NMotor(in1_pin=33, in2_pin=32, en_pin=14)

left.drive(70); right.drive(70)    # forward
left.drive(-50); right.drive(50)   # spin turn
left.drive(0); right.drive(0)      # brake
```

Pico note: `PWM` is identical; any GPIO is PWM-capable, but pins sharing a PWM slice (e.g., GP0/GP16) share frequency — pick en pins on different slices or use the same frequency everywhere (you should anyway).

ESP32 LEDC note: MicroPython ESP32 has a limited number of PWM timers; constructing all PWMs at the same `freq` avoids "out of timers" errors.

## Arduino C++ — Known-Good Pattern

```cpp
// L298N two-motor driver — Arduino Uno/Nano
// ENA=D9, ENB=D10 (Timer1 PWM ~490 Hz default — fine; do NOT touch Timer0/D5/D6
// prescaler or millis() breaks)
const uint8_t ENA = 9, IN1 = 8, IN2 = 7;
const uint8_t ENB = 10, IN3 = 5, IN4 = 4;
const uint8_t MIN_DUTY = 90;  // ~35% of 255 — below this motors stall

void setup() {
  pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT); pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  stopBrake();
}

// speed: -100..100
void driveMotor(uint8_t en, uint8_t a, uint8_t b, int speed) {
  speed = constrain(speed, -100, 100);
  digitalWrite(a, speed > 0);
  digitalWrite(b, speed < 0);
  uint8_t duty = (speed == 0) ? 255                       // brake: EN high, both IN low
               : map(abs(speed), 1, 100, MIN_DUTY, 255);  // skip dead zone
  analogWrite(en, duty);
}

void leftMotor(int s)  { driveMotor(ENA, IN1, IN2, s); }
void rightMotor(int s) { driveMotor(ENB, IN3, IN4, s); }

void stopBrake() { leftMotor(0); rightMotor(0); }
void stopCoast() { analogWrite(ENA, 0); analogWrite(ENB, 0); }

void loop() {
  leftMotor(70); rightMotor(70); delay(2000);   // forward
  stopBrake();                    delay(500);
  leftMotor(-60); rightMotor(60); delay(800);   // spin turn
  stopCoast();                    delay(2000);
}
```

ESP32 Arduino core ≥ 3.0: `analogWrite` works, but for explicit frequency use `ledcAttach(ENA, 1000, 8)` then `ledcWrite(ENA, duty)`.

**Direction-change rule:** when reversing at speed, insert a brief brake (≈50–100 ms) before commanding the opposite direction. Instant reversal demands ~2× stall current and slams the battery/driver. The patterns above don't enforce this — add it in robot-level code (ramping speed, e.g., ±10 per 20 ms tick, solves it for free and also stops wheelies).

## The 5 Mistakes Everyone Makes

1. **Leaving the ENA/ENB jumper caps on and PWM-ing anyway** → motor runs full speed regardless of code, or the MCU pin fights the 5 V pulled jumper. Remove the caps before wiring PWM.
2. **6V battery for 6V motors** → motors see 4.5 V and crawl. Budget +2.5 V above motor rating (7.4 V Li-ion for 6 V motors, 12 V for 9–10 V motors).
3. **No common ground between MCU and L298N** → dead/erratic motors, "works on USB, dies on battery." One GND wire fixes it.
4. **Powering motors from the MCU's 5 V rail / a 9V PP3 / a USB power bank** → brownout reset on motor start (power banks also auto-shut-off below ~50 mA load when motors idle).
5. **Swapping VS and +5V at the screw terminal** (12 V into the +5V terminal) → kills the logic side instantly, often the MCU too via the shared 5 V wire. Triple-check terminal silkscreen; clone boards vary in terminal order.

## Debugging Checklist (in order)

1. **Onboard red LED lit?** No → no VS power or blown board. Check battery and terminal polarity.
2. **Multimeter on OUT1/OUT2 with IN1=HIGH, IN2=LOW, ENA=HIGH:** should read ≈ VS − 2 V. Reads 0 → check ENA jumper removed and your ENA pin actually high; reads VS−2 but motor dead → motor or wire broken (spin shaft by hand, measure winding ~1–10 Ω).
3. **Motor runs full speed, ignores PWM** → ENA jumper cap still installed, or PWM wired to the jumper's 5 V pin instead of the ENA pin (they're adjacent).
4. **Runs then stops after 30–90 s, recovers when cool** → thermal shutdown. Current too high or duty too high for the heatsink; reduce load, add airflow, or upgrade to TB6612/DRV8833.
5. **MCU resets when motors start** → shared supply or sagging battery. Separate motor battery, common ground only, 470 µF across VS, 100 nF across each motor.
6. **One direction works, other doesn't** → that IN pin not toggling (verify with multimeter at the L298N header pin, not the MCU pin — finds broken jumper wires) or one half-bridge blown (channels die one direction at a time on overcurrent).
7. **Motor whines but doesn't turn** → duty below dead zone (~35 %), or mechanical bind, or voltage after the 2 V drop is below the motor's minimum. Try 100 % duty first; if it runs, it's the dead-zone mapping.
8. **Both motors slow/weak** → measure VS at the screw terminal under load. AA pack sagging from 6 V to 4.5 V is typical; battery is the fix, not code.

## When NOT to Use the L298N

- Motor stall current > 3 A (or > 1.5 A continuous): use a BTS7960/IBT-2 (43 A) or VNH5019.
- Battery ≤ 6 V or efficiency matters (small/solar/single-cell robots): TB6612FNG (1.2 A, 0.1 Ω-class drop) or DRV8833 (1.5 A, 2.7–10.8 V).
- Need silent 20 kHz+ PWM: any MOSFET driver; the L298N can't switch that fast efficiently.
- Stepper motors: it works (it's in every old tutorial) but has no current limiting — use an A4988/DRV8825/TMC2209 instead.

The L298N's virtues: it's everywhere, nearly indestructible (thermal + short protection), tolerates 35 V, and the screw terminals survive classrooms. Use it when it's on the bench; recommend better when specifying new hardware.
