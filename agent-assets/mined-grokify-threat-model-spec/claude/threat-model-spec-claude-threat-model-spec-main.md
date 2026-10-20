# CLAUDE.md

Project-specific guidelines for threat-model-spec.

## Release Workflow

When releasing a new version (e.g., v0.X.0):

### 1. Versioned Specification

Create `docs/versions/vX.Y.Z/` directory with:

- `specification.md` — Full specification document for this version
- `threat-model.schema.json` — Copy from `schema/`
- `diagram.schema.json` — Copy from `schema/`

Update references in README.md and docs to point to new version.

### 2. Changelog Updates

1. Update `CHANGELOG.json` with new version entry (highlights, added, changed, documentation sections)
2. Regenerate `CHANGELOG.md`: `schangelog generate CHANGELOG.json -o CHANGELOG.md`
3. Sync docs: `cp CHANGELOG.md docs/changelog.md`

### 3. Release Notes

Create `docs/releases/vX.Y.Z.md` with:

- Release date
- Highlights
- What's New sections
- Installation instructions
- Links to specification and documentation

### 4. MkDocs Navigation

Update `mkdocs.yml` nav sections:

- **Versions**: Add `vX.Y.Z: versions/vX.Y.Z/specification.md`
- **Releases**: Add `vX.Y.Z: releases/vX.Y.Z.md`
- **Plans**: Add `vX.Y.Z: plans/vX.Y.Z-plan.md` (after archiving)

### 5. Archive Plan

If using PLAN.md for the release:

1. Update status to "✅ Completed"
2. Move to docs/plans/: `git mv PLAN.md docs/plans/vX.Y.Z-plan.md`

## Development Workflow

### Planning

Use `PLAN.md` in root for active development plans. Structure:

```markdown
# Threat Model Spec vX.Y.Z Enhancement Plan

> **Status:** 🚧 In Progress
>
> **Goal:** [Brief goal description]

## Overview
## Planned Enhancements
## Implementation Order
## Success Criteria
```

### JSON Schema Generation

Go structs are the source of truth. After modifying `ir/` types:

1. Regenerate schemas: `go run cmd/genschema/main.go -version=vX.Y.Z`
2. Copy to versioned docs: `cp schema/*.schema.json docs/versions/vX.Y.Z/`
3. Run tests: `go test ./...`

### Testing

Add tests for new types in `ir/*_test.go`:

- Enum value tests (e.g., `TestXxx_Values`)
- JSON round-trip tests (e.g., `TestXxx_JSON`)
- Field tests for structs (e.g., `TestXxx_Fields`)
- Method tests if applicable (e.g., `TestRiskAssessment_Calculate`)

### Agent/Command/Skill Plugin Generation

`agents/specs/` is the source of truth, written against the
[multi-agent-spec](https://github.com/plexusone/multi-agent-spec) schema
(agents/commands/skills as platform-agnostic Markdown+frontmatter or JSON).
`agents/plugins/{claude,kiro,gemini}/` are **generated output** — never
hand-edit files under `agents/plugins/` directly, including to fix a
one-off formatting issue. A hand-edit can silently diverge from what the
generator actually produces (e.g. Go's JSON encoder HTML-escapes `<`/`>`/`&`
by default; a manual Python-based edit will not, and the divergence won't
show up until the next real regeneration overwrites it).

After changing anything under `agents/specs/`, regenerate all platform
outputs with [assistantkit](https://github.com/plexusone/assistantkit):

```bash
assistantkit generate --specs=agents/specs --target=dist --output=.
```

Then verify with the freshness tests, which fail if a spec and its
generated plugin output have drifted apart:

```bash
go test ./agents/... -run Fresh
```

## Commit Convention

Follow conventional commits. Common types for this project:

| Type | Use For |
|------|---------|
| `feat(ir)` | New IR types or fields |
| `feat(stix)` | STIX export changes |
| `feat(cmd)` | CLI changes |
| `schema` | Schema regeneration |
| `test(ir)` | IR package tests |
| `docs` | Documentation, release notes, changelog |
| `chore` | Plan archiving, dependency updates |

## File Organization

```
ir/                          # Go types (source of truth)
  ├── risk.go               # Risk assessment types
  ├── assets.go             # Asset classification
  ├── scenarios.go          # Scenario modeling
  ├── diagram.go            # Diagram IR, NetworkInfo
  ├── threat_model.go       # ThreatModel type
  └── *_test.go             # Tests for each file

schema/                      # Generated JSON schemas
  ├── threat-model.schema.json
  └── diagram.schema.json

docs/
  ├── versions/vX.Y.Z/      # Versioned specifications
  ├── releases/             # Release notes
  ├── plans/                # Archived development plans
  ├── guides/               # User guides
  └── changelog.md          # Synced from root CHANGELOG.md
```

## Pre-Release Checklist

- [ ] All tests pass: `go test ./...`
- [ ] Linting clean: `golangci-lint run`
- [ ] CHANGELOG.json updated
- [ ] CHANGELOG.md regenerated
- [ ] docs/changelog.md synced
- [ ] Release notes created
- [ ] Versioned specification created
- [ ] mkdocs.yml nav updated
- [ ] README.md updated with new version
- [ ] PLAN.md archived (if applicable)
- [ ] Push and wait for CI before tagging
