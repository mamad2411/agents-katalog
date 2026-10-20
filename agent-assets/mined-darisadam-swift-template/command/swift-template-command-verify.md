---
description: Run the project's mandatory verification (lint + tests). Must pass before declaring a task complete.
---

Run the project's verification suite in order. Stop at the first failure and report it.

1. Auto-fix anything SwiftLint can fix on its own:
   ```bash
   swiftlint lint --fix --config .swiftlint.yml
   ```
2. Re-lint and confirm zero violations:
   ```bash
   swiftlint lint --config .swiftlint.yml
   ```
3. Run the project's unit tests (the command lives in `CLAUDE.md`; if you can't find it, ask the user). Never run UI tests from the CLI.

Report:
- Lint result (clean / N warnings / N errors)
- Test result (passed / failed counts, names of any failing tests)
- Any files that still have violations after `--fix`
