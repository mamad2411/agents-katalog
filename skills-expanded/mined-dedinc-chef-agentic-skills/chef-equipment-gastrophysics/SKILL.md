---
name: chef-equipment-gastrophysics
description: >-
  Appliance and food-science authority for sous vide, pressure/multicookers,
  air fryers, slow cookers, microwaves, convection ovens and blenders, plus
  heat transfer, Maillard browning, emulsions and starch/protein behavior. Use
  for appliance conversions, device-specific recipes and "why does this work".
---

# Chef Equipment & Gastrophysics

An appliance is a heat-transfer profile plus manufacturer limits. Convert the **function** of a technique, not just its clock time.

Read `references/appliance-playbook.md` for conversion patterns and device-specific safety gates.

## Conversion protocol

Identify what the original step must achieve: crust, evaporation, pasteurization, collagen conversion, gentle coagulation or simple reheating. Map each function to the target device and keep functions that the target cannot perform as a separate step.

Manufacturer limits win for pressure-cooker minimum liquid, maximum fill, blender hot-liquid handling and microwave-safe containers. Do not invent a universal minimum or a workaround that contradicts the manual.

## Sous vide

Separate **bath temperature**, **time for the food center to heat**, **pasteurization hold**, **food thickness/start temperature**, and **texture time**. Never claim that a bath setting plus a generic clock automatically makes poultry/ground food safe. For safety-critical low-temperature cooking, use a complete applicable source; otherwise offer the conventional safe-minimum-temperature path.

## Blender

Hot-liquid handling is model-specific. If the manufacturer prohibits hot liquids in a sealed jar, cool the contents or use a suitable immersion/vented system; do not prescribe "crack the lid" as a universal hack.

## Slow cooker and dry kidney beans

Do not cook raw dry red kidney beans directly from dry/soaked state in a slow cooker. Use the separate boil treatment in `chef-grains-legumes-guide` or canned beans before slow cooking.

## Gastrophysics core

- Browning needs a sufficiently hot, relatively dry surface and room for steam to escape.
- Protein texture depends on temperature and time, but culinary denaturation points are not automatically regulatory safety endpoints.
- Reduction concentrates salt and flavor; season with the final concentration in mind.
- Emulsions are droplets + emulsifier + shear; coagulated protein may not be reversible even when a separated emulsion is.
- Starch thickening depends on starch type, water, heat, acid, sugar and shear.

Use the simplest device that produces the requested effect. Fancy equipment is optional; safety controls are not.
