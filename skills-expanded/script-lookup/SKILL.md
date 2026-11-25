---
name: script-lookup
description: Locate a specific FileMaker script in the `agent/xml_parsed/` folder, resolving to the matching pair of scripts from `scripts_sanitized` - human-readable version - and the Save a Copy as XML (SaXML)  version. Use when the user says "review/refactor/optimize/open/show" a script, mentions "script ID", or asks about a specific script by name.
---

# Script Lookup

Locate a FileMaker script by ID or name, resolving to the paired human-readable and Save-As-XML files. Optimized for minimum tool calls.

**Performance target**: 4 tool calls for ID-based lookups, 5 for name-based.

## Interpreting the user's request

### Script ID extraction

Treat these as script IDs:

- "ID 123", "script 123", "script id: 123", "#123"

### Script name extraction

If no ID is present, treat the remainder as a script name hint, e.g.:

- "review the new invoice for client script" → name hint: "new invoice for client"

Normalize name hints:

- Case-insensitive
- Remove the trailing word "script"
- Collapse repeated whitespace/punctuation

## Lookup workflow

### Step 1 — Index lookup (PARALLEL)

**This is the critical optimization.** `agent/context/{solution}/scripts.index` is a pipe-delimited file (`ScriptName|ScriptID|FolderPath`) covering every script in the solution. Use it as the **primary lookup source** — never start with filesystem traversal.

Run these in **parallel** (single message, multiple tool calls):

**Tool call A — Grep the index:**

- **ID-based**: `grep "|{id}|" agent/context/*/scripts.index` — returns the exact match plus the solution name from the file path.
- **Name-based**: `grep -i "{name_hint}" agent/context/*/scripts.index` — returns matching rows. If the user also mentions a solution name, include it in the grep path: `agent/context/{solution_hint}*/scripts.index`.

**Tool call B — List sandbox:**

- `ls agent/sandbox/` — check for any existing fmxmlsnippet files (in-progress work).

### Step 2 — Resolve paths and read excerpt

From the index result, extract:
- **Script name** (column 1)
- **Script ID** (column 2)
- **Folder path** (column 3)
- **Solution name** (from the index file path: `agent/context/{solution}/scripts.index`)

**Multi-solution handling**: If index results come from multiple solution paths, or the user mentions a specific solution, resolve to one. If ambiguous, use `AskUserQuestion` to ask which solution.

**Derive file paths** — the sanitized filename follows the pattern `{ScriptName} - ID {ScriptID}.txt`, nested inside a folder whose name starts with the folder path value from the index. Since the folder's own ID suffix isn't in the index, use a glob:

- Sanitized: `agent/xml_parsed/scripts_sanitized/{solution}/{FolderPath}*/{ScriptName} - ID {ScriptID}.txt`
- Save-As-XML: `agent/xml_parsed/scripts/{solution}/{FolderPath}*/{ScriptName} - ID {ScriptID}.xml`

For **top-level scripts** (empty folder path in index): files are directly in `agent/xml_parsed/scripts_sanitized/{solution}/`.

**Sandbox match**: From the sandbox listing (Step 1B), check if any file matches the script name (sandbox files don't include IDs — match by name).

Run in **parallel**:

**Tool call A — Glob for sanitized file:**
Use Bash: `ls agent/xml_parsed/scripts_sanitized/"{solution}"/"{FolderPath}"*/*"ID {ScriptID}"* 2>/dev/null || ls agent/xml_parsed/scripts_sanitized/"{solution}"/*"ID {ScriptID}"* 2>/dev/null`

**Tool call B — Read first 20 lines of the sanitized script** (for the excerpt). If you already know the exact path from the glob, read it directly. Otherwise, combine with tool call A by using a single Bash command that finds and reads:
```bash
file=$(find "agent/xml_parsed/scripts_sanitized/{solution}" -name "*ID {ScriptID}*" -type f | head -1) && head -20 "$file"
```

For **name-based lookups** where multiple index rows matched: pick the best candidate using the matching rules below, then resolve paths for that candidate.

### Step 3 — Script match report + confirmation

Present the report and confirm in one response:

**Selected script**
- Name: `{script name}`
- ID: `{id}`
- Confidence: High/Medium/Low (why)

**Paths found**
- Sanitized (readable): `{path or "not found"}`
- Save-As-XML (reference): `{path or "not found"}`
- fmxmlsnippet (editable base): `{path in agent/sandbox, or "not found"}`

**Alternates (if any)**
- Up to 3–5 other candidate scripts from the index results (name + ID)

**Quick excerpt**
- First few lines from `scripts_sanitized` to confirm identity

Then use `AskUserQuestion`: "Is this the correct script? — {Script Name} (ID: {id}) in {solution}"
- Options: `yes` — "Yes, proceed" / `no` — "No, that's not it — let me clarify"

### Step 4 — Post-confirmation

**If confirmed:**

- If an fmxmlsnippet already exists in `agent/sandbox/`, use it as the editable base.
- If none exists, convert the Save-As-XML source:
  ```bash
  python3 agent/scripts/fm_xml_to_snippet.py "agent/xml_parsed/scripts/{solution}/{folder}/{ScriptName} - ID {ScriptID}.xml" "agent/sandbox/{ScriptName}.xml"
  ```
- Proceed with the next action (handoff to review/refactor, or simply present the script).

**If declined:**

- Ask for a corrected script name or ID.
- Re-run from Step 1.

## Name-based matching rules

When the index grep returns multiple rows, rank candidates:

1. **Exact name match** (case-insensitive) — highest confidence
2. **Contains match** (all tokens from the hint present in the candidate name)
3. **Fuzzy match** (most tokens match) — pick the best, include alternates in report

Pick the best candidate and continue. The confirmation step is the redirect gate — don't block on a separate disambiguation question unless confidence is truly Low across all candidates.

## Fallback: no index available

If `agent/context/` has no `scripts.index` files, fall back to filesystem search:

1. `ls agent/xml_parsed/scripts_sanitized/` — determine solution subfolders.
   - One subfolder → use automatically.
   - Multiple → `AskUserQuestion` to disambiguate.
2. Search within the solution subfolder:
   - ID: `find "agent/xml_parsed/scripts_sanitized/{solution}" -name "*ID {id}*" -type f`
   - Name: `find "agent/xml_parsed/scripts_sanitized/{solution}" -iname "*{hint}*" -type f`
3. Continue from Step 2 (resolve paths and read excerpt).

**If `agent/xml_parsed/` does not exist or is empty**, report that explicitly and stop.

## Mapping between sanitized and Save-As-XML variants

The sanitized and XML variants are a pair sharing the same name pattern: `{ScriptName} - ID {ScriptID}` with `.txt` vs `.xml` extension, in mirrored folder structures under `scripts_sanitized/` vs `scripts/`.

When ID and name conflict, **trust ID**.

## Handoff: when the user asked to "review" or "refactor"

If the user request is a review/refactor/optimization:

- Use this lookup to identify the correct script and its artifacts.
- Then follow the existing `script-review` or `script-refactor` workflow:
  - Prefer an existing fmxmlsnippet version in `agent/sandbox/` as the base.
  - If none exists, translate from Save-As-XML using `agent/scripts/fm_xml_to_snippet.py`.

## Examples

### Example 1 — ID-based lookup (fast path)

User: "Lets work on script 104"

**Step 1 (parallel):**
- Grep: `grep "|104|" agent/context/*/scripts.index` → `Quick Find Clients|104|Quick Find` in `Invoice Solution`
- List: `ls agent/sandbox/` → check for existing "Quick Find Clients" file

**Step 2 (parallel):**
- Glob: `ls agent/xml_parsed/scripts_sanitized/"Invoice Solution"/"Quick Find"*/*"ID 104"*`
- Read: first 20 lines of the matched sanitized file

**Step 3:** Report + confirm → "Is this the correct script? — Quick Find Clients (ID: 104) in Invoice Solution"

**Step 4:** On confirmation → convert to sandbox if no fmxmlsnippet exists.

**Tool calls: 4** (2 parallel + 1 read/glob + 1 confirm) + 1 convert if needed.

### Example 2 — Name-based lookup (fuzzy)

User: "Let's work on the invoices quick find for the invoice solution"

**Step 1 (parallel):**
- Grep: `grep -i "quick find" agent/context/"Invoice Solution"/scripts.index` → multiple matches:
  - `Quick Find Clients|104|Quick Find`
  - `Quick Find Invoices|106|Quick Find`
  - `Quick Find Products|108|Quick Find`
  - `Quick Find Staff|110|Quick Find`
- List: `ls agent/sandbox/`

Best match: "Quick Find Invoices" (contains "invoices" token from hint).

**Step 2:** Resolve paths for ID 106, read excerpt.

**Step 3:** Report with alternates (104, 108, 110) + confirm.

**Step 4:** Convert on confirmation.

**Tool calls: 5** (2 parallel + 1 resolve + 1 confirm + 1 convert).

### Example 3 — Multiple solutions

User: "Review the New Invoice script"

**Step 1:**
- Grep: `grep -i "new invoice" agent/context/*/scripts.index` → results from two solutions

**Step 1.5:** `AskUserQuestion` to disambiguate solution, then continue from Step 2.

### Example 4 — Ambiguous name

User: "Show me the invoice script"

**Step 1 (parallel):**
- Grep: `grep -i "invoice" agent/context/*/scripts.index` → many matches
- List: `ls agent/sandbox/`

Pick best candidate, include alternates prominently. Confirmation step acts as redirect gate.
