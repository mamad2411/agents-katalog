---
name: init
description: Install or upgrade the Aevum harness core (agents, hooks, rules, scripts, settings deny list) into the current project.
disable-model-invocation: true
argument-hint: "[--force]"
---

Install the Aevum harness into this project, or upgrade an earlier install.

The installer is deterministic; your job is to run it, explain the result,
and get the user's decision on conflicts. Do not copy or merge files by hand.

1. Dry run from the project root:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aevum-install.py" "$(git rev-parse --show-toplevel)"
   ```

2. Summarise the report: files to create, settings.json and .gitignore
   merges, files left alone because they differ, obsolete files.

3. If files differ, show the user `diff -u <project file> "${CLAUDE_PLUGIN_ROOT}/<same path>"`
   for each one and ask which to take. Projects customise rules and the
   Gate-1 runner on purpose (see docs/swap-points.md), so keeping theirs is
   a normal answer. Pass `--force` only when the user wants every
   differing file replaced; otherwise copy the individual files they chose.

4. Apply:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aevum-install.py" "$(git rev-parse --show-toplevel)" --apply
   ```

5. Smoke test: set `base_sha` in `docs/blocks/EXAMPLE/block.yaml` to
   `git rev-parse --short HEAD` (skip this step in a repository with no
   commits yet), then run the preflight. The expected result is exactly one blocker,
   `status is 'draft'`: that means the harness is wired correctly.

   ```bash
   python3 scripts/block-preflight.py EXAMPLE
   ```

   Next steps for the user: swap the Gate-1 runner for their stack
   (`.claude/scripts/gate1.sh`, Seam 1 in the Aevum docs), author
   specialist agents from `${CLAUDE_PLUGIN_ROOT}/examples/agents/AGENT_TEMPLATE.md`,
   then `/aevum:new-block`. Hook and permission changes apply to new
   sessions, so suggest restarting Claude Code.

Do not stage or commit the installed files; the user reviews and commits them.
