---
name: workflow-scan
description: Generate a `WORKFLOW_QUESTIONS.md` report for an embedded Trellis temp project. Use when scanning the full workflow currently in use inside the temp project for problems, gaps, residual issues, or new issues before source-side repair.
compatibility: Requires `trellis` on PATH, access to the temp project fixture, and inline CLI execution with local filesystem access.
---

# workflow-scan

## Version History

- **v2.0**: Re-scoped the skill to analyze only the full workflow content currently present in the temp project; removed source-repo inputs, source-repo evidence layers, and source-location requirements from the scan contract
- **v1.3**: Aligned frontmatter with the latest public skill spec by making the description explicitly cover both purpose and trigger, and by adding compatibility requirements
- **v1.2**: Replaced misleading fixed example paths and version literals with runtime-sensitive placeholders
- **v1.1**: Clarified temp-project provenance, no-agent execution, analysis-summary output, and evidence classification rules
- **v1.0**: Initial release

## Purpose

Scan the embedded workflow currently in use inside a Trellis temp project and
produce a structured `WORKFLOW_QUESTIONS.md` report.

This skill is the **analyzer/producer** half of the `workflow-scan` /
`workflow-repair` coupled pair.

Its target of judgment is the full workflow surface currently present inside the
temp project. It does not compare against the current source repository. It
does not edit workflow source files, installed artifacts, or task state.

## When to Use

Use this skill when any of the following is true:

- you are working in a trellis temp project and need to analyze the workflow
  currently installed there
- you need to inspect the temp project's active workflow surfaces for problems,
  gaps, residual issues, or new issues
- the user asks to "scan the temp project workflow" or "check the embedded
  workflow for issues"
- the user asks to "produce workflow questions" or "generate a workflow scan
  report"
- the user asks to "run workflow-scan"
- a workflow analysis cycle starts and a structured report is needed before
  repair

## When Not to Use

- you need to fix issues: use `workflow-repair` in the source project
- you need a comprehensive audit with version gates and runtime validation: use
  `workflow-audit`
- you need version-drift analysis: use `workflow-capability-audit`
- you are doing a normal implementation task without workflow analysis

## Core Rules

1. **Scan only**: this skill produces a question/evidence document; it never
   edits workflow source files or any code.
2. **Main CLI only**: do not use agents, sub-agents, or task orchestration. Run
   the scan directly in the current CLI session.
3. **Temp project only**: this skill runs in or targets a Trellis temp project.
   The analysis target is the temp project's currently installed workflow, not
   the current source repository.
4. **Embedded-workflow truth target**: judge whether issues exist from the full
   workflow result under `/tmp/trellis-{VERSION}-2`, not from any external
   source tree.
5. **All active workflow surfaces count**: scan the full workflow content that
   the temp project is currently using, not only
   `.trellis/workflow-installed.json`.
6. **Evidence comes from the temp project only**: every finding must use an
   `Evidence Layer` value grounded in the temp project's actual state.
7. **Conservative severity**: severity estimates are preliminary, set by the
   scan running in isolation before repair. Mark explicitly as estimates.
8. **Complete catalog**: every anomaly discovered must be recorded. Do not
   filter by severity during the scan phase.
9. **Origin classification is mandatory**: every finding must classify as
   either `trellis-native` (produced by `trellis init`) or `workflow-source`
   (introduced by the embedded workflow's install/patch layer).
10. **Contract format**: the output must use the `WORKFLOW_QUESTIONS.md` format
    exactly as defined in `references/scan-output-template.md`.

## Inputs

| Input | Required | Default | Meaning |
|-------|----------|---------|---------|
| `temp_project_path` | No | auto-detect | Absolute path to temp project root |
| `candidate_focus` | No | empty | Supplementary focus areas to prioritize |

### Temp Project Path Resolution

1. If `temp_project_path` is explicitly provided, use it.
2. Otherwise: run `trellis -v` to get VERSION, construct path
   `/tmp/trellis-{VERSION}-2/`.
3. Validate: the directory must exist and contain `.trellis/`.
4. If not found: stop as **Blocked / Temp Project Not Found**.

## Output

Single file: `WORKFLOW_QUESTIONS.md` at the temp project root.

Format specification: see `references/scan-output-template.md`.

## Workflow

### Step 0: Environment Preflight

1. Resolve the temp project path (see Path Resolution above).
2. Verify the temp project is a valid Trellis-initialized project:
   - `.trellis/` directory exists
   - `.trellis/.version` exists and is readable
3. Verify the temp project also looks workflow-embedded:
   - `.trellis/workflow-installed.json` exists, or
   - `.trellis/scripts/workflow/` exists, or
   - `.trellis/workflow.md` exists and clearly represents an embedded workflow,
     not only a baseline Trellis workflow
4. Read runtime version/context fields from the temp project where available:
   - `trellis -v` → live trellis version
   - `.trellis/.version` → temp project's trellis version
   - `.trellis/workflow-installed.json` → `workflow_version`,
     `workflow_schema_version`, `critical_runtime_patches`, `commands`,
     `scripts`, `cli_types`, and other install-record fields if present
5. If the temp project is not fully initialized (no `.trellis/` or no
   `.version`): stop as **Blocked / Invalid Temp Project**.
6. If the temp project is not workflow-embedded: stop as
   **Blocked / Workflow Not Embedded**.
7. If `WORKFLOW_QUESTIONS.md` already exists at the temp project root: stop and
   ask whether to overwrite or append.

### Step 1: Workflow Surface Inventory

1. Catalog the workflow surfaces currently present in the temp project.
2. At minimum inspect these paths when they exist:
   - `.trellis/workflow.md`
   - `.trellis/workflow-installed.json`
   - `.trellis/scripts/workflow/`
   - `.trellis/workflow-docs/`
   - `.agents/skills/`
   - `.codex/`
   - `.claude/commands/trellis/`
   - `.opencode/commands/trellis/`
   - `AGENTS.md` and other installed runtime control files whose current
     content affects workflow behavior
3. For each observed artifact, classify the strongest supported evidence layer:
   - `generated-target-baseline` — observed in a Trellis baseline surface that
     exists in the temp project
   - `generated-target-installed` — observed in a workflow-installed or
     workflow-patched surface in the temp project
   - `generated-target-runtime` — observed in a temp-project runtime/control
     surface whose current behavior matters but is not well-explained by the
     install record alone
4. If an origin or evidence-layer classification is inferred rather than
   directly obvious, state that inference explicitly inside the finding
   evidence.
5. Build an artifact inventory that later steps reference.

### Step 2: Script, Command, Skill, Hook, and Agent Verification

For every workflow-related executable or control surface found in the temp
project:

1. **Existence**: verify the file exists at the expected path implied by the
   temp project's own workflow surfaces.
2. **Executability / syntax shape**: for shell/Python scripts, verify the file
   is executable or has a valid shebang; for config/markdown carriers, verify
   the file is structurally readable.
3. **Cross-surface consistency**: compare what the file claims against the temp
   project's own other workflow surfaces:
   - install record vs actual scripts/commands/skills/hooks
   - workflow docs vs actual installed helper paths
   - AGENTS/hook/config guidance vs actual installed runtime surfaces
4. **Exit-code or gate contracts**: where the temp project documents a command
   or validation contract, check whether the installed surface appears to match
   that contract.
5. Note any missing files, wrong paths, broken references, contradictory
   install-record entries, or mismatched runtime surfaces.

### Step 3: CLI Adaptation Surface Scan

For each CLI carrier in the temp project:

1. **Skills**: catalog installed skills and check for:
   - missing workflow skills referenced elsewhere in the temp project
   - duplicate or contradictory skill carriers
   - stale instructions that reference absent runtime surfaces
2. **Commands**: catalog installed commands and check for:
   - missing command surfaces referenced by docs, hooks, or installed routing
   - stale references or broken paths
3. **Agents**: catalog installed agents and check for:
   - legacy names that conflict with the current installed workflow behavior
   - missing routing or context-loading guidance where the temp project expects
     it
4. **Hooks / runtime controls**: catalog hook configurations and check for:
   - missing patch markers or strong-gate markers referenced by the temp
     project's own workflow files
   - hook scripts that reference wrong or missing paths
   - runtime-control drift between installed docs/config and actual patched
     files

### Step 4: Document and Reference Integrity

For every installed workflow document or installed runtime-control document:

1. Check that internal cross-references resolve to existing temp-project files.
2. Check that helper-script references use the installed temp-project paths
   actually present in the temp project.
3. Check that execution-card references resolve when such cards are installed.
4. Flag any broken, stale, contradictory, or misleading references.

### Step 5: Residual and New Issue Detection

1. **Residual artifacts**: flag any workflow-related file, directory, or
   reference that appears retired, stale, or contradictory within the temp
   project's own current workflow surfaces.
2. **Install/runtime drift**: compare `.trellis/workflow-installed.json`
   against the actual installed state when the record exists. Flag
   inconsistencies.
3. **Missing surfaces**: flag workflow surfaces referenced by temp-project docs,
   configs, or records that are absent from the actual temp project.
4. **New issues**: flag anomalies not covered above — wrong permissions,
   encoding issues, broken assumptions, unexpected files, or contradictory
   routing/runtime behavior.

### Step 6: Compile WORKFLOW_QUESTIONS.md

1. Assign unique IDs to each finding: `WS-001`, `WS-002`, etc. (sequential,
   zero-padded to 3 digits).
2. For each finding, include all required fields per the finding entry schema:
   - Category (from the 6 allowed values)
   - Severity Estimate (P0/P1/P2, preliminary)
   - Origin (`trellis-native` or `workflow-source`)
   - Evidence Layer (`generated-target-baseline`,
     `generated-target-installed`, or `generated-target-runtime`)
   - Evidence (list of observations)
   - Temp Project Location (relative path within temp project, or a concise
     multi-path description when more than one surface is involved)
   - Description (what is wrong and why)
   - Suggested Investigation (what `workflow-repair` should verify in the temp
     project before deciding the source-side repair)
3. Write the required `Analysis Summary` section so the report explicitly
   includes:
   - overall problem analysis
   - gap / missing-surface analysis
   - residual issue summary
   - new issue summary
4. Set frontmatter `protocol: workflow-scan-repair-v2` (must match the current
   coupled contract version).
5. Write the document using the format from
   `references/scan-output-template.md`.
6. Write to the temp project root as `WORKFLOW_QUESTIONS.md`.

### Step 7: Echo and Stop

1. Echo the output summary:
   - temp project path
   - output file path
   - total findings, P0/P1/P2 counts
2. Suggest the next step: run `workflow-repair` in the source project to
   consume the report.
3. Do not attempt any fixes, aggregation, or workflow state changes.

## Error Handling

| Case | Behavior |
|------|----------|
| Temp project not found | Stop as **Blocked / Temp Project Not Found**. Suggest creating or locating the temp project first. |
| Temp project not fully initialized | Stop as **Blocked / Invalid Temp Project**. Verify `.trellis/` and `.version` exist. |
| Temp project not workflow-embedded | Stop as **Blocked / Workflow Not Embedded**. Verify the temp project really contains an embedded workflow instead of only the Trellis baseline. |
| `WORKFLOW_QUESTIONS.md` already exists | Stop and ask whether to overwrite or append. |
| No findings | Write `WORKFLOW_QUESTIONS.md` with `total-findings: 0` and all counts at 0. |

## Related Skills

- `workflow-repair`: consumer/fixer pair — consumes the
  `WORKFLOW_QUESTIONS.md` this skill produces
- `workflow-audit`: comprehensive audit with version gates, evidence mainline,
  and runtime validation (complementary, not replacement)
- `workflow-capability-audit`: version-drift audit

## Examples

### Example 1: Standard Scan in Temp Project

```text
User: /workflow-scan

AI:
1. Auto-detect temp project: run `trellis -v`, read the live version, then resolve `/tmp/trellis-{LIVE_VERSION}-2/`
2. Validate: `.trellis/` exists, `.version` matches, workflow embed markers exist
3. Inventory the workflow surfaces currently present in the temp project
4. Execute script/command/CLI/reference/residual checks using only temp-project evidence
5. Compile findings and analysis summary into `WORKFLOW_QUESTIONS.md`
6. Echo:
   ✅ Workflow scan complete
   📁 Temp Project: /tmp/trellis-{LIVE_VERSION}-2
   📄 Report: /tmp/trellis-{LIVE_VERSION}-2/WORKFLOW_QUESTIONS.md
   📊 Findings: 5 total (P0: 1, P1: 2, P2: 2)
   ➡️ Next: run /workflow-repair in the source project
```

### Example 2: Temp Project Not Found

```text
User: /workflow-scan

AI:
❌ Blocked / Temp Project Not Found
   Expected: /tmp/trellis-{LIVE_VERSION}-2/
   The directory does not exist or is not a valid trellis project.
   Suggestion: create or locate the temp project first, then re-run /workflow-scan.
```

### Example 3: Clean Install With No Issues

```text
User: /workflow-scan

AI:
1. Auto-detect temp project from the current `trellis -v` result
2. Execute all scan steps against the temp project's installed workflow
3. No anomalies found
4. Write WORKFLOW_QUESTIONS.md with total-findings: 0

   ✅ Workflow scan complete — no issues found
   📁 Temp Project: /tmp/trellis-{LIVE_VERSION}-2
   📄 Report: /tmp/trellis-{LIVE_VERSION}-2/WORKFLOW_QUESTIONS.md
   📊 Findings: 0 total (P0: 0, P1: 0, P2: 0)
```
