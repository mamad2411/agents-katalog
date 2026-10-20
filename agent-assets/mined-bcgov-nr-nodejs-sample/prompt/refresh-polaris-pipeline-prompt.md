---
name: refresh-polaris-pipeline
description: "Run the Polaris Pipeline refresh workflow in the current repository."
argument-hint: "Optional notes about repository scope or service runtime"
agent: "agent"
---

Refresh the Polaris Pipeline files in this repository.

Use the repo-local guidance files created by this generator:

- [AGENTS.md](../../AGENTS.md)
- [.github/instructions/polaris-composer.instructions.md](../instructions/polaris-composer.instructions.md)
- [.github/skills/polaris-pipeline-composer/SKILL.md](../skills/polaris-pipeline-composer/SKILL.md)

Follow the repository guidance to:

1. Run the required preflight checks.
   GitHub auth preflight passes when either command succeeds:
   - `gh auth status`
   - `gh api user --jq .login`
   Stop if both GitHub auth checks fail.
   Report preflight results in chat as a checklist that marks each check as pass or fail.
   Use `✅` for pass items and `❌` for failed items.
   Include one short reason for each failed check.
   Pull latest changes with `git pull --ff-only` before running generators.
   Stop immediately if pull fails or merge conflicts are present (`git diff --name-only --diff-filter=U` is not empty).
2. Determine whether this repository is a Node.js or Maven service.
3. Run the matching build generator with `--headless --force`.
4. If headless mode reports missing prompt values, inspect `catalog-info.yaml` and nearby repository context, add only values you can justify confidently, and summarize any added values in chat.
5. If any missing value cannot be deduced confidently, ask the user for that value before continuing.
6. Run `gh-oci-deploy-onprem` with `--headless --force`.
7. Review the diff and keep changes limited to expected generated Polaris Pipeline artifacts.
8. Create a branch, commit, push, and open a pull request if changes exist.
9. Stop cleanly if preflight fails, required data is missing, or unrelated churn appears.

End in one of the allowed states: pull request opened, no changes needed, or a deliberate stop with a human-readable summary in chat. For deliberate stops, include the preflight pass/fail checklist in the summary.