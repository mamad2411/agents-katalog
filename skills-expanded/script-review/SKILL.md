---
name: script-review
description: Code review a FileMaker script and its full call tree — all subscripts reached via Perform Script are loaded and analysed together. Evaluates error handling, structure, naming, performance, parameter contracts, and cross-script issues. Use when the developer says "review", "code review", "evaluate", or "assess" a script, or mentions "script ID" in a review context.
---

# Script Review

Perform a thorough code review of a FileMaker script and every script it calls. The review covers the full call tree — not just the entry-point script in isolation.

**CRITICAL**: Debugging breakpoints within FileMaker scripts are not a runtime issue. Breakpoints are only active when a developer explicitly invokes the FileMaker debugger. Do not flag them.

---

## Step 1: Locate the target script

Use the `script-lookup` skill to find the script if not already identified. Read the human-readable version from `agent/xml_parsed/scripts_sanitized/`.

---

## Step 2: Resolve the call tree (parallel loading)

Before analysing any logic, build the full picture of every script involved. The goal is to minimize tool calls by loading subscripts in parallel batches — one batch per depth level.

**Performance target**: For a script with N subscripts at depth 1, the call tree should load in 2 tool calls (1 grep + 1 parallel read), not N+1 sequential calls.

### 2a. Extract ALL Perform Script references in one pass

Grep the entry script's sanitized text for every `Perform Script` line at once. Extract all target script names from the results.

```bash
grep -i "Perform Script" "agent/xml_parsed/scripts_sanitized/{solution}/{path}.txt"
```

This returns lines like:
- `Perform Script [ "Subscript A" ; Parameter: $param ]` — extract `Subscript A`
- `Perform Script [ "Subscript B" ]` — extract `Subscript B`
- `Perform Script By Name [ ... ]` — flag as unresolvable (calculated name)

### 2b. Batch-resolve names to file paths

Take ALL extracted script names and resolve them to file paths in a **single grep** against the scripts index:

```bash
grep -E "Subscript A|Subscript B|Subscript C" "agent/context/{solution}/scripts.index"
```

This returns pipe-delimited rows (`ScriptName|ScriptID|FolderPath`) for every match. From each row, derive the sanitized file path:

- **With folder path**: `agent/xml_parsed/scripts_sanitized/{solution}/{FolderPath}*/{ScriptName} - ID {ScriptID}.txt`
- **Top-level** (empty folder path): `agent/xml_parsed/scripts_sanitized/{solution}/{ScriptName} - ID {ScriptID}.txt`

Since folder directory names include an ID suffix not in the index, use a glob to resolve the exact path if needed.

### 2c. Parallel-read ALL subscripts

Read ALL resolved subscript files in a **single message with multiple Read tool calls** — one per subscript. This replaces the old sequential "find one, read one, find next, read next" pattern.

For example, if the entry script calls 5 subscripts, issue 5 Read tool calls in a single message. All 5 load in parallel.

### 2d. Recurse (parallel per depth level)

After loading depth-1 subscripts, scan ALL of them for further `Perform Script` references. Collect any new (not yet visited) script names across all depth-1 subscripts, then repeat 2b–2c for the next depth level.

Track visited scripts by name to avoid cycles. Continue until no new references are found.

Each depth level adds at most 2 tool calls (1 batch grep + 1 parallel read), regardless of how many subscripts exist at that level.

### 2e. Present the call tree

Before starting the review, present the resolved call tree so the developer can see the full scope:

```
## Call tree: [Entry Script Name]

1. Entry Script Name
   ├── Subscript A
   │   └── Subscript A1
   ├── Subscript B
   └── Subscript C
       └── Subscript A  (already loaded)
```

Flag these edge cases:
- **Calculated names** — `Perform Script By Name` references cannot be statically resolved. Flag them so the developer can clarify which scripts may be called.
- **Missing scripts** — `Perform Script` references to scripts not found in `scripts_sanitized/` may be in a different solution file or deleted. Flag them.
- **Cycles** — scripts already visited are noted but not re-loaded.

---

## Step 3: Analyse — entry script

Review the entry-point script against these categories:

### Error handling
- Missing `Set Error Capture [ On ]` / `Allow User Abort [ Off ]` header (especially for server-side scripts)
- Steps that can fail without an immediate `Get ( LastError )` check
- Error data captured in separate steps instead of the single-expression `$errData` pattern (see `agent/docs/knowledge/error-data-capture.md`)
- Missing cleanup path (no revert/commit on failure)

### Structure
- Deeply nested If/Else chains that should be a single-pass loop (see `agent/docs/knowledge/single-pass-loop.md`)
- Repeated logic that could be hoisted to a variable or extracted to a subscript
- Missing guard clauses (parameter validation, empty found set checks)
- Dead code (disabled steps that serve no documentation purpose)

### Naming and conventions
- Variable names that don't follow conventions (`agent/docs/CODING_CONVENTIONS.md`)
- Inconsistent naming within the script
- Magic numbers or repeated string literals that should be variables (see `agent/docs/knowledge/dry-coding.md`)

### Performance
- Unnecessary layout switches
- Commit Records inside loops (should be after the loop where possible)
- Redundant Perform Find when a constrained find or GTRR would suffice

### Parameter contract
- Is the expected parameter format documented (via `$README` or comment)?
- Does the script validate its parameter before using it?
- Does it `Exit Script` with a documented result format?

---

## Step 4: Analyse — subscripts and cross-script issues

Review each subscript using the same categories as Step 3. Additionally, look for issues that only emerge when scripts are considered together:

### Parameter contract alignment
- Does the caller pass what the callee expects? Compare the `Perform Script` parameter expression against the subscript's `Get ( ScriptParameter )` parsing.
- Does the caller check `Get ( ScriptResult )` after the call? Does the callee actually `Exit Script` with a result?
- Type mismatches — caller sends a plain string, callee expects JSON (or vice versa)

### Layout context assumptions
- Does a subscript assume it's on a specific layout without navigating there?
- Does a subscript change the layout without restoring it, breaking the caller's context?
- Does a subscript call `Go to Layout [ original layout ]` before exiting?

### Error propagation
- If a subscript encounters an error, does it report it via `Exit Script` result?
- Does the caller check the subscript's result and handle errors?
- Or does the error silently disappear at the script boundary?

### Variable scope leakage
- Does a subscript set global variables (`$$`) that the caller depends on? (This is a fragile coupling — flag it)
- Does a subscript read global variables set by the caller instead of receiving them as parameters?

### Transaction boundaries
- If the entry script opens a transaction, do subscripts commit or revert within it? (This can break the outer transaction)
- Are Commit Records calls in subscripts aware of the caller's transaction state?

---

## Step 5: Present findings

Organise the review as a single report covering the full call tree. Group by severity:

```
## Code Review: [Entry Script Name]

### Call tree
(from Step 2d)

### Critical
Issues that will cause failures or data corruption:
- [Script Name, line N] — Set Field after Perform Find with no error 401 check
- [Subscript A, line N] — Commits inside caller's transaction

### Important
Issues that affect reliability or maintainability:
- [Script Name, line N] — Error data captured in separate steps (use single-expression pattern)
- [Script Name → Subscript B] — Caller doesn't check Get(ScriptResult)

### Suggestions
Improvements that are not urgent:
- [Script Name, line N] — Magic number "30" should be a variable ($dayThreshold)
- [Subscript A] — Missing $README documentation block

### Positive
Things the script does well (acknowledge good patterns):
- Clean parameter validation with early exit
- Consistent variable naming
```

**Line number references** must always refer to the human-readable (`scripts_sanitized`) version, never the XML.

---

## Two script formats — know the difference

There are two distinct XML formats in this project. They are **not interchangeable**:

| Format | Location | Usable as output? |
|---|---|---|
| FileMaker "Save As XML" export | `agent/xml_parsed/scripts/` | **No** — read-only reference only |
| FileMaker clipboard / fmxmlsnippet | `agent/scripts/` or `agent/sandbox/` | **Yes** — this is the output format |

When applying review findings as code changes, follow the refactoring workflow:

1. **Find or create the fmxmlsnippet version** — check `agent/sandbox/` first. If none exists, convert via `python3 agent/scripts/fm_xml_to_snippet.py`.
2. **Apply only the targeted changes** — unchanged steps remain verbatim.
3. **Validate**: `python3 agent/scripts/validate_snippet.py agent/sandbox/{script_name}`
