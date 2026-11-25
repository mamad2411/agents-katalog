---
name: datasheet-to-symbol-lib
description: >
  Use whenever the user wants to turn a component datasheet PDF into KiCad
  symbols — e.g. "create a KiCad symbol library from this datasheet," or any
  mention of generating KiCad symbols, footprints, or .kicad_sym files from an
  IC/component datasheet. Also trigger for follow-on work on the same
  library: adding a part number, fixing a pinout, splitting package variants,
  or rebuilding after a correction. Extracts every part and pinout from the
  PDF into a verified JPD (JSON Part Description) file, then builds the
  .kicad_sym file with the kipart MCP server's jpd2spd, spd2csv, and kipart
  tools. Always use this for datasheets with multiple package variants,
  multi-unit parts (gate arrays, opamp channels), high pin-count packages
  (QFP/BGA), or alternate/muxed pin functions — these are exactly the cases
  this skill is built to get right where ad-hoc transcription goes wrong.
---

# Datasheet PDF to KiCad symbol library

    datasheet.pdf → (you write) parts.jpd → jpd2spd → spd2csv → kipart → parts.kicad_sym

The three conversions are tools on the **kipart MCP server**. The JPD file is the
only artifact you author; everything downstream is generated. A wrong pin raises
no error anywhere in the pipeline — it just produces a plausible-looking wrong
symbol — so accuracy comes from landing the extraction in JSON and checking it
mechanically, not from re-reading your own transcription.

Work through the six steps below in order. Read the server's
**`kipart://docs/jpd`** resource for the JPD schema, and
`references/jpd_for_datasheets.md` for how this skill uses it, before writing
any JPD.

If the kipart MCP server isn't available, stop and say so — the build has no
other path. (Its tools may appear under a client-specific prefix; `jpd2spd`
below means whatever this client calls that tool.)

## 1. Identify every part

Search the datasheet for part numbers, best sources first: **ordering
information table**, **package marking diagrams**, **device naming/options
section**, page headers.

- Separate part: different package with a different pin arrangement
  (SOIC-14 vs PDIP-14), or a functionally different device in the same
  datasheet (LM358 vs LM393).
- Not a separate part: temperature/grade variants sharing one pinout. They
  become `properties` on one part.

Produce a checklist of `(part name, package, pin count)`. It feeds each JPD
part's `package` and `expected_pin_count` fields and is what step 5 checks
against.

## 2. Extract pinouts into the JPD

Cross-reference all three sources — never one alone:

| Source | Authoritative for |
|---|---|
| Pin function table | names, numbers, types, descriptions |
| Pinout/package diagram | side placement; catching table errors |
| Functional block diagram | signal direction when the type column is vague |

Read the datasheet pages directly as images — your PDF vision is the primary
extraction path, including for pinout diagrams and scanned tables. Reach for
`pdfplumber` only when a pin table is long and machine-readable enough that
text extraction is faster and less error-prone than reading pages; then still
check the rendered page against what it returned. Multi-page tables: scan
every page and carry the column headers across page breaks.

Table reading rules:

- **Footnote markers** — strip `(1)`, `[a]`, `*`, `†` from names, and read the
  footnote text: it sometimes changes a pin's type or adds a real function.
- **Split pin-number columns** (one column per package) — each column is its
  own part object.
- **`-` or blank pin number** — that function doesn't exist on that variant.
  Omit it; never invent a number.
- **One name across several pins** (a `GND` row spanning 4 rows, or `7, 14,
  21`) — one pin object with all numbers in `numbers` and no `increment`:
  `{"name": "gnd", "numbers": ["7","14","21"], "type": "power_in"}`.
- **A numbered bus** (`a0..a7`) — one object, first name, all numbers,
  `"increment": true`.

Shape (see `kipart://docs/jpd` for the full schema; a pin's side is the array
it sits in, and types/styles are spelled in full):

```json
{ "format": "jpd", "version": 1,
  "parts": [
    { "name": "74hc00", "package": "SOIC-14", "expected_pin_count": 14,
      "properties": { "Footprint": "soic-14" },
      "units": [
        { "name": "LOGIC",
          "left":  [ { "name": "a1", "numbers": ["1"], "type": "input" } ],
          "right": [ { "name": "y1", "numbers": ["3"], "type": "output" } ] },
        { "name": "PWR",
          "top":    [ { "name": "vcc", "numbers": ["14"], "type": "power_in" } ],
          "bottom": [ { "name": "gnd", "numbers": ["7"],  "type": "power_in" } ]
        }
      ] } ] }
```

`package` and `expected_pin_count` exist only for verification; `jpd2spd`
ignores them.

## 3. Capture alternate functions

Alternate/muxed functions are part of the pin's real behavior — do not drop
them. Look for slash notation in names (`MISO/SDI/SDO`), an alternate-function
column or cross-referenced table, the same pin number under two names in
different tables, or mode-dependent prose ("when MODE=1, pin 12 is SDO").

The main function is the pin object; every other function is an entry in its
`alternates` array, with the parent's `type`/`style` unless the datasheet says
otherwise. The number appears once, on the parent:

```json
{ "name": "gpio12", "numbers": ["12"], "type": "bidirectional",
  "alternates": [ { "name": "miso", "type": "input" },
                  { "name": "sdo",  "type": "output" } ] }
```

Alternates cost nothing in symbol size — all functions of a pin share one slot.

## 4. Place the pins

- **Physical** (default whenever a pinout diagram exists): match the package
  layout so the symbol matches the reader's mental model of the part. No
  spacers — diagram spacing carries no meaning.
- **Logical** (no diagram, or user asks): inputs left, outputs right, power
  top, ground bottom, bidirectional/unspecified either side; group by function
  and separate groups with `{"spacer": N}`.

No diagram available, by package: DIP — pin 1 top-left, down the left side,
then up the right. Quad — from the top-left corner, down the left, across the
bottom, up the right, across the top. BGA — logical arrangement only; the ball
grid is not a side assignment.

## 5. Verify the JPD

```bash
python <skill dir>/scripts/verify_jpd.py parts.jpd
```

Checks pin counts against `expected_pin_count`, duplicate pin numbers,
increment-collided names, KiCad type/style validity, empty units, supply pins
not typed as power, footnote/whitespace residue in names, and duplicate part
names. It needs nothing but Python — no kipart install. Fix every error and
read every warning before building. Whether the file is structurally a valid
JPD is `jpd2spd`'s call, and step 6 makes it.

The script cannot see the datasheet, so after it reports clean, do the one
check it can't: compare the pin function table against the pinout diagram
pin-by-pin for each part, and resolve any discrepancy by re-reading the
datasheet rather than picking a source. Confirm every part on the step 1
checklist has a part object.

## 6. Build

Three MCP tool calls, chained by file path so the intermediates stay out of the
conversation:

1. `jpd2spd` — `input_path: "parts.jpd"`, `output_path: "parts.spd"`,
   `overwrite: true`
2. `spd2csv` — `input_path: "parts.spd"`, `output_path: "parts.csv"`,
   `overwrite: true`
3. `kipart` — `input_path: "parts.csv"`, `output_path: "parts.kicad_sym"`,
   `overwrite: true`

A tool that fails reports it in the result's `messages`, or raises — read both.
Every tool also returns its output as `content` even when writing a file, so
step 3 hands back the whole library; don't re-read the file afterwards.

Confirm the library holds one symbol per part object and spot-check pin counts
on the largest parts. Then delete `parts.spd` and `parts.csv` unless the user
wants them.

The SPD, CSV, and `.kicad_sym` are build products: never hand-edit them. Fix
`parts.jpd` and re-run. Keep the JPD in version control — it is the record of
what the datasheet said.

### Checking against an existing library

If a symbol for the part already exists somewhere — a KiCad standard library, a
house library, an earlier build — the server's `cmpparts` tool will diff the two
part-for-part. Pass both libraries and `ignore: ["geometry"]` so only what the
parts *are* is compared, not how they happen to be drawn. Every difference is a
question for the datasheet, and the existing symbol is as likely to be the wrong
one; don't change the JPD to match it without checking.

## High pin-count parts (QFP-100+, BGA, MCUs)

- Split into units by function (`PORTA`, `PORTB`, `PWR`, `JTAG`) rather than
  one unit with 100+ pins.
- Extract and verify one unit at a time — a missing pin is far easier to spot
  in a 16-pin port than in a 144-pin flat list.
- For BGAs, the pin function table is the source of pin identity, not the ball
  map.
- With several independent parts in one datasheet, extracting each into its own
  JPD in parallel is fine — but only if each subagent gets the PDF and the
  same rules; merge the `parts` arrays afterward and verify the merged file.

## Failure modes

| Symptom | Cause |
|---|---|
| `jpd2spd` errors or emits no part | malformed JSON, or a missing `name`/`units`/`numbers`; `numbers` given as a bare string instead of an array |
| Wrong pin count in the symbol | a JPD problem — re-run step 5, don't debug the SPD or CSV |
| Unexpected auto-incremented names | `increment: true` on a shared name (power/ground) — drop it; a bus without it repeats one name — add it |
| Missing symbol for a part | duplicate part `name`, or a unit whose sides are all empty |
| Odd characters in pin names | curly quotes / non-breaking spaces carried out of the PDF — clean them in the JPD |
| A tool refuses to write its output | the file exists and `overwrite` wasn't set |

## Gotchas

- Pin names take no whitespace — use underscores.
- Don't hide pins (`"hidden": true`) unless asked.
- Pinout diagrams are drawn for physical clarity, not numeric order — confirm
  every number against the pin function table.
