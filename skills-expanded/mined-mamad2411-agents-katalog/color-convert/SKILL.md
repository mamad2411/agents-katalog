---
name: color-convert
description: Convert between HEX, RGB, HSL, and OKLCH color formats; generate palettes and check contrast pairs for accessibility. Use when theming UI, debugging CSS colors, or validating WCAG contrast ratios.
---

# Color Convert

Convert between color formats, generate harmonious palettes, and validate contrast for accessibility. **Always state color space** — sRGB is default unless wide-gamut (P3, OKLCH) is specified.

## When to Use This Skill

| Trigger | Example request |
|---------|-----------------|
| Format conversion | "Convert #3B82F6 to RGB and HSL" |
| CSS modernization | "Express this hex in OKLCH" |
| Palette generation | "Generate monochromatic shades from #6366F1" |
| Accessibility | "Does white text on #2563EB pass WCAG AA?" |
| Design tokens | "Create 9-step neutral scale" |
| Color matching | "Find complementary color for #E11D48" |

## Phase Checklist

```
[ ] 1. Parse input format (HEX, RGB, HSL, OKLCH, named)
[ ] 2. Validate values (hex length, RGB 0-255, HSL ranges)
[ ] 3. Convert through canonical space (usually linear sRGB or OKLab)
[ ] 4. Present all requested output formats
[ ] 5. For contrast: specify text size and WCAG level (AA/AAA)
[ ] 6. Note gamut limits if converting to/from OKLCH
```

---

## Supported Formats

| Format | Example | CSS syntax |
|--------|---------|------------|
| HEX | `#3B82F6` | `#RRGGBB` or `#RGB` |
| RGB | `rgb(59, 130, 246)` | 0-255 per channel |
| RGBA | `rgba(59, 130, 246, 0.8)` | Alpha 0-1 |
| HSL | `hsl(217, 91%, 60%)` | H: 0-360, S/L: 0-100% |
| HSLA | `hsla(217, 91%, 60%, 0.8)` | With alpha |
| OKLCH | `oklch(0.62 0.21 264)` | L: 0-1, C: 0+, H: 0-360 |
| Named | `cornflowerblue` | CSS named colors |

---

## HEX ↔ RGB

```python
def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"Invalid hex: {hex_color}")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02X}{g:02X}{b:02X}"

r, g, b = hex_to_rgb("#3B82F6")
print(f"RGB: ({r}, {g}, {b})")           # (59, 130, 246)
print(f"HEX: {rgb_to_hex(r, g, b)}")     # #3B82F6
print(f"CSS: rgb({r}, {g}, {b})")
```

```bash
# ImageMagick (if available)
convert -size 1x1 xc:"#3B82F6" -format "%[fx:255*r],%[fx:255*g],%[fx:255*b]" info:
```

---

## RGB ↔ HSL

```python
import colorsys

def rgb_to_hsl(r: int, g: int, b: int) -> tuple[float, float, float]:
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return round(h * 360, 1), round(s * 100, 1), round(l * 100, 1)

def hsl_to_rgb(h: float, s: float, l: float) -> tuple[int, int, int]:
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return round(r * 255), round(g * 255), round(b * 255)

h, s, l = rgb_to_hsl(59, 130, 246)
print(f"HSL: ({h}, {s}%, {l}%)")         # (217, 91%, 60%)
print(f"CSS: hsl({h}, {s}%, {l}%)")

r, g, b = hsl_to_rgb(h, s, l)
print(f"Back to RGB: ({r}, {g}, {b})")
```

---

## OKLCH Conversion

OKLCH provides perceptually uniform lightness — preferred for modern CSS theming.

```python
# Requires: pip install coloraide
from coloraide import Color

def convert_all(hex_color: str) -> dict:
    c = Color(hex_color)
    return {
        "hex": c.to_string(hex=True, upper=True),
        "rgb": c.to_string(naive=True, fit=False),  # rgb(...)
        "hsl": c.convert("hsl").to_string(naive=True, fit=False),
        "oklch": c.convert("oklch").to_string(naive=True, fit=False),
    }

for k, v in convert_all("#3B82F6").items():
    print(f"{k:8} {v}")
```

```css
/* Modern CSS — OKLCH in stylesheets */
.button {
  background: oklch(0.62 0.21 264);
  color: oklch(0.98 0.01 264);
}

/* With fallbacks */
.button {
  background: #3B82F6;
  background: oklch(0.62 0.21 264);
}
```

**Gamut note:** OKLCH colors may clip when converted to sRGB. Report if clipping occurs.

---

## Palette Generation

### Monochromatic (Lightness Scale)

```python
import colorsys

def monochromatic_palette(hex_color: str, steps: int = 9) -> list[str]:
    r, g, b = hex_to_rgb(hex_color)
    h, s, l = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)

    palette = []
    for i in range(steps):
        new_l = 0.1 + (0.85 * i / (steps - 1))
        nr, ng, nb = colorsys.hls_to_rgb(h, new_l, s)
        palette.append(rgb_to_hex(round(nr * 255), round(ng * 255), round(nb * 255)))
    return palette

for i, color in enumerate(monochromatic_palette("#6366F1", 9)):
    print(f"  {i+1}: {color}")
```

### Complementary

```python
def complementary(hex_color: str) -> str:
    r, g, b = hex_to_rgb(hex_color)
    h, s, l = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    comp_h = (h + 0.5) % 1.0
    nr, ng, nb = colorsys.hls_to_rgb(comp_h, l, s)
    return rgb_to_hex(round(nr * 255), round(ng * 255), round(nb * 255))

print(f"Complement of #E11D48: {complementary('#E11D48')}")
```

### Analogous (±30° hue)

```python
def analogous(hex_color: str, spread: float = 30 / 360) -> list[str]:
    r, g, b = hex_to_rgb(hex_color)
    h, s, l = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    colors = []
    for offset in [-spread, 0, spread]:
        nh = (h + offset) % 1.0
        nr, ng, nb = colorsys.hls_to_rgb(nh, l, s)
        colors.append(rgb_to_hex(round(nr * 255), round(ng * 255), round(nb * 255)))
    return colors
```

### Tailwind-Style Scale (50–950)

```python
def tailwind_scale(hex_color: str) -> dict[str, str]:
    r, g, b = hex_to_rgb(hex_color)
    h, s, l = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    steps = {"50": 0.97, "100": 0.94, "200": 0.87, "300": 0.77,
             "400": 0.65, "500": l, "600": l * 0.85, "700": l * 0.7,
             "800": l * 0.55, "900": l * 0.4, "950": l * 0.25}
    return {
        name: rgb_to_hex(*[round(c * 255) for c in colorsys.hls_to_rgb(h, lv, s)])
        for name, lv in steps.items()
    }
```

---

## Contrast Ratio (WCAG)

```python
def relative_luminance(r: int, g: int, b: int) -> float:
    def linearize(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)

def contrast_ratio(fg_hex: str, bg_hex: str) -> float:
    l1 = relative_luminance(*hex_to_rgb(fg_hex))
    l2 = relative_luminance(*hex_to_rgb(bg_hex))
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return round((lighter + 0.05) / (darker + 0.05), 2)

def wcag_check(fg: str, bg: str) -> dict:
    ratio = contrast_ratio(fg, bg)
    return {
        "ratio": ratio,
        "AA_normal": ratio >= 4.5,      # < 18pt text
        "AA_large": ratio >= 3.0,       # ≥ 18pt or 14pt bold
        "AAA_normal": ratio >= 7.0,
        "AAA_large": ratio >= 4.5,
    }

result = wcag_check("#FFFFFF", "#2563EB")
print(result)
# ratio: 5.17, AA_normal: True, AA_large: True, ...
```

### WCAG Requirements

| Level | Normal text | Large text |
|-------|-------------|------------|
| AA | ≥ 4.5:1 | ≥ 3:1 |
| AAA | ≥ 7:1 | ≥ 4.5:1 |

Large text = 18pt+ (24px) or 14pt bold (18.5px).

### Contrast Pair Suggestions

```python
def suggest_text_color(bg_hex: str) -> str:
    white_ratio = contrast_ratio("#FFFFFF", bg_hex)
    black_ratio = contrast_ratio("#000000", bg_hex)
    return "#FFFFFF" if white_ratio > black_ratio else "#000000"

print(f"Best text on #2563EB: {suggest_text_color('#2563EB')}")
```

---

## CSS Output Generation

```python
def css_variables(palette: dict[str, str], prefix: str = "--color-primary") -> str:
    lines = [":root {"]
    for step, hex_val in palette.items():
        r, g, b = hex_to_rgb(hex_val)
        lines.append(f"  {prefix}-{step}: {hex_val};")
        lines.append(f"  {prefix}-{step}-rgb: {r}, {g}, {b};")
    lines.append("}")
    return "\n".join(lines)
```

---

## Worked Examples

### Example 1: Full conversion chain

```
Input:  #3B82F6 (Tailwind blue-500)
HEX:    #3B82F6
RGB:    rgb(59, 130, 246)
HSL:    hsl(217, 91%, 60%)
OKLCH:  oklch(0.62 0.21 264)
```

### Example 2: Contrast failure

```
Foreground: #94A3B8 (slate-400)
Background: #FFFFFF
Ratio:      2.56:1
Result:     ✗ Fails WCAG AA for normal text (need 4.5:1)
Fix:        Use #64748B (slate-500, ratio 4.68:1) or darker
```

### Example 3: Design token scale

```
Base: primary-500 = #6366F1
Generated: 50, 100, 200, ... 950 (11 steps)
Output: CSS custom properties for design system
See: frontend-design skill for usage in components
```

---

## Output Template

```markdown
## Color: {input}

| Format | Value |
|--------|-------|
| HEX | `#3B82F6` |
| RGB | `rgb(59, 130, 246)` |
| HSL | `hsl(217, 91%, 60%)` |
| OKLCH | `oklch(0.62 0.21 264)` |

### Contrast Check
| Pair | Ratio | AA Normal | AA Large |
|------|-------|-----------|----------|
| `#FFFFFF` on `#3B82F6` | 5.17:1 | ✓ | ✓ |
| `#000000` on `#3B82F6` | 4.07:1 | ✗ | ✓ |

### Palette (monochromatic, 5 steps)
1. `#1E3A5F` (darkest)
2. `#2563EB`
3. `#3B82F6` (base)
4. `#93C5FD`
5. `#DBEAFE` (lightest)
```

---

## Anti-Patterns

- Converting colors without specifying color space (sRGB vs P3)
- Using HSL lightness for perceptually even scales (use OKLCH instead)
- WCAG check without specifying text size (normal vs large)
- Ignoring alpha/transparency in contrast calculations
- Hardcoding colors without CSS custom property fallbacks
- Assuming hex with alpha (#RRGGBBAA) works in all browsers
- Generating palettes without checking contrast on each step

---

## Cross-References

| Related need | Skill |
|--------------|-------|
| Colors in JSON theme config | `format-convert` |
| CSS class naming (kebab-case) | `text-utils` |
| QR code with brand colors | `qr-generator` |
| Encode color in URL params | `encode-decode` |
| SQL storing hex color values | `sql-format` |
| Frontend design system usage | `frontend-design` (frontend plugin) |
