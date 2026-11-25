---
name: esp32-pin-safety
description: Use when choosing, reviewing or debugging ESP32 GPIO assignments in firmware. Catches the four failure modes that compile cleanly and then kill the board — flash pins, input-only pins, strapping pins, ADC2 with Wi-Fi — before anything is flashed.
license: MIT
---

# ESP32 pin safety

Most ESP32 firmware that "compiles but does not work" fails on the pin map, not
on the logic. Check the pin map before writing driver code.

## Order of checks

Work through these in order. Each one can invalidate everything after it.

1. **Does the pin exist on this module?**
   `GPIO6`-`GPIO11` are wired to the SPI flash. `GPIO16`/`GPIO17` exist only on
   WROVER modules; on WROOM they are inside the PSRAM package. Touching either
   group produces a board that will not boot, not an error message.
2. **Is the pin allowed to drive an output?**
   `GPIO34`-`GPIO39` are input-only. They have no output driver and no internal
   pull-up or pull-down. A button on `GPIO34` needs an external resistor; a relay
   on `GPIO34` will simply never switch.
3. **Is it a strapping pin?**
   `GPIO0`, `GPIO2`, `GPIO5`, `GPIO12`, `GPIO15` are sampled at reset to pick the
   boot mode and the flash voltage. They are usable, but only if whatever is
   attached cannot hold them at the wrong level during power-up. `GPIO12` HIGH on
   a 3.3 V module selects 1.8 V flash and the board stays dark.
4. **Does it need the ADC?**
   ADC2 pins (`GPIO0`, `2`, `4`, `12`-`15`, `25`-`27`) return garbage while Wi-Fi
   is active. If the sketch reads an analog sensor and also joins a network, move
   the sensor to an ADC1 pin (`GPIO32`-`GPIO39`).
5. **Is it already taken?**
   `GPIO1`/`GPIO3` are UART0. The serial monitor owns them until you remap the
   console, and remapping it early removes your only debugging channel.

## Rules for the agent

- Never invent a pin number. Ask for the board variant or read it from the
  project's `platformio.ini` / `pins_arduino.h`.
- Prefer `GPIO32`-`GPIO33` for analog inputs, `GPIO25`-`GPIO27` for outputs that
  must be quiet at boot, and `GPIO4`/`GPIO13`-`GPIO14` for I2C when Wi-Fi is on.
- When a pin is only *conditionally* safe (strapping, UART0), say so in a comment
  next to the `#define` and state the condition. Silence reads as approval.
- If the user asks for a pin that is on the forbidden list, do not silently
  substitute another one. Explain the constraint and offer two alternatives.

## Automated check

`tools/pincheck.py` encodes the constraints above for `esp32`, `esp32s3` and
`esp32c3`:

```bash
python tools/pincheck.py --soc esp32 --assign "12=relay,34=button,6=led"
python tools/pincheck.py --soc esp32 --file examples/pinmap.txt --json
```

It exits non-zero on errors, so it can run in CI or in a pre-flash hook.

## Worked example

```
$ python tools/pincheck.py --soc esp32 --assign "12=relay1,34=button,6=status_led"

  GPIO6   ERROR  status_led     GPIO6 is connected to the SPI flash, using it bricks the module
  GPIO12  WARN   relay1         GPIO12 is a strapping pin and must be LOW at boot ...
  GPIO34  WARN   button         GPIO34 is input-only ...
```

The fix in that case is `GPIO26` for the relay, `GPIO32` for the button with a
10 kΩ pull-up, and `GPIO2` or `GPIO25` for the status LED — `GPIO2` is itself a
strapping pin, so `GPIO25` is the safer of the two.

## Reference

[`reference/pin-table.md`](reference/pin-table.md) - Every GPIO of all three SoCs, with the strapping reason spelled out.
