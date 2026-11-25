---
name: readme-updater
description: |
  Update README.md based on actual project structure and code changes.
  Triggers on "update readme", "refresh readme", "sync readme", "readme outdated".
metadata:
  type: workflow
  version: "1.0.0"
  author: community
  tags: [readme, documentation, project-maintenance]
triggers:
  - "update readme"
  - "refresh readme"
  - "sync readme"
  - "readme is outdated"
  - "fix readme"
allowed-tools:
  - Read
  - Write
  - Bash
---

# README Updater

Keep README.md in sync with the actual project state.

## When to Use
- README has outdated setup instructions
- Project structure changed but README wasn't updated
- Adding new features that should be documented in README
- User mentions "update readme", "readme is outdated"

## When NOT to Use
- Writing a README from scratch (use `/init` for context first)
- Minor typo fixes (just fix directly)

## Workflow
1. Scan the project: `package.json`, directory structure, config files
2. Compare against current README sections:
   - **Setup instructions**: Are deps, env vars, build steps still correct?
   - **Project structure**: Does the directory tree match reality?
   - **Features**: Are new features listed?
   - **Scripts**: Are `npm run` scripts documented and current?
   - **Tech stack**: Dependencies match `package.json`?
   - **Contributing**: Link to CONTRIBUTING.md still works?
3. List discrepancies found
4. Propose updates section by section
5. Apply approved changes
6. Run `npm run build` or equivalent to verify project still works

## What to Check
```
✓ Setup steps actually work (run them to verify)
✓ Environment variables match .env.example
✓ Script commands in README match package.json scripts
✓ Directory tree matches actual folder structure
✓ Tech stack badges/versions match package.json
✓ API examples match actual routes
✓ License matches LICENSE file
✓ Contributing link is not broken
✓ All links in README are not 404
```

## Key Principles
- README should be accurate, not aspirational — document what IS, not what WILL BE
- Setup instructions must be copy-paste runnable
- Don't remove content without confirming with user
- Keep it concise — README is the entry point, not the full docs

## Notes
- Don't add emoji or decorative elements unless they already exist
- Follow the existing README style and tone
- If README is extremely long, suggest moving sections to a docs site
- Always show a diff of proposed changes before applying
