# EYES PEELED - Contrast & Accessibility Validator

## Purpose
Validates WCAG color accessibility compliance and generates compliant alternatives while preserving design intent. Acts as quality control for color palettes and design systems.

## When to Use
- After generating palettes with Hexed
- Validating design system tokens from Specimen
- Quick contrast checks during design work
- Bulk auditing of existing color systems
- Generating accessible alternatives for failing combinations

## Core Capabilities

### 1. Contrast Validation
Checks color combinations against WCAG 2.1 standards:
- **AA Normal Text**: 4.5:1 minimum
- **AA Large Text**: 3:1 minimum (18pt+ or 14pt+ bold)
- **AAA Normal Text**: 7:1 minimum
- **AAA Large Text**: 4.5:1 minimum
- **UI Components**: 3:1 minimum (non-text elements)

### 2. Smart Fix Generation
When combinations fail, generate minimal adjustments:
- Preserve hue relationships and color temperature
- Adjust only luminance when possible
- Offer multiple strategies (lighten bg, darken fg, both)
- Maintain perceptual color character
- Show before/after with exact contrast ratios

### 3. Palette-Wide Analysis
Audit entire color systems:
- Matrix of all possible text/background combinations
- Identify universally safe colors
- Flag problematic colors needing alternatives
- Generate summary statistics (% passing, problem areas)

### 4. Alternative Generation
Create accessible variants that preserve aesthetics:
- Use CIELAB color space for perceptual accuracy
- Maintain saturation character when adjusting lightness
- Generate tints/shades that pass requirements
- Provide multiple alternatives at different compliance levels

## Tool Selection

Always use Python with these libraries:
```python
import numpy as np
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
```

Required: `pip install colormath numpy --break-system-packages`

## Implementation Patterns

### Contrast Ratio Calculation
```python
def relative_luminance(rgb):
    """Calculate relative luminance per WCAG formula"""
    r, g, b = [v/255.0 for v in rgb]
    
    def adjust(val):
        return val/12.92 if val <= 0.03928 else ((val + 0.055)/1.055) ** 2.4
    
    R = adjust(r)
    G = adjust(g)
    B = adjust(b)
    
    return 0.2126 * R + 0.7152 * G + 0.0722 * B

def contrast_ratio(rgb1, rgb2):
    """Calculate WCAG contrast ratio between two colors"""
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)
```

### WCAG Compliance Check
```python
def check_wcag(fg_rgb, bg_rgb):
    """Return compliance levels for a color pair"""
    ratio = contrast_ratio(fg_rgb, bg_rgb)
    
    return {
        'ratio': round(ratio, 2),
        'AA_normal': ratio >= 4.5,
        'AA_large': ratio >= 3.0,
        'AAA_normal': ratio >= 7.0,
        'AAA_large': ratio >= 4.5,
        'UI_component': ratio >= 3.0
    }
```

### Smart Fix Generation
```python
def generate_fixes(fg_rgb, bg_rgb, target_ratio=4.5):
    """Generate minimal adjustments to meet target contrast ratio"""
    current_ratio = contrast_ratio(fg_rgb, bg_rgb)
    
    if current_ratio >= target_ratio:
        return None  # Already passes
    
    # Convert to LAB for perceptual adjustments
    fg_lab = convert_color(sRGBColor(*[v/255 for v in fg_rgb]), LabColor)
    bg_lab = convert_color(sRGBColor(*[v/255 for v in bg_rgb]), LabColor)
    
    fixes = []
    
    # Strategy 1: Darken foreground only
    fg_darker = adjust_lightness(fg_lab, target_ratio, bg_lab, darken=True)
    if fg_darker:
        fixes.append({
            'strategy': 'darken_foreground',
            'foreground': lab_to_hex(fg_darker),
            'background': rgb_to_hex(bg_rgb),
            'ratio': contrast_ratio(lab_to_rgb(fg_darker), bg_rgb)
        })
    
    # Strategy 2: Lighten background only
    bg_lighter = adjust_lightness(bg_lab, target_ratio, fg_lab, lighten=True)
    if bg_lighter:
        fixes.append({
            'strategy': 'lighten_background',
            'foreground': rgb_to_hex(fg_rgb),
            'background': lab_to_hex(bg_lighter),
            'ratio': contrast_ratio(fg_rgb, lab_to_rgb(bg_lighter))
        })
    
    # Strategy 3: Balanced adjustment (both colors move)
    balanced = balanced_adjustment(fg_lab, bg_lab, target_ratio)
    if balanced:
        fixes.append({
            'strategy': 'balanced',
            'foreground': lab_to_hex(balanced['fg']),
            'background': lab_to_hex(balanced['bg']),
            'ratio': balanced['ratio']
        })
    
    return fixes

def adjust_lightness(color_lab, target_ratio, fixed_color_lab, darken=False, lighten=False):
    """Adjust L* in LAB space to meet target contrast while preserving a* and b*"""
    # Binary search for the right L* value
    current_L = color_lab.lab_l
    min_L, max_L = (0, current_L) if darken else (current_L, 100)
    
    for _ in range(20):  # Iterate to find optimal L*
        test_L = (min_L + max_L) / 2
        test_color = LabColor(test_L, color_lab.lab_a, color_lab.lab_b)
        test_rgb = lab_to_rgb(test_color)
        fixed_rgb = lab_to_rgb(fixed_color_lab)
        
        ratio = contrast_ratio(test_rgb, fixed_rgb)
        
        if abs(ratio - target_ratio) < 0.1:
            return test_color
        
        if ratio < target_ratio:
            if darken:
                max_L = test_L
            else:
                min_L = test_L
        else:
            if darken:
                min_L = test_L
            else:
                max_L = test_L
    
    return None

def balanced_adjustment(fg_lab, bg_lab, target_ratio):
    """Adjust both colors proportionally to meet target ratio"""
    # Try moving both colors toward opposite ends of lightness
    for fg_factor in [0.3, 0.5, 0.7]:
        bg_factor = 1 - fg_factor
        
        # Determine direction based on current luminance
        fg_rgb = lab_to_rgb(fg_lab)
        bg_rgb = lab_to_rgb(bg_lab)
        
        if relative_luminance(fg_rgb) > relative_luminance(bg_rgb):
            # FG is lighter, so darken FG and lighten BG
            new_fg_L = fg_lab.lab_l - (fg_lab.lab_l * fg_factor * 0.3)
            new_bg_L = bg_lab.lab_l + ((100 - bg_lab.lab_l) * bg_factor * 0.3)
        else:
            # BG is lighter, so lighten FG and darken BG
            new_fg_L = fg_lab.lab_l + ((100 - fg_lab.lab_l) * fg_factor * 0.3)
            new_bg_L = bg_lab.lab_l - (bg_lab.lab_l * bg_factor * 0.3)
        
        new_fg = LabColor(new_fg_L, fg_lab.lab_a, fg_lab.lab_b)
        new_bg = LabColor(new_bg_L, bg_lab.lab_a, bg_lab.lab_b)
        
        new_fg_rgb = lab_to_rgb(new_fg)
        new_bg_rgb = lab_to_rgb(new_bg)
        
        ratio = contrast_ratio(new_fg_rgb, new_bg_rgb)
        
        if ratio >= target_ratio:
            return {
                'fg': new_fg,
                'bg': new_bg,
                'ratio': round(ratio, 2)
            }
    
    return None
```

### Palette Matrix Analysis
```python
def audit_palette(colors):
    """
    Generate complete accessibility matrix for a palette
    colors: dict of {name: hex_code}
    """
    results = {
        'combinations': [],
        'safe_backgrounds': [],
        'safe_foregrounds': [],
        'problem_colors': [],
        'stats': {}
    }
    
    color_list = list(colors.items())
    total_combos = 0
    passing_aa = 0
    passing_aaa = 0
    
    # Check all text/background combinations
    for fg_name, fg_hex in color_list:
        for bg_name, bg_hex in color_list:
            if fg_name == bg_name:
                continue
            
            fg_rgb = hex_to_rgb(fg_hex)
            bg_rgb = hex_to_rgb(bg_hex)
            compliance = check_wcag(fg_rgb, bg_rgb)
            
            results['combinations'].append({
                'foreground': fg_name,
                'background': bg_name,
                'compliance': compliance
            })
            
            total_combos += 1
            if compliance['AA_normal']:
                passing_aa += 1
            if compliance['AAA_normal']:
                passing_aaa += 1
    
    # Identify universally safe colors
    for name, hex_code in color_list:
        rgb = hex_to_rgb(hex_code)
        
        # Check as background
        safe_bg_count = sum(1 for fn, fh in color_list 
                           if fn != name and 
                           check_wcag(hex_to_rgb(fh), rgb)['AA_normal'])
        if safe_bg_count >= len(color_list) * 0.7:
            results['safe_backgrounds'].append(name)
        
        # Check as foreground
        safe_fg_count = sum(1 for bn, bh in color_list 
                           if bn != name and 
                           check_wcag(rgb, hex_to_rgb(bh))['AA_normal'])
        if safe_fg_count >= len(color_list) * 0.7:
            results['safe_foregrounds'].append(name)
    
    results['stats'] = {
        'total_combinations': total_combos,
        'aa_pass_rate': round(passing_aa / total_combos * 100, 1),
        'aaa_pass_rate': round(passing_aaa / total_combos * 100, 1)
    }
    
    return results
```

### Accessible Alternative Generation
```python
def generate_accessible_variants(hex_color, target_bg_hex, levels=['AA', 'AAA']):
    """
    Generate accessible variants of a color that work with target background
    Preserves hue and saturation character
    """
    color_rgb = hex_to_rgb(hex_color)
    bg_rgb = hex_to_rgb(target_bg_hex)
    color_lab = convert_color(sRGBColor(*[v/255 for v in color_rgb]), LabColor)
    bg_lab = convert_color(sRGBColor(*[v/255 for v in bg_rgb]), LabColor)
    
    variants = {}
    
    # Target ratios
    targets = {
        'AA_normal': 4.5,
        'AA_large': 3.0,
        'AAA_normal': 7.0,
        'AAA_large': 4.5
    }
    
    for level_key, target_ratio in targets.items():
        if any(level in level_key for level in levels):
            # Try to adjust while preserving a* and b*
            adjusted = adjust_lightness(
                color_lab, 
                target_ratio, 
                bg_lab,
                darken=relative_luminance(color_rgb) > relative_luminance(bg_rgb)
            )
            
            if adjusted:
                adjusted_rgb = lab_to_rgb(adjusted)
                variants[level_key] = {
                    'hex': rgb_to_hex(adjusted_rgb),
                    'rgb': adjusted_rgb,
                    'ratio': contrast_ratio(adjusted_rgb, bg_rgb),
                    'delta_e': delta_e_cie2000(color_lab, adjusted)
                }
    
    return variants
```

## Utility Functions

```python
def hex_to_rgb(hex_code):
    """Convert hex to RGB tuple"""
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex"""
    return '#{:02x}{:02x}{:02x}'.format(*[int(v) for v in rgb])

def lab_to_rgb(lab_color):
    """Convert LAB to RGB tuple"""
    rgb = convert_color(lab_color, sRGBColor)
    return (
        max(0, min(255, int(rgb.rgb_r * 255))),
        max(0, min(255, int(rgb.rgb_g * 255))),
        max(0, min(255, int(rgb.rgb_b * 255)))
    )

def lab_to_hex(lab_color):
    """Convert LAB to hex"""
    return rgb_to_hex(lab_to_rgb(lab_color))
```

## Output Formats

### Single Pair Check
```
Contrast Check: #2563eb (Blue) on #ffffff (White)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Contrast Ratio: 8.59:1

WCAG Compliance:
  ✓ AA Normal Text (4.5:1)
  ✓ AA Large Text (3:1)
  ✓ AAA Normal Text (7:1)
  ✓ AAA Large Text (4.5:1)
  ✓ UI Components (3:1)

Status: PASSES ALL REQUIREMENTS
```

### Failed Pair with Fixes
```
Contrast Check: #60a5fa (Light Blue) on #ffffff (White)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Contrast Ratio: 2.13:1

WCAG Compliance:
  ✗ AA Normal Text (needs 4.5:1)
  ✗ AA Large Text (needs 3:1)
  ✗ AAA Normal Text (needs 7:1)
  ✗ AAA Large Text (needs 4.5:1)
  ✗ UI Components (needs 3:1)

Suggested Fixes (AA Normal Text):

1. Darken Foreground
   Before: #60a5fa  After: #1d6fc9
   Ratio: 4.51:1  ✓ AA Normal
   Color Shift: ΔE = 23.4 (moderate)

2. Lighten Background  
   Not viable (background already white)

3. Balanced Adjustment
   FG: #2b7dd6  BG: #f8fafc
   Ratio: 4.52:1  ✓ AA Normal
   Color Shift: ΔE = 15.2 (minimal)
   
Recommendation: Use Balanced Adjustment to minimize visual change
```

### Palette Audit Summary
```
Accessibility Audit: Design System Palette
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8 colors analyzed, 56 combinations tested

Overall Statistics:
  AA Compliance: 42.9% (24/56 combinations)
  AAA Compliance: 21.4% (12/56 combinations)

Universally Safe Backgrounds (work with 70%+ foregrounds):
  • slate-50 (#f8fafc) - works with 7/8 colors
  • slate-900 (#0f172a) - works with 7/8 colors

Universally Safe Foregrounds (work on 70%+ backgrounds):
  • slate-900 (#0f172a) - works on 6/8 backgrounds
  • slate-700 (#334155) - works on 5/8 backgrounds

Problem Colors (low compatibility):
  ⚠ blue-400 (#60a5fa) - only 2/8 as foreground, 1/8 as background
  ⚠ yellow-300 (#fde047) - only 1/8 as foreground, 3/8 as background

Recommended Actions:
  1. Add darker variant of blue-400 for text use
  2. Reserve yellow-300 for large UI elements only
  3. Consider slate-50 and slate-900 as primary text colors
```

## Integration Workflows

### With Hexed
```python
# After Hexed generates a palette
hexed_palette = {
    'primary': '#3b82f6',
    'secondary': '#8b5cf6',
    'accent': '#f59e0b',
    'neutral-dark': '#1f2937',
    'neutral-light': '#f3f4f6'
}

# Audit for accessibility
audit_results = audit_palette(hexed_palette)

# Generate fixes for failing combinations
for combo in audit_results['combinations']:
    if not combo['compliance']['AA_normal']:
        fixes = generate_fixes(
            hex_to_rgb(hexed_palette[combo['foreground']]),
            hex_to_rgb(hexed_palette[combo['background']])
        )
        # Present fixes to user
```

### With Specimen
```python
# Validate design system tokens
design_tokens = {
    'text-primary': '#111827',
    'text-secondary': '#6b7280',
    'bg-primary': '#ffffff',
    'bg-secondary': '#f9fafb',
    'accent-blue': '#3b82f6'
}

# Check all text/background combinations
text_colors = {k: v for k, v in design_tokens.items() if 'text' in k}
bg_colors = {k: v for k, v in design_tokens.items() if 'bg' in k}

for text_name, text_hex in text_colors.items():
    for bg_name, bg_hex in bg_colors.items():
        compliance = check_wcag(hex_to_rgb(text_hex), hex_to_rgb(bg_hex))
        # Report results
```

### Standalone Quick Check
```python
# Quick contrast check during design work
result = check_wcag(
    hex_to_rgb('#2563eb'),  # Text color
    hex_to_rgb('#ffffff')   # Background color
)

if not result['AA_normal']:
    fixes = generate_fixes(
        hex_to_rgb('#2563eb'),
        hex_to_rgb('#ffffff'),
        target_ratio=4.5
    )
```

## Best Practices

1. **Always calculate exact ratios** - Don't just report pass/fail, show the actual number
2. **Preserve design intent** - When suggesting fixes, maintain hue relationships
3. **Use perceptual color spaces** - LAB space for adjustments, not RGB
4. **Provide multiple strategies** - Different fixes work better in different contexts
5. **Show before/after** - Visual comparison helps designers make informed decisions
6. **Context matters** - Large text has different requirements than normal text
7. **Batch operations** - Audit entire palettes, not just individual pairs
8. **Document edge cases** - Some color combinations may be mathematically impossible to fix

## Common Pitfalls to Avoid

- Don't adjust saturation when fixing contrast (preserve color character)
- Don't assume both colors can be adjusted (backgrounds may be fixed)
- Don't ignore visual weight (7:1 can look harsh if not handled carefully)
- Don't forget to clamp RGB values after LAB conversion
- Don't use simple lighten/darken without perceptual models

## Example Usage Patterns

**Quick Check:**
"Check if #3b82f6 on #ffffff meets AA standards"

**Fix Generation:**
"This blue (#60a5fa) fails on white - give me accessible alternatives"

**Palette Audit:**
"Here's my color palette [list] - audit all combinations and flag problems"

**System Validation:**
"Validate these design tokens for WCAG AA compliance"

**Alternative Generation:**
"Generate AAA-compliant versions of these brand colors for a light background"

## Notes

- Always use the WCAG 2.1 formula for relative luminance (not simple averaging)
- Delta E (CIE2000) measures perceptual color difference - lower is better
- A ΔE of 2-5 is barely perceptible, 5-10 is noticeable, >10 is significant
- Some color combinations are impossible to fix while maintaining the color (e.g., yellow on white)
- When a fix isn't viable, recommend alternative color choices from the palette
