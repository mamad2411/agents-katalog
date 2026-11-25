---
name: icon-swap
description: Swap SVG icons in FileMaker Button and ButtonBar layout objects with icons from open-source libraries (Lucide, Heroicons, Tabler, Phosphor, Bootstrap, Iconoir, MDI, Ionicons). Handles stroke-to-fill conversion for FM compatibility. Use when the developer says "swap icons", "replace icons", "change icons to", "use lucide icons", "use heroicons", or wants to update button icons from a library.
compatibility: Stroke-to-fill conversion requires a Python venv with cairosvg and Pillow, plus the potrace CLI. Fill-based libraries (Heroicons solid, MDI, Bootstrap) work without conversion dependencies.
---

# Icon Swap

Replace embedded SVG icons in FileMaker layout objects with icons from open-source libraries. Supports both fill-based and stroke-based icon libraries — stroke-based icons are automatically converted to FM-compatible filled SVGs via a rasterise-then-trace pipeline.

---

## Step 0: Ensure dependencies

### Always available (no deps)

The icon extraction and XML replacement functionality uses stdlib Python only. Swapping icons from **fill-based** libraries (Heroicons solid, MDI, Bootstrap Icons, Phosphor, Tabler filled, Ionicons filled) works without any extra dependencies.

### Required for stroke-based libraries

Stroke-based libraries (Lucide, Heroicons outline, Tabler, Iconoir, Ionicons outline) require conversion dependencies. Check first:

```bash
python3 agent/scripts/fm_svg_convert.py --check-deps
```

If deps are missing, guide the developer through setup:

> **Stroke-to-fill conversion requires additional dependencies.**
>
> These are needed because FileMaker button icons only support filled shapes — stroke-based SVG libraries (like Lucide) must be converted.
>
> **Option A: venv in the project folder (recommended)**
> ```bash
> python3 -m venv agent/.venv
> source agent/.venv/bin/activate
> pip install cairosvg Pillow
> ```
>
> **System dependency (potrace):**
> ```bash
> brew install potrace   # macOS
> ```
>
> Once set up, run commands with the venv active, or prefix with `agent/.venv/bin/python3`.

If the developer declines, suggest a **fill-based alternative library** instead:
- Lucide (stroke) → suggest **Heroicons solid** or **Bootstrap Icons** as fill-based alternatives
- Tabler (stroke) → suggest **Tabler filled** or **MDI**

---

## Step 1: Determine input source

Same as `icon-extract` skill — the input can come from:

**A) File in sandbox:**
```bash
python3 agent/scripts/fm_icon_extract.py agent/sandbox/<filename>.xml --json
```

**B) Clipboard via companion server:**
```bash
curl -s http://local.hub:8765/clipboard | python3 -c "
import json, sys
data = json.load(sys.stdin)
if data.get('success'):
    with open('agent/sandbox/_clipboard_input.xml', 'w') as f:
        f.write(data['xml'])
    print('Saved clipboard content to agent/sandbox/_clipboard_input.xml')
else:
    print('ERROR:', data.get('error', 'Unknown error'), file=sys.stderr)
    sys.exit(1)
"
```

Fall back to `host.docker.internal:8765` if `local.hub:8765` is unreachable.

**C) Developer pastes XML directly** — save to sandbox and proceed.

---

## Step 2: Extract and catalogue current icons

Run extraction:
```bash
python3 agent/scripts/fm_icon_extract.py agent/sandbox/<input>.xml --json
```

Also save individual SVGs for visual reference:
```bash
python3 agent/scripts/fm_icon_extract.py agent/sandbox/<input>.xml --output-dir agent/sandbox/icons_current/
```

Present the catalogue to the developer:

| # | Label | Current Icon | Suggested Replacement | Preview |
|---|-------|--------------|-----------------------|---------|
| 0 | Dashboard | grid/table (filled) | `layout-dashboard` | [view](https://lucide.dev/icons/layout-dashboard) |
| 1 | Companies | building (filled) | `building-2` | [view](https://lucide.dev/icons/building-2) |
| 2 | Contacts | person (filled) | `contact` | [view](https://lucide.dev/icons/contact) |

Replace the preview URLs with the correct pattern for the target library (see URL patterns in Step 3).

---

## Step 3: Build the icon mapping

### Auto-matching (attempt first)

Use the button name and label to suggest matching icons from the target library. Common mappings for business apps:

| Label pattern | Lucide suggestion | Heroicons suggestion |
|---|---|---|
| Dashboard | `layout-dashboard` | `squares-2x2` |
| Company/Companies | `building-2` | `building-office-2` |
| Contacts | `contact` | `user-group` |
| Leads | `target` | `flag` |
| Opportunities | `trending-up` | `chart-bar` |
| Quotes/Estimates | `file-text` | `document-text` |
| Orders | `shopping-cart` | `shopping-cart` |
| Purchase Orders/POs | `clipboard-list` | `clipboard-document-list` |
| Shipments | `truck` | `truck` |
| Receiving | `package-check` | `inbox-arrow-down` |
| Returns | `undo-2` | `arrow-uturn-left` |
| Work Orders | `wrench` | `wrench-screwdriver` |
| Reports | `bar-chart-3` | `chart-bar` |
| Settings/Setup | `settings` | `cog-6-tooth` |
| Builds | `hammer` | `wrench` |
| Inventory | `warehouse` | `archive-box` |
| Invoices | `receipt` | `document` |
| Payments | `credit-card` | `credit-card` |
| Calendar/Schedule | `calendar` | `calendar` |
| Search | `search` | `magnifying-glass` |
| Users | `users` | `users` |
| Home | `home` | `home` |
| Email | `mail` | `envelope` |
| Phone | `phone` | `phone` |
| Notes | `sticky-note` | `document` |

### Present mapping for approval

Always present the proposed mapping and ask the developer to confirm or override before proceeding. Include a **Preview** column with a direct link to the icon on the library's website so the developer can visually verify each choice.

**Icon preview URL patterns by library:**

| Library | URL pattern |
|---|---|
| Lucide | `https://lucide.dev/icons/{name}` |
| Heroicons (outline/solid) | `https://heroicons.com/outline#{name}` or `https://heroicons.com/solid#{name}` |
| Tabler | `https://tabler.io/icons/icon/{name}` |
| Phosphor | `https://phosphoricons.com/icons/{name}` |
| Bootstrap | `https://icons.getbootstrap.com/icons/{name}/` |
| Iconoir | `https://iconoir.com/icons/{name}` |
| MDI | `https://pictogrammers.com/library/mdi/icon/{name}/` |
| Ionicons | `https://ionic.io/ionicons/ionicons/#{name}` |

Example presentation:

> **Proposed icon mapping** (library: Lucide)
>
> | # | Label | Replacement icon | Preview |
> |---|-------|-----------------|---------|
> | 0 | Dashboard | `layout-dashboard` | [view](https://lucide.dev/icons/layout-dashboard) |
> | 1 | Companies | `building-2` | [view](https://lucide.dev/icons/building-2) |
> | ... | | | |
>
> Edit any names, or reply **go** to proceed.

### Developer-provided mapping

If the developer provides explicit icon names (one-for-one list), use those directly. The developer may provide them as:
- A numbered list: `0: home, 1: building, 2: users`
- A comma-separated list (positional): `home, building, users, target, ...`
- A JSON object: `{"Dashboard": "layout-dashboard", "Companies": "building-2"}`

---

## Step 4: Fetch and convert replacement icons

For each icon in the mapping:

### 4a. Fetch from library

```bash
python3 agent/scripts/fm_svg_convert.py --fetch lucide:layout-dashboard --fm -o agent/sandbox/icons_new/layout-dashboard.svg
```

If the icon is not found (404), inform the developer and ask for an alternative name. Common issues:
- Plural vs singular (`users` vs `user`)
- Hyphenation (`shopping-cart` vs `shoppingcart`)
- Library-specific naming (`file-text` in Lucide vs `document-text` in Heroicons)

### 4b. Convert stroke-based icons

If the library is stroke-based, the `--fm` flag on `fm_svg_convert.py` handles conversion automatically. If conversion deps are not available, the script will error — fall back to a fill-based library.

### 4c. Format for FileMaker

Whether fetched as fill-based or converted from stroke, the final SVG must have:
- `<g class="fm_fill">` wrapping all shape elements
- `viewBox="0 0 24 24"` (or matching dimensions)
- `width` and `height` attributes with `px` units
- No `stroke` attributes on any element
- No `fill="none"` on shape elements
- XML declaration: `<?xml version="1.0" encoding="utf-8"?>`

The `format_for_fm()` function in `fm_svg_convert.py` handles this, and is also invoked by the `--fm` flag.

For fill-based libraries that don't need stroke conversion, use the formatting function directly:
```python
from agent.scripts.fm_svg_convert import format_for_fm
formatted = format_for_fm(svg_text)
```

Or from the CLI:
```bash
python3 -c "
import sys; sys.path.insert(0, '.')
from agent.scripts.fm_svg_convert import format_for_fm, fetch_icon
svg = fetch_icon('heroicons-solid', 'building-office-2')
print(format_for_fm(svg))
" > agent/sandbox/icons_new/building-office-2.svg
```

---

## Step 5: Build the replacement XML

Use the `replace_icons_in_file` function from `fm_icon_extract.py`:

```python
python3 -c "
import sys; sys.path.insert(0, '.')
from agent.scripts.fm_icon_extract import replace_icons_in_file

# Read all replacement SVGs
replacements = {}
# Map: index -> path to replacement SVG
mapping = {
    0: 'agent/sandbox/icons_new/layout-dashboard.svg',
    1: 'agent/sandbox/icons_new/building-2.svg',
    # ...
}
for idx, path in mapping.items():
    with open(path) as f:
        replacements[idx] = f.read()

replace_icons_in_file(
    'agent/sandbox/<input>.xml',
    replacements,
    'agent/sandbox/<input>_updated.xml'
)
"
```

The function:
- Updates the `<HexData>` with the new SVG encoded as uppercase hex
- Updates the `<Stream size="">` attribute to match the new byte count
- Preserves the `GLPH` stream and all other XML structure unchanged
- Writes to `_updated` suffix file

---

## Step 6: Deploy or deliver

**If the input came from clipboard**, write the updated XML back to clipboard:
```bash
python3 agent/scripts/clipboard.py write agent/sandbox/<input>_updated.xml
```

Then instruct the developer:
> The updated layout object is on your clipboard. In FileMaker Layout Mode:
> 1. Delete the original button bar
> 2. **Cmd+V** to paste the updated version

**If the input came from a file**, inform the developer:
> The updated XML is at `agent/sandbox/<input>_updated.xml`. You can load it to clipboard with:
> ```
> python3 agent/scripts/clipboard.py write agent/sandbox/<input>_updated.xml
> ```

---

## Supported icon libraries

| Library | ID | Style | Conversion needed? |
|---|---|---|---|
| Lucide | `lucide` | stroke | Yes |
| Heroicons (outline) | `heroicons-outline` | stroke | Yes |
| Heroicons (solid) | `heroicons-solid` | fill | No |
| Tabler Icons | `tabler` | stroke | Yes |
| Tabler Icons (filled) | `tabler-filled` | fill | No |
| Phosphor Icons | `phosphor` | fill | No |
| Bootstrap Icons | `bootstrap` | fill | No |
| Iconoir | `iconoir` | stroke | Yes |
| Material Design Icons | `mdi` | fill | No |
| Ionicons (outline) | `ionicons-outline` | stroke | Yes |
| Ionicons (filled) | `ionicons-filled` | fill | No |

Browse icons at their respective websites to find names:
- Lucide: https://lucide.dev/icons
- Heroicons: https://heroicons.com
- Tabler: https://tabler.io/icons
- Bootstrap: https://icons.getbootstrap.com
- MDI: https://materialdesignicons.com
- Phosphor: https://phosphoricons.com
- Iconoir: https://iconoir.com
- Ionicons: https://ionic.io/ionicons

---

## Troubleshooting

- **Icon not found (404)**: Check the exact icon name on the library's website. Names are kebab-case.
- **Conversion produces blank SVG**: The render size may be too small for fine details. Try `--render-size 2048`.
- **Converted icon looks rough**: Potrace tracing is lossy. For critical icons, consider using a fill-based library instead, or manually adjusting the traced SVG.
- **FM doesn't show the icon**: Verify the SVG has `<g class="fm_fill">` and no stroke attributes. Check that the XML declaration is present.
- **Size mismatch**: The `stream_size` must match the actual byte count of the hex-decoded SVG. The replacement function handles this automatically.
