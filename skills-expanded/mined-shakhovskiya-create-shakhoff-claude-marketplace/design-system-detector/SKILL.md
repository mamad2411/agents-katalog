---
name: design-system-detector
description: "Detects project design system for HTML report styling. Searches by convention paths, falls back to neutral default theme. Returns design tokens (colors, typography, spacing) for html-report-generator."
---

# Design System Detector

Находит design system проекта чтобы HTML отчёт выглядел в branding.

## Когда применять

- Перед html-report-generator
- Один раз per task cycle (cached в `.sprints/active/design-system-detection.md`)

## Detection order

Поиск по convention в этом порядке (first match wins):

### 1. Explicit config

`.sprints/config.yaml` field:
```yaml
html_reports:
  design_system_path: "/path/to/design.md"
```

Если specified - use this path.

### 2. Adjacent design system repo

`~/Dev/{project_name}-design-system/DESIGN.master.md`

Where `{project_name}` derived from current project's directory name.

Example:
- Project at `~/Dev/meridian/`
- Look for `~/Dev/meridian-design-system/DESIGN.master.md`

### 3. In-project design system

`<project>/design-system/DESIGN.master.md`

Single subfolder convention.

### 4. Single-file design

`<project>/DESIGN.md`

Simpler convention - one file.

### 5. None found - use default

Если ничего не найдено - use baked-in neutral default theme.

## What's extracted

If design file found, parse for:

### CSS variables / design tokens

Pattern matching:
```markdown
## Colors
- Primary: #1a73e8
- Secondary: #34a853
- Background: #ffffff
- Foreground: #1a1a1a
```

Or block:
```css
:root {
  --color-primary: #1a73e8;
  --color-secondary: #34a853;
}
```

Or YAML/JSON tokens:
```yaml
colors:
  primary: '#1a73e8'
  secondary: '#34a853'
```

Skill парсит multiple formats, extracts tokens.

### Typography

- Font families
- Heading font / body font
- Sizes scale (если specified)

### Spacing scale

- Space tokens (xs, sm, md, lg, xl)
- Or numeric scale (4px, 8px, 16px, etc.)

### Border radius

- Radius tokens (sm, md, lg)

### Brand assets

- Logo path (relative to design system file)
- Brand name

### Semantic colors

- Success / warning / error / info
- Severity colors (для finding visualizations)

## Output

`.sprints/active/design-system-detection.md`:

```markdown
# Design System Detection

**Detected at**: {{TIMESTAMP}}
**Method**: {{METHOD}}  <!-- explicit_config | adjacent_repo | in_project | single_file | not_found -->
**Source**: {{PATH or 'none - using default'}}

## Tokens extracted

### Colors
- primary: #1a73e8
- secondary: #34a853
- accent: #fbbc04
- background: #ffffff
- foreground: #1a1a1a
- muted: #5f6368

### Typography
- font_heading: 'Inter', sans-serif
- font_body: 'Source Sans Pro', sans-serif
- font_mono: 'JetBrains Mono', monospace

### Spacing
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 40px

### Brand
- name: "Project Name"
- logo: /path/to/logo.svg (or "none")

## Confidence

{{HIGH | MEDIUM | LOW}}

If LOW: parsing was partial, some defaults applied для missing tokens.
```

## Fallback behavior

### When design system found но parsing fails

Some tokens parsed, some missing:
- Use parsed where available
- Default fallback для missing
- Confidence: MEDIUM
- Log в detection file what was missed

### When no design system

Confidence: N/A (default mode)

Use complete default theme (modern neutral).

## Default theme tokens

Если nothing detected:

```yaml
colors:
  primary: "#3b82f6"     # Blue
  secondary: "#10b981"   # Green
  accent: "#f59e0b"      # Amber
  background: "#ffffff"
  foreground: "#1a1a1a"
  muted: "#666666"

typography:
  font_heading: "-apple-system, system-ui, sans-serif"
  font_body: "-apple-system, system-ui, sans-serif"
  font_mono: "Monaco, monospace"

spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "40px"

severity_colors:
  blocker: "#dc2626"
  critical: "#ea580c"
  high: "#ca8a04"
  medium: "#2563eb"
  low: "#6b7280"
```

These mapped to CSS variables в HTML report template.

## Caching

Detection cached в `.sprints/active/design-system-detection.md`:
- Re-used для регенерации HTML reports без re-detection
- Refreshed при new task cycle

## Validation

Detected tokens validated:
- Colors are valid hex/rgb format
- Sizes are valid CSS values
- Fonts are reasonable fallback chains

Invalid tokens: replaced с defaults, logged как warning.

## Integration с html-report-generator

```python
def generate_html_report(data):
    design_system = design_system_detector.detect()
    
    css = render_css_template(
        defaults=DEFAULT_TOKENS,
        overrides=design_system.tokens if design_system else {}
    )
    
    html = render_html_template(data, inline_css=css)
    return html
```

## Output for user transparency

В final report user message:

```
HTML report generated: .sprints/archive/<TS>/report.html

Design system: {{DETECTION_RESULT}}
- Found: {{PATH}} (confidence: HIGH)
- OR Not found: using neutral default theme
```

User знает откуда стилизация - можно adjust если не нравится.
