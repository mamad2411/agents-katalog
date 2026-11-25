---
name: microbit
description: "Use when writing code or wiring designs for the BBC micro:bit (V1 or V2) — edge connector projects, motor drivers, sensors, radio, or breakout boards. Provides V1/V2 hardware differences, full edge-connector pinout, LED-matrix pin conflicts, power budget limits, radio group behaviour, and MicroPython vs MakeCode tradeoffs."
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


# BBC micro:bit (V1 & V2) — Hardware-Correct Coding

The micro:bit is NOT an Arduino. It is a 3.3 V board with a multiplexed LED display that
steals six of the edge-connector pins, a software radio that conflicts with Bluetooth,
and (on V1) only 90 mA of spare 3.3 V current. Most broken micro:bit robot code fails
for one of those three reasons. This skill exists so you never write that code.

## 1. Identify the board version FIRST

Never generate code without knowing (or branching on) the version. The differences are not cosmetic:

| Feature | V1.x | V2.x |
|---|---|---|
| MCU | nRF51822, Cortex-M0 @ 16 MHz | nRF52833, Cortex-M4F @ 64 MHz |
| Flash / RAM | 256 KB / 16 KB | 512 KB / 128 KB |
| MicroPython heap | ~10 KB usable (tiny!) | ~64 KB usable |
| Speaker | none | onboard speaker (shares **P0** audio default — see §5) |
| Microphone | none | onboard MEMS mic + LED indicator |
| Touch logo | none | capacitive touch logo (`pin_logo`) |
| 3.3 V regulator budget for accessories | **90 mA** | **190 mA** (270 mA total regulator) |
| Edge pads | same physical layout | same, plus notched pads for crocodile-clip grip |
| Power LED / USB | no power LED | red power LED, sleep mode (long-press reset) |
| Bluetooth + radio | BLE 4.1; can't run BLE and `radio` together | BLE 5.1; same restriction in MicroPython |
| I2C bus | one shared internal+external bus | **separate internal I2C** for accel/mag; external bus is free |
| `pin_speaker`, `microphone`, `audio` on P0 default | N/A | present |

Runtime detection in MicroPython:

```python
import os
is_v2 = 'nRF52' in os.uname().machine  # 'micro:bit v2.x with nRF52833'
```

Practical consequences:
- **V1 MicroPython runs out of memory constantly.** Importing `radio` + `music` + a
  driver module can exceed 10 KB heap. For V1, prefer MakeCode or trim imports ruthlessly.
- Code using `microphone`, `audio.play()` on speaker, `pin_logo`, or `power` module
  throws `NameError`/`AttributeError` on V1. Guard it.
- V2's separate internal I2C means external I2C devices can't address-clash with the
  onboard LSM303AGR. On **V1**, the accelerometer/magnetometer share the external bus
  at addresses **0x1D / 0x1E** (or 0x0E/0x1D depending on stock variant) — never assign
  an external device to those addresses on V1.

## 2. Edge connector pinout (the table you actually need)

25 pads total: 5 large ring pads (0, 1, 2, 3V, GND) + 20 small pads. Numbering left→right
with display facing you.

| Pin | Default function | Shared with LED display? | Notes |
|---|---|---|---|
| P0  | large pad, GPIO/ADC, touch | no | V2: default analog audio output pin |
| P1  | large pad, GPIO/ADC, touch | no | safe for anything |
| P2  | large pad, GPIO/ADC, touch | no | safe for anything |
| P3  | GPIO/ADC | **YES — display col** | |
| P4  | GPIO/ADC | **YES — display col** | |
| P5  | Button A | no | input w/ external pull-up on board; reading it = reading button A |
| P6  | GPIO | **YES — display** | |
| P7  | GPIO | **YES — display** | |
| P8  | GPIO | no | one of the few free digital pins — use it |
| P9  | GPIO | **YES — display** | |
| P10 | GPIO/ADC | **YES — display col** | |
| P11 | Button B | no | reading it = reading button B |
| P12 | GPIO | no | free (was "reserved" historically; usable on both versions) |
| P13 | GPIO / SPI SCK | no | default SPI clock |
| P14 | GPIO / SPI MISO | no | |
| P15 | GPIO / SPI MOSI | no | |
| P16 | GPIO | no | free; common choice for SPI CS |
| P19 | I2C SCL | no | has on-board pull-ups; don't repurpose as GPIO |
| P20 | I2C SDA | no | has on-board pull-ups; don't repurpose as GPIO |
| 3V  | 3.3 V out | | see power budget §4 |
| GND | ground | | three GND pads, all common |

There are no P17/P18 GPIO pads — those positions are 3V pads. ADC-capable pins:
**P0, P1, P2, P3, P4, P10** only. PWM: any GPIO, but only **three independent PWM
periods** at once on V1 (nRF51 has 3 PWM-capable timer setups); requesting a 4th
distinct frequency silently degrades. Keep all servo/motor PWM at the same period
(e.g. 20 ms / 50 Hz) and you can drive many channels.

### Truly safe pins with display ON

**P0, P1, P2, P8, P12, P13, P14, P15, P16** (+ P19/P20 as I2C only).
That is your whole budget. Design wiring around these nine pins.

## 3. The LED matrix pin conflict (the #1 micro:bit bug)

The 5×5 display is a multiplexed matrix scanned continuously by the runtime. It drives
**P3, P4, P6, P7, P9, P10** with row/column scan signals.

Symptoms when you use those pins with the display on:
- Sensor on P3/P4/P10 reads garbage that changes ~every few ms (you're reading the scan waveform).
- LED/transistor on P6/P7/P9 flickers dimly or pulses (scan signal driving your load).
- Writing those pins makes random display pixels light or whole rows go dark.
- `analog_read` on P3 returns wildly bouncing 0–1023 values with nothing connected — that's the matrix, not noise.

Fixes, in order of preference:
1. **Move to a safe pin** (P0/P1/P2/P8/P12/P13–P16). Always possible for ≤9 signals.
2. **Disable the display** if you genuinely need >9 GPIO:

```python
# MicroPython
from microbit import display
display.off()      # releases P3,P4,P6,P7,P9,P10 as plain GPIO
# display.on() re-claims them
```

```typescript
// MakeCode
led.enable(false)
```

```cpp
// Arduino C++ (micro:bit via nRF5 core) — there is no codal display unless you
// instantiate one; simply don't create MicroBitDisplay and the pins are free.
```

3. Never "disable display, use pin, re-enable" in a tight loop — the matrix scan
   restart causes visible flash and ~ms-level pin glitches.

Also remember: **P5 and P11 ARE buttons A and B.** Driving P5/P11 as outputs makes
button callbacks fire; conversely you can read external switches wired to them, but
they have on-board 4.7 k–10 k pull-ups to 3.3 V, so external circuits must be
open-drain / switch-to-GND style.

## 4. Power budget — the silent robot killer

The micro:bit's 3V pad is fed by the on-board regulator **after** the board's own load:

| Source | Available at 3V pad for your circuit |
|---|---|
| V1, USB powered | **~90 mA max** |
| V2, USB powered | **~190 mA max** |
| Either, battery pack (2×AAA via JST) | battery feeds 3V rail through protection; same order of limits, sagging as cells drain |

Hard rules:
- **Never power motors, servos, or >2 standard LEDs-worth of load from the 3V pad.**
  A single SG90 servo stalls at 600–800 mA — that's a brownout and reset on contact.
  Even an "idle" SG90 draws 100–250 mA while holding position.
- Motor/servo projects need a **separate battery** (e.g. 4×AA → motor driver), with
  **GND commoned** to micro:bit GND. The only wires from micro:bit to the driver are
  GND + logic signals.
- GPIO pins source/sink **0.5 mA** comfortably, ~5 mA absolute ceiling in
  high-drive mode (nRF "standard drive" is 0.5 mA spec). You cannot drive an LED to
  full brightness directly to spec — use ≥1 kΩ and accept dim, or use a transistor.
  Total GPIO current across all pins: keep under 15 mA (V1) / 30 mA (V2 high-drive aware).
- The board is **3.3 V logic, NOT 5 V tolerant.** A 5 V sensor output into any pin
  damages the nRF. HC-SR04 echo pin needs a divider (e.g. 1 kΩ/2 kΩ) or use a 3.3 V
  ultrasonic (RCWL-1601). Most motor driver INx pins accept 3.3 V logic fine
  (L9110S, DRV8833, TB6612: yes; bare L298N: marginal but works).
- Powering the micro:bit FROM a breakout: 3V pad accepts a **regulated 3.3 V input**
  only. Never feed 5 V into the 3V pad. USB and battery JST are the safe inputs.

## 5. V2 speaker / audio pin gotcha

On V2, audio (`music`, `audio`, `speech`) routes to the **onboard speaker AND P0**
by default. Consequences:
- A sensor or LED on P0 will buzz/glitch whenever any sound plays.
- To keep P0 clean:

```python
# MicroPython V2
from microbit import *
speaker.off()                 # silence speaker, audio still on P0 — NOT enough
audio.set_pin(pin1)           # better: move audio output entirely (V2 only)
# or use set_audio_pin in MakeCode: pins.setAudioPin(AnalogPin.P1)
```

If a project uses sound at all, treat **P0 as reserved** unless you explicitly re-route audio.

## 6. Radio — groups, ranges, and the BLE conflict

The `radio` module is a raw 2.4 GHz protocol (not Bluetooth, not WiFi).

```python
import radio
radio.config(group=42, power=7, length=64, channel=7, queue=10)
radio.on()
radio.send("L:128,R:90")
msg = radio.receive()   # None if queue empty — ALWAYS check for None
```

Facts that prevent bugs:
- **group** (0–255) is the only isolation mechanism. Default group is 0 — every
  classroom micro:bit left on defaults will receive your packets. **Always set an
  explicit group**, and in multi-robot settings give each pair its own group.
- **channel** (0–83) gives RF separation; group is just a filter byte on the same
  channel. Two heavy-traffic pairs on the same channel but different groups still
  collide at the RF level. For >3 simultaneous pairs, spread channels too.
- **power** 0–7; 7 ≈ 0 dBm ≈ 70 m line-of-sight, 0 ≈ −30 dBm ≈ same-desk. Use low
  power for desk testing to avoid cross-talk.
- Max payload: 32 bytes default, configurable to **251** via `length=`. `radio.send()`
  of a longer string silently truncates on V1 builds — keep messages short or chunk.
- `radio.receive()` returns **None** when empty and raises `ValueError` on a packet
  that isn't valid UTF-8 string data — if peers send bytes, use `radio.receive_bytes()`.
- Queue depth default 3 — fast senders overflow a slow receiver and packets drop
  silently. For telemetry, send state (latest values) not events, so drops don't matter.
- **You cannot use `radio` and Bluetooth simultaneously in MicroPython** (BLE is
  disabled in the MicroPython build anyway). In MakeCode, adding the Bluetooth
  extension *removes* the radio blocks (and vice versa) — they share the 2.4 GHz
  hardware and softdevice. Pick one per program.
- There is no ACK/delivery guarantee. For control links (e.g. RC car), the receiver
  should treat radio as lossy: apply a **deadman timeout** — stop motors if no packet
  for 500 ms:

```python
from microbit import running_time
last_rx = running_time()
while True:
    msg = radio.receive()
    if msg:
        last_rx = running_time()
        apply_command(msg)
    if running_time() - last_rx > 500:
        stop_motors()
```

## 7. MicroPython vs MakeCode vs Arduino — choose deliberately

| Criterion | MicroPython | MakeCode (Blocks/TS) | Arduino C++ |
|---|---|---|---|
| V1 viability | poor (10 KB heap) | **good** (compiled, small) | good |
| Speed | interpreted, ~100× slower than C | compiled to native — fast | fastest |
| Event handlers / multi-tasking | none built-in; manual loop + `running_time()` | `forever` loops + `onEvent` fibers — real cooperative scheduler | manual or codal fibers |
| Bluetooth services | not available | full BLE service blocks | via libs |
| Servo/PWM ergonomics | `pin.set_analog_period(20); pin.write_analog(…)` | `pins.servoWritePin` | Servo lib |
| Filesystem | small flash FS available | no | no |
| REPL debugging | **yes — serial REPL is gold** | no (serial print only) | serial print |
| Float math, ML, big programs on V2 | good | good | best |

Rules of thumb for code generation:
- **V1 + anything nontrivial → MakeCode/TypeScript.** MicroPython on V1 dies with
  `MemoryError` once you combine radio + a sensor driver + string formatting.
- **V2 + sensors/logic/REPL debugging → MicroPython.**
- Hard real-time (ultrasonic pulse timing, WS2812): MicroPython has `machine.time_pulse_us`
  and a built-in `neopixel` module that handle the timing in C — use those, never
  bit-bang timing loops in Python.
- MicroPython servo idiom (50 Hz, 1–2 ms pulse):

```python
from microbit import pin1
pin1.set_analog_period(20)            # 20 ms = 50 Hz, sets period for ALL analog pins!
def servo_angle(pin, deg):            # 0–180°
    pulse_ms = 1.0 + deg / 180.0      # 1.0–2.0 ms (trim per servo: often 0.6–2.4)
    pin.write_analog(int(1023 * pulse_ms / 20))
servo_angle(pin1, 90)
```

  Note `set_analog_period` is **global across pins** in micro:bit MicroPython — a
  servo at 50 Hz and an LED you want PWM-dimmed at 1 kHz cannot coexist; the LED
  will visibly flicker at 50 Hz. Accept it or move LED dimming to on/off.

- Arduino C++: use the official `Sandeep Mistry nRF5` core or (better) **CODAL via
  PlatformIO** (`platform = nordicnrf52`, `board = bbcmicrobit_v2`). Pin names map
  edge-pin → nRF GPIO differently between V1 and V2; always use the board variant's
  `PIN_BUTTON_A`-style macros, never raw nRF port numbers.

## 8. I2C and SPI specifics

- I2C: P19 = SCL, P20 = SDA, on-board pull-ups present (4.7 kΩ region) — do NOT add
  strong external pull-ups on short buses. Bus runs at 100 kHz default; 400 kHz works:
  `i2c.init(freq=400000, sda=pin20, scl=pin19)`.
- On **V1** the bus is shared with the onboard accel/mag — calling `i2c.init()` with
  a non-default frequency can break `accelerometer` readings until reset. Scan first:

```python
from microbit import i2c
print([hex(a) for a in i2c.scan()])
# V1 will show 0x1d/0x1e (or 0x0e) — onboard sensors. V2 shows only YOUR devices.
```

- SPI: `spi.init(baudrate=1000000, sclk=pin13, mosi=pin15, miso=pin14)`; CS is manual
  GPIO (use P16). Max reliable SPI clock over the edge connector + breakout wiring:
  ~4 MHz; the nRF can do more but ribbon/croc-clip wiring can't.
- Crocodile-clip projects: only P0/P1/P2/3V/GND are clippable. Touch sensing on
  P0–P2 (`pin0.is_touched()`) is resistive on V1 (needs GND contact with other hand);
  V2 adds true capacitive mode: `pin0.set_touch_mode(pin0.CAPACITIVE)`.

## 9. The five mistakes everyone makes

1. **Wiring a sensor/LED to P3/P4/P6/P7/P9/P10 with the display on.** Garbage reads,
   flicker, ghost pixels. Use the nine safe pins or `display.off()`.
2. **Powering a servo/motor from the 3V pad.** Brownout → board resets mid-move and
   the bug looks like a software crash. Separate supply, common ground, always.
3. **Leaving radio group at default 0** (or no deadman timeout) → robot obeys the
   neighbouring desk / drives into a wall when the controller sleeps.
4. **Writing V2-only code (`speaker`, `microphone`, `pin_logo`, `audio.set_pin`) for
   a V1 board**, or a memory-heavy MicroPython program for V1 — `MemoryError` at
   import time. Branch on version or target MakeCode for V1 fleets.
5. **Feeding 5 V into a pin** (HC-SR04 echo, 5 V sensor boards) or expecting a pin to
   drive an LED/motor directly. 3.3 V logic, ~0.5 mA spec drive — level-shift in,
   transistor out.

## 10. Debugging checklist

- Board resets when motors engage → power: scope/measure 3V rail; move motor supply off-board.
- Analog pin reads bouncing values with nothing attached → it's P3/P4/P10 with display on.
- `MemoryError` in MicroPython → V1, or string concatenation in a loop on V2; use
  `'%s' % x`-free fixed messages, `gc.collect()`, or switch V1 to MakeCode.
- Radio works on desk, fails across room → power level, or BLE pairing left enabled
  in a MakeCode build; also check both ends share group AND channel AND length config.
- I2C device not found → run `i2c.scan()`; empty list = wiring/power; address present
  but driver fails on V1 = clash with onboard 0x1D/0x1E.
- Servo jitters → 3V-pad power (fix supply) or another `write_analog` elsewhere
  changed the global analog period.
- Flashing works but program "does nothing" → MicroPython syntax error: connect serial
  REPL at **115200 baud** and read the traceback scrolling on the display/serial.
- Pin "input" always reads high on P5/P11 → those are the buttons with pull-ups; that's correct behaviour.
