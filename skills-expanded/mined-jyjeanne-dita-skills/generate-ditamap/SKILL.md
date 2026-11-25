---
name: generate-ditamap
description: Generates a valid DITA 1.3 map template. Use this skill when you need a correctly structured starting point for a DITA map with topicref placeholders, key definitions, and an optional relationship table. Output includes the correct DOCTYPE declaration.
compatibility: Python 3.9+. No third-party dependencies.
---

## Overview

Generates a DITA 1.3 `<map>` template from a title and ID.

## Usage

```bash
python scripts/generate_ditamap.py "My Map Title" my-map-id

# With topic hrefs pre-filled
python scripts/generate_ditamap.py "My Map Title" my-map-id --topics intro.dita config.dita usage.dita
```

## Output

Well-formed XML to stdout including:
- `<?xml?>` + `<!DOCTYPE map PUBLIC "-//OASIS//DTD DITA 1.3 Map//EN">` 
- `<title>`, one `<topicref>` per `--topics` argument (or two placeholder refs)
- A `<keydef>` block for each topic ref
- A skeleton `<reltable>` with two columns

## Common edge cases

- `href` values use forward slashes even on Windows (DITA convention)
- `<keydef>` `keys` attribute is derived from the filename stem (e.g., `intro.dita` → `key-intro`)
- `<reltable>` is scaffolded but empty; remove it if not needed
