# Repository Instructions

## Project Context

Before making changes, read `README.md` to understand the repository structure, rebuild commands, desktop selection, and installation flow.

## Change Guidelines

- Keep changes small and focused.
- Do not include unrelated worktree changes in commits.

## Commit Guidelines

- Keep commits as small as possible and limited to one logical change.
- If a file contains changes for multiple logical changes, stage and commit only the relevant hunks instead of committing the entire file.
- Use conventional commit messages without scopes.
- Include a commit body with bullet points describing what changed.

## Verification

For Nix changes, run the most targeted Nix verification command that applies to the change before claiming it is complete. If verification is skipped, state why.
