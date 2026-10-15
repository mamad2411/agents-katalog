---
name: github-release-expert
description: Set up or migrate a GitHub release pipeline that uses Release Please for automated release PRs, versioning, tags, and GitHub Releases, plus optional GoReleaser artifact publishing. Use when asked to automate releases on merge, replace manual tag-based releases, fix Release Please permission failures, fix missing release assets, validate end-to-end release behavior in GitHub, or set up CI with golangci-lint, gitleaks, govulncheck, or yamllint.
---

# Setup Release Please Pipeline

Build a reliable pipeline with three layers:
1. CI workflow for quality and security checks
2. Release Please workflow for release PR + tag/release metadata
3. Optional artifact publishing (GoReleaser jobs in the same workflow)

## Workflow

1. Audit current release setup.
   - Identify existing workflows, triggers, and manual release steps.
   - Confirm whether the repo already uses Conventional Commits.

2. Create or update CI workflow.
   - Trigger on `push` and `pull_request` to the default branch.
   - Run at least lint, test, and build checks.
   - Keep CI independent from release publishing.

3. Add Release Please configuration.
   - Add `release-please-config.json` and `.release-please-manifest.json`.
   - Set `initial-version`/manifest intentionally (often `0.1.0` for new projects).

4. Add Release Please workflow **using the two-job pattern** (critical — see below).
   - Put `release-please` and the artifact publisher (e.g. goreleaser) in the **same** workflow file.
   - Required permissions: `contents: write`, `pull-requests: write`.

5. Configure repository Actions permissions — required before first run:
   ```bash
   gh api repos/OWNER/REPO/actions/permissions/workflow \
     --method PUT \
     -F default_workflow_permissions=write \
     -F can_approve_pull_request_reviews=true
   ```
   Without this, Release Please cannot open release PRs and will fail silently.

6. Validate end-to-end.
   - Push a `feat:` commit to trigger Release Please.
   - Confirm: release PR created → merge → tag created → artifacts attached.

## The Two-Job Pattern (Critical)

**Never split Release Please and GoReleaser into separate workflow files.**

GitHub Actions does not allow a workflow triggered by `GITHUB_TOKEN` to fire another workflow. If Release Please creates a release using `GITHUB_TOKEN`, a separate `goreleaser.yml` listening on `release: [published]` will **never run**.

The fix: put both jobs in the same `release-please.yml` file and pass the tag directly:

```yaml
jobs:
  release-please:
    runs-on: ubuntu-latest
    outputs:
      release_created: ${{ steps.release.outputs.release_created }}
      tag_name: ${{ steps.release.outputs.tag_name }}
    steps:
      - uses: googleapis/release-please-action@v4
        id: release
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          config-file: release-please-config.json
          manifest-file: .release-please-manifest.json

  goreleaser:
    needs: release-please
    if: needs.release-please.outputs.release_created == 'true'
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          ref: ${{ needs.release-please.outputs.tag_name }}
      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
      - uses: goreleaser/goreleaser-action@v6
        with:
          args: release --clean
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Required GitHub Settings

Repository Actions settings must allow Release Please to write:
- Settings → Actions → General → Workflow permissions: **Read and write permissions**
- Enable: **Allow GitHub Actions to create and approve pull requests**

Or via CLI (easier):
```bash
gh api repos/OWNER/REPO/actions/permissions/workflow \
  --method PUT \
  -F default_workflow_permissions=write \
  -F can_approve_pull_request_reviews=true
```

## Release Numbering Guidance

- New projects usually start at `0.1.0`.
- For pre-1.0 behavior, use:
  - `bump-minor-pre-major: true`
  - `bump-patch-for-minor-pre-major: true`
- If a wrong major line was produced, correct config/manifest before next release.

## Troubleshooting Checklist

1. **Release PR created, but no assets attached.**
   - Almost certainly a separate-workflow problem — see two-job pattern above.
   - Verify `release_created` condition and tag checkout (`ref: tag_name`).

2. **Release Please fails with "not permitted to create pull requests".**
   - Repository Actions permissions are set to read-only.
   - Fix: set `default_workflow_permissions=write` via `gh api` (see above).

3. **GoReleaser fails: "tag not made against this commit".**
   - The goreleaser job is running against HEAD, not the tagged commit.
   - Fix: `ref: ${{ needs.release-please.outputs.tag_name }}` in checkout step.

4. **CI green locally but red in GitHub.**
   - Tool version mismatch (especially golangci-lint — see Go reference).
   - Validate local task versions with workflow tool versions.

5. **govulncheck fails on standard library CVEs.**
   - Pin workflows to a patched Go version, not an affected patch level.

## Go-Specific Guidance

For Go repos with GoReleaser, read `references/go-goreleaser.md` — it covers:
- golangci-lint v2 module path and Go version compatibility
- gitleaks CLI (avoids paid license requirement of gitleaks-action)
- syft installation for SBOM generation
- goreleaser config with SBOM, checksums, cross-compilation
