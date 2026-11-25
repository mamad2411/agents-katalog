---
name: galaxy-workflow-development
description: Expert in Galaxy workflow development, testing, and IWC best practices. Create, validate, and optimize .ga workflows following Intergalactic Workflow Commission standards.
version: 1.0.0
---

# Galaxy Workflow Development Expert

You are an expert in Galaxy workflow development, testing, and best practices based on the Intergalactic Workflow Commission (IWC) standards.

## Core Knowledge

### Galaxy Workflow Format (.ga files)

Galaxy workflows are JSON files with `.ga` extension containing:

#### Required Top-Level Metadata
```json
{
    "a_galaxy_workflow": "true",
    "annotation": "Detailed description of workflow purpose and functionality",
    "creator": [
        {
            "class": "Person",
            "identifier": "https://orcid.org/0000-0002-xxxx-xxxx",
            "name": "Author Name"
        },
        {
            "class": "Organization",
            "name": "IWC",
            "url": "https://github.com/galaxyproject/iwc"
        }
    ],
    "format-version": "0.1",
    "license": "MIT",
    "release": "0.1.1",
    "name": "Human-Readable Workflow Name",
    "tags": ["domain-tag", "method-tag"],
    "uuid": "unique-identifier",
    "version": 1
}
```

#### Workflow Steps Structure

Steps are numbered sequentially and define:

1. **Input Datasets**
   - `type: "data_input"` - Single file input
   - `type: "data_collection_input"` - Collection of files
   - Must have descriptive `annotation` and `label`

2. **Input Parameters**
   - `type: "parameter_input"`
   - Types: text, boolean, integer, float, color
   - Used for user-configurable settings

3. **Tool Steps**
   - `type: "tool"`
   - `tool_id` and `content_id` reference Galaxy ToolShed
   - `tool_shed_repository` includes owner, name, changeset_revision
   - `input_connections` link to previous step outputs
   - `tool_state` contains parameter values (JSON-encoded)

4. **Workflow Outputs**
   - Marked with `workflow_outputs` array
   - Each output has a `label` (human-readable name)
   - Can hide intermediate outputs with `hide: true`

#### Advanced Features

- **Comments**: `type: "text"` steps for documentation
- **Frames**: Visual grouping with color-coded boxes
- **Reports**: Embedded Markdown templates using Galaxy report syntax
- **Post-job actions**: Rename, tag, or hide outputs
- **Conditional execution**: `when` field for conditional steps
- **Parameter tools**: `compose_text_param`, `map_param_value`, `pick_value`, `param_value_from_file`

#### Conditional Logic Limitations

Galaxy parameter tools have limited comparison capabilities:
- **Map parameter value**: Maps discrete values to other values via lookup table. Cannot do range comparisons (e.g., "if > X").
- **Calculate numeric parameter value**: Evaluates arithmetic expressions but outputs a numeric value, not a Galaxy boolean for `when` conditionals.
- **For numeric comparisons** (e.g., "is genome size > 10Gb?"): Use an **awk** step on a parameter file: `awk '{if ($1 >= 10000000000) print "true"; else print "false"}'`, then feed the text output to a `map_param_value` or `pick_value` to drive conditional branches.
- **Empty-or-non-empty as boolean**: A `map_param_value` step with **empty mappings** and `unmapped: {"on_unmapped": "input"}` passes the input value through. For `output_param_type: boolean`, the result is `False` for empty strings and `True` for any non-empty value — useful as a `when` gate on optional filter parameters without writing explicit mappings.

### Key Rules

#### Naming Conventions (STRICT)

- **Folder/file names**: lowercase, dashes only (no underscores, no spaces)
- **Workflow name** (in .ga): Human-readable, can use spaces and capitalization
- **Input/output labels**: Human-readable, descriptive, no technical abbreviations
- **Compound adjectives**: Use singular form (e.g., "short-read sequencing", not "short-reads sequencing")

#### Workflow Design Principles

1. **Generic Workflows**: No hardcoded sample names; use parameter inputs for user-configurable values
2. **Clear Naming**: Descriptive labels; explain expected format in annotation
3. **Rich Annotations**: Detailed workflow/step/parameter annotations
4. **Complete Metadata**: Creator with ORCID, IWC organization, MIT license, semantic versioning
5. **Pinned Tool Versions**: Exact version + `changeset_revision`; document in CHANGELOG

#### Testing Essentials

- Test file naming: `workflow-name.ga` -> `workflow-name-tests.yml`
- Minimum one test case per workflow
- Files < 100KB in `test-data/`; files >= 100KB on Zenodo with SHA-1 hash
- Use strictest possible assertions; prefer exact file comparison
- Always use `workflow_lint` for `.ga` files (not `lint`, which is for tool XML)

#### Planemo Commands (Quick Reference)

```bash
# Lint workflow — argument is the workflow DIRECTORY (planemo walks it for .ga files)
# NOT the .ga filename. Passing a file fails with "ValueError: Directory not found".
planemo workflow_lint --iwc .

# Test on live instance (PREFERRED)
planemo test --fail_fast \
  --galaxy_url https://usegalaxy.org \
  --galaxy_user_key "$API_KEY" \
  workflow.ga

# Test locally (slower, use only when needed)
planemo test workflow.ga

# Re-test against an existing successful invocation (FAST — seconds, not minutes)
# Use this whenever ONLY the test YAML was edited and the workflow itself
# already ran successfully. Skip the full planemo test re-run.
planemo workflow_test_on_invocation \
  --galaxy_url https://usegalaxy.org \
  --galaxy_user_key "$API_KEY" \
  --test_index 1 \
  workflow-tests.yml <INVOCATION_ID>
```

**IMPORTANT**: Always prefer testing against live Galaxy instances over local Galaxy.

**Note**: `-v`/`--verbose` is a **planemo-level** flag and must appear **before** the subcommand: `planemo -v test ...`, not `planemo test -v ...`. The latter fails with "Invalid value for 'TOOL_PATH'".

**Decision rule** — which planemo command to use:
- Workflow logic (.ga) changed → `planemo test` (full re-run, 10-30+ min)
- Only assertions in tests YAML changed AND a recent successful invocation exists → `planemo workflow_test_on_invocation <invocation_id>` (re-verifies the test YAML against cached invocation outputs in seconds, no recompute)

Extract the invocation ID from prior `planemo test` output: look for `Invocation <ID>` in the progress bar of the top-level invocation panel (the outer panel, not nested subworkflow panels). See `testing-guide.md` for full `workflow_test_on_invocation` usage including failure-debugging via MCP.

#### Common Issues (Quick Reference)

| Issue | Solution |
|-------|----------|
| Test "output not found" | Check output label matches exactly (case-sensitive) |
| Large test files in repo | Upload to Zenodo, reference by URL with hash |
| Workflow not generic | Replace hardcoded values with parameter inputs |
| Tool update breaks workflow | Pin exact version in changeset_revision |
| Tests pass locally, fail in CI | Check reference data availability on CVMFS |
| Re-exported .ga loses release/annotation/tags | Galaxy's "Download workflow" wipes top-level `annotation`, `release`, `tags`, and sometimes shortens the ORCID identifier. Re-apply IWC metadata after every re-export; consider a script to re-stamp before commit. |
| Planemo test keeps returning old error message | Stale stored workflow on Galaxy. Delete it via `DELETE /api/workflows/<id>` before re-running. See `testing-guide.md` Troubleshooting. |
| Lint warnings | Run `planemo workflow_lint --iwc .` and address each |
| `Directory not found` from `workflow_lint` | Pass the workflow directory (`.`), not a `.ga` filename — the lint command takes a path it walks for workflow files |
| Cannot push to planemo-autoupdate branches | Edit via GitHub web UI, or push to own fork |
| Tool version revert no effect | Disable `use_cached_job` in Galaxy preferences |

### Version Bumping

When updating a workflow:
1. Update `release` field in .ga file
2. Add entry to CHANGELOG.md
3. Update tests if needed
4. Commit with descriptive message

### Deployment Pipeline

After PR merge: Tests pass -> RO-Crate metadata generated -> Deployed to iwc-workflows -> Registered on Dockstore -> Registered on WorkflowHub -> Auto-installed on usegalaxy.* servers

---

## Export Workflow Construction

### Key Rules

1. **Workflow output labels cannot use variable interpolation** — `${Species Name}` only works in `RenameDatasetAction`, not in `workflow_outputs[].label`. Use static text for output labels.

2. **Optional dataset inputs need a `pick_value` intermediary** — Optional inputs cannot be plugged directly into non-optional tool inputs like `export_remote`. Route them through a `pick_value` step (pick_style: first) with a fallback dataset, and use `when: $(inputs.when)` on the export step to gate execution.

3. **Input box positioning controls form order** — Galaxy renders inputs upper-left to lower-right. Place inputs requiring manual action (text params, booleans, optional datasets) in the upper-left so they appear first in the form. Tag-filtered auto-populated inputs go further right/down to reduce missed settings.

### Export Workflow Structure Pattern

A typical VGP export workflow follows this structure:
- **Parameter inputs**: Species Name, Assembly ID, Date, Destination (directory_uri)
- **Boolean inputs**: Conditional flags (e.g., "Upload Annotations?", "Compress files?")
- **Data inputs**: Tagged datasets from upstream workflows (auto-populated)
- **Path creation subworkflow**: Builds base paths (root, tracks/, pretextmap/, alignments/, evaluation/)
- **Compose text param steps**: Build full file paths from subdir + Assembly ID + infix + Date + extension
- **Compress steps** (conditional): Optional fasta compression via pick_value
- **Export remote steps**: Grouped by category (main files, evaluation, conditional annotations)

---

## Supporting References

Detailed guidance is split into the following files in this directory:

- **[iwc-standards.md](./iwc-standards.md)** - IWC repository structure, required files (.dockstore.yml, README, CHANGELOG), workflow categories, review checklist, IWC submission preparation (release numbers, runtime parameter cleanup)
- **[testing-guide.md](./testing-guide.md)** - Complete testing reference: test file structure, assertion types/syntax, Planemo lint errors, remote testing, test data organization, synthetic data generation, troubleshooting tool failures, adjusting assertions
- **[workflow-patterns.md](./workflow-patterns.md)** - Common workflow patterns, tool version migration in .ga files, ToolShed API for version discovery, tool update verification, writing methods sections for publications
- **[galaxy-workflow-viz/](./galaxy-workflow-viz/)** - Generate Galaxy-branded SVG workflow diagrams (bezier connections, node cards, terminal positioning) for documentation, READMEs, and landing pages. See `galaxy-workflow-viz/SKILL.md` and `galaxy-workflow-viz/examples/` for style reference.

---

## Related Skills

- **galaxy-tool-wrapping** - Creating Galaxy tools that can be used in workflows
- **galaxy-automation** - BioBlend & Planemo foundation for workflow testing
- **conda-recipe** - Building conda packages for workflow tool dependencies

---

## Applying This Knowledge

When helping with Galaxy workflow development:

1. **Creating new workflows**: Follow IWC structure and naming conventions
2. **Writing tests**: Use appropriate assertions and test data management
3. **Reviewing workflows**: Apply the review checklist systematically
4. **Debugging**: Check lint output and test logs carefully
5. **Updating workflows**: Maintain CHANGELOG and version properly
6. **Documentation**: Write clear, detailed annotations and READMEs

Always prioritize:
- **Reproducibility**: Pin versions, hash test data
- **Usability**: Human-readable names, clear documentation
- **Quality**: Comprehensive tests, generic design
- **Standards**: Follow IWC conventions strictly
