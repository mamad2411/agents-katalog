---
name: "solidworks-parametric-assembly-build"
description: "Use when building a SolidWorks assembly from a spec that should be driven by one global-variables file, especially when sizes are placeholders pending inputs."
---

# Parametric assembly from one global-variables file

Read the solidworks-bridge-tool-selection skill first for the exact calls.

## 0. Gate on the spec
- If the spec leaves sizing inputs Open, ask the user: placeholder layout, supply inputs first, or skeleton only. Never present assumed sizes as a design.
- Placeholder parts carry custom properties: PartNo, Description, Material (OPEN if not given), Status = PLACEHOLDER - NOT SIZED, Note naming which spec input will size it.

## 1. Folder structure
01_Specification (copy of spec), 02_CAD/Parts, 02_CAD/Assembly, 02_CAD/Equations, 03_Drawings, 04_Calculations (open-inputs register), 05_Exports (STEP + picture), README.md.

## 2. Global variables file
02_CAD/Equations/<PROJ>_GlobalVariables.txt, one per line: "Name"= value (mm), derived values as expressions of others. Include all positions along the main axis plus a motion variable (for a cylinder: StrokePos, 0 = retracted).

## 3. Parts: each about its own origin
- Revolved-type parts: circles centred on origin on the Front plane, extrude along Z. No position dimensions needed.
- Lugs and eyes: CreateSketchSlot centred on the pin at the origin, mid-plane extrude; extra plates on an offset ref plane; bore cut through all.
- Boxes: corner rectangle at origin.
- Pins and bearings: mid-plane extrude so they are symmetric about the eye.
- The open part's features, equations, `rebuild`, `feature_errors`, `mass_properties`, and `save` with a full path are one batch. Then `CloseDoc`. Then `NewDocument`. Then `set_units`. `save_as` is not a batch step. Link the file (FilePath, LinkToFile, UpdateValuesFromExternalEquationFile) and Add2 one equation per driving dim inside that batch.
- Record each part's frame (which part axis is the main axis) in the README; mates depend on it.

## 4. Assembly
- New assembly, save_as first, OpenDoc each part one by one, ActivateDoc the assembly, AddComponent5 each instance near its final spot.
- UnfixComponent the first component.
- Every component: three plane mates to the assembly planes (two coincident, one distance along the axis). Pick align so the part axis maps onto the assembly axis; flipped parts (e.g. rod eye) use anti-aligned.
- Link the assembly to the same file and drive each D1@DistanceN with an equation (moving parts add StrokePos).

## 5. Validate
- check_interference with coincidence excluded; capture_view front, top, isometric.
- Set the motion variable to full stroke in the file, UpdateValuesFromExternalEquationFile, rebuild, read back the extended length with Parameter, re-check clash, then set it back.
- A clean rebuild is geometry only, not engineering acceptance. Say so in the README and the reply.

## 6. Deliver
Save, export STEP and a picture to 05_Exports, write README (structure, how to change sizes, conventions, not-modelled list, checks done) and the open-inputs register.