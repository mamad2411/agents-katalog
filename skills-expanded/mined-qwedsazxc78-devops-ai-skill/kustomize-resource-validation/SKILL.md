---
name: kustomize-resource-validation
description: >
  Auto-trigger skill that activates when any kustomization.yaml file is edited.
  Validates resource references, patch references, orphaned files, cross-environment
  consistency, build success, and generator configurations.
version: "1.0.0"
---

# Kustomize Resource Validation -- Auto-trigger Skill

Automatically activates when any `kustomization.yaml` file is edited.

## Activation

**Trigger:** Any file named `kustomization.yaml` inside a Kustomize module directory (any directory containing `base/` and `overlays/` structure) is created or edited.

**Scope:** This applies to both base and overlay `kustomization.yaml` files.

## Instructions

After the user edits a `kustomization.yaml`, perform these validations in order. Use the file system tools (Glob, Read) to verify references -- do not guess.

### 1. Resource Reference Validation

For every entry in the `resources:` list, verify the target exists:

- **Directory references** (e.g., `../../base`): Resolve the relative path from the `kustomization.yaml` location and confirm the directory exists and contains its own `kustomization.yaml`.
- **File references** (e.g., `gitlab-runner-secret.yaml`): Confirm the file exists in the same directory as the `kustomization.yaml`.

Report missing references as **FAIL**.

### 2. Patch Reference Validation

For every entry in the `patches:` list that uses a `path:` key, verify:

- The referenced YAML file exists relative to the `kustomization.yaml` directory.
- The file contains valid Kubernetes resource structure (must have `apiVersion`, `kind`, and `metadata` fields).

Report missing or malformed patches as **FAIL**.

### 3. Orphaned File Detection

List all `.yaml` files in the same directory as the `kustomization.yaml`, then check whether each file is referenced as a `resources` entry or a `patches` path entry.

**Exclude from orphan detection:**
- `kustomization.yaml` itself
- Files inside the `env/` subdirectory (used by secretGenerator)
- Files matching `*.env`

Report unreferenced files as **WARN** with the message:

> WARNING: `<filename>` exists in `<directory>/` but is not referenced in `kustomization.yaml`. It may be orphaned.

### 4. Cross-Environment Consistency

This check only applies when the edited file is in an overlay directory (e.g., `overlays/dev/kustomization.yaml`).

Discover sibling environments by listing subdirectories under the `overlays/` parent directory. Compare the `resources:` and `patches:` lists across all discovered sibling environments. Report differences as **WARN** -- not FAIL, since environment-specific resources are sometimes intentional.

Example warning format:

> WARNING: `overlays/dev/kustomization.yaml` includes patch `airflow-sa-patch.yaml` which is absent from `overlays/stg/` and `overlays/prd/`. Verify this is intentional.

### 5. Build Validation

Determine the Kustomize module from the file path (the nearest ancestor directory containing both `base/` and `overlays/`).

- **If the file is in an overlay directory:** Run `kustomize build` for that specific environment only.
- **If the file is in a base directory:** Discover all environments under `overlays/` and run `kustomize build` for each.

```bash
kustomize build <module>/overlays/<env>
```

Report build failures as **FAIL** with the error output.

### 6. SecretGenerator / ConfigMapGenerator Check

If `secretGenerator` or `configMapGenerator` entries exist in the edited file, verify:

1. All referenced `envs` file paths exist relative to the `kustomization.yaml` directory.
2. All referenced `files` paths exist relative to the `kustomization.yaml` directory.
3. Each generator entry specifies a `namespace`.
4. If the repo convention is to use `generatorOptions.disableNameSuffixHash: true`, check it is set. If missing, warn:

> WARNING: `generatorOptions.disableNameSuffixHash` is not set to `true`. Consider setting `disableNameSuffixHash: true` at the top level of kustomization.yaml to maintain consistent resource names.

**Kustomize module conventions to detect:**
- If the module uses `namePrefix` in overlays, verify `namePrefix` is set and matches the environment directory name (e.g., `dev-`, `stg-`, `prd-`).
- If sibling overlays do not use `namePrefix`, do not flag its absence.

## Output Format

Always show the validation summary table, regardless of whether issues are found.

```
Kustomize Validation: <path/to/kustomization.yaml>

| # | Check                  | Status | Details                              |
|---|------------------------|--------|--------------------------------------|
| 1 | Resources              | PASS   | 5 resources, 0 missing               |
| 2 | Patches                | PASS   | 3 patches, 0 missing                 |
| 3 | Orphaned Files         | WARN   | 1 orphaned: unused-config.yaml       |
| 4 | Cross-Env Consistency  | OK     | Consistent across all environments   |
| 5 | Build (<env>)          | PASS   | Build succeeded                      |
| 6 | Generators             | PASS   | 2 secretGenerators, all refs valid   |
```

If there are errors or warnings, list them after the table:

```
Errors:
- [#1 Resources] File `missing-secret.yaml` not found in overlays/dev/

Warnings:
- [#3 Orphaned] `unused-config.yaml` is not referenced in kustomization.yaml
- [#4 Cross-Env] Patch `extra-patch.yaml` exists only in dev overlay
```

If all checks pass with no warnings, end with: "All checks passed. No issues found."

## Check 2a: Patch-Resource Match Validation

For each entry in the `patches:` list, verify that the patch targets a resource that actually exists in the build:

1. Read the patch file and extract its `apiVersion`, `kind`, and `metadata.name`
2. Read all resources in the `resources:` list and extract their `apiVersion`, `kind`, and `metadata.name`
3. If the patch targets a resource not found in the resources list, report as **WARN**:
   > WARNING: Patch `<patch-file>` targets `<kind>/<name>` but no matching resource found in `resources:`. The patch may apply to a resource from a base directory.
4. For strategic merge patches (no `op` field), verify the patch structure matches the target resource's structure
5. For JSON patches (contains `op: add/remove/replace`), verify the path exists in the target resource

This check reduces the risk of patches silently doing nothing because their target was renamed or removed.

## Error Handling

### Discovery Failures
- **kustomization.yaml is empty or invalid YAML**: Report as FAIL with the parse error. Skip all subsequent checks.
- **Base directory referenced but doesn't exist**: Report as FAIL in Check 1 and skip Check 5 (build will fail anyway).
- **Overlay directory with no sibling environments**: Skip Check 4 (cross-env consistency). Only one environment exists.

### Tool Failures
- **`kustomize` not installed**: Skip Check 5 (build validation). Report as SKIP with install command: `brew install kustomize`. All other checks (1-4, 6) work with file reading only.
- **`kustomize build` fails**: Report the error output as FAIL in Check 5. Continue with Check 6.
- **`kustomize build` times out (> 30s)**: Kill the process, report as FAIL with timeout message.

### Edge Cases
- **Deeply nested base references** (base referencing another base): Follow the chain up to 3 levels deep. Beyond that, warn about complexity.
- **Remote resources** (`resources: [https://...]`): Skip existence check, note as INFO that remote resources can't be validated offline.
- **Helm chart generators**: If `helmCharts:` section exists, note it as INFO — these are validated by Helm, not Kustomize.

## Report Persistence

After all checks complete, write the full validation report to the repository's `docs/reports/` directory.

### File path

```
docs/reports/kustomize-validation-<YYYY-MM-DD>.md
```

- Use today's date in `YYYY-MM-DD` format.
- Create `docs/reports/` if it does not exist (use `mkdir -p`).
- If a report file for today already exists, overwrite it.

### File content

The written report must include:

1. A header with repository name, date, branch (`git rev-parse --abbrev-ref HEAD`), and trigger file path.
2. The same validation summary table(s) shown in the terminal output.
3. Any Errors / Warnings sections, or "All checks passed." if clean.

### Example header

```markdown
# Kustomize Validation Report

**Repository:** <repo-root-directory-name>
**Date:** <YYYY-MM-DD>
**Branch:** <current-branch>
**Triggered by:** <path/to/kustomization.yaml>
```

### Error handling

- If the write fails (e.g., permission error), print a warning to the terminal but do not fail the pipeline.

## Dry-Run Support

This skill is **read-only by default** — validation doesn't modify files. All checks use Glob/Read to verify references. The only command that has side effects is `kustomize build`, which writes to stdout only. The **Report Persistence** step is the sole exception — it writes one Markdown file to `docs/reports/`.

## Rollback Strategy

No rollback needed — this skill only reads and reports. The only file written is the Markdown report under `docs/reports/`, which can be safely deleted.
