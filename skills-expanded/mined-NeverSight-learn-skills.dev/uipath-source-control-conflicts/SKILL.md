---
name: uipath-source-control-conflicts
description: "Resolve an in-progress source-control merge or rebase conflict involving UiPath project artifacts by recovering the intent of both sides, using structure-aware edits, and rerunning the owning product validations. Use for conflicts in project files, JSON manifests, coded automation, XAML, Maestro artifacts, solution wrappers, tests, documentation, and generated metadata."
category: "Build, test, and change quality"
---

# UiPath Source Control Conflicts

Preserve compatible intent, choose explicitly when intent conflicts, and finish with a structurally valid project instead of treating UiPath artifacts as undifferentiated text.

**Maturity:** pilot.

## Ownership Boundary

**This custom skill owns:** Preserve compatible intent, choose explicitly when intent conflicts, and finish with a structurally valid project instead of treating UiPath artifacts as undifferentiated text.

Keep current product commands, schemas, artifact validation, live tenant operations, and policy administration with official UiPath skills.

## Compose With Official UiPath Skills

Use official skills for current product commands and artifact contracts:

- `uipath-rpa`
- `uipath-agents`
- `uipath-maestro-flow`
- `uipath-maestro-bpmn`
- `uipath-maestro-case`
- `uipath-coded-apps`
- `uipath-api-workflow`
- `uipath-solution`
- `uipath-review`

## Workflow

### 1. Inspect source-control state

Identify merge or rebase mode, base, ours, theirs, conflicting files, generated files, relevant commits, and the command needed to continue.

**Completion criterion:** Every conflict and its source state is known.

### 2. Recover both intents

Read commit messages, issues, SDD sections, tests, ADRs, and surrounding artifact structure. State what each side was trying to preserve.

**Completion criterion:** Each hunk has two evidence-backed intents or a documented unknown.

### 3. Choose a structure-aware strategy

Preserve both intents where compatible. When incompatible, follow the merge goal and approved specification. Prefer regeneration through the owning official skill for generated or structured artifacts when possible.

**Completion criterion:** The resolution strategy is explicit before editing each artifact.

### 4. Resolve without inventing behavior

Edit only the conflicted behavior and necessary structural glue. Remove markers and avoid unrelated modernization.

**Completion criterion:** All conflict markers are gone and no new unapproved behavior was added.

### 5. Validate by artifact owner

Run the official build, validation, tests, solution checks, and two-axis review required by every affected artifact type.

**Completion criterion:** The merged structure and behavior have observed evidence.

### 6. Finish safely

Stage resolved files and continue the merge or rebase. Commit, push, force-update, or open a PR only under the user's source-control authority and policy.

**Completion criterion:** The operation is complete or the exact remaining command and blocker are reported.

## Output Contract

- Intent summary per conflict.
- Resolved source artifacts.
- Validation and test evidence.
- Completed or precisely paused merge or rebase.

## Guardrails

- Never resolve by taking ours or theirs blindly for structured artifacts.
- Never invent business behavior to make a conflict disappear.
- Never force-push or rewrite shared history without explicit authority.
- Never claim success until the merge or rebase state and product validation are checked.

## Example Requests

- "Resolve a project.json dependency conflict."
- "Merge two branches that both changed Main.xaml."
- "Recover a conflicted UiPath solution wrapper."

## Finish

Report completed work, observed evidence, the next official owner, and every blocker. Mark unobserved actions as pending.
