---
name: repo-bootstrap
description: "Bootstrap a new or newly adopted repository with standard metadata, license posture, package metadata, issue and PR templates, labels, Codex guidance, validation guidance, and lightweight governance. Use when creating a repo, onboarding an existing repo, or applying the standards pack for the first time."
---

# Repo Bootstrap

Use this skill for first-pass setup of a repository.

## Workflow

1. Inspect repository purpose, visibility, default branch, package manager, validation surface, deployment target, and whether the repo contains first-party or vendored code.
2. Add or verify root `LICENSE` with the selected project license.
3. For first-party packages, align package metadata with repository visibility, publishability, and the selected license.
4. Apply standard issue templates, PR template, labels, Codex guidance, and product-specific About metadata.
5. Disable Wiki and per-repo Projects unless intentionally used.
6. Document the minimal validation that can pass today. Add hosted CI only when it is intentionally selected for the repository.
7. Verify all GitHub metadata after changes.

## Decision Rules

- Do not use generic About text when product-specific metadata can be inferred.
- Do not overwrite meaningful existing descriptions, URLs, or templates without approval.
- Keep single-developer governance light: prefer safety checks over mandatory review ceremony.
- Treat vendored code as third-party and avoid rewriting its package metadata.
- Do not add workflow files or hosted runner dependencies without explicit owner approval.

## Output

Summarize:

- Metadata changed.
- Files added or updated.
- Governance settings changed.
- Verification commands and GitHub reads performed.
