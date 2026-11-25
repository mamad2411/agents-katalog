---
name: routeros-hardware
description: MikroTik hardware knowledge for RouterOS. Covers decoding product codes and model naming, the 246 product user manuals (ports, power inputs, buttons, LEDs, reset and Netinstall sequences per model) with a search script, RouterBOOT firmware and /system/routerboard, Protected RouterBOOT, reset and mode button scripts, PoE-out standards, power classes, port statuses and power-cycle ping, LEDs and LED dark mode, serial and USB ports, USB power reset, LCD touchscreen, S+RJ10 placement, grounding, supported modems and the pre-RMA checklist. Use when identifying or choosing a MikroTik device, looking up a model's ports or reset procedure, debugging PoE, power or boot problems, or checking regulatory and safety information.
---

# RouterOS hardware

The references hold the manual for every product (`references/products/<model>.md`, with safety and regulatory text split into
`references/regulatory/<model>.md`) and the general hardware guides. Specifications such as CPU, RAM, throughput and price live on
mikrotik.com product pages, which are not part of these references; the product manual says how to power, set up and reset the device.

## Find a product

```bash
python scripts/find_product.py hap ac                       # all terms must match title, file name or text
python scripts/find_product.py --category "LTE products" sim
python scripts/find_product.py --grep "passive poe" --limit 5
python scripts/find_product.py --list-categories
```

Categories: Switches, LTE products, Ethernet routers, Wireless systems, Indoor wireless, IoT products, Accessories, 60 GHz products, RouterBOARD,
Data over Powerlines, Antennas, Interfaces. `/system/routerboard/print` on a device gives its exact `model` (for example `CCR2116-12G-4S+`),
`serial-number`, and `current-firmware` against `upgrade-firmware`.

## Decode a model name

`<board name><features>-<built-in wireless> <wireless card features>-<connector>-<enclosure>`. Board names are three symbols (series, wired
interface count, wireless interface count) or words (hAP, hEX, cAP, wAP, SXT, LHG, Groove, Metal, OmniTIK, ...). Feature letters: `U` USB, `P`
power injection with controller, `i` single-port injector, `A` more memory or higher licence, `H` stronger CPU, `G` gigabit, `L` lite, `D` extra
disk, `S` SFP, `e` PCIe extension, `xN` cores, `R` miniPCIe, `M` M.2. Wireless part: band (`2`, `5`, `52` dual, `6`), power (`H`, `HP`, `SHP`),
protocol (`n`, `ac`, `ax`, `be`), chains (`D` two, `T` three, `Q` four ...). Full tables: `references/guides/hardware/product-naming.md`.

## RouterBOOT, buttons and recovery

```ros
/system/routerboard/print
/system/routerboard/upgrade                    # then /system/reboot; compare current-firmware and upgrade-firmware
/system/routerboard/settings/print
```

- Keep the firmware current after RouterOS upgrades (`routeros-install-upgrade`). `preboot-etherboot=9s preboot-etherboot-server=10.10.10.100`
  makes a device look for a Netinstall server at every boot, which allows remote reinstall with a power cycle; disable the server afterwards.
- **Protected RouterBOOT** (`protected-routerboot=enabled`, change confirmed by pressing the button within 60 s) disables the reset button and
  pin-hole, the RouterBOOT serial menu and Netinstall. With a forgotten password the only way out is the emergency reformat (hold reset at power-on
  longer than `reformat-hold-button`, shorter than `reformat-hold-button-max`), which erases everything and needs Netinstall. Never enable it on a
  device you might lose the password for.
- Reset button sequences differ slightly per model (see the product's "Buttons and jumpers" section): hold at power-on to load the backup
  bootloader; release when the LED flashes to reset the configuration; hold about 5 s more for CAPs mode; hold until the LED sequence finishes for Netinstall mode.
- Mode, reset and WPS (D53, C53, S53, H53 series) buttons can run scripts: `/system/routerboard/mode-button/set on-event=<script> hold-time=3..5
  enabled=yes`, and the same under `/system/routerboard/reset-button`. Supported models are listed in the RouterBOARD guide.

## PoE

PoE out uses RJ45 mode B (pins 4,5 positive, 7,8 negative). Standards on MikroTik devices: passive PoE up to 30 V, passive PoE up to 57 V, IEEE
802.3af/at, 802.3bt. The model's specification shows which: a "Low voltage PoE-Out current limit" entry means passive up to 30 V, an extra "High
voltage" entry means up to 57 V as well.

| Class | Standard | PSE output | PD available |
| --- | --- | --- | --- |
| 0 to 3 | 802.3af | 15.4 W | 12.95 W |
| 4 | 802.3at | 30 W | 25.5 W |
| 5, 6 | 802.3bt Type 3 | 45 W, 60 W | 40 W, 51 W |
| 7, 8 | 802.3bt Type 4 | 75 W, 90 W | 62 W, 71.3 W |

```ros
/interface/ethernet/poe/print
/interface/ethernet/poe/monitor [find]                         # poe-out-status, voltage, current, power
/interface/ethernet/poe/set ether3 poe-out=auto-on poe-voltage=auto poe-priority=10
/interface/ethernet/poe/power-cycle ether3 duration=5s
/interface/ethernet/poe/set ether3 power-cycle-ping-enabled=yes power-cycle-ping-address=192.168.88.50 power-cycle-ping-timeout=1m
```

- Statuses worth knowing: `waiting-for-load` (nothing to power, detection needs 3 k to 26.5 k ohm), `short-circuit`, `overload` (current limit),
  `voltage-too-low` or `-high` (supply does not fit the PD), `current-too-low` (PD draws under 10 mA), `no-valid-PSU` (input cannot support PoE out),
  `low-voltage-pd-detected` (set `poe-voltage=low`), `voltage-on-poe-in` (another source feeds the port), `lldp-power-off`.
- With passive PoE the output voltage follows the supply voltage: 18 V minimum is recommended, and the supply must fit what the PD accepts
  (`voltage-too-high` or `low-voltage-pd-detected` otherwise). Third-party PDs on passive ports can classify too low and run reduced.
- Power-cycle ping needs a route to the PD for an IP address, or a MAC address for a directly attached PD; `power-cycle-interval` reboots the PD periodically.
- Logs use topics `poe-out` and `poe-in`; SNMP exposes PoE out under `1.3.6.1.4.1.14988.1.1.15` (`routeros-diagnostics-monitoring`).
- Power budget tables per model are in `references/guides/hardware/poe-out.md` ("How to choose your PoE PSE").

## LEDs, ports, USB, LCD

- `/system/leds` configures what each LED shows (signal strength, interface activity or speed, modem signal, fan fault). Not every board supports it.
  `/system/leds/settings/set all-leds-off=after-1min|after-1h|immediate|never` is LED dark mode on supported models (some LEDs cannot be turned off).
- `/port` lists serial and USB ports (`baud-rate` default `auto`, `data-bits`, `parity`, `stop-bits`, `flow-control`). `serial0` is the console
  by default and must be released before another service uses it. `/port/remote-access/add port=serial0 protocol=rfc2217 tcp-port=9999` shares a
  serial device over TCP; restrict `allowed-addresses`.
- `/system/routerboard/usb/power-reset duration=10s [bus=1]` cuts power to a USB port to restart a stuck modem without physical access.
- `/lcd` configures the touchscreen of RB2011U and CCR models (`read-only-mode` is on by default; `backlight-timeout`, `default-screen`).
- **S+RJ10** copper modules run hot (about 2.7 W): put them in every second SFP+ cage with an optical module or an empty port between, or add cooling.
- Grounding: use shielded cable and lightning arresters on external antennas, 2.5 to 4 mm2 copper wire to the grounding point; never power a
  MikroTik device from a PSE whose positive terminal is connected to protective earth.

## Before an RMA

Try another power supply or injector, load the backup bootloader (hold reset at power-on for 2 to 3 s) and run `/system/routerboard/upgrade`,
reinstall with Netinstall, upgrade RouterOS, and reset the configuration. For LTE: check SIM orientation, APN and that the modem is installed
(`routeros-mobile-networking`). If nothing helps, contact MikroTik support with a supout.rif (`routeros-troubleshooting`). Checklist:
`references/guides/hardware/try-before-rma.md`.

## Where to look

| Need | Open |
| --- | --- |
| Product manual for a model (ports, power input, buttons, setup) | `references/products/<model>.md` (search with `scripts/find_product.py`) |
| Safety and regulatory text of a model | `references/regulatory/<model>.md` |
| Naming scheme | `references/guides/hardware/product-naming.md` |
| RouterBOOT, Protected RouterBOOT, buttons | `references/guides/hardware/routerboard.md` |
| PoE, LEDs, ports, USB, LCD, grounding, peripherals (supported modems) | `poe-out.md`, `leds.md`, `ports.md`, `usb-features.md`, `lcd-touchscreen.md`, `grounding.md`, `peripherals.md` in the same folder |
| Quick guides and regulatory PDFs for newer devices | `references/help/quick-guides/`, `references/help/compliance.md` |
| Properties | `references/cli/interface/ethernet/poe.md`, `references/cli/port.md`, `references/cli/system/leds.md`, `references/cli/lcd.md` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-ethernet` (links, SFP, MTU), `routeros-mobile-networking` (LTE hardware), `routeros-wireless`,
`routeros-install-upgrade` (Netinstall, licence levels), `routeros-troubleshooting`, `routeros-system-utilities` (device mode).
