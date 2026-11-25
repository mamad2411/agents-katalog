---
name: readme-update
description: Updates README.md to reflect the current state of the project
user-invocable: true
allowed-tools: Read Bash Edit Glob
effort: medium
---

## Update README

1. Read the current README.md and understand what it covers.

2. Inspect the actual project state:
```bash
cat package.json
ls src/ 2>/dev/null || ls lib/ 2>/dev/null
git log --oneline -10
```

3. Identify gaps and outdated information:
   - Installation instructions still accurate?
   - All CLI commands/flags documented?
   - Environment variables listed?
   - Examples actually work with current API?
   - Badges pointing to correct URLs?

4. Write the updated sections. Keep existing structure unless it's fundamentally broken.

5. Ensure README includes at minimum:
   - What it does (1-2 sentences)
   - Prerequisites
   - Installation
   - Quick start / example
   - Configuration
   - Contributing

6. Show diff and ask for confirmation before applying.
