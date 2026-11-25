---
name: solidworks-modeler
description: Create or revise SolidWorks parts, assemblies, and three-view drawings from natural-language descriptions, dimensioned drawings, sketches, or reference images; automatically lay out views, import model dimensions, and export SLDPRT, SLDASM, SLDDRW, PDF, or DWG deliverables in single or batch workflows without a separate vision API.
---

# SolidWorks Modeler

Use built-in vision and local SolidWorks COM automation. Do not require a browser service or API key.

For user-facing installation, first-run checks, example prompts, and troubleshooting, read `使用教程.md`.

> **Runtime requirement:** This skill controls desktop SolidWorks through `cscript.exe` and the `SldWorks.Application` COM object. It only works on a Windows host with SolidWorks and Node.js 20 or newer. When local desktop execution is unavailable, generate the scripts plus a one-click `.bat` launcher for the user to run on the Windows host.

## Supported Deliverables

- connect to a visible local SolidWorks session through COM;
- generate parts and assemblies from natural language, drawings, or images;
- inspect images with built-in vision and convert visible evidence into a parameter table before modeling;
- create third-angle front, top, and right engineering views from `.SLDPRT` or `.SLDASM` files;
- use the selected drawing template to arrange the three views and fit the sheet;
- import model dimensions into the drawing when requested;
- save the editable `.SLDDRW` and export `.PDF` and `.DWG` files;
- process up to 64 drawing jobs in one visible SolidWorks session.

This is automation, not an assertion that a raster image contains hidden dimensions. Automatic dimension mode imports dimensions that exist in the model; it does not invent missing tolerances, GD&T, datums, fits, surface finish, or a complete manufacturing dimension scheme.

## Write Authorization

A request to create, rebuild, revise, or save a SolidWorks model authorizes writes inside a new task output directory. If the user asked only to analyze, compare, estimate, diagnose, or review, ask for approval before writing CAD files or changing an installed skill. Never treat a read-only request as build authorization.

## Compatibility Check

Require Windows, desktop SolidWorks, Windows Script Host (`cscript.exe`), Node.js 20 or newer, part/assembly templates, and a drawing template for drawing workflows. On first use, after moving the Skill to another computer, or after any COM/template failure, run:

```powershell
node "<skill-dir>\scripts\check-environment.mjs"
```

Do not start a build until this check passes. Keep its exact diagnostic output when reporting a failure.

## Input Rules

Accept:

- text only;
- image or drawing only;
- images plus text;
- changes to an earlier model.

Apply evidence in this order:

1. Explicit dimensions and constraints in the user's text.
2. Dimensions printed on drawings.
3. Geometric relationships that are unambiguous.
4. Named concept defaults, clearly reported as assumptions.

Never infer an absolute dimension from photo scale. If a critical dimension is missing and no named default applies, ask one consolidated question.

When the reference is a SolidWorks or other CAD screenshot, treat visible silhouette, part count, coaxial holes, face contact, symmetry, and component overlap as stronger evidence than generic concept defaults. A raster screenshot still does not reveal exact dimensions, hidden features, mates, or the original feature tree; report those limits.

## Choose Model Level

- **Concept model:** Use for vague requests such as "make a normal robotic arm" or "make a teacup." Select conservative defaults, list them, and produce inspectable geometry. Do not claim it is load-rated or manufacturing-ready.
- **Manufacturing model:** Use only when materials, loads, interfaces, purchased components, tolerances, and fabrication constraints are supplied or confirmed.

For a default desktop robotic arm concept, use:

- 4 rotational axes: base yaw, shoulder pitch, elbow pitch, wrist pitch;
- two-finger parallel gripper;
- base: diameter 180 mm, height 25 mm;
- upper-arm joint-center distance: 220 mm;
- forearm joint-center distance: 180 mm;
- link thickness: 16 mm;
- joint pin diameter: 20 mm;
- wrist envelope: diameter 60 mm, length 50 mm;
- finger length: 90 mm; maximum opening: 80 mm;
- separate named components and a top-level assembly.

For a default teacup or mug concept (mm), use: height 85; base outer/inner diameter 50/42; rim outer/inner diameter 80/72; wall thickness about 4; floor thickness 6; ring handle centered 48 from the axis at height 45; outer/inner handle radius 22/14; handle thickness 10.

State that motor mounts, bearings, fasteners, cable routing, wall thickness, capacity, fillets, limits, strength, and tolerances remain unspecified unless the user provides them.

## Coordinate Calibration

Do not assume that a reference-plane name, feature order, sketch X/Y axes, assembly X/Y/Z axes, or positive extrusion direction maps the way it did in another template or SolidWorks version.

Before a multi-part build:

1. Create or inspect one simple probe part in the selected templates.
2. Confirm the sketch-plane axis mapping and extrusion sign from the resulting geometry or preview.
3. Record the mapping in the task specification, for example `Top sketch X/Y -> assembly X/Z; extrusion -> -Y`.
4. Express stacked components as explicit min/max ranges on the stack axis. Adjacent ranges must meet at zero gap, or use a small, declared concept overlap only when manufacturing interfaces are unspecified.

If a preview contradicts the intended coordinates, the preview wins. Stop, recalibrate the mapping, and rebuild in a new output directory. Do not defend a connection from coordinates that the rendered model disproves.

## Workflow

1. Inspect every supplied image with the available image-viewing tool before reasoning about it.
2. Classify the request as a single part, multi-part assembly, or revision.
3. Produce a compact feature tree or assembly tree, a millimeter parameter table, and an interface table for every critical connection.
4. Calibrate the task's plane mapping and extrusion directions before placing a stack or articulated chain.
5. List only material assumptions and unresolved engineering risks. Proceed with concept defaults when the user asked for a normal, generic, simple, or default design.
6. Select the build route:
   - For one rectangular or circular plate with circular through-holes, use `scripts/build-part.mjs`.
   - For two or more supported plate parts, use one `scripts/build-batch.mjs` invocation. Do not loop over `build-part.mjs`; the batch builder reuses one SolidWorks COM session.
   - For a compact cycloidal pin reducer, use `scripts/generate-cycloidal-reducer.mjs`. It creates separate housing, cover, pin, disc, bearing, shaft, cam, and flange parts with a 34-component default assembly.
   - For bodies of revolution such as cups, mugs, bottles, shafts, and flanges, use the **Revolved Parts** recipe below.
   - For other parts or assemblies, create a task-specific VBScript in the user's workspace. Reuse the late-bound COM and template-discovery patterns from `scripts/solidworks.vbs`; do not modify the installed skill.
   - For assembly templates, prefer the configured default, then `gb_assembly.asmdot`, then another `.asmdot` in the installed templates directory.
7. Keep SolidWorks visible during automation. Save new outputs under the workspace `output/solidworks/` directory with unique names.
8. Whenever you generate a `.vbs`, also emit a matching one-click `.bat` launcher using the recipe below.
9. Export a full-assembly preview and a close-up of every critical interface. Inspect each image with the image-viewing tool.
10. When drawings or exports are requested, run the drawing workflow after all source models pass model verification.
11. Apply the verification gate below. Report exact paths, verification evidence, assumptions, and any failed check.

## One-Click Run Helper

Whenever you generate a task-specific `.vbs`, create a matching `.bat` launcher in the same directory:

```bat
@echo off
setlocal
cd /d "%~dp0"
if not exist "output" mkdir "output"
set "TARGET=%~dp0output\<part-name>.SLDPRT"
set /a N=1
:findname
if exist "%TARGET%" (
  set "TARGET=%~dp0output\<part-name>_%N%.SLDPRT"
  set /a N+=1
  goto findname
)
cscript //NoLogo "%~dp0<script-name>.vbs" "%TARGET%"
echo Done. Output: %TARGET%
pause
```

The launcher must work by double-click, create an `output` directory beside itself, choose a unique output name, and keep the console open so errors remain visible. Never overwrite an existing SolidWorks file.

## Revolved Parts

For bodies of revolution such as cups, mugs, bottles, shafts, flanges, and wheels, do not use the flat-plate builder. Build a task-specific VBScript that:

1. Opens a sketch on the calibrated reference plane.
2. Draws a closed cross-section where X is radial distance from the axis and Y is height, converting millimeters to meters.
3. Adds one `CreateCenterLine` along Y as the revolve axis.
4. Selects only the centerline and calls `FeatureRevolve2` for a full 360-degree revolve.
5. Adds handles, spouts, bosses, or other attachments as additional sketches and merged extrusions.

Reuse the late-bound COM and template-discovery patterns from `scripts/solidworks.vbs`. State wall thickness, capacity, fillets, and tolerances as assumptions unless the user supplies them.

## Simple Plate Plan

Create a JSON file with this shape:

```json
{
  "name": "mounting-plate",
  "shape": "rectangle",
  "length": 120,
  "width": 80,
  "diameter": 0,
  "height": 8,
  "holes": [
    { "x": -48, "y": -28, "diameter": 8 }
  ]
}
```

Use `shape: "circle"` with `diameter` for a circular plate. Coordinates are millimeters from the plate center, with positive X right and positive Y up.

Run:

```powershell
node "<skill-dir>\scripts\build-part.mjs" --plan "<plan.json>" --output "<output.SLDPRT>"
```

The builder validates positive dimensions, edge clearance, overlapping holes, output overwrite, SolidWorks templates, and file creation.

## Batch Part Build

For mechanisms or assemblies containing multiple supported plate parts, create one manifest:

```json
{
  "parts": [
    { "plan": "plans/base.json", "output": "parts/base.SLDPRT" },
    { "plan": "plans/link.json", "output": "parts/link.SLDPRT" }
  ]
}
```

Resolve manifest paths relative to the manifest file. Run exactly once:

```powershell
node "<skill-dir>\scripts\build-batch.mjs" --manifest "<manifest.json>"
```

The batch builder applies the same dimension, edge, overlap, extension, and overwrite checks as the single-part builder, then creates every distinct geometry in one visible SolidWorks session. When multiple plans have identical validated geometry, it builds the first once and copies it to the other requested output paths; every copied file remains a separate `.SLDPRT`. The result reports `builtParts`, `reusedParts`, and `elapsedMs`. Use `elapsedMs` when reporting performance problems.

## Cycloidal Reducer Generator

Create a reference-matched concept reducer in one new output directory:

```powershell
node "<skill-dir>\scripts\generate-cycloidal-reducer.mjs" --output-dir "output/solidworks/reducer-unique" --plan "reducer.json"
```

The default model uses 18 ring pins, two 17-lobe approximation discs, six output pins, an eccentric input cam, transparent covers, 11 unique parts, and 34 assembly components. The generated profile is a visual concept approximation, not a manufacturing cycloid calculation.

The builder uses symmetric two-sided extrusions about each sketch plane. Assembly placement values are therefore part midplanes and remain valid when a template reverses its plane normal or SolidWorks fixes the first inserted component at the origin.

If all 11 parts already exist but assembly creation failed, copy those parts into a new output directory and run:

```powershell
node "<skill-dir>\scripts\generate-cycloidal-reducer.mjs" --output-dir "output/solidworks/reducer-recovery-unique" --plan "reducer.json" --assembly-only
```

Never rebuild completed parts merely to recover an assembly. The command refuses missing parts and refuses to overwrite the assembly or any preview.

## Drawing And Export Workflow

Generate an editable three-view drawing plus PDF and DWG from one model:

```powershell
node "<skill-dir>\scripts\create-drawings.mjs" --model "part.SLDPRT" --output-dir "deliverables" --sheet a3 --dimensions model
```

Options:

- `--sheet a0|a1|a2|a3|a4|a4p` selects the matching `gb_*.drwdot` template; default is `a3`.
- `--dimensions model|none` imports model dimensions or omits them; default is `model`.
- `--name NAME` changes the output base name.
- `--no-pdf` or `--no-dwg` disables an export.

The command refuses to overwrite outputs. It creates the editable `.SLDDRW` batch in one visible SolidWorks session, then reopens each saved drawing in isolated `solidworks-export-one.vbs` calls for PDF/DWG so a translator state change cannot corrupt the next format. `Create3rdAngleViews2` supplies front/top/right views and the drawing template supplies initial view layout. Inspect the result; view crowding, an unsuitable model orientation, or excessive dimensions requires a task-specific drawing revision rather than blind acceptance.

For multiple models, create one manifest and invoke the command once:

```json
{
  "defaults": {
    "outputDir": "deliverables",
    "sheet": "a3",
    "dimensions": "model",
    "pdf": true,
    "dwg": true
  },
  "drawings": [
    { "model": "parts/base.SLDPRT", "name": "base" },
    { "model": "parts/link.SLDPRT", "name": "link", "sheet": "a4" }
  ]
}
```

```powershell
node "<skill-dir>\scripts\create-drawings.mjs" --manifest "drawings.json"
```

Resolve manifest paths relative to the manifest. Use one batch for up to 64 models so template discovery and COM connection happen once. If a requested export translator or drawing template is unavailable, return `FAIL` with the exact SolidWorks error; do not silently omit that deliverable. Do not rename a PDF or DXF to `.DWG`; a DWG is valid only when SolidWorks itself creates it.

### Automatic Dimension Rules

- Use `dimensions: model` only after the model's driving dimensions are meaningful and rebuilt.
- Imported model dimensions are a starting point. Inspect for duplicates, overlaps, off-sheet annotations, missing datums, and missing manufacturing-critical dimensions.
- If the source is an unscaled image, label dimensions based on defaults as assumptions in the drawing notes or companion specification.
- Do not claim a drawing is production-ready until the user supplies or confirms tolerances, datums, fits, materials, finishes, purchased interfaces, and applicable drafting standard.

## Assembly Requirements

For mechanisms such as robotic arms:

- create one part file per replaceable component;
- use stable component names;
- define joint axes and zero pose before placing components;
- keep an interface table with parent, child, joint center, axis, expected face contact, and permitted gap or overlap;
- keep an assembly bill of materials beside the output;
- distinguish fixed, revolute, prismatic, and cosmetic relationships;
- create a concept assembly first, then add detailed motor or bearing interfaces only from confirmed specifications.

Do not silently collapse an assembly request into one decorative solid.

For articulated links, place geometry from confirmed joint centers rather than overall part endpoints. If a hole is inset from the end of a link, position the part using the hole center, not half the outside length. Match clearly visible solid, paired-plate, boxed, or clevis construction from the reference instead of imposing the generic default.

Do not hide a positioning error with unexplained part interference. Use coincident faces or mates when interfaces are known. For concept geometry without specified interfaces, a small declared overlap is acceptable only to express intended attachment and must be listed in the interface table.

## COM Session Reliability

- Keep one visible SolidWorks session where practical.
- After saving and confirming each newly created part, close its standalone document. Reload only the distinct parts required for assembly insertion, then close the task assembly and standalone part documents after previews are saved.
- Before a domain generator starts, count open SolidWorks documents. Refuse a new build when more than 24 documents are already open; ask the user to close or restart SolidWorks instead of pushing into a resource failure.
- Prefer symmetric two-sided extrusions for stacked mechanisms. This makes local part origins usable as midplanes and removes dependence on extrusion sign.
- Treat the first inserted assembly component as fixed at the origin unless a saved preview and component transform prove otherwise. Place all other components relative to that fixed origin.
- Prefer direct assembly insertion by saved path. Use explicit open APIs only when required, and check both the returned object and error code.
- Do not accumulate dozens of open parts across retries. Before retrying after a resource failure, enumerate open documents and close only saved documents located under this task's `output/solidworks/` paths.
- Never close unrelated documents, discard a user's unsaved document, kill SolidWorks, or delete partial outputs to recover resources.
- A COM call failing after several successful parts is not proof of bad geometry. Preserve the partial directory, diagnose the exact stage, and continue in a new unique directory with assembly-only recovery when all expected parts exist.

## Verification Gate

Automation exit code `0` is necessary but not sufficient. Mark the result `COMPLETE` only when every applicable check passes:

1. Every expected `.SLDPRT` and `.SLDASM` exists and is non-empty.
2. The saved assembly reopens, resolves lightweight components, rebuilds, and contains the expected component count.
3. Joint holes and axes use the interface-table coordinates; critical stacked faces have zero declared gap or the declared concept overlap.
4. A fresh full preview shows the complete model at a useful scale.
5. Fresh close-up previews show no background gap at required contacts, no disconnected parts, no unintended center voids, and no obviously incorrect overlap.
6. The final preview is compared directly with every supplied reference image. For a CAD screenshot, verify silhouette, bend directions, component order, joint placement, and visible contact relationships.
7. A stacked circular mechanism has fresh isometric, front, and right previews. The right preview must show no background gap at housing/cover/flange face contacts.
8. Every requested `.SLDDRW`, `.PDF`, and `.DWG` exists and is non-empty.
9. Reopen the `.SLDDRW`; confirm the expected sheet, three model views, useful scale, no off-sheet views, and readable annotations.
10. Inspect the PDF visually and confirm the DWG was exported by SolidWorks. File existence alone does not prove drawing quality.

Use SolidWorks mates, interference/contact tools, body checks, or component bounds when they return reliable data. If a COM geometry-inspection API cannot be read reliably, report that limitation and use explicit construction ranges plus close-up visual evidence; do not claim that the unavailable numeric check passed.

If any check fails, the verdict is `FAIL`: explain the observed mismatch, preserve the failed directory, correct the model in a new unique directory, and repeat the full gate. Never call a model connected merely because intended coordinate ranges touch when the preview shows a gap.

## Safety And Trust

- Do not use `EncodedCommand`, `ExecutionPolicy Bypass`, hidden processes, startup persistence, registry autoruns, or antivirus exclusions.
- Do not request or store API keys.
- Do not overwrite existing CAD files.
- Do not delete or silently replace earlier output directories, including partial failed builds.
- Do not suppress SolidWorks dialogs or licensing errors.
- Do not present concept geometry as verified structural or safety engineering.

## Follow-Up

After a `COMPLETE` concept model, recommend confirming dimensions and purchased-component interfaces before manufacturing detail is added. After a `COMPLETE` drawing export, recommend a drafting review for dimension completeness, tolerances, datums, title-block metadata, and downstream DWG compatibility. Use the final interface table, drawing, and previews as the starting evidence for the next revision.
