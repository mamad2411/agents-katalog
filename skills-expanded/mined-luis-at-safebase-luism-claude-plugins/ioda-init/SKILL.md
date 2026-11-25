---
name: ioda-init
description: Initialize ioda configuration — storage location, ticket CLI command, verification commands, code review agent. Run once per machine.
argument-hint: '[--reset to reconfigure]'
disable-model-invocation: true
---

User's request: $ARGUMENTS

# Initialize ioda

You are setting up ioda configuration for this machine. Run this wizard step by step. **Use the `AskUserQuestion` tool for every multiple-choice question** — do not ask questions in plain text.

## Step 0: Check existing configuration

Run:

```bash
cat "$HOME/.ioda/config.json" 2>/dev/null || echo "NOT_CONFIGURED"
```

**If config exists and `--reset` was NOT passed:** use `AskUserQuestion` to ask whether to reconfigure. If the user keeps current config, exit with "Configuration unchanged."

**If NOT configured (or user chose to reconfigure):** proceed to Step 1.

## Step 1: Storage location

Use `AskUserQuestion` to ask where artifacts should live. Offer:

1. **Default** — `~/.ioda/features/` (tool-owned, easy cleanup)
2. **Custom path** — any absolute path. Common options: an Obsidian vault, Logseq graph, or notes directory.

If the user picks custom, prompt them for the absolute path. Expand `~` to `$HOME`. Strip trailing slashes.

Store as `base_dir`.

## Step 2: Ticket CLI fetch command

Use `AskUserQuestion` to ask how ioda should fetch ticket information. Offer:

1. **Skip** — always paste ticket contents manually
2. **Configure** — provide a shell command template with `{key}` placeholder

If configure, prompt for the template. Examples to show: `jira issue view {key} --plain`, `linear issue {key}`, `gh issue view {key} --repo owner/repo`.

Store as `ticket_cli_fetch`. Empty string if skipped.

## Step 3: Verification commands

These are the shell commands the implementor runs at the end of Act as the final quality gate. They need to cover the **full CI surface** for the kinds of changes ioda will drive — a too-narrow list means the implementor ships a feature the implementor thinks is green but CI rejects. See `${CLAUDE_PLUGIN_ROOT}/references/verification-commands.md` for the full authoring guide; the Step runs a monorepo check so first-time configuration lands on a coverage-aware shape, not a workspace-scoped gap.

### Step 3a: Monorepo check

Use `AskUserQuestion` to ask whether the repos ioda will run in are monorepos (multiple workspaces under `apps/`, `packages/`, `services/`, or a `workspaces` field in `package.json`). Offer:

1. **Monorepo** — repo-wide commands required (e.g. `yarn run g:type-check`, `pnpm -r type-check`, `turbo run typecheck`, `nx affected --target=typecheck`)
2. **Single workspace** — workspace-scoped commands are fine (`npm run type-check`, `yarn run type-check`)
3. **Mixed / not sure** — treat as monorepo for the global default; per-project overrides can narrow later

### Step 3b: Gather the commands

Ask the user for the verification commands as a newline-separated list. Tailor the examples shown to the Step 3a answer:

- **Monorepo:** suggest `yarn run fix`, `yarn run g:type-check`, and test commands that cover the CI surface. Emphasize: *use the repo-wide type-check, not workspace-scoped — workspace-scoped misses sibling-workspace consumers of types you change. See `references/verification-commands.md` for why.*
- **Single workspace:** suggest `yarn run fix`, `yarn run type-check`, `yarn test`.
- **Mixed:** default to the monorepo suggestions.

Point out that per-project overrides in `<repo>/.ioda/config.json` can narrow (or widen) the global default for specific repos — the global is the starting default, not a lock.

Accept as a newline-separated list. Convert to a JSON array. If the user has none, use an empty array.

Store as `verification_commands` (JSON array).

## Step 4: Code review agent

Use `AskUserQuestion` to ask which Claude Code agent to spawn for the final code review pass. Offer:

1. **general-purpose** (default, always available)
2. **code-reviewer** (if available in the user's setup)
3. **Custom** — prompt for an agent name

Store as `code_review_agent`.

## Step 5: Confirm

Use `AskUserQuestion` to show a summary and ask for confirmation:

> Ready to configure ioda:
>
>   Base directory:         `<base_dir>/<repo-name>/<feature>/`
>   Config file:            `~/.ioda/config.json`
>   Ticket CLI fetch:       `<ticket_cli_fetch>` (or "none")
>   Verification commands:  `<verification_commands>`
>   Code review agent:      `<code_review_agent>`
>
> Proceed?

Options: `Yes, apply` / `No, cancel`.

If cancelled, exit with "Configuration cancelled. Nothing was changed."

## Step 6: Apply

Call the setup script:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup-ioda.sh" "<base_dir>" "<ticket_cli_fetch>" '<verification_commands_json>' "<code_review_agent>"
```

## Step 7: Done

Once the script succeeds, say:

```
ioda initialized.

  Artifacts: <base_dir>/<repo-name>/<feature>/
  Config:    ~/.ioda/config.json

Run /ioda to start your first feature.
```

## Notes

- `base_dir` is stored without the repo-name segment. `resolve-basedir.sh` appends the current repo name at runtime.
- Per-project overrides can be created at `<repo>/.ioda/config.json` with the same schema.
