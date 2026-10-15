---
name: ros2-design
description: Use this skill whenever the user wants to author or refresh a complete ROS 2 architectural design package — per-node specs, custom interface specs, a package-structure document, and a set of PlantUML data-flow + node-map diagrams — under a `designs/` (or similarly named) directory in the project's planning area (`docs/`, `_bmad-output/planning-artifacts/`, or wherever architecture lives). Trigger on phrases like "design the ROS 2 nodes", "create node design docs", "draw the data flow / node map", "lay out the colcon packages", "spec out the topics and services", or any request to take a PRD + architecture doc + hardware/wiring doc and produce the implementation contract that downstream agents will code against. Also trigger when the user says they have a PRD/architecture for a robotics project and asks "what's next" or "how should I structure the implementation". This is the load-bearing pre-implementation deliverable for any ROS 2 (Jazzy / Humble / Iron / Rolling) project.
---

# ros2-design — Author the design contract for a ROS 2 project

## Why this skill exists

A PRD says *what* to build. An architecture document says *how* the major decisions go. Neither tells the implementer what topics each node publishes, what schema fits in each message, where each package lives, or how data flows through the graph. That gap is filled by a set of design documents — and authoring them well takes discipline that AI agents tend to skip when they jump straight to code.

This skill turns three inputs (PRD, architecture, hardware/wiring) into the *exact* implementation contract — one markdown file per node, one custom-interfaces catalogue, one package-structure design, and a set of focused PlantUML diagrams — laid out so any future implementation story can be opened against a single authoritative reference.

The patterns are tuned for multi-tier robotics projects (microcontroller firmware over micro-ROS + Linux ROS 2 stack with SLAM, Nav2, optional behavior-tree missions, optional layered-architecture metaphors). They scale down: a Linux-only rover or a single-tier inspection bot uses the same templates with fewer files. Carry the patterns over; carry the *judgement* that decides which apply to *this* project.

## Inputs you must read first

Before writing a single design file, locate and read these inputs. Common locations are listed; ask the user if you can't find them.

1. **PRD** — `docs/PRD.md`, `docs/prd.md`, `_bmad-output/planning-artifacts/prd.md`, or wherever the project keeps it. Read all FRs and NFRs. Note any voided/excluded requirements. Note the Build Milestones / phases.
2. **Architecture document** — `docs/architecture.md`, `_bmad-output/planning-artifacts/architecture.md`, etc. Read the decisions list (D1, D2, …). Note custom packages mentioned. Note any biology metaphor or layered architecture (Spinal Cord / Cerebellum / Cortex / Senses) — and only adopt that vocabulary if the architecture has already adopted it.
3. **Hardware / wiring** — `hardware/WIRING-GUIDE.md`, `docs/hardware.md`, etc. Read GPIO assignments, sensor protocols, voltage rails, safety hardware (BMS, e-stops). The firmware-side node spec depends entirely on this.
4. **Epics / stories** if present — to confirm the package list, the timing of phases, and which FRs map to which stories.
5. **Roadmap** if present — to understand phase boundaries (P1/P2/P3) and what gets a placeholder vs. a full spec.

If any of these is missing, ask the user where it lives or whether it doesn't exist for this project. Don't guess.

## The design tree you produce

```
designs/
├── package-structure.md          # 1 file: colcon workspace + per-package layout + FR-to-package traceability
├── nodes/
│   ├── index.md                  # catalogue grouped by layer / process group
│   └── <node>.md                 # 1 file per node
├── interfaces/
│   ├── index.md
│   └── <pkg>_interfaces.md       # 1 file per custom interface package
└── diagrams/
    ├── index.md                  # embeds the rendered SVGs
    ├── node-map.puml + .svg      # layer-grouped catalogue
    ├── data-flow-overview.puml   # high-level inter-layer flows
    ├── data-flow-sensing.puml
    ├── data-flow-control.puml
    ├── data-flow-safety.puml
    ├── data-flow-operator.puml
    └── data-flow-tf.puml
```

The exact directory name (`designs/`, `design-artifacts/`, `architecture/`, …) depends on convention. Default to `designs/` adjacent to `architecture.md`. Always confirm with the user if there's an existing convention.

## Authoring order — follow this exactly

The order matters because each step's output becomes the next step's input. Doing them out of order causes drift (parameter names that don't match between node specs and the interfaces catalogue, BT nodes that the package-structure doesn't list, etc.).

### Step 0 — Pre-flight (always)

Read the three inputs. Build a working list of:

- **All custom packages** referenced in the architecture or epics (anything matching `<project>_<purpose>` — e.g. `<project>_safety`, `<project>_mission`, `<project>_perception`).
- **All nodes** referenced anywhere — custom *and* off-the-shelf (Nav2 stack nodes, `slam_toolbox`, `robot_localization`, `foxglove_bridge`, `joy_node`, vendor drivers).
- **All custom message/service/action types** mentioned anywhere
- **The firmware tier** if there is one (ESP32, STM32, Pico W, Arduino, …) — even though firmware isn't a colcon package, it gets a node spec because it appears in the ROS 2 graph as a single XRCE-DDS participant. **Critical design constraint:** the XRCE bridge in `micro_ros_agent` creates DDS participants using the `domain_id` sent in the XRCE `CREATE PARTICIPANT` request — `ROS_DOMAIN_ID` env var is ignored by the bridge. The firmware node spec must explicitly call `rcl_init_options_set_domain_id(&init_options, <domain>)` to join the correct DDS domain. Document this as a required parameter in the firmware node spec.
- **Phase tagging** — which nodes ship in which phase. P2/P3 nodes get a "placeholder" spec, not full detail.

Confirm this list with the user before authoring. Misses here are expensive to fix later.

### Step 1 — Decide which architectural patterns apply

A common pattern in robotics architectures is the biology metaphor (Spinal Cord = reactive safety, Cerebellum = sequencing/sensor fusion, Cortex = deliberative). **Don't impose this on a project that hasn't adopted it.** Read `references/three-layer-pattern.md` for when it fits and how to express it.

Ask the user (do **not** assume) about:

- **Behavior tree (BT.CPP) mission system** — only if the architecture mentions it. Otherwise, mission-level coordination might be Nav2's `/navigate_through_poses`, a Python state machine, SMACH, or just direct service calls. Don't fabricate a BT layer.
- **Spinal Cord override mechanism** — only if the architecture defines soft-vs-hard threshold classes. Otherwise, safety topics are just regular `/emergency_stop` `Bool` publishers.
- **Custom interface package** — required only if there are mission/safety/perception messages that don't fit standard `std_msgs` / `sensor_msgs` / `nav_msgs` / `geometry_msgs` / `vision_msgs`. Avoid creating one for a single trivial wrapper around an existing type.

> **Critical drift trap (the most common skill failure):** Once you've decided the project rejects the biology metaphor, **the words "Spinal Cord", "Cerebellum", "Cortex" must not appear anywhere in the design tree** — not in node Identity tables, not in Process Group fields, not in Layer fields, not as the name of a process group, not as a sub-grouping in diagrams. They may appear *only* as meta-mentions in prose that explicitly say the metaphor was rejected (e.g. "Per architecture decision Dn, no Spinal Cord / Cerebellum / Cortex split"). The templates list these as defaults because they're a common pattern; you must replace them with the project's actual vocabulary.
>
> Instead, use the project's flat-layout vocabulary (look at the architecture's process orchestration or package-structure section): typically `drivers`, `safety`, `navigation`, `perception`, `mission`, `operator I/O`, `infrastructure` — or the actual systemd unit / Compose service names like `<project>_mission`, `<project>_drivers`. The Process Group field should name the runtime unit, never an abstraction.
>
> Before writing the next file, verify your previous output: `grep -r 'Spinal Cord\|Cerebellum\|Cortex' designs/`. If you get hits and the architecture rejects the metaphor, fix them now — every additional file you write under the wrong vocabulary makes the leak worse.
- **Phased design** (Phase 1 / Phase 2 / Phase 3) — only adopt phase tagging if the roadmap uses it.

When in doubt, ask the user with a yes/no question. Don't proceed under assumption.

### Step 2 — Write `interfaces/` first

Always start here. The custom message and service schemas are the load-bearing dependency for every node spec. If you write the node specs first, you'll discover schema mismatches halfway through and have to backtrack.

**Before creating any custom type, read `references/standard-ros2-types.md`** — it catalogues every standard ROS 2 type by domain (sensor_msgs, std_msgs, geometry_msgs, nav_msgs, vision_msgs, etc.). Custom types add build complexity and reduce interoperability. Only create one when standard types genuinely cannot represent the data.

For each custom interface package (often just one):

1. Create `interfaces/index.md` — file catalogue + standard ROS 2 types used unchanged.
2. Create `interfaces/<pkg>_interfaces.md` — one heading per `.msg`, `.srv`, `.action`, with full schema + 1–2 YAML-style examples per type. End with a CMakeLists.txt skeleton.

Use the template at `assets/interfaces-template.md`. Read `references/qos-and-conventions.md` for the field-naming rules (snake_case fields, PascalCase types, leading `builtin_interfaces/Time timestamp`, string enums for readability).

### Step 3 — Write `nodes/<node>.md` for every node

One file per node. Order doesn't matter, but doing them grouped by layer (firmware → drivers → safety → fusion → SLAM → Nav2 → BT → mission → infrastructure) helps you spot duplicate decisions.

Each node file uses the template at `assets/node-template.md` and contains, in order:

- **Identity** — package, module, process group, layer, node type (`LifecycleNode` vs standalone vs micro-ROS client), logic class
- **Published Topics** — topic name, message type, QoS, rate, description; full schema + 1+ example for each type that hasn't appeared in an earlier node file
- **Subscribed Topics** — same shape
- **Services Served** — full request/response schema + examples; rejection reasons enumerated
- **Services Called** — pointer back to the providing node
- **Actions Served / Called** — same shape
- **Parameters** — full table with type, default, soft/hard if applicable, override range if soft
- **Lifecycle Behavior** — what each `on_configure` / `on_activate` / `on_deactivate` / `on_cleanup` does
- **Dependencies** — `Depends On` table + `Consumed By` table
- **Related Stories** — pointer to the epic stories that deliver this node (only if epics.md exists)

Read `references/node-spec-rules.md` for the load-bearing rules (when to inline a schema vs reference an earlier file, how to handle off-the-shelf nodes, when to mark a node "Phase 2 placeholder").

After writing all node files, write `nodes/index.md` — group by layer/process and reference every file. Don't write `index.md` first; you'll always miss a node.

### Step 4 — Write `package-structure.md`

This document describes the colcon workspace. Use the template at `assets/package-structure-template.md`. Sections:

1. **Design principles** — one layer ↔ one package, pure-logic separation, single-source YAML config, build-type rationale, naming convention, phase tagging
2. **Package catalogue** — table with row per package: layer, build type (`ament_cmake` for IDL/C++, `ament_python` for the rest), phase, nodes hosted
3. **Per-package detail** — directory layout per package, key code skeletons for the load-bearing logic classes
4. **Internal structure template** — the standard layout every Python package uses
5. **Dependency graph** — `<pkg>_interfaces` is the sink; verify no circular deps
6. **CMakeLists.txt / setup.py skeletons** — Python, CMake-IDL, C++ examples
7. **Workspace layout** + external configs location
8. **Build commands** — `colcon build`, `--packages-select`, common patterns
9. **FR-to-package traceability** — every active FR mapped to exactly one site
10. **Anti-patterns** — what's forbidden in this workspace
11. **Implementation sequence** — phase-by-phase package roll-out
12. **Validation checklist** — every dimension checked

Read `references/package-structure-rules.md` for traceability discipline (no orphan FRs, no duplicate ownership).

> **micro-ROS + Docker interface alignment:** If the stack uses `network_mode: "service:agent"` (shared namespace), the micro-ros-agent's Fast DDS participant binds to all container interfaces including `eth0`. Cyclone DDS in the sim container must be configured to use `eth0` (not `lo`) in `cyclonedds.xml` — otherwise they're on different interfaces and RTPS SPDP multicast never reaches Cyclone DDS. Document the required `cyclonedds.xml` interface in the package-structure deployment section.

### Step 5 — Write the diagrams

Order: node-map first, then data-flow-overview, then the five detail flows.

Use the template files at `assets/diagrams/*.puml.template`. Read `references/diagram-style.md` for the rules (one purpose per diagram, ≤10 arrows per canvas, no `title` line — markdown heading is the title, declare components before referencing them in arrows, never use `--> "label" as alias` shorthand).

After writing all `.puml` files, render SVGs:

```bash
cd <designs>/diagrams
plantuml -tsvg *.puml
```

If `plantuml` isn't available, tell the user how to install it (`brew install plantuml` on macOS, `apt install plantuml` on Debian/Ubuntu) and skip the SVG step — but still write `index.md` with `<img>` tags so the previews appear once they render.

Then write `diagrams/index.md` with the catalogue table + each diagram embedded under its own heading using `<img src="file.svg" width="100%">`. Don't use markdown `![](…)` because GitHub sometimes blocks inline SVG and oversized diagrams overflow the preview pane. Use the template at `assets/diagrams/index.md.template`.

### Step 6 — Cross-reference + propose architecture edits

Now do a drift sweep. Open `architecture.md` side-by-side with the design tree you've just produced. Compile a list of mismatches:

- **Threshold names** — does the architecture use the same parameter names as the interface and node specs? (Common drift: architecture says `battery_threshold_return`, interfaces use `battery_return_voltage`.)
- **Decision count** — does the architecture say "N decisions D1–D17" but actually define D1–D23?
- **Custom interfaces enumerated** — does the architecture's interfaces list match what's actually in the `<pkg>_interfaces.md` catalogue?
- **Project tree** — does the architecture's directory tree include the new `designs/` subtree and every package the design proposes?
- **Mission YAML schema** — does it use canonical threshold registry names?
- **Implementation Handoff section** — does it tell agents to read the design docs as the per-node contract?

**Propose edits to the architecture document** — do **not** apply them. Show the user a numbered list of proposed changes. Wait for approval per change before editing.

### Step 7 — Verify links + commit

Run a link-resolution pass:

```bash
# Pick out every relative markdown link and check it exists
grep -rnoE '\]\([^)]+\)' designs/ | …
```

Read `references/link-verification.md` for the exact verification snippet and how to handle false positives from regex matching parenthetical text.

Tell the user the design tree is ready. Don't commit unless asked.

## Checklist — run this before declaring "done"

- [ ] All three input documents read (PRD, architecture, hardware/wiring)
- [ ] User confirmed the package list, node list, custom interface list, and phase boundaries
- [ ] User explicitly answered yes/no on biology metaphor, BT mission system, override mechanism
- [ ] `interfaces/<pkg>_interfaces.md` written before any node file
- [ ] One `nodes/<node>.md` per node — including firmware tier and every off-the-shelf node Nav2/SLAM/etc
- [ ] `nodes/index.md` written *after* all per-node files
- [ ] `package-structure.md` includes a 100% FR-to-package traceability table (no orphans, no duplicates)
- [ ] All 7 diagrams (`node-map` + `data-flow-overview` + 5 details) authored
- [ ] Each `.puml` has its `.svg` rendered (or instructions provided if plantuml unavailable)
- [ ] `diagrams/index.md` embeds every SVG with `<img width="100%">`, not `![]()`
- [ ] Architecture-doc drift swept; user shown a proposed-edits list
- [ ] No `title` line in any `.puml` file (markdown heading is the title)
- [ ] No `--> "label" as alias` shorthand in any `.puml` (PlantUML rejects it)
- [ ] All cross-document relative links resolve
- [ ] **Vocabulary leak check** — if the architecture rejected the biology metaphor, run `grep -r 'Spinal Cord\|Cerebellum\|Cortex' designs/` and verify every hit is a meta-mention (a sentence that uses words like "no", "not", "rejected", "instead of", "replaced by"). Real usages — in Identity tables, Process Group fields, diagram sub-groups — are leaks; fix them before declaring done.
- [ ] **Pattern leak check** — same drill for `bt_executor` / `BT custom nodes` / `BT.CPP` if BT was rejected, and `OverrideThreshold` / `threshold_manager` / `/safety/override` if the override mechanism was rejected.

## Output to the user

End with three things:

1. **Tree** — `tree designs/` so the user sees what they got
2. **Open this first** — pointer to `designs/diagrams/index.md` since it's the most visual entry point
3. **Architecture-doc edit proposal** — numbered list of suggested changes to align `architecture.md`, awaiting user approval

## Reference files (read as needed)

| File | When to read |
|---|---|
| `references/three-layer-pattern.md` | Architecture mentions layers, biology metaphor, or Spinal Cord/Cerebellum/Cortex |
| `references/qos-and-conventions.md` | Authoring any topic/service/spec |
| `references/standard-ros2-types.md` | **New interface design** — always check for existing standard types before creating custom ones |
| `references/node-spec-rules.md` | Authoring node files, especially edge cases (firmware bridges, off-the-shelf nodes, placeholders) |
| `references/package-structure-rules.md` | Writing the `package-structure.md` |
| `references/diagram-style.md` | Authoring or reviewing PlantUML files |
| `references/link-verification.md` | Final verification pass |

## Templates

| Template | Use for |
|---|---|
| `assets/node-template.md` | Each `nodes/<node>.md` |
| `assets/interfaces-template.md` | Each `interfaces/<pkg>_interfaces.md` |
| `assets/interfaces-index-template.md` | `interfaces/index.md` |
| `assets/nodes-index-template.md` | `nodes/index.md` |
| `assets/package-structure-template.md` | `package-structure.md` |
| `assets/diagrams/node-map.puml.template` | Layer-grouped node map |
| `assets/diagrams/data-flow-overview.puml.template` | Layer-to-layer overview |
| `assets/diagrams/data-flow-sensing.puml.template` | Sensing chain |
| `assets/diagrams/data-flow-control.puml.template` | Control chain |
| `assets/diagrams/data-flow-safety.puml.template` | Safety chain |
| `assets/diagrams/data-flow-operator.puml.template` | Operator I/O |
| `assets/diagrams/data-flow-tf.puml.template` | TF tree |
| `assets/diagrams/index.md.template` | `diagrams/index.md` |

The templates contain the exact formatting (tables, headings, code-block placement) the rest of the skill assumes. Copy them, then fill in. Don't reinvent the structure on each project.
