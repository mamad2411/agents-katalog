---
name: esp32-mcp4725-analog-output
description: Use when an ESP32 must output an analog voltage - 0 to 10 V command, valve position, 4-20 mA loop driver or a setpoint - with an MCP4725 or a similar I2C DAC. Covers reference, buffering and the load it cannot drive.
license: MIT
---

# Analog output with MCP4725

A DAC is not an analog output. The MCP4725 gives you a 12-bit voltage on a pin
that can source about 20 mA and cannot drive a cable, a valve or a 4-20 mA loop.

## The chain, not the chip

```
DAC -> op-amp buffer -> (optional gain x2.5) -> protection -> field terminals
```

- **Buffer** is mandatory for anything leaving the board. The DAC output
  impedance changes with code, so a load pulls the voltage down by an amount that
  depends on the value you set - a nonlinearity that looks like a software bug.
- **Gain** turns 0 to 4.096 V into 0 to 10 V with a non-inverting stage. The
  op-amp needs a rail above 10 V, so a 12 V supply is the usual choice.
- **Protection** on the field terminals: a miswired 24 V finds the op-amp
  otherwise.

## The reference decides everything

MCP4725 variants use VDD or an internal 2.048 V reference. With VDD as reference,
every millivolt of supply noise appears in the output. For a setpoint, use the
internal reference and a clean supply, or an external reference.

Code to volts: `V = code / 4096 * Vref`. One LSB on a 4.096 V reference is 1 mV;
after a x2.5 gain it is 2.5 mV at the terminals. State that in the design.

## I2C details that bite

- Address 0x60 to 0x67 by part and A0 strap.
- The write is 3 bytes (fast mode) or 5 bytes (write EEPROM). Writing EEPROM on
  every setpoint change wears it out and takes 25 ms - do not.
- On power-up the DAC loads from EEPROM. If you wrote a value once during a test,
  the output starts there forever until you rewrite it.

## Symptom table

| Symptom | Usually |
|---|---|
| output sags when the load connects | no buffer, load above 20 mA |
| output moves in steps larger than 1 LSB | wrong reference assumed |
| output starts at a random value at boot | EEPROM holds an old setpoint |
| 50 Hz ripple on the output | VDD reference, shared with a switching rail |
| device not found | address strap, 5 V pull-ups on a 3.3 V bus |

## Agent rules

- Never specify a DAC output as a field signal without a buffer and protection.
- State the reference, the gain and the resulting resolution in volts.
- Define the safe output at boot, before the first I2C write.
