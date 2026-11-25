---
license: CC-BY-4.0
description: >-
  Report a defect in an installed skill to the skill's upstream GitHub
  repository. Use when a skill gives wrong instructions, errors, or fails
  silently, or when the user says "this skill is broken", "file a bug for this
  skill", or "report this to the skill author". Searches for duplicates, drafts
  one issue per problem, and files it when the user asks.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Report Skill Issue

Report a failing installed skill to its upstream repository using an available
GitHub integration or the authenticated `gh` CLI.

## Identify the installed skill

1. Identify the failing skill from the conversation, including its plugin and
   leaf name when available (for example `gh:send-pr`). If it is ambiguous, ask
   which skill the user means.
2. Read that skill's installed `SKILL.md`. Use the path the skill was loaded
   from (Claude Code shows each skill's base directory when it loads) or the
   host's skill listing. Plugin skills live in the installed plugin's
   `skills/<leaf>/` directory, independent of the working directory. Do not
   assume `skills/<name>/SKILL.md` exists in the project, and never use this
   reporting skill's own metadata as the failing skill's repository.
3. Only after discovery fails, ask for the installed skill path or the upstream
   repository URL.
4. Read `metadata.repo` from the failing skill's frontmatter. If it is absent,
   ask for the upstream repository rather than guessing. Keep the qualified
   skill name and the installed version or commit for the report's environment
   section.

## Review and publish

Read and follow [references/reporting.rst](references/reporting.rst), the required
shared procedure for duplicate search, diagnosis, authorization, publication,
and failure handling. Use a GitHub integration's issue tools when one is
available, or `gh` with a body file. If neither works, return the report for
manual filing and state that it was not filed.
