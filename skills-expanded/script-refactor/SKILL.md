---
name: script-refactor
description: Analyse an existing FileMaker script and produce an improved version — better error handling, cleaner variable naming, consolidation of repeated logic — while preserving observable behaviour. At Tier 1 the refactored script is placed on the clipboard for manual paste. At Tier 3 the agent can autonomously deploy the replacement into Script Workspace. Triggers on phrases like "refactor", "improve this script", "clean up script", "modernise script", or "optimize script".
---

# Script Refactor

Analyse an existing script, identify improvements, and produce a refactored version as fmxmlsnippet — preserving observable behaviour while improving structure, error handling, and conventions.

---

## Step 1: Determine the automation tier

Read `agent/config/automation.json` and check `project_tier` (preferred) or `default_tier`:

- **Tier 1** — refactored script goes to clipboard with paste instructions
- **Tier 3** — agent can deploy the refactored script directly into Script Workspace, replacing the original

---

## Step 2: Locate the target script

If the developer has not already identified the script, use the `script-lookup` skill to find it.

Once identified, read the human-readable version from `agent/xml_parsed/scripts_sanitized/` to understand the current logic. Also check if an fmxmlsnippet version already exists in `agent/sandbox/`.

If neither exists, convert the SaXML version to fmxmlsnippet:

```bash
python3 agent/scripts/fm_xml_to_snippet.py "agent/xml_parsed/scripts/{solution}/{path}.xml" "agent/sandbox/{ScriptName}.xml"
```

Read `agent/CONTEXT.json` or index files for any field/layout/script references needed.

---

## Step 3: Resolve the call tree (parallel loading)

Before analysing logic, build the full picture of every script involved. The goal is to minimize tool calls by loading subscripts in parallel batches — one batch per depth level.

**Performance target**: For a script with N subscripts at depth 1, the call tree should load in 2 tool calls (1 grep + 1 parallel read), not N+1 sequential calls.

### 3a. Extract ALL Perform Script references in one pass

Grep the entry script's sanitized text for every `Perform Script` line at once. Extract all target script names from the results.

```bash
grep -i "Perform Script" "agent/xml_parsed/scripts_sanitized/{solution}/{path}.txt"
```

This returns lines like:
- `Perform Script [ "Subscript A" ; Parameter: $param ]` — extract `Subscript A`
- `Perform Script [ "Subscript B" ]` — extract `Subscript B`
- `Perform Script By Name [ ... ]` — flag as unresolvable (calculated name)

### 3b. Batch-resolve names to file paths

Take ALL extracted script names and resolve them to file paths in a **single grep** against the scripts index:

```bash
grep -E "Subscript A|Subscript B|Subscript C" "agent/context/{solution}/scripts.index"
```

This returns pipe-delimited rows (`ScriptName|ScriptID|FolderPath`) for every match. From each row, derive the sanitized file path:

- **With folder path**: `agent/xml_parsed/scripts_sanitized/{solution}/{FolderPath}*/{ScriptName} - ID {ScriptID}.txt`
- **Top-level** (empty folder path): `agent/xml_parsed/scripts_sanitized/{solution}/{ScriptName} - ID {ScriptID}.txt`

Since folder directory names include an ID suffix not in the index, use a glob to resolve the exact path if needed.

### 3c. Parallel-read ALL subscripts

Read ALL resolved subscript files in a **single message with multiple Read tool calls** — one per subscript. This replaces the old sequential "find one, read one, find next, read next" pattern.

For example, if the entry script calls 5 subscripts, issue 5 Read tool calls in a single message. All 5 load in parallel.

### 3d. Recurse (parallel per depth level)

After loading depth-1 subscripts, scan ALL of them for further `Perform Script` references. Collect any new (not yet visited) script names across all depth-1 subscripts, then repeat 3b–3c for the next depth level.

Track visited scripts by name to avoid cycles. Continue until no new references are found.

Each depth level adds at most 2 tool calls (1 batch grep + 1 parallel read), regardless of how many subscripts exist at that level.

### 3e. Present the call tree

Show the developer the full scope before starting analysis:

```
Call tree: [Script Name]
├── Subscript A
│   └── Subscript A1
├── Subscript B
└── Subscript C
```

Flag these edge cases:
- **Calculated names** — `Perform Script By Name` references cannot be statically resolved. Ask the developer to clarify.
- **Missing scripts** — references to scripts not found in `scripts_sanitized/` may be in a different solution file or deleted. Flag them.
- **Cycles** — scripts already visited are noted but not re-loaded.

---

## Step 4: Analyse the script

Read through the target script and its call tree. Identify issues in these categories:

### Error handling
- Missing `Set Error Capture [ On ]` / `Allow User Abort [ Off ]` header
- Steps that can fail without an immediate `Get ( LastError )` check
- Error data captured in separate steps instead of the single-expression `$errData` pattern (see `agent/docs/knowledge/error-data-capture.md`)
- Missing cleanup path (no revert/commit on failure)

### Structure
- Deeply nested If/Else chains that should be a single-pass loop
- Repeated logic that could be hoisted to a variable or extracted to a subscript
- Missing guard clauses (parameter validation, empty found set checks)
- Dead code (disabled steps that serve no documentation purpose)

### Naming and conventions
- Variable names that don't follow conventions (`agent/docs/CODING_CONVENTIONS.md`)
- Inconsistent naming within the script
- Magic numbers or repeated string literals that should be variables

### Performance
- Unnecessary layout switches
- Commit Records inside loops (should be after the loop where possible)
- Redundant Perform Find when a constrained find or GTRR would suffice

### Cross-script issues
Review the interactions between the target script and its subscripts:
- **Parameter contract** — does the caller pass what the callee expects?
- **Result handling** — does the caller check `Get ( ScriptResult )`?
- **Layout context** — does a subscript change the layout without restoring it?
- **Error propagation** — does a subscript report errors via `Exit Script` result?

Flag issues in subscripts but **do not refactor them** — only the target script is modified unless the developer asks otherwise.

---

## Step 5: Plan the refactoring

Use the `implementation-plan` skill internally to reason about the approach. When called internally, produce the plan inline without waiting for developer confirmation.

Present a summary of proposed changes to the developer:

```
## Proposed refactoring: [Script Name]

### Changes
1. Add error handling header (Set Error Capture + Allow User Abort)
2. Wrap main logic in single-pass loop with error exits
3. Replace inline find with Go to Related Record
4. Hoist repeated client name lookup to $clientName variable
5. Fix error capture pattern (separate steps → single expression)

### Preserved behaviour
- Same parameter format and exit result
- Same layout navigation sequence
- Same field modifications

### Risk
- None — structural changes only, no logic changes
```

Wait for developer confirmation before generating code.

---

## Step 6: Generate the refactored script

Work from the fmxmlsnippet base in `agent/sandbox/`. Apply only the targeted changes — unchanged steps remain verbatim.

Follow all output rules from CLAUDE.md:
- Steps only within `<fmxmlsnippet type="FMObjectList">` — no `<Script>` wrapper
- Use step catalog for step structure, not xml_parsed verbose format
- Validate all field/layout/script references against CONTEXT.json or index files

Run the validator:

```bash
python3 agent/scripts/validate_snippet.py agent/sandbox/{ScriptName}.xml
```

Fix any errors before proceeding.

---

## Step 7: Present the diff

Show the developer what changed. Present a before/after comparison of the human-readable script — not the raw XML.

### Generate HR text for both versions

Use `snippet_to_hr.py` to convert the refactored fmxmlsnippet to HR:

```bash
python3 agent/scripts/snippet_to_hr.py agent/sandbox/{ScriptName}.xml --raw
```

The original HR is already available in `agent/xml_parsed/scripts_sanitized/`.

### Terminal output (always)

Present a concise summary in the terminal listing each change with the relevant line numbers (from the human-readable version).

### Webviewer hint

Check if the companion server is reachable:

```bash
curl -s --max-time 2 -o /dev/null -w "%{http_code}" {companion_url}/status
```

If reachable (HTTP 200 or 404), append this note after the terminal summary:

> The webviewer is available — ask to "show the diff in the webviewer" for a side-by-side visual comparison.

**Do not push the diff automatically.** Only push when the developer explicitly asks. To push:

1. Read the original HR from `scripts_sanitized/`
2. Generate the refactored HR via `snippet_to_hr.py --raw`
3. POST the diff payload to the companion:

```bash
python3 -c "
import json, sys
before = open(sys.argv[1]).read()
after = open(sys.argv[2]).read()
payload = json.dumps({
    'type': 'diff',
    'before': before,
    'content': after,
    'repo_path': '{repo_path}'
})
sys.stdout.write(payload)
" "{original_hr_path}" "{refactored_hr_path}" \
  | curl -s -X POST -H 'Content-Type: application/json' -d @- {companion_url}/webviewer/push
```

---

## Step 8: Deploy

### Tier 3 (autonomous)

After developer approval:

1. Load clipboard via `POST {companion_url}/clipboard`
2. Deploy via `deploy.py` or direct companion calls:
   - For an existing script: use Tier 2 mechanics (open script tab via Agentic-fm Paste, AXPress tab, Cmd+A → Delete → Cmd+V) to replace the content
   - Alternatively: `POST {companion_url}/trigger` with raw AppleScript to open the script tab and paste
3. Confirm deployment succeeded

### Tier 1 (developer-assisted)

Present paste instructions:

> The refactored script is on your clipboard. To install it:
>
> 1. Open **Script Name** in Script Workspace
> 2. **Cmd+A** — select all existing steps and delete
> 3. **Cmd+V** — paste

---

## Constraints

- **Preserve observable behaviour** — the refactored script must produce the same results for the same inputs. If a change would alter behaviour, flag it explicitly and get developer approval.
- **Do not refactor subscripts** unless explicitly asked. Flag issues in subscripts in the analysis but only modify the target script.
- **Do not add features** — refactoring improves structure, not functionality. If the developer's request includes new functionality, that is a script creation task, not a refactor.
