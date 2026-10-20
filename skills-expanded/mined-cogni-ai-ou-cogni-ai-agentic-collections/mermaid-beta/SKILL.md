---
name: mermaid-beta
description: >-
  Guide for creating and maintaining experimental Mermaid.js beta diagrams
  (Architecture, Block, Ishikawa, Packet, Radar, Sankey, Treemap, TreeView,
  Venn, XY Chart, ZenUML).
  You MUST load this skill when working with experimental Mermaid.js beta diagrams.
license: MIT
---
# Mermaid Beta Skill

Expert in creating, optimizing, and troubleshooting experimental Mermaid.js beta diagrams.

## WHEN TO USE

- User wants to use experimental beta Mermaid diagram types like Architecture, Flow, Sankey, etc.
- Working with newer versions of Mermaid.js.

## WHEN NOT TO USE

- For standard, fully stable Mermaid diagrams (like simple Flowcharts, Sequence diagrams, or Class
  diagrams) where `mermaid/SKILL.md` is more appropriate.
- In environments or markdown renderers that use outdated Mermaid versions (pre-v11.x) lacking beta support.
- When generating complex, data-heavy visualizations better suited for dedicated charting libraries (e.g., D3.js, Chart.js).

## Common Pitfalls

- **Renderer Incompatibility**: Embedding beta diagrams in platforms (like standard GitHub markdown
  rendering) that haven't updated to the required Mermaid version, resulting in syntax errors.
- **Syntax Volatility**: Relying on beta syntax for permanent, strict documentation without acknowledging
  that beta features may break or change in future updates.
- **Missing Plugin Registration**: Attempting to use external integrations like ZenUML without explicitly
  registering the required plugins in the rendering environment.

## Related Instructions

- **mermaid.instructions.md**: Formatting standards, best
  practices, and anti-patterns for Mermaid.js.

## Diagram Types & Patterns

### Architecture Diagrams

An Architecture diagram is specialized for mapping out topological structures,
infrastructure components, and their network or logical relationships.

- Use `architecture-beta` to initialize the diagram.
- Define logical groupings using `group <alias>(<icon>)[<Label>]`.
- Define individual services using `service <alias>(<icon>)[<Label>]`.
- Nest a service inside a group by appending `in <group_alias>`.
- Connect components by specifying their connection sides (`L`, `R`, `T`, `B`)
  separated by `--` (e.g., `serviceA:R -- L:serviceB`).

Example mapping out a cloud-based serverless architecture:

```mermaid
architecture-beta
    group aws(cloud)[AWS Cloud]

    service gateway(internet)[API Gateway] in aws
    service lambda(server)[Compute Logic] in aws
    service db(database)[Database] in aws
    service storage(disk)[Storage Container] in aws

    gateway:B -- T:lambda
    lambda:R -- L:db
    lambda:L -- R:storage
```

Docs: <https://mermaid.js.org/syntax/architecture.html>

### Block Diagrams

A Block diagram is well-suited for visualizing architectures, systems, or process
flows by arranging blocks in a customizable grid layout.

- Use `block-beta` to initialize the diagram type.
- Define grid columns using `columns <number>` (e.g., `columns 3`).
- Define blocks by using an ID, optionally with text and shape (e.g., `DB(("Database"))`).
- Group blocks within a parent block using `block:<ID>` or `block:<ID>:<width>` and close with `end`.
- Use `space` or `space:<number>` to skip grid columns.
- Connect blocks using arrows (e.g., `A --> B`) and apply styles using the `style` directive.

Example demonstrating a grid-based architecture layout:

```mermaid
block-beta
columns 3
  Client
  space
  Internet

  block:Server:3
    API
    space:2
    Logic
  end

  Database

  Client --> Internet
  Internet --> Server
  Server --> Database
```

Docs: <https://mermaid.js.org/syntax/block.html>

### Ishikawa Diagram (v11.12.3+)

An Ishikawa diagram (also known as a fishbone or cause-and-effect diagram) is used
to represent the causes of a specific event or problem.

- Use `ishikawa-beta` to initialize the diagram type.
- The first line after the declaration represents the main event or problem (the "head").
- Subsequent lines are the major categories of causes.
- Indent lines to create nested "fishbone" sub-causes under their parent categories.

Example mapping out the causes of a website outage:

```mermaid
ishikawa-beta
    Website Outage
    Infrastructure
        Server Crash
        Network Failure
    Code
        Bug in Deployment
        Configuration Error
    External
        DDoS Attack
        Third-party API Down
```

Docs: <https://mermaid.js.org/syntax/ishikawa.html>

### Packet Diagram

A Packet diagram is typically used to visualize network protocols or binary data
structures, showing the bits and bytes that make up headers or payloads.

- Use `packet-beta` to initialize the diagram type.
- Add an optional `title` to describe the structure.
- Define bits mapping using ranges representing bit boundaries (e.g., `0-7`).
- Add descriptive labels for each bit range (e.g., `0-7: "Field Name"`).
- The diagram automatically wraps fields into 32-bit rows by default.

Example using a binary block, such as the PNG magic signature file header:

```mermaid
packet-beta
    title "PNG File Signature (8 bytes)"
    0-7: "0x89 (High Bit Set)"
    8-15: "0x50 ('P')"
    16-23: "0x4E ('N')"
    24-31: "0x47 ('G')"
    32-39: "0x0D (CR)"
    40-47: "0x0A (LF)"
    48-55: "0x1A (EOF)"
    56-63: "0x0A (LF)"
```

Docs: <https://mermaid.js.org/syntax/packet.html>

### Radar Diagram (v11.6.0+)

A Radar diagram (or spider chart) is a graphical method of displaying multivariate data
in the form of a two-dimensional chart of three or more quantitative variables represented
on axes starting from the same central point.

- Use `radar-beta` to initialize the diagram.
- Include an optional `title` to identify what the radar chart represents.
- Specify the variable categories along the perimeter using `axis` and a comma-separated list.
- Provide the numeric datasets for each entity using `curve <label> {values}`.

Example representing a team skill assessment:

```mermaid
radar-beta
    title Skill Assessment
    axis Communication, Technical, Teamwork, Leadership, Time_Management
    curve Alice {8, 9, 7, 6, 8}
    curve Bob {6, 8, 9, 8, 7}
```

Docs: <https://mermaid.js.org/syntax/radar.html>

### Sankey Diagram

A Sankey diagram is a flow diagram in which the width of the bands is proportional
to the flow rate. It is typically used to visualize energy, material, or cost
transfers between processes.

- Use `sankey-beta` to initialize the diagram.
- Define flows using comma-separated values in the format `source, target, value`.
- The `value` specifies the thickness of the connection between nodes.
- Define nodes via their usage; no prior declaration is needed.

Example visualizing energy flows:

```mermaid
sankey-beta
    Renewables, Grid, 50
    Fossil Fuels, Grid, 30
    Nuclear, Grid, 20
    Grid, Commercial, 40
    Grid, Residential, 35
    Grid, Industrial, 25
```

Docs: <https://mermaid.js.org/syntax/sankey.html>

### Treemap Diagram

A Treemap diagram represents hierarchical data as a set of nested rectangles, where
the area of each rectangle is proportional to its value.

- Use `treemap-beta` to initialize the diagram type.
- Define hierarchical structures using consistent indentation. Ensure string labels are enclosed in double quotes.
- Specify values for leaf nodes by appending a colon and a number after the label (`"label": <value>`).
- The diagram will automatically calculate the size of parent nodes based on their children.

Example representing a company's budget breakdown:

```mermaid
treemap-beta
  "Marketing"
    "Social Media": 20000
    "Email Campaigns": 5000
  "R&D"
    "New Features": 40000
    "Maintenance": 15000
  "Operations"
    "Software Licenses": 10000
    "Hardware": 5000
```

Docs: <https://mermaid.js.org/syntax/treemap.html>

### TreeView Diagram (v11.14.0+)

A TreeView diagram is used to represent hierarchical data in the form of a directory-like structure.

- Use `treeView-beta` to initialize the diagram type.
- Define items as strings enclosed in double quotes (e.g., `"folder name"`).
- Establish hierarchy and parent-child relationships purely through line indentation.

Example mapping out a project directory structure:

```mermaid
treeView-beta
    "src"
        "components"
            "Header.tsx"
            "Footer.tsx"
        "utils"
            "helpers.ts"
    "tests"
        "unit"
    "package.json"
    "README.md"
```

Docs: <https://mermaid.js.org/syntax/treeView.html>

### Venn Diagrams (v11.12.3+)

Venn diagrams visually represent the relationships between sets using overlapping circles.

- Use `venn-beta` to initialize the diagram type.
- Define a single set using the `set` keyword (e.g., `set Frontend`).
- Define the overlap of two or more sets using `union` (e.g., `union Frontend,Backend`).
- Custom display labels can be assigned using bracket syntax (e.g., `set Dev["Developers"]`).
- Specify sizes for sets or unions by appending a suffix `:N` (e.g., `set Dev:20`).
- Place additional labels inside a set or union using the `text` keyword on an indented line.

Example representing overlapping capabilities:

```mermaid
venn-beta
    title "DevOps Culture"
    set Dev["Development"]:10
    set Ops["Operations"]:10
    set QA["Quality Assurance"]:8

    union Dev,Ops["Continuous Delivery"]:4
    union Dev,QA["Test Automation"]:3
    union Ops,QA["Environments"]:3
    union Dev,Ops,QA["Cross-Functional"]:2
```

Docs: <https://mermaid.js.org/syntax/venn.html>

### XY Chart

An XY chart is an essential data visualization tool that lets you depict data points
on Cartesian coordinates. It supports visualizing data using line charts and bar charts.

- Use `xychart-beta` to initialize the diagram.
- Define an optional `title` to describe the chart.
- Specify the `x-axis` with specific categories (e.g., `[Jan, Feb]`) or a range.
- Specify the `y-axis` with an optional title and range (e.g., `"Revenue" 0 --> 100`).
- Add data series by using `bar` or `line` followed by an array of values (`[10, 20]`).

Example illustrating monthly sales and targets:

```mermaid
xychart-beta
    title "Monthly Sales and Targets"
    x-axis [Jan, Feb, Mar, Apr, May, Jun]
    y-axis "Revenue (in $)" 0 --> 10000
    bar [5000, 6000, 7500, 8200, 9500, 8800]
    line [4000, 5000, 7000, 8000, 9000, 8500]
```

Docs: <https://mermaid.js.org/syntax/xyChart.html>

### ZenUML

ZenUML is an extension that allows you to write sequence diagrams
using a declarative pseudo-code syntax, focusing on speed and readability.
**Important**: ZenUML is an external integration. It requires importing the `@mermaid-js/mermaid-zenuml` plugin
and registering it with `mermaid.registerExternalDiagrams()` before it can be rendered by viewers.

- Use `zenuml` to initialize the diagram type.
- Add an optional `title` to label the diagram.
- Use `A->B: message` or `A->B: method() { ... }` for synchronous or asynchronous messages.
- Utilize programming constructs like `if (condition)`, `else`, `for`, `while`,
  and `try/catch` to build complex flow logic naturally.
- Use `return` statements to denote explicit responses.

Example of a ZenUML Sequence Diagram:

```mermaid
zenuml
    title Authentication Flow
    Client->Server: authenticate(credentials) {
        if (isValid) {
            Server->Database: fetchUser()
            return token
        } else {
            return error
        }
    }
```

Docs: <https://mermaid.js.org/syntax/zenuml.html>

## Troubleshooting

```mermaid
mindmap
  root((Troubleshooting))
    %% Keep items in alphabetical order within branches
    Parsing Issues
      Hierarchy breaks
        ::icon(fa fa-indent)
        "Fix: Use strict indentation"
    Rendering Issues
      Architecture connection
        ::icon(fa fa-network-wired)
        "Fix: Use side indicators (L,R,T,B)"
      Missing ZenUML
        ::icon(fa fa-puzzle-piece)
        "Fix: Register external plugin"
    Version Issues
      Beta Volatility
        ::icon(fa fa-flask)
        "Fix: Check official docs for changes"
```
