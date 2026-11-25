---
name: unit-converter
description: >
  Converts values between units of measurement across categories: length (km, miles,
  feet, inches), weight (kg, lbs, oz, stone), temperature (Celsius, Fahrenheit, Kelvin),
  volume (liters, gallons, cups, ml), area (m², acres, ft²), speed (km/h, mph, knots),
  time (seconds to years), data storage (bytes to petabytes), pressure, and energy.
  Use when the user asks to convert, calculate, or express a measurement in different units.
license: Apache-2.0
metadata:
  author: ai-powered-apps-development-expert
  version: "1.0"
allowed-tools: execute_code
---

# Unit Converter

Performs a one-shot conversion between two units that belong to the same physical category.

## Function

`convert_units(value, from_unit, to_unit)` → `(result: float, category: str)`

- `result` is `value` expressed in `to_unit`.
- `category` is the detected physical category — one of `length`, `weight`, `temperature`, `volume`, `area`, `speed`, `time`, `data`, `pressure`, `energy`.
- Unit names are case-insensitive and accept common aliases: `pounds`, `lbs`, `lb`, and `pound` all refer to the same unit; so do `kilometers`, `kilometer`, and `km`; `sec` is accepted as `seconds`; and so on. See [references/examples.md](references/examples.md) for the full alias list per category.

A `fmt(value)` helper is also provided for pretty-printing numeric results (scientific notation for very large or very small values, comma grouping for thousands).

## Errors

`convert_units` raises `ValueError`:

- `Unknown unit: '<unit>'` — the unit isn't recognized in any category. Surface the message and ask the user to clarify.
- `Cannot convert between '<a>' (<cat_a>) and '<b>' (<cat_b>)` — the two units belong to different categories. Surface the message; do not attempt to bridge categories.

## Resources

- [references/examples.md](references/examples.md) — sample natural-language inputs mapped to function arguments, the full alias list per category, and example error outputs.
- [scripts/convert.py](scripts/convert.py) — implementation. Inside `execute_code` the same file is available at `/skills/unit-converter/scripts/convert.py`.
