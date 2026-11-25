---
name: circuit-diagram
description: >
  Generate reasonably laid-out circuit diagrams from natural language descriptions
  or SPICE netlist texts using the SchemDraw Python library. Use when the user asks
  to draw, render, or generate circuit schematics, electrical diagrams, logic circuits,
  timing diagrams, flowcharts, or when given SPICE netlists to visualize. Outputs
  SVG, PNG, or other formats.
---

# Circuit Diagram

Generate publication-quality circuit schematics from natural language or SPICE netlists using [SchemDraw](https://schemdraw.readthedocs.io/), a Python library for electrical circuit drawing. Supports basic components, opamps, transistors, logic gates, timing diagrams, and flowcharts.

## Installation

```bash
pip install schemdraw
```

Optional but recommended:

```bash
pip install matplotlib    # for PNG/PDF output and Matplotlib backend
pip install ziamath latex2mathml  # for full LaTeX math in SVG backend
pip install pyparsing     # for logic expression parsing
```

## Quick Start

```python
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(file='circuit.svg') as d:
    elm.Resistor().right().label('1kΩ')
    elm.Capacitor().down().label('10μF', loc='bottom')
    elm.Line().left()
    elm.SourceV().up().label('5V')
```

This draws: source-up → resistor-right → capacitor-down → line-left (closing the loop).

## Workflow Decision Tree

When a user requests a circuit diagram, follow this decision tree:

```
User asks for circuit diagram
├─ Natural language description → Parse components & topology → Plan & build SchemDraw code
├─ SPICE netlist text            → Parse netlist → Extract topology → Plan & build SchemDraw code
├─ Logic/Boolean expression      → Use logicparse() or logic gates
├─ Timing diagram                → Use timing diagram elements
└─ Flowchart                     → Use flowchart elements

**Do NOT render/plot the SVG during thinking or planning.**
Only at the very final step, after the code is complete and presented,
ask the user: "Shall I render and save the SVG?"
```

### Natural Language → Schematic

1. **Identify components** — resistors, capacitors, inductors, sources, diodes, transistors, opamps, grounds, etc.
2. **Extract topology** — series connections ("followed by", "connected to"), parallel branches, node labels, values.
3. **Plan layout** — typically left-to-right, top-to-bottom. Use anchors and `.push()`/`.pop()` for branches.
4. **Generate SchemDraw code** — write a Python script that draws the circuit (do NOT execute yet).
5. **Present code to user** — show the planned script and ask whether to render the SVG.

### SPICE Netlist → Schematic

1. **Parse the netlist** — extract component lines (R, C, L, D, Q, M, V, I, X) and their nodes/values.
2. **Infer topology** — build a graph from node connections.
3. **Assign positions** — lay out nodes and place components between them.
4. **Generate SchemDraw code** — place each element between its nodes (do NOT execute yet).
5. **Present code to user** — show the planned script and ask whether to render the SVG.

Use `scripts/spice_parser.py` to parse standard SPICE netlists into JSON for easier consumption.

## Element Reference

SchemDraw provides extensive built-in elements. See `references/element-catalog.md` for the complete categorized reference with code snippets. Quick reference below:

### Two-Terminal Elements (`elm.*`)

| Element | Notes |
|---------|-------|
| `Resistor` | Also `ResistorIEC`, `ResistorVar`, `RBox` (US/box style) |
| `Capacitor` | Also `CapacitorVar`, `CapacitorPolar` |
| `Inductor` | Also `Inductor2` |
| `Diode` | Also `Zener`, `Schottky`, `LED`, `Tunnel`, `Varactor` |
| `SourceV`, `SourceI` | Voltage/current sources |
| `SourceSin`, `SourcePulse`, `SourceSquare`, `SourceTriangle` | Waveform sources |
| `Battery`, `BatteryCell` | Battery symbols |
| `Ground`, `GroundSignal`, `GroundChassis` | Ground symbols |
| `Line`, `Dot`, `Wire` | Connecting elements |
| `Gap` | Open-circuit gap (for voltage labels) |
| `Switch`, `SwitchSpdt`, `SwitchDpst`, `SwitchDpdt` | Switches |
| `Potentiometer` | Variable resistor/pot |
| `Fuse` | Fuse symbol |
| `Lamp` | Lamp/light bulb |
| `MeterV`, `MeterA` | Voltmeter, ammeter |
| `Speaker`, `Mic` | Audio elements |

### Transistors (`elm.*`)

| Element | Notes |
|---------|-------|
| `BjtNpn`, `BjtPnp` | BJT transistors |
| `JfetN`, `JfetP` | JFET transistors |
| `AnalogNFet`, `AnalogPFet` | MOSFETs (analog style, 3-pin) |
| `NFet`, `PFet` | MOSFETs (digital style, 4-pin) |

### Opamps & Amplifiers (`elm.*`)

| Element | Notes |
|---------|-------|
| `Opamp` | Standard opamp with +/− inputs |
| `Integrator`, `Differentiator` | Opamp configs |
| `Comparator` | Comparator symbol |

### Logic Gates (`from schemdraw import logic`)

| Element | Notes |
|---------|-------|
| `And`, `Nand`, `Or`, `Nor`, `Xor`, `Xnor` | Basic gates |
| `Not`, `Buf`, `NotNot` | Buffer/inverter |
| `Schmitt`, `SchmittNot`, `SchmittAnd`, `SchmittNand` | Schmitt triggers |

### Connectors & Labels

| Element | Notes |
|---------|-------|
| `CurrentLabel`, `CurrentLabelInline` | Current arrows |
| `VoltageLabelArc` | Arc voltage label |
| `LoopCurrent` | Loop current arrow |
| `Annotate` | Curved annotation arrow |
| `Encircle`, `EncircleBox` | Group/encircle elements |
| `ZLabel` | Impedance arrow label |

## Layout & Positioning

Elements chain directionally. Each new element starts where the previous one ended.

### Direction Methods

```python
elm.Resistor().right()   # → (default)
elm.Resistor().down()    # ↓
elm.Resistor().left()    # ←
elm.Resistor().up()      # ↑
```

### Absolute Positioning

```python
elm.Resistor().at((3, 2))          # place at absolute coordinate
elm.Capacitor().at(R1.end)         # place at an element's anchor
elm.Inductor().at(R1.start).down() # start at R1's left terminal, go down
```

### Anchors

Every element defines named anchors: `start`, `end`, `center`, `top`, `bottom`, `N`, `S`, `E`, `W`, `NE`, `NW`, `SE`, `SW`. Transistors have `base`/`gate`, `collector`/`drain`, `emitter`/`source`. Opamps have `in1`, `in2`, `out`, `vdd`, `vss`.

```python
elm.Line().at(R1.N).up()    # draw line up from resistor's north anchor
elm.Dot().at(R1.end)        # place a connection dot at the end
```

### Push/Pop for Branches

Save and restore positions for parallel branches:

```python
with schemdraw.Drawing():
    d.push()                          # save position
    elm.Resistor().right().label('R1')
    elm.Capacitor().down().label('C1')
    d.pop()                           # restore position
    elm.Capacitor().down().label('C2')  # parallel branch
```

### Rotating & Flipping

```python
elm.Resistor().theta(45)    # rotate 45 degrees
elm.Resistor().flip()       # mirror horizontally
elm.Resistor().reverse()    # reverse direction (swap start/end)
```

## Labels & Annotations

### Basic Labels

```python
elm.Resistor().label('1kΩ')                          # default: top
elm.Capacitor().label('10μF', loc='bottom')           # bottom
elm.Resistor().label('R1', loc='left')                # left
elm.Inductor().label('L', loc='right')                # right
```

### LaTeX Math

Labels support LaTeX math in `$...$`:

```python
elm.Capacitor().label(r'$C = 10\mu F$')
elm.Resistor().label(r'$R_1$')
```

### Voltage Labels

```python
# Spread labels across element
elm.Resistor().label(('–', '$V_R$', '+'))

# Arc-style voltage label
R1 = elm.Resistor()
elm.VoltageLabelArc().at(R1).label('$V_{out}$')
```

### Current Labels

```python
R1 = elm.Resistor()
elm.CurrentLabel().at(R1).label('$I_C$')            # arrow over element
elm.CurrentLabelInline(direction='in').at(R1).label('$i_b$')  # inline arrow
```

### Loop Currents

```python
R1 = elm.Resistor(); C1 = elm.Capacitor().down()
D1 = elm.Diode().left(); L1 = elm.Inductor().up()
elm.LoopCurrent([R1, C1, D1, L1], direction='cw').label('$I_1$')
```

### Annotations & Grouping

```python
elm.Annotate().at(R1.N).delta(dx=1, dy=1).label('feedback')
elm.Encircle([R1, R2], padx=.6).linestyle('--').color('red')
```

## Styling

### Colors & Line Styles

```python
elm.Resistor().color('red')
elm.Resistor().fill('lightblue')         # fill color
elm.Resistor().linestyle('--')           # dashed
elm.Resistor().linestyle(':')            # dotted
elm.Resistor().linewidth(2)              # thicker lines
```

### Font Styling

```python
elm.Resistor().label('R1', fontsize=14, font='sans-serif')
```

### Global Style

```python
schemdraw.style(elm.STYLE_IEC)    # IEC-style resistors
schemdraw.style(elm.STYLE_USA)    # US-style resistors (default)
```

## Saving Output

### SVG (recommended — fast, no extra deps)

```python
with schemdraw.Drawing(file='circuit.svg') as d:
    elm.Resistor().right().label('1kΩ')

# Or: schemdraw.use('svg') for all subsequent drawings
```

### PNG / PDF (Matplotlib backend)

```python
with schemdraw.Drawing(file='circuit.png') as d:
    elm.Resistor().right().label('1kΩ')
```

### Inline Display (Jupyter)

```python
with schemdraw.Drawing() as d:
    elm.Resistor().right().label('1kΩ')
    display(d)  # in Jupyter, draws automatically
```

### Saving to a BytesIO buffer

```python
from io import BytesIO
buf = BytesIO()
with schemdraw.Drawing() as d:
    elm.Resistor().right().label('1kΩ')
    d.save(buf, format='svg')
svg_data = buf.getvalue()
```

## Logic Circuits

### From Boolean Expressions

```python
from schemdraw.parsing import logicparse

logicparse('(A and B) or (C and D)', outlabel='$Y$')
logicparse('not ((w and x) or (y and z))', outlabel=r'$\overline{Q}$')
```

Supports operators: `and`, `or`, `nand`, `nor`, `xor`, `xnor`, `not`, plus symbols `&`, `|`, `⊕`, `¬`, `∨`, `∧`.

### Manual Logic Gates

```python
from schemdraw import logic

with schemdraw.Drawing():
    g1 = logic.And().right().label('A')
    g2 = logic.Nand(inputs=3).at(g1.out).right()
    # inputnots for active-low inputs:
    logic.And(inputs=3, inputnots=[1, 3])
```

### Truth Tables & K-Maps

```python
# Truth table
table = '''
 A | B | Y
---|---|---
 0 | 0 | 0
 0 | 1 | 1
 1 | 0 | 1
 1 | 1 | 1
'''
with schemdraw.Drawing(file='truthtable.svg'):
    logic.Table(table, colfmt='cc|c')

# K-Map
logic.Kmap(names='AB', truthtable=[('01', '1')])
```

## SPICE Netlist to Schematic

Use `scripts/spice_parser.py` to convert a SPICE netlist into structured JSON:

```bash
python3 scripts/spice_parser.py input.cir --json components.json
```

The parser extracts:
- Component type, name, connecting nodes, and value
- Top-level subcircuits and models

Then map the parsed JSON to SchemDraw elements:

| SPICE Letter | SchemDraw Element |
|-------------|-------------------|
| R | `elm.Resistor` |
| C | `elm.Capacitor` |
| L | `elm.Inductor` |
| D | `elm.Diode` |
| Q (NPN) | `elm.BjtNpn` |
| Q (PNP) | `elm.BjtPnp` |
| M (NMOS) | `elm.NFet` |
| M (PMOS) | `elm.PFet` |
| V | `elm.SourceV` |
| I | `elm.SourceI` |
| X (subcircuit) | Use manual layout for complex ICs |

### Layout Strategy for SPICE

1. **Identify ground node** (usually node 0) — place `elm.Ground()` there
2. **Trace from sources outward** — voltage/current sources define the driving paths
3. **Branch at nodes** — use `d.push()`/`d.pop()` at nodes with >2 connections
4. **Stack series components** — chain `.right()`, `.down()`, `.left()`, `.up()`

## Timing Diagrams

```python
from schemdraw import timing

with schemdraw.Drawing():
    timing.Clock().label('CLK')
    timing.Signal().down().label('DATA')
```

## Flowcharts

```python
from schemdraw import flowchart as fc

with schemdraw.Drawing():
    fc.Start().label('Start')
    fc.Arrow().down()
    fc.Process().label('Do something')
    fc.Arrow().down()
    fc.Decision().label('Done?')
    fc.Arrow().right().label('No')
    fc.Process().label('Try again')
```

## Schemdraw Backends at a Glance

| Backend | Pros | Cons |
|---------|------|------|
| **SVG** | 4-10× faster, no Matplotlib/NumPy needed, searchable text | Limited to SVG output |
| **Matplotlib** | PNG/PDF/JPG, post-draw customization with Matplotlib API | Heavier deps, slower |

```python
schemdraw.use('svg')       # switch to SVG (recommended for most uses)
schemdraw.use('matplotlib') # switch back to Matplotlib
```

## Best Practices

1. **Always use `with schemdraw.Drawing(...) as d:` context manager** — ensures proper cleanup.
2. **Prefer SVG backend** for speed and lighter dependencies unless you need PNG/PDF.
3. **Use `d.push()`/`d.pop()` for parallel branches** rather than absolute coordinates — it's more maintainable.
4. **Label every component** with value and/or reference designator for readability.
5. **Use `.at()` with element anchors** (not raw coordinates) for precise connections to existing elements.
6. **Keep drawings closed-loop** where possible — SchemDraw doesn't auto-close paths.
7. **Test incrementally** — draw 2-3 elements, verify, then continue building.
8. **For complex circuits**, sketch the node layout on paper first, then translate to SchemDraw.
9. **Use `logicparse()` for Boolean expressions** instead of manually placing logic gates.
10. **Check `references/element-catalog.md`** when unsure about an element name or its anchors.
11. **Revise wire routing with `elm.Wire(shape, k)`** — after placing all components, route connecting wires with explicit shapes to avoid wire-to-wire overlap and wire-to-gate-symbol overlap. Use `shape` for routing direction (e.g. `'-|'`, `'|-'`, `'-|-'`, `'|-|'`) and `k` to control bend radius/corner curvature.

## Resources

### scripts/
- `spice_parser.py` — Parse standard SPICE netlists into JSON for conversion to SchemDraw.

### references/
- `element-catalog.md` — Complete catalog of SchemDraw elements organized by category with usage snippets and anchor diagrams.
