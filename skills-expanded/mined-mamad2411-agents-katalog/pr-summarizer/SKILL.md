---
name: pr-summarizer
description: Use when the user provides a pull request number to summarize. Fetches the PR diff and commit history from the local agentic-starter-kits clone, analyzes the changes, and writes a structured PR description with summary, changed files, risk assessment, and test plan.
---

# PR Summarizer

Fetch a pull request from the local `agentic-starter-kits` repository clone and
write a structured PR description that a reviewer or author could use directly.

## Setup assumption

The repository is already cloned at:

```text
/opt/app-root/workspace/repos/agentic-starter-kits
```

Do not clone it. If it is missing, report the error and stop.

## Instructions

You will be given a pull request number. Follow these steps in order:

1. **Fetch the PR ref** — run:

   ```bash
   git -C /opt/app-root/workspace/repos/agentic-starter-kits fetch origin refs/pull/<PR_NUMBER>/head:pr/<PR_NUMBER>
   ```

2. **Get the commit list** — run:

   ```bash
   git -C /opt/app-root/workspace/repos/agentic-starter-kits log main..pr/<PR_NUMBER> --oneline
   ```

3. **Get the full diff** — run:

   ```bash
   git -C /opt/app-root/workspace/repos/agentic-starter-kits diff main...pr/<PR_NUMBER>
   ```

   If the diff is very large (more than 500 lines), summarize by file rather than
   reading every line.

4. **Get the changed file list with stats** — run:

   ```bash
   git -C /opt/app-root/workspace/repos/agentic-starter-kits diff --stat main...pr/<PR_NUMBER>
   ```

5. **Analyze the changes** across these dimensions:
   - **Purpose** — what problem does this PR solve or what feature does it add?
   - **Approach** — how was it implemented? Key design decisions.
   - **Scope** — which components, layers, or systems are affected?
   - **Risk** — what could break? Are there missing tests, config changes, or
     dependency bumps that warrant extra scrutiny?
   - **Test coverage** — are new code paths tested? Are there gaps?

6. **Write the PR description** to:

   ```text
   /opt/app-root/workspace/pr-summaries/pr-<PR_NUMBER>-summary.md
   ```

   Create the directory if it does not exist.

7. **Verify the write (required)** — you MUST read back the first few lines of
   the written file before reporting completion. Do not skip this step even if
   the write appeared to succeed. Report the full output path only after
   confirming the file exists and the content looks correct.

## Output format

```text
# PR #<NUMBER>: <inferred title from commits>

## Summary
<2-4 bullet points describing what changed and why>

## Changed files
<bullet list of the most significant files with one-line description of each change>

## Risk assessment
**Level:** Low | Medium | High

<2-3 sentences on what could break and what a reviewer should focus on>

## Test plan
- [ ] <concrete verification step>
- [ ] <concrete verification step>
- [ ] <concrete verification step>

## Notes
<any implementation quirks, follow-up work, or context a reviewer needs>
```

If the PR is purely documentation or dependency bumps with no logic changes,
note that in the Risk assessment and keep the Test plan minimal.

## Input

A pull request number from the `agentic-starter-kits` repository, provided with
the skill invocation.

## Output

A markdown file at `/opt/app-root/workspace/pr-summaries/pr-<PR_NUMBER>-summary.md`.
