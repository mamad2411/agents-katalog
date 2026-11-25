---
name: "set-material"
description: "Assign a library material (steel, aluminum, etc.) to the open SolidWorks part's active configuration through the SolidWorks API tools. Use this whenever the user asks to set, change, apply or assign a material on a part, including casual phrasing like \"make this part steel\" or \"set plain steel\", even if they don't say \"material\"."
---

# Set material on a SolidWorks part

Works on the active part document. Assemblies are not covered: material is set on each part, so open the part first. Lengths on tools are meters; angles are radians.

## Steps

`model` change action `material`, with the exact library name from the table. The change read-back is the name that landed; a missing name fails silently, so stop when the read-back is not that name.

## Mapping names
The library uses its own names, which differ from EN/DIN/ISO designations. Names that failed silently in a real run, and the library names that worked:

| Wanted | Failed (not in library) | Worked |
|---|---|---|
| Plain carbon steel | - | `Plain Carbon Steel` |
| 42CrMo4 / 1.7225 / AISI 4140 | `1.7225 (42CrMo4)`, `AISI 4140` | nearest: `AISI 4340 Steel, normalized` or `Alloy Steel` |
| C45 / 1045 | - | `AISI 1045 Steel, cold drawn` |
| EN-GJL-250 grey cast iron | - | `Gray Cast Iron` |
| NBR / elastomer (seals) | - | `Rubber` |

Libraries differ between installs, so treat this as a starting point. When the exact grade isn't in the library, use the nearest one with a similar density and stiffness, and record the real specified material in the part's custom properties (and the BOM), e.g. `Material_Spec = 42CrMo4 QT (EN 10083-3)`; the library material only drives mass and appearance.

## Check

When the body must be judged, `mass_properties`: Mass ÷ Volume should equal the material's density (Plain Carbon Steel: 7,800 kg/m³; alloy steels about 7,850; grey cast iron about 7,200). A density of 1,000 kg/m³ means no material was applied.

If the check fails, stop and name the step that failed, then try the nearest library name. Do not search the API.

## Avoid

- Don't read the material back with `invoke` → `GetMaterialPropertyName2`. Its second parameter is a `ref string`, which `invoke` can't pass, so the call fails with DISP_E_TYPEMISMATCH.
- Setting the material doesn't save the file. Save only if the user asks, or as part of a build that saves each part.