---
name: unit-conversion
description: Convert between length, energy, and temperature units commonly used in nanoscale simulations (nm, angstrom, eV, K, ...) using this server's convert_units tool
metadata:
  category: physical-sciences
---

# Unit Conversion

Nanoscale simulation output rarely arrives in the unit you want to report in
— lattice constants come back in angstrom, binding energies in eV, and
device temperatures in Kelvin. This skill covers converting between the
units this server supports and presenting the result clearly.

## Supported units

See `references/UNITS.md` for the full table of supported units, grouped by
physical quantity (length, energy, temperature). Two units can only be
converted into each other if they belong to the same group.

## How to convert a value

Call the `convert_units` tool with `value`, `from_unit`, and `to_unit`:

```json
{"value": 5.43, "from_unit": "angstrom", "to_unit": "nm"}
```

The tool returns the converted value and echoes both unit symbols. If the
two units are not in the same group (e.g. converting an energy to a length),
the tool returns an error explaining why — check `references/UNITS.md`
first if you are not sure which group a unit belongs to.

## Reporting results

When you report a converted value back to the user:

- Round to a sensible number of significant figures for the source
  precision — don't paste back 15 decimal digits from a floating point
  division.
- State both the original and converted value, e.g. "5.43 Å = 0.543 nm".
- If the user gave a value without units, ask which unit they meant rather
  than guessing.
