# Target Repository Agent Guide

Use this file when running Polaris Pipeline composer updates in this repository.

## Scope

- Run Polaris Pipeline composer updates for this repository only.
- Keep changes focused on generated Polaris Pipeline artifacts.

## Direct-In-Repository Execution

1. Move to the component root where `catalog-info.yaml` exists.
2. Run the matching build generator:
   - Node.js: `gh-nodejs-build`
   - Java/Maven: `gh-maven-build`
3. Run `gh-oci-deploy-onprem` for Polaris deploy workflow updates (OCI/ORAS under the hood).
4. Review diff and confirm only expected generated Polaris Pipeline files changed.
5. If changes exist, create a branch, commit, push, and open a pull request with `gh`.
6. If there are no changes, exit cleanly.
7. If execution cannot proceed safely, stop and provide a human-readable summary in chat.

## Command Guidance

- Use the `/refresh-polaris-pipeline` chat prompt in this repository when you want a chat-driven run.
- Default mode assumes required prompt values are already present.
- Use `--headless --force` for non-interactive composer runs.
- If headless mode fails on missing prompt values, inspect `catalog-info.yaml` first, add only values you can justify confidently, and summarize those additions in chat.
- Ask the user for any remaining value you cannot deduce confidently.
- Use `--ask-answered` only when you intentionally need to review or change stored prompt values.

## Required Preflight Checks

- `gh` is installed and available.
- At least one GitHub auth check is successful:
   - `gh auth status`
   - `gh api user --jq .login`
- `podman` or `docker` is installed and available.
- Git working tree is clean before generation.
- `catalog-info.yaml` exists for the component being updated.
- Branch is up to date with remote using `git pull --ff-only`.
- No unresolved merge conflicts are present (`git diff --name-only --diff-filter=U` is empty).

When preflight runs, report results in chat as a pass/fail checklist and include a short reason for each failed check.
Use `✅` for pass items and `❌` for failed items.
If pull or conflict checks fail, stop and let a developer resolve branch state before running generators.

## Completion States

Each run must end in one state:

1. Pull request opened with Polaris Pipeline updates.
2. No changes needed.
3. Stopped with a human-readable summary in chat.

## Pull Request Flow

When generated changes exist:

1. Create a branch (example: `feat/polaris-composer-<service>`).
2. Commit only expected generated Polaris Pipeline files.
3. Push the branch to origin.
4. Open a pull request with `gh pr create`.
