---
name: go-module-hygiene
description: >
  Go modules hygiene: go.mod/go.sum discipline, go mod tidy, MVS awareness,
  retract, exclude, replace pitfalls, pseudo-versions, and dependency review.
  Use for owned modules before release; pair with govulncheck and sumdb verify.
---

# Go Module Hygiene

## Scope And Authorization

- **In scope:** Modules you maintain or are authorized to update.
- **Out of scope:** Force-pushing module paths you do not own on the public proxy.
- Never commit secrets in modules; treat `replace => ../local` carefully for releases.
- Pair with `go-govulncheck-workflow`, `go-sumdb-verify`, `go-module-release-workflow`.

## When To Use

- Cleaning dirty `go.mod` after experiments.
- Preparing a tagged release of a library.
- Reviewing PRs that add large dependency trees.
- Removing abandoned `replace` directives before publish.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Publishing/tagging modules | `go-module-release-workflow` |
| Vulnerability scan | `go-govulncheck-workflow` |
| Checksum DB | `go-sumdb-verify` |
| Style | `go-style-conventions` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Term | Meaning |
| --- | --- |
| MVS | Minimal version selection — highest required min versions |
| `go.mod` | Module path, go version, require/exclude/retract/replace/tool |
| `go.sum` | Cryptographic checksums of deps |
| Pseudo-version | `v0.0.0-yyyymmddhhmmss-commithash` |
| `retract` | Publisher marks bad versions |
| `replace` | Local/fork override — **not** for public consumers usually |
| `exclude` | Block bad versions in your build |

## Workflow

### 1. Baseline

```bash
go version
cat go.mod
go list -m all | head
go mod verify
```

### 2. Tidy and verify

```bash
go mod tidy
go mod verify
git diff go.mod go.sum
```

Ensure CI fails if `go mod tidy` produces a diff:

```bash
go mod tidy
git diff --exit-code go.mod go.sum
```

### 3. Add/upgrade deps deliberately

```bash
go get example.com/foo@v1.2.3
go get example.com/foo@latest
go get example.com/foo@none   # remove
go mod tidy
```

Review:

- License compatibility
- Import surface (do you need the whole SDK?)
- Star/maintenance signals
- Transitive count (`go mod graph | wc`)

### 4. replace discipline

```go
// go.mod — OK for local dev, bad for released libraries without docs
replace example.com/foo => ../foo
```

Before tagging a public module:

- [ ] Remove local replaces or document forks with versioned replace to remote
- [ ] Prefer upstream merge over permanent replace

### 5. retract bad releases (as publisher)

```go
retract (
    v1.0.1 // wrong go.sum / broken API
    [v1.1.0, v1.1.3] // security
)
```

Publish retract in a newer version; communicate to consumers.

### 6. exclude (as consumer)

```go
exclude example.com/foo v1.2.3
```

Temporary shield; still plan upgrade path.

### 7. Toolchain / go line

```go
go 1.22
// optionally: toolchain go1.22.5
```

Keep CI and developers aligned; avoid accidental old compiler.

### 8. PR review checklist

- [ ] `go mod tidy` clean
- [ ] `go.sum` updated with `go.mod`
- [ ] No unexpected module path changes
- [ ] No secrets in new deps’ install scripts (rare but check)
- [ ] govulncheck clean
- [ ] replace absent or justified

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| tidy | CI enforces | Hand-edit require randomly |
| replace | Local only / documented fork | Ship library with `=> ../` |
| Versions | Semantic tags | Always `@master` pseudo forever |
| sum | Committed + verified | Delete go.sum lines to “fix CI” |
| Scope | Minimal deps | Import huge SDK for one func |

## Output Checklist

- [ ] go.mod tidy and consistent
- [ ] go.sum verified
- [ ] replaces reviewed
- [ ] retracts published if you broke releases
- [ ] Dependency review notes for new requires
- [ ] CI tidy check enabled
- [ ] Linked vuln + sumdb skills
- [ ] `code-quality-standards` applied

## Rules

- Commit `go.mod` and `go.sum` together.
- Do not hand-hack checksums.
- Public modules: no private replace leftovers.
- Prefer tagged versions over floating branches.
- Release process → `go-module-release-workflow`.
