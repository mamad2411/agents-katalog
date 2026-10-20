---
name: mcp-inline-snapshot-parsing
description: Extract structured data from Chrome DevTools MCP inline JSON-encoded accessibility tree snapshots — the correct workflow for parsing `take_snapshot(verbose=true)` output when `filePath` is omitted and the result is a single-line JSON blob with escaped newlines and quotes.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mcp, chrome-devtools, snapshot, parsing, accessibility-tree]
    triggers: [parse snapshot, inline snapshot, json-encoded snapshot, take_snapshot verbose, chrome devtools mcp snapshot, parse mcp output]
    related_skills: [hermes-browser-internals, a betting-pipeline skill]
---

# MCP Inline Snapshot Parsing

When `mcp__chrome_devtools_mcp__take_snapshot(verbose=true)` is called **without `filePath`**, the tool returns a single-line JSON-encoded string embedded in a `{"result": "..."}` wrapper. The escaped characters (`\\n`, `\\"`) make grep, `search_files`, and direct regex on the Hermes cache file all fail on content patterns.

## The Format

The raw tool output is a JSON object:
```json
{"result": "## Latest page snapshot\nuid=8_0 RootWebArea \"MLB Odds\"\n  uid=8_1 ignored\n    uid=8_2 generic\n      ..."}
```

When this exceeds ~100KB, Hermes saves it to a cache file under `cache/terminal/hermes-results/call_*.txt` — still in the same escaped JSON format.

## The Problem

| What you'd like to search for | Why it fails |
|---|---|
| `grep 'button "−169"'` | The file has `button \\"−169\\"` (escaped backslash+quote) |
| `rg 'StaticText "Today"'` | Same escaping issue |
| `search_files(pattern="button")` | File is one line — no newline-separated matches |
| `re.findall(r'button "..."', text)` | Python reads `\\"` as literal `\"`, breaking the match |

After `json.loads`, the escapes are resolved and you get a real multi-line string. But the raw cache file is unusable with grep/rg/search_files for content patterns.

## Correct Workflow

### Step 1: Parse the outer JSON wrapper

```python
import json

with open("path/to/hermes-results/call_RANDOM_HASH.txt", "r") as f:
    raw = f.read()

data = json.loads(raw)       # Parses {"result": "..."} outer wrapper
text = data["result"]        # Decodes \\n → real newlines, \\" → real quotes
lines = text.split("\n")     # Now a usable line array
```

### Step 2: Verify parsing worked

```python
for i in range(min(5, len(lines))):
    print(f"L{i}: {lines[i][:100]}")
# Expected: uid=8_0 RootWebArea "Page Title" url="..."
```

### Step 3: Process with Python regex

```python
import re

# Find all button texts (odds, run lines, totals)
buttons = []
for i, line in enumerate(lines):
    m = re.search(r'button "([^"]+)"', line)
    if m:
        buttons.append((i, m.group(1)))

# Find all team names
teams = []
for i, line in enumerate(lines):
    m = re.search(r'-logo [A-Z]{2,3} ([A-Za-z ]+?)" url=', line)
    if m:
        teams.append((i, m.group(1).strip()))
```

### Step 4: Categorize button values

```python
for line_no, btn_text in buttons:
    if re.match(r'^[+-]\d{2,4}$', btn_text):
        print(f"L{line_no}: MONEYLINE {btn_text}")
    elif re.match(r'^[+-]?\d+\.\d+\s[+-]\d+', btn_text):
        print(f"L{line_no}: RUN LINE {btn_text}")
    elif re.match(r'^[OU]\s\d+\.?\d*\s', btn_text):
        print(f"L{line_no}: TOTAL {btn_text}")
```

## Pitfalls

1. **Cache file path changes per call** — check the tool result for the exact path under `hermes-results/call_*.txt`. Always capture it from the tool output.

2. **`json.loads` fails if the file was truncated** — Hermes caps tool outputs at ~162KB. If the raw snapshot exceeds this, the cache file will be a partial JSON value and `json.loads` raises `JSONDecodeError`. Fall back to MLB Stats API or other non-browser data sources.

3. **Unicode minus signs** — Moneyline odds use Unicode U+2212 (`−`) not ASCII `-` (e.g., `−169`). After `json.loads`, this character survives as-is. Match with `[−-]` in Python regex or include the explicit character.

4. **Do NOT use `search_files` or `grep` on the cache file for content** — they can find line numbers by `uid=` patterns (for orientation), but any pattern containing quotes, minus signs, or odds values will be corrupted by the escaping. Reserve them for line-number discovery only.

5. **Do NOT use `execute_code` with `read_file` for this** — `read_file` returns the cache file as one long line (no split on escaped `\\n`). The `json.loads` + split pattern requires a Python script written to disk with `write_file` and executed via `terminal()`.

6. **Snapshot output has two formats:**
   - **Inline (no filePath):** Returns as JSON-encoded string inside `{"result": "..."}` — the subject of this skill
   - **File-based (with filePath):** Writes to a file with real newlines — works with grep/search_files normally (see `draftkings-snapshot-parsing.md` for that workflow)
   - Use filePath whenever the MCP workspace allows writes; reserve the inline approach for when workspace restrictions block file writes

## Related Skills

- `a betting-pipeline skill` — references/draftkings-snapshot-parsing.md covers file-based snapshot workflow
- `hermes-browser-internals` — Chrome DevTools MCP architecture and session management
