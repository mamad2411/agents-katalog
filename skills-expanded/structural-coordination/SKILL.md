---
name: structural-coordination
description: "Coordinate architecture with structural systems at concept through technical design: grids, spans, columns/walls, cores, transfer conditions, openings, floor zones, movement joints, foundations, roof systems and structural interfaces. Use for structural strategy options and architect-engineer coordination, not final engineering design."
---

# Structural Coordination

Support multidisciplinary coordination while keeping structural calculations and capacity decisions with qualified structural engineers.

## Preflight

- Structural engineer inputs if available, building geometry/use, grids, floor-to-floor heights, major spans, cores, basements, material/system preferences and site/geotechnical constraints.
- Known transfer zones, cantilevers, large openings, facade/support conditions, plant loads and movement/seismic/wind considerations.

Keep verified facts, project assumptions, design options, and unresolved questions visibly separate. If a required input is absent, record it as `UNKNOWN` rather than inventing it.

## Workflow

1. Map architectural constraints to a plausible structural grid/system and identify where geometry creates transfers or discontinuities.
2. Coordinate columns/walls/cores with rooms, facades, parking, circulation, risers and openings across levels.
3. Reserve structural depths and movement/connection zones in sections; flag long spans, cantilevers, penetrations and load-sensitive uses.
4. Prepare a decision/request matrix for the structural engineer and update architecture only from confirmed structural information.

## Deliverables

- Grid/system option matrix
- Structural coordination overlays/sections
- Openings/transfer/interface register
- Engineer question/decision log

## Verification

- Grids and vertical elements align across levels; major penetrations and floor/roof zones are coordinated.
- All capacity/span/load statements are labelled conceptual unless engineer-verified.

For file/model changes, compare the result against a pre-change baseline and report changed items, skipped items, failures, and checks actually run.

## Professional boundaries

- Do not size structural members for construction or claim adequacy.
- Do not provide signed/stamped engineering or substitute for structural analysis.

If a live CAD/BIM/GIS/analysis tool or MCP integration is available, inspect the current document/model and tool version before write operations. Prefer read-only inspection, dry runs, bounded samples, new output paths, and native undo/transaction mechanisms. Never claim a model or drawing was changed unless the tool confirms it.

If the native application is unavailable, produce a reproducible plan, script, structured data, SVG/DXF artifact, or exact in-application procedure instead of pretending to have operated the software.
