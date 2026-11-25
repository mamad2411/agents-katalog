---
name: cartographic-design
description: "Design maps people can read: projection and scale choice, visual hierarchy, colour for classification, typography, generalization, legend and accessibility."
type: procedural
category: geospatial
domain: geospatial
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - map design principles
  - map colour palette classification
  - map label placement
  - map generalization scale
  - accessible map design
keywords:
  - cartography
  - map-design
  - legend
  - colour
  - typography
  - generalization
source: custom
enabled: true
---

# Cartographic Design

## Purpose

Design maps people can read: projection and scale choice, visual hierarchy, colour for classification, typography, generalization, legend and accessibility.

## When to Use

- A map must communicate a decision to a non-specialist audience.
- The current map is cluttered, misleading or unreadable at print size.
- Colour or classification choices could distort the data's story.

## When NOT to Use

- The output is an analysis artifact only you will read.
- The task is purely technical data conversion.
- No map is needed at all — a table or chart communicates better.

## Capabilities

- Choose projection, scale and extent that fit the message.
- Build a visual hierarchy with restrained colour and weight.
- Classify data honestly (quantiles vs equal interval vs natural breaks).
- Place labels and legends that survive print and small screens.

## Inputs

- The map's single message and its audience.
- The data's distribution and the classification question it implies.
- Output medium: A4 print, slide, mobile screen or dashboard panel.

## Workflow

1. Write the one-sentence message before choosing any symbol.
2. Pick the projection for the purpose (equal-area for density, conformal for navigation).
3. Classify with a method that matches the distribution and state it in the legend.
4. Apply a limited palette with colour-blind-safe sequential/diverging ramps.
5. Print at final size and check every label, then test with a colleague unfamiliar with the data.

## Tools

- QGIS/Illustrator for composition
- ColorBrewer / viridis ramps
- accessibility contrast checkers

## Examples

- `qgis_process run native:savefeatures -- INPUT=classified.gpkg OUTPUT=export.geojson`
- `allskills explain geospatial.cartographic-design --query "choose map colours"`
- `allskills route "make this map readable for the board"`

## Safety

- Truncating a colour ramp at a data threshold hides outliers — annotate instead.
- Red-green classification excludes colour-blind readers; use shape or labels too.
- Choropleths of raw counts mislead when populations differ; normalize first.

## Source

All-Skills canonical library (`skills/geospatial/cartographic-design`). First-party skill, maintained in this repository.

## Notes

- Fewer classes read better than many; three to five is usually enough.
- The legend is part of the analysis: state the classification method and units.
- Pairs with: `geospatial/qgis-map-production`, `design/ui-ux`.
