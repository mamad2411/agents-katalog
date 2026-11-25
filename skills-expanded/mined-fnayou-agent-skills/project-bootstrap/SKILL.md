---
name: project-bootstrap
description: Create, adopt, or audit an AI-ready GitHub project foundation. Use when setting up repository instructions, governance files, Taskfile commands, or optional Docker Compose conventions; exclude application feature development.
---

# Project Bootstrap

Create, adopt, or audit an existing project in its current directory. Keep
application code and stack-specific CI out of scope unless the user requests
them and confirms the stack.

1. Read [execution contract](references/execution-contract.md) before acting.
2. Inspect local files, Git boundaries and state, tools, remotes, and installed
   Matt Pocock setup skills. Redact credentials from any displayed remote.
3. Confirm mode and profile. For Create, confirm display name, slug, owner,
   description, private-by-default visibility, license choice, and release
   convention when relevant. Always ask whether Docker is wanted; if yes, ask
   application image, development dependencies, or both.
4. Present planned files, existing-file conflicts, warnings, and validation
   limits. Get approval before substantive writes. Never replace existing
   content without reviewing and approving its diff.
5. For Create and Adopt, validate existing Matt setup outputs first. Reuse
   complete, consistent setup. If incomplete and
   `setup-matt-pocock-skills` is installed, ask the user to invoke it; it
   disables model invocation. If it is absent, report the blocker.
6. Generate only approved, supported files. Run `python3 scripts/inspect.py`
   for read-only inventory and `python3 scripts/scaffold.py --plan --diff`
   for a reviewable preview. Use `--apply --approved` only after approval.
   Review supplied Docker and license source files separately; plan output
   omits their contents. Run `python3 scripts/validate.py` for checks. Scripts
   do not publish, commit, push, install tools, or overwrite existing files.
7. For Audit, run `python3 scripts/inspect.py` and
   `python3 scripts/validate.py --audit` only.
   Audit validation does not execute project-defined tasks or Docker commands.
   Never scaffold, install, or mutate GitHub.
8. Report changed files, blockers, and each validation as pass, fail, not
   applicable, or not verified. Propose repository creation and commit/push
   separately; require explicit approval for every remote or Git mutation.
   Require `gh_auth: authenticated` before any GitHub mutation. Missing or
   unauthenticated `gh` means stop remote work and give a safe remediation.
   Perform each mutation separately; stop after any failure. Verify the exact
   staged file set and resulting commit before the separately approved push.

Read [profiles and questions](references/profiles.md) when choosing files,
[GitHub standards](references/github-standards.md) for community files,
[Taskfile and Docker](references/taskfile-docker.md) for generated commands,
and [Matt workflow](references/matt-workflow.md) before declaring setup done.
Read [validation evidence](references/acceptance-tests.md) when checking
coverage or reporting unsupported branches.
