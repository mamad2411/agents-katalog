---
name: antv-infographic
description: "Template-driven medical infographics using the AntV Infographic framework. Use when creating structured infographics from clinical data, trial results, or patient education content using pre-built templates for hero stats, comparison layouts, process flows, myth-busters, and checklists. Outputs publication-ready HTML/PNG infographics with JACC/NEJM-grade design tokens."
---

# AntV Infographic Integration

**Purpose:** Template-driven medical infographics using the AntV Infographic framework

---

## Quick Start & Workflow

### Step 1 — List Available Templates

```bash
cd skills/cardiology/visual-design-system/antv_infographic
python scripts/antv_cli.py list --verbose
```

**Available Templates** (full catalog: see `TEMPLATES.md`):
1. `trial_result_simple` — Clinical trial timeline (4 phases)
2. `mechanism_of_action` — Drug mechanism steps (5 steps)
3. `treatment_comparison` — Side-by-side treatment comparison
4. `patient_journey` — Patient care pathway (5 stages)
5. `guideline_recommendations` — Guideline strength classification
6. `dosing_schedule` — Medication dosing schedule (4 weeks)
7. `safety_profile` — Adverse events by frequency
8. `biomarker_progression` — Biomarker changes over time
9. `trial_endpoints` — Primary and secondary endpoints
10. `risk_stratification` — Risk level classification
11. `diagnostic_pathway` — Diagnostic workflow (5 steps)

### Step 2 — Render to HTML

```bash
python scripts/antv_cli.py render \
  --template mechanism_of_action \
  --output outputs/mechanism_of_action.html \
  --width 1000 --height 800 \
  --title "Drug Mechanism"
```

### Step 3 — Validate Output

Confirm the HTML file exists and is non-empty before proceeding.

```bash
ls -lh outputs/mechanism_of_action.html   # Should be >10KB; if missing or tiny, re-run with --verbose
```

### Step 4 — Download Output

Open the HTML in your browser (path is printed in CLI output), then click **Download SVG** (vector, editable) or **Download PNG** (raster, 2× resolution, publication quality).

---

### Python API

```python
from scripts.antv_renderer import render_template, AntvRenderer

# Quick render
output = render_template('trial_result_simple', 'output.html')
assert output.exists() and output.stat().st_size > 1000, "Render failed"

# Advanced usage
renderer = AntvRenderer()
renderer.render_template_to_html(
    'mechanism_of_action',
    'mechanism.html',
    width=1000,
    height=800,
    title='Drug Mechanism of Action'
)
```

**Programmatic batch rendering:**
```python
from scripts.antv_renderer import AntvRenderer

renderer = AntvRenderer()
templates = ['trial_result_simple', 'mechanism_of_action', 'patient_journey']

for template in templates:
    output = renderer.render_template_to_html(
        template,
        f'outputs/{template}.html',
        width=1200,
        height=900
    )
    assert output.exists() and output.stat().st_size > 1000, f"Render failed: {template}"
    print(f"Generated: {output}")
```

---

## Template Examples

### Mechanism of Action (`mechanism_of_action`)

**Use for:** Drug mechanisms, biological pathways

```
infographic list-row-simple-vertical
data
  items:
    - label: Oral Administration
      desc: Drug taken orally, absorbed in GI tract
    - label: Systemic Distribution
      desc: Reaches target organs via bloodstream
    - label: Receptor Binding
      desc: Binds to specific receptors at cellular level
    - label: Cellular Response
      desc: Triggers cascade of intracellular signaling
    - label: Clinical Effect
      desc: Measurable improvement in symptoms/outcomes
```

---

## Custom Spec Syntax

```
infographic [TEMPLATE_TYPE]
data
  items:
    - label: [LABEL_TEXT]
      desc: [DESCRIPTION_TEXT]
```

**Template types:**
- `list-row-simple-horizontal-arrow` — Horizontal timeline with arrows
- `list-row-simple-vertical` — Vertical list with connectors
- (200+ more — see AntV documentation)

**Render custom spec:**
```bash
python scripts/antv_cli.py render \
  --spec "infographic list-row-simple-horizontal-arrow
data
  items:
    - label: Step 1
      desc: First action
    - label: Step 2
      desc: Second action" \
  --output custom.html
```

---

## Visual Router Integration

**Routing keywords:** "template infographic", "structured infographic", "step-by-step infographic", "trial timeline", "mechanism steps", "treatment pathway infographic"

```python
from cardiology_visual_system.scripts.visual_router import VisualRouter

router = VisualRouter()
router.route("Create a template infographic showing trial timeline")   # → AntV
# Other tools: custom infographic → Gemini | forest plot → Plotly | flowchart → Mermaid
```

---

## CLI Reference

```bash
python scripts/antv_cli.py list                    # Simple list
python scripts/antv_cli.py list --verbose          # With descriptions
python scripts/antv_cli.py render \
  --template mechanism_of_action \
  --output outputs/mechanism.html \
  --width 1000 --height 800 \
  --title "Drug Mechanism"
python scripts/antv_cli.py examples               # Generate all 11 examples to outputs/examples/
python scripts/antv_cli.py info                   # Show integration info
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| HTML doesn't open automatically | Open manually; path is printed in CLI output |
| SVG download button fails | Use a modern browser (Chrome, Firefox, Safari); check console for errors |
| Python import error | Run from `skills/cardiology/visual-design-system/antv_infographic/` |
| Template not found | Check spelling; use `list --verbose`; templates live in `templates/*.txt` |

---

## References

- [AntV Infographic GitHub](https://github.com/antvis/Infographic)
- [AntV Documentation](https://antv.vision/en)
- [Full Template Catalog](TEMPLATES.md)
- [Python API Reference](API.md)
- [Visual Design System](../SKILL.md)
- [Visual Router](../../cardiology-visual-system/scripts/visual_router.py)
