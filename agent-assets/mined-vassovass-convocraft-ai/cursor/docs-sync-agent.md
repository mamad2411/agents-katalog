version: 1

rules:
  - id: docs-sync-agent
    name: Docs Sync Agent
    description: |
      Runs documentation linting when API files change to ensure README/docs stay updated.
    trigger: onFileChange(src/**/*.ts)
    run: node scripts/docsSync.js
    success_message: "✅ Docs in sync."
    failure_message: "❌ Documentation out of sync – please update docs."
 