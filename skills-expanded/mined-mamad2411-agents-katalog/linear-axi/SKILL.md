---
name: linear-axi
description: "Operate Linear through the linear-axi CLI - issues, projects, cycles, teams, workflow states, labels, users, documents, search, authentication checks, and raw GraphQL access. Use whenever a task touches Linear: listing, filing, or updating issues, commenting, moving issues through workflow states, starting work on an issue (git branch), checking cycles or project progress, or searching the workspace."
---

# linear-axi

Agent ergonomic CLI for the Linear API. Prefer this over MCP and raw GraphQL for Linear operations.

You do not need linear-axi installed globally - invoke it with `npx -y @affable-co/linear-axi <command>`.
If linear-axi output shows a follow-up command starting with `linear-axi`, run it as `npx -y @affable-co/linear-axi ...` instead.

linear-axi requires a Linear API key in the `LINEAR_API_KEY` environment variable (create one at https://linear.app/settings/account/security). Keys stored by schpet/linear-cli in `~/.config/linear/credentials.toml` are detected automatically. Run `npx -y @affable-co/linear-axi auth status` to verify authentication; do not guess or invent other login commands. If it fails with `AUTH_REQUIRED`, ask the user to set `LINEAR_API_KEY` themselves.

## Workflow

1. Run `npx -y @affable-co/linear-axi auth status` when authentication is unknown or needs verification.
2. Run `npx -y @affable-co/linear-axi` with no arguments for a dashboard - your active issues and suggested next commands.
3. Drill in command-first: `issue list`, `issue view ABC-123`, `project view <name>`, `cycle view current --team <key>`, and so on.
4. Issues accept identifiers everywhere (`ABC-123`, case-insensitive); teams accept keys or names; states, labels, projects, and cycles accept names; assignees accept `me`, an email, or a display name.
5. Scope to a team by placing `--team <key>` AFTER the command. Without it, the team comes from `LINEAR_TEAM`, a `.linear.toml` `team_id`, or the current git branch's issue identifier.
6. Move work along with `issue start ABC-123` (assigns you, moves to started, creates the git branch), then `issue close ABC-123` when it ships.
7. Filter lists tightly (`--state`, `--assignee me`, `--label`, `--updated-since 2w`) - narrow queries cost fewer tokens than wide ones.
8. Every response ends with contextual next-step hints under `help:` - follow them.

## Commands

```
commands[14]:
  (none)=dashboard, issue, project, cycle, team, state, label, user, doc, search, api, auth, setup
```

Installed copies also inherit the SDK built-in `update` command.
Run `linear-axi update --check` to compare the installed version with npm, or `linear-axi update` to upgrade.
When using `npx -y @affable-co/linear-axi`, npx already resolves the package on demand.

Run `npx -y @affable-co/linear-axi --help` for global flags, or `npx -y @affable-co/linear-axi <command> --help` for per-command usage.

## Tips

- Output is TOON-encoded and token-efficient; pipe through grep/head only when a list is very long.
- Mutations are idempotent and report what changed; re-running a failed mutation is safe.
- For multi-line markdown bodies or comments, write the text to a UTF-8 file and pass `--body-file <path>`.
- `issue close` moves to the team's first completed-type state; `issue close --cancel` uses the canceled-type state instead.
- States accept a name ("In Review") or a type (`triage`, `backlog`, `unstarted`, `started`, `completed`, `canceled`).
- `--updated-since` accepts friendly durations: `2h`, `3d`, `2w`, `1m`, `1y`, or an ISO date.
- Use `api` for anything the dedicated commands do not cover, e.g. `npx -y @affable-co/linear-axi api 'query { viewer { email } }'`.
