---
name: release-upgrade
description: Performs a full release upgrade — bumps version in AI_ACCELERATOR_STACK_VERSION, vars.tf, and common_schema.yaml, validates with terraform fmt/validate, creates a test matrix, and generates per-pack ORM zip files. Use when cutting a new release version (e.g., /release-upgrade v0.0.4).
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, Edit, Write, TaskCreate, TaskUpdate, TaskGet, TaskList
argument-hint: [version]
---

# Release Upgrade

Automate the release upgrade process for AI Accelerator Starter Packs.

## Arguments

- `$0` — New version in semver format (e.g., `v0.0.4`, `v1.0.0`). If not provided, ask the user.

## Prerequisites

1. Ensure working directory is clean (`git status`)
2. Confirm on the correct release branch (`release_v<VERSION>`). If not, look for it. If it doesn't exist, create it from latest main.
3. Ask the user if they also want to update `corrino_image_version`

## Step 1: Validate Version Format

- Must match `vMAJOR.MINOR.PATCH`
- Read current version from `ai-accelerator-tf/AI_ACCELERATOR_STACK_VERSION`
- Compare semver components numerically to confirm new version is higher:
  ```
  Split both versions on "." after stripping "v" prefix.
  Compare MAJOR, then MINOR, then PATCH as integers.
  ```

## Step 2: Update Version Files

All three files must be updated together — never proceed with partial updates.

**a. `ai-accelerator-tf/AI_ACCELERATOR_STACK_VERSION`**
- Replace contents with the new version

**b. `ai-accelerator-tf/vars.tf`**
- Update `accelerator_pack_stack_version` default value
- Optionally update `corrino_image_version` if requested in prerequisites

**c. `ai-accelerator-tf/schemas/common_schema.yaml`**
- Add new version to the TOP of the `accelerator_pack_stack_version` enum list
- Update default to new version
- Keep all previous versions for rollback capability

## Step 3: Validate

Run validation with a feedback loop — fix and retry until clean:

```bash
cd ai-accelerator-tf
terraform fmt -recursive
terraform validate
```

If schema was updated, also regenerate and test:
```bash
cd schemas && python3 create_final_schema.py --all
cd .. && pytest schemas/tests/ -v
```

Clean up build artifacts after validation:
```bash
find . -name ".terraform" -type d -exec rm -rf {} + 2>/dev/null
rm -f .terraform.lock.hcl
```

If validation fails, fix the issues and re-run. Only proceed when all checks pass.

## Step 4: Display Summary

- Show all files updated
- Display `git diff` of changes
- Ask user to confirm before proceeding

## Step 5: Commit and Push

After user confirmation:

```bash
git add ai-accelerator-tf/AI_ACCELERATOR_STACK_VERSION \
       ai-accelerator-tf/vars.tf \
       ai-accelerator-tf/schemas/common_schema.yaml
git commit -m "Release <VERSION>"
git push -u origin release_v<VERSION>
```

## Step 6: Create Test Matrix

See [TEST_MATRIX.md](TEST_MATRIX.md) for the full test matrix creation workflow.

## Step 7: Create Zip Files

See [ZIP_PACKAGING.md](ZIP_PACKAGING.md) for the release zip packaging workflow. The core exclusion logic (`.terraform/`, `.terraform.lock.hcl`, sensitive `*.tfvars`, `__pycache__/`, `.pytest_cache/`) is shared with `/zip-tf`.

## Next Steps

After zip files have been created, tested via the test matrix, and all packs pass:

Run `/release-push <VERSION>` to validate zips, rename for distribution, generate the Slack announcement, merge the release PR, and tag the release.

## Starter Pack Ownership

See [OWNERS.md](OWNERS.md) for current starter pack owner assignments.

## Version Conventions

- **MAJOR**: Breaking changes requiring user action
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes and minor improvements

## Error Handling

- If any file update fails, stop and report the error
- If validation fails, show errors and suggest fixes
- Never proceed with partial updates — all files must be updated together
