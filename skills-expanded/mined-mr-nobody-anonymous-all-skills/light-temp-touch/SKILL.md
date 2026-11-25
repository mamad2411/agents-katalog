---
name: light-temp-touch
description: "Use when wiring or coding LDRs/photodiodes, temperature sensors (TMP36, DS18B20, NTC thermistor), or capacitive touch inputs (ESP32 touchRead, TTP223). Provides voltage-divider sizing math, sensor selection rules, ADC pitfalls, touch debouncing patterns, and working MicroPython + Arduino code."
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


# Light, Temperature & Touch Sensors

Hard rules first, then per-sensor detail.

## Quick Selection Matrix

| Need | Pick | Why not the others |
|---|---|---|
| "Is it bright or dark?" indoor | LDR + 10K divider | Cheapest, no code complexity |
| Light level for control loop, fast response | Photodiode (BPW34) + transimpedance or load resistor | LDR is too slow (tens of ms–seconds) |
| Detect IR remote / pulses / line following | Photodiode or phototransistor | LDR cannot see 38 kHz pulses, period |
| Room temp, ±2 °C OK, analog input free | TMP36 | Simplest, but ADC-quality dependent |
| Accurate temp (±0.5 °C), long cable, multiple sensors | DS18B20 | One-wire bus, digital, immune to cable resistance |
| Cheap temp embedded in a divider you already have | NTC 10K thermistor | Needs Steinhart–Hart math, nonlinear |
| Touch button on ESP32, zero extra parts | `touchRead()` on a touch pin | Free, but needs calibration + debounce |
| Touch button on any other MCU | TTP223 module | Outputs clean digital HIGH/LOW |

---

## 1. LDR (Photoresistor) — Voltage Divider Sizing

### The circuit
```
3V3 ──[ LDR ]──┬──[ R_fixed ]── GND
               │
              ADC pin
```
With LDR on top: **more light → higher ADC reading** (LDR resistance drops, node pulls toward 3V3). Swap positions to invert. Pick the orientation that matches your code's intuition and document it.

### Sizing R_fixed — the rule everyone gets wrong
The divider has maximum sensitivity when **R_fixed ≈ √(R_dark × R_light)** — the geometric mean of the LDR's resistance at the two extremes you care about.

Typical GL5528 LDR:
- Bright sunlight: ~1 kΩ
- Indoor room light: ~8–20 kΩ
- Darkness: ~500 kΩ–1 MΩ

| Application | R_dark/R_light range | R_fixed |
|---|---|---|
| Indoor light/dark detection | 10K ↔ 1M | **10 kΩ** (the standard answer) |
| Outdoor daylight tracking | 1K ↔ 100K | 4.7–10 kΩ |
| Distinguishing dim levels (night light) | 100K ↔ 1M | 100 kΩ–330 kΩ |

10K indoor is the right default — with R_fixed too small (1K) everything indoor reads near rail; too big (1M) and bright/dim are indistinguishable.

### Current draw
Worst case (LDR fully lit, ~1K): I = 3.3 V / (1K + 10K) ≈ 0.3 mA. Fine. Never connect an LDR straight to a GPIO without the fixed resistor — at full light it can pass >3 mA and the node voltage is meaningless anyway.

### MicroPython (ESP32)
```python
from machine import ADC, Pin
ldr = ADC(Pin(34))            # input-only pin, ideal for ADC
ldr.atten(ADC.ATTN_11DB)      # full 0-3.3V range (actually ~0-3.1V usable)
raw = ldr.read()              # 0-4095
# Don't convert to lux. Calibrate empirically:
DARK_THRESHOLD = 800          # measure YOUR room, hardcode after testing
is_dark = raw < DARK_THRESHOLD
```

### Arduino C++ (Uno / ESP32)
```cpp
const int LDR_PIN = A0;        // ESP32: use GPIO 34/35/36/39 (ADC1)
int raw = analogRead(LDR_PIN); // Uno: 0-1023, ESP32: 0-4095
// Smooth it — LDR + mains lighting flickers at 100/120 Hz:
long sum = 0;
for (int i = 0; i < 16; i++) { sum += analogRead(LDR_PIN); delay(2); }
int smoothed = sum / 16;
```

### ESP32 ADC traps (apply to ALL analog sensors here)
1. **ADC2 pins (GPIO 0,2,4,12-15,25-27) are unusable while WiFi is on.** Use ADC1 only: GPIO 32, 33, 34, 35, 36, 39.
2. ESP32 ADC is nonlinear and dead below ~0.13 V and above ~3.1 V at 11 dB attenuation. Don't expect readings near 0 or 4095 to be proportional.
3. Always set attenuation explicitly (`ATTN_11DB`); default 0 dB clips at ~1.1 V.

### LDR vs photodiode response time
- **LDR (CdS cell): 10–100 ms rise, up to several SECONDS to recover in the dark** (resistance "memory" effect). Useless for anything pulsed, fast-moving, or PWM-lit. Also: CdS is RoHS-restricted in the EU — photodiodes/phototransistors are the modern replacement.
- **Photodiode (BPW34): nanoseconds–microseconds.** Use for line followers, encoders, IR communication, laser tripwires.
- Photodiode quick circuit (photoconductive, no op-amp): reverse-biased diode in series with 100K–1M load resistor to GND, read voltage across resistor. Larger R = more sensitivity, slower response (RC with junction capacitance).
- A **phototransistor** (e.g. PT334) is the middle ground: photodiode speed class (~10 µs), LDR-like signal amplitude, drop-in replacement in an LDR divider with R_fixed ≈ 10K.

---

## 2. Temperature: TMP36 vs DS18B20 vs Thermistor

### TMP36 (analog, 3-pin TO-92)
- Output: **500 mV at 0 °C, +10 mV/°C**. So 750 mV = 25 °C.
- Formula: `tempC = (voltage_V - 0.5) * 100`
- Runs on 2.7–5.5 V. Output is ratiometric to nothing — it's an absolute voltage, so **your ADC reference accuracy = your temperature accuracy**. ESP32's sloppy ADC gives ±2–3 °C error; Uno with 5 V reference jitter similar.
- **The classic mistake: TMP36 pinout is the MIRROR of an LM35 and of what the flat-face diagram suggests.** Flat face toward you, pins down: left = +Vs, middle = Vout, right = GND. Wiring it backward makes it heat up to ~80 °C and read garbage — if your TMP36 is warm to the touch, it's backwards. It usually survives if corrected quickly.
- Add a 0.1 µF decoupling cap V+ to GND right at the sensor.

```cpp
// Arduino Uno (5V ref)
float v = analogRead(A0) * 5.0 / 1024.0;
float tempC = (v - 0.5) * 100.0;
```
```python
# ESP32 MicroPython — use read_uv() to dodge ADC nonlinearity (v1.18+)
from machine import ADC, Pin
adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)
temp_c = (adc.read_uv() / 1_000_000 - 0.5) * 100
```

### DS18B20 (digital, 1-Wire)
Choose this when: you need ±0.5 °C, the sensor is on a cable >20 cm, you want multiple sensors on one pin, or the host ADC is bad (ESP32 — almost always pick DS18B20 over TMP36 on ESP32).

Wiring: VDD→3V3, GND→GND, DQ→any GPIO with a **4.7 kΩ pull-up from DQ to 3V3. The pull-up is not optional.** Without it you read 85 °C (power-on default) or -127 °C / CRC errors.

- **Reads of exactly 85.0 °C = the conversion never ran** (you read before issuing convert, or power glitched). Not a real temperature.
- **-127 °C (Arduino lib) / CRC fail = bus problem**: missing pull-up, bad ground, counterfeit chip.
- Conversion takes **750 ms at 12-bit**. Don't block: start conversion, do other work, read later. At 9-bit it's 94 ms but resolution drops to 0.5 °C.
- Parasite power (2-wire) works but is flaky with counterfeits; wire all 3 pins.
- Waterproof-probe versions: red=VDD, black=GND, yellow=DQ (usually — verify, clones vary).

```cpp
// Arduino: OneWire + DallasTemperature libs
#include <OneWire.h>
#include <DallasTemperature.h>
OneWire oneWire(4);
DallasTemperature sensors(&oneWire);
void setup() { sensors.begin(); sensors.setWaitForConversion(false); }
void loop() {
  sensors.requestTemperatures();        // non-blocking due to flag above
  delay(800);                           // or do real work for 750ms+
  float t = sensors.getTempCByIndex(0);
  if (t == DEVICE_DISCONNECTED_C) { /* bus fault: check 4.7K pull-up */ }
}
```
```python
# MicroPython (ds18x20 built in)
import onewire, ds18x20, time
from machine import Pin
ow = onewire.OneWire(Pin(4))
ds = ds18x20.DS18X20(ow)
roms = ds.scan()                 # empty list => wiring/pull-up problem
ds.convert_temp()
time.sleep_ms(750)               # mandatory wait at 12-bit
for rom in roms:
    print(ds.read_temp(rom))
```

### NTC Thermistor (10K, B=3950)
Use only when cost matters or it's already in the divider (e.g., 3D-printer hotends). Circuit: same divider as the LDR — 3V3 → thermistor → node(ADC) → 10K → GND. 10K fixed resistor matches the 10K-at-25°C thermistor for best mid-range sensitivity.

Simplified B-equation (good to ~±1 °C over 0–50 °C):
```python
import math
def thermistor_c(raw, raw_max=4095, beta=3950, r_fixed=10_000, r0=10_000, t0=298.15):
    if raw == 0 or raw == raw_max: return None      # open/short
    r_therm = r_fixed * raw / (raw_max - raw)        # thermistor on TOP of divider
    inv_t = 1/t0 + math.log(r_therm / r0) / beta
    return 1/inv_t - 273.15
```
Mistakes: using the B-equation far outside 0–50 °C (use full Steinhart–Hart), forgetting self-heating (keep divider current < 0.2 mA), and mixing up which leg of the divider the thermistor occupies (inverts the curve).

---

## 3. Capacitive Touch

### ESP32 native touch (no external parts)
Touch-capable pins (classic ESP32): T0=GPIO4, T1=GPIO0, T2=GPIO2, T3=GPIO15, T4=GPIO13, T5=GPIO12, T6=GPIO14, T7=GPIO27, T8=GPIO33, T9=GPIO32. (Note T1/T2 are strapping pins — prefer T0, T3–T9. **ESP32-S2/S3 use different pins AND inverted semantics: touch RAISES the reading instead of lowering it.**)

Electrode = any bare wire, copper tape, or pad. Keep the wire < ~20 cm or baseline drifts wildly.

Classic ESP32 behavior: `touchRead()` returns ~50–100 untouched, **drops** to ~10–30 when touched. Values are board- and wire-dependent — **never hardcode a threshold from a tutorial; calibrate at boot**:

```cpp
// Arduino C++ (classic ESP32)
const int TPIN = T0;             // GPIO4
int baseline;
void setup() {
  long sum = 0;
  for (int i = 0; i < 32; i++) { sum += touchRead(TPIN); delay(10); }
  baseline = sum / 32;           // calibrate while NOT touching
}
bool touched() { return touchRead(TPIN) < baseline * 0.7; }  // 30% drop
```
```python
# MicroPython
from machine import TouchPad, Pin
import time
tp = TouchPad(Pin(4))
baseline = sum(tp.read() for _ in range(32)) // 32
def touched():
    return tp.read() < baseline * 0.7
```

### Debouncing touch (mandatory — raw reads chatter badly)
Capacitive readings are noisy near the threshold; a finger approaching produces a ragged transition. Require N consecutive agreeing samples:

```cpp
// Debounce + edge detection: fires once per touch
bool stableTouch = false;
int agree = 0;
const int NEED = 4;              // 4 samples * 10ms = 40ms latency

void loop() {
  bool rawT = touchRead(TPIN) < baseline * 0.7;
  if (rawT != stableTouch) {
    if (++agree >= NEED) {
      stableTouch = rawT;
      agree = 0;
      if (stableTouch) onTouchPressed();   // rising edge only
    }
  } else agree = 0;
  delay(10);
}
```
Same pattern in MicroPython — count consecutive samples, flip state at N, act on the press edge only.

Avoid `touchAttachInterrupt()` for buttons unless you also debounce in the handler — it fires repeatedly while touched and on noise spikes.

### Touch gotchas
1. **WiFi TX changes touch baselines** (shared RF/power domain). Calibrate after `WiFi.begin()`, and use relative (% of baseline) thresholds, not absolute numbers.
2. **Battery vs USB power shifts readings** — USB ground-couples your body to the board, making touches "stronger". Test on the final power source.
3. Long/coiled electrode wires act as antennas; readings drift with humidity and nearby hands. Re-baseline slowly (e.g., drift baseline 1 count/second toward current untouched reading).
4. GPIO0/GPIO2/GPIO15 (T1/T2/T3) are boot-strapping pins — touch hardware on them can prevent flashing/booting.
5. For non-ESP32 boards (Uno, Pico): use a **TTP223 module** (VCC 2–5.5 V, clean digital out, jumpers select active-high/low and momentary/toggle) — treat it as a plain button, simple digital-read debounce suffices. RP2040/Pico has no native touch peripheral; CircuitPython's `touchio` bit-bangs it with a 1 MΩ pull-down on the pin.

---

## Debugging Checklist

**LDR reads constant ~4095 or ~0:** fixed resistor missing/wrong leg, or wrong ADC pin (ESP32: confirm ADC1 pin, WiFi off ADC2). Cover/uncover the LDR — if value doesn't move at all, the divider node isn't on the ADC pin.

**TMP36 reads ~ -50 °C:** output pin floating (broken wire) → ADC reads 0. Reads ~80 °C and chip is warm: **wired backwards**.

**DS18B20 reads 85 °C:** conversion not started/finished — add the 750 ms wait. Reads -127/CRC errors: add the 4.7K pull-up DQ→3V3.

**Thermistor temp moves the WRONG direction:** thermistor and fixed resistor swapped relative to your formula.

**touchRead() returns 0 always:** on some Arduino-ESP32 core versions a read on a non-touch pin or during WiFi init returns 0 — verify the pin is in the T0–T9 list.

**Touch fires randomly at night / when unplugged from USB:** floating ground, threshold too tight — widen to 40% drop and add the consecutive-sample debounce.

**ADC values jump ±100 counts:** normal on ESP32. Median-of-5 or average-of-16 every analog read; never compare a single raw sample against a threshold.
