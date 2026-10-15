---
name: skidl
description: "Design electronic circuits using the SKiDL Python library. Use when the user asks to: (1) create or describe electronic circuits in Python code, (2) generate netlists, PCB layouts, or schematics programmatically, (3) use SKiDL APIs (Part, Net, Bus, Pin, Circuit, SubCircuit), (4) run SPICE simulations with SKiDL/PySpice, (5) search for electronic components in KiCad libraries or online (Octopart, Digi-Key, Mouser, LCSC, SnapEDA), (6) convert KiCad schematics to Python code, (7) generate BOMs or find component pricing/sourcing, or (8) any task involving programmatic EDA/circuit design with Python."
---

# SKiDL — Programmatic Electronic Circuit Design

SKiDL is a Python module for describing electronic circuits using code instead of schematic editors. It outputs netlists for PCB layout tools (primarily KiCad) and supports SPICE simulation via PySpice/InSpice.

Install: `pip install skidl`

Set KiCad symbol path:
- Linux/Mac: `export KICAD_SYMBOL_DIR="/usr/share/kicad/symbols"`
- Windows: `set KICAD_SYMBOL_DIR=C:\Program Files\KiCad\share\kicad\kicad-symbols`

## Quick Start

```python
from skidl import *

vin, vout, gnd_net = Net('VI'), Net('VO'), Net('GND')
r1, r2 = 2 * Part("Device", 'R', dest=TEMPLATE)
r1.value, r2.value = '1K', '500'

vin & r1 & vout & r2 & gnd_net

ERC()
generate_netlist(tool=KICAD8)
```

## Core Objects

| Object | Purpose | Creation |
|--------|---------|----------|
| `Part` | Electronic component | `Part('Device', 'R', value='1K')` |
| `Pin` | Component terminal | Accessed via `part[1]`, `part['VCC']` |
| `Net` | Electrical connection | `Net('GND')` |
| `Bus` | Collection of nets | `Bus('DATA', 8)` |
| `Circuit` | Container for all elements | `Circuit()` |

## Connections

The `+=` operator connects pins to nets:

```python
net += part[1]
net += part['VCC']
part[1] += part[2]            # Implicit net created
part['GP2 GP1 GP0'] += b[2:0] # Bus connection
```

### Network Operators (series/parallel)

```python
vcc & r1 & r2 & gnd                    # Series
vcc & (r1 | r2) & gnd                  # Parallel
vcc & r1 & d1['A,K'] & gnd             # Explicit pin order
inp & tee(c & gnd) & l & tee(c2 & gnd) & outp  # Tee junctions
```

## Finding Parts

SKiDL searches **local KiCad libraries only**. For online component search, sourcing, and downloading missing parts, see [component_search.md](references/component_search.md).

```bash
$ skidl-part-search opamp           # Command line
$ skidl-part-search --interactive   # Interactive mode
```

```python
search('opamp')                     # In code (regex across names/descriptions/keywords)
search('opamp dual')                # AND logic
search('lm358 | tl072')            # OR logic
search_footprints('QFP')
show(Part('Amplifier_Operational', 'LM358'))  # Display part details
```

## Instantiating & Copying Parts

```python
r = Part('Device', 'R', value='1K')
rt = Part('Device', 'R', dest=TEMPLATE)     # Template (not in netlist)
r2 = rt.copy(value='2K')                    # Copy with override
r3 = rt(value='2K')                         # Shorthand copy
r4, r5, r6 = rt(3, value='1K')              # Multiple copies
r7, r8 = 2 * rt                             # Multiplication
r9, r10, r11 = rt(value=['1K','2K','3K'])   # Different values
```

## Pin Access

```python
part[3]              # By number
part[3, 1, 6]        # Multiple
part[2:4]            # Slice
part['VDD']          # By name
part['GP0 GP1 GP2']  # Space-separated names
part['DQ[0:2]']      # Index range
part['.*/AN1/.*']    # Regex (set part.match_pin_regex = True)
```

## ERC & Output

```python
ERC()                                # Electrical Rules Check
generate_netlist()                   # KiCad netlist
generate_netlist(tool=KICAD8)        # Specify KiCad version
generate_pcb()                       # PCB file
generate_schematic()                 # KiCad schematic
generate_svg()                       # SVG (requires netlistsvg)
generate_dot()                       # Graphviz DOT
generate_xml()                       # XML

# Suppress ERC on specific elements
my_net.do_erc = False
my_part[5].do_erc = False
part[:] += NC                        # No-connect all pins
```

## Hierarchy (SubCircuits)

### Decorator Pattern (preferred)

```python
@SubCircuit
def regulator():
    reg = Part('Regulator_Linear', 'AMS1117-3.3')
    c_in = Part('Device', 'C', value='100nF')
    c_out = Part('Device', 'C', value='10uF')
    reg['VI'] & c_in & reg['GND']
    reg['VO'] & c_out & reg['GND']
    return Interface(vin=reg['VI'], vout=reg['VO'], gnd=reg['GND'])

vreg = regulator()
power_12v += vreg.vin
```

### Context Manager Pattern

```python
with SubCircuit('power_section'):
    reg = Part('Regulator_Linear', 'AMS1117-3.3')
    # ...
```

## Buses

```python
data = Bus('DATA', 8)            # 8-bit bus
addr = Bus('ADDR', 16)
combo = Bus('MIX', 4, a_net, existing_bus)  # Composite

data[0]       # Single line
data[3:0]     # Slice
data[-1]      # Last line
```

## Units (Multi-Unit Parts)

```python
rn = Part("Device", 'R_Pack02')
rn.make_unit('A', 1, 4)
rn.make_unit('B', 2, 3)
rn.A[1, 4] += Net(), Net()
```

## Part/Net Classes

```python
passive = PartClass("passive", priority=1, tolerance="5%")
high_speed = NetClass("high_speed", priority=2, width="0.1mm")
r = Part("Device", "R", value="1K", partclasses=(passive,))
clk = Net("CLK", netclasses=(high_speed,))
```

## Libraries

```python
set_default_tool(KICAD)
lib_search_paths[KICAD].append('/path/to/libs')
lib_search_paths[KICAD].append('https://gitlab.com/...')  # Remote

# Direct file
r = Part('/path/to/my_lib.kicad_sym', 'R')

# Create/export libraries
my_lib = SchLib(name='my_lib')
my_lib += Part('Device', 'R', dest=TEMPLATE)
my_lib.export('my_skidl_lib')
```

## Ad-Hoc Parts

```python
p = Part(name='MY_PART', tool=SKIDL, dest=TEMPLATE, ref_prefix='U')
p += Pin(num=1, name='IN', func=Pin.funcs.INPUT)
p += Pin(num=2, name='OUT', func=Pin.funcs.OUTPUT)
p += Pin(num=3, name='GND', func=Pin.funcs.PWRIN)
my_instance = p()
```

## Multiple Circuits

```python
ckt = Circuit()
with ckt:
    r = Part('Device', 'R', value='1K')
    n = Net('GND')
ckt.ERC()
ckt.generate_netlist()
```

## SPICE Simulations

For SPICE simulation, read [spice_guide.md](references/spice_guide.md). Quick overview:

```python
from skidl.pyspice import *

r1 = R(ref='R1', value=1 @ u_kOhm)
v1 = V(ref='V1', dc_value=5 @ u_V)
v1['p'] & r1[1]
r1[2] & gnd
v1['n'] & gnd

circ = generate_netlist()
sim = circ.simulator()
analysis = sim.operating_point()
```

## References

- **Full API**: See [api_reference.md](references/api_reference.md) for all classes, methods, properties, and enums
- **SPICE guide**: See [spice_guide.md](references/spice_guide.md) for simulation setup, available parts, and examples
- **Examples**: See [examples.md](references/examples.md) for complete working circuits (LED, op-amp, 555 timer, bus interfaces, hierarchy, parametric designs)
- **Component search & sourcing**: See [component_search.md](references/component_search.md) for online part search, distributor APIs (Octopart, Digi-Key, Mouser), symbol/footprint downloads (SnapEDA, Ultra Librarian), LCSC/JLCPCB workflow, and BOM pricing
