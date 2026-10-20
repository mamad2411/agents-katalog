---

name: api-versioning-visualization-pattern
description: Multi-view composition for rendering API version lifecycles, schema diffs, and traffic splits side-by-side
category: design
triggers:
  - api versioning visualization pattern
tags: [design, api, versioning, visualization, schema]
version: 1.0.0
---

# api-versioning-visualization-pattern

API versioning dashboards benefit from a three-panel composition: a **timeline lane** showing version states (alpha → beta → stable → deprecated → sunset) plotted against absolute dates with lifecycle-colored bars, a **diff viewer** rendering schema/endpoint changes between two selected versions using unified or split layout with syntax-aware highlighting (added in green, removed in red, modified in amber), and a **traffic distribution** view (stacked area or Sankey) showing per-version request share over time. Each panel is driven by the same `selectedVersionPair` state so that hovering a date on the timeline pins the diff and the traffic cursor simultaneously.

Use lifecycle color tokens consistently across all three panels — v1.0 stable should appear in the same hue whether it's a timeline bar, a diff header pill, or a traffic stream. Reserve red exclusively for "breaking change" or "removed endpoint" signals, never for sunset status (use gray/faded instead) so red retains semantic weight. Include a deprecation countdown badge anywhere a deprecated version appears, computed from `sunsetDate - today`.

For the diff panel specifically, group changes by resource (endpoint path or schema name) rather than by raw JSON line, and collapse unchanged fields by default with a "show all" toggle. Breaking changes float to the top of each group and are tagged with a migration-required marker. This grouping is the single most important affordance for API consumers scanning for what will actually break their integration.
