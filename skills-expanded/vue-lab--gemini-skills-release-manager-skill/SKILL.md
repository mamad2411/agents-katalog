---
name: release-manager
description: Independent workflows for the release lifecycle. Handles Milestone-to-Develop PRs, Develop-to-Main PRs, and Git Tagging/Releases as separate, independent tasks. Use this only when a specific release operation is requested.
---

# Release Manager

This skill provides independent workflows for managing high-level branch transitions and releases. These are **not** sequential; each must be invoked separately.

## Independent Workflows

### 1. [OP: MILESTONE-TO-DEVELOP]
- **Goal**: Merge a completed milestone into the development branch.
- **Action**: 
    1. Verify all tests pass on the `milestone/X` branch.
    2. Open a PR from `milestone/X` to `develop`.
    3. Link the PR to the GitHub milestone.
- **Stop**: Wait for the user to merge and confirm before any further action.

### 2. [OP: DEVELOP-TO-MAIN]
- **Goal**: Prepare a production-ready PR.
- **Action**:
    1. Open a PR from `develop` to `main`.
    2. Title it "Release Candidate [Version]".
- **Stop**: Wait for PR approval and merge.

### 3. [OP: TAGGING-AND-RELEASE]
- **Goal**: Finalize a production release.
- **Action**:
    1. Create a signed git tag (e.g., `git tag -a v1.0.0 -m "Release v1.0.0"`).
    2. Use `gh release create` to generate the final release notes.
    3. Push the tag to remote.

## Mandates
- Do NOT combine these operations unless explicitly asked.
- Verify branch stability before every operation.
- Use `gh` CLI for all PR and release actions.
