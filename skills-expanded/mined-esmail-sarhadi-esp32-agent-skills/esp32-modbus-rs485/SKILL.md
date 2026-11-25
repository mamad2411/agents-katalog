---
name: esp32-modbus-rs485
description: Use when an ESP32 talks Modbus RTU over RS485 - wiring a MAX485, timing the DE pin, computing the CRC, or debugging a slave that never answers.
license: MIT
---

# Modbus RTU over RS485 on ESP32

Modbus is simple enough to look trivial and precise enough that every shortcut
produces silence. A slave that does not answer gives no error, so the timing and
the wiring have to be right by construction.

## The physical layer

- RS485 is a differential two-wire bus. `A` and `B` naming is not standardised:
  vendors swap them. If every frame times out, swap `A` and `B` before touching
  the code. This is the single most common cause of "no response".
- A MAX485 module has `DE` and `RE`; tie them together and drive the pin high to
  transmit, low to listen. If `DE` stays high, the transceiver holds the bus and
  no slave can answer.
- Long buses need 120 Ω termination at both physical ends, and a common ground
  between the nodes. Without the ground reference the differential pair drifts.

## The DE pin is a timing problem, not a wiring problem

The sequence has a trap: releasing `DE` before the last byte has left the UART
shift register truncates the frame, and the slave sees a CRC error.

```cpp
digitalWrite(DE_PIN, HIGH);          // take the bus
Serial1.write(frame, frameLen);
Serial1.flush();                     // wait until the last bit is out
digitalWrite(DE_PIN, LOW);           // release, now listen
```

`Serial1.write()` only fills the driver buffer. `Serial1.flush()` is the call
that waits for the wire. Dropping it works at 9600 on a fast board and fails at
115200, which is why it survives testing and breaks in the field.

## Frame timing

Modbus RTU delimits frames by silence: at least **3.5 character times** between
frames. At 9600 baud with 8N1, one character is 10 bits, about 1.04 ms, so the
gap is roughly 3.6 ms. At 115200 the gap is under 0.3 ms and a naive
`delay(10)` between frames is both too slow and, on a busy RTOS, not guaranteed.

- Do not send the next request until the response timeout has expired or the
  expected number of bytes arrived.
- The response timeout is the slave's problem, not yours: give it 100-300 ms
  before declaring a timeout.

## The CRC

CRC-16/MODBUS: initial value `0xFFFF`, polynomial `0xA001` (reflected), and the
result is appended **low byte first**.

```cpp
uint16_t modbusCrc(const uint8_t *buf, size_t len) {
  uint16_t crc = 0xFFFF;
  for (size_t i = 0; i < len; i++) {
    crc ^= buf[i];
    for (int bit = 0; bit < 8; bit++) {
      crc = (crc & 1) ? (crc >> 1) ^ 0xA001 : (crc >> 1);
    }
  }
  return crc;
}
```

## Register addressing

The protocol addresses holding registers from 0. Device documentation usually
numbers them from 1 and calls the first one `40001`. `40001` in a datasheet is
register `0` on the wire. An off-by-one here returns a valid frame with the
wrong value, which is worse than a timeout because nothing looks broken.

## Rules for the agent

- Always include `Serial1.flush()` before dropping `DE`, and comment why.
- Never compute the CRC by hand in the request; use the function, and append it
  low byte first.
- When a slave does not answer, ask in this order: A/B swapped? DE pin driven?
  baud and parity match? slave address correct? Only then look at the frame.
- Do not poll faster than the device's documented cycle time. Some meters answer
  a request per second and silently drop the rest.
