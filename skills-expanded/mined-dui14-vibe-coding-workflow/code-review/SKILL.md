---
name: code-review
description: "Review a src path or diff against project standards and feature spec."
---

# Code Review

Two-axis review, reported separately:

- **Standards**: follows `AGENTS.md` + relevant `ai-context/` files?
- **Spec**: matches `spec/features/` or `spec/ui/`?

## Procedure

1. Define scope: a path (`src/[path]`) or a diff (`git diff <fixed-point>...HEAD`). Fail fast on bad ref or empty diff.

2. Load minimal context per `AGENTS.md`: always `03-architecture.md`, `06-coding-standards.md`, nearest `AGENTS.md`. Add others only if touched. Skip `N/A` files.
3. Find spec: `spec/features/[name].md` or `spec/ui/[screen].md`, else `spec/progress.md` or user path. If none, mark Spec `N/A`.
4. Check Standards: layer boundaries, naming, patterns, Code Rules, contract and token mismatches.
5. Check Spec: missing, partial, creep, or wrong behavior. Quote spec line per finding.
6. Report under `## Standards` and `## Spec` with `file:line`. End with counts + worst item per axis.

## Rules

- Keep axes separate; do not merge or rerank.
- Nearest `AGENTS.md` overrides generic judgement.
- Cite a source per finding; skip tooling-enforced items.
- Review only; do not fix code or touch unrelated files.
