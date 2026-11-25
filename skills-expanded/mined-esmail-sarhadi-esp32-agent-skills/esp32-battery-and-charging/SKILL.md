---
name: esp32-battery-and-charging
description: Use when a battery-powered ESP32 dies early, the fuel gauge lies, the charger never finishes, or the board resets at low battery. Covers chargers, protection, measurement and the load-sharing problem.
license: MIT
---

# Battery and charging on ESP32

The ESP32 is not a low-power part. A Wi-Fi transmit burst is 240 mA peak, and
that peak is what decides whether the product works at 3.3 V from a battery.

## The peak, not the average

A Li-ion cell goes from 4.2 V to 3.0 V. An LDO that needs 3.3 V plus dropout
stops regulating at about 3.5 V, so the last 20 % of the cell is unusable and the
board browns out when the radio transmits - not when the battery is empty. Use a
buck-boost, or accept the cutoff and size the battery accordingly.

A 100 µF (or larger) bulk capacitor next to the radio absorbs the transmit burst.
Without it, the peak current comes from the cell through the protection circuit,
and the drop is what resets the chip.

## The charger is not a power path

TP4056 charges at up to 1 A and has no load-sharing: while charging, the load
sees the battery node, which sits between 3.0 and 4.2 V depending on charge
state. A product that must run while charging needs a power-path IC (BQ24074,
MCP73871) or a separate 5 V rail for the load. This is the single most common
mistake in hobby designs that become products.

## Measuring the charge

| Method | Reality |
|---|---|
| ADC on a divider | simple, and the divider itself drains the cell (two 100 k resistors = 20 µA) |
| Fuel gauge (MAX17048, BQ27441) | gives state of charge, costs a part and an I2C address |
| Counting coulombs | drifts; needs a full cycle to re-calibrate |

A Li-ion discharge curve is flat between 3.9 and 3.6 V: an ADC voltage reading
tells you "somewhere in the middle" for most of the runtime. If the UI shows a
percentage, a fuel gauge is the honest way to get it.

Measure with the radio off, or the reading is the transmit sag, not the cell.

## Deep sleep is where the budget is won

- The regulator's quiescent current is often larger than the ESP32's sleep
  current: 3.3 V LDOs run 50 µA to 1 mA. Pick one with a real low-Iq spec, or
  switch it off with a load switch during sleep.
- A USB-serial chip (CP2102, CH340) draws 100 to 300 µA and keeps the board
  awake-ish. Remove it from the battery path.
- An LED with a 1 k resistor is 1.3 mA - more than the whole sleep budget.
- Measure the sleep current with a µA meter, on the final board, with everything
  populated. The datasheet number is not your number.

## Protection

A bare 18650 without a protection circuit is a fire. Either use a protected cell
or add DW01 + dual MOSFET. Also: never charge below 0 °C, and a product that
charges unattended should have a thermistor input on the charger IC.

| Symptom | Usually |
|---|---|
| resets when the radio transmits | no bulk capacitor, or an LDO near dropout |
| battery reads full, dies in an hour | measuring the charger node, not the cell |
| never finishes charging | no thermistor, or a load larger than the termination current |
| runs while charging, then dies | no power path, cell discharged through the load |
| sleep current 10x the datasheet | LDO Iq, USB chip, or an LED |
