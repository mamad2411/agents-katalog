# Documentation Agent Guide

## Scope

This file applies to everything under `docs/`. Follow the repository-root `AGENTS.md` as well.

## Canonical language and parity

- `docs/en/` is the canonical documentation source.
- `docs/zh/` is the required Simplified Chinese translation tree.
- Always update the English document first, then update its Simplified Chinese counterpart in the same change.
- Every durable document must have a counterpart at the same relative path in the other language tree.
- Paired documents must preserve equivalent meaning, heading hierarchy, examples, status labels, warnings, and link intent.
- Do not add information only to the Chinese version. If useful information originates in Chinese, incorporate it into the English canonical document and then translate it back faithfully.

## Organization

- Keep `docs/en/index.md` and `docs/zh/index.md` as the language-specific documentation routers.
- Use relative Markdown links only for repository documentation.
- Store documents in matching category directories under both languages.
- Do not place uncategorized documents directly under a language root other than `index.md`.
- Update both indexes whenever a document is added, moved, renamed, or removed.
- Agents must consult the relevant English document before making implementation or architecture decisions.

## Content ownership

- `architecture/` owns durable system boundaries, models, data flow, storage, and architectural decisions.
- `development/` owns repository layout, implementation conventions, frontend rules, testing, and developer workflows.
- `integrations/` owns external systems and protocol integrations such as OpenSpec.
- `contributing/` owns contribution and documentation maintenance policy.
- README files own only project introduction, quick start, and onboarding links.
- OpenSpec specs own stable requirements; active changes own proposed work.

## Accuracy

- Clearly label current implementation separately from target design.
- Verify current-state claims against source, tests, manifests, and configuration.
- Do not convert a design intention into a statement of shipped behavior.
- Update documentation when accepted architecture or externally observable behavior changes.

## Temporary material

Never reference `.tmp/` paths, file names, or temporary identities in committed documentation. Temporary material may inform a document only after its useful content has been restated as a durable project-owned requirement, decision, explanation, or example.

## Review checklist

- English source updated first.
- Simplified Chinese counterpart updated in the same change.
- Headings and coverage match.
- Relative links resolve and point to the corresponding language tree.
- Both language indexes are current.
- Current and planned behavior are clearly distinguished.
- No `.tmp/` references remain.
