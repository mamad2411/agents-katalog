---
name: deploy-checklist
description: Run a pre-deploy checklist (tests, build, env). Use when the user asks to deploy, prepare for release, or run a deploy checklist.
---

# Deploy Checklist

When the user wants to deploy or run a pre-deploy check, follow this workflow.

## Steps

1. **Run tests**
   - Execute the project test command (e.g. `npm test` or `pytest`).
   - If tests fail, report failures and do not proceed until they pass (unless the user says otherwise).

2. **Build**
   - Run the build command (e.g. `npm run build`).
   - Note any build errors or warnings.

3. **Environment**
   - Remind the user to confirm env vars and secrets are set for the target environment.
   - Do not print secrets; only remind to verify they exist.

4. **Report**
   - Summarize: tests (pass/fail), build (success/fail), and a short reminder about env/secrets.

## Notes

- If the project has no test or build script, say so and skip that step.
- This is an example skill for learning; adapt commands to the actual project.
