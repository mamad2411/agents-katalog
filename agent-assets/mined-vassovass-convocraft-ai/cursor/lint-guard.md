version: 1

rules:
  - id: lint-guard
    name: LintGuard
    description: |
      Runs the project linter ("npm run lint --fix") on every save and commit.
      Blocks the commit if lint errors remain after auto-fix.
    trigger: onSave|onCommit
    run: node scripts/lintGuard.js
    success_message: "✅ Lint clean."
    failure_message: "❌ Lint errors – fix before committing."
 