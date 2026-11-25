---
name: "heal-ci"
description: "Claude Code self-healing ci pipeline: workflow guidelines, best practices, instructions, and integration examples"
---

# Self-Healing CI Pipeline

## When to activate
Activate when a pull request fails a CI check (GitHub Actions, GitLab CI). Invoked via `/heal-ci`.

## When NOT to use
Do not use to rewrite core business logic. Only use to fix linting errors, minor type mismatches, or fragile tests that broke during CI.

## Instructions
1. **Fetch CI Logs:** Ask the user to paste the failing CI logs, or use the GitHub MCP server to fetch the logs from the failed run.
2. **Analyze Failure:** Identify exactly which linter, type-checker, or test failed and on what line.
3. **Patch:** Navigate to the local file. Write the exact fix required to satisfy the CI pipeline (e.g., adding an `eslint-disable` comment, fixing a TypeScript interface, or updating a snapshot).
4. **Test Locally:** Run the failing check locally using `Bash` to confirm the fix works.
5. **Push:** Ask the user: "I have fixed the CI failure locally. Shall I commit and push this patch to update the PR?"

## Example
User: `/heal-ci The build failed on GitHub.`
Claude: [Analyzes logs]. The build failed because Prettier enforced double quotes on line 42 of `auth.ts`, but you used single quotes. I have fixed the formatting. Shall I push the patch?