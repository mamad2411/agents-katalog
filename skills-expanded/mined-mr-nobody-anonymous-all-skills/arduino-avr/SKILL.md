---
name: arduino-avr
description: "Use when writing or debugging code for Arduino Uno, Nano, Pro Mini, or any ATmega328P/ATmega168 board. Provides expert AVR knowledge: 2KB SRAM discipline (F()/PROGMEM), Timer0/1/2 conflict map (Servo vs tone() vs PWM pins 9/10/3/11), external interrupts (pins 2/3 only) vs pin-change interrupts, 5V↔3.3V level shifting for I2C/SPI/UART peripherals, millis() rollover-safe timing, bootloader vs ISP programming, exact electrical limits, and the standard mistakes that brick first attempts."
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


# Arduino AVR (Uno / Nano / Pro Mini — ATmega328P)

Authoritative reference for generating correct ATmega328P code and wiring on the first attempt.
Everything below applies to Uno R3, Nano (classic, not "Nano Every"/"Nano 33"), Pro Mini 5V/16MHz
unless stated otherwise. **It does NOT apply to** Uno R4 (Renesas RA4M1), Nano Every (ATmega4809),
Nano 33 IoT/BLE (SAMD/nRF52), or ESP boards — those have different timers, RAM, and 3.3V logic.

---

## 1. Hard Electrical Limits (memorize these numbers)

| Parameter | Value | Consequence of exceeding |
|---|---|---|
| Logic voltage | 5.0V (Pro Mini 3.3V variant: 3.3V/8MHz) | — |
| Absolute max per I/O pin | 40mA (abs max), **20mA recommended** | pin driver burns out |
| Total current all I/O pins | **200mA** (sum, through VCC/GND pins) | chip dies |
| 5V rail from onboard regulator (Uno, VIN 9V) | ~500mA minus board's own ~50mA; regulator thermal-limits hard above ~9V VIN | brownout resets, hot regulator |
| 3.3V pin on Uno/Nano | **50mA max** (from FT232/separate LDO) | NOT a power supply — never run an ESP8266 or nRF24 radio off it |
| VIN / barrel jack | 7–12V recommended (6–20V absolute) | <7V: unstable 5V; >12V: regulator overheats |
| USB supply | 5V, 500mA fuse (Uno polyfuse) | polyfuse trips, board resets |
| ADC input | 0 – VREF (default 5V), 10-bit (0–1023) | >VCC+0.5V damages pin |
| EEPROM | 1KB, ~100,000 write cycles per cell | wear-out if written in loop() |
| Flash | 32KB (−0.5KB bootloader) | sketch too big |
| **SRAM** | **2KB (2048 bytes)** | silent crashes — see §2 |
| Clock | 16MHz (5V) / 8MHz (3.3V Pro Mini) | — |

**Rules derived from the table:**
- An LED needs a series resistor: (5V − 2V) / 220Ω ≈ 14mA. Never drive an LED bare.
- **Never drive a motor, solenoid, relay coil, or speaker directly from a pin.** A hobby servo's
  *signal* is fine (µA); its *power* (red wire) must come from a separate 5–6V supply ≥1A per servo,
  **grounds tied together**.
- SG90 servo stall current ≈ 650mA–1A. Powering servos from the Arduino 5V pin causes the #1
  beginner failure: resets/jitter when the servo moves. Separate supply, common ground. Always.
- Driving 8 LEDs at 20mA = 160mA — already near the 200mA total budget. Use a shift register
  (74HC595) or transistor drivers for more.
- Inductive loads (relay/motor/solenoid) need a flyback diode (1N4007/1N5819) across the coil and
  an NPN/MOSFET driver (2N2222 up to ~500mA with base resistor ~1kΩ; logic-level MOSFET like
  IRLZ44N for amps — note: IRF520 modules are NOT logic-level, they barely turn on at 5V and
  not at all from 3.3V).

---

## 2. 2KB SRAM Discipline — the silent killer

Symptoms of RAM exhaustion: sketch resets randomly, Serial prints garbage, `String` operations
"work then stop", behavior changes when you add one more `Serial.println`. The compiler warning
"Low memory available, stability problems may occur" at >75% global usage is **real**.

### F() macro — mandatory for every string literal printed

```cpp
// BAD: "Temperature: " consumes 14 bytes of SRAM forever
Serial.println("Temperature: ");

// GOOD: string stays in flash, streamed out byte-by-byte
Serial.println(F("Temperature: "));
lcd.print(F("Hello"));          // works with LiquidCrystal too
```

`F()` works with any `Print`-derived class (Serial, LCD, Ethernet client). It does NOT work
where a plain `char*` is required — for that use PROGMEM + helper:

```cpp
const char msg[] PROGMEM = "stored in flash";
char buf[24];
strcpy_P(buf, msg);             // copy out when needed
// or print directly:
Serial.println((__FlashStringHelper*)msg);
```

### PROGMEM lookup tables

```cpp
#include <avr/pgmspace.h>

const uint8_t sineTable[256] PROGMEM = { 128, 131, 134, /* ... */ };
const uint16_t freqs[] PROGMEM = { 262, 294, 330, 349, 392, 440, 494, 523 };

uint8_t s  = pgm_read_byte(&sineTable[i]);    // NOT sineTable[i] — that reads SRAM address space!
uint16_t f = pgm_read_word(&freqs[note]);
float    x = pgm_read_float(&floatTable[i]);
```

**The classic bug:** declaring `PROGMEM` but reading with normal array syntax. It compiles,
returns garbage. Every access must go through `pgm_read_*` / `memcpy_P` / `strcpy_P`.

Array of strings in PROGMEM (menus):

```cpp
const char item0[] PROGMEM = "Start";
const char item1[] PROGMEM = "Settings";
const char* const menu[] PROGMEM = { item0, item1 };

char buf[16];
strcpy_P(buf, (char*)pgm_read_ptr(&menu[idx]));
```

### Banned / restricted patterns on 2KB

- **`String` class: avoid entirely.** Heap fragmentation on a 2KB heap kills sketches in minutes.
  Use fixed `char buf[N]` + `snprintf`. If you must parse Serial input:
  ```cpp
  char line[32]; uint8_t pos = 0;
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') { line[pos] = '\0'; handleLine(line); pos = 0; }
    else if (pos < sizeof(line) - 1) line[pos++] = c;
  }
  ```
- `malloc`/`new` in loop(): no. Allocate everything statically at global scope.
- Recursion: stack and heap share the 2KB and grow toward each other. Keep stack shallow.
- Large local arrays (`char buf[512]` inside a function) blow the stack silently.
- `double` == `float` on AVR (both 4 bytes). Float math is software-emulated and slow (~30–80µs
  per multiply); prefer integer math (e.g. store temperature as tenths: `int16_t tempC10`).

### Measuring free RAM

```cpp
int freeRam() {
  extern int __heap_start, *__brkval;
  int v;
  return (int)&v - (__brkval == 0 ? (int)&__heap_start : (int)__brkval);
}
// Healthy: keep > 256 bytes free at the worst point.
```

Compile-time check: avr-size output / IDE "Global variables use X bytes". That number EXCLUDES
stack and heap — 75%+ globals means trouble.

---

## 3. Timer Conflict Map — why Servo + tone() + PWM fight

ATmega328P has exactly three timers. Almost every "library X breaks feature Y" bug is here.

| Timer | Bits | Arduino uses it for | PWM pins driven | Libraries that seize it |
|---|---|---|---|---|
| Timer0 | 8 | **millis(), micros(), delay()** + PWM | **5, 6** | (don't touch — breaks timekeeping) |
| Timer1 | 16 | PWM | **9, 10** | **Servo**, TimerOne, IRremote (send), some stepper libs |
| Timer2 | 8 | PWM | **3, 11** | **tone()**, IRremote (recv, some versions), MsTimer2 |

### Consequences — state these to the user when relevant

1. **Servo library disables `analogWrite()` on pins 9 and 10** — on EVERY Servo instance, even one.
   Need PWM + servos? Use pins 3, 5, 6, 11 for PWM.
2. **`tone()` disables `analogWrite()` on pins 3 and 11** (Timer2). `noTone()` restores it.
3. **`tone()` + IRremote** conflict in older IRremote versions (both want Timer2). IRremote ≥3.x
   lets you change timer via `#define IR_USE_AVR_TIMER1` — which then conflicts with Servo instead.
   You can have at most: Servo (T1) + tone (T2) + millis (T0), OR IRremote + Servo but no tone.
4. **Servo + tone() together is fine** (T1 vs T2).
5. Changing Timer0 prescaler to speed up PWM on pins 5/6 **breaks millis()/delay() timing** by the
   same factor. Never do it; change Timer1 or Timer2 prescaler instead:
   ```cpp
   // 31.4kHz PWM on pins 9/10 (silent motor drive), millis() unaffected:
   TCCR1B = (TCCR1B & 0b11111000) | 0x01;   // prescaler 1
   // Pins 3/11 (Timer2) to 31.4kHz:
   TCCR2B = (TCCR2B & 0b11111000) | 0x01;
   ```
6. Default PWM frequencies: pins 5/6 ≈ **976Hz**; pins 3/9/10/11 ≈ **490Hz**. 490Hz audibly whines
   on motor drivers — bump Timer1/2 prescaler as above if the whine matters.
7. `delayMicroseconds()` does NOT use timers (busy loop) — safe everywhere, accurate from 3µs up,
   but blocks interrupts' effect on it; avoid values >16383µs.
8. **Servo on ATmega328P supports max 12 servos** on any pins (it's software-multiplexed off
   Timer1's compare interrupt — that's why it owns the whole timer, not just pins 9/10).

### tone() specifics

```cpp
tone(8, 440);            // any digital pin, 31Hz–65kHz
tone(8, 440, 500);       // auto-stop after 500ms (non-blocking)
noTone(8);
```
- Only ONE tone at a time, chip-wide. Calling tone() on a second pin while one plays does nothing
  until you `noTone()` the first.
- Passive buzzer: needs tone(). Active buzzer: just `digitalWrite(pin, HIGH)` — running tone()
  into an active buzzer produces garbage sound. Ask which type if unknown (active has internal
  oscillator, usually marked with a sticker / has white sealed top).
- Speaker on a pin: 100Ω series resistor minimum (8Ω speaker directly = 600mA dead pin).

---

## 4. Interrupts — pins 2 and 3 only (external INT0/INT1)

```cpp
volatile uint32_t pulseCount = 0;     // volatile is MANDATORY for ISR-shared vars

void countPulse() { pulseCount++; }   // keep ISRs tiny: no Serial, no delay, no millis math

void setup() {
  pinMode(2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(2), countPulse, FALLING);
}

void loop() {
  uint32_t copy;
  noInterrupts();                     // atomic read of multi-byte var
  copy = pulseCount;
  interrupts();
  // use copy ...
}
```

Rules:
- `attachInterrupt(digitalPinToInterrupt(pin), ...)` — always wrap with `digitalPinToInterrupt()`.
  On Uno/Nano: pin 2 → INT0, pin 3 → INT1. **Only these two pins.** `attachInterrupt(2, ...)`
  (raw number) is a classic bug — interrupt 2 doesn't exist on 328P.
- Modes: `LOW`, `CHANGE`, `RISING`, `FALLING`.
- Inside an ISR: `millis()` is frozen (returns last value), `delay()` hangs forever,
  `micros()` works but drifts after ~1ms, `Serial.print` can deadlock if buffer fills.
  Pattern: set a `volatile bool flag`, handle it in loop().
- Any variable shared with an ISR: `volatile`. Any shared variable >1 byte: read/write inside a
  `noInterrupts()/interrupts()` guard in main code (AVR is 8-bit; a 16/32-bit read can be torn).
- Need interrupts on other pins? **Pin-change interrupts** cover all pins (grouped into 3 ports,
  one ISR per port, you must determine which pin changed yourself), or use the PinChangeInterrupt
  library. Encoders on 2&3 directly is the clean design; suggest that first.
- Quadrature encoder pattern (both channels on 2/3):
  ```cpp
  volatile int32_t pos = 0;
  void isrA() { (digitalRead(2) == digitalRead(3)) ? pos++ : pos--; }
  attachInterrupt(digitalPinToInterrupt(2), isrA, CHANGE);
  ```
- Mechanical switches bounce 1–10ms. Debounce in the ISR with a timestamp:
  ```cpp
  volatile uint32_t lastIsr = 0;
  void isr() {
    uint32_t now = millis();          // frozen but still readable — OK for coarse debounce
    if (now - lastIsr > 50) { /* handle */ lastIsr = now; }
  }
  ```
  (Better: hardware RC debounce 10kΩ + 100nF, or debounce by polling in loop().)

---

## 5. 5V ↔ 3.3V Level Shifting — what actually needs it

Uno/Nano I/O is 5V. Most modern sensors/radios are 3.3V parts. The damage is usually slow
(works for a week, then dies), so "it worked without shifting" is not evidence.

| Peripheral | 5V-tolerant? | Required interface handling |
|---|---|---|
| nRF24L01+ | inputs NOT 5V tolerant by spec margin... actually SPI inputs ARE 5V tolerant per datasheet; **VCC must be 3.3V** | Power from real 3.3V ≥100mA + 10µF cap on module; SPI lines direct OK |
| ESP8266 / ESP-01 | **NO** | 3.3V power ≥250mA (NOT the Uno 3.3V pin), level-shift TX→RX with divider |
| SD card (bare) | **NO** | Use a module with onboard regulator + level shifter, or 4050/divider on MOSI/SCK/CS; MISO (card→Arduino) needs nothing |
| MPU6050 / BMP280 / most GY- modules | module has regulator + (usually) I2C is open-drain | Usually fine: I2C pull-ups to 3.3V on module; do NOT add extra 5V pull-ups |
| HC-05/HC-06 Bluetooth | RX pin is 3.3V (not 5V tolerant) | divider on Arduino TX → HC-05 RX (1kΩ/2kΩ); HC-05 TX → Arduino RX direct (3.3V reads as HIGH on 5V AVR, threshold 0.6×VCC=3.0V — marginal but works) |
| RC522 RFID | **NO**, 3.3V part | 3.3V power; SPI inputs tolerate 5V poorly — use divider or shifter for reliability |
| WS2812B LEDs | wants data ≥ 0.7×VLED | 5V Arduino driving 5V strip: fine. 3.3V MCU driving 5V strip: needs shifter — not this board's problem |
| Hobby servos, HC-SR04, DHT11/22, relays modules | 5V native | direct |

Note HC-SR04 echo pin outputs 5V — fine for Uno, would need a divider only on 3.3V boards.

### Methods, fastest to slowest

1. **Direct (3.3V output → 5V input):** always fine; VIH of 5V AVR is 3.0V, so 3.3V reads HIGH.
2. **Resistor divider (5V output → 3.3V input), unidirectional, <1MHz:**
   `5V pin → 1kΩ → node → 2kΩ → GND`, node = 3.33V. Good for UART up to 115200, trigger pins.
   Too slow for 8MHz SPI (RC with input capacitance rounds edges) — usually still OK at
   SPI_CLOCK_DIV4 (4MHz) with short wires, but flaky.
3. **BSS138 bidirectional module (the 4-channel boards):** correct for **I2C** (open-drain, needs
   bidirectional). Works to ~400kHz I2C fine. Mediocre for SPI >2MHz.
4. **74HC4050 / 74LVC245 powered at 3.3V:** proper unidirectional buffer, full SPI speed.
5. **I2C special case:** because I2C is open-drain, you can often just put pull-ups to 3.3V only
   and never drive high — Wire library drives low/releases, so a 5V master with 3.3V pull-ups is
   spec-clean. Make sure no 5V pull-ups exist anywhere on the bus (some 5V modules have them —
   remove or it pulls the bus to 5V).

---

## 6. millis() Rollover — write it safe, every time

`millis()` (uint32_t) rolls over after **49.71 days**; `micros()` after **71.6 minutes**.
`micros()` resolution is 4µs (Timer0 prescaler).

```cpp
// CORRECT — survives rollover due to unsigned subtraction wrap-around:
uint32_t last = 0;
const uint32_t INTERVAL = 1000;
void loop() {
  if (millis() - last >= INTERVAL) {
    last += INTERVAL;        // drift-free; use `last = millis()` if missed ticks should be dropped
    doTask();
  }
}

// WRONG — breaks at rollover (and the comparison logic is upside down anyway):
if (millis() >= last + INTERVAL)        // last + INTERVAL can overflow → condition true forever/never
if (millis() > nextTime)                 // any absolute-deadline comparison is broken at wrap
```

Rules:
- The ONLY safe pattern is `(now - then) >= interval` with all three as `uint32_t`.
- Never store millis in `int` or `long` (signed) — comparisons break long before 49 days.
- Never compare two timestamps with `<`/`>` directly; subtract first.
- Multiple independent timers: one `uint32_t lastX` per task; this is the standard
  non-blocking superloop. Avoid `delay()` in anything that also reads sensors/serial — a
  `delay(1000)` drops incoming serial bytes after the 64-byte RX buffer fills.

Non-blocking blink skeleton (the template for all periodic tasks):

```cpp
struct Task { uint32_t last; uint32_t interval; };
Task blink{0, 500}, sensor{0, 100};

void loop() {
  uint32_t now = millis();
  if (now - blink.last  >= blink.interval)  { blink.last  = now; togglePin(); }
  if (now - sensor.last >= sensor.interval) { sensor.last = now; readSensor(); }
}
```

---

## 7. Bootloader vs ISP — programming paths

| Path | Hardware | Erases bootloader? | Use when |
|---|---|---|---|
| Bootloader (normal upload) | USB cable (Uno: ATmega16U2 USB-serial; Nano: CH340 or FT232) | No | normal development |
| ISP / ICSP | USBasp, or another Arduino as ISP, on the 6-pin ICSP header (MISO/MOSI/SCK/RESET/VCC/GND = pins 12/11/13/RST) | Yes (unless you re-burn it) | bricked bootloader, fresh chips, setting fuses, reclaiming the 512B bootloader space, sketches that must start instantly |
| Burn Bootloader (IDE menu) | ISP programmer attached | writes bootloader + **fuses** | new bare ATmega328P, wrong-fuse recovery |

Critical facts:
- **Old Nano bootloader:** many clones ship the old ATmega328 bootloader at 57600 baud. If upload
  fails with `avrdude: stk500_recv(): programmer is not responding`, select
  *Tools → Processor → ATmega328P (Old Bootloader)*. This is the #1 Nano upload failure.
- **CH340 driver:** Nano clones use CH340G USB-serial; Windows/macOS need the WCH driver or no COM
  port appears at all. If no port shows up, it's the driver (or a charge-only USB cable).
- **Auto-reset:** uploading works because DTR toggling resets the chip into the bootloader via a
  100nF cap to RESET. Anything connected to RESET or pin 0/1 (RX/TX) can break uploads —
  **disconnect modules from pins 0/1 before uploading**, and don't use 0/1 for I/O in designs
  that need serial debugging. A 10µF cap RESET→GND *disables* auto-reset (used when the Uno
  acts as a USB-serial bridge or ArduinoISP host — required for "Arduino as ISP" on some boards).
- **Optiboot timing:** bootloader waits ~1s after reset before running the sketch. A sketch via
  ISP (no bootloader) starts in ~60ms. Burning via ISP **erases the bootloader** — USB upload
  stops working until you re-burn it.
- **Fuses (via avrdude/ISP only):** Uno stock = lfuse 0xFF, hfuse 0xDE, efuse 0xFD (0x05).
  Setting the wrong clock fuse (e.g. external crystal selected with no crystal) bricks the chip
  for normal ISP — recovery needs an injected clock. Never guess fuses; copy known-good values.
- **Brown-out:** efuse 0xFD = BOD 2.7V. Battery projects glitching at low voltage → check BOD.
- A bare ATmega328P on a breadboard at 16MHz needs: crystal + 2×22pF, 10kΩ RESET pull-up,
  100nF decoupling on each VCC/AVCC, AVCC connected (ADC dies otherwise).
- Pin 13 has the onboard LED (with buffer op-amp on Uno R3, bare on Nano — as INPUT on a Nano the
  LED+resistor acts as an unwanted pull-down; don't use 13 as a button input).

---

## 8. Pin Map & Special Functions (Uno/Nano)

| Pin | PWM | Special | Notes |
|---|---|---|---|
| 0 | — | UART RX | shared with USB — avoid |
| 1 | — | UART TX | shared with USB — avoid |
| 2 | — | INT0 | external interrupt |
| 3 | T2 | INT1 | interrupt + PWM |
| 4 | — | | |
| 5 | T0 | | 976Hz PWM |
| 6 | T0 | | 976Hz PWM |
| 7, 8 | — | | 8 = common tone() choice |
| 9 | T1 | | killed by Servo |
| 10 | T1 | SPI SS | killed by Servo; **must stay OUTPUT for SPI master mode** even if unused as CS |
| 11 | T2 | SPI MOSI | killed by tone() |
| 12 | — | SPI MISO | |
| 13 | — | SPI SCK | onboard LED |
| A0–A3 | — | analog in | also full digital pins (14–17) |
| A4 | — | **I2C SDA** | shared — can't use A4/A5 for ADC while Wire active |
| A5 | — | **I2C SCL** | |
| A6, A7 | — | **Nano only, analog INPUT ONLY** | no digitalRead/Write — analogRead only |
| AREF | — | external ADC ref | if used: `analogReference(EXTERNAL)` BEFORE first analogRead or you short the internal ref |

ADC notes: `analogRead` takes ~112µs. First reading after switching channels is noisy — read
twice and discard the first when multiplexing high-impedance sources (>10kΩ). For better than
±2 LSB, average 8–16 samples. `analogReference(INTERNAL)` = 1.1V ref, great for thermistors/
battery measurement via divider.

`INPUT_PULLUP` is ~20–50kΩ to 5V. Buttons: pin→button→GND with INPUT_PULLUP, pressed == LOW.
There are no internal pull-downs on AVR.

---

## 9. Working Patterns (copy these)

### Servo, correct power, no Timer surprises

```cpp
#include <Servo.h>
Servo s;                         // Timer1 now taken: pins 9/10 PWM dead
void setup() {
  s.attach(6, 544, 2400);        // pin 6 signal; pulse range tuned for SG90
  s.write(90);
}
// SG90: ~544µs=0°, ~2400µs=180°. Defaults (544–2400) usually fine; cheap clones vary.
// writeMicroseconds() for precision. Detach (s.detach()) to stop holding torque/jitter.
// POWER: servo red→external 5V ≥1A, brown→external GND AND Arduino GND, orange→pin 6.
```

### L298N / TB6612 DC motor (PWM off Timer1 pins is fine if no Servo)

```cpp
const uint8_t ENA = 5, IN1 = 7, IN2 = 4;   // ENA on Timer0 pin: 976Hz, no Servo conflict
void driveA(int16_t speed) {               // -255..255
  digitalWrite(IN1, speed > 0);
  digitalWrite(IN2, speed < 0);
  analogWrite(ENA, abs(speed));
}
// L298N drops ~2V (Darlington) — 6V battery gives motors ~4V. TB6612 drops ~0.1V; prefer it.
// Remove the L298N "5V-EN" jumper if motor supply >12V; below 12V the jumper lets its onboard
// regulator make 5V (can back-power the Arduino — fine, but never USB + that 5V simultaneously
// into the 5V pin).
```

### HC-SR04 ultrasonic, non-blocking-safe timeout

```cpp
const uint8_t TRIG = 7, ECHO = 8;
uint16_t readDistanceCm() {
  digitalWrite(TRIG, LOW);  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  uint32_t us = pulseIn(ECHO, HIGH, 25000UL);   // 25ms timeout ≈ 4m; NO timeout = 1s hang on no echo
  if (us == 0) return 0;                        // out of range
  return us / 58;                               // µs → cm
}
// Min cycle 60ms between pings (echo decay). pulseIn blocks up to timeout — for truly
// non-blocking, use NewPing library or echo-pin interrupt on pin 2/3.
```

### I2C device with the right failure handling

```cpp
#include <Wire.h>
void setup() {
  Wire.begin();                 // A4=SDA, A5=SCL; default 100kHz
  Wire.setClock(400000);        // only if all devices support Fast Mode
  Wire.beginTransmission(0x68);
  if (Wire.endTransmission() != 0) {
    Serial.println(F("MPU6050 not found - check wiring/address"));
    while (1) {}                // fail loudly, don't read garbage
  }
}
// I2C scanner first whenever an address is in doubt — modules lie (0x68 vs 0x69 via AD0, 0x3C
// vs 0x3D OLEDs, 0x27 vs 0x3F PCF8574 LCD backpacks).
// Wire has a 32-byte buffer: requestFrom()/write() bursts >32 bytes are silently truncated.
// Bus hangs (endTransmission never returns) = missing pull-ups or a slave holding SDA: power-
// cycle the slave, or clock out 9 pulses on SCL manually before Wire.begin().
```

### Software serial — know the limits

```cpp
#include <SoftwareSerial.h>
SoftwareSerial bt(10, 11);     // RX, TX — RX pin must support pin-change int (all Uno pins do)
bt.begin(9600);                // reliable ≤ 9600 on 16MHz when other interrupts exist;
                               // 57600 only if nothing else runs. RX is blocking & disables
                               // interrupts per bit — breaks Servo jitter-free operation and
                               // can corrupt NeoPixel timing. Only ONE SoftwareSerial can
                               // listen at a time (bt.listen()).
```

### Watchdog for field robustness

```cpp
#include <avr/wdt.h>
void setup() {
  wdt_disable();               // first thing — old-bootloader boards can boot-loop otherwise
  // ... init ...
  wdt_enable(WDTO_2S);
}
void loop() { wdt_reset(); /* work */ }
// WARNING: the OLD Nano bootloader does not clear WDT flags — a WDT reset can loop forever.
// Optiboot (Uno, new Nano bootloader) handles it correctly.
```

### EEPROM without wearing it out

```cpp
#include <EEPROM.h>
EEPROM.update(addr, val);      // update() writes ONLY if changed — always prefer over write()
EEPROM.put(0, myStruct);       // any POD type; get(0, myStruct) to read
// Each write = 3.3ms blocking. 100k cycles/cell: a write-per-loop kills a cell in <10 minutes.
```

---

## 10. Debugging Checklist (work top-down)

**Upload fails (`programmer is not responding`):**
1. Correct port selected? Board unplug/replug, watch which COM appears.
2. Nano → try *Processor: ATmega328P (Old Bootloader)*.
3. Anything on pins 0/1 or RESET? Disconnect, retry.
4. CH340 driver installed (clone Nano)? Charge-only USB cable? Try another cable/port.
5. Sketch from before spamming Serial at weird baud can sometimes block — hold RESET, release
   as upload starts ("Uploading..." appears).
6. All else fails: re-burn bootloader via ISP.

**Board resets randomly / Serial prints restart banner mid-run:**
1. Servo/motor on Arduino 5V rail → separate supply, common GND. (Most common cause.)
2. SRAM exhaustion → check globals %, remove String, add F().
3. Inductive spikes — flyback diode present? Decoupling caps (100nF) near noisy modules?
4. Brown-out: VIN too low under load, or USB hub current limit.

**Sketch runs but behaves wrong / variables corrupt:**
1. RAM (again). `freeRam()` < 200 bytes = found it.
2. Shared ISR variable missing `volatile` or atomic guard.
3. PROGMEM array read without `pgm_read_*`.
4. `int` overflow: `int` is **16-bit** on AVR (−32768..32767). `1000 * 60` overflows. Use
   `uint32_t`/`long` and `1000UL * 60`.
5. millis comparison not in `now - then >= dt` form.

**PWM/analogWrite does nothing:**
1. Pin actually PWM-capable (3,5,6,9,10,11)?
2. Servo attached anywhere → 9/10 dead. tone() active → 3/11 dead.
3. Pin set to OUTPUT? (analogWrite sets it, but a later digitalWrite or library may flip it.)

**I2C device not responding:**
1. Run the I2C scanner sketch. No devices found → wiring (SDA=A4, SCL=A5 swapped?), power,
   missing pull-ups (most modules have them; bare chips don't — add 4.7kΩ to VCC).
2. Found at unexpected address → use that address.
3. Works alone, fails with second device → address clash or total bus capacitance/pull-up issue.
4. 3.3V device on 5V bus → see §5.

**Serial garbage:**
1. Baud mismatch (monitor vs `Serial.begin`).
2. 3.3V/8MHz Pro Mini compiled as 16MHz board → all timing (and baud) is 2× off. Select
   *Pro Mini 3.3V/8MHz* explicitly.
3. RAM corruption (yes, again).

**Buttons trigger multiple times:** debounce — 30–50ms lockout or a debounce library; check
INPUT_PULLUP and wiring to GND (floating input reads noise).

**Servo jitters:** shared/weak power (fix first), SoftwareSerial active, long unshielded signal
wire, or cheap servo hitting end-stop (constrain write() to 10–170).

---

## 11. Decision Rules for Code Generation

1. Default board assumption: Uno/Nano 5V/16MHz unless told otherwise; ask if the user mentions
   "Nano 33", "Every", or "R4" — different chip, much of this file does not apply.
2. Always: `F()` on every literal in print calls, no `String`, no `delay()` in multi-task
   sketches, millis pattern from §6, `volatile` + atomic guard on ISR shares.
3. Choose pins to dodge conflicts up front: servos signal anywhere, PWM on 5/6 when Servo
   present, tone on 8, I2C reserved A4/A5, SPI reserved 10–13, keep 0/1 free.
4. Any actuator >20mA: driver stage + external power + common ground, stated explicitly in the
   wiring section of the answer.
5. State the wiring as a table (component pin → Arduino pin → power rail) before the code.
6. If flash >90% or globals >75%: act, don't warn — PROGMEM tables, F(), drop floats.
7. When the user reports "it worked, then stopped": rank causes as RAM > power > wiring,
   in that order, and check them in that order.
