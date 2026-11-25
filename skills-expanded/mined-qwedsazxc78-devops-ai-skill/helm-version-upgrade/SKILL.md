---
name: helm-version-upgrade
description: >
  Manages Helm chart version upgrades across Terraform+Helm platforms.
  Handles atomic 3-file updates with version discovery from ArtifactHub.
  Use when upgrading Helm charts, checking for outdated versions, or
  performing version consistency checks.
version: "1.0.0"
---

# Helm Version Upgrade Skill

## Purpose

Manages Helm chart version upgrades across Terraform+Helm platforms. Handles an **atomic multi-file update** pattern: the Terraform file containing Helm module blocks + each module's variable file + any version-tracking documentation.

## Activation

This skill activates when the user requests:
- Checking for outdated Helm charts
- Upgrading a specific Helm chart version
- Upgrading all Helm charts
- Checking version consistency across module files

## Step 0: Discover Repository Layout

**Do NOT assume any hardcoded file names or paths.** Discover the repo structure at runtime:

### 0a: Find the Helm Module Orchestrator File
Search for Terraform files containing Helm module blocks:
```bash
grep -rl 'source\s*=.*modules.*helm\|module.*helm\|helm_release' --include="*.tf" . | grep -v '.terraform/'
```
This identifies the orchestrator file(s) (e.g., `3-gke-package.tf`, `main.tf`, `helm.tf`, etc.).

### 0b: Discover Module Directories
Parse the orchestrator file(s) for `module` blocks. Extract `source` paths to find module directories:
- Pattern: `source = "./modules/helm/<name>"` or `source = "../modules/<name>"` or any relative path
- Verify each discovered directory exists

### 0c: Discover Module Variable Files
For each module directory, find the variable file:
- Check for `variable.tf` (singular), `variables.tf` (plural), or any `.tf` file containing `variable "install_version"` blocks
- Pattern: `grep -l 'variable.*install_version\|variable.*chart_version\|variable.*version' <module-dir>/*.tf`

### 0d: Discover Version-Tracking Documentation
Search for any Markdown file containing version references:
```bash
find . -name "*.md" -not -path "./.terraform/*" | xargs grep -l '\-\-version\|helm.*upgrade\|helm.*install' 2>/dev/null
```
This may find version-tracking docs, install guides, or project readmes. If none found, skip the documentation update step.

### 0e: Discover Chart Metadata
For each module, read its `main.tf` (or any `.tf` file containing `helm_release`) and extract:
- `repository` + `chart` fields from the `helm_release` resource
- For OCI charts (no `repository` field), extract `chart = "oci://..."` URL
- Skip commented-out module blocks (lines starting with `#`)

## Workflow

### Step 1: Determine Scope

Ask the user which modules to check:
- **Single module**: e.g., "upgrade grafana"
- **Category**: e.g., "upgrade monitoring stack" — discover by reading module namespaces
- **All**: Discover and check every active module via dynamic discovery

### Step 2: Read Current Versions

Parse the discovered orchestrator file(s) to extract current `install_version` (or `chart_version`/`version`) for each module block. Use the module list from Step 0.

### Step 3: Verify 3-File Consistency

For each module in scope, verify the version matches across all discovered locations:

| Location | How to find version |
|----------|-------------------|
| Orchestrator file (from Step 0a) | `install_version = "X.Y.Z"` in the module block |
| Module variable file (from Step 0c) | `default = "X.Y.Z"` in the version variable |
| Version doc (from Step 0d, if found) | `--version X.Y.Z` in the helm command |

**CRITICAL:** Variable files vary across repos (`variable.tf`, `variables.tf`, or others). Always use the file discovered in Step 0c. If no version-tracking doc was found in Step 0d, skip that check.

If any mismatch is found:
1. Report the inconsistency with exact values from each file
2. Ask user whether to fix the mismatch first or proceed with upgrade
3. If fixing, align all files to the version in the orchestrator file (source of truth)

### Step 4: Query Latest Versions

For each module, derive the ArtifactHub slug from the module's `main.tf`:
- Extract `repository` URL and `chart` name from the `helm_release` resource
- Map repository URL to ArtifactHub owner (e.g., `https://grafana.github.io/helm-charts` → owner `grafana`)
- Query ArtifactHub API:

```
GET https://artifacthub.io/api/v1/packages/helm/{owner}/{chart}
```

**Response parsing:**
- Extract `version` field from the response (this is the latest version)
- Extract `app_version` for informational display
- Note any `deprecated` flags

**For OCI-only charts** where ArtifactHub may not have data:
- Note that manual checking is required
- Provide the OCI registry URL for the user to check manually
- Extract OCI URL from the module's `chart` field in `main.tf`

### Step 5: Present Comparison Table

Display results in a table:

```
| Module               | Current   | Latest    | Change Type | Notes          |
|---------------------|-----------|-----------|-------------|----------------|
| argocd              | 9.2.4     | 9.3.0     | Minor       |                |
| grafana             | 10.5.4    | 10.5.4    | Up to date  |                |
| litellm             | 1.81.8... | ???       | OCI-manual  | Check manually |
```

**Change Type classification:**
- `Up to date` — same version
- `Patch` — only Z changed (X.Y.Z)
- `Minor` — Y changed
- `Major` — X changed (highlight with warning)
- `OCI-manual` — cannot auto-check

### Step 6: User Confirms Updates

Present the list of available upgrades and ask user to confirm:
- Which modules to upgrade
- Whether to accept major version bumps (warn about breaking changes)
- Option to skip specific modules

### Step 7: Atomic 3-File Update

For each confirmed module, update all discovered files atomically:

**File 1: Orchestrator file (from Step 0a)**
- Find the module block by matching the `source` path for this module
- Update `install_version = "<new_version>"` (or `chart_version`/`version` as used)
- For multi-instance modules (same source, multiple blocks), update ALL instances

**File 2: Module variable file (from Step 0c)**
- Find the version variable block (`install_version`, `chart_version`, or `version`)
- Update `default = "<new_version>"`
- Use the exact filename discovered in Step 0c

**File 3: Version-tracking doc (from Step 0d, if found)**
- Find the section for this module (by heading or helm command)
- Update `--version <new_version>` in the helm command
- Skip this step if no version doc was discovered

See UPGRADE_PATTERNS.md for exact regex patterns and edge cases per module.

### Step 8: Summary

After all updates:
1. List all modules updated with old -> new versions
2. Provide ArtifactHub links for release notes
3. Remind user to run `terraform validate` and `terraform plan`

## Check-Only Mode

When invoked with check-only (e.g., from `*health` pipeline):
- Execute Steps 1-5 only
- Do NOT modify any files
- Return the comparison table for reporting

## Edge Cases

- **Commented modules**: Skip commented-out module blocks. Note in output.
- **Multi-instance modules**: Multiple module blocks sharing the same `source`. Update ALL instances in the orchestrator file and the one shared variables file.
- **OCI charts**: Different helm_release pattern — `chart` field contains full OCI URL instead of `repository` + `chart`.
- **Nightly versions**: Semver parsing needs to handle pre-release suffixes (e.g., `1.81.8-nightly-latest`).
- **Version in module block comment**: Ignore comments, only update the `install_version` value.

## Error Handling

### Discovery Failures
- **0 orchestrator files found**: Report "No Helm module orchestrator found in this repository. This skill requires Terraform files with Helm module blocks." and stop.
- **Module directory doesn't exist**: Skip that module, log warning, continue with remaining modules.
- **No variable file found for a module**: Skip version consistency check for that module, warn user.
- **No version doc found**: Skip documentation updates silently (already covered in Step 0d).

### API Failures
- **ArtifactHub unreachable or returns error**: Fall back to displaying "???" in the Latest column and suggest manual checking. Provide the chart's repository URL so the user can check manually. Never block the pipeline on an API failure.
- **ArtifactHub returns unexpected format**: Log the raw response, skip that chart, continue with others.
- **Rate limited (HTTP 429)**: Wait 5 seconds and retry once. If still failing, fall back to manual check mode.

### Update Failures
- **File write fails**: Report which file failed and which files were already updated. Provide the original values for manual rollback.
- **Regex pattern doesn't match**: Report the expected vs. actual file content for the user to investigate. Do NOT force-write.

## Dry-Run Support

When invoked with `--dry-run` or when the user asks to "preview" or "check only":

1. Execute Steps 0-5 normally (discovery + version comparison)
2. For Step 7, instead of writing files, display a **diff preview** for each file:
   ```
   --- a/3-gke-package.tf
   +++ b/3-gke-package.tf
   @@ module "grafana" @@
   -  install_version = "10.5.4"
   +  install_version = "10.6.0"
   ```
3. Ask user to confirm before applying any changes
4. This is the default behavior — always show the diff preview before writing, unless the user explicitly requests immediate application

## Rollback Strategy

If an update needs to be reverted:

1. Before making changes in Step 7, record the **original values** for each file in memory:
   - File path, line number, original content
2. If the user requests rollback or if a subsequent validation fails:
   - Restore each file to its original content using the recorded values
   - Verify restoration by re-reading the files
3. If automatic rollback fails, provide the user with the exact original values and line numbers for manual restoration
4. Suggest `git checkout -- <file>` as a last resort if working in a clean Git state

## Dependencies

- UPGRADE_PATTERNS.md — File-specific regex patterns and edge cases
