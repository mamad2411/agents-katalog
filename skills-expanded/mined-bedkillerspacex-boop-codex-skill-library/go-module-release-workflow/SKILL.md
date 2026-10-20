---
name: go-module-release-workflow
description: >
  Release workflow for public/private Go modules: semver tags, module paths,
  v2+ major paths, pre-release tags, go.mod go version, changelog, proxy
  indexing, and retract. Use when publishing owned modules consumers will import.
---

# Go Module Release Workflow

## Scope And Authorization

- **In scope:** Modules your team owns and may tag/publish.
- **Out of scope:** Tag bombing others’ repositories; impersonating module paths.
- Tags are largely **immutable** in the public ecosystem — test before pushing tags.
- Pair with `go-module-hygiene`, `changelog-and-release-notes`, `go-govulncheck-workflow`.

## When To Use

- Cutting `vX.Y.Z` for a library.
- Introducing a v2 major with `/v2` path.
- Publishing first version of a new module.
- Retracting a broken release.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Day-to-day go.mod hygiene | `go-module-hygiene` |
| Vuln scan | `go-govulncheck-workflow` |
| Sum DB | `go-sumdb-verify` |
| Commit messages | `commit-message-conventions` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Rule | Detail |
| --- | --- |
| Semver | `vMAJOR.MINOR.PATCH` tags |
| Major ≥ 2 | Import path must end with `/vN` matching major |
| Pseudo-versions | For untagged commits — avoid for official releases |
| Proxy | proxy.golang.org caches versions after fetch |
| Canonical | Module path in go.mod must match repo layout |
| Pre-release | `v1.2.3-rc.1` — not chosen by `@latest` the same way as stables |

## Workflow

### 1. Preflight

```bash
go test ./...
go test -race ./...
govulncheck ./...
go mod tidy
go mod verify
git status  # clean tree
```

- [ ] API changes reviewed (breaking?)
- [ ] Docs/godoc updated
- [ ] Changelog entry drafted
- [ ] No local `replace`

### 2. Version decision

| Change | Version bump |
| --- | --- |
| Bugfix, compatible | PATCH |
| New compatible API | MINOR |
| Breaking API | MAJOR (+ `/vN` path if ≥2) |
| First stable | `v1.0.0` after intentional freeze |

### 3. Major v2+ example

```go
// module example.com/foo/v2
// import "example.com/foo/v2"
```

Repo layout often `foo/v2/` or root with go.mod path `/v2` per team convention.
Do not tag `v2.0.0` without path suffix — consumers break.

### 4. Tag and push

```bash
git checkout main
git pull
# ensure commit to release is on main
git tag -a v1.4.0 -m "v1.4.0"
git push origin v1.4.0
git push origin main
```

Annotated tags preferred.

### 5. Verify fetch as consumer

```bash
# From empty module
go get example.com/foo@v1.4.0
go list -m example.com/foo
```

Check pkg.go.dev (may lag) and `GOPROXY`.

### 6. Pre-releases

```bash
git tag -a v1.5.0-rc.1 -m "v1.5.0-rc.1"
git push origin v1.5.0-rc.1
```

Consumers opt in explicitly: `go get example.com/foo@v1.5.0-rc.1`.

### 7. Broken release → retract

1. Fix forward; tag `v1.4.1`.
2. Add to go.mod:

```go
retract v1.4.0 // incorrect checksum / panic on nil
```

3. Tag version that contains retract (e.g. `v1.4.1` or later).
4. Announce; do not delete public tags lightly (proxy may have cached).

### 8. Monorepo multi-module

- Each module own go.mod; tag with subdirectory prefix if required
  (`git tag services/api/v1.2.3` patterns) matching Go’s versioning rules for nested modules.
- Document tagging scheme in CONTRIBUTING.

### 9. Automation (optional)

- CI on tag: tests, govulncheck, goreleaser for binaries (libs may only need tags).
- CODEOWNERS for release branches.
- Release PR checklist bot.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Tags | Annotated semver on tested commit | Move tags after people fetched |
| Breaking | `/v2` path | v2 tag with v1 import path |
| Hygiene | tidy + no replace | Tag with broken tests |
| Retract | Document reason | Silent broken forever |
| Docs | Changelog + migration | “See commits” only |

## Output Checklist

- [ ] Tests/race/vuln clean
- [ ] Version bump rationale recorded
- [ ] go.mod path correct for major
- [ ] Changelog updated
- [ ] Annotated tag pushed
- [ ] Consumer `go get` verified
- [ ] Retract plan if issues found
- [ ] Monorepo tag scheme followed
- [ ] `code-quality-standards` applied to API changes

## Rules

- Test before tag; tags are sticky.
- Major ≥2 requires path `/vN`.
- No private replace in released modules.
- Prefer retract over history rewrite.
- Hygiene skill for day-to-day; this for publish moments.
