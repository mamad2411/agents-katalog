---
name: ns-docs-writer
description: (NS) Write and edit human-facing project documentation — README, docs/ guides, runbooks, and contributor-facing markdown. Use whenever the user asks for documentation, README updates, how-to guides, or docs/ content — even if they say "explain how to use" instead of "write docs". Stack-agnostic; follow project layout from AGENTS.md. Do NOT use for code comments, API docblocks in source, requirements.md, or SDD version artifacts (use PM skills).
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.0"
depends:
  - ns-harness
---

# Docs Writer

Author **clear, maintainable** project documentation under `docs/` and README files.

## Session boot

See `../../ns-harness/references/session-boot.md`.

## Scope

| In scope | Out of scope |
| -------- | ------------ |
| `README.md` at product or repo root | Inline `//` or `/**` code comments |
| `docs/**/*.md` guides | `docs/versions/*/requirements.md` |
| Runbooks, install guides, architecture overviews for humans | Living specs in `docs/specs/` (use `ns-living-spec`) |
| Changelog entries when requested | Marketing copy outside repo |

## When to use

- New feature needs user or developer documentation
- README is stale after structural changes
- Onboarding guide for contributors
- Consolidating scattered notes into `docs/`

## Workflow

1. **Discover** — list existing `docs/`, README, and `AGENTS.md` links; avoid duplicating harness/brownfield artifacts (link instead).
2. **Audience** — confirm developer vs operator vs end-user (default: developer).
3. **Outline** — short TOC before drafting long guides.
4. **Draft** — follow `references/style-guide.md`.
5. **Link** — prefer relative links; point to canonical rules in `.nextstage-harness/rules/` when relevant.

## Layout (stack-agnostic)

Do not assume monorepo `packages/` layout. Infer from:

- `AGENTS.md` layout table
- `architecture-rules.md`
- Existing `docs/` structure

Create subfolders only when they match project convention.

## Integration

When called from `ns-spec-driven`, document **delivered behavior** — do not invent requirements.

## Forbidden

- Copying full bodies of `brownfield-map.md` or `system-reverse-spec.md` into new docs (link them)
- English violations when project mandates English docs
- Auto-generating docs for code that does not exist yet
