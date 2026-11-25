---
name: steppers-buzzers
description: "Use when driving a 28BYJ-48 stepper via ULN2003, or generating sound from passive/active buzzers on Arduino, ESP32, or Raspberry Pi Pico. Provides exact half-step sequences, step math (2048 steps/rev), RPM/torque limits, holding-current thermal data, coil de-energizing, passive-vs-active buzzer identification, tone() timer conflicts, MicroPython PWM beep patterns, and RTTTL melody playback."
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


# 28BYJ-48 Stepper (ULN2003) + Buzzers — Expert Reference

## PART 1: 28BYJ-48 STEPPER MOTOR

### 1.1 Hardware Facts (memorize these numbers)

| Parameter | Value | Notes |
|---|---|---|
| Type | Unipolar, 5-wire, geared | Cannot be bipolar-driven without cutting the red wire trace |
| Rated voltage | 5 V (common); 12 V variant exists | Check the sticker — 12 V unit on 5 V barely moves |
| Coil resistance | ~50 Ω per coil (5 V version) | 12 V version ≈ 200 Ω |
| Current per energized coil | ~100 mA @ 5 V (5/50) | Half-step energizes 1–2 coils: 100–200 mA peak |
| Internal motor steps/rev | 32 (full-step), 64 (half-step) | Stride angle 11.25° full, 5.625° half |
| Gear ratio | 63.68395:1 (≈64:1) | Exact: 25792/405. NOT exactly 64! |
| Steps per output rev | **2048 half-steps** (nominal) | Exact: 4075.77 half-steps... see 1.2 |
| Wait — common convention | **4096 half-steps/rev** or **2048 full-steps/rev** | See 1.2, this trips everyone up |
| Max useful speed | ~15 RPM output shaft | Above this it stalls/skips under any load |
| Min step delay (half-step) | ~900 µs–1 ms reliable; 850 µs absolute floor unloaded | <850 µs = silent stall |
| Torque | ~34 mN·m (300 gf·cm) at low speed | Drops fast with RPM |
| Backlash | ~1–2° at output shaft (gear train) | Matters for bidirectional positioning |

### 1.2 The steps-per-revolution confusion (resolve it once)

- Internal rotor: 32 full steps/rev → 64 half steps/rev.
- Gear ratio ≈ 63.684:1.
- **Full-stepping**: 32 × 63.684 ≈ **2038 steps/rev** (everyone rounds to 2048).
- **Half-stepping**: 64 × 63.684 ≈ **4076 steps/rev** (everyone rounds to 4096).
- The task prompt convention "half-stepping 2048 steps/rev" appears in many tutorials because they count one half-step *pair* per loop iteration, or because libraries like Arduino `Stepper.h` use 2048 with the FULL-step sequence.
- **Rule for code**: if your loop advances ONE entry of the 8-entry half-step table per step, use **4096** per output revolution (4076 for precision work). If using the 4-entry full-step table, use **2048** (2038 precise).
- Cumulative error if you use 2048/4096 instead of exact: ~0.5% — about 1.8° per revolution. Fine for fans/dials; NOT fine for clocks or multi-turn positioning. For a clock, use 4075.7728395 and accumulate fractional steps.

### 1.3 Wiring: 28BYJ-48 → ULN2003 board → MCU

The motor's JST connector keys into the ULN2003 driver board — wiring errors only happen on the MCU side.

Motor wire colors (5 V version): Blue=coil4, Pink=coil3, Yellow=coil2, Orange=coil1, **Red=common +5 V** (goes to V+ via the ULN2003 board).

| ULN2003 board pin | Arduino Uno | ESP32 | Pi Pico (MicroPython) |
|---|---|---|---|
| IN1 | D8 | GPIO 14 | GP2 |
| IN2 | D9 | GPIO 27 | GP3 |
| IN3 | D10 | GPIO 26 | GP4 |
| IN4 | D11 | GPIO 25 | GP5 |
| VCC (motor power) | **5 V external supply** (≥500 mA) | 5 V / VIN | VBUS (5 V from USB) ok for ONE motor |
| GND | GND — **common with MCU GND** | GND | GND |

Rules:
- ULN2003 inputs are fine at 3.3 V logic (input threshold ~0.9–1.4 V per Darlington pair). ESP32/Pico drive it directly, no level shifter.
- Motor power: 200 mA peak per motor. USB 5 V handles one motor; two or more → external 5 V supply, common ground.
- **Never power the motor from the Arduino 5 V pin while also running servos/LEDs** — the onboard regulator browns out and the MCU resets mid-move (classic "stepper makes Arduino reboot" bug).
- The ULN2003 board LEDs (A–D) show coil activation — free debugging: at slow speed you should see a clean rotating LED pattern. Frozen/erratic pattern = wiring or sequence bug.
- ULN2003 has built-in flyback diodes (COM pin tied to V+ on these boards). No external diodes needed.

### 1.4 Step sequences (the exact tables)

**Half-step, 8 phases (smoothest, most torque-consistent, the default choice):**
```
Index: IN1 IN2 IN3 IN4
0:      1   0   0   0
1:      1   1   0   0
2:      0   1   0   0
3:      0   1   1   0
4:      0   0   1   0
5:      0   0   1   1
6:      0   0   0   1
7:      1   0   0   1
```
Forward = ascending index; reverse = descending. 4096 of these per output rev.

**Full-step, 4 phases, two-coil ("wave drive" 1-coil variant has ~30% less torque — don't use it):**
```
0: 1 1 0 0
1: 0 1 1 0
2: 0 0 1 1
3: 1 0 0 1
```
2048 per output rev. Slightly louder/rougher than half-step.

**The #1 mistake**: applying the sequence to pins in the wrong order. If the motor *vibrates/buzzes in place but doesn't rotate*, the sequence is reaching coils out of order — swap IN2↔IN3 in your pin list first (this fixes 90% of cases), motor wiring is rarely the issue.

### 1.5 Speed limits and timing

- Step period = delay between sequence advances. Half-step at 1 ms/step → 4096 ms/rev → **~14.6 RPM**. That is essentially the ceiling.
- Reliable range: **1–2 ms per half-step** (7–15 RPM). 3–5 ms for high-torque slow moves.
- Below ~900 µs the rotor can't keep up → it stalls SILENTLY (no error, motor hums, position lost). Open-loop steppers have no feedback; a stall means all subsequent position math is wrong.
- `delayMicroseconds()` / `time.sleep_us()` based loops are blocking. For non-blocking, advance the sequence from `millis()`/`time.ticks_us()` comparisons or a timer.
- No acceleration ramp needed at ≤15 RPM with this motor — the gear train provides enough mechanical advantage that you can start at full speed. (Unlike NEMA17s, where ramping is mandatory.)
- Don't use Arduino `Stepper.h` for half-stepping — it only does full-step. Use `AccelStepper` with `AccelStepper::HALF4WIRE` or roll your own (below).

### 1.6 Holding current and heat — DE-ENERGIZE WHEN IDLE

- If you leave the last step pattern latched, 1–2 coils stay energized: **100–200 mA continuous, ~0.5–1 W dissipated in a tiny plastic-geared motor**. After 10–30 minutes the case exceeds 60 °C; sustained operation deforms the nylon gears and shifts coil resistance.
- Holding torque you get from this is modest anyway, and the 64:1 gear train is largely self-holding (worm-like friction) — most loads won't backdrive it.
- **Always write 0,0,0,0 to all four inputs after a move completes** unless you specifically need active holding. This is the single most-forgotten line in 28BYJ-48 code.
- ULN2003 itself drops ~0.9–1.1 V (Darlington VCE(sat)), so the motor actually sees ~4 V — already torque-derated. Don't "compensate" by feeding 7 V; coils overheat.

### 1.7 MicroPython driver (Pi Pico / ESP32) — copy-paste correct

```python
from machine import Pin
import time

class Stepper28BYJ:
    HALF_SEQ = (
        (1,0,0,0),(1,1,0,0),(0,1,0,0),(0,1,1,0),
        (0,0,1,0),(0,0,1,1),(0,0,0,1),(1,0,0,1),
    )
    STEPS_PER_REV = 4096  # half-steps; use 4075.7728 for precision

    def __init__(self, in1, in2, in3, in4, delay_us=1200):
        self.pins = [Pin(p, Pin.OUT, value=0) for p in (in1, in2, in3, in4)]
        self.delay_us = delay_us  # 1200us = ~12 RPM, safe under load
        self.idx = 0
        self.position = 0  # signed half-steps from start

    def _apply(self, pattern):
        for pin, v in zip(self.pins, pattern):
            pin.value(v)

    def step(self, n):
        """n>0 = CW (viewed from shaft side), n<0 = CCW. Blocking."""
        direction = 1 if n > 0 else -1
        for _ in range(abs(n)):
            self.idx = (self.idx + direction) % 8
            self._apply(self.HALF_SEQ[self.idx])
            self.position += direction
            time.sleep_us(self.delay_us)

    def rotate_deg(self, deg):
        self.step(round(deg * self.STEPS_PER_REV / 360))

    def release(self):
        """CALL THIS after every move — kills holding current/heat."""
        self._apply((0, 0, 0, 0))

m = Stepper28BYJ(2, 3, 4, 5)
m.rotate_deg(90)
m.release()
```

Notes:
- `time.sleep_us()` on ESP32 under WiFi load can jitter; if steps skip, raise delay to 1500 µs or run the loop on core 1 / use a hardware Timer.
- Don't drop `delay_us` below 900 even though the loop "works" — verify under actual mechanical load.

### 1.8 Arduino C++ driver (non-blocking)

```cpp
const uint8_t MOTOR_PINS[4] = {8, 9, 10, 11};        // IN1..IN4
const uint8_t HALF_SEQ[8] = {                         // bit0=IN1..bit3=IN4
  0b0001, 0b0011, 0b0010, 0b0110,
  0b0100, 0b1100, 0b1000, 0b1001
};
const long STEPS_PER_REV = 4096;
const unsigned int STEP_INTERVAL_US = 1200;

long stepsRemaining = 0;
int8_t dir = 1;
uint8_t seqIdx = 0;
unsigned long lastStepUs = 0;

void applyPattern(uint8_t p) {
  for (uint8_t i = 0; i < 4; i++) digitalWrite(MOTOR_PINS[i], (p >> i) & 1);
}

void startMove(long halfSteps) {           // signed
  dir = (halfSteps >= 0) ? 1 : -1;
  stepsRemaining = abs(halfSteps);
}

void serviceStepper() {                    // call every loop()
  if (stepsRemaining == 0) return;
  unsigned long now = micros();
  if (now - lastStepUs < STEP_INTERVAL_US) return;
  lastStepUs = now;
  seqIdx = (seqIdx + dir + 8) % 8;
  applyPattern(HALF_SEQ[seqIdx]);
  if (--stepsRemaining == 0) applyPattern(0);  // auto de-energize
}

void setup() {
  for (uint8_t i = 0; i < 4; i++) pinMode(MOTOR_PINS[i], OUTPUT);
  startMove(STEPS_PER_REV / 4);            // 90 degrees CW
}

void loop() { serviceStepper(); }
```

With AccelStepper (preferred for multi-motor):
```cpp
#include <AccelStepper.h>
// HALF4WIRE pin order is IN1, IN3, IN2, IN4 — NOT sequential! Classic gotcha.
AccelStepper stepper(AccelStepper::HALF4WIRE, 8, 10, 9, 11);
void setup() {
  stepper.setMaxSpeed(900.0);      // half-steps/sec; ~13 RPM. >1000 risks stall
  stepper.setAcceleration(500.0);
  stepper.moveTo(4096);
}
void loop() {
  stepper.run();
  if (stepper.distanceToGo() == 0) stepper.disableOutputs(); // de-energize
}
```
**AccelStepper pin order for 4-wire is (IN1, IN3, IN2, IN4)** — using sequential order makes it vibrate without turning.

### 1.9 ROS2 / Raspberry Pi (Python, RPi.GPIO or gpiozero)

On a Pi, Linux scheduling jitter makes sub-millisecond software stepping unreliable while the system is loaded. Practical guidance:
- delay ≥ 2 ms per half-step (≈7 RPM max) from userspace Python; use `time.sleep(0.002)`.
- For real speed on a Pi, offload to a Pico/Arduino over serial, or use pigpio waveforms (`pigpio.wave_create`) which DMA-time the pulses in the kernel driver.
- In a ROS2 node, run the step loop in a dedicated thread; never step inside a subscriber callback with a spin-blocking sleep.

```python
# ROS2 Jazzy/Humble node skeleton (gpiozero on Pi 5: uses lgpio backend)
import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from gpiozero import OutputDevice
import time

HALF_SEQ = [(1,0,0,0),(1,1,0,0),(0,1,0,0),(0,1,1,0),
            (0,0,1,0),(0,0,1,1),(0,0,0,1),(1,0,0,1)]

class StepperNode(Node):
    def __init__(self):
        super().__init__('stepper_28byj48')
        self.pins = [OutputDevice(p) for p in (17, 27, 22, 23)]
        self.target = 0      # half-steps
        self.pos = 0
        self.lock = threading.Lock()
        self.create_subscription(Float32, 'stepper/angle_deg', self.on_angle, 10)
        threading.Thread(target=self.worker, daemon=True).start()

    def on_angle(self, msg):
        with self.lock:
            self.target = round(msg.data * 4096 / 360)

    def worker(self):
        idx = 0
        while True:
            with self.lock:
                delta = self.target - self.pos
            if delta == 0:
                for p in self.pins: p.off()   # de-energize while idle
                time.sleep(0.05)
                continue
            d = 1 if delta > 0 else -1
            idx = (idx + d) % 8
            for pin, v in zip(self.pins, HALF_SEQ[idx]): pin.value = v
            with self.lock: self.pos += d
            time.sleep(0.002)                  # 2ms: Pi-safe rate

def main():
    rclpy.init(); rclpy.spin(StepperNode())
```

### 1.10 Stepper debugging checklist (in order)

1. **Motor buzzes/vibrates, no rotation** → pin order wrong. Swap middle two pins (IN2↔IN3 in your array). For AccelStepper, confirm (IN1,IN3,IN2,IN4) order.
2. **Turns the wrong direction** → reverse sequence traversal, or reverse the pin array. (Both motors on a robot: one is usually mirrored.)
3. **No motion, no buzz, board LEDs dark** → no motor power or missing common ground. Check VCC at ULN2003, check GND continuity to MCU.
4. **LEDs cycle correctly but shaft is still** → motor connector unseated, or you have a 12 V motor on 5 V.
5. **Stalls at speed / loses position over time** → step delay too short. Set 1500 µs and binary-search down. Also check supply sag during moves (scope or multimeter min-hold on VCC; <4.5 V under load = inadequate supply).
6. **MCU resets when motor starts** → motor sharing the MCU's regulator. Separate 5 V supply, common ground, optionally 470 µF across motor VCC/GND.
7. **Motor hot when "idle"** → you never wrote 0000 after the move. Add `release()`/`disableOutputs()`.
8. **Position drifts ~0.5%/rev in long runs** → you used 2048/4096 instead of the true 2037.9/4075.8. Accumulate float steps.
9. **Random skipped steps on ESP32 with WiFi** → `sleep_us` jitter; use a hardware timer ISR or raise delay.
10. **Works unloaded, stalls with mechanism** → torque limit. Lower speed (raise delay), check binding/backlash in your mechanism; do NOT raise voltage.

---

## PART 2: BUZZERS

### 2.1 Active vs passive — identify before writing any code

| Test | Active buzzer | Passive buzzer |
|---|---|---|
| Apply steady DC (3–5 V) | Beeps continuously (internal oscillator, fixed ~2–4 kHz) | Faint click only |
| Multimeter resistance | ~hundreds of Ω–open, often a diode-like internal circuit | ~8–42 Ω (it's a coil/piezo element) |
| Look at it | Sealed back, often a sticker/drop of sealant on top, taller can | Exposed PCB / green board visible underneath, shorter |
| Markings | Often "+" marked, polarity matters | Frequently no polarity marking (piezo passive truly doesn't care; magnetic passive has weak polarity preference) |
| Code needed | `digitalWrite(HIGH)` = sound | Must supply a square wave (`tone()`/PWM) |

The defining failure modes:
- **Passive buzzer + digitalWrite(HIGH)** → silence (one click). Symptom: "my buzzer doesn't work."
- **Active buzzer + tone()** → distorted warble, can't change pitch. Symptom: "every note sounds the same."

Electrical:
- Typical 5 V active buzzer: ~30 mA. AVR pin limit is 40 mA absolute / 20 mA recommended → drive small ones directly, but anything >20 mA gets an NPN (2N2222: pin→1 kΩ→base, emitter→GND, buzzer between 5 V and collector) **with a flyback diode (1N4148) across MAGNETIC buzzers** — magnetic buzzers are coils.
- Piezo passive elements draw <10 mA — direct pin drive is fine. Add a 100–220 Ω series resistor with magnetic passive buzzers on direct drive.
- ESP32/Pico GPIO: 12 mA recommended max — transistor-drive any magnetic 5 V buzzer; a bare piezo disc is fine direct.
- 3.3 V logic driving a "5 V" active buzzer often produces weak/no sound — power the buzzer from 5 V via transistor.

### 2.2 Arduino tone() — timer conflicts (the part everyone hits)

`tone(pin, freq[, duration_ms])` facts:
- **Uses Timer2 on Uno/Nano/Mega (ATmega328/2560)**. Consequences:
  - **Conflicts with PWM on pins 3 and 11 (Uno/Nano)** — `analogWrite` on those pins breaks while tone is active and after (timer reconfigured). On Mega: pins 9 and 10.
  - Conflicts with any library using Timer2: `MsTimer2`, some IR libraries (older `IRremote` used Timer2 for receive on AVR — tone() + IR receive = broken IR), `TimerTwo`.
- **Servo library uses Timer1** → tone() and Servo coexist fine on Uno. But `NewTone`/`TimerFreeTone` alternatives exist if you need Timer2 back.
- Only **one tone() at a time** across all pins. Calling tone() on a second pin while the first plays does nothing until you `noTone(firstPin)`.
- Min frequency 31 Hz on 16 MHz AVR. Below that, tone() output is wrong.
- `tone()` with a duration is still non-blocking — it returns immediately and an ISR stops it. A melody loop therefore needs your own `delay(noteDuration)` between notes, plus a small gap (`delay(dur*0.30)` silence) or notes slur together.
- **ESP32 Arduino core**: classic `tone()` was historically absent; cores ≥2.0.x provide it via LEDC. If unavailable or conflicting, use LEDC directly: `ledcAttach(pin, freq, 10); ledcWriteTone(pin, freq);` (core 3.x API) — and note each LEDC tone consumes a channel (ESP32 has 16, shared with `analogWrite`).
- After `noTone(pin)` the pin may rest HIGH on some cores — follow with `digitalWrite(pin, LOW)` or an active buzzer wired pin→buzzer→GND will keep whining, and a transistor-driven one stays on.

```cpp
// Passive buzzer melody, correct timing, Uno pin 6 (NOT 3 or 11 — keep PWM free)
const int BUZZER = 6;
struct Note { unsigned int f; unsigned int ms; };
const Note melody[] = {{262,250},{330,250},{392,250},{523,500},{0,250},{523,250}};

void setup() {
  for (auto &n : melody) {
    if (n.f) tone(BUZZER, n.f);
    else     noTone(BUZZER);          // f==0 means rest
    delay(n.ms * 0.9);                // note body
    noTone(BUZZER);
    delay(n.ms * 0.1 + 20);           // articulation gap
  }
  digitalWrite(BUZZER, LOW);          // ensure silent idle
}
void loop() {}
```

Active buzzer (no tone() at all):
```cpp
const int BUZZER = 6;
void beep(unsigned int ms) { digitalWrite(BUZZER, HIGH); delay(ms); digitalWrite(BUZZER, LOW); }
void setup() { pinMode(BUZZER, OUTPUT); beep(100); delay(100); beep(100); }  // double beep
void loop() {}
```

### 2.3 MicroPython PWM beeps (Pico / ESP32)

Core pattern — **frequency sets pitch, duty sets volume, duty=0 (or deinit) = silence**:

```python
from machine import Pin, PWM
import time

buzzer = PWM(Pin(15))           # Pico: any GPIO. ESP32: avoid input-only 34-39

def beep(freq=1000, ms=100, duty=32768):   # duty_u16 max 65535; 32768 = 50% = loudest for piezo
    buzzer.freq(freq)
    buzzer.duty_u16(duty)
    time.sleep_ms(ms)
    buzzer.duty_u16(0)          # SILENCE = duty 0, do NOT just deinit mid-program

beep(440, 200)                  # A4
beep(880, 200)                  # A5
```

Gotchas:
- **Silence is `duty_u16(0)`, not `freq(0)`** — `freq(0)` raises ValueError on Pico and is invalid on ESP32.
- 50% duty = maximum loudness for a square wave into a piezo. Lower duty (e.g. 5000/65535) = quieter — this is your volume control.
- Pico PWM: 8 slices × 2 channels; **GPIOs sharing a slice share frequency** (GP0/GP1 same slice, GP2/GP3, ...). A buzzer and a motor-PWM on the same slice will fight over freq. Pick a GPIO whose slice partner is unused.
- Pico min PWM freq ≈ 8 Hz, max in audio range no issue. ESP32 MicroPython: PWM freq changes can glitch audibly; set freq before duty.
- ESP32 has a limited number of PWM timers (4 on classic ESP32 under MicroPython ≤1.19-ish; channels grouped per timer) — multiple PWM objects at different frequencies can exhaust timers and raise `ValueError: out of PWM timers`. Reuse one PWM object for the buzzer.
- On exit/Ctrl-C, PWM keeps running — wrap in try/finally with `buzzer.duty_u16(0)` or the buzzer screams forever.

Non-blocking beep (so robot keeps driving while beeping):
```python
from machine import Pin, PWM, Timer
buzzer = PWM(Pin(15)); buzzer.duty_u16(0)

def beep_async(freq=1500, ms=80):
    buzzer.freq(freq); buzzer.duty_u16(32768)
    Timer(-1).init(mode=Timer.ONE_SHOT, period=ms,
                   callback=lambda t: buzzer.duty_u16(0))
```

### 2.4 RTTTL melodies (Ring Tone Text Transfer Language)

Format: `Name:d=<default duration>,o=<default octave>,b=<BPM>:<notes>`
Note token: `[duration]note[#][octave][.]` — duration ∈ {1,2,4,8,16,32}, note ∈ {c,c#,d,d#,e,f,f#,g,g#,a,a#,b,p} (p = pause), `.` = dotted (×1.5).

Timing math: whole note ms = `(60000 / BPM) * 4`; a duration-d note = whole/d.

Frequency: `f = 440 * 2^((semitones from A4)/12)`. RTTTL octave 5 a = A5 = 880 Hz in most players (RTTTL octaves 4–7 map a4=440).

Complete MicroPython RTTTL player (correct parser — handles the classic pitfalls: duration digits before the note, dot AFTER the octave digit, '#'):

```python
from machine import Pin, PWM
import time

NOTE_SEMITONE = {'c':0,'c#':1,'d':2,'d#':3,'e':4,'f':5,'f#':6,'g':7,'g#':8,'a':9,'a#':10,'b':11}

def rtttl_play(pwm, tune, volume=32768):
    name, defaults, notes = tune.split(':')
    d, o, b = 4, 6, 63
    for part in defaults.split(','):
        k, v = part.strip().split('=')
        if k == 'd': d = int(v)
        elif k == 'o': o = int(v)
        elif k == 'b': b = int(v)
    whole_ms = 240000 // b
    for tok in notes.split(','):
        tok = tok.strip().lower()
        i = 0
        # 1) duration digits
        num = ''
        while i < len(tok) and tok[i].isdigit(): num += tok[i]; i += 1
        dur = int(num) if num else d
        # 2) note letter (+ optional #)
        note = tok[i]; i += 1
        if i < len(tok) and tok[i] == '#': note += '#'; i += 1
        # 3) dot may appear before OR after octave (both occur in the wild)
        dotted = False
        if i < len(tok) and tok[i] == '.': dotted = True; i += 1
        octv = o
        if i < len(tok) and tok[i].isdigit(): octv = int(tok[i]); i += 1
        if i < len(tok) and tok[i] == '.': dotted = True
        ms = whole_ms // dur
        if dotted: ms = ms * 3 // 2
        if note == 'p':
            pwm.duty_u16(0)
        else:
            semis = NOTE_SEMITONE[note] + (octv - 4) * 12 - 9  # offset from A4=440
            freq = round(440 * (2 ** (semis / 12)))
            pwm.freq(freq); pwm.duty_u16(volume)
        time.sleep_ms(ms * 9 // 10)
        pwm.duty_u16(0)
        time.sleep_ms(ms // 10)         # articulation gap
    pwm.duty_u16(0)

buzzer = PWM(Pin(15)); buzzer.duty_u16(0)
rtttl_play(buzzer, "Mario:d=4,o=5,b=100:16e6,16e6,32p,8e6,16c6,8e6,8g6,8p,8g")
rtttl_play(buzzer, "Nokia:d=4,o=5,b=180:8e6,8d6,f#,g#,8c#6,8b,d,e,8b,8a,c#,e,2a")
```

Arduino: use the `anyrtttl` or `PlayRtttl` library (non-blocking variants available), or port the parser above with `tone()/noTone()`.

RTTTL parser bugs that recur:
1. Forgetting `p` (pause) → KeyError mid-tune.
2. Treating the dot as only-after-note → wrong rhythm on dotted notes (`8e.6` vs `8e6.` both occur).
3. Octave off-by-one (RTTTL `a5` = 880 Hz, not 440) → tune plays an octave low.
4. No inter-note gap → repeated notes ("e6,e6,e6") merge into one long tone.
5. Integer division on whole_ms with high BPM → cumulative tempo drift; acceptable, but don't also truncate the gap to 0.

### 2.5 Buzzer debugging checklist

1. **Total silence** → run the identify test (2.1): steady HIGH. Beeps? It's active — your tone code is unnecessary. Clicks once? It's passive — you need PWM/tone. No click? Wiring/polarity/dead pin.
2. **Continuous whine that never stops** → forgot `noTone()` / `duty_u16(0)` on a code path (especially exceptions/Ctrl-C). Add try/finally.
3. **All notes same pitch** → it's an active buzzer; pitch is fixed by its internal oscillator. Swap to a passive buzzer for melodies.
4. **Very quiet on ESP32/Pico** → 3.3 V drive into a 5 V-rated magnetic buzzer; transistor-drive from 5 V, or accept it, or use a piezo.
5. **tone() broke my PWM/IR/servo timing** → Timer2 conflict (Uno pins 3/11, Mega 9/10; IR libraries). Move PWM pins, or use `TimerFreeTone`.
6. **Second buzzer won't play simultaneously (AVR)** → tone() is single-channel by design. Use two PWM channels manually or a tone-multiplexing library.
7. **Random ValueError on Pico PWM** → `freq(0)` for silence, or two PWM pins on the same slice with different frequencies. Use duty 0 for silence; check slice pairing (GPn and GPn+1 for even n share).
8. **Buzzer clicks when motors start** → supply dip coupling; decouple with 100 µF near the buzzer driver, separate motor supply.
9. **Melody tempo drags or notes slur** → no articulation gap (add 10% silence), or blocking sleeps fighting other tasks — go non-blocking (Timer one-shot pattern in 2.3).
