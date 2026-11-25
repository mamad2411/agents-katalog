---
name: github-actions-edit
description: Use when adding or changing anything under .github/ (workflows, composite actions, their scripts, dependabot) or bumping a pinned CI tool version such as golangci-lint, kubeconform or helm-docs. Pins every action to its latest release and audits all uses lines, not only the ones you touched.
---

# GitHub Actions edits

Goal: every `uses:` in `.github/` points at the current latest release of its action, pinned to an exact tag, and the workflows still pass. Versions remembered from training data or old notes are stale by definition, so look each one up. Stale majors run on deprecated Node runtimes, flood every run with deprecation warnings and miss fixes.

## Pin and audit

```sh
grep -rhoE 'uses: [^ ]+' .github | sort -u                    # every action in use
gh api repos/<owner>/<repo>/releases/latest --jq .tag_name    # latest release of one action
```

- Pin the full commit SHA of the release with the tag in a trailing comment (`@<sha> # v7.0.1`), resolved with `git ls-remote https://github.com/<owner>/<repo> refs/tags/<tag>` (annotated tags: use the commit the tag points at, `refs/tags/<tag>^{}`). Tags are mutable, SHAs are not. If an action publishes tags without GitHub releases, read its tags instead. Local composite actions (`./.github/actions/...`, `./release/.github/actions/...`) aren't versioned.
- On any workflow edit, audit every `uses:` line, not only the ones you touched, and bump the stale ones.
- Before a major bump, read the release notes for new requirements (for example, `golangci-lint-action` v9 needs golangci-lint v2, which needs `version: "2"` in `.golangci.yml`). Bump when compatible; flag it when not.
- Dependabot (`.github/dependabot.yml`) also proposes action bumps; that doesn't replace the audit.

## Pinned tools

| Tool | Where it's pinned |
|---|---|
| golangci-lint | `version:` in `.github/actions/go-ci/action.yaml` |
| kubeconform | `kubeconform-version` default in `.github/actions/helm-kubeconform-validate/action.yaml` |
| helm-docs | `HELM_DOCS` in the `Makefile` and the command in `.github/actions/helm-docs-regenerate/action.yaml`; keep both the same |

Bump the linter deliberately: run the new version locally over every Go service and shared package and fix what it finds before changing the pin, because a linter release can add rules that break unrelated PRs.

## Keep the gates

- Coverage floors in `ci.yaml` only go up. Don't relax lint, tests or checks to get a run green.
- Files matching `.github/workflows/local-*` are git-ignored and local-only.
