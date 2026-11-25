---
name: esp32-lora-and-lorawan
description: Use when an ESP32 drives a LoRa radio - the module never answers on SPI, DIO0 never fires, the join request is never accepted, or the gateway hears nothing. Covers SX127x wiring, airtime and duty cycle, and join failures.
license: MIT
---

# LoRa and LoRaWAN on ESP32

The radio is a separate chip on SPI. Almost every failure is one of three things:
the wiring, the interrupt line, or the duty cycle.

## Wiring the SX127x

- 3.3 V only. The module draws up to 120 mA during transmit at +20 dBm; a weak
  regulator browns out the ESP32 on every packet, which looks like a crash.
- SPI mode 0, up to 10 MHz. Long wires at 10 MHz give intermittent NOP answers.
- **DIO0 must be connected.** Polling the register works for a test and fails in
  production: you will miss the TxDone window and the driver will hang waiting.
- RESET must be a real GPIO. Tying it high leaves the chip in an undefined state
  after a brownout.

## Airtime is the design constraint

A 20 byte payload at SF12/125 kHz occupies the channel for 1.319 seconds. In the
EU868 band the legal duty cycle is 1 %, so that same packet may be sent once
every 132 seconds - 27 packets an hour, and no more. A design that reports every
30 seconds has to use a lower spreading factor, a shorter payload, or a
different band.

Those are not estimates. `tools/airtime.py` computes them from the Semtech
formula, including the low data rate optimize bit that changes the denominator
at SF11 and SF12 and that most hand calculations forget:

```bash
python tools/airtime.py --sf 12 --bw 125 --payload 20 --interval 30
#   airtime       1318.912 ms   (1.319 s)
#   earliest next packet  131.9 s
#   every 30.0 s is 4.4x over the duty cycle: ...
#   exit 1
```

The same 20 byte payload at SF7 is 56.6 ms, which allows one every 5.7 seconds.
The range difference between those two settings is the price of the interval.

Work out the airtime before choosing the interval, not after the gateway starts
dropping frames.

## Join failures

| What you see | What it means |
|---|---|
| join accept never arrives | wrong region/plan, or the gateway is on another sub-band |
| joins once, then never again | nonces lost on reset - the counter restarted |
| works near the gateway only | antenna mismatch, or the module is inside a metal box |
| accepted, then all uplinks fail | duty cycle limiter on the network server |
| RSSI good, SNR negative | interference, not distance - check the channel plan |

## Antenna and ground

The module needs a ground plane under it and a keepout around the antenna. A
quarter-wave wire soldered to the pad and folded against the PCB loses most of
its efficiency, and no amount of software gain fixes it.

## When it is not LoRaWAN

Point-to-point LoRa has no join, no duty-cycle limiter and no server: the two
ends must share frequency, spreading factor, bandwidth and sync word. A mismatch
in any one of them is silence, and the radio will happily report a successful
transmit.
