---
name: github_actions_node24
description: Cheatsheet for resolving Node 20 deprecation warnings, bumping major versions of GitHub Actions for Node 24 support, and resolving related input/cache errors.
---

# GitHub Actions Node 24 Migration Guide

**CRITICAL INSTRUCTION:** Whenever a GitHub workflow file (e.g., in `.github/workflows/`) is created or modified alongside other repository changes, you MUST proactively check and bump the major versions of any affected actions to ensure Node 24 support, using the versions listed below. Do not wait for a deprecation warning to appear.

When a GitHub Action runner complains about Node 20 deprecation (`Node.js 20 is deprecated... forced to run on Node.js 24`), simply injecting `setup-node` does not fix third-party actions. You MUST bump the major version of the affected actions.

## Action Version Cheatsheet (Node 24 Support)
> [!IMPORTANT]
> **Security Pinning Constraint:** While upgrading actions to these Node 24-compatible major versions, you MUST pin the action step to its explicit 40-character commit SHA (e.g. `uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1`) instead of using the mutable tag/branch name (e.g., `@v7`, `@v4`). Using mutable tags triggers automated SAST warnings (such as Semgrep) and exposes workflows to supply-chain attacks.
>
> You can query the latest commit SHA for a tag using `git ls-remote https://github.com/org/repo.git refs/tags/vX*`.

Bump to these major versions to resolve Node 20 deprecation warnings:
- `actions/checkout` -> `@v7` (e.g., `3d3c42e5aac5ba805825da76410c181273ba90b1` for `v7.0.1`)
- `actions/setup-node` -> `@v6`
- `actions/cache/restore` -> `@v5`
- `actions/cache/save` -> `@v5`
- `docker/login-action` -> `@v4`
- `docker/setup-qemu-action` -> `@v4`
- `docker/setup-buildx-action` -> `@v4`
- `docker/build-push-action` -> `@v7`
- `docker/metadata-action` -> `@v6` *(Note: v7 does not exist yet!)*
- `gitleaks/gitleaks-action` -> `@v3`
- `softprops/action-gh-release` -> `@v3`

## Known Unpatched Actions
- `mathieudutour/github-tag-action@v6.1` currently lacks native Node 24 support. Warnings associated with this action are benign and safe to ignore until the maintainer publishes a new major release.

## Common Errors & Quirks

### Gitleaks Action (`Unexpected input(s) 'args'`)
- **Error:** `Unexpected input(s) 'args', valid inputs are ['']`
- **Cause:** Strict input validation in GitHub Actions rejects the `args` parameter for `gitleaks/gitleaks-action@v3`.
- **Solution:** Remove the `with: args: ...` block entirely. The action executes the default `detect` command and outputs a report automatically.

### QEMU Cache Locking (`Unable to reserve cache with key`)
- **Error:** `Failed to save: Unable to reserve cache with key docker.io--tonistiigi--binfmt-latest-linux-x64, another job may be creating this cache.`
- **Cause:** Race condition when concurrent jobs (e.g., simultaneous push and PR triggers) attempt to save the exact same QEMU cache.
- **Solution:** This is a benign warning. It does not fail the build and does not impact the resulting container image. Safely ignore it.

## Anti-Patterns

- NEVER deploy code changes without validating them against target test suites.
- NEVER skip documenting non-obvious code assumptions, constraints, and side effects.


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
