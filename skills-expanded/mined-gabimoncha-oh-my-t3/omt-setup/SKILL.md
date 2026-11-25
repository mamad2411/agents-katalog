---
name: omt-setup
description: Set up, configure, update, or explain omt in T3 Code. Use when the user asks to set up, configure, or update omt, change models, roles, or profiles, pick the harnesses (Claude Code, Codex), or review new defaults, or asks for help, what omt can do, what to do next, which skill to use, or what a command means. Asks before each write.
---

# Setup and help

You answer questions about omt and configure it through the omt CLI. Show the text output of each command.

## Write rules

1. Show the command, or the planned edit, before you run it.
2. When the command has `--dry-run`, run that first and show the output.
3. Ask. Pass `--yes`, or make the edit, only after the user agrees.
4. After the write, run the check of the step.

## Steps

Run step 1 first. For a question, run step 3. For a change, run step 2, then the steps that it names. For a plain "set up omt", run steps 2, 4, 5, and 6, then check for Anthropic's optional `frontend-design` skill and recommend it for UI work when it is missing. End with step 9 when you proposed a write.

### 1. Find the CLI and your mode

Follow [The CLI](../omt/references/delegation.md#the-cli). Call `t3_thread_configure` with no arguments and read `interactionMode`. In `plan` mode, run only read commands, list the writes for the user, and ask the user to switch to default mode.

Done when: `omt --version` prints a version, and you know your mode.

### 2. Read the doctor

Run `omt doctor --project --dry-run`, or `omt doctor --dry-run` for a global install. Map each line that is not `PASS`: `harnesses` to step 4, `defaults` to step 5, `worktree` to step 6, `config` to step 7, and `skills` with `outdated`, `hooks`, or `update` with `is out` to step 8. For another line, give the user its printed fix.

Done when: each line that is not `PASS` has a step or a fix, and the user knows your proposed steps.

### 3. Answer a question

This step writes nothing. Sort the question, and run its commands first:

- Which skill to use, or what omt can do: the workflow list of the [router](../omt/SKILL.md).
- What a command means: `omt help <command>`.
- A config question: `omt config show`, `omt config explain`, `omt profile list`, `omt profile show <name>`, `omt roles`, or `omt detect`.
- What to do next: the doctor command of step 2, and `omt update --check` for a new version.

Answer first, in one to three sentences. For a skill, give its composer form, such as `$omt-ulw <task>`. For a change, name the key and the file, and offer the write steps. Link one doc as `https://github.com/gabimoncha/oh-my-t3/blob/main/docs/<file>.md`: `install`, `configuration`, `commands`, `workflows`, `walkthrough`, or `design`.

Done when: every fact in the answer comes from a command that you ran in this turn, the router, or the linked doc.

### 4. Fit the roles to the harnesses

Pass `--project`, or `--user` for a global install, to each command of this step. With the T3 tools, save the full JSON result of `orchestrator_capabilities` to a temp file, and also pass `--capabilities <file>`.

1. Run `omt detect`, and read the driver and effect lines.
2. When it recommends a change, run `omt detect --write --dry-run`, and ask.
3. After the user agrees, run `omt detect --write --yes`.
4. The check: `omt detect`, then `omt roles`.

Without the T3 tools, say that detection sees only the T3 settings file and `PATH`. When `omt detect` finds no driver, ask the user to sign in to Claude Code or Codex and enable it in T3 Settings, then run this step again.

Done when: the check recommends no further change, and `omt roles` shows each role as the effect lines said.

### 5. Review current defaults

Run the doctor command of step 2, and explain each `<path>: <from> -> <to>` line. A line marked `(overridden by <file>)` has no effect. On the first review of an older install, show the current role choices, since no baseline exists. After the user accepts, run the same command with `--yes` in place of `--dry-run`. Declining keeps the last accepted defaults.

Done when: the user accepted or declined, and `omt config validate` exits 0 after acceptance.

### 6. Set up worktrees

Follow [worktrees.md](../omt/references/worktrees.md) on the first run in a project, or for a `worktree` line that is not `PASS`.

Done when: you finished each step of worktrees.md that applies.

### 7. Change a profile or a role

1. Run `omt config path`. Pick the project file for one project, or the user file for all. When it is absent, propose `omt init` or `omt config init`.
2. Read the file and `omt config show --defaults`. Write the JSONC edit with its key path by the [configuration guide](https://github.com/gabimoncha/oh-my-t3/blob/main/docs/configuration.md). A new role needs `description`, `access`, and `chain`. A `chain` replaces the old chain, and `null` removes a role.
3. Show the edit and ask. After yes, make it, and keep every other byte of the file.
4. The check: `omt config validate`, then `omt profile show <name>`.

Done when: `omt config validate` exits 0, and `omt profile show <name>` shows the new values.

### 8. Update omt

1. Run `omt update --dry-run`, and show its update command, pin, hint, or package switch.
2. When you ask, say that `--yes` also accepts the current defaults. When the user wants to see a defaults diff that the dry run cannot show, run `omt update` interactively instead.
3. After the user agrees, run `omt update --yes`. Tell the user each `kept <skill>` line: that skill keeps the user's edits. When the npm registry is out of reach, follow [Update omt](https://github.com/gabimoncha/oh-my-t3/blob/main/docs/agents/quickstart.md#update-omt).
4. The check: the doctor command of step 2. When a skill changed, tell the user to start new threads, because a running session keeps the old skills.

Done when: the doctor prints `PASS` for `skills`, and the user knows to start new threads.

### 9. Report

The report contains each changed file and key, each write command with its check result, each declined step, and each open `WARN` or `FAIL` line.

Done when: each write of this run is in the report with its check result.
