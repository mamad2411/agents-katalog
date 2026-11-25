---
name: ifc-query
description: Reads IFC (openBIM) models read-only with IfcOpenShell, or the official IfcOpenShell MCP server run with --no-execute, to answer model questions with counts taken from the model. Produces summaries, door, window, space and wall schedules, property-set completeness checks, and quantity totals by storey, always reporting the schema, the exact query and how many elements lacked a value, never estimates. Use when the architect wants to "check the IFC", "door schedule from the model", "how many windows", "which walls have no fire rating", "model QA before issue", "quantities from the IFC", "property set audit", "BIM coordination check", or to understand a consultant's model. Hands to area-check for space areas against the brief, carbon-estimate for quantities into embodied carbon, and revit-mcp or the authoring tool to fix what it finds.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# IFC Query

Ask the model, not the model's author. This skill opens an IFC file, runs a stated query and reports what is actually there: how many, which ones, which are missing data. It never estimates a count or fills an empty property.

## When to use

- Model QA before issuing to a consultant or contractor: are the required properties filled in?
- Schedules (doors, windows, spaces, walls) straight from the model, when the authoring tool isn't to hand.
- Understanding a model someone else sent: what's in it, how it's organised, what's missing.
- Quantities for a cost or carbon check, with the gaps stated.

## Input

- An **IFC file** (IFC2X3, IFC4 or IFC4X3). Ask which tool exported it and roughly when. Export settings drive what's inside.
- A **question**, which becomes a selector query. For QA, a **list of required properties**: an information requirement (EIR or OIR), a BIM execution plan, a national annex or the office standard. If the architect has none, propose a short list and label it as a proposal.

## Process

1. **Start with `summary`** to get the schema, units, class counts, storeys, spaces with quantities, and elements without types.
   `uv run scripts/ifc_query.py model.ifc summary`
2. **Turn the question into a selector query** and run the matching command:
   - `schedule "IfcDoor" --props "Name,type,storey,Pset_DoorCommon.FireRating,Qto_DoorBaseQuantities.Width" --csv doors.csv`
   - `gaps "IfcWall" --require "Pset_WallCommon.FireRating,Pset_WallCommon.IsExternal,Pset_WallCommon.LoadBearing"`
   - `qto "IfcSlab" --quantity "Qto_SlabBaseQuantities.NetVolume"`
   - Filtered: `schedule "IfcWall, Pset_WallCommon.IsExternal=TRUE" --props "Name,Qto_WallBaseQuantities.NetSideArea"`
3. **Quote the output's own numbers**: matched count, empty values, and elements without a quantity. Put the query string in the answer so anyone can re-run it.
4. **If the IfcOpenShell MCP server is connected** (`ifcmcp`, from the IfcOpenShell project), you can use its query and select tools in place of the script. Run it with `--no-execute` so the agent cannot execute arbitrary Python against the model, and keep it read-only unless the architect explicitly asks for an edit. Even then, write to a copy. See [references/tool-notes.md](references/tool-notes.md).
5. **Report findings as a punch list** the model author can act on: GlobalId, Name, what's missing.

## Domain knowledge

- **Schemas differ.** IFC2X3 is still the commonest export. IFC4 added and renamed property sets and quantities. IFC4X3 adds infrastructure. A property can exist in one schema and not another, so always state the schema next to the result.
- **Psets and Qtos.** Property sets (`Pset_*`) hold declared data such as fire rating, load bearing, external or acoustic rating. Quantity sets (`Qto_*`) hold measured values such as length, area, volume or width. Standard `Pset_`/`Qto_` names are defined by buildingSMART. Custom sets (often prefixed with the tool or office name) are common, so look at what the summary shows before writing queries.
- **A property in the model is not a verified property.** `FireRating = "REI 60"` means somebody typed it. It doesn't mean the element achieves it. Report it as "declared in the model".
- **Quantities depend on export settings.** Revit, Archicad and others compute `Qto_` values on export if asked to, and their methods differ (with or without openings, net or gross). The `qto` command sums only elements that carry the value and says how many didn't.
- **Units.** The summary prints the length unit scale. Area and volume quantities are in the project's area and volume units. Check them before converting.
- **Elements without types**, unnamed elements, and elements not contained in a storey are common QA findings. They break schedules downstream.
- **Federated models.** Architecture, structure and MEP usually arrive as separate IFCs. Run each one. Don't merge counts across disciplines without saying so.

## Output format

```
## IFC query: [file], [schema], exported from [tool] (as stated)

Query: "IfcWall, Pset_WallCommon.IsExternal=TRUE"  |  Matched: 214 elements

| GlobalId | Name | Storey | FireRating (declared) | NetSideArea |
|---|---|---|---|---|

Gaps: FireRating empty on 37 of 214 (17%), listed in walls_gaps.csv
Quantity: NetSideArea sum 3,412.5 m2 over 209 walls; 5 walls have no value and are not included

Actions for the model author:
1. [GlobalId / Name]: [what to fix]
```

When results feed fire, acoustic, structural, cost or carbon decisions, end with:

```markdown
> **Disclaimer:** AI-generated analysis for preliminary purposes only. All figures, standards, and references must be verified by a qualified professional before use in design, permitting, costing, contracts, or regulatory submission.
<!-- architect:requires-disclaimer -->
```

Copy the disclaimer exactly as shown, including the `<!-- architect:requires-disclaimer -->` line. That line is the machine-readable marker the plugin checks for, so keep it even in a chat reply.

## What you don't do

- Don't estimate, extrapolate or round away a count. If the query returned 214, say 214.
- Don't treat a declared property as verified performance. Fire, acoustic and structural values need confirmation by the responsible consultant.
- Don't write to the model. This skill is read-only; edits belong in the authoring tool (see `revit-mcp` or the tool's own MCP).
- Don't enable arbitrary code execution on an MCP server to answer a question a query can answer.
