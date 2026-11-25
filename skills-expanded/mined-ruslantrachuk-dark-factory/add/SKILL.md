---
name: add
description: Add a dark-factory module to the current project — base (the full harness; level 1), on-call (the Telegram feedback desk), monitor (the production monitor), release (production only from a tag), observability, code-audit, feature-pipeline, factory (the skeleton of your own factory repository), agent-codex (Codex CLI working in the project under the same fences). Lists the steps only the owner can do first, then copies the module's files from the plugin, fills in what the project shows, runs the module's tests, registers the units on a provisioned server and finishes with a status check. Invoked by the human as /dark-factory:add <module>.
argument-hint: "base | on-call | monitor | release | observability | code-audit | feature-pipeline | factory | agent-codex"
disable-model-invocation: true
---

# /dark-factory:add — install a module into this project

One command per module, from any project directory: the files come from the installed plugin
(`${CLAUDE_PLUGIN_ROOT}/templates/`), nothing is cloned. The mechanics are two scripts —
`${CLAUDE_PLUGIN_ROOT}/scripts/deploy-base.sh` (base) and `${CLAUDE_PLUGIN_ROOT}/scripts/add-module.sh` (every other
module); this skill and the module's manifest are the questions, the filling in and the checks.

**Plugin root for every command in `base.md` and the manifests (`<plugin root>` there): `${CLAUDE_PLUGIN_ROOT}` — use this
absolute path.** Those files are opened with Read, where the variable is not substituted; only this file is.

| Argument | Module (directory in `templates/`) | What the project gets | Needs |
|---|---|---|---|
| `base` | `base` | the full harness (level 1): OpenSpec changes, the `bd` queue, the test pyramid, CI tiers, the skills, the merge script; releases by tag too when the project has production | the plugin (this command runs from it) |
| `on-call` | `feedback-desk` | the On-call agent for the client's Telegram group | base; a server for it to live on |
| `monitor` | `prod-monitor` | a production watchdog plus a read-only monitor agent that reports through On-call | base, on-call |
| `release` | `release-tag` | production is built only from a `vYYYY.MM.DD.N` tag | base; a production deploy (`add base` offers it when there is one) |
| `observability` | `observability` | business metrics contract, dashboard as code, alert catalog | base; a production |
| `code-audit` | `code-audit` | fan-out audit of many repositories | base |
| `feature-pipeline` | `feature-pipeline` | the project settings for `/dark-factory:feature` | base |
| `factory` | `factory` | the skeleton of your own factory repository: registry, machines, plugin pin, notes ([docs/your-factory.md](https://github.com/ruslantrachuk/dark-factory/blob/main/docs/your-factory.md)) | an empty repository (not a project) |
| `agent-codex` | `agent-codex` | Codex CLI in the project: its session hook calls the shared session header, a permission profile closes the secrets, the plugin's hooks approved | base; Codex CLI and the plugin installed in it on the machine |

## Rules

1. **The owner's steps first, in one list.** Before touching a file, read the module's manifest section
   "Setup by /dark-factory:add <module>" and give the owner the whole list of steps only a human can do (a bot token, a
   database role, a hosting login …), so they can do them while you work. Say exactly where each secret goes. **You
   never see, print or move a secret**: the owner writes it into its file themselves.
2. **Dry run first, then write.** `"${CLAUDE_PLUGIN_ROOT}/scripts/add-module.sh" <module> --dry-run` (for `base`, `"${CLAUDE_PLUGIN_ROOT}/scripts/deploy-base.sh" <target> --dry-run`)
   → show the plan, every SKIP included → after "yes", the real run. Existing files are never overwritten.
3. **Fill in what the project shows, ask for what it does not.** Name, paths, main branch, stack, test command,
   project language come from the repository (`git remote`, `pyproject.toml`/`package.json`, `AGENTS.md` or `CLAUDE.md`, the layout).
   Draft project knowledge from code and history for the owner to edit, and say it is a draft. Ask one question at a
   time, with the default you derived.
4. **Adapt the seams to the project, do not leave them for later.** Every module names its seams (`> **Seam:**` lines
   in its manifest and skills: the tool each function is wired to). Compare each with what the project uses (layout,
   test stack, tracker, code host); where they differ, show the owner what you would rewrite and roughly how much, and
   on "yes" rewrite those files in place. Record each adapted canon file as the project's deviation (registry row or
   PR description). A seam the project cannot meet without a rewrite larger than the module is said plainly, before
   anything is copied.
5. **Nothing external without a "yes"**: creating a repository or a bot, a ruleset, a cron entry, a systemd unit, a
   message to a group. Fence files (`.claude/settings*.json`, `.claude/fences.env`, `.githooks/`,
   `scripts/merge-feature.sh`) change only through the permission dialog.
6. **Run the module's tests** (the manifest names them) before reporting; a red test is reported, not worked around.
7. **On a server the fleet provisions, register the units**: when `systemctl --user` works and the server is
   provisioned (`~/.config/systemd/user/df-fleet-watch.timer` exists) or the owner says this machine runs the factory,
   check the project is listed in `~/.config/dark-factory/projects` (add its path after a "yes"), then
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fleet.py" provision --dry-run` → show → "yes" → `provision`. It is
   idempotent. On a machine that is not provisioned say so and point at `/dark-factory:provision-server`.
8. **Finish with a status check** the manifest names (and, for On-call, a test message to the group), then report: what
   was installed, what the owner still has to do, what is unfilled. The change goes out like any other (files under `.claude/factory/` are the server's and stay out of git): a branch, a PR
   whose description has `## Done`, `## Decisions`, `## Open questions`, merged with `scripts/merge-feature.sh`. If the
   project is listed in a factory registry, add the module to its row.

## Steps

1. **No argument**: show the table, run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/level.py" status` for the signals and
   what is already installed, and ask which module. Never install a module on your own initiative: propose it with
   its "time to install" signal (`.harness/modules.md` in a base project) and wait.
2. **`base`**: follow `${CLAUDE_PLUGIN_ROOT}/skills/add/base.md`. It asks the level to start at, whether the project
   has a production deploy (then the `release` module comes with it) and the configuration questions.
3. **Any other module**: check the precondition from the table (a base project has `openspec/` and
   `CODING_STANDARDS.md`; `monitor` needs On-call's `scripts/feedback-desk.sh`; `factory` goes into an empty repository, not a project). If it is missing, offer the missing
   module first. Then follow `${CLAUDE_PLUGIN_ROOT}/templates/<directory>/MANIFEST.md`, section "Setup by
   /dark-factory:add <module>", step by step. The file copy is
   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/add-module.sh" <module> --dry-run     # then without --dry-run after the "yes"
   ```
4. The module's own operating skill (`feedback-desk`, `prod-monitor`) lands in the project's `.agents/skills/` with
   the files (Codex reads it there, Claude Code through the `.claude/skills` link; a project still on the v23 layout,
   with a real `.claude/skills/` directory, gets it there until `/dark-factory:upgrade`): it is what the development session reads at run time. Its setup section points back here.

## Not this command

Levels and the fence level are `/dark-factory:level`; the solo kit is `/dark-factory:init`; the server is
`/dark-factory:provision-server`. A module is removed by the manifest's "Abandon criterion", by hand.
