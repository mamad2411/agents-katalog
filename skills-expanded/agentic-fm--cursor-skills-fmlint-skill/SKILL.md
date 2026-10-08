---
name: fmlint
description: "Lint FileMaker scripts in fmxmlsnippet XML or human-readable format. Validates structure, naming conventions, references, best practices, and calculations. Tier 3 validates calculations against a live FM engine via AGFMEvaluation. Triggers on phrases like 'lint this', 'validate script', 'check conventions', 'run fmlint', or automatically after script generation."
compatibility: "Tier 1 always available. Tier 2 requires CONTEXT.json. Tier 3 requires OData connectivity to a hosted FM solution."
---

# FMLint — FileMaker Code Linter

Validate FileMaker scripts for structural correctness, naming conventions, reference integrity, best practices, and calculation validity.

---

## Step 1: Determine what to lint

Identify the target:

1. **Just-generated script** — lint the file in `agent/sandbox/` that was most recently written
2. **Specific file** — lint a file the developer names explicitly
3. **All sandbox files** — lint everything in `agent/sandbox/`
4. **HR script text** — lint human-readable script content directly (from webviewer or clipboard)

---

## Step 2: Run FMLint

Run the linter from the project root:

```bash
# Lint a specific file
python3 -m agent.fmlint agent/sandbox/MyScript.xml

# Lint all sandbox XML files
python3 -m agent.fmlint agent/sandbox/

# JSON output (for programmatic use)
python3 -m agent.fmlint --format json agent/sandbox/MyScript.xml

# Force tier or disable rules
python3 -m agent.fmlint --tier 2 --disable N003,D002 agent/sandbox/
```

The linter auto-detects:
- **Format** (XML vs HR) from file content
- **Tier** from available context (CONTEXT.json → tier 2, OData → tier 3)

---

## Step 3: Interpret results

### Severity levels

| Level | Meaning | Action |
|-------|---------|--------|
| ERROR | Will break in FileMaker | Must fix before deployment |
| WARNING | Likely bug or convention violation | Should fix |
| INFO | Style suggestion | Optional improvement |
| HINT | Minor recommendation | Informational only |

### Rule categories

| Prefix | Category | Tier | Examples |
|--------|----------|------|----------|
| **S** | Structure | 1 | Block pairing, XML well-formedness, step attributes |
| **N** | Naming | 1 | Unicode operators, variable naming, hard tabs |
| **D** | Documentation | 1 | PURPOSE comment, $README block |
| **B** | Best Practices | 1 | Error capture pairing, commit before nav |
| **C** | Calculations | 1/3 | Unclosed strings, unbalanced parens, live eval |
| **R** | References | 2 | Field/layout/script existence, ID matching |

---

## Step 4: Fix issues

For each ERROR or WARNING:

1. Read the diagnostic message and rule ID
2. Apply the fix (the `fix_hint` field suggests how)
3. Re-run the linter to verify the fix

Common fixes:
- **S005** (paired blocks): Add missing End If / End Loop / Commit Transaction
- **N001** (operators): Replace `<>` with `≠`, `<=` with `≤`, `>=` with `≥`
- **N002** (variable naming): Use `$camelCase`, `$$ALL_CAPS`, `~camelCase`
- **N004** (hard tabs): Replace leading spaces with tab characters in CDATA calculations
- **D001** (purpose): Add `# PURPOSE: description` as the first step

---

## Step 5: Tier 3 — Live calculation validation (optional)

When OData is configured in `agent/config/automation.json` and the developer approves:

1. The linter extracts all calculation expressions from the script
2. Calls AGFMEvaluation via OData for each unique expression
3. Reports C004 errors for calculations that fail in the FM engine

**Important**: Always confirm with the developer before triggering OData calls:

> FMLint found N calculations to validate against the live FM engine. Proceed?

This catches issues that offline analysis cannot — invalid field references, nonexistent custom functions, context-dependent calculation failures.

---

## Step 6: Integration with script creation workflow

When used as part of the standard script creation workflow (CLAUDE.md steps 6-7):

1. After writing fmxmlsnippet to `agent/sandbox/`, run:
   ```bash
   python3 -m agent.fmlint agent/sandbox/<script_name>
   ```
2. Fix any ERROR-level diagnostics before deployment
3. Review WARNING-level diagnostics with the developer
4. Proceed to `deploy.py` only after errors are resolved

The linter replaces `validate_snippet.py` as the primary validation tool while maintaining backward compatibility — `validate_snippet.py` continues to work for its original XML-only checks.
