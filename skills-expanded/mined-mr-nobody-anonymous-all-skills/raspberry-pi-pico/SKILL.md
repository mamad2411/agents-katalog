---
name: raspberry-pi-pico
description: "Use when writing firmware for Raspberry Pi Pico, Pico W, Pico 2, or any RP2040/RP2350 board. Covers PIO state machines for precise timing, dual-core programming with _thread, ADC quirks (internal temp sensor, VSYS divider), the GP25 LED vs Pico W WiFi-chip LED trap, UF2 flashing, and 3.3V-only GPIO constraints."
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


# Raspberry Pi Pico / Pico W (RP2040)

## Identity Card — know which board you have

| | Pico | Pico W | Pico 2 (RP2350) |
|---|---|---|---|
| MCU | RP2040, 2× Cortex-M0+ @ 133 MHz | RP2040 | RP2350, 2× Cortex-M33 @ 150 MHz |
| Flash | 2 MB QSPI (W25Q16) | 2 MB | 4 MB |
| SRAM | 264 KB | 264 KB | 520 KB |
| WiFi | none | CYW43439 (2.4 GHz only, no 5 GHz) | W variant only |
| Onboard LED | **GP25** | **NOT a GPIO — on the CYW43 chip** | GP25 |
| ADC | 3× external (GP26-28) + temp | same, but **GP29 shared with WiFi** | same |
| USB | micro-USB, USB 1.1 FS (12 Mbps) | same | same |

**GPIO is 3.3V ONLY. Not 5V tolerant. No exceptions.** Connecting a 5V signal (classic HC-SR04 echo pin, 5V-powered encoder outputs, Arduino Uno TX) to any GP pin will degrade or kill that pin. Use a voltage divider (1kΩ + 2kΩ) or a level shifter (BSS138 module) for every 5V input. 5V *outputs from* the Pico don't exist — if a peripheral needs 5V logic-high to register (some relay modules, WS2812 at 5V supply), it usually still works at 3.3V, but WS2812 data is marginal at 5V supply: power the strip at 5V and either use a 74AHCT125 level shifter or drop strip VCC to ~4.3V via a diode.

## Power pins — the part everyone wires wrong

```
Pin 40  VBUS   — 5V straight from USB connector. Output only when USB plugged in.
Pin 39  VSYS   — main system input, 1.8V–5.5V. Feed batteries HERE, not VBUS.
Pin 36  3V3(OUT) — output of onboard SMPS, max ~300 mA spare for peripherals.
Pin 37  3V3_EN — pull LOW to shut down the 3.3V regulator (soft power-off).
Pin 35  ADC_VREF — ADC reference; noisy by default (shared with 3V3 via filter).
```

- Battery power: 3×AA or 1S LiPo → **VSYS** through a Schottky diode (so USB and battery can coexist). Never feed a battery into VBUS — it back-powers the USB port.
- Do NOT power servos or motors from 3V3(OUT). It browns out the RP2040 → random resets that look like firmware bugs. Servos get their own 5V supply, **grounds tied together**.
- VSYS/3 is internally wired to **ADC3 (GP29)** via a divider — you can read your battery voltage: `vsys = adc3.read_u16() * 3 * 3.3 / 65535`. On **Pico W this conflicts with WiFi** (GP29 doubles as SPI CLK for CYW43) — read it only while WiFi is idle, and set GP25 high during the read on W.

## UF2 flashing and the BOOTSEL workflow

- Hold **BOOTSEL**, plug USB (or pulse RUN pin 30 low while holding BOOTSEL) → board enumerates as `RPI-RP2` mass-storage drive. Drag a `.uf2` on; it reboots automatically.
- MicroPython firmware: Pico and Pico W have **different UF2 files**. Flashing plain-Pico MicroPython on a Pico W boots fine but `import network` fails with `ImportError` — this confuses everyone. Get the `-w` build.
- **Flash nuke**: if the filesystem is corrupted (common after yanking USB during a write), flash `flash_nuke.uf2` first, then re-flash MicroPython. Symptoms of corruption: Thonny hangs at "Connecting", or `OSError: [Errno 5] EIO` on file ops.
- From running MicroPython, reboot to BOOTSEL programmatically: `machine.bootloader()`. From Arduino/C SDK: `rom_reset_usb_boot(0,0)` or double-tap reset if the board has a reset button + appropriate bootloader.
- Arduino IDE: use **earlephilhower/arduino-pico** core (not the mbed one — mbed core is deprecated, slower, no PIO API). Board appears as a UF2 drive on first flash; afterwards the core auto-resets via 1200-baud touch.
- `main.py` runs at boot in MicroPython. If `main.py` has a tight loop with no `sleep`, the USB REPL can become unreachable — always keep a way in: hold BOOTSEL + flash nuke is the recovery path. Putting `time.sleep_ms(10)` per loop iteration, or a startup delay (`time.sleep(3)`) before the main loop, saves you.

## Onboard LED — the Pico W trap

```python
# Pico (non-W): LED is GP25
led = machine.Pin(25, machine.Pin.OUT)

# Pico W: GP25 is the WiFi chip's SPI CS. The LED hangs off the CYW43.
led = machine.Pin("LED", machine.Pin.OUT)   # string "LED", works on BOTH boards
```

`Pin("LED")` is the portable form — use it always. On Pico W, `Pin(25)` doesn't error; it silently does nothing visible (and can disturb WiFi). In Arduino (earlephilhower core), `LED_BUILTIN` is mapped correctly for both as long as you selected the right board; `digitalWrite(25, ...)` on a W is the same trap. Also note: the Pico W LED **cannot be PWM-dimmed** (it's behind the WiFi chip's GPIO, not an RP2040 PWM slice).

## ADC — 4 channels, 3 usable pins, 1 temperature sensor

| Channel | Pin | Notes |
|---|---|---|
| ADC0 | GP26 | general |
| ADC1 | GP27 | general |
| ADC2 | GP28 | general |
| ADC3 | GP29 | hardwired to VSYS/3; WiFi conflict on Pico W |
| ADC4 | — | **internal temperature sensor**, no pin |

- 12-bit SAR, 500 ksps. MicroPython `read_u16()` returns 0–65535 (left-shifted 12-bit).
- ADC pins are **NOT 5V tolerant** and also not even fully 3.3V-spec'd through the ESD diodes — keep inputs ≤ ADC_VREF.
- Known silicon erratum (RP2040-E11): DNL spikes at codes 512/1536/2560/3584 — readings cluster around these values. For precise analog work, oversample 16× and average, or use an external ADC (ADS1115).
- The ADC is noisy when WiFi is active (Pico W) and when the SMPS is in PFM mode. Drive **GP23 (Pico) / WL_GPIO1 (Pico W) high** to force the regulator into PWM mode for cleaner analog readings:

```python
# MicroPython — internal temperature, both cores' classic example
import machine
sensor = machine.ADC(4)
machine.Pin(23, machine.Pin.OUT, value=1)  # plain Pico: quieten SMPS (skip on W)
def read_temp_c():
    v = sensor.read_u16() * 3.3 / 65535
    return 27 - (v - 0.706) / 0.001721     # datasheet formula, ±2°C at best
```

```cpp
// Arduino (earlephilhower core)
float readTempC() {
  return analogReadTemp();   // built-in, handles ADC4 selection
}
// Raw channel read: analogReadResolution(12); analogRead(A0); // A0=GP26
```

The temp formula constants (0.706 V, -1.721 mV/°C) vary chip to chip — treat absolute accuracy as ±3°C uncalibrated. Good for "is the chip overheating", bad for room thermometers.

## PWM — 8 slices, 16 channels, the pairing rule

- 8 PWM slices × 2 channels (A/B). **GP(n) and GP(n+16) share the exact same slice channel** — driving PWM on GP0 and GP16 simultaneously gives you ONE signal, not two independent ones.
- Pins on the same slice (e.g., GP0/GP1 = slice 0 A/B) share **frequency** but have independent **duty**. You cannot run 50 Hz servo on GP0 and 25 kHz motor PWM on GP1.
- Plan pin allocation: servos (50 Hz) on one slice's pins, motor drivers (20–25 kHz, above audible) on another.

```python
# MicroPython servo on GP2 — duty_u16, NOT duty (that's ESP32 API)
from machine import Pin, PWM
servo = PWM(Pin(2))
servo.freq(50)
def angle(deg):  # 500–2500 µs pulse over 20 ms period
    us = 500 + deg * 2000 // 180
    servo.duty_u16(int(us * 65535 / 20000))
```

```cpp
// Arduino: analogWriteFreq + analogWriteRange (earlephilhower extensions)
analogWriteFreq(25000);      // 25 kHz for DRV8833/TB6612
analogWriteRange(1023);
analogWrite(4, 512);         // 50% on GP4
```

## PIO — the RP2040 superpower

PIO gives cycle-exact timing independent of the CPU: WS2812 without bit-banging, quadrature decode without interrupts, extra UARTs, ultrasonic echo timing. 2 PIO blocks × 4 state machines, 32 instruction slots per block (shared by all programs loaded into that block).

Rules that bite:
- Max 32 instructions per PIO block, total, across all loaded programs. Loading a 5th program that overflows raises `OSError: [Errno 12] ENOMEM` in MicroPython.
- `sm.active(1)` starts it; a state machine left running keeps driving pins after a soft reboot — call `sm.active(0)` in cleanup, or pins stay stuck.
- Each instruction can carry side-set and delay; `[n]` delays count toward the cycle budget.

WS2812 (NeoPixel) — the canonical PIO use. In MicroPython ≥1.20 just use the built-in:

```python
import neopixel, machine
np = neopixel.NeoPixel(machine.Pin(6), 30)   # uses PIO under the hood on RP2040
np[0] = (255, 0, 0); np.write()
```

Custom PIO example — precise pulse counter (e.g., wheel encoder edges) with zero CPU load:

```python
import rp2
from machine import Pin

@rp2.asm_pio()
def edge_counter():
    wrap_target()
    wait(0, pin, 0)        # wait for low
    wait(1, pin, 0)        # rising edge
    jmp(x_dec, "next")     # decrement X (counts edges; X starts at 0 → wraps)
    label("next")
    wrap()

sm = rp2.StateMachine(0, edge_counter, freq=10_000_000, in_base=Pin(14))
sm.exec("set(x, 0)")
sm.active(1)
def read_count():
    sm.exec("mov(isr, x)"); sm.exec("push()")
    return (-sm.get()) & 0xFFFFFFFF   # X counted DOWN
```

```cpp
// Arduino/C SDK: generate a 1 µs-resolution pulse train via PIO
// Use the pioasm-generated header, then:
// uint offset = pio_add_program(pio0, &myprog_program);
// myprog_program_init(pio0, 0, offset, PIN);
// For HC-SR04 echo timing in C++, pulseIn() on the earlephilhower core is
// actually reliable (it uses busy-wait at 133 MHz) — PIO is for when the CPU
// must do other work simultaneously.
```

PIO clock: `freq=` sets the state-machine clock (min ~1908 Hz due to 16.8 divider limit, max = sys clock 125 MHz). Each `wait`/`jmp`/`set` is one cycle at that clock — do your timing math from there.

## Dual core — _thread in MicroPython

Core 1 is real and useful: run sensor polling / PID on core 1 while core 0 handles WiFi or USB.

```python
import _thread, time
from machine import Pin

lock = _thread.allocate_lock()
shared = {"distance_mm": 0}

def core1_sensor_loop():
    while True:
        d = read_ultrasonic()          # blocking 30 ms measurement, fine here
        with lock:
            shared["distance_mm"] = d
        time.sleep_ms(50)

_thread.start_new_thread(core1_sensor_loop, ())

while True:   # core 0
    with lock:
        d = shared["distance_mm"]
    drive_logic(d)
    time.sleep_ms(20)
```

Hard-won rules:
- **Only 2 threads total** (one per core). A second `start_new_thread` while core 1 runs raises `OSError: core1 in use`.
- **Protect shared state with a lock.** Single dict reads of small ints are atomic-ish in practice, but compound read-modify-write is not.
- **Core 1 + flash writes don't mix**: writing files (or `machine.freq()` changes) from core 0 while core 1 executes from flash can hard-fault on some firmware versions. Keep file I/O off the hot path, or pause core 1 around it.
- **KeyboardInterrupt only stops core 0.** Core 1 keeps running until power cycle — design a `running = False` flag the thread checks.
- On **Pico W, do NOT touch the `network` module from core 1** — the WiFi driver is not thread-safe; keep all socket/WiFi calls on core 0.
- Garbage collection pauses BOTH cores. For motor-control timing tighter than ~1 ms, pre-allocate buffers and call `gc.collect()` at controlled moments, or move the timing-critical part into PIO.

Arduino dual core (earlephilhower): define `setup1()`/`loop1()` — they run on core 1 automatically. Use `rp2040.fifo.push()/pop()` for inter-core messages (hardware FIFO, 8 entries deep, blocking when full/empty).

```cpp
void setup1() {}
void loop1() {                       // core 1: sensor
  uint32_t d = readUltrasonicMm();
  rp2040.fifo.push(d);               // blocks if FIFO full
}
void loop() {                        // core 0: control
  uint32_t d;
  if (rp2040.fifo.pop_nb(&d)) driveLogic(d);
}
```

## WiFi on Pico W (CYW43439)

```python
import network, time
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm=0xa11140)            # disable WiFi power-save — CRITICAL for servers
wlan.connect("SSID", "password")
deadline = time.ticks_add(time.ticks_ms(), 15000)
while not wlan.isconnected():
    if time.ticks_diff(deadline, time.ticks_ms()) < 0:
        raise RuntimeError(f"wifi failed, status={wlan.status()}")
    time.sleep_ms(200)
print(wlan.ifconfig()[0])
```

- `pm=0xa11140` (power-save off) is the single most important line: without it, a Pico W web server responds in 2–8 **seconds** instead of milliseconds, because the radio sleeps between beacons.
- 2.4 GHz only. WPA3-only networks fail with status `-3` (CONNECT_FAIL); mixed WPA2/WPA3 works.
- `wlan.status()` codes: 3 = got IP, -1 = generic fail, -2 = no AP found (wrong SSID or 5 GHz-only), -3 = bad auth.
- Country code matters for channels 12–13: `rp2.country('GB')` before activating, on firmware that supports it.
- WiFi + ADC3, GP23/GP24/GP25 are all repurposed on the W (see LED section). GP23 = WiFi power-save control, GP24 = VBUS sense — don't use them as GPIO on the W.

## I2C / SPI / UART pin map

Any function appears on multiple pins, but only specific sets per controller. Defaults in MicroPython:

```python
from machine import I2C, SPI, UART, Pin
i2c0 = I2C(0, sda=Pin(0), scl=Pin(1), freq=400_000)   # also GP4/5, GP8/9, GP12/13, GP16/17, GP20/21
i2c1 = I2C(1, sda=Pin(2), scl=Pin(3), freq=400_000)   # also GP6/7, GP10/11, GP14/15, GP18/19, GP26/27
spi0 = SPI(0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
uart0 = UART(0, 115200, tx=Pin(0), rx=Pin(1))          # uart1: tx=GP4/8, rx=GP5/9
```

- `I2C(0, sda=Pin(2), ...)` raises `ValueError: bad SDA pin` — SDA must be an I2C0-capable pin for controller 0. When an I2C constructor errors, it's almost always controller/pin mismatch, not hardware.
- No internal I2C pull-ups worth using — add 4.7 kΩ external pull-ups to 3V3 if your breakout lacks them (most breakouts have them).
- `i2c.scan()` first, always. Empty list = wiring/pull-up problem; never debug driver code before scan succeeds.

## The 5 mistakes everyone makes

1. **Feeding 5V into a GPIO** (HC-SR04 echo, 5V-Arduino serial). Divider or level shifter, every time. The HC-SR04 itself runs fine powered at 5V with a divider on echo only (trigger accepts 3.3V).
2. **`Pin(25)` for the LED on a Pico W.** Use `Pin("LED")`.
3. **Powering motors/servos from 3V3(OUT)** → brownout resets misdiagnosed as software crashes. Separate supply, common ground.
4. **Putting two "independent" PWMs on GP-n and GP-n+16**, or two different frequencies on one slice. Check the slice map before assigning pins.
5. **Forgetting `pm=0xa11140` on Pico W servers**, then blaming MicroPython for multi-second latency.

## Debugging checklist

- Board not enumerating? Many micro-USB cables are charge-only. Swap the cable before anything else.
- Thonny can't connect / EIO errors → corrupted flash FS → `flash_nuke.uf2`, re-flash MicroPython.
- `import network` ImportError → you flashed non-W firmware on a Pico W.
- Random resets under load → measure VSYS with a scope/meter while motors run; brownout if it dips below ~1.8 V. Add bulk capacitance (470 µF on motor rail) and separate supplies.
- ADC reads jumpy → GP23 high (PWM SMPS mode), average 16 samples, check for WiFi activity, remember the E11 DNL erratum codes.
- PIO `ENOMEM` → 32-instruction budget per block exceeded; move a program to the other PIO block (`rp2.StateMachine(4..7)` uses PIO1).
- Pin stuck high/low after soft reset → an active state machine or PWM slice survives soft reboot; `machine.reset()` (hard) clears it, or explicitly deinit.
- Code runs in Thonny but not standalone → it's not saved as `main.py` on the device, or it crashes before USB is ready — add `time.sleep(2)` at the top and write exceptions to a log file to diagnose.
