---
name: Global Testing and Git Rules
alwaysApply: true
description: General testing and commit discipline for all projects.
---

# Global Testing and Git Rules

## Testing

After code changes:

1. Run focused tests for the touched area.
2. Run broader tests when the change affects shared logic.
3. Run formatting or lint checks if the project uses them.
4. Run `git diff --check` before committing.

If tests fail:

- Do not ignore failures.
- Identify whether the failure is related to the change.
- Fix related failures before committing.
- Report unrelated pre-existing failures separately.

## Commits

- Commit only relevant files.
- Do not commit generated junk files.
- Do not commit logs unless explicitly needed.
- Do not commit local cache directories.
- Use clear commit messages.

Commit message style:

```text
feat(scope): add ...
fix(scope): correct ...
docs(scope): add ...
test(scope): cover ...
chore(scope): update ...
Before final response

Always summarize:

files changed
tests run
commit hash if committed
remaining open issues

## Optional: installieren und committen?

Globale Rules liegen nicht im Projekt, also normalerweise **nicht committen**:

```bash
mkdir -p ~/.continue/rules
nano ~/.continue/rules/00-global-agent-behavior.md
nano ~/.continue/rules/01-global-code-quality.md
nano ~/.continue/rules/02-global-security.md
nano ~/.continue/rules/03-global-testing-and-git.md

Projektregeln bleiben zusätzlich hier:

.continue/rules/

Damit gilt:

Global = Arbeitsweise, Sicherheit, Tests, Git
Projekt = Atomizer, Nurovelle, API, Frontend
