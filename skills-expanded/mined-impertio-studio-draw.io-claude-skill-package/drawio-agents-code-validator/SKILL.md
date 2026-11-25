---
name: drawio-agents-code-validator
description: >
  Use when validating Draw.io mxGraph XML for correctness before presenting to
  the user or saving to a file. Runs an 8-stage validation pipeline from XML
  well-formedness to perimeter consistency. Prevents delivering broken diagrams
  by catching structural, style, and geometry errors before output.
  Keywords: validate diagram, check XML, verify mxGraph, validation pipeline,
  diagram quality, diagram broken, fix diagram, check Draw.io file,
  diagram not rendering correctly.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io Code Validator

## Purpose

This skill defines an 8-stage validation pipeline for Draw.io mxGraph XML. Run this pipeline on EVERY diagram before presenting it to the user or saving it to a file. The pipeline catches structural, style, and geometry errors in order of severity — blocking errors first, warnings second.

## Critical Rules (Memorize These)

1. **ALWAYS run ALL 8 stages** — NEVER skip a stage, even if earlier stages pass.
2. **Stages 1-4 are BLOCKING** — If ANY stage from 1 to 4 fails, STOP and fix before continuing. NEVER deliver XML that fails a blocking stage.
3. **Stages 5-8 produce WARNINGS** — Fix these when possible, but they do NOT block delivery.
4. **ALWAYS report errors in severity order** — BLOCKING errors first, then WARNINGS.
5. **ALWAYS provide a fix for each error** — NEVER report an error without its correction.
6. **NEVER silently fix errors** — Report what was found AND what was corrected.
7. **ALWAYS validate the COMPLETE file** — NEVER validate a partial snippet and assume the rest is correct.

## Pipeline Overview

```
Stage 1: XML Well-Formedness .......... BLOCKING
Stage 2: Structure Check .............. BLOCKING
Stage 3: ID Uniqueness ................ BLOCKING
Stage 4: Parent-Child Integrity ....... BLOCKING
Stage 5: Style Validation ............. WARNING
Stage 6: Geometry Check ............... WARNING
Stage 7: Connection Validation ........ WARNING
Stage 8: Perimeter Check .............. WARNING
```

If Stage 1 fails, Stages 2-8 CANNOT run (no parseable tree).
If Stage 2 fails, Stages 4-8 produce unreliable results.
Stages 3-8 are independent of each other and ALWAYS run regardless of other warning-stage results.

---

## Stage 1: XML Well-Formedness (BLOCKING)

**What:** Verify the XML document is syntactically valid.

**Checks:**

| # | Check | Pass Criteria |
|---|-------|---------------|
| 1.1 | Tag closure | Every `<mxCell>`, `<mxGeometry>`, `<mxPoint>` is self-closed (`/>`) or has a matching close tag |
| 1.2 | Nesting | Tags are properly nested: `mxfile > diagram > mxGraphModel > root > mxCell` |
| 1.3 | Attribute quoting | Every attribute value is enclosed in double quotes |
| 1.4 | Special characters | No raw `<`, `>`, `&` in attribute values (MUST be `&lt;`, `&gt;`, `&amp;`) |
| 1.5 | No compressed content | No Base64 text inside `<diagram>` elements — ALWAYS `<mxGraphModel>` directly |

**On Failure:** STOP pipeline. Report the exact location (tag name, approximate position) and the fix.

**Auto-Fix Capabilities:**
- Add missing self-close slash (`>` to `/>` on childless elements)
- Escape unescaped `&` to `&amp;` in attribute values
- Remove fabricated Base64 content and replace with empty `<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/></root></mxGraphModel>`

---

## Stage 2: Structure Check (BLOCKING)

**What:** Verify the mandatory mxGraph document structure exists.

**Checks:**

| # | Check | Pass Criteria |
|---|-------|---------------|
| 2.1 | Root cell | `<mxCell id="0"/>` exists as a direct child of `<root>` |
| 2.2 | Default layer | `<mxCell id="1" parent="0"/>` exists as a direct child of `<root>` |
| 2.3 | Root cell purity | Cell id="0" has NO `parent`, `vertex`, `edge`, or `style` attributes |
| 2.4 | Layer purity | Cell id="1" has `parent="0"` and NO `vertex`, `edge`, or `style` attributes |
| 2.5 | Document wrapper | `<mxGraphModel>` exists and contains `<root>` |
| 2.6 | Content ordering | id="0" appears BEFORE id="1" in document order |

**On Failure:** STOP pipeline. Insert missing structural cells.

**Auto-Fix Capabilities:**
- Insert `<mxCell id="0"/>` if missing
- Insert `<mxCell id="1" parent="0"/>` if missing
- Remove illegal attributes from structural cells
- Wrap bare `<root>` in `<mxGraphModel>`

---

## Stage 3: ID Uniqueness (BLOCKING)

**What:** Verify every cell has a unique identifier.

**Checks:**

| # | Check | Pass Criteria |
|---|-------|---------------|
| 3.1 | No duplicate IDs | Every `id` attribute value appears exactly once across ALL `<mxCell>`, `<object>`, and `<UserObject>` elements |
| 3.2 | Cross-page uniqueness | IDs are unique across ALL `<diagram>` pages in the file |
| 3.3 | Reserved IDs | Only the structural cells use id="0" and id="1" |
| 3.4 | Non-empty IDs | No cell has an empty `id=""` attribute |

**On Failure:** STOP pipeline. Report every duplicate pair with their cell values/labels for identification.

**Auto-Fix Capabilities:**
- Reassign duplicate IDs to new unique values (sequential integers starting from max existing ID + 1)
- Update all `parent`, `source`, and `target` references that pointed to the reassigned ID
- NEVER reassign id="0" or id="1"

---

## Stage 4: Parent-Child Integrity (BLOCKING)

**What:** Verify every parent reference resolves to an existing cell.

**Checks:**

| # | Check | Pass Criteria |
|---|-------|---------------|
| 4.1 | Parent exists | Every `parent` attribute value matches an existing cell's `id` |
| 4.2 | No circular refs | No cell is its own parent (directly or through a chain) |
| 4.3 | Layer parenting | All content cells have `parent="1"` or reference a valid group/container cell |
| 4.4 | Orphan detection | No cell (except id="0") lacks a `parent` attribute |

**On Failure:** STOP pipeline. Report each broken reference with the orphaned cell's ID and value.

**Auto-Fix Capabilities:**
- Set `parent="1"` on orphaned cells (assigns them to the default layer)
- Break circular references by resetting the child's parent to "1"

---

## Stage 5: Style Validation (WARNING)

**What:** Verify style strings use correct syntax, known properties, and valid values.

**Checks:**

| # | Check | Pass Criteria |
|---|-------|---------------|
| 5.1 | Semicolon separation | Properties separated by `;` with no spaces around `=` |
| 5.2 | Known properties | All property names are recognized Draw.io style properties |
| 5.3 | Valid values | Boolean properties use `1`/`0` (NEVER `true`/`false`) |
| 5.4 | html=1 present | Every vertex and edge style contains `html=1` |
| 5.5 | whiteSpace=wrap | Every vertex with a `value` (label) contains `whiteSpace=wrap` |
| 5.6 | Valid shape names | Every `shape=` value references a real Draw.io shape |
| 5.7 | No vertex styles on edges | `fillColor`, `container`, `swimlane` NOT on edge cells |
| 5.8 | No edge styles on vertices | `edgeStyle`, `startArrow`, `endArrow`, `curved` NOT on vertex cells |

**Known Style Properties (non-exhaustive — common ones):**
```
fillColor, strokeColor, fontColor, fontSize, fontFamily, fontStyle,
rounded, dashed, shadow, opacity, html, whiteSpace, align, verticalAlign,
overflow, container, collapsible, swimlane, startSize, endSize,
shape, perimeter, arcSize, spacing, spacingTop, spacingBottom,
spacingLeft, spacingRight, labelPosition, verticalLabelPosition,
edgeStyle, startArrow, endArrow, startFill, endFill, curved,
jettySize, orthogonalLoop, exitX, exitY, exitDx, exitDy,
entryX, entryY, entryDx, entryDy, sourcePerimeterSpacing,
targetPerimeterSpacing, strokeWidth, rotation, direction,
gradientColor, gradientDirection, glass, sketch, comic,
jumpStyle, jumpSize, fixedSize, resizable, movable, deletable,
connectable, noLabel, imageWidth, imageHeight, image, aspect
```

**Valid Shape Names (built-in):**
```
rectangle, ellipse, rhombus, triangle, hexagon, cylinder, cylinder3,
cloud, actor, swimlane, line, image, document, parallelogram, step,
trapezoid, process, callout, note, cross, plus, card, umlLifeline,
folder, internalStorage, manualInput, delay, display, merge, or,
offPageConnector, tape, tapeData, sumEllipse, sortShape, collate,
doubleEllipse, singleArrow, doubleArrow, curlyBracket, link
```

Shapes starting with `shape=mxgraph.` are valid stencil library references.

**Auto-Fix Capabilities:**
- Add `html=1;` to styles missing it
- Add `whiteSpace=wrap;` to vertex styles missing it
- Replace `true`/`false` with `1`/`0` in boolean properties
- Remove spaces around `=` in style properties

---

## Stage 6: Geometry Check (WARNING)

**What:** Verify geometry attributes are correct for the cell type.

**Checks:**

| # | Check | Pass Criteria |
|---|-------|---------------|
| 6.1 | Vertex dimensions | Every vertex has `<mxGeometry>` with `width` > 0 and `height` > 0 |
| 6.2 | Edge relative | Every edge `<mxGeometry>` has `relative="1"` |
| 6.3 | Geometry as-attribute | Every `<mxGeometry>` has `as="geometry"` |
| 6.4 | Non-negative dimensions | No negative `width` or `height` values |
| 6.5 | Reasonable dimensions | Width and height are between 10 and 2000 (warn if outside) |
| 6.6 | Group child coords | Children of containers use coordinates relative to parent (small offsets, not absolute canvas positions) |
| 6.7 | mxPoint validity | Every `<mxPoint>` has numeric `x` and `y` attributes |

**Auto-Fix Capabilities:**
- Add `relative="1"` to edge geometries missing it
- Add `as="geometry"` to `<mxGeometry>` elements missing it
- Set minimum width/height of 40x40 for vertices with missing or zero dimensions

---

## Stage 7: Connection Validation (WARNING)

**What:** Verify edges connect to valid cells with correct routing.

**Checks:**

| # | Check | Pass Criteria |
|---|-------|---------------|
| 7.1 | Source exists | Every edge `source` attribute references an existing vertex |
| 7.2 | Target exists | Every edge `target` attribute references an existing vertex |
| 7.3 | No self-loops | No edge has `source` equal to `target` (unless intentional) |
| 7.4 | Edge has endpoints | Every `edge="1"` cell has both `source` and `target` OR has explicit `<mxPoint>` waypoints |
| 7.5 | Valid edge style | `edgeStyle` value is a recognized routing algorithm |
| 7.6 | Arrow configuration | `endArrow`/`startArrow` values are valid names |

**Valid Edge Styles:**
```
orthogonalEdgeStyle, elbowEdgeStyle, entityRelationEdgeStyle,
isometricEdgeStyle, segmentEdgeStyle, straightEdgeStyle (not a real value — omit edgeStyle for straight)
```

**Valid Arrow Names:**
```
classic, block, open, oval, diamond, diamondThin, box,
halfCircle, dash, cross, circlePlus, circle, ERone,
ERmany, ERmanyToMany, ERoneToMany, ERzeroToMany,
ERzeroToOne, ERoneToOne, none
```

**Auto-Fix Capabilities:**
- Remove `source`/`target` attributes that reference non-existent cells
- Add `endArrow=classic` to edges missing arrow configuration

---

## Stage 8: Perimeter Check (WARNING)

**What:** Verify that shape perimeters match their shape types for correct edge connection points.

**Checks:**

| # | Check | Pass Criteria |
|---|-------|---------------|
| 8.1 | Perimeter matches shape | The `perimeter` style property matches the shape type |
| 8.2 | Explicit perimeter | Shapes that are NOT rectangles MUST have an explicit `perimeter` |

**Shape-to-Perimeter Mapping:**

| Shape | Required Perimeter |
|-------|-------------------|
| rectangle / rounded | `rectanglePerimeter` (default — omission OK) |
| ellipse | `ellipsePerimeter` |
| rhombus | `rhombusPerimeter` |
| triangle | `trianglePerimeter` |
| hexagon | `hexagonPerimeter` |
| cloud | `ellipsePerimeter` |
| cylinder / cylinder3 | `rectanglePerimeter` (default — omission OK) |
| parallelogram | `parallelogramPerimeter` |
| trapezoid | `trapezoidPerimeter` |
| swimlane | `rectanglePerimeter` (default — omission OK) |

**Auto-Fix Capabilities:**
- Add the correct `perimeter=` property based on the shape type
- Remove mismatched perimeter values and replace with the correct one

---

## Error Report Format

ALWAYS report validation results using this structure:

```
VALIDATION RESULT: [PASS | FAIL]

BLOCKING ERRORS (must fix):
  [S1-E1] Stage 1 — XML Well-Formedness
    Severity: BLOCKING
    Location: <mxCell id="5" ...>
    Error: Unclosed tag — missing self-close slash
    Fix: Change <mxCell id="5" value="Test"> to <mxCell id="5" value="Test" />

  [S4-E1] Stage 4 — Parent-Child Integrity
    Severity: BLOCKING
    Location: <mxCell id="7" parent="99" ...>
    Error: Parent "99" does not exist
    Fix: Change parent="99" to parent="1"

WARNINGS (should fix):
  [S5-W1] Stage 5 — Style Validation
    Severity: WARNING
    Location: <mxCell id="3" style="rounded=1;" ...>
    Error: Missing html=1 in style
    Fix: Change style to "rounded=1;html=1;"

  [S8-W1] Stage 8 — Perimeter Check
    Severity: WARNING
    Location: <mxCell id="4" style="ellipse;html=1;" ...>
    Error: Ellipse shape missing ellipsePerimeter
    Fix: Change style to "ellipse;html=1;perimeter=ellipsePerimeter;"

SUMMARY: 2 blocking errors, 2 warnings
AUTO-FIXED: [list of auto-applied fixes, if any]
```

---

## Validation Decision Tree

```
START
  |
  v
[Stage 1: XML Well-Formedness]
  FAIL --> Report BLOCKING errors --> Attempt auto-fix --> Re-run Stage 1
           STILL FAIL --> STOP. Report "XML is unparseable. Manual fix required."
  PASS
  |
  v
[Stage 2: Structure Check]
  FAIL --> Report BLOCKING errors --> Auto-fix (insert structural cells) --> Re-run Stage 2
           STILL FAIL --> STOP. Report structural errors.
  PASS
  |
  v
[Stage 3: ID Uniqueness]
  FAIL --> Report BLOCKING errors --> Auto-fix (reassign IDs) --> Re-run Stage 3
  PASS
  |
  v
[Stage 4: Parent-Child Integrity]
  FAIL --> Report BLOCKING errors --> Auto-fix (reset orphans to parent="1") --> Re-run Stage 4
  PASS
  |
  v
[Stage 5: Style Validation]       -- runs regardless of Stage 6-8 results
[Stage 6: Geometry Check]          -- runs regardless of Stage 5,7-8 results
[Stage 7: Connection Validation]   -- runs regardless of Stage 5-6,8 results
[Stage 8: Perimeter Check]         -- runs regardless of Stage 5-7 results
  |
  Collect all WARNINGS
  |
  v
[Generate Report]
  BLOCKING errors found?
    YES --> Overall: FAIL. Apply auto-fixes and re-validate.
    NO  --> Overall: PASS (with warnings if any).
```

---

## Integration with Related Skills

- **drawio-errors-xml** — Provides the detailed error catalog (E-001 through E-019) referenced by this validator. When this pipeline detects an error, reference the corresponding E-code from that skill.
- **drawio-errors-rendering** — Covers visual rendering issues that occur AFTER XML is structurally valid. Stage 5 and Stage 8 of this pipeline catch many rendering issues at the XML level.
- **drawio-core-xml-format** — Defines the expected XML structure that Stage 1 and Stage 2 validate against.
- **drawio-syntax-styles** — Defines the valid style properties and values that Stage 5 validates against.
- **drawio-syntax-connections** — Defines edge connection patterns that Stage 7 validates against.

---

## Quick Reference: Minimum Valid XML

ALWAYS validate against this minimum structure:

```xml
<mxfile compressed="false">
  <diagram id="page-1" name="Page-1">
    <mxGraphModel>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- content cells here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Every content cell MUST have:
- A unique `id` attribute
- A `parent` attribute referencing an existing cell
- Either `vertex="1"` or `edge="1"`
- A `style` attribute containing at minimum `html=1`
- A child `<mxGeometry as="geometry" ... />` element

## Reference Links

- [Complete Reference](references/methods.md)
- [Working Examples](references/examples.md)
- [Anti-Patterns](references/anti-patterns.md)
