---
name: excalidraw-diagram
description: Generate Excalidraw diagrams from text content as raw JSON scene data. Use when user asks to create diagrams, flowcharts, mind maps, or visual representations in Excalidraw format. Triggers on "Excalidraw", "画图", "流程图", "思维导图", "可视化", "diagram".
metadata:
  version: 1.3.1
---

# Excalidraw Diagram Generator (JSON-only)

Create Excalidraw diagrams from text content, outputting raw JSON scene data files.

## Workflow (concise)
1. Analyze content: concepts, relationships, hierarchy.
2. Choose diagram type (see `references/diagram-types.md`).
3. Build Excalidraw JSON elements.
4. Save a single JSON file in the current working directory.
5. You may edit the same file multiple times until JSON is complete.
6. Validate with `scripts/validate_excalidraw.py`.
7. Report file path and confirm.

## Output Rules (hard requirements)
- Output is **raw JSON only** (no Markdown, no code fences).
- Single file, extension: `*.excalidraw.json`.
- Start from `assets/scene_skeleton.json` and then edit in batches.
- JSON must be valid and directly renderable by Excalidraw.
 - **Execute tool restriction:** validation commands must run under `/workspace`. If the validator script is not in `/workspace`, copy it there before running.

## JSON Rules (hard requirements)
- Every element has a unique `id`.
- All text elements use `fontFamily: 5` and `lineHeight: 1.25`.
- Replace `"` with `『』`, and `()` with `「」` inside text.
- Include `appState` and `files` at top level.
- Keep elements within the recommended 0-1200 x 0-800 range.
 - **Layering:** element order is z-order. Put container shapes first, arrows second, and text elements last so text is never hidden.
 - **Binding:** for any labeled node, bind text to the container using `containerId` and add `{ "id": "text-id", "type": "text" }` to the container’s `boundElements`.
 - **Layout:** use deterministic layout constants and sizing rules from `references/layout-guidelines.md`.

## File Writing Guidance
- Prefer multiple small edits (5-15 elements per edit) over one huge write.
- Write nodes first, then arrows, then styles.

## Validation (execute-safe)
If `execute` returns `Error: execute only allows paths under /workspace`, do this:
1. Copy the validator into `/workspace` (write the script content there).
2. Run: `python /workspace/validate_excalidraw.py /workspace/<file>.excalidraw.json`

### Validation Template (paste + run)
Use this exact template when validation is needed:
1. `write_file` → `/workspace/validate_excalidraw.py` with the full script content from `scripts/validate_excalidraw.py`.
2. `execute` → `python /workspace/validate_excalidraw.py /workspace/<file>.excalidraw.json`

### Copy-Paste Validator Script (inline)
Use this block as the `write_file` content for `/workspace/validate_excalidraw.py`:
```python
#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def _err(msg: str) -> int:
    print(f"ERROR: {msg}", file=sys.stderr)
    return 1


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate_excalidraw.py <path-to-json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return _err(f"file not found: {path}")
    except OSError as exc:
        return _err(f"cannot read file: {exc}")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return _err(f"invalid JSON: {exc}")

    required = ["type", "version", "elements", "appState", "files"]
    missing = [k for k in required if k not in data]
    if missing:
        return _err(f"missing required keys: {', '.join(missing)}")

    if data.get("type") != "excalidraw":
        return _err(f"unexpected type: {data.get('type')!r}")

    elements = data.get("elements")
    if not isinstance(elements, list):
        return _err("elements must be a list")

    ids = []
    id_index = {}
    missing_ids = 0
    non_dict = 0
    text_font_warnings = 0
    text_line_warnings = 0

    for el in elements:
        if not isinstance(el, dict):
            non_dict += 1
            continue
        el_id = el.get("id")
        if not el_id:
            missing_ids += 1
        else:
            ids.append(el_id)
            id_index[el_id] = len(ids) - 1

        if el.get("type") == "text":
            if el.get("fontFamily") != 5:
                text_font_warnings += 1
            if el.get("lineHeight") != 1.25:
                text_line_warnings += 1

    if non_dict:
        return _err(f"elements contain {non_dict} non-object entries")
    if missing_ids:
        return _err(f"elements missing id: {missing_ids}")

    dupes = {x for x in ids if ids.count(x) > 1}
    if dupes:
        return _err(f"duplicate ids: {', '.join(sorted(dupes))}")

    # Z-order and binding checks (warnings)
    missing_bound = 0
    text_before_container = 0
    for idx, el in enumerate(elements):
        if not isinstance(el, dict):
            continue
        if el.get("type") == "text":
            cid = el.get("containerId")
            if cid:
                container = next((c for c in elements if isinstance(c, dict) and c.get("id") == cid), None)
                if container is None:
                    missing_bound += 1
                else:
                    bound = container.get("boundElements") or []
                    if not any(
                        b.get("id") == el.get("id") and b.get("type") == "text"
                        for b in bound
                        if isinstance(b, dict)
                    ):
                        missing_bound += 1
                    container_idx = id_index.get(cid)
                    if container_idx is not None and container_idx > idx:
                        text_before_container += 1

    if not isinstance(data.get("appState"), dict):
        return _err("appState must be an object")
    if not isinstance(data.get("files"), dict):
        return _err("files must be an object")

    print(f"OK: {len(elements)} elements, ids unique")
    if text_font_warnings:
        print(f"WARN: {text_font_warnings} text elements not using fontFamily=5")
    if text_line_warnings:
        print(f"WARN: {text_line_warnings} text elements not using lineHeight=1.25")
    if missing_bound:
        print(f"WARN: {missing_bound} text elements missing proper container binding")
    if text_before_container:
        print(f"WARN: {text_before_container} text elements appear before their containers (z-order risk)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## References
- `references/excalidraw-schema.md`
- `references/excalidraw-output-format.md`
- `references/diagram-types.md`
- `references/layout-guidelines.md`

## Tools
- `scripts/validate_excalidraw.py`
