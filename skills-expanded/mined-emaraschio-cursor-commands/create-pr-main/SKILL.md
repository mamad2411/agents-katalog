---
name: create-pr-main
description: Create a pull request targeting main
user-invocable: false
---
## Overview

Create a well-structured pull request for the main branch of a GitHub repository with proper description, labels, and reviewers.

## Steps

1. **Prepare branch**
   - Ensure all changes are committed to the correct branch using the conventional commit message convention
   - Push branch to remote
   - Verify branch is up to date with main or master

2. **Write PR description**
   - Must use the PR template to write the PR description. Refer to ./pull_request_template.md for the PR template.
   - Summarize changes clearly
   - Include context and motivation
   - List any breaking changes
   - Add screenshots if UI changes

3. **Set up PR**
    - Only use the GitHub UI to create the PR. Do not use the CLI.
    - Create PR with descriptive title

## Guardrails

- Push only when the user asks; do not push unrequested changes before opening the PR.
- Do not open empty PRs; confirm the branch has real changes to review first.
- Use the PR template and the Conventional Commits convention for the title.
- Never print, stage, or commit secrets or credential files (.env, .env.*, keys); exclude them and warn instead.