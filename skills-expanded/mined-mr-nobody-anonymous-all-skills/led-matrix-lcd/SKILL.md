---
name: led-matrix-lcd
description: "Use when wiring or coding MAX7219 LED matrix chains, WS2812B/NeoPixel addressable strips, or 16x2/20x4 character LCDs with PCF8574 I2C backpacks on Arduino, ESP32, Raspberry Pi Pico, or Raspberry Pi. Provides exact wiring tables, voltage/level-shifting rules, current budgets, timing constraints, working MicroPython/Arduino/Python code patterns, and debugging checklists for displays that show nothing, garbage, or wrong colors."
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


# LED Matrix, Addressable Pixels & Character LCD — Expert Reference

Three display families, three completely different electrical contracts:

| Display | Protocol | Logic level | Power | Typical fail mode |
|---|---|---|---|---|
| MAX7219 8x8 matrix / 7-seg | SPI-like (CLK/DIN/CS), 10 MHz max | **5V logic required** (VIH = 3.5V min at 5V supply) | 5V, ~330 mA max per module all-on | Garbage after first module in chain; dim/flicker |
| WS2812B / NeoPixel | Single-wire, 800 kHz, strict ±150 ns timing | VIH = 0.7 × VDD → **3.5V at 5V supply** | 5V, 60 mA/pixel full white | First pixel green/flicker (level shift), brownout resets |
| HD44780 16x2 + PCF8574 I2C backpack | I2C @ 100 kHz, addr 0x27 or 0x3F | 5V module; I2C lines OK from 3.3V host if no strong 5V pullups (most backpacks have 4.7k to 5V — usually tolerated, see notes) | 5V, ~25 mA w/ backlight | Blank squares row 1 (contrast), nothing (wrong address) |

---

## 1. MAX7219 — 8x8 Matrix and 7-Segment Chains

### Electrical facts (from datasheet, not folklore)

- Supply: 4.0–5.5V. **Run it at 5V.** At 3.3V supply it is out of spec.
- Logic thresholds at VCC=5V: VIH min = 3.5V. **A 3.3V MCU output (3.3V high) is below spec.** It often "works" on one module then corrupts on chains — use a level shifter (74HCT125/74AHCT125) or run the MCU pin through one HCT buffer. ESP32/Pico → 74HCT125 → DIN/CLK/CS.
- CLK max 10 MHz. SPI mode 0 (CPOL=0, CPHA=0). Data latched on CLK rising edge, output to next module on falling edge — that's how chaining works.
- CS (LOAD) must rise **after** the last bit of the last 16-bit packet for the whole chain; one 16-bit packet per module per latch.
- Current: each segment driven up to 40 mA peak (set by RSET + intensity register). 8x8 module all-LEDs at max intensity ≈ 330 mA. Four-module FC-16 chain all-on ≈ 1.3 A — **do not power from Arduino 5V pin for chains > 1 module; use external 5V, common GND.**
- RSET on common modules is 10 kΩ → ~40 mA segment peak. Lower intensity in software, never below 9.53 kΩ in hardware.

### Wiring (FC-16 4-in-1 module, ESP32 example)

| MAX7219 pin | ESP32 (via 74HCT125) | Arduino Uno (direct, 5V logic) | Pico (via 74HCT125) |
|---|---|---|---|
| VCC | 5V external | 5V | VBUS (5V) |
| GND | GND (common with MCU!) | GND | GND |
| DIN | GPIO23 (MOSI) | D11 (MOSI) | GP3 (SPI0 TX) |
| CS  | GPIO5 | D10 | GP5 |
| CLK | GPIO18 (SCK) | D13 (SCK) | GP2 (SPI0 SCK) |

Chain: module 1 DOUT → module 2 DIN. CLK and CS are bused to all modules in parallel (on FC-16 boards this is already done on-PCB).

### Register map (you will need these for raw init)

| Register | Addr | Init value | Why |
|---|---|---|---|
| Decode mode | 0x09 | 0x00 (matrix) / 0xFF (7-seg BCD) | Matrix needs raw bits |
| Intensity | 0x0A | 0x00–0x0F | 0x08 = mid. Start LOW (0x01) on big chains |
| Scan limit | 0x0B | 0x07 | Drive all 8 digits/rows. Less = brighter rows but uneven |
| Shutdown | 0x0C | 0x01 = normal | **Powers up in shutdown (0x00) — display is blank until you write 1** |
| Display test | 0x0F | 0x00 | Powers up sometimes with test on; explicitly write 0 |

**The #1 init mistake:** not writing shutdown=1 and display-test=0 to *every* module in the chain. Second mistake: forgetting that powering on leaves random RAM contents — clear digits 1–8 (0x01–0x08) to 0x00.

### MicroPython (Pico/ESP32) — raw driver, no library needed

```python
from machine import Pin, SPI

NUM = 4  # modules in chain
spi = SPI(0, baudrate=5_000_000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3))
cs = Pin(5, Pin.OUT, value=1)

def write_all(reg, data):
    """Write same reg:data to every module in chain."""
    cs.value(0)
    for _ in range(NUM):
        spi.write(bytes([reg, data]))
    cs.value(1)  # latch — all modules latch on this rising edge

def init():
    write_all(0x0F, 0x00)  # display test off
    write_all(0x0B, 0x07)  # scan all 8 rows
    write_all(0x09, 0x00)  # no decode (raw matrix)
    write_all(0x0A, 0x02)  # low intensity to start
    for row in range(1, 9):
        write_all(row, 0x00)  # clear RAM
    write_all(0x0C, 0x01)  # exit shutdown — LAST

def set_row(module, row, value):
    """module 0 = nearest to MCU. row 1-8."""
    cs.value(0)
    for m in range(NUM - 1, -1, -1):  # farthest module shifts in first
        if m == module:
            spi.write(bytes([row, value]))
        else:
            spi.write(bytes([0x00, 0x00]))  # no-op register
    cs.value(1)

init()
set_row(0, 1, 0xFF)  # top row of first module on
```

Key detail: per-module writes use the **no-op register 0x00** for modules you don't want to change, and data for the farthest module goes in first (it shifts through the chain).

### Arduino C++ — use MD_Parola/MD_MAX72XX for text, raw for control

```cpp
#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>

// FC-16 modules: HARDWARE_TYPE must match your PCB or text is mirrored/rotated
#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 4
#define CS_PIN 10  // hardware SPI: MOSI=11, SCK=13 on Uno

MD_Parola disp = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

void setup() {
  disp.begin();
  disp.setIntensity(2);   // 0-15; keep low unless externally powered
  disp.displayClear();
  disp.displayScroll("HELLO", PA_LEFT, PA_SCROLL_LEFT, 50);
}

void loop() {
  if (disp.displayAnimate()) disp.displayReset();
}
```

`HARDWARE_TYPE` options: `FC16_HW` (most common blue 4-in-1), `GENERIC_HW`, `PAROLA_HW`, `ICSTATION_HW`. Wrong choice = text mirrored, upside down, or column-shifted. Try FC16_HW first for AliExpress 4-in-1 boards.

### MAX7219 debugging checklist

1. **Totally blank** → shutdown register still 0, or display-test never cleared, or CS wired to wrong pin (CS must idle HIGH).
2. **First module fine, rest garbage** → 3.3V logic marginal. Add 74HCT125. Also check DOUT→DIN chain order.
3. **Random pixels at power-on that never clear** → you never wrote digit registers 1–8; RAM is undefined at power-up.
4. **Flicker/dim, MCU browns out** → drawing >500 mA from USB. External 5V supply, common ground, intensity ≤ 4.
5. **Text mirrored/rotated** → wrong HARDWARE_TYPE constant (library) or your row/column mapping doesn't match the module PCB layout.
6. **Works on bench, dies on long wires** → CLK ringing. Keep DIN/CLK < 30 cm, add 100 Ω series resistor on CLK, 10 µF + 100 nF decoupling per module (most boards have it — check).

---

## 2. WS2812B / NeoPixel — Addressable RGB

### The timing contract (why you NEVER bit-bang in Python)

800 kHz data, 1.25 µs per bit:

| Symbol | High time | Low time | Tolerance |
|---|---|---|---|
| 0 bit | 0.4 µs | 0.85 µs | ±150 ns |
| 1 bit | 0.8 µs | 0.45 µs | ±150 ns |
| RESET (latch) | — | > 50 µs low (>280 µs on newer batches) | — |

±150 ns is far tighter than any interpreter loop. **Use hardware-assisted libraries only:**

- **Pico (MicroPython):** built-in `neopixel` module uses PIO — exact timing in hardware. Best platform for this.
- **ESP32 (Arduino):** Adafruit_NeoPixel uses RMT peripheral; FastLED uses RMT/I2S. Both fine. Avoid `delayMicroseconds` hand-rolled code.
- **AVR (Uno):** Adafruit_NeoPixel uses cycle-counted asm with interrupts disabled during show() — millis() loses ticks during long updates, expected.
- **Raspberry Pi (Linux):** `rpi_ws281x` library (PWM/DMA via GPIO18, or SPI via GPIO10). **Plain RPi.GPIO bit-bang can never work** — Linux scheduling jitter is milliseconds, not nanoseconds.

Color order is **GRB** on WS2812B (not RGB). SK6812 RGBW variants are GRBW. If your red shows green, this is why.

### Power budget — do this math before wiring anything

- **60 mA per pixel at full white (255,255,255), 5V.** ~20 mA per color channel.
- 30 pixels full white = 1.8 A. 144/m strip, 1 m, full white = **8.6 A**. A USB port gives 0.5–0.9 A.
- Realistic budget for animations: plan 20 mA/pixel average, but the *supply must survive worst case* or cap brightness in software: `strip.setBrightness(64)` caps at ~25%.
- **Inject power every 2–3 m / every ~100 pixels** on long runs — both 5V and GND. Voltage droop down the strip shows as red-shifted/dim far pixels (blue LED forward voltage ~3V dies first as rail sags).
- **1000 µF electrolytic across 5V/GND at strip input** (across, not in series) — absorbs hot-plug inrush that kills pixel #1.
- **300–500 Ω resistor in series with the data line**, placed at the strip end of the wire — damps ringing/reflections that corrupt the first pixel.
- Never hot-plug data before ground. Connect order: GND, then 5V, then data.

### Level shifting 3.3V → 5V (ESP32/Pico → WS2812B)

VIH = 0.7 × VDD = 3.5V at a 5V supply. 3.3V data is **out of spec** — it sometimes works on short wires and fails with flicker/wrong colors at random, especially on the first pixel.

Options, best to worst:

1. **74AHCT125 / 74HCT125** quad buffer (~$0.50). Power it from 5V; HCT inputs threshold at ~1.6V so 3.3V drives it cleanly; output is full 5V. The correct answer.
2. **Sacrificial first pixel at lower VDD:** power pixel #1 from 5V through a 1N4001 diode (≈4.3V at the pixel). 0.7 × 4.3 = 3.01V < 3.3V, so it accepts 3.3V data; its regenerated output to pixel 2 is at ~4.3V which satisfies the 5V strip. Hacky but field-proven.
3. **BSS138 bidirectional I2C shifter modules: DO NOT USE.** Too slow (designed for open-drain I2C, ~100 ns+ edges with pullup rise times) — corrupts 800 kHz data. This is the most common wrong purchase.
4. Just wiring 3.3V directly: works on the bench, ships flicker to production. Don't.

### Wiring table

| Strip wire | Connects to |
|---|---|
| 5V (red) | External 5V PSU + terminal. NOT the MCU 3.3V/5V pin for >8 pixels |
| GND (white/black) | PSU − terminal **AND** MCU GND (common ground is mandatory — no common GND = no valid logic levels = garbage) |
| DIN (green, arrow pointing away from input end) | 330 Ω → 74AHCT125 output ← MCU data pin |

Check the arrows printed on the strip: data flows IN at the end the arrows point away from. Feeding DOUT does nothing.

### MicroPython (Pico) — built-in PIO driver

```python
from machine import Pin
import neopixel, time

NUM_PIXELS = 30
np = neopixel.NeoPixel(Pin(16), NUM_PIXELS)  # GRB handled internally

# Set + show. Nothing appears until write().
np[0] = (255, 0, 0)        # red
np.fill((0, 0, 32))        # dim blue everywhere
np.write()                 # transmit — PIO does exact 800kHz timing

def wheel(pos):
    if pos < 85:  return (255 - pos * 3, pos * 3, 0)
    if pos < 170: pos -= 85; return (0, 255 - pos * 3, pos * 3)
    pos -= 170;   return (pos * 3, 0, 255 - pos * 3)

while True:
    for j in range(256):
        for i in range(NUM_PIXELS):
            np[i] = wheel((i * 256 // NUM_PIXELS + j) & 255)
        np.write()
        time.sleep_ms(20)
```

Brightness capping in MicroPython (no built-in): scale tuples yourself, e.g. `tuple(c * 64 // 255 for c in color)` — protect your PSU in code, not hope.

### Arduino C++ (ESP32 or Uno) — Adafruit_NeoPixel

```cpp
#include <Adafruit_NeoPixel.h>

#define PIN        6      // through 74AHCT125 on 3.3V boards
#define NUM_PIXELS 30

Adafruit_NeoPixel strip(NUM_PIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.setBrightness(64);   // 25% — caps current at ~15mA/pixel white
  strip.clear();
  strip.show();              // mandatory: pixels hold random data at power-up
}

void loop() {
  for (int i = 0; i < NUM_PIXELS; i++) {
    strip.clear();
    strip.setPixelColor(i, strip.Color(0, 0, 255));
    strip.show();            // ~30µs/pixel + >50µs latch
    delay(30);
  }
}
```

`show()` takes 30 µs × N pixels and (on AVR) runs with interrupts off — at 300 pixels that's 9 ms per frame with `millis()` frozen. Budget your frame rate: max ≈ 1 / (N × 30 µs + 1 ms).

### Raspberry Pi (Python, ROS2-compatible) — rpi_ws281x

```python
# sudo pip install rpi_ws281x  (needs root for DMA: run with sudo)
from rpi_ws281x import PixelStrip, Color

LED_COUNT  = 30
LED_PIN    = 18      # GPIO18 = PWM0 — only PWM/PCM/SPI-capable pins work
LED_FREQ   = 800000
LED_DMA    = 10
LED_INVERT = False
LED_BRIGHT = 64

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ, LED_DMA,
                   LED_INVERT, LED_BRIGHT, 0)
strip.begin()
strip.setPixelColor(0, Color(255, 0, 0))
strip.show()
```

Pi gotchas: GPIO18 PWM conflicts with onboard audio — add `dtparam=audio=off` in /boot/config.txt or pixels glitch on every sound. The Pi is 3.3V: level shift exactly like ESP32. In a ROS2 node, call `strip.show()` from a single timer callback, never from multiple subscription callbacks (the C library is not thread-safe).

### WS2812B debugging checklist

1. **Nothing at all** → data wired to DOUT end (check arrows); no common ground; forgot `show()`/`write()`.
2. **First pixel wrong color / flickers, rest OK** → marginal 3.3V logic. Level shift. (First pixel regenerates the signal at 5V, hence "rest OK".)
3. **Random flicker, worse with animation** → BSS138 shifter (replace with 74AHCT125), data wire too long without series resistor, or PSU sag — scope the 5V rail under load.
4. **Red shows as green** → RGB vs GRB order. Use NEO_GRB.
5. **Far end dim/orange** → voltage droop. Inject power at far end too.
6. **Whole strip resets/white-flashes under load** → PSU undersized; cap brightness or upsize supply.
7. **Works until WiFi/interrupt activity (ESP8266/AVR)** → interrupts corrupt bit-banged timing; use RMT-based driver (ESP32) or accept AVR's interrupt-off show().

---

## 3. 16x2 / 20x4 Character LCD with PCF8574 I2C Backpack

### Electrical facts

- HD44780 controller + PCF8574 8-bit I2C expander. Module is **5V**: at 3.3V VCC the contrast range barely works and many clones won't display.
- I2C address: **0x27** (PCF8574, Ti marking) or **0x3F** (PCF8574A). A2/A1/A0 solder jumpers subtract from these (all bridged → 0x20/0x38). Scan, don't guess.
- I2C speed: 100 kHz standard. The PCF8574 maxes at 100 kHz — setting 400 kHz causes intermittent garbage. Keep the bus at 100 kHz if this device shares it.
- Backpack drives the LCD in **4-bit mode**: each byte = two nibble transfers, each nibble needs an E (enable) pulse — that's 3 I2C writes per nibble (data+E high, E pulse, E low). ~1 ms per character; a full 16x2 refresh ≈ 35 ms. Don't redraw the whole screen every loop.
- Current: ~2 mA logic + ~20 mA backlight (jumper on backpack enables it).
- 3.3V hosts: backpack pullups (4.7k–10k to 5V) pull SDA/SCL to 5V. ESP32/Pico pins are not officially 5V-tolerant. In practice 4.7k-limited 5V on an I2C pin is widely tolerated, but the clean fix is a level shifter (BSS138 modules are FINE here — I2C is slow and open-drain, the opposite of the WS2812B case) or desolder the backpack pullups and add your own to 3.3V.

### Wiring

| Backpack pin | Uno | ESP32 | Pico |
|---|---|---|---|
| GND | GND | GND | GND |
| VCC | 5V | 5V (VIN) | VBUS |
| SDA | A4 | GPIO21 (via shifter ideally) | GP0 (I2C0 SDA, via shifter ideally) |
| SCL | A5 | GPIO22 | GP1 (I2C0 SCL) |

### The contrast pot — the #1 "broken" LCD

The blue trimpot on the backpack sets the V0 contrast voltage. Out of the box it is almost always misadjusted.

- **One row of solid blocks, no text** → module is powered and in its power-on (uninitialized) state, contrast is fine → your I2C init never ran (wrong address or wiring).
- **Completely blank, backlight on** → contrast turned too far. Turn the pot slowly through its full range while displaying text; the sweet spot is narrow (~10–20° of rotation).
- **Both rows solid blocks** → contrast cranked to max. Back it off.

Rule for diagnosis: **blocks on row 1 only = LCD alive, init failed. No blocks anywhere = contrast or power.**

### Address scan first, always

```python
# MicroPython
from machine import I2C, Pin
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100_000)
print([hex(a) for a in i2c.scan()])   # expect ['0x27'] or ['0x3f']
```

```cpp
// Arduino
#include <Wire.h>
void setup() {
  Wire.begin(); Serial.begin(115200);
  for (byte a = 8; a < 120; a++) {
    Wire.beginTransmission(a);
    if (Wire.endTransmission() == 0) { Serial.print("Found 0x"); Serial.println(a, HEX); }
  }
}
void loop() {}
```

Empty scan = SDA/SCL swapped, no pullups (bare PCF without backpack), or no power.

### Arduino C++ — LiquidCrystal_I2C

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);  // addr from your scan, cols, rows

void setup() {
  lcd.init();          // some forks use lcd.begin() — check your library
  lcd.backlight();
  lcd.setCursor(0, 0); // col, row — zero-indexed
  lcd.print("Temp:");
}

void loop() {
  lcd.setCursor(6, 0);
  lcd.print(analogRead(A0));
  lcd.print("   ");    // pad to erase stale digits — there is no auto-clear
  delay(500);          // don't spam: full update costs ms over I2C
}
```

Stale-digit bug everyone hits: printing "9" over "100" leaves "900". Pad with spaces or snprintf to fixed width: `char buf[17]; snprintf(buf, 17, "Temp: %4d", v); lcd.setCursor(0,0); lcd.print(buf);`. Avoid `lcd.clear()` in the loop — it takes ~2 ms and causes visible blink.

20x4 quirk: lines map 0→0x00, 1→0x40, 2→0x14, 3→0x54 — line 2 is a continuation of line 0 in DDRAM. Libraries handle it if you constructed with (20, 4); raw code must use those offsets.

### MicroPython — minimal PCF8574 HD44780 driver

No built-in library; this is a complete working driver:

```python
from machine import I2C, Pin
import time

class LCD:
    # PCF8574 bit map (standard backpack): P0=RS P1=RW P2=E P3=backlight P4-7=D4-7
    def __init__(self, i2c, addr=0x27, cols=16, rows=2):
        self.i2c, self.addr, self.cols, self.rows = i2c, addr, cols, rows
        self.bl = 0x08
        time.sleep_ms(50)              # HD44780 needs >40ms after power
        for _ in range(3):             # magic 3x 0x03: force 8-bit mode reset
            self._nib(0x30); time.sleep_ms(5)
        self._nib(0x20)                # switch to 4-bit
        self._cmd(0x28)                # 4-bit, 2 lines, 5x8 font
        self._cmd(0x0C)                # display on, cursor off
        self._cmd(0x06)                # entry mode: increment
        self.clear()

    def _nib(self, d):
        self.i2c.writeto(self.addr, bytes([d | self.bl | 0x04]))  # E high
        self.i2c.writeto(self.addr, bytes([d | self.bl]))         # E low: latch
    def _cmd(self, c):
        self._nib(c & 0xF0); self._nib((c << 4) & 0xF0)
        if c <= 3: time.sleep_ms(2)    # clear/home need 1.52ms
    def _data(self, c):
        self._nib((c & 0xF0) | 1); self._nib(((c << 4) & 0xF0) | 1)
    def clear(self): self._cmd(0x01)
    def move(self, col, row):
        self._cmd(0x80 | (col + (0x00, 0x40, 0x14, 0x54)[row]))
    def print(self, s):
        for ch in s: self._data(ord(ch))

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100_000)
lcd = LCD(i2c)
lcd.print("Hello Pico")
lcd.move(0, 1)
lcd.print("Line 2")
```

Timing constraints baked in above — violate them and you get garbage: ≥40 ms after power before init; the 3× 0x30 reset dance (handles all power-on states); ≥1.52 ms after clear (0x01) and home (0x02); ~37 µs per other command (I2C at 100 kHz is slower than that anyway, so it's free).

### LCD debugging checklist

1. **Blank, backlight on** → contrast pot. Turn it through full range first, before touching code.
2. **Row of blocks** → power+contrast OK, init never reached the chip → run I2C scan; likely 0x3F not 0x27, or SDA/SCL swapped.
3. **Garbage characters** → I2C at 400 kHz (drop to 100 kHz); missing 2 ms delay after clear; long unshielded I2C wires (>50 cm: lower speed, stronger pullups 2.2k).
4. **Works then corrupts after minutes** → noise on shared I2C bus (motors? add 100 nF at VCC, twist SDA/GND), or a second device clashing at same address.
5. **Faint ghost text** → running module at 3.3V. Give it 5V.
6. **Backlight dead, text fine** → backlight jumper on backpack removed.
7. **First character of each write garbled** → missing E-pulse low time; ensure two separate I2C writes per nibble (E high then E low), never one.

---

## 4. Cross-Cutting Rules

- **Common ground always.** Every "random garbage" report across all three display types traces to a missing MCU↔PSU ground at least a third of the time.
- **Decoupling:** 100 nF ceramic at every display's VCC pin; 1000 µF bulk at WS2812B strip input; 10 µF bulk per MAX7219 module.
- **Level-shifter selection is protocol-specific:** 74AHCT125 for fast push-pull (WS2812B data, MAX7219 SPI from 3.3V hosts). BSS138 modules ONLY for open-drain I2C (LCD backpack). Swapping these two is the single most common hardware-design error in hobby builds.
- **Power source decision table:**

| Load | USB/MCU 5V pin OK? |
|---|---|
| 1× MAX7219 module, intensity ≤ 4 | Yes |
| MAX7219 chain ≥ 2 modules | No — external 5V |
| ≤ 8 NeoPixels, brightness ≤ 64 | Yes |
| > 8 NeoPixels | No — external 5V, injected |
| 16x2 LCD + backlight | Yes (~25 mA) |

- **Shared SPI/I2C:** MAX7219 has no MISO and ignores the bus when CS is high — shares SPI fine. PCF8574 caps the whole I2C bus at 100 kHz — put fast I2C sensors (400 kHz+) on a second bus.
- **First-try success ritual:** wire → power check (measure 5V at the display, not at the PSU) → I2C scan / single-module smoke test → minimal "one pixel / one char / one row" program → only then the real code.
