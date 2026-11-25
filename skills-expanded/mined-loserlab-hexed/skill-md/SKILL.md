# Hexed

**Hexed** is an image-to-color-system compiler that extracts structured color palettes from visual references.

## Overview

Hexed accepts 1-5 images (PNG, JPG, WebP) and returns a complete color system suitable for UI design, product themes, and design tokens. The output is deterministic, structured, and ready for downstream automation.

This skill does **not** generate copy, layouts, or branding concepts. It only produces color systems derived from visual input.

---

## When to Use This Skill

Use Hexed when the user:
- Uploads images and asks to extract colors, create a palette, or build a color system
- Requests design tokens, theme colors, or UI colors from visual references
- Wants to export colors in specific formats (CSS, Tailwind, Figma)
- Needs a structured color system for design or development work
- Mentions terms like: "color palette", "color scheme", "design tokens", "theme colors"

**Example triggers:**
- "Extract colors from these images"
- "Create a color system based on this photo"
- "Generate Tailwind colors from my brand images"
- "Build me a design token system from these screenshots"

---

## What Hexed Produces

Given uploaded images, Hexed produces a **structured color system** including:

1. **Core colors**: Primary, secondary, accent
2. **Neutral ramp**: 10-step grayscale (50-900)
3. **Semantic colors**: Success, warning, error, info
4. **UI theme tokens**: Complete light and dark theme definitions
5. **Debug data**: Image processing details, extracted palettes, sample colors

The output structure is stable and designed for direct use in design systems and frontend tooling.

---

## Usage Instructions

### Step 1: Locate User-Uploaded Images

When the user uploads images, they're available at `/mnt/user-data/uploads/`. Check what's available:

```bash
ls -lh /mnt/user-data/uploads/
```

### Step 2: Run the Compiler

Use the `hexed_compiler.py` script to process images:

```python
import sys
sys.path.append('/mnt/skills/user/hexed')

from hexed_compiler import compile_from_images

# Process 1-5 images
image_paths = [
    '/mnt/user-data/uploads/image1.png',
    '/mnt/user-data/uploads/image2.jpg'
]

result = compile_from_images(image_paths, mode='ui_first')

if result['ok']:
    color_system = result['color_system']
    debug_info = result['debug']
    # Use the color system...
else:
    print(f"Error: {result['message']}")
```

**Modes:**
- `ui_first` (default): Optimized for UI/product design
- `brand_first`: Optimized for brand/marketing materials

### Step 3: Export to Desired Format

After compiling, export the color system:

```python
from hexed_exports import (
    export_css_variables,
    export_tailwind_config,
    export_figma_tokens
)

# CSS Variables
css = export_css_variables(color_system)

# Tailwind Config
tailwind = export_tailwind_config(color_system)

# Figma Tokens
figma_result = export_figma_tokens(color_system)
figma_json = figma_result['tokens']
```

### Step 4: Save and Present Outputs

Save exports to `/mnt/user-data/outputs/` so the user can access them:

```python
import json

# Save JSON color system
with open('/mnt/user-data/outputs/color-system.json', 'w') as f:
    json.dump(color_system, f, indent=2)

# Save CSS variables
with open('/mnt/user-data/outputs/colors.css', 'w') as f:
    f.write(css)

# Save Tailwind config
with open('/mnt/user-data/outputs/tailwind.config.js', 'w') as f:
    f.write(tailwind)

# Save Figma tokens
with open('/mnt/user-data/outputs/figma-tokens.json', 'w') as f:
    json.dump(figma_json, f, indent=2)
```

Then use `present_files` to share them with the user.

---

## Output Structure

The compiled color system follows this structure:

```json
{
  "version": "1.0",
  "meta": {
    "id": "cs_generated",
    "mode": "ui_first",
    "generated_at": "2026-01-21T...",
    "engine": { "name": "hexed", "engine_version": "0.2.0" }
  },
  "colors": {
    "core": {
      "primary": { "hex": "#3B6EF5", "space": "srgb" },
      "secondary": { "hex": "#1CC7A1", "space": "srgb" },
      "accent": { "hex": "#FF4D6D", "space": "srgb" }
    },
    "neutrals": {
      "ramp": [
        { "step": 50, "hex": "#F7F8FA" },
        { "step": 100, "hex": "#EDF0F4" },
        ...
        { "step": 900, "hex": "#151825" }
      ],
      "intent": "cool_neutral"
    },
    "semantic": {
      "success": { "hex": "#1DB954", "space": "srgb" },
      "warning": { "hex": "#F5A623", "space": "srgb" },
      "error": { "hex": "#E02424", "space": "srgb" },
      "info": { "hex": "#3B6EF5", "space": "srgb" }
    }
  },
  "ui": {
    "themes": {
      "light": { /* theme tokens */ },
      "dark": { /* theme tokens */ }
    }
  }
}
```

---

## Export Formats

### CSS Variables

Outputs `:root` variables plus theme-specific selectors:

```css
:root {
  --color-primary: #3B6EF5;
  --color-secondary: #1CC7A1;
  --neutral-500: #7E8AA3;
}

[data-theme="light"] {
  --background: #F7F8FA;
  --text: #151825;
}
```

### Tailwind Config

Outputs a JavaScript module for `tailwind.config.js`:

```javascript
export default {
  theme: {
    extend: {
      colors: {
        primary: "#3B6EF5",
        neutral: {
          "500": "#7E8AA3",
          "600": "#5C667D"
        }
      }
    }
  }
};
```

### Figma Tokens

Outputs JSON compatible with Tokens Studio for Figma plugin.

---

## Best Practices

1. **Always check `/mnt/user-data/uploads/`** before running the compiler
2. **Validate that images exist** before processing
3. **Handle errors gracefully** - image processing can fail if files are corrupted
4. **Show the user what was extracted** - include the debug palette in your response
5. **Ask which export formats they want** - don't generate all formats unless requested
6. **Save outputs to `/mnt/user-data/outputs/`** so users can download them

---

## Example Workflow

**User:** "Can you extract colors from these images and give me CSS variables?"

**Claude response pattern:**
1. Check uploads directory
2. Run `compile_from_images()` with the image paths
3. Show extracted palette (debug info)
4. Run `export_css_variables()` 
5. Save to `/mnt/user-data/outputs/colors.css`
6. Use `present_files` to share the CSS file

---

## Limitations

- Maximum 5 images per compilation
- Images are resized to 768px max dimension for processing
- Only extracts colors - does not generate layouts, copy, or designs
- No persistent storage - each compilation is independent
- Color extraction uses histogram bucketing (deterministic but approximate)

---

## Technical Details

**Algorithm:**
1. Resize images to 768px max dimension
2. Convert to RGB/RGBA
3. Calculate average color from non-transparent pixels
4. Build histogram with 24-step color quantization
5. Rank colors by frequency
6. Pick top 8 distinct colors (minimum 40-unit distance)
7. Map extracted colors to structured system

**Dependencies:**
- Pillow (PIL) for image processing
- NumPy for color calculations and histogram analysis

---

## Troubleshooting

**"Image processing failed"**: The image file may be corrupted or in an unsupported format. Ask user to re-upload.

**"No colors extracted"**: Image may be fully transparent or monochrome. Check the debug output.

**"Colors don't match expectations"**: Try the other mode (`brand_first` vs `ui_first`) or suggest adjusting the source images.

---

Created by Heathen ([x.com/heathenft](https://x.com/heathenft))
