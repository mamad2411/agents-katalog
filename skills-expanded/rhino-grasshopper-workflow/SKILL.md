---
name: rhino-grasshopper-workflow
description: Plan and review safe Rhino 3D, Grasshopper, RhinoCommon, Rhino Python, and parametric AEC geometry workflows. Use for Grasshopper definitions, data trees, geometry pipelines, bake/export operations, and repeatable Rhino automation.
---

# Rhino / Grasshopper Workflow

Use for Rhino and Grasshopper-specific geometry and parametric automation. Route general IFC/DWG/DXF/SVG and other CAD/BIM tasks to `cad-bim-automation`; Revit/pyRevit/Dynamo tasks belong to `revit-workflow`.

## Establish the working context

Record the Rhino and Grasshopper versions, operating system, document units and tolerances, coordinate system, available plug-ins, input file formats, and execution surface (manual Rhino, Grasshopper graph, Rhino Python, RhinoCommon, or a verified integration). Leave unknowns as `UNKNOWN`. Check the installed environment or official version-matched documentation before naming API members or components.

## Model and graph safety

1. Preserve source .3dm and .gh/.ghx files. Prefer a duplicate document, versioned definition, or new export path for experiments.
2. Inventory inputs, expected outputs, geometry types, object counts, layers, units, tolerances, and reference dependencies before edits.
3. Identify whether data is internal, referenced, or live-linked; do not assume external references are portable.
4. Treat Grasshopper data trees explicitly: branches, paths, item ordering, graft/flatten behavior, nulls, and empty lists may change results.
5. Identify cyclic dependencies, uncontrolled recomputation, stochastic inputs without fixed seeds, and expensive operations before batch execution.
6. For any bake, replace, delete, or export action, require explicit scope and a reversible plan. Do not silently modify the original model.
7. Never assert fabrication, structural, accessibility, or code compliance from geometry alone.

## Repeatable workflow

### 1. Define invariants

Specify intended geometry and parametric relationships, allowable tolerance, expected counts, coordinate system, unit convention, and acceptance checks. State whether topology, object IDs, layer assignment, and naming must remain stable.

### 2. Preflight

Inspect definition inputs, slider ranges, referenced geometry, plug-in dependencies, data-tree shapes, missing components, warning/error states, and computation cost. Mark anything uninspected rather than guessing.

### 3. Prototype on a bounded sample

Prefer read-only inspection or a small subset first. Record baseline values and export previews to new paths. Verify closed/open curves and solids, invalid geometry, duplicate objects, normals, intersections, and bounding boxes where relevant.

### 4. Execute with checkpoints

For graph changes, document the components/parameters affected and expected branch-level output changes. For scripting, use the runtime's supported document context and undo/transaction facilities where available; verify their exact behavior for the installed version. For baking, capture source-to-output mapping and avoid overwriting unrelated objects.

### 5. Verify and report

Compare before/after object counts, data-tree paths, geometry validity, units, tolerances, bounding boxes, exported file integrity, and sample element mappings. Separate successes, skipped items, and failures. Supply rollback steps and unresolved dependencies.

## Deliverable

Return a compact **Environment / Inputs / Invariants / Proposed graph or script / Safety and rollback / Verification / Unknowns** plan. For reviews, prioritize silent data-tree changes, unit/tolerance drift, invalid geometry, plug-in/version assumptions, reference loss, and destructive bake/export operations.

Do not invent RhinoCommon API signatures, Grasshopper components, plug-in availability, or jurisdictional requirements. Verify version-specific behavior before prescribing executable code.
