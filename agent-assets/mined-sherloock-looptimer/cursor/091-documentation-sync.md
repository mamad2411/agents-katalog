---
description: Keep README, package.json scripts, and env.example in sync (no separate doc files).
globs:
  - "package.json"
  - "README.md"
  - "env.example"
alwaysApply: false
---

## Documentation sync (mandatory)

### When you modify package.json scripts

1. Update inline section comments in package.json.
2. Add or update the corresponding one-line entry in README.md script section (concise list only).
3. If the script affects testable behavior, add/update tests.

### When you modify README.md

1. Ensure referenced scripts exist in package.json.
2. Keep file paths and examples current.
3. Keep tech stack versions accurate.

### When you add or change env vars

1. Update `env.example`.
2. Update README environment section if user-facing.

### Checklist before committing

- [ ] package.json scripts have inline section headers
- [ ] README.md script section includes new/changed scripts (one line each)
- [ ] env.example updated if new env vars added
- [ ] README and package.json are consistent
