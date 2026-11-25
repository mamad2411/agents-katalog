---
name: pwrl-phase-checkpoint
description: "Enforce deterministic phase completion in PWRL workflows (review, work, plan, etc.). Use to: validate artifact generation, verify quality gates, block progression without completion. Works across all PWRL pipeline skills. Agent-agnostic, checkpoint-driven validation."
argument-hint: "[workflow-name] [phase-number] [artifact-path or artifact-json]"
user-invocable: true
disable-model-invocation: false
---

# PWRL Phase Checkpoint

Enforce strict phase completion across all PWRL deterministic workflows by validating artifacts and quality gates. This skill acts as a verification layer to ensure all agents follow pipeline discipline.

## When to Use

- **Running pwrl-review or pwrl-work**: Validate each phase before progression
- **Skipped steps detected**: Verify artifact completeness before continuing
- **Quality gate failures**: Block progression until gates pass
- **Cross-agent workflows**: Ensure consistency across different AI models
- **Phase resumption**: Resume from checkpoint with full artifact state

**Use alongside:** `pwrl-review`, `pwrl-work`, `pwrl-plan`, `pwrl-tasks`, `pwrl-learnings`.

## Principle

All PWRL workflows produce explicit **artifacts** (YAML + structured data) at each phase. Each phase is **independent but sequential** — progression blocked until both conditions met:

1. **Artifact Generated** — Phase output explicitly created and contains required fields
2. **Quality Gates Pass** — All acceptance criteria for the phase verified

This skill validates BOTH conditions before allowing next phase.

## Workflow

### 1. Phase Status Check

**Input:** Workflow name + phase number

**Process:**

1. Identify workflow family (review, work, plan, tasks, learnings)
2. Look up phase schema and quality gates (see [./references/phase-schemas.md](./references/phase-schemas.md))
3. Ask: "Current phase status?" or check provided artifact
4. Display expected deliverables + gates for this phase

**Output:** Current phase status (not-started, in-progress, complete, failed)

### 2. Validate Artifact

**Input:** Artifact path or JSON data

**Process:**

1. Check artifact exists and contains required fields for this phase
2. Parse YAML frontmatter
3. Validate against [phase-schemas.md](./references/phase-schemas.md): required fields present, data types correct, no empty critical fields
4. Report: ✓ Valid or ✗ Missing fields

**Output:** Validation report (valid/invalid + missing fields if any)

### 3. Verify Quality Gates

**Input:** Artifact content + phase-specific gates

**Process:**

1. Extract completion criteria for phase (see [./references/quality-gates.md](./references/quality-gates.md))
2. Check each gate: **phase-level** outputs present, **acceptance** criteria met, **evidence** data supporting each gate
3. Report pass/fail for each gate
4. Block or allow progression based on results

**Output:** Gate verification report (all pass/partial/fail)

### 4. Checkpoint Decision

**Input:** Artifact validity + gate status

**Process:**

1. **Valid + all gates pass:** ✓ ALLOW PROGRESSION — display "Phase [N] complete. Ready for Phase [N+1].", next phase schema, suggested next action
2. **Valid + gates partial:** ⚠️ WARN BEFORE PROGRESSION — show failing gates, ask "Continue anyway? (Not recommended)", require explicit confirmation and log decision if yes, else provide remediation steps
3. **Invalid:** ✗ BLOCK PROGRESSION — show missing/invalid fields, provide recovery instructions (complete current phase, regenerate artifact, reference [phase-schemas.md](./references/phase-schemas.md)), ask "Would you like instructions to complete this phase?"

## Usage

```
/pwrl-phase-checkpoint [workflow] [phase] [artifact-path-or-json]
```

Validate the current phase before progressing, or resume from an interrupted pipeline by re-checking a previously produced artifact. For worked examples (check phase status, validate & allow progression, handle missing artifact, recover from a failed gate) see [./references/checklists-examples.md](./references/checklists-examples.md) § Worked Examples.

## Integration

**For agents:** When running `/pwrl-review`, `/pwrl-work`, or other PWRL workflows, automatically check phase completion — ask user to confirm phase done, call `/pwrl-phase-checkpoint [workflow] [N] [artifact-path]`, block next phase if validation fails, display remediation path if needed.

**For users:** Run checkpoint explicitly to verify work or resume after interruption.

**For custom workflows:** Extend with [custom phase schemas](./references/phase-schemas.md#extending).

## Output

Each checkpoint run produces a status report with this structure:

- ✓/✗ **Artifact valid** — required fields present and typed correctly
- ✓/✗ **Quality gates pass** — per-gate pass/fail list
- **Progression status** — `allowed` | `warn` | `blocked`
- **Next phase** — identifier and schema reference, if allowed
- **Remediation steps** — ordered actions to reach `allowed`, if blocked or warned

**Decision rule:** progression is `allowed` only when artifact validity is ✓ AND every critical quality gate passes; `warn` when artifact is valid but one or more non-critical gates fail; `blocked` when the artifact is invalid or any critical gate fails.

## Standards Compliance

Enforces standards from [pwrl-standards](../pwrl-standards/):

- [SCHEMA.md](../pwrl-standards/SCHEMA.md) — Artifact structure
- [TEMPLATE.md](../pwrl-standards/TEMPLATE.md) — Phase template format
- [AUDIT.md](../pwrl-standards/AUDIT.md) — Audit trail for phase completion

See [./references/standards-mapping.md](./references/standards-mapping.md) for detailed compliance mappings.
