---
name: ATT&CK Navigator Layer Generator
description: Generate MITRE ATT&CK Navigator layers for coverage visualization, threat actor mapping, and gap analysis. Produces JSON files compatible with the Navigator web app.
---

# ATT&CK Navigator Layer Generator Skill

## Overview

ATT&CK Navigator layers are JSON files that visualize technique coverage on the MITRE ATT&CK matrix. This skill covers generating layers for three primary use cases:

1. **Coverage heatmaps** — Show which techniques have detections (and how many)
2. **Threat actor mapping** — Highlight techniques used by a specific group
3. **Gap analysis** — Compare your coverage against a threat profile

## Navigator Layer JSON Format

Every layer follows this structure:

```json
{
  "name": "Layer Name",
  "versions": {
    "attack": "18.1",
    "navigator": "5.3.1",
    "layer": "4.5"
  },
  "domain": "enterprise-attack",
  "description": "Layer description",
  "techniques": [
    {
      "techniqueID": "T1059.001",
      "tactic": "execution",
      "score": 75,
      "color": "#66b2ff",
      "comment": "3 Sigma rules, 2 Splunk ESCU rules",
      "enabled": true
    }
  ],
  "gradient": {
    "colors": ["#ff6666", "#ffe766", "#8ec843"],
    "minValue": 0,
    "maxValue": 100
  }
}
```

### Key Fields

| Field | Type | Purpose |
|-------|------|---------|
| `techniqueID` | string | MITRE technique ID (e.g., `T1059.001`) |
| `tactic` | string | Tactic shortname (required for sub-techniques that appear in multiple tactics) |
| `score` | number | 0–100, drives gradient coloring |
| `color` | string | Hex color override (takes precedence over score gradient) |
| `comment` | string | Hover text with details |
| `enabled` | boolean | Whether technique is visible |

### Color Conventions

| Color | Meaning |
|-------|---------|
| `#8ec843` (green) | Good coverage (score 70–100) |
| `#ffe766` (yellow) | Partial coverage (score 30–69) |
| `#ff6666` (red) | Weak/no coverage (score 0–29) |
| `#6baed6` (blue) | Threat actor uses this technique |
| `#ffffff` (white) | Not assessed / not applicable |

## Use Case 1: Coverage Heatmap

Visualize detection coverage across all techniques. Score is based on number and quality of detections.

**Using MCP tools:**

```
1. get_technique_ids()                    → Get all covered technique IDs
2. analyze_coverage()                     → Get tactic-level breakdown
3. generate_coverage_layer(covered_ids)   → Generate the layer JSON
```

**Scoring formula (suggested):**
- 1 detection = score 25
- 2–3 detections = score 50
- 4–5 detections = score 75
- 6+ detections = score 100
- Bonus: +10 for each additional source type (Sigma + Splunk + Elastic)

## Use Case 2: Threat Actor Mapping

Highlight all techniques attributed to a specific threat group.

**Using MCP tools:**

```
1. search_groups("APT29")                 → Find group ID (G0016)
2. get_group_techniques("G0016")          → Get technique list
3. generate_group_layer("G0016", "APT29") → Generate the layer
```

## Use Case 3: Gap Analysis

Compare your detection coverage against a target set of techniques (e.g., a threat actor's TTPs).

**Using MCP tools:**

```
1. get_technique_ids()                                → Your covered IDs
2. get_group_techniques("G0016")                      → Target IDs
3. generate_gap_layer(covered, target, "APT29 Gaps")  → Gap layer
```

**Gap layer color scheme:**
- Green = covered (you have detections AND the threat actor uses it)
- Red = gap (threat actor uses it but you have NO detection)
- Gray = not used by this actor

## Generating Layers Programmatically

If MCP tools aren't available, build the JSON directly:

```python
import json

def make_layer(name, techniques, description=""):
    return {
        "name": name,
        "versions": {"attack": "18.1", "navigator": "5.3.1", "layer": "4.5"},
        "domain": "enterprise-attack",
        "description": description,
        "techniques": techniques,
        "gradient": {
            "colors": ["#ff6666", "#ffe766", "#8ec843"],
            "minValue": 0,
            "maxValue": 100,
        },
    }

techniques = [
    {"techniqueID": "T1059.001", "score": 80, "comment": "5 detections"},
    {"techniqueID": "T1053.005", "score": 40, "comment": "1 detection"},
]

layer = make_layer("My Coverage", techniques, "Detection coverage as of 2026-02")
with open("coverage_layer.json", "w") as f:
    json.dump(layer, f, indent=2)
```

## Viewing Layers

1. Open [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/)
2. Click **Open Existing Layer** → **Upload from local**
3. Select the generated JSON file

Or host Navigator locally:

```bash
git clone https://github.com/mitre-attack/attack-navigator.git
cd attack-navigator/nav-app
npm install && npm start
```

## Tips

- **Layer per audience:** Executives want simple red/green; analysts want score gradients with comments.
- **Version pin:** Always set `versions.attack` to match the ATT&CK version your analysis used.
- **Combine layers:** Navigator supports overlaying multiple layers — useful for comparing before/after or two threat actors.
- **Export as SVG:** Navigator can export layers as SVG for inclusion in reports.
