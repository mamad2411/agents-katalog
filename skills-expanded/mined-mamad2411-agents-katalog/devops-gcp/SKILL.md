---
name: devops-gcp
description: Containerize and ship apps with Docker, CI/CD pipelines that deploy on a MANUAL trigger, and Google Cloud Platform. Use when setting up build/deploy, writing Dockerfiles or CI workflows, or planning a release. Primary skill of the release-engineer.
---

# DevOps on GCP

## Docker
Multi-stage builds; minimal base (alpine/distroless); run as non-root; `.dockerignore`; pin versions; add a healthcheck.

## CI/CD (manual-trigger deploy)
- CI on every push/PR: build, lint, test.
- Deploy is a SEPARATE, MANUALLY triggered job (e.g. GitHub Actions `workflow_dispatch` or an environment approval) — never auto-deploy on merge.
- Promote along branches: `development` → staging env, `main` → production — each a manual trigger.

### Tag & release on the production deploy (`main`)
The production deploy job (manual `workflow_dispatch` / environment approval, targeting `main`) ends
by tagging the released version — idempotently, so it is safe to run on every deploy:

- `permissions: { contents: write }` — required to push the tag and create the Release.
- Run **only** when the ref is `main`, and **after** the deploy step succeeds.
- Read the version from the manifest (`package.json` / `composer.json` / `VERSION`).
- If `git tag -l "v$VERSION"` is non-empty → already tagged; log and skip.
- Else → create annotated tag `v$VERSION`, push it, and `gh release create "v$VERSION"` with notes
  from the matching `CHANGELOG.md` section.

Re-deploying the same version is a no-op; a deploy after a bump cuts the new tag. Never tag from
`development`/`staging`. See `release-management` for the version-derivation rule.

**No deploy job?** A repo with nothing to deploy (a library/docs/plugin) has no production deploy job
to host this step — publish the tag + forge Release manually at Gate ④ instead (`gh release create`
with `CHANGELOG.md` notes; see `git-conventions` → Production release).

**Forge:** GitHub Actions + `gh release create` is shown because **GitHub is the default**. If the git
remote is a GitLab host, generate the GitLab CI analog (`glab release create` / Releases API) instead —
the tag step and idempotency are identical. Detect the forge during `stack-detection`; default to
GitHub when unknown.

## GCP targets
- **Cloud Run** (default for containers): scale-to-zero, pay-per-use; deploy the built image.
- **Artifact Registry** for images; **Cloud SQL** (MySQL) for the database; **Secret Manager** for secrets (never bake them into images).
- Least-privilege service accounts; set min/max instances to balance latency vs cost.

## Output (05-release.md)
Build/deploy steps, CI config added, env/secret needs, the version, and the manual deploy-trigger instructions.

> The CI workflow + Dockerfile you author are audited by `cicd-pipeline-audit` — the release-engineer
> self-audits in Phase 5, and the `pipeline-reviewer` audits any pre-existing config in Phase 4.
> Author config that passes: pinned actions, least-privilege `permissions:`, job timeouts, caching,
> and a manual-trigger deploy. If a run later fails, `/sdlc-fix-ci` diagnoses it and repairs config issues.
