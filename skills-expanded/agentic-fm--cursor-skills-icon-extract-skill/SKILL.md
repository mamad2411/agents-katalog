---
name: icon-extract
description: Extract SVG icons from FileMaker layout objects (Button, ButtonBar) and save as individual SVG files. Use when the developer says "extract icons", "show me the icons", "get the icons from", "export the SVGs", "what icons are in this", or wants to inspect or reuse icons embedded in FM layout XML.
---

# Icon Extract

Extract embedded SVG icons from FileMaker layout object XML. Parses `<Stream><Type>SVG </Type><HexData>...</HexData></Stream>` elements inside Button and ButtonBar objects, decodes the hex-encoded SVGs, and saves them as individual files.

This skill uses no external dependencies — it is stdlib-only Python.

---

## Step 1: Determine the input source

The developer may provide input in one of three ways:

**A) File in sandbox** — the developer has placed or named an XML file:
```bash
python3 agent/scripts/fm_icon_extract.py agent/sandbox/<filename>.xml --json
```

**B) Clipboard** — the developer says the layout object is on the clipboard. Read it via the companion server:
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

If the companion server is not reachable, try the Docker-internal hostname:
```bash
curl -s http://host.docker.internal:8765/clipboard | python3 -c "..."
```

If neither works, instruct the developer:
> Please run this command to save the clipboard content:
> ```
> python3 agent/scripts/clipboard.py read agent/sandbox/_clipboard_input.xml
> ```

Then proceed with the saved file.

**C) XML text pasted directly** — save to `agent/sandbox/_clipboard_input.xml` and proceed.

---

## Step 2: Extract icons

Run the extraction script:
```bash
python3 agent/scripts/fm_icon_extract.py agent/sandbox/<input>.xml --json
```

This outputs a JSON array with one entry per icon:
```json
{
  "index": 0,
  "button_name": "NAV:Dashboard",
  "label": "Dashboard",
  "is_stroke": false,
  "has_fm_fill": true,
  "viewbox": "0 0 24 24",
  "stream_size": 941,
  "byte_size": 941
}
```

Present a summary table to the developer:

| # | Button Name | Label | Format | ViewBox |
|---|-------------|-------|--------|---------|
| 0 | NAV:Dashboard | Dashboard | filled | 0 0 24 24 |
| 1 | NAV:Company | Companies | filled | 0 0 40 42.67 |
| ... | | | | |

Note whether icons are stroke-based (would need conversion for FM) or already filled.

---

## Step 3: Save individual SVG files (if requested)

If the developer wants individual files:
```bash
python3 agent/scripts/fm_icon_extract.py agent/sandbox/<input>.xml --output-dir agent/sandbox/icons/
```

Files are named from the button label (e.g., `dashboard.svg`, `companies.svg`). Duplicates get a numeric suffix.

Report the saved file paths to the developer.

---

## Step 4: Display or describe icons

If the developer asks what an icon looks like, read the SVG content from the extracted file and describe its visual appearance based on the SVG shapes (paths, rects, circles, etc.). Common patterns:

- Grid of rectangles = dashboard/spreadsheet
- Person silhouette = contacts/user
- Building shape = company
- Gear/cog = settings
- Document/page = reports
- Truck = shipments
- Box = orders/packages

---

## Notes

- The extraction script is **read-only** — it never modifies the input XML.
- The `icon-swap` skill depends on this extraction capability for its workflow.
- All extracted SVGs preserve the original hex encoding fidelity — re-encoding produces identical bytes.
- The GLPH stream (typically `01`) is metadata that pairs with each SVG stream. The extraction report includes it for reference.
