---
name: 7d
description: Work with the repository's 7D process registry over OKF concept types. Use when validating 7D usage, generating reports by lifecycle stage, deriving feature progress, or creating/editing 7D lifecycle artifacts without changing OKF format.
metadata:
  version: "1.0"
  scope: simple-okf-local
---

# 7D Skill

Use this skill for 7D lifecycle work in this repository.

7D is a process registry over existing OKF concept types. It does **not** change
OKF concept format. The canonical rules are in `SPEC.md`, `AGENTS.md`, and the
7D registry implemented by `okf_mcp/okf.py`.

## Core rules

1. Do not add 7D-specific frontmatter keys such as `process`, `stage`,
   `stage_order`, `artifact_key`, `artifact_order`, `gate_decision`, or `raci`
   solely to support 7D.
2. Use the existing OKF `type` field as the lifecycle artifact type, for example
   `PRD`, `Architecture & NFR`, or `Test Report`.
3. Do not create generic 7D types such as `Lifecycle Artifact`, `Lifecycle
   Check`, `Role`, or `Decision Gate` when the real artifact type is known.
4. Resolve stage and RACI responsibility from the registry, not from per-concept
   metadata.
5. Derive feature progress from linked artifact concepts and their types.
6. Every OKF concept type must be registered. An unmapped type is a validation
   error; missing required lifecycle artifacts are static-analysis coverage gaps.
7. OKF concepts also require `status`. Allowed values are `draft`, `to-review`,
   `not-valid`, `valid`, `rejected`, and `accepted`; status is document/artifact
   state, not implementation progress, and transitions are recommended only.
8. When creating or editing OKF concepts, also load and follow the `okf` skill.

## Preferred MCP tools

Use the `simple-okf` MCP server first when available:

```text
seven_d_registry()
seven_d_mapping_for_type(type_name)
list_7d_artifact_concepts(stage?)
seven_d_stage_report(stage?)
seven_d_stage_report_markdown(stage?)
seven_d_dashboard(write?, out_path?, include_html?)
seven_d_feature_status(concept_id)
validate_7d()
validate_bundle()
build_graph(write=false)
```

Typical workflows:

- Registry lookup: call `seven_d_registry()` or
  `seven_d_mapping_for_type(type_name)`.
- Stage report: call `seven_d_stage_report(stage)` for structured data, or
  `seven_d_stage_report_markdown(stage)` for a compact Markdown report.
- Kanban dashboard: call `seven_d_dashboard(write=true, out_path="artifacts/7d-dashboard.html")`
  to generate a self-contained HTML board with stage columns and readonly
  concept detail modals.
- Stage inventory: call `list_7d_artifact_concepts(stage)` for one stage, or for
  every stage in the registry.
- Feature progress: call `seven_d_feature_status(concept_id)` and report the
  derived stage, supporting artifacts, and gaps.
- Validation: call `validate_7d()` and `validate_bundle()` before finishing.

## CLI helper tools

If MCP is unavailable or the user explicitly asks for a command, use the MCP
package multi-app CLI. Resolve paths from the repository root.

Generate a compact report for every 7D stage:

```sh
python3 -m okf_mcp 7d report --bundle okf
python3 -m okf_mcp 7d report --bundle okf --stage Design
```

Generate the interactive Kanban dashboard HTML:

```sh
python3 -m okf_mcp 7d dashboard --bundle okf --out artifacts/7d-dashboard.html
```

Return the same report as JSON:

```sh
python3 -m okf_mcp 7d report --bundle okf --json
```

Validate 7D usage:

```sh
python3 -m okf_mcp 7d validate --bundle okf
```

Show one feature's derived 7D status:

```sh
python3 -m okf_mcp 7d status --bundle okf requirements/flows/first-reasoning-onboarding
```

Show the registry:

```sh
python3 -m okf_mcp 7d registry --bundle okf
```

## Stage report expectations

A stage report should include:

1. bundle path and validation status;
2. all seven stages in order;
3. registered artifact types for each stage;
4. actual OKF concepts found for each stage;
5. explicit static-analysis gaps for missing required lifecycle artifacts;
6. unmapped type validation errors, if any;
7. warnings/errors from `validate_7d()`.

Do not treat missing 7D artifacts as OKF validation errors. They are lifecycle
coverage gaps unless the user defines a stricter gate. Do treat unmapped concept
`type` values as validation errors.

## Creating lifecycle artifacts

When the user asks to create or update 7D artifacts:

1. Identify the correct registered artifact type.
2. Use that value as normal OKF frontmatter `type` and set an allowed `status`
   such as `draft` for a new artifact.
3. Place the concept in an appropriate OKF directory based on content, not on
   the 7D stage name alone.
4. Link the artifact to the feature or related concepts using relative Markdown
   links.
5. Regenerate indexes/graph only when concepts are added, removed, renamed, or
   links materially change.
6. Run `validate_7d()` and `validate_bundle()`.

## Output format

When reporting 7D work, summarize:

1. stage coverage and derived feature status;
2. registered artifact types used;
3. gaps or unknown types;
4. validation results;
5. files changed, if any.
