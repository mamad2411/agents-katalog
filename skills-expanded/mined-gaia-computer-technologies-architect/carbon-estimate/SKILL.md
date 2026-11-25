---
name: carbon-estimate
description: Produce an early-stage embodied carbon estimate (A1-A3 product stage by default; A4-A5, B, or C only when the factors cover them) from material quantities, with every emission factor cited (ICE database version, EPD number and URL, or EC3 with attribution), units checked, scopes never mixed, and the result compared against a cited target labelled as a target, not a requirement. Ships a script that refuses to total uncited or unit-mismatched lines. Use when the architect wants "embodied carbon", "carbon estimate", "kgCO2e per m2", "compare the carbon of timber vs concrete", "whole-life carbon early stage", "LETI / RIBA 2030 target check", or "which elements drive the carbon". Takes quantities from ifc-query, area-check, or massing-study; hands to material-palette and spec-writer for lower-carbon alternatives.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Carbon estimate

An early carbon estimate is useful for one thing: showing which decisions matter, while they are still cheap to change. It is only useful if every number can be traced. A total built from remembered factors is worse than no total.

## When to use

- Concept or feasibility: compare structural or envelope options by embodied carbon.
- A client or brief sets a carbon target and the team wants an early read.
- Finding the hotspots: which elements drive most of the total.

This is not a whole-life carbon assessment to a standard (e.g. EN 15978, the RICS professional standard, a national method such as the Dutch MPG or French RE2020). Those need a qualified assessor and specified tools. Say so if that's what the project actually needs.

## Input

- **Quantities**, by element and material, with units: from a model (`ifc-query`), an area schedule plus assumed build-ups (`area-check`), or `massing-study`. State where each came from.
- **Emission factors**, each with a citation. Acceptable sources, in order of preference for early stage:
  1. Product-specific EPDs (EN 15804 or ISO 21930), with the EPD number and URL.
  2. A named generic database and version (e.g. ICE, the Inventory of Carbon and Energy, with its version number; national databases such as the Dutch NMD or the French INIES; the project's local equivalent).
  3. EC3 (Building Transparency): their API terms require notifying them before integrating, and attribution.
  If the architect has no factors, **ask for them or search for them with the source shown.** Do not supply factors from memory.
- GIA (or the area basis the target uses).
- The target, if any, with its source, version, scope, and which building elements it covers.

## Process

1. **Fix the scope.** Default A1-A3. Use a wider scope only if every factor covers it. State the scope in the first line of the output.
2. **Check coverage.** List which building elements are included (substructure, frame, upper floors, roof, envelope, internal walls, finishes, services). Missing elements make the total look better than it is. Say which are missing.
3. **Build two CSVs** (quantities, factors) and run [scripts/carbon_estimate.py](scripts/carbon_estimate.py):
   `uv run scripts/carbon_estimate.py quantities.csv factors.csv --gia 1500 --benchmark <value> --benchmark-source "<source, version, scope>"`
   The script refuses if a factor has no source, units don't match (it converts m3 to kg only with a cited density), or scopes differ. Fix the input. Never work around a refusal.
4. **Report hotspots,** the top three lines by share, and what decision each one depends on.
5. **Compare options** by running the script once per option with identical coverage and scope. Compare like with like only.
6. **Compare to target** only when the target's scope and element coverage match the estimate's. If they don't match, say the comparison is indicative and why.

## Domain knowledge

- **Declared units differ.** Concrete is often per m3, steel and timber per kg, insulation per m2 at a stated thickness and R-value. Mixing them silently is the classic error. That's why the script checks units.
- **Biogenic carbon:** timber stores carbon. Many methods report sequestration separately (module A1 as a negative, balanced at end of life in module C). Don't net it off against the total unless the chosen method says to, and say which convention you used.
- **Factor ranges are wide.** Concrete varies widely with cement content and replacement; steel varies with recycled content and production route. Report the factor's source mix, and give a low/high run where the choice of factor drives the answer.
- **Targets are not requirements** unless a regulation or contract makes them so. RIBA 2030 Climate Challenge, LETI, and national limits each use different scopes and boundaries. Name the version.

## Output format

```
## Embodied carbon estimate: [project / option]

**Scope:** [A1-A3] · **Area basis:** [GIA m2, source] · **Coverage:** [elements included] · **Missing:** [elements excluded]

| Element | Material | Quantity | Factor (source) | kgCO2e | Share |
|---|---|---|---|---|---|

**Total:** [x] tCO2e · **Intensity:** [y] kgCO2e/m2 GIA ([scope])
**Hotspots:** [top 3 and the decision each depends on]
**Against target:** [target value, source, version, scope] -> [above/below by z], [like-for-like / indicative because ...]
**Biogenic carbon:** [reported separately / excluded, and why]
**Sensitivity:** [low/high run if a factor choice drives the result]

> **Disclaimer:** AI-generated analysis for preliminary purposes only. All figures, standards, and references must be verified by a qualified professional before use in design, permitting, costing, contracts, or regulatory submission.
<!-- architect:requires-disclaimer -->
```

Copy the disclaimer exactly as shown, including the `<!-- architect:requires-disclaimer -->` line. That line is the machine-readable marker the plugin checks for, so keep it even in a chat reply.

## What you don't do

- Don't use an emission factor without a citation. Not even "a typical value". Ask or search, and show the source.
- Don't mix life-cycle scopes or declared units in one total.
- Don't call a target a requirement, or say a scheme "meets" a regulation's carbon limit. "Below the stated target on this coverage and scope (verify)" is the claim.
- Don't present this as a compliant whole-life carbon assessment.
