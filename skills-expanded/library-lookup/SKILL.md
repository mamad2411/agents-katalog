---
name: library-lookup
description: Look up and integrate reusable code from the curated snippet library — scripts, step patterns, custom functions, layout objects, and web viewer components. Use when the developer says "use this from the library", "look up the snippet for", "include the library script", "add a timeout loop", or references any library item by name or keyword.
---

# Library Lookup

The library is a curated collection of reusable fmxmlsnippet code. The full manifest — including file paths, descriptions, and keyword tags — lives at:

```
agent/library/MANIFEST.md
```

---

## Using the library

**Step 1 — Read the manifest.**
Always read `agent/library/MANIFEST.md` first. It is the filter; do not browse the library folder directly.

**Step 2 — Match keywords to the task.**
Scan the manifest's keyword column against the current task. If any entry matches, proceed to step 3. If nothing matches, skip the library entirely.

**Step 3 — Read only matching files.**
Use the Read tool to open the specific file(s) identified in step 2. Each file path in the manifest is relative to `agent/library/` and includes the `.xml` extension.

**Step 4 — Adapt and integrate.**
- Replace placeholder field/table/ID references with values from CONTEXT.json.
- Adjust placeholder variable names to match the current script's conventions.
- Keep structural and purpose comments; remove or update comments that describe the template itself.
- When incorporating a library Script item, extract the inner `<Step>` elements only — do not include the enclosing `<Script>` wrapper unless explicitly requested. Output remains in `<fmxmlsnippet type="FMObjectList">` format.

**On direct developer reference** — when a developer names or quotes a library item (e.g. "use the HTTP request script", "add the timeout loop", "include a spinner"), read the manifest to locate it, then read and output that file.

---

## Updating the manifest

The manifest is maintained separately from the skill so it reflects the actual contents of the library folder at any time. Two approaches:

### Ask AI to regenerate

Ask AI:

> "Scan the `agent/library` folder, compare it against `agent/library/MANIFEST.md`, and update the manifest — adding entries for any new files and removing entries for any deleted files. For new files, read each one to write an accurate description and relevant keyword tags."

AI will list the folder, diff against the current manifest, read any new files, and rewrite `MANIFEST.md` in place.

### Edit manually

Open `agent/library/MANIFEST.md` and add or remove rows directly. Follow the existing column format:

```
| `Category/filename` | One-sentence description of what the code does | keyword1, keyword2, keyword3 |
```

Keep keywords concrete and drawn from how a developer would describe the need — not from the file name itself.
