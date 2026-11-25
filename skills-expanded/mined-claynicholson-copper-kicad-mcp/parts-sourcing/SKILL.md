---
name: parts-sourcing
description: Choose and lock real, orderable parts for a KiCad design with Copper — search the project's parts providers (LCSC/JLCPCB by default, a local catalogue file, generic KiCad parts, or third-party providers), check stock and price, find alternatives, import symbols/footprints, and make the BOM 100% sourced. Use when the user asks to pick parts, find a part number, reduce assembly cost, replace an unavailable part, or "make the BOM orderable".
---

# Parts sourcing with Copper

Where parts come from is **configuration**. `copper_status` shows the active parts providers (in order) under
`config`; every `parts_*` result says which `provider` answered, and every tool takes `provider=` to ask one directly.

| Provider | What it is |
|---|---|
| `lcsc` (default) | LCSC parts for JLCPCB assembly: offline Basic-parts table, live JLC stock, EasyEDA symbol/footprint/3D import |
| `local` | the user's own catalogue file (CSV/JSON: MPN, value, package, KiCad symbol + footprint, any supplier numbers) — fully offline |
| `kicad` | generic KiCad library parts: value + footprint only, no supplier lock |
| third-party | loaded from a Python entry point or a path in the Copper config |

Goal: every component carries the project's part-number field (shown as `part_field`; `LCSC` with the default
provider) pointing at a part that can be bought or assembled **today** — plus the vendor-neutral `MPN` and
`Manufacturer`, which Copper stamps whenever the provider knows them so the design can be re-sourced elsewhere.

## Workflow

1. **Inventory** — `project_summary` (or `parts_source_bom(write=false)`) lists components without a part number.
2. **Passives in bulk** — `parts_source_bom` matches every unsourced component from its MPN field, then value +
   footprint, across the active providers in one call. Review the `write=false` report first.
3. **ICs and connectors one by one** — `parts_search(query=...)` with the *function* and key parameters
   ("LDO 3.3V 500mA SOT-23-5", "USB-C 16 pin SMD", "ESP32-C3 module"). Then `parts_get(part=...)` for stock,
   price, datasheet and package.
4. **Import** — `parts_import(part=...)` gives the symbol + footprint: KiCad's stock libraries when they fit, else
   the provider's own drawing (the `lcsc` provider converts EasyEDA symbol, footprint and 3D model into the
   project's `copper-lcsc` library and checks pad count against pin count).
5. **Swap in place** — `sch_apply` `set_field` (part number / MPN) or `swap` for parts already placed.
6. **Confirm** — `parts_source_bom(write=false)` again → 0 lines needing a choice.

## The default provider: LCSC parts for JLCPCB assembly

JLCPCB keeps a set of **Basic** parts permanently loaded on its pick-and-place feeders. They have no setup fee.
Each *unique* **Extended** part adds a loading fee (about $3) per order; **Preferred** parts waive it on economic
PCBA. Copper ranks Basic > Preferred > Extended, then by stock, then by price, and `parts_search(basic_only=true)`
restricts to Basic. JLC *assembly* stock and LCSC *retail* stock are different pools: `parts_get` labels both.
`parts_alternatives(target="C…")` finds a Basic substitute for an Extended part.

Common Basic workhorses (verify the current class with parts_search — it changes): 10 kΩ / 5.1 kΩ / 4.7 kΩ / 1 kΩ /
100 kΩ resistors (0402, 0603); 100 nF, 1 µF, 10 µF, 22 pF capacitors; AMS1117-3.3 LDO; 1N4148W, SS34 / SS14 diodes;
0603 LEDs; AO3400 / AO3401 MOSFETs; small-signal NPN/PNP (S8050/S8550, MMBT3904/3906).

## Selection rules that save respins (any provider)

- **Stock**: require stock ≥ 10× your build quantity where the provider reports it.
- **Package first**: confirm the footprint matches the datasheet's recommended land pattern (pitch, exposed pad,
  pin 1). An SOT-23 regulator comes in several pinouts (e.g. XC6206 vs AP2112 vs ME6211 differ). Check pins by
  name, not by position.
- **Capacitor voltage and DC bias**: X7R/X5R ceramics lose capacitance under DC bias. A 10 µF 0402 6.3 V part at
  5 V may give 3 µF. Choose a voltage rating ≥ 2× the rail for bulk caps, or step up a package size.
- **Dielectric**: C0G/NP0 for crystal load caps, filters and timing. X7R for decoupling. Avoid Y5V.
- **Resistor power**: 0402 = 1/16 W, 0603 = 1/10 W. Check current-sense and LED resistors.
- **Connectors**: mechanical fit matters more than price. Keep a connector's footprint from the same source as
  its 3D model.
- **Second source**: for any single-source IC, `parts_alternatives` lists substitutes. Note one in a `Notes` field.

## Never

- Never invent a part number. If search fails, say so and offer alternatives.
- Never leave a placeholder value such as "TBD" in a part-number field. Leave it empty so the fab check catches it.
- Never trust a part's description alone. Open the datasheet URL from `parts_get` for pinout-critical parts.
