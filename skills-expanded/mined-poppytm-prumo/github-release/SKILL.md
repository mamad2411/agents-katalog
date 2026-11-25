# GitHub Release Packaging

## Purpose
Ship trustworthy releases: SemVer-correct tags, generated changelog deltas, verified build assets with checksums, and release notes that state upgrade impact honestly — including breaking changes and migration steps.

## Use when
- Cutting a versioned release (major, minor, patch, or prerelease) from `main` or a release branch.
- Publishing release notes with changelog, asset list, and upgrade guidance.
- Auditing a past release for missing assets, wrong version bumps, or undocumented breaking changes.
- Operating in mode(s): `documentation`, `implementation`.

## Do not use when
- Handling reviewer feedback on a PR (use `github-pr-feedback`).
- Debugging CI pipeline failures (use `github-ci-debug`).
- Deciding product roadmap or what ships (release implements the decision; product owns it).

## Required context
- Previous tag and target version (SemVer bump rationale: breaking/feature/fix).
- Merged PR list since last release (for changelog generation, e.g. `gh api repos/{owner}/{repo}/releases/generate-notes`).
- Build and signing pipeline: asset matrix (binaries, checksums file, SBOM), expected CI workflow.

## Procedure
1. **Confirm SemVer intent**: classify the bump from merged changes (any breaking API/config change → major; additive feature → minor; fixes only → patch); prereleases use `-rc.N` suffixes and never mutate published tags.
2. **Generate the delta**: produce changelog from merged PRs grouped as Features / Fixes / Breaking, each entry linking its PR and issue; never hand-write entries that automation can derive.
3. **Build from the tag**: create the annotated tag, push, and let CI build assets from that exact commit; verify asset matrix complete (per-platform binaries, `SHA256SUMS`, SBOM) and checksums match downloads.
4. **Write honest notes**: lead with upgrade impact (breaking changes + migration steps first), then highlights, then full changelog link; state supported upgrade paths explicitly.
5. **Verify the published release**: fetch the release via `gh release view`, confirm tag target SHA equals the intended commit, assets downloadable, and notes render correctly.
6. **Record evidence**: link the release URL, CI run, and checksum verification output in the task report.

## Decision rules
- **Tags are immutable**: never force-move a published tag; cut a new patch instead.
- **No silent breaking changes**: any breaking change ships with migration steps in the notes or the release is blocked.
- **Assets from CI only**: hand-uploaded binaries without a reproducible CI build are prohibited.
- **Checksum mandatory**: every downloadable asset is covered by a published checksum file.

## Evidence required
- Release URL, tag SHA match proof, and checksum verification log.
- Changelog delta review (grouped entries with PR links).
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Structured GitHub artifact (published release with notes, assets, checksums).
- Validation confirmation (tag-SHA match + asset verification).

## Stop conditions
- Release published with correct SemVer, complete verified assets, and honest notes.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to maintainer if a published release needs yanking or a security-driven expedited patch.
- Escalate immediately on compromised signing keys or tampered assets.
