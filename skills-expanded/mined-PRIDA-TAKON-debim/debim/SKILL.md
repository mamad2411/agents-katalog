---
name: debim
description: Deterministic BOQ generation, Quantitative Take-Off (QTO), and Declarative BIM modeling (Building-as-Code) using debim. Use when asked to generate a bill of quantities (BOQ), estimate construction costs, calculate concrete/steel/formwork quantities from architectural plans or sketches, compile IFC4/IFC4.3 models, ingest Open GIS/OSM data, or produce 3D HTML web viewers.
---

# debim Skill — Deterministic BOQ & Declarative BIM Engine
**Version:** 1.1.0 (Urban Scale GIS Ingestion & ISO 19650 IFC4.3 Civil Infrastructure)  
**Specification:** debim Standard Spatial & Declarative Language Specification v1.1.0

This skill empowers AI agents to generate professional, deterministic **Bills of Quantities (BOQ)**, calculate structural material quantities (**QTO**), model **complex organic & algorithmic freeform architectures (lofts, swept columns, diagrid bracing, hexagonal facades)**, ingest **Open GIS & OSM city scale data**, and compile international standard **IFC4 / IFC4.3 BIM models** from architectural descriptions or sketches without hallucinating numbers.

---

## 🏛️ Core Philosophy for AI Agents

> **"Never guess construction numbers or hallucinate math in text."**

Instead of guessing concrete cubic meters or estimating rebar weights with vague approximations, the agent synthesizes the building geometry into a minimal **Declarative YAML/JSON manifest** (`project.yaml` or `project.json`) and executes deterministic calculation rules to produce mathematically exact figures.

---

## 🔒 Zero-Dependency & Offline Air-Gapped Operation

In air-gapped Virtual Machines (VMs) without internet connection or external package installations:
1. **Zero External Dependencies:**
   - debim relies on standard Python libraries (`argparse`, `json`, `math`, `re`, `pathlib`) and standard numerical tools (`numpy`).
   - CLI is migrating from `typer` to Python standard library `argparse`.
   - 3D mesh volume and bounding boxes are calculated directly via NumPy / divergence theorem, eliminating `trimesh`.
2. **Offline VM Execution via `scripts/debim_zero.py`:**
   - When running inside a pure Python 3 VM with **NO pip packages installed**, run:
     ```bash
     python scripts/debim_zero.py validate project.json
     python scripts/debim_zero.py qto project.json
     ```
3. **Local Schema Validation via `schemas/debim.schema.json`:**
   - A complete, self-contained JSON Schema is bundled at `schemas/debim.schema.json`.
   - AI agents and IDEs can perform static validation, schema enforcement, and parameter validation offline without querying any remote servers.

---

## 🏛️ Architectural Thinking & Modeling Sequence (The Architect's SOP)

Agents designing floor plans or modeling buildings must strictly follow the architectural workflow detailed in `references/architectural_workflow.md` (and `docs/ARCHITECTURAL_WORKFLOW.md`):

1. **Phase 1: Spatial Thinking & Programming (Before Drafting):**
   - **Human Scale + 30% Intra-room Circulation:** Calculate room net areas from furniture/sanitary fixtures footprints:
     $$\text{Area} = \left(\sum \text{Furniture Footprints}\right) \times 1.30$$
   - **Function Diagram & Adjacency:** Map connections (Living $\leftrightarrow$ Dining $\leftrightarrow$ Kitchen) and negative adjacencies (restrooms away from dining; quiet bedrooms away from mechanical/pump rooms).
   - **Volumetric 3D Spaces (`IfcSpace`):** Define functional volumes. Add **+30% overall circulation** for corridors and stairs.
   - **Site Boundaries & Stacking:** Comply with Thai building laws (setbacks, OSR $\ge 30\%$, FAR). Stack overflow functions onto upper storeys (Storey 1: Public, Storey 2: Private).
   - **MEP Coordination Priority:**
     $$\textbf{MEP relocates first} \longrightarrow \textbf{Structure adapts second} \longrightarrow \textbf{Architectural Space & Clear Height are preserved}$$

2. **Phase 2: Drafting Sequence:**
   `Schematic Spaces (IfcSpace)` $\rightarrow$ `Columns (IfcColumn)` $\rightarrow$ `Grid Axes (grids)` $\rightarrow$ `Beams & Slabs (IfcBeam, IfcSlab)` $\rightarrow$ `Roof (IfcRoof)` $\rightarrow$ `Walls & Openings (IfcWall, IfcDoor, IfcWindow based on Space adjacency)` $\rightarrow$ `Verification by Furniture Fit`.

---

## 📐 Coordinate & Bounding Rules (Immutable Standards)

### 1. Right-Handed Coordinate System
* **$+X$ Axis:** East / Grid Horizontal (Rightwards on 2D floor plans).
* **$+Y$ Axis:** North / Grid Vertical (Upwards on 2D floor plans).
* **$+Z$ Axis:** Elevation (Upwards towards the sky).
* **Base Units:** Meters ($m$), Square Meters ($m^2$), Cubic Meters ($m^3$), Radians ($rad$) or Degrees ($^\circ$).

### 2. Storey Elevation Inheritance
* Each storey defines base `elevation` (e.g. Ground = `0.00m`, First Floor = `3.50m`) and `height`.
* Elements assigned to a `storey` inherit that storey's elevation as their base $Z=0$ datum.
* `offset_z`: Positive lifts above floor line; negative lowers below floor line.

### 3. Counter-Clockwise (CCW) Vertex Ordering Rule
* For all horizontal area elements (**Slabs**, **Roofs**, and **Spaces**), polygon boundary vertices **MUST be listed in Counter-Clockwise (CCW)** order when looking down from $+Z$.
* CCW ordering guarantees positive upward normal $(0, 0, 1)$ and deterministic positive area calculation via the Shoelace Formula.

### 4. Wall Orientation & Thickness Centering
* Wall vector is defined by `from_grid` $\rightarrow$ `to_grid`.
* Looking along the vector:
  * **LEFT Side:** $90^\circ$ CCW normal vector (typically exterior).
  * **RIGHT Side:** $90^\circ$ CW normal vector (typically interior).
  * **CENTER (Default):** Wall baseline lies directly on grid axis; thickness expands $\pm t/2$ symmetrically.

---

## 🎯 AI Geometry Interpretation Standards (Anchor Points & Dimensions)

To eliminate AI ambiguity when synthesizing or modifying BIM elements, debim enforces deterministic **Anchor Points**, **Euler Rotations**, and **Dimension Keys**:

### 1. Position Anchor Points (จุดอ้างอิงพิกัดตายตัว)
* **`IfcColumn`:** `BOTTOM-CENTER` — กึ่งกลางฐานเสาที่ระดับพื้นชั้นล่าง ($Z=0$), เนื้อเสาพุ่งขึ้น $+Z$ สู่ชั้นบน.
* **`IfcBeam`:** `TOP-CENTERLINE` — แนวเส้นเชื่อมระดับ **หลังคาน** ($Z=0$), ความลึก `depth` **ห้อยจมลงด้านล่าง ($-Z$)**.
* **`IfcSlab`:** `TOP-FINISH` — ผิวบนสุดของพื้นอยู่ที่ระดับชั้น ($Z=0$), ความหนา `thickness` **จมลงด้านล่าง ($-Z$)** เพื่อรักษาความสูงเคลียร์ของห้องชั้นบน.
* **`IfcWall`:** `BOTTOM-START-CENTERLINE` — จุดเริ่มต้นผนังริมล่างสุดบนพื้นชั้น, ความหนาสมมาตรรอบแนวกริต, ความสูง `height` **ก่อขึ้นสู่ $+Z$**.
* **`IfcFooting`:** `TOP-CENTER` — ผิวบนสุดระดับหลังฐานราก, ความหนาจมลงดิน ($-Z$).
* **`IfcFurniture` / `IfcEquipment`:** `BOTTOM-CENTER` — ฐานล่างกึ่งกลางชิ้นงานแตะระดับพื้นพอดี ($Z_{\text{base}} = 0$).
* **`IfcSpace`:** `BOTTOM-PERIMETER` — ระนาบพื้นห้อง, ความสูง `height` พุ่งขึ้น $+Z$ สู่ฝ้าเพดาน.

### 2. Rotation & Euler Axis Order
* **Standard Unit:** **Radian** (ทวนเข็มนาฬิกาเป็นบวก, $0 = +X\text{ East}$, $+\frac{\pi}{2} = +Y\text{ North}$).
* **3D Euler Angles:** `[rx, ry, rz]` in **Radians** with **Z-up Extrinsic / Intrinsic Z-Y-X** order:
  * `rz`: Yaw (หมุนระนาบพื้นราบรอบแกน $Z$)
  * `ry`: Pitch (หมุนเงยรอบแกน $Y$)
  * `rx`: Roll (หมุนเอียงรอบแกน $X$)

### 3. Dimension Keys Per Class (ป้องกัน AI สับสน)
* **`IfcWall`:** `[thickness, height]` — *ห้ามใส่ length หรือ width* (ความยาวคำนวณจากระยะกริตอัตโนมัติ).
* **`IfcBeam`:** `[width, depth]` — *ห้ามใช้ height* (width = ความกว้างหน้าคาน, depth = ความลึกคานในแนวดิ่ง).
* **`IfcColumn`:** `[width, depth]` — มิติหน้าตัดตามแกน $X \times Y$.
* **`IfcSlab`:** `[thickness]` — ความหนาแผ่นพื้น.
* **`IfcSpace`:** `[height]` — ความสูงเคลียร์ของห้อง.
* **`IfcFurniture`:** `[width, depth, height]` — ขนาดตามแกน $X \times Y \times Z$.

---

## 🎯 Hybrid Reference Design (Grid + Offset + Inset)

Room boundaries and partitions rarely align perfectly with structural column grids. debim supports 3 flexible, interchangeable reference modes:

### Mode 1: Grid-Offset Mathematical Expressions
Human-readable arithmetic strings referencing grid centerlines with offsets:
```yaml
placement:
  boundary:
    - ["GX_1 + 0.10", "GY_1 + 0.10"]   # Offset 10cm inside from structural column grid
    - ["GX_2 - 0.10", "GY_1 + 0.10"]
    - ["GX_2 - 0.10", "GY_2 - 0.10"]
    - ["GX_1 + 0.10", "GY_2 - 0.10"]
```

### Mode 2: Automatic Inset (`inset` / `boundary_offset`)
Define the main column grids and automatically shrink/expand the polygon:
```yaml
placement:
  boundary:
    - [GX_1, GY_1]
    - [GX_2, GY_1]
    - [GX_2, GY_2]
    - [GX_1, GY_2]
  inset: 0.10   # Shrinks polygon inward by 10cm to account for half-wall thickness
```

### Mode 3: Explicit Cartesian Coordinates (`boundary_points`)
Direct $(X, Y)$ coordinate tuples in meters, ideal for irregular rooms or imported CAD/IFC polygons:
```yaml
placement:
  boundary_points:
    - [2.50, 1.20]
    - [6.50, 1.20]
    - [6.50, 4.80]
    - [2.50, 4.80]
```

---

## 🏢 Room & Space Modeling (`IfcSpace`)

Representing room geometry, usable areas, and HVAC volumes:
```yaml
- class: IfcSpace
  tag: master-bedroom
  name: "Master Bedroom"
  long_name: "Master Bedroom 101"
  room_number: "101"
  height: 2.80
  placement:
    storey: 00 groundfloor
    boundary:
      - ["GX_1 + 0.10", "GY_1 + 0.10"]
      - ["GX_3 - 0.10", "GY_1 + 0.10"]
      - ["GX_3 - 0.10", "GY_3 - 0.10"]
      - ["GX_1 + 0.10", "GY_3 - 0.10"]
  properties:
    occupancy: 2
    hvac_zone: "ZONE-AC-01"
    finish_floor: "FIN-PARQUET-01"
    finish_ceiling: "FIN-GYPSUM-01"
```
* **Net Floor Area ($m^2$):** Calculated via Shoelace Formula on boundary.
* **Air Volume ($m^3$):** $\text{Floor Area} \times \text{Height}$ for cooling load calculations.

---

## ⚡ Agent Workflow (Step-by-Step)

### Step 1: Synthesize Declarative Manifest (`project.yaml` or `project.json`)
Create the building manifest adhering to `schemas/debim.schema.json`.

```yaml
schema: IFC4-Minimal
project:
  id: PRJ-HOUSE-01
  name: "Modern Residence"
  units:
    length: METER
    area: SQUARE_METER
    volume: CUBIC_METER

spatial_structure:
  storeys:
    - id: Ground
      name: "Ground Floor"
      elevation: 0.00
      height: 3.50

grids:
  axes_x:
    A: 0.00
    B: 4.00
    C: 8.00
  axes_y:
    1: 0.00
    2: 5.00
    3: 10.00

materials:
  - id: CONC_240
    name: "Ready-Mixed Concrete 240 ksc"
    category: concrete
    unit_cost_ref: "MAT-CONC-01"
  - id: STEEL_RB9
    name: "Round Bar Steel RB9"
    category: rebar
    unit_cost_ref: "MAT-STEEL-01"
  - id: BLOCK_AAC
    name: "Autoclaved Aerated Concrete 7.5cm"
    category: masonry
    unit_cost_ref: "MAT-BLOCK-01"

elements:
  # Columns
  - class: IfcColumn
    tag: C-A1
    material: CONC_240
    profile: { shape: BOX, width: 0.20, depth: 0.20 }
    placement: { grid: [A, 1], base_storey: Ground, top_storey: Ground }

  # Beams
  - class: IfcBeam
    tag: B-A1-B1
    material: CONC_240
    profile: { shape: BOX, width: 0.20, depth: 0.40 }
    placement:
      storey: Ground
      from_grid: [A, 1]
      to_grid: [B, 1]

  # Slabs
  - class: IfcSlab
    tag: S-1
    material: CONC_240
    thickness: 0.15
    placement:
      storey: Ground
      boundary: [[A, 1], [B, 1], [B, 2], [A, 2]]

  # Spaces (Rooms)
  - class: IfcSpace
    tag: living-room
    name: "Living Room"
    height: 3.00
    placement:
      storey: Ground
      boundary:
        - ["A + 0.10", "1 + 0.10"]
        - ["B - 0.10", "1 + 0.10"]
        - ["B - 0.10", "2 - 0.10"]
        - ["A + 0.10", "2 - 0.10"]
```

### Step 2: Validate Model Integrity & Continuity
Run validation to check schema, structural continuity (floating columns/unsupported beams), and AABB clash detection:
```bash
# Standard CLI
debim validate -m project.yaml

# Offline VM (Zero-Dependency)
python scripts/debim_zero.py validate project.yaml
```

### Step 3: Calculate Quantitative Take-Off (QTO)
Extract concrete volume ($m^3$), formwork surface area ($m^2$), and rebar schedule ($kg$):
```bash
# Standard CLI
debim qto -m project.yaml

# Offline VM (Zero-Dependency)
python scripts/debim_zero.py qto project.yaml
```

### Step 4: Generate Cost Estimation & BOQ
#### Option A: Thai Government Public Works (ว480 & Commercial Ministry Index)
Automatically calculate rebar tonnage by member density, formwork contact deductions, Factor F, and export official ปร.4, ปร.5:
```bash
debim boq --rules cg-v480 --province nakhon_ratchasima -m project.yaml -o boq_v480.csv
```

#### Option B: Custom Commercial Unit Price Catalog
```bash
debim cost template -m project.yaml -o prices.yaml
debim cost -m project.yaml -p prices.yaml -o boq.csv
```

### Step 5: Compile IFC4 & 3D Web Viewer
```bash
debim compile -m project.yaml -o model.ifc
debim view -m project.yaml -e viewer.html --no-browser
```

---

## 🏗️ Advanced v0.6.0 Modeling Patterns

### 1. Module Array Replication (`modules:` & `instances: replicate:`)
```yaml
modules:
  - id: SHOPHOUSE_BAY
    local_grids: { axes_x: { "1": 0.0, "2": 4.0 }, axes_y: { "A": 0.0, "B": 12.0 } }
    elements: [...]

instances:
  - replicate:
      module: SHOPHOUSE_BAY
      count: 4
      along: grid_x
      prefix_pattern: "U{index}_"
      party_wall_deduplication: true
```

### 2. Slab Voids (Double-Volume & Stair Openings)
```yaml
elements:
  - class: IfcSlab
    tag: SLAB-MEZZ
    thickness: 0.12
    placement:
      storey: Mezzanine
      boundary: [["1", "A"], ["5", "A"], ["5", "D"], ["1", "D"]]
      voids:
        - [["2", "B"], ["4", "B"], ["4", "C"], ["2", "C"]] # Atrium void
```

### 3. Parametric Vernacular Roof (`IfcRoof: GABLE_HIP`)
```yaml
elements:
  - class: IfcRoof
    tag: ROOF-MAIN
    roof_type: GABLE_HIP
    pitch_deg: 32.5
    boundary: [["1", "A"], ["5", "A"], ["5", "D"], ["1", "D"]]
    framing: { rafter_spacing: 1.00, purlin_spacing: 0.35, material: STEEL_SS400 }
```

### 4. Multi-Flight Dog-Leg Stairs with Landing Elevation (v0.7.0)
```yaml
elements:
  - class: IfcStair
    tag: STAIR-L1-L2
    stair_type: DOG_LEG
    flight_steps: [11, 6]      # Explicit riser scheduling (Flight 1: 11, Flight 2: 6)
    landing_elevation: 2.20    # Explicit intermediate landing level datum
    width: 1.10
    waist_thickness: 0.15
    material: CONC_240
    placement:
      grid_anchor: ["1", "A"]
      from_storey: L1
      to_storey: L2
```

### 5. Sunken Bathroom Slabs & Cantilevers with Arithmetic Offsets (v0.7.0)
```yaml
elements:
  - class: IfcSlab
    tag: SLAB-BATH-SUNKEN
    material: CONC_240
    thickness: 0.10
    elevation_offset: -0.10    # Recessed 10cm below storey level for waterproofing
    placement:
      storey: L1
      boundary:
        - ["1 + 0.10", "A + 0.10"]
        - ["2 - 0.10", "A + 0.10"]
        - ["2 - 0.10", "B - 0.10"]
        - ["1 + 0.10", "B - 0.10"]
```

### 6. Host-Wall Auto-Punching & Multi-Storey Openings (v0.7.0)
```yaml
elements:
  - class: IfcWindow
    tag: W5-STAIR-TALL
    host_wall: WALL-EXT-1       # Automatically cuts opening in host wall geometry
    span_storeys: ["L1", "L2"]  # Spans double-height stairwell without tag duplication
    overall_width: 1.40
    overall_height: 2.90
    placement:
      storey: L1
      offset_x: 1.20
      sill_height: 0.80
```

### 7. L-Shaped Composite Hip Roof with 3D Valley & Hip Solver (v0.7.0)
```yaml
elements:
  - class: IfcRoof
    tag: ROOF-COMPOSITE-L
    roof_type: HIP
    pitch_deg: 35.0
    storey: L2
    elevation: 6.65
    boundary:
      - ["1", "A"]
      - ["5", "A"]
      - ["5", "C"]
      - ["3", "C"]
      - ["3", "E"]
      - ["1", "E"]
    eaves_overhang: 1.00
```

### 8. Structural Framing Array Macros (ColumnGrid & BeamBay) (v0.8.0)
```yaml
# Eliminate manual coding of 50+ columns and 70+ beams!
macro_elements:
  - type: ColumnGrid
    prefix: "COL"
    material: CONC_240
    profile: { shape: BOX, width: 0.25, depth: 0.25 }
    grids_x: ["1", "2", "3", "5", "6", "7"]
    grids_y: ["A", "B", "C", "D"]
    base_storey: FL1
    top_storey: FL2
    except_points:
      - ["1", "A"]   # Point without column (e.g. open porch corner)

  - type: BeamBay
    prefix: "BEAM-FL1"
    material: CONC_240
    profile: { shape: BOX, width: 0.20, depth: 0.50 }
    storey: FL1
    grids_x: ["1", "2", "3", "5", "6", "7"]
    grids_y: ["A", "B", "C", "D"]
    direction: BOTH  # Generates beams along X and Y axes automatically
```

### 9. Point Offsets & String Arithmetic on Columns and Walls (v0.8.0)
```yaml
elements:
  # Displaced column (e.g. carport offset from main grid)
  - class: IfcColumn
    tag: COL-CARPORT-OFFSET
    material: CONC_240
    profile: { shape: BOX, width: 0.25, depth: 0.25 }
    placement:
      grid: ["3 + 1.00", "B - 0.50"]   # Direct string arithmetic
      offset_x: 0.20                   # Or explicit offset parameters
      offset_y: 0.00
      base_storey: FL1
      top_storey: FL2
```

### 10. The Pure Algorithmic Architecture Engine & Organic Lofts (v1.0.0 GA)
When tasked with modeling double-curved landmark buildings (e.g. Museo Soumaya, Guggenheim, twist towers, or organic amphitheaters):
```yaml
# 1. Macro-Geometry: Asymmetric Multi-Level Organic Polygon Loft
geometry_rules:
  type: POLYGONAL_LOFT # or HYPERBOLIC_LOFT / CYLINDRICAL_LOFT / CONICAL_LOFT
  base_polygon:
    - [-26.84, -3.92]
    - [35.19, -3.92]
    - [-0.06, 31.96]
  waist_polygon:
    - [-16.34, -3.35]
    - [14.40, -3.35]
    - [-2.17, 16.61]
  roof_polygon:
    - [-16.59, -3.15]
    - [20.93, -3.15]
    - [1.34, 21.21]

# 2. Swept Curved Columns, Diagrid X-Bracing, & Compression Rings
structures:
  column_generator:
    count: 28
    distribution: UNIFORM_PERIMETER
    profile: CIRCULAR_HOLLOW_D600
    trajectory: LOFT_SURFACE_ISOPARAMETRIC
    material: STEEL_WHITE

# 3. Conformal Hexagonal Facade Panels
facade:
  envelope_skin:
    target: POLYGONAL_LOFT
    pattern: HEXAGONAL_CONFORMAL # or VORONOI_CENTROIDAL
    target_panel_size: 0.85
    joint_gap: 0.015
    material: ALUMINUM_ANODIZED_SILVER
    ifc_representation: IfcTriangulatedFaceSet
```

### 11. Urban Scale Ingestion & ISO 19650 IFC4.3 Civil Infrastructure (v1.1.0)
When tasked with city-scale digital twins, municipal road networks, or open GIS ingestion:
```yaml
schema: IFC4-Minimal
project:
  id: PRJ-URBAN-001
  name: "Asoke-Sukhumvit City Model"
  crs:
    epsg: 32647          # WGS 84 / UTM zone 47N
    name: "WGS 84 / UTM zone 47N"
    easting: 668889.88   # Local map origin
    northing: 1519258.81

elements:
  # Civil Infrastructure: Road with Layered Pavement & Sidewalk Curbs
  - class: IfcRoad
    tag: RD-SUKHUMVIT-PRIMARY
    dimensions: { width: 14.0, height: 0.30 }
    placement:
      coordinates: [[0.0, 0.0], [500.0, 0.0]]
    facility_part: ROADWAY
    pavement:
      wearing_course_thickness: 0.05
      base_course_thickness: 0.20
      kerb: { width: 0.15, height: 0.30 }

  # Automated 3D Extruded Building from GIS Footprint
  - class: IfcBuildingElementProxy
    tag: BLDG-TOWER-01
    predefined_type: USERDEFINED
    placement:
      position: [120.0, 45.0, 0.0]
    geometry:
      type: EXTRUSION
      height: 48.0       # Extruded from OSM building:levels
      polygon: [[0, 0], [25, 0], [25, 30], [0, 30], [0, 0]]
```

CLI Command:
```bash
# Ingest OpenStreetMap Overpass Bounding Box (Lat/Lon) into native .debim
debim urban ingest --bbox "13.734,100.558,13.742,100.566" --crs 32647 -o asoke.debim

# Compile to ISO 19650 IFC4.3
debim compile -m asoke.debim -o asoke.ifc
```

---

## 📂 Bundled Skill Assets

* **`SKILL.md`:** This master guide.
* **`schemas/debim.schema.json`:** Official offline JSON Schema (Draft 2020-12).
* **`scripts/debim_zero.py`:** Standalone Python standard library engine for air-gapped VMs.
* **`references/coordinate_and_bounding_rules.md`:** Formal specification of coordinate systems, winding rules, and vector formulas.
