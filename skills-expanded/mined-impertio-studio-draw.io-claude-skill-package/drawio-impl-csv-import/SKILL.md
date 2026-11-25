---
name: drawio-impl-csv-import
description: >
  Use when generating Draw.io diagrams from tabular/CSV data or creating data-driven
  diagrams. Prevents the common mistake of missing directive lines or wrong connection
  JSON format. Covers all CSV directives (label, style, connect, layout, identity),
  column references, conditional styling, and auto-layout options.
  Keywords: CSV import, csv-to-diagram, data-driven diagram, # label, # style,
  # connect, tabular data, diagram from spreadsheet, import data,
  generate diagram from CSV, auto-generate diagram.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io CSV Import Implementation

## Purpose

This skill enables correct generation of Draw.io diagrams from CSV (tabular) data. It covers the complete CSV import format: directive lines that configure shape rendering, connection routing, conditional styling, and automatic layout. The CSV import feature converts rows into shapes and column references into connections, labels, and styles.

## Critical Rules (Memorize These)

1. **ALWAYS place ALL directive lines BEFORE the CSV header row** — Directives start with `#`. Data rows NEVER start with `#`.
2. **ALWAYS include a `# label:` directive** — Without it, shapes render with no visible text.
3. **ALWAYS use valid JSON in `# connect:` directives** — The value MUST be a JSON object with `"from"` and `"to"` keys as strings. NEVER use bare words or single quotes.
4. **ALWAYS wrap column references in `%` delimiters** — Use `%columnName%` in labels, styles, and connect directives. NEVER use `{columnName}` or `$columnName`.
5. **ALWAYS include a CSV header row** — The first non-directive, non-comment line MUST contain column names that match all `%placeholder%` references.
6. **NEVER put data values in directive lines** — Directives define templates; data comes from CSV rows only.
7. **ALWAYS use `# identity:` when connection targets reference a column other than the first** — Without it, Draw.io matches against the first column by default.
8. **ALWAYS use `# ignore:` for utility columns** — Columns used only for styling, connections, or IDs MUST be listed in ignore to prevent them from appearing as shape metadata.

## CSV Format Structure

The CSV import format consists of three sections in strict order:

```
1. Comment lines        (## prefix — ignored by parser)
2. Directive lines      (# prefix — configure rendering)
3. CSV header row       (column names, comma-separated)
4. CSV data rows        (values, comma-separated — one shape per row)
```

## Directive Reference

### Label Directive

Defines the text displayed inside each shape. Supports HTML and column placeholders.

```
# label: %name%
# label: %name%<br><i style="color:gray;">%role%</i>
# label: <b>%title%</b><br>%description%
```

### Style Directive

Sets the mxGraph style string applied to ALL shapes. Supports column placeholders for dynamic values.

```
# style: rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
# style: shape=ellipse;whiteSpace=wrap;html=1;fillColor=%fill%;strokeColor=%stroke%;
```

### Conditional Style Directives

Use `stylename` + `styles` together to apply different styles based on a column value.

```
# stylename: type
# styles: {"server": "shape=image;image=server.png;", \
#   "database": "shape=cylinder3;whiteSpace=wrap;html=1;", \
#   "client": "rounded=1;whiteSpace=wrap;html=1;"}
```

Rules:
- `stylename` names the column whose values act as style keys.
- `styles` is a JSON object mapping column values to mxGraph style strings.
- Every distinct value in the `stylename` column MUST have a corresponding key in `styles`.
- NEVER mix `style` and `stylename`/`styles` — use one approach or the other.

### Identity Directive

Designates which column provides unique identifiers for connection matching.

```
# identity: id
```

- If omitted, the first column is used as the identity.
- Connection targets (`"to"`) match against the identity column values.

### Namespace Directive

Adds a prefix to all generated cell IDs to prevent collisions when importing multiple CSVs.

```
# namespace: orgchart-
```

### Connect Directive

Defines connections (edges) between shapes. MUST be valid JSON.

```
# connect: {"from": "manager", "to": "name", "invert": true, "label": "reports to", \
#   "style": "curved=1;endArrow=blockThin;endFill=1;fontSize=11;"}
```

JSON properties:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `from` | string | YES | Column name in the current row containing the target reference |
| `to` | string | YES | Column name in the target row to match against (matched via identity) |
| `invert` | boolean | NO | If `true`, reverses arrow direction (arrow points from target to source) |
| `label` | string | NO | Text label displayed on the edge |
| `style` | string | NO | mxGraph style string for the edge |

Multiple connections require separate `# connect:` lines:

```
# connect: {"from": "manager", "to": "name", "invert": true}
# connect: {"from": "refs", "to": "id", "style": "dashed=1;"}
```

### Layout Directive

Specifies the automatic layout algorithm applied after import.

```
# layout: auto
# layout: verticalTree
# layout: horizontalTree
# layout: organic
# layout: circle
```

| Layout | Best For |
|--------|----------|
| `auto` | General purpose (Draw.io picks the best algorithm) |
| `verticalTree` | Org charts, hierarchies (top-to-bottom) |
| `horizontalTree` | Left-to-right hierarchies |
| `organic` | Network topologies, unstructured graphs |
| `circle` | Peer relationships, ring topologies |

### Dimension Directives

Control shape sizing:

```
# width: auto
# width: 120
# height: auto
# height: 60
```

- `auto` sizes shapes to fit their label content.
- Numeric values set fixed pixel dimensions for ALL shapes.

### Spacing Directives

Control distance between elements in the auto-layout:

```
# padding: -12
# nodespacing: 40
# levelspacing: 100
# edgespacing: 40
```

| Directive | Purpose | Default |
|-----------|---------|---------|
| `padding` | Internal label padding (negative reduces it) | 0 |
| `nodespacing` | Horizontal distance between sibling nodes | 40 |
| `levelspacing` | Vertical distance between hierarchy levels | 100 |
| `edgespacing` | Distance between parallel edges | 40 |

### Ignore Directive

Lists columns to exclude from shape metadata/tooltips. Utility columns (IDs, color codes, connection targets) MUST be ignored.

```
# ignore: id,fill,stroke,manager,refs,image
```

### Link Directive

Designates a column whose values become hyperlinks on the shapes.

```
# link: url
```

### Parent Style Directive

Sets the style for automatically created parent/container shapes (used when the layout groups nodes).

```
# parentstyle: swimlane;whiteSpace=wrap;html=1;childLayout=stackLayout;horizontal=1;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;
```

## Line Continuation

Long directive lines can be split using backslash `\` at the end of a line. The next line MUST start with `#`:

```
# connect: {"from": "manager", "to": "name", "invert": true, \
#   "label": "manages", "style": "curved=1;endArrow=blockThin;endFill=1;"}
```

## Column Reference Syntax

Wrap column names in `%` delimiters to insert row values:

```
%columnName%
```

Column references work in:
- `# label:` — inserts values into shape labels
- `# style:` — inserts values into style strings (e.g., `fillColor=%fill%`)
- `# connect:` — column names in `from`/`to` reference column headers

## Import Method

Menu path: **Arrange > Insert > Advanced > CSV**

A dialog accepts the combined directive + CSV text. Import generates the diagram on the canvas immediately.

## Complete Example: Org Chart

```csv
## Organizational chart with hierarchy
# label: %name%<br><i style="color:gray;">%position%</i>
# style: label;whiteSpace=wrap;html=1;rounded=1;fillColor=%fill%;strokeColor=%stroke%;
# namespace: org-
# identity: name
# connect: {"from": "manager", "to": "name", "invert": true, \
#   "style": "curved=1;endArrow=blockThin;endFill=1;fontSize=11;"}
# width: auto
# height: auto
# padding: -12
# ignore: fill,stroke,manager
# layout: verticalTree
# nodespacing: 40
# levelspacing: 100
#
name,position,manager,fill,stroke
Alice Johnson,CEO,,#dae8fc,#6c8ebf
Bob Smith,CTO,Alice Johnson,#d5e8d4,#82b366
Carol White,CFO,Alice Johnson,#d5e8d4,#82b366
Dave Brown,Lead Dev,Bob Smith,#fff2cc,#d6b656
Eve Davis,DevOps,Bob Smith,#fff2cc,#d6b656
Frank Lee,Accountant,Carol White,#fff2cc,#d6b656
```

## Complete Example: Flowchart with Conditional Styles

```csv
## Process flow with different shape types
# label: %name%
# stylename: type
# styles: {"decision": "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;", \
#   "process": "rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;", \
#   "terminal": "ellipse;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;"}
# connect: {"from": "next", "to": "id", "style": "endArrow=classic;html=1;"}
# identity: id
# namespace: flow-
# width: 120
# height: 60
# layout: auto
# ignore: id,next,type
#
id,name,type,next
start,Start,terminal,step1
step1,Process Data,process,check
check,Valid?,decision,step2
step2,Save Result,process,end
end,End,terminal,
```

## Complete Example: Network Topology

```csv
## Network diagram with device types
# label: %hostname%<br><small>%ip%</small>
# stylename: device
# styles: {"router": "shape=mxgraph.cisco.routers.router;whiteSpace=wrap;html=1;", \
#   "switch": "shape=mxgraph.cisco.switches.workgroup_switch;whiteSpace=wrap;html=1;", \
#   "server": "shape=mxgraph.cisco.servers.standard_server;whiteSpace=wrap;html=1;", \
#   "firewall": "shape=mxgraph.cisco.firewalls.firewall;whiteSpace=wrap;html=1;"}
# connect: {"from": "uplink", "to": "hostname", "style": "endArrow=none;strokeWidth=2;"}
# identity: hostname
# namespace: net-
# width: 80
# height: 80
# layout: organic
# ignore: ip,device,uplink
#
hostname,ip,device,uplink
core-rtr,10.0.0.1,router,
fw-01,10.0.0.2,firewall,core-rtr
sw-floor1,10.0.1.1,switch,fw-01
sw-floor2,10.0.2.1,switch,fw-01
srv-web,10.0.1.10,server,sw-floor1
srv-db,10.0.1.11,server,sw-floor1
srv-mail,10.0.2.10,server,sw-floor2
```

## Checklist: Before Outputting CSV Import Data

1. ALL directive lines appear before the CSV header row.
2. A `# label:` directive exists and references valid column names.
3. ALL `# connect:` values are valid JSON with double-quoted keys.
4. ALL `%placeholder%` names exactly match CSV column headers (case-sensitive).
5. A CSV header row exists as the first non-directive line.
6. Every data row has the same number of fields as the header.
7. Utility columns are listed in `# ignore:`.
8. `# identity:` is set if connections target a column other than the first.
9. `# namespace:` is set when multiple CSV imports coexist in one diagram.
10. `# layout:` is set to an appropriate algorithm for the data structure.

## Cross-References

- **XML fundamentals:** See `drawio-core-xml-format` for mxGraph file structure.
- **Style syntax:** See `drawio-syntax-styles` for the complete style property reference.
- **Connection details:** See `drawio-syntax-connections` for edge routing and style options.
- **Flowcharts:** See `drawio-impl-flowcharts` for flowchart-specific shapes and patterns.

## Reference Links

- [Complete Reference](references/methods.md)
- [Working Examples](references/examples.md)
- [Anti-Patterns](references/anti-patterns.md)
