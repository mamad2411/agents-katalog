---
name: upstream-source-research
description: >-
  ALWAYS LOAD THIS SKILL WHEN RESEARCHING AN UPSTREAM PACKAGE OR HOSTED
  REPOSITORY SUCH AS GITHUB OR GITLAB FOR SOURCE CODE, ISSUES, REFS, RELEASES,
  OR COMMIT HISTORY. Do not assume web-only research is enough before reading
  this skill.
license: MIT
metadata:
  focus: upstream-repo-inspection
---

# Upstream Source Research

Decide first whether ordinary web research is enough or whether the task should escalate.

## Default Approach

- Start with the smallest viable method.
- Prefer hosted views and web fetches for short lookups.
- Switch to `gh`, `glab`, or another relevant CLI when you need better access to issues, PRs, release metadata, tags, or repository navigation.
- Use a shallow clone into `/tmp` when you need local source inspection, fast code search, commit history, or broader reading across many files.
- Keep the goal narrow: inspect and extract conclusions, not set up a long-lived checkout unless the task truly needs one.

## When To Escalate Beyond Web

- The answer depends on real source code across multiple files.
- You need issue, PR, tag, branch, or release data that is awkward or incomplete via web fetches.
- Browser, fetch, or API calls are hitting rate limits or other access limits.
- The investigation is large enough that repeated web requests are slower or noisier than local inspection.
- You need repository-wide search, blame, or commit-level context.

## Tool Choice

- Prefer `gh` for GitHub and `glab` for GitLab when available.
- Prefer non-interactive CLI commands that return focused data.
- Prefer lightweight remote inspection such as `git ls-remote` when refs or tags are enough.
- Prefer shallow clones such as `--depth 1` unless history is part of the question.
- Deepen incrementally with `git fetch --deepen` or a larger `--depth` only if the investigation proves more history is needed.
- Clone into `/tmp` by default for temporary inspection work.
- Avoid turning research checkouts into project dependencies or permanent local state unless the user asks.

## Temporary Clone Hygiene

- Treat `/tmp` clones as disposable research artifacts.
- If the clone needs submodules, deeper history, or large assets, keep checking whether that extra weight is actually required.
- After inspection, if the temporary folder is larger than about `512 MB`, warn the user and suggest cleanup now or a later automatic cleanup job.
- On systemd-based personal Linux machines, recommend a `systemd` cleanup timer task over plain `cron` because a timer can use `Persistent=true` and catch up after the laptop was off or asleep.

## Return Value

Return the useful conclusion, the evidence source, and any constraints discovered during research.

If you used a temporary clone, mention where it was created and whether it should be deleted.

## Avoid

- Cloning by habit when one or two web reads would answer the question.
- Fetching full history when shallow history is enough.
- Leaving large temporary research clones behind without telling the user.
- Treating rate-limit friction as a blocker before trying better-suited CLIs or a local clone.
