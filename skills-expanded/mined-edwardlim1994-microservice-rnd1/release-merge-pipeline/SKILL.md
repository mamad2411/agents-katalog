# Release Merge Pipeline

## Purpose
Builds and tags a release candidate image when a story branch merges into the release branch.

## Role
DevOps Engineer

## Phase
Release

## Triggered By
`story/` PR merged to `release/` branch.

## Inputs
- Merged release branch commit

## Process
1. Secrets scan.
2. Build release candidate image.
3. Tag: `{service}-v{X}.{Y}.{Z}-rc{N}-{short-commit-hash}`.
4. Push to Harbor.
5. Create Git release tag: `v{X}.{Y}.{Z}-rc{N}`.
6. Harbor Trivy auto-scan.

## Outputs
Tagged release candidate image in Harbor, Git RC tag.

## Quality Gates
- [ ] Secrets scan passes before build
- [ ] RC image tagged per convention
- [ ] Git RC tag created
- [ ] Trivy scan completes on the RC image

## References
- `.claude/skills/release-manager/versioning/SKILL.md`
- `.claude/skills/devops-engineer/harbor-registry-management/SKILL.md`
