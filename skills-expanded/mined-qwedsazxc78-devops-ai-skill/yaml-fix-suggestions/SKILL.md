---
name: yaml-fix-suggestions
description: >
  Auto-trigger skill that activates when YAML files in Kustomize module directories are modified.
  Checks formatting, Kubernetes label compliance, kustomization.yaml references, and build validation.
  Reports only when issues are found.
version: "1.0.0"
---

# YAML Fix Suggestions -- Auto-trigger Skill

Automatically activates when YAML files in Kustomize module directories are modified.

## Activation

**Trigger:** Any `.yaml` or `.yml` file is created or edited inside a Kustomize module directory (any directory containing `base/` and `overlays/` structure).

**Exclude:** Files under `.claude/`, `.bmad-*/`, tool/agent configuration directories, and any paths excluded by a local `.yamllint.yml`.

## Instructions

After the user edits a YAML file, perform these checks silently and only report if issues are found.

### 1. Formatting Check

Read the modified file and check against the repo's `.yamllint.yml` configuration (if present). Fall back to these defaults if no `.yamllint.yml` exists:

- **Indentation:** 2-space indent, sequences indented (`indent-sequences: true`)
- **Trailing whitespace:** Not allowed
- **Line length:** 120 characters (or no limit if the repo disables it)
- **Document start marker:** Optional
- **Duplicate keys:** Not allowed

If formatting issues are found, suggest running the repo's formatter. Example:

```bash
pre-commit run yamlfmt --files <modified-file>
```

If `pre-commit` is not configured, suggest `yamllint` directly:

```bash
yamllint <modified-file>
```

### 2. Label Compliance Check

For any resource with a `metadata:` section, verify standard Kubernetes labels exist.

**Recommended Kubernetes labels (check for presence of at least these 4):**

| Label | Description |
|-------|-------------|
| `app.kubernetes.io/name` | Application name |
| `app.kubernetes.io/component` | Component type (e.g., `service-account`, `ingress`, `deployment`) |
| `app.kubernetes.io/part-of` | Higher-level system or platform |
| `app.kubernetes.io/managed-by` | Management tool (e.g., `kustomize`, `helm`) |

**Optional organizational labels (warn if absent):**

| Label | Description |
|-------|-------------|
| `team` | Owning team |
| `cost-center` | Cost allocation identifier |
| `environment` | Deploy target (e.g., `dev`, `stg`, `prd`) |

**Note:** Labels inherited via Kustomize `commonLabels` in base or overlay `kustomization.yaml` count as present. Check the relevant `kustomization.yaml` chain before reporting missing labels.

If labels are missing, suggest the specific labels to add with values inferred from the resource type, namespace, and file path context.

### 3. Kustomize Reference Check

Check the `kustomization.yaml` in the same directory as the edited file. If the edited file is not referenced as a `resources` entry or a `patches` entry (by `path`), warn:

> WARNING: `<filename>` is not referenced in `<directory>/kustomization.yaml`. It may be orphaned and will not be included in the Kustomize build.

### 4. Build Validation

Discover the available environments by listing subdirectories under `overlays/` in the same Kustomize module.

If the edited file is under an overlay directory (e.g., `<module>/overlays/dev/`), identify the affected module and environment, then suggest running:

```bash
kustomize build <module>/overlays/<env>
```

If the edited file is under a `base/` directory, suggest building all discovered environments for the affected module:

```bash
kustomize build <module>/overlays/<env1>
kustomize build <module>/overlays/<env2>
# ... for each environment discovered under overlays/
```

## Output Format

Only show output if at least one check produces a WARN or FAIL status. Use this format:

```
YAML Fix Suggestions for <filename>

| # | Check     | Status | Details                          |
|---|-----------|--------|----------------------------------|
| 1 | Format    | OK     | No issues found                  |
| 2 | Labels    | WARN   | Missing: team, cost-center       |
| 3 | Reference | OK     | Listed in kustomization.yaml     |
| 4 | Build     | WARN   | Suggest: kustomize build ...     |

Suggested fix: pre-commit run yamlfmt --files <file>
```

If all checks pass, do not produce any output.

## Error Handling

### Discovery Failures
- **No kustomization.yaml in the same directory**: Skip Check 3 (reference check). The file might be a standalone YAML, not part of a Kustomize module.
- **No overlays/ directory found**: Skip Check 4 (build validation). The file might be in a flat Kustomize structure.
- **No .yamllint.yml found**: Use built-in defaults (defined in Check 1). Don't report the absence as an error.

### Tool Failures
- **`yamllint` not installed**: Perform basic formatting checks using file reading only (indentation, trailing whitespace, duplicate keys). Suggest installing yamllint for comprehensive checking.
- **`pre-commit` not installed**: Suggest `yamllint <file>` directly as the fix command instead.
- **`kustomize` not installed**: Skip Check 4 (build validation). Report as INFO with install command.

### Edge Cases
- **CRD YAML files**: Files containing `kind: CustomResourceDefinition` may not need standard Kubernetes labels (Check 2). Skip label compliance for CRDs.
- **Helm template files**: Files containing `{{ }}` Helm template syntax are not valid YAML. Skip formatting check and note this is a Helm template.
- **Very large YAML files (> 1000 lines)**: Run checks but note that line-by-line formatting review may be slow. Suggest using `yamllint` CLI for better performance.

## Dry-Run Support

This skill is **read-only by default** — it only reports suggestions, never modifies files. All suggested fixes are presented as commands for the user to run manually.

## Rollback Strategy

No rollback needed — this skill only reads and suggests. It never modifies files directly.
