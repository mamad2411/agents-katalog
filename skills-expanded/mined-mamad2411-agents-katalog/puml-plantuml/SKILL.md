---
name: puml-plantuml
description: >-
  Full-stack PlantUML expert: create PUML from descriptions, convert images to
  PUML (vision reverse engineering), render locally (PNG/SVG/PDF) with no internet.
  macOS/Windows/Linux; auto-installs PlantUML+Java+Python. Covers all 27 chapters
  of the PlantUML Language Reference Guide v1.2025.0 (607 pages): Sequence, Use
  Case, Class, Object, Activity (legacy+new), Component, Deployment, State, Timing,
  JSON, YAML, nwdiag, Salt/Wireframe, Archimate, Gantt, MindMap, WBS, Maths, ER,
  Common Commands, Creole, Sprites, Skinparam, Preprocessing, Unicode, StdLib
  (C4/AWS/Azure/K8s/ArchiMate). Use for: draw a diagram, create PUML, convert
  image to PUML, render .puml, debug PUML, explain PlantUML syntax, any UML task.
license: AGPL-3.0-only
compatibility: >-
  Python 3.9+ (stdlib only). PlantUML + Java auto-installed on first use.
  Java auto-detected: Azul/Zulu, Temurin/Adoptium, OpenJDK, Microsoft JDK,
  SDKMAN, Homebrew (any JRE 11+). macOS / Windows / Linux. Works in Claude
  Code, Gemini Code, Cursor, Copilot, and any AI coding assistant with
  bash/terminal access.
metadata:
  author: Erez Kalman / KSEC
  version: "2.0.0"
  category: developer-tools
  pdf-source: "PlantUML Language Reference Guide v1.2025.0 (607 pages)"
---

# PUML-PlantUML Expert Skill

Deep PlantUML knowledge (all 27 chapters from official reference) + cross-platform
local rendering + image→PUML reverse engineering. **Offline rendering.** Any OS. No
assumed paths. Full Python + Java + PlantUML auto-detection and installation.

---

## Quick Decision Tree

```
User request
├── "Create/draw a diagram from description"   → § Generate PUML
├── "Convert image/screenshot to PUML"         → § Image → PUML
├── "Render/preview/generate image from code"  → § Render Locally
├── "Fix/debug my PUML"                        → § Diagnose & Fix
└── "Explain syntax / how do I..."             → references/syntax-quick-ref.md
```

---

## § First Run — Bootstrap from Zero

The bootstrap scripts require **no pre-installed tools** — they install
Python → Java → PlantUML in the correct order. Run once per machine.

### macOS / Linux
```bash
bash scripts/bootstrap.sh           # install everything
bash scripts/bootstrap.sh --verify  # install + test render
```

### Windows (PowerShell — built into Windows 10/11)
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\bootstrap.ps1
.\scripts\bootstrap.ps1 -Verify
```

### If Python is already available
```bash
python3 scripts/render.py --detect      # show what's detected
python3 scripts/setup.py               # install Java + PlantUML
python3 scripts/setup.py --java        # ensure Java only
python3 scripts/setup.py --jar         # force JAR download
python3 scripts/setup.py --verify      # install + test render
python3 scripts/render.py --install-hint  # show manual steps
```

**What gets installed:**

| Component | macOS | Linux | Windows |
|-----------|-------|-------|---------|
| Python 3.9+ | brew | apt/dnf/pacman/snap | winget/choco/scoop |
| Java JRE 11+ | brew cask temurin | apt/dnf/pacman | winget Temurin/Zulu |
| PlantUML | brew | apt/dnf/pacman/snap | winget/choco/scoop |
| Fallback | — | `~/.plantuml/plantuml.jar` | `~/.plantuml/plantuml.jar` |

Java detected from: `$JAVA_HOME`, PATH, macOS `/usr/libexec/java_home`,
Azul/Zulu (`zulu*`), Temurin, Homebrew OpenJDK, SDKMAN, `/usr/lib/jvm/*`.

---

## § Generate PUML from Description

**Step 1 — Identify diagram type:**

| Keywords in request | Type | Tag |
|--------------------|------|-----|
| sequence of calls, API flow, messages | Sequence | `@startuml` |
| classes, OOP, inheritance, methods | Class | `@startuml` |
| process, workflow, flowchart, steps | Activity (new) | `@startuml` |
| architecture, services, components | Component | `@startuml` |
| database, schema, tables, entities | ER | `@startuml` |
| states, lifecycle, status transitions | State | `@startuml` |
| use cases, actors, user stories | Use Case | `@startuml` |
| objects, instances, runtime snapshot | Object | `@startuml` |
| timing, signals, waveforms | Timing | `@startuml` |
| brainstorm, concept map, topics | MindMap | `@startmindmap` |
| project timeline, schedule, milestones | Gantt | `@startgantt` |
| work breakdown, project phases | WBS | `@startwbs` |
| UI form, wireframe, mockup | Salt | `@startsalt` |
| JSON data structure | JSON | `@startjson` |
| YAML data structure | YAML | `@startyaml` |
| network topology, servers, subnets | nwdiag | `@startuml` + `nwdiag {}` |
| enterprise architecture, ArchiMate | Archimate | `@startuml` + `archimate` kw |
| math formula, equation, LaTeX | Maths | `@startmath` / `@startlatex` |
| ASCII art diagram | Ditaa | `@startditaa` |

**Step 2 — Generate** using the full syntax in `references/syntax-quick-ref.md`.
Always include: a `title` line, `skinparam shadowing false`, labels on all arrows.

**Step 3 — Write, validate & render:**
```bash
cat > /tmp/diagram.puml << 'PUML'
@startuml
title My Diagram
... generated code ...
@enduml
PUML

python3 scripts/render.py /tmp/diagram.puml --check   # validate
python3 scripts/render.py /tmp/diagram.puml -f svg -o /tmp/  # render
```

---

## § Image → PUML (Reverse Engineering)

1. **View the image** — use the `view` tool or examine the upload
2. **Identify the diagram type** — `references/image-to-puml.md`
3. **Extract elements** — names, labels, arrows, relationships, cardinality
4. **Generate PUML** — reproduce faithfully, correct arrow types
5. **Validate & render** — compare against original; refine if needed

> Visual analysis guide: `references/image-to-puml.md`

---

## § Render Locally

Use `scripts/render.py` — auto-detects binary vs JAR+Java, any OS.

```bash
# macOS / Linux
python3 scripts/render.py diagram.puml                        # PNG
python3 scripts/render.py diagram.puml -f svg -o ./output/   # SVG
python3 scripts/render.py diagram.puml -f pdf -o ./output/   # PDF
cat diagram.puml | python3 scripts/render.py --stdin -f svg -n "name" -o /tmp/

# Windows
py scripts\render.py diagram.puml
py scripts\render.py diagram.puml -f svg -o .\output\
```

Direct CLI (if `plantuml` is in PATH):
```bash
plantuml -tsvg diagram.puml
plantuml -tpng -o ./output/ *.puml
plantuml -checkonly diagram.puml
```

Present the output file to the user after rendering using `present_files`.

> Full options, env vars, formats, troubleshooting: `references/local-rendering.md`

---

## § Diagnose & Fix PUML

```bash
python3 scripts/render.py diagram.puml --check
```

| Error | Cause | Fix |
|-------|-------|-----|
| `No @startuml found` | Missing wrapper | Add `@startuml` / `@enduml` |
| `Unknown command` | Typo or wrong diagram type | Check syntax-quick-ref.md |
| Arrow `→` (Unicode) | ASCII required | Use `->` not `→` |
| `Cannot find class` | Forward reference | Declare before use |
| Graphviz error | `dot` not installed | `brew/apt install graphviz` OR add `!pragma layout smetana` |
| PlantUML not found | Not installed | `bash scripts/bootstrap.sh` |
| Java not detected | Non-standard JDK | Set `JAVA_HOME` env var |
| Python not found | Python missing | `bash scripts/bootstrap.sh` |
| Unicode broken | Charset issue | `plantuml -charset UTF-8 file.puml` |

---

## § Syntax Cheatsheet (Ultra-Quick)

> Full reference (all 27 chapters, 2700+ lines): `references/syntax-quick-ref.md`

**Sequence arrows:**
```
->   sync          -->  response/dashed
->>  thin           -->> thin dashed
->x  lost           ->o  open arrowhead
<->  bidirectional  ->+  activate   -->-  deactivate
[->  incoming      ->]   outgoing
```

**Class relationships:**
```
<|--  inheritance    <|..  realization
o--   aggregation    *--   composition
-->   dependency     ..>   usage
--    association    --()  lollipop (provided interface)
"1" *-- "0..*"  : label  (with cardinality and label)
```

**ER cardinality (crow's foot):**
```
||   exactly one    o|   zero or one
o{   zero or more   |{   one or more
```

**All @start tags:**
```
@startuml          most diagrams
@startmindmap      mind maps
@startgantt        gantt charts
@startwbs          work breakdown
@startsalt         wireframes
@startjson         JSON display
@startyaml         YAML display
@startmath         AsciiMath
@startlatex        LaTeX formula
@startditaa        Ditaa ASCII art
```

**Universal formatting:**
```plantuml
title My Title
skinparam shadowing false
skinparam monochrome true
!theme cerulean
left to right direction
!pragma layout smetana    ' no Graphviz needed
```

---

## Complete Diagram Coverage (All 27 Chapters from PDF)

| Ch | Type | Notes |
|----|------|-------|
| 1 | **Sequence** | Full: arrows, groups, activation, notes, autonumber, mainframe, parallel, stereotypes/spots, anchors, encompass, hide footbox |
| 2 | **Use Case** | Full: actors, extends/include, notes, packages, business UC, JSON overlay |
| 3 | **Class** | Full: visibility, stereotypes, spots, generics, lollipop, extends/implements keywords, hide/show/remove, $tags, namespaces |
| 4 | **Object** | Instances, relations, maps, association objects |
| 5 | **Activity (Legacy)** | Old `(*) -->` syntax, branches, synchronization bars, partitions |
| 6 | **Activity (New)** | start/stop, if/else/elseif, switch/case, while, repeat, fork, split, swimlanes, SDL shapes, goto/label, connectors, condition style |
| 7 | **Component** | Components, interfaces, ball-socket, grouping, ports, hide unlinked |
| 8 | **Deployment** | All element types, nesting, ports, round corners, orientation |
| 9 | **State** | Nested, concurrent, fork/join, history, choice, pin, expansion, note on link, inline colour |
| 10 | **Timing** | robust, concise, binary, clock, analog; relative time, anchors, highlights |
| 11 | **JSON** | Display, highlight, styles, minimal examples |
| 12 | **YAML** | Display, highlight, aliases, Creole |
| 13 | **Network (nwdiag)** | Networks, nodes, addresses, grouping, sprites, peer networks |
| 14 | **Wireframe (Salt)** | All widgets: button, input, dropdown, radio, checkbox, grid, tree, tabs, group box, scrollbox |
| 15 | **Archimate** | archimate keyword, junctions, macros, StdLib integration |
| 16 | **Gantt** | Tasks, constraints, milestones, colours, completion %, hyperlinks, closed days, zoom, scale |
| 17 | **MindMap** | OrgMode and Markdown syntax, left branches, multiroot, colours, direction |
| 18 | **WBS** | OrgMode syntax, direction, colours, arrows, word wrap |
| 19 | **Maths** | AsciiMath (`@startmath`), LaTeX/JLaTeXMath (`@startlatex`), inline `<math>` tags |
| 20 | **ER (Info Engineering)** | Entities, attributes, PK/FK markers, crow's foot relations |
| 21 | **Common Commands** | comments, scale/zoom, title, caption, header, footer, legend, newpage, mainframe, appendix, pragma |
| 22 | **Creole** | Bold, italic, mono, strike, underline, wave; lists, headings, tables, links, emoji, HTML tags, Unicode |
| 23 | **Sprites** | Define hex sprites, inline SVG sprites, import from StdLib, OpenIconic, Font Awesome |
| 24 | **Skinparam** | Full per-element skinparam + modern `<style>` CSS-like alternative + all themes |
| 25 | **Preprocessing** | Variables, conditions, while/loop, procedures, functions, default args, unquoted, keyword args, includes, subparts, themes, define, builtins (`%string`, `%strlen`, `%date`, `%random`, `%hsl_color`, etc.) |
| 26 | **Unicode** | Native UTF-8, `&#XXXX;` and `<U+XXXX>` references, emoji `<:name:>`, charset flag |
| 27 | **StdLib** | ArchiMate, AWS, Azure, C4, Kubernetes, Elastic, GCP, CloudOgu, Tupadr3/FontAwesome, EDGY |
| — | **Ditaa** | `@startditaa` ASCII art to diagram |

---

## Reference Files

| File | Content |
|------|---------|
| `references/syntax-quick-ref.md` | **2700+ lines** — complete syntax for all 27 chapters |
| `references/image-to-puml.md` | Visual analysis guide for image→PUML reverse engineering |
| `references/local-rendering.md` | Setup, CLI flags, formats, env vars, troubleshooting |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/bootstrap.sh` | **Start here — macOS/Linux** — installs Python→Java→PlantUML (no deps) |
| `scripts/bootstrap.ps1` | **Start here — Windows** — PowerShell 5+, no deps required |
| `scripts/setup.py` | Python setup: detect/install Java + PlantUML; also reports Python |
| `scripts/render.py` | Cross-platform render: auto-detects Python/binary/JAR/Java |
