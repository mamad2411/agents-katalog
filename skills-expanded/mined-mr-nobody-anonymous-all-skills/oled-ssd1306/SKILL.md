---
name: oled-ssd1306
description: "Use when wiring or coding an SSD1306 128x64/128x32 OLED over I2C (or SPI) on ESP32, Pico, or Arduino. Covers the 0x3C address trap, the 1KB framebuffer RAM cost, MicroPython ssd1306 lib quirks, Adafruit GFX/SSD1306 on Arduino, drawing robot faces with primitives, real refresh-rate limits, burn-in avoidance, and the I2C debugging checklist."
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


# SSD1306 OLED (128x64 / 128x32) — Field Guide

The SSD1306 is the default tiny display in robotics: 0.96" 128x64 (most common), 0.91" 128x32, and 1.3" modules that are *often actually SH1106* (see Gotcha #1). Monochrome, I2C or SPI, 3.3V logic, self-emissive — no backlight, true black, but it burns in.

## Identification — before you write any code

| Marking / clue | What it really is | Driver |
|---|---|---|
| 0.96", 4 pins (GND VCC SCL SDA) | SSD1306 I2C | ssd1306 lib |
| 0.91" narrow strip, 128x32 | SSD1306 I2C, 32px tall | ssd1306, height=32 |
| 1.3", 4-pin I2C | **Usually SH1106**, not SSD1306 | sh1106 lib (132-col RAM, 2px offset) |
| 7 pins (GND VCC CLK MOSI RES DC CS) | SPI variant | SSD1306 SPI constructor |

**SH1106 symptom on SSD1306 driver:** display works but the image is shifted ~2px and the rightmost columns show garbage/wrap. The SH1106 has 132x64 RAM and no horizontal addressing mode. Fix = use an SH1106 driver, not offset hacks.

## Wiring (I2C)

All modules have onboard 3.3V regulation of logic? **No** — most cheap modules have a regulator for VCC (so 3.3–5V VCC is fine) but SDA/SCL go straight to the chip. On 3.3V MCUs (ESP32, Pico) this is moot. On a 5V Arduino Uno/Nano it works in practice because the module's pull-ups go to 3.3V and I2C is open-drain — the Uno never drives the line high. Do **not** add external pull-ups to 5V.

| OLED pin | ESP32 | Pico (RP2040) | Arduino Uno/Nano | ESP8266 |
|---|---|---|---|---|
| GND | GND | GND | GND | GND |
| VCC | 3V3 (or 5V if module has reg) | 3V3 | 5V | 3V3 |
| SCL | GPIO22 | GP5 (I2C0 SCL) | A5 | D1/GPIO5 |
| SDA | GPIO21 | GP4 (I2C0 SDA) | A4 | D2/GPIO4 |

- Modules ship with 4.7k–10k pull-ups onboard. With short wires (<20cm) you need nothing extra.
- Current draw: ~8mA typical (sparse pixels), up to ~25–30mA all-pixels-on at full contrast. Fine off a 3.3V rail; irrelevant to your motor power budget.
- Some 7-pin SPI modules can be converted to I2C via solder jumpers on the back — don't bother, buy the right one.
- A few modules have a RES(reset) pin even in I2C mode. If present and floating, the display may randomly fail to init. Tie it high or to an MCU pin and pulse low 10ms at boot.

## The address: 0x3C, rarely 0x3D

- **0x3C is the address on ~95% of modules** — even when the silkscreen says "0x78". 0x78 is the *8-bit write address* (0x3C << 1). Datasheets and silkscreens use 8-bit; every Arduino/MicroPython lib uses 7-bit. If your code says 0x78, it's wrong.
- 0x3D only if the SA0/address solder jumper on the back is moved (lets you run two OLEDs on one bus).
- Always scan first when debugging:

```python
# MicroPython
from machine import I2C, Pin
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
print([hex(a) for a in i2c.scan()])   # expect ['0x3c']
```

```cpp
// Arduino
#include <Wire.h>
void setup() {
  Wire.begin(); Serial.begin(115200);
  for (uint8_t a = 1; a < 127; a++) {
    Wire.beginTransmission(a);
    if (Wire.endTransmission() == 0) { Serial.print("Found 0x"); Serial.println(a, HEX); }
  }
}
```

Empty scan = wiring problem (swapped SDA/SCL is the #1 cause), not a code problem. Stop and fix hardware.

## Framebuffer RAM cost — 1KB, and it matters

128 x 64 / 8 = **1024 bytes** of RAM for the framebuffer, allocated by the driver:

| MCU | Total RAM | 1KB framebuffer = |
|---|---|---|
| Arduino Uno/Nano (ATmega328P) | 2KB | **50% of all RAM.** Adafruit_SSD1306 `begin()` returns false if malloc fails. Expect crashes if you also use String, large arrays, or SoftwareSerial buffers. |
| ESP8266 | ~40KB usable | fine |
| Pico | 264KB | fine |
| ESP32 | ~320KB | fine |

On the Uno, if you only need text, use the **U8x8** mode of u8g2 (no framebuffer, writes 8x8 tiles directly, ~zero RAM) or `U8G2 _1_` page-buffer mode (128 bytes, redraws in 8 passes — your draw code runs inside a `do{...}while(u8g2.nextPage())` loop and must be idempotent).

The framebuffer model means: **nothing appears on screen until you call `show()` / `display()`.** Forgetting this is the single most common "my OLED is blank but init worked" bug.

## MicroPython — ssd1306 lib

The driver is `ssd1306.py` (in ESP32/ESP8266 firmware as built-in on some builds; on Pico copy it from micropython-lib to the filesystem). It subclasses `framebuf.FrameBuffer` in `MONO_VLSB` format, so you get all framebuf methods.

```python
from machine import I2C, Pin
import ssd1306

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)          # addr=0x3c default

oled.fill(0)                      # clear buffer (not screen — yet)
oled.text("HELLO", 0, 0, 1)       # 8x8 font ONLY, fixed. 16 chars x 8 lines max
oled.pixel(10, 20, 1)
oled.hline(0, 30, 128, 1)
oled.vline(64, 0, 64, 1)
oled.line(0, 0, 127, 63, 1)
oled.rect(5, 35, 20, 10, 1)       # outline
oled.fill_rect(30, 35, 20, 10, 1) # filled
oled.ellipse(96, 40, 12, 8, 1)            # MicroPython >= 1.19.1
oled.ellipse(96, 40, 12, 8, 1, True)      # filled
oled.show()                       # NOW it appears (full 1KB I2C transfer)

oled.contrast(128)                # 0-255 brightness
oled.invert(1)                    # white<->black, instant, no redraw
oled.poweroff() / oled.poweron()  # display sleep, ~10uA, buffer retained
oled.scroll(dx, dy)               # shifts buffer; vacated area is NOT cleared
```

Hard facts:
- `text()` font is fixed 8x8. No size parameter exists. For big digits, draw them with `fill_rect` segments (7-seg style) or blit a prebuilt `FrameBuffer` sprite. Don't go hunting for `setTextSize` — that's Arduino.
- No circle before MicroPython 1.19.1 — use `ellipse(x, y, r, r, 1)`.
- On Pico: `ImportError: no module named 'ssd1306'` → the lib is not frozen in; `mpremote mip install ssd1306` or copy ssd1306.py over.
- Construct with the **actual height**: `SSD1306_I2C(128, 32, i2c)` for the 0.91". Using 64 on a 32px panel gives interleaved/stretched garbage.
- Sprites via blit:

```python
import framebuf
heart = bytearray(b'\x0c\x1e\x3f\x7f\x7f\x3f\x1e\x0c')   # 8x8, column bytes
fb = framebuf.FrameBuffer(heart, 8, 8, framebuf.MONO_VLSB)
oled.blit(fb, 60, 28)
oled.show()
```

## Arduino — Adafruit_SSD1306 + Adafruit GFX

```cpp
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_W 128
#define SCREEN_H 64        // 32 for the 0.91" — wrong value = garbled
Adafruit_SSD1306 display(SCREEN_W, SCREEN_H, &Wire, -1);  // -1 = no reset pin

void setup() {
  Wire.setClock(400000);                       // 400kHz, big refresh win
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {  // 0x3C even if silk says 0x78
    for(;;);                                   // malloc failed or no ACK
  }
  display.clearDisplay();                      // buffer starts with Adafruit splash!
  display.setTextColor(SSD1306_WHITE);         // forget this -> invisible text
  display.setTextSize(2);                      // integer scale of 5x7 font
  display.setCursor(0, 0);
  display.print(F("HI"));                      // F() keeps strings out of SRAM on AVR
  display.display();                           // push buffer -> screen
}
```

GFX primitives: `drawPixel, drawLine, drawRect/fillRect, drawCircle/fillCircle, drawRoundRect/fillRoundRect, drawTriangle/fillTriangle, drawBitmap(x,y,bitmap,w,h,color)` with bitmaps in PROGMEM (use image2cpp web tool to convert PNGs).

The 5 Arduino-specific mistakes:
1. **Not calling `display.display()`** — nothing renders without it.
2. **`begin()` with no address arg on clone boards** — pass `0x3C` explicitly.
3. **Adafruit splash screen** flashes because `clearDisplay()` wasn't called before first `display()`.
4. **Text invisible** — default text color after some operations is unset/black; always `setTextColor(SSD1306_WHITE)`.
5. **Uno RAM exhaustion** — `begin()` returns false, or random resets mid-run. Check free RAM; switch to u8g2 page mode if tight.

Custom fonts: `display.setFont(&FreeSansBold12pt7b);` — note GFX fonts position by **baseline**, not top-left; `setCursor(0,0)` puts text *above* the screen. Use `getTextBounds()` to place them.

## Drawing robot faces / expressions with primitives

A robot face needs ~6 expressions and zero bitmaps. Geometry that works on 128x64: eyes at x=38 and x=90, eye center y=24, mouth around y=50.

```python
# MicroPython expression engine — primitives only
EYE_L, EYE_R, EYE_Y, R = 38, 90, 24, 12

def eyes_open(o):
    o.fill_rect(EYE_L-R, EYE_Y-R, 2*R, 2*R, 1)     # square eyes read better
    o.fill_rect(EYE_R-R, EYE_Y-R, 2*R, 2*R, 1)     # than circles at this res
    o.fill_rect(EYE_L-4, EYE_Y-4, 8, 8, 0)          # pupil holes
    o.fill_rect(EYE_R-4, EYE_Y-4, 8, 8, 0)

def eyes_closed(o):
    o.fill_rect(EYE_L-R, EYE_Y-2, 2*R, 4, 1)        # horizontal slits
    o.fill_rect(EYE_R-R, EYE_Y-2, 2*R, 4, 1)

def mouth_smile(o):                                  # arc faked with hlines
    for i, w in enumerate((24, 20, 14)):
        o.hline(64 - w//2, 48 + i*3, w, 1)          # widest on top = smile

def mouth_sad(o):
    for i, w in enumerate((14, 20, 24)):
        o.hline(64 - w//2, 48 + i*3, w, 1)          # widest on bottom = frown

def mouth_flat(o):
    o.fill_rect(50, 50, 28, 3, 1)

def face(o, expr):
    o.fill(0)
    if expr == "happy":    eyes_open(o);   mouth_smile(o)
    elif expr == "sad":    eyes_open(o);   mouth_sad(o)
    elif expr == "sleep":  eyes_closed(o); mouth_flat(o)
    elif expr == "blink":  eyes_closed(o); mouth_smile(o)
    o.show()
```

Animation rules learned the hard way:
- **Blink** = swap to `eyes_closed` for 120–150ms every 3–6s (randomize the interval; fixed intervals look robotic in the bad way). Use `time.ticks_ms()` scheduling, never `sleep()` in the robot's main loop.
- **Looking left/right** = shift only the pupil holes ±5px, not the whole eye.
- **Talking** = alternate mouth height 2px/8px at ~120ms while audio plays.
- Always `fill(0)` and redraw the whole face. Partial erase-and-redraw saves nothing (show() sends the full buffer anyway) and leaves artifacts.
- Squares/rounded-rects beat circles for eyes at 128x64 — circles under r=10 look like blobs.

## Refresh rate — real numbers

`show()`/`display()` transfers the whole 1KB buffer + command bytes over I2C:

| Bus | Theoretical | Real-world full-frame | Practical FPS ceiling |
|---|---|---|---|
| I2C 100kHz (default!) | ~10.3KB/s | ~110ms/frame | ~9 FPS |
| I2C 400kHz | ~41KB/s | ~25–30ms/frame | ~30 FPS |
| I2C 1MHz (ESP32 can; out of SSD1306 spec but usually works) | — | ~12ms | ~60 FPS |
| SPI 8MHz | — | ~1.5ms | panel-limited |

- **Set 400kHz explicitly.** Arduino `Wire` defaults to 100kHz; MicroPython default varies by port. This is the cheapest 3x speedup available.
- The panel itself refreshes ~100+ Hz internally; the bus is always the bottleneck on I2C.
- For a robot: face animation at 10–15 FPS looks perfectly smooth. Don't call `show()` every loop iteration — call it only when the frame content changed.
- Tearing is invisible at this size; don't build double-buffering, the driver buffer *is* the back buffer.

## Burn-in — OLEDs are consumable

SSD1306 OLEDs visibly burn in. A static UI shown 24/7 ghosts in **weeks**; noticeably dimmer pixels within months. For a robot face that's mostly static, mitigate:

1. **Screen sleep**: `oled.poweroff()` (MicroPython) / `display.ssd1306_command(SSD1306_DISPLAYOFF)` (Arduino) after 30–60s idle. Buffer survives; `poweron()` restores instantly. This is the #1 fix.
2. **Pixel shifting**: every 2–5 min, offset the whole face by ±2px (just add a jitter offset to all draw coords). Invisible to users, spreads wear.
3. **Contrast down**: `contrast(80)` instead of 255. Brightness vs lifetime is roughly linear; half brightness ≈ double life. Full contrast is rarely needed indoors.
4. **Avoid permanent static elements** — battery icons, fixed borders, and labels are what actually burn in, not the animated parts.
5. `invert()` does NOT help (it just inverts which pixels wear).

Blue-pixel regions on dual-color (yellow/blue) modules age fastest.

## Debugging checklist (in order)

1. **I2C scan.** No 0x3C? → swapped SDA/SCL (most common), no power, dead module, or floating RES pin. Don't touch code until scan passes.
2. **Scan OK, screen blank** → missing `show()`/`display()`, or drawing in color 0, or `setTextColor` unset (Arduino).
3. **Garbled / interleaved / stretched** → wrong height in constructor (32 vs 64), or it's an SH1106 (offset + right-edge garbage).
4. **Works then freezes/corrupts during robot motion** → I2C bus noise from motors. Shorten wires, twist SDA/SCL with GND, keep away from motor leads; on ESP32 add I2C timeout + reinit-on-error. The SSD1306 has no readback — you can't detect corruption, only reinit periodically.
5. **Random init failure on Uno** → RAM. `begin()` false = framebuffer malloc failed.
6. **Dim or uneven** → burn-in (see above) or VCC sag; check 3V3 rail under load.
7. **Two OLEDs needed** → second one at 0x3D (resolder SA0 jumper), or use both I2C peripherals (ESP32/Pico have two), or a TCA9548A mux.

## When NOT to use SSD1306

- Need color or images → ST7735/ST7789 TFT (SPI, similar price).
- Need >1.3" → SH1106 1.3", or SSD1309 2.42" (SSD1306-compatible commands, usually SPI).
- Sunlight-readable, always-on, near-zero power → Sharp Memory LCD or e-paper.
- Uno with <1KB RAM to spare and you insist on graphics → u8g2 page-buffer mode.
