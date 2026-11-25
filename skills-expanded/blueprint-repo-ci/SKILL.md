---
name: blueprint-repo-ci
description: "Find out whether GitHub Actions already runs the recorded gates on every pull request, and record what is missing. Change nothing: adding CI is the first change the person approves."
---

# Does CI run what we run?

Every later change is merged on the strength of CI, so CI has to run the gates recorded in
`.blueprint/gates.json`, on pull requests, from a clean install. This step only **looks**: anything it
finds missing becomes the first target of the plan, and is changed only after the person approves it.

1. Read every workflow under `.github/workflows/`.
2. For each recorded gate, find the workflow step that runs it on `pull_request`.
3. Note every workflow without a top-level `permissions:` block, and every `actions/checkout` without
   `persist-credentials: false`.
4. Look at CI on the default branch's current commit: `gh run list --commit $(git rev-parse HEAD)`.
5. Write `.blueprint/ci.json`:
   ```json
   {
     "gaps": ["the typecheck gate is not run on pull requests", "ci.yml has no permissions: block"],
     "defaultBranchGreen": true
   }
   ```
   An empty `gaps` means CI already covers everything.

Change nothing in the repository in this step. If the default branch is red in CI for a reason you cannot
see locally, ask.

Done when the check passes: `.blueprint/ci.json` records the gaps (possibly none) and the state of CI on
the default branch.

## Always

- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
