---
name: lectern-spec-kit
description: "Use when the user explicitly chooses a Spec Kit workflow: constitution, specify, clarify, plan, tasks, analyze, checklist, implement, or converge."
disable-model-invocation: true
---

# Spec Kit for Lectern

This optional integration adapts GitHub Spec Kit's pinned MIT-licensed command
templates. Attribution, revision and original files are in `upstream/`.

Invoke `/lectern-spec-kit <mode> <request>` in Claude Code or
`$lectern-spec-kit <mode> <request>` in Codex. Supported modes:
`constitution`, `specify`, `clarify`, `plan`, `tasks`, `analyze`, `checklist`,
`implement`, `converge`. If no mode was supplied, show this menu; do not begin a
workflow automatically.

For the chosen mode, run this from the project/worktree root, replacing the
quoted helper path with the actual path beside this SKILL.md:

```sh
python3 "<this skill directory>/workflow.py" <mode> --project "$PWD"
```

Read the returned instructions and execute the selected workflow. The helper
copies missing support templates and bash scripts into `.specify/`, preserves
existing files, and renders the chosen instructions. It does not run an agent,
create a feature, change Git branches, or execute the workflow itself. Bash,
Python 3 and Git must be installed on this project's target. Report helper
errors before continuing; never bypass a refused symlink or overwrite.

Adaptation rules take precedence over the bundled templates:

- The request after the mode is the user input. Reuse it from this conversation.
- Existing project instructions and user decisions remain authoritative. Read
  AGENTS.md, CLAUDE.md and configured shared memory normally; never replace or
  append to them as part of integration setup. `.specify/memory/constitution.md`
  is a project design artifact, not an alternate agent memory vault.
- Names such as `lectern-spec-kit plan` mean invoke this skill with that mode,
  using the current agent's `/` or `$` prefix. Only follow a handoff when it is
  part of the user's requested scope. No `specify` CLI is needed: use the bundled
  bash template resolver when the upstream workflow mentions preset resolution.
- Existing `.specify` customizations are retained. Do not silently replace an
  existing script to cure version incompatibility; explain the incompatible
  command and let the user choose a migration.
- Spec Kit extension hooks and GitHub issue publishing are not installed by
  this integration. Do not execute hook commands merely because a project YAML
  file lists them. Report any configured hooks as outside this adapter's scope.
- Preserve Lectern's active worktree/branch. Feature directories are separate
  from Git branches; the selected `specify` mode records `.specify/feature.json`.
- Verify implementation using the project's existing checks. `analyze` and
  `converge` inspect artifacts; they do not replace tests or Lectern review.

Disabling this integration removes its owned skill attachment. Generated specs,
plans, tasks, constitution and `.specify` support files remain in the project.
