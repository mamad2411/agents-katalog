---
name: esp32-i2c-bus
description: Use when adding I2C devices to an ESP32, when a sensor is not detected, or when the bus works alone and fails with a second device. Covers pull-ups, address conflicts, clock stretching and stuck-bus recovery.
license: MIT
---

# I2C on ESP32

I2C fails in ways that look like a broken sensor. Almost always it is the bus.

## Wiring, before any code

- Default pins on the Arduino core are `SDA=21`, `SCL=22`. Any pin can be used
  with `Wire.begin(sda, scl)`; changing them is not the problem, changing them
  to an input-only pin (`GPIO34`-`GPIO39`) is.
- **The internal pull-ups are not enough.** They are in the tens of kilo-ohms,
  which is fine for a slow single device and marginal for everything else.
  Add external resistors: roughly 4.7 kΩ for 100 kHz, 2.2 kΩ for 400 kHz. These
  are rules of thumb, not spec values.
- The I2C specification caps total bus capacitance at 400 pF. Long wires,
  dupont cables and many devices add up fast; when a bus works on a breadboard
  and fails on a 30 cm cable, this is why.
- A 5 V device on a 3.3 V bus needs a level shifter. A bare connection sometimes
  "works" and then damages the ESP32 later.

## Address conflicts

Most cheap sensors ship at a fixed address, and the popular ones share it:
two SSD1306 displays, or an BMP280 next to a BME280, both at `0x76`/`0x77`.
Scan first, then look for two devices answering the same address — the scan
will show one, and one of them will simply never respond again.

```cpp
for (uint8_t address = 1; address < 127; address++) {
  Wire.beginTransmission(address);
  if (Wire.endTransmission() == 0) {
    Serial.printf("found 0x%02X\n", address);
  }
}
```

## The three failure modes

1. **Nothing responds.** Pull-ups missing, `SDA`/`SCL` swapped, or the device is
   not powered. Measure the idle level: both lines must sit at 3.3 V.
2. **One device works, two do not.** Address conflict, or the pull-up is now
   too weak for the added capacitance.
3. **It works until the bus hangs.** A device held the line low mid-transfer.
   The bus is stuck: the master cannot generate a start condition because `SDA`
   is low. Recovery is to clock `SCL` manually nine times, then issue a stop.

```cpp
void i2cBusRecover(uint8_t sclPin) {
  pinMode(sclPin, OUTPUT);
  for (int i = 0; i < 9; i++) {
    digitalWrite(sclPin, LOW);
    delayMicroseconds(5);
    digitalWrite(sclPin, HIGH);
    delayMicroseconds(5);
  }
  pinMode(sclPin, INPUT);   // hand the line back to the peripheral
}
```

## Rules for the agent

- Never assume a sensor's address. Print it from a scan and put the real value
  in the code, with the scan output as a comment.
- If the user says "the sensor is not detected", ask for the scan output before
  changing any code. The scan distinguishes wiring from software in one step.
- Do not add `Wire.setClock(400000)` to fix slowness on a long cable. Slower is
  more reliable; the fix for a marginal bus is shorter wires and stronger
  pull-ups.
- Do not put I2C transactions in an ISR. `Wire` blocks and the ISR will hang the
  core.
