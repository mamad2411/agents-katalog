---
name: vpsctl
description: Operate remote Linux VPS hosts through the vpsctl CLI, including SSH host inventory, project deployment profiles, commands, transfers, tunnels, jump hosts, keys, local context, snapshots, and recorded changes. Use for remote VPS administration or deployment tasks; do not use for localhost-only work.
license: MIT
compatibility: Requires the vpsctl CLI, Python 3.9+, an OpenSSH client, and SSH hosts configured in ~/.ssh/config. Remote operations require network access.
metadata:
  author: Xichun123
  version: "0.3.0"
---

# vpsctl

Use the installed `vpsctl` command for remote SSH and VPS operations. Do not depend on this Skill's installation path and do not invoke package-internal Python files.

Read [references/commands.md](references/commands.md) when exact command syntax or less common operations are needed.

## Preconditions

Confirm the CLI is available before remote work:

```bash
vpsctl --version
```

If it is missing, report that the Python package must be installed. Installing this Skill does not install the `vpsctl` executable.

## Mandatory policy

- Use aliases from `~/.ssh/config`; discover unknown aliases with `vpsctl list` or `vpsctl find <query>`.
- Prefer `vpsctl` for all remote SSH, SCP, and rsync work instead of invoking those tools directly.
- Use JSON `success` and `exit_code` to determine command status. Read `stdout` for command output and optional `stderr` when present; empty `stderr` is omitted.
- Use `vpsctl exec` for simple read-only commands.
- Use `vpsctl apply` for modifications to an existing profiled project so the change is recorded.
- Respect every project's `protected_paths`; do not overwrite, delete, or recreate protected content without explicit approval.
- Treat profile deploy, restart, and log commands as documentation, not standing authorization.
- Confirm the target and impact before production changes, deletion, authentication migration, or key writes.
- Combine independent read-only queries for one host into a single `exec` where practical.
- Use `--stdin` or `--script-file` for commands containing `$()`, backticks, `${VAR}`, heredocs, nested quoting, secrets, certificates, JSON/YAML, or long scripts.
- After a change, perform the smallest relevant read-only verification; do not refresh unrelated projects.
- Record uploads, migrations, and changes outside `apply` with `vpsctl change add`.
- Update the static project profile when paths, services, Compose files, domains, or operational commands change.

## Project workflow

For an existing project:

1. Run `vpsctl project list` or `vpsctl project show <name>`.
2. Run `vpsctl context --project <name>` without `--refresh` for routine work.
3. Inspect `protected_paths`, `recent_changes`, `changes_since_baseline`, and `warnings`.
4. Execute read-only work with `exec` and modifications with `apply`.
5. Verify the changed behavior with a focused read-only command.
6. Update static profile fields and add supplemental change records when required.

Context is local by default. Use explicit refresh only for first baselines, missing caches, suspected external drift, troubleshooting, or a user request for current remote state.

Interpret context status precisely:

- `tracked`: initial baseline plus the vpsctl change journal, not a fresh remote check.
- `fresh`: an explicitly age-bounded snapshot is still within its requested maximum age.
- `stale`: an explicitly age-bounded snapshot is older than requested.
- `missing`: no successful baseline exists.
- `refresh_failed`: the latest refresh failed while the last successful snapshot remains available.

Clearly report `missing` and `refresh_failed` states.

## New project rule

Any task that deploys, migrates, or creates a project on a VPS must end with a vpsctl project profile. Deployment and profile creation may happen in either order.

Create a minimum profile as soon as practical:

```bash
vpsctl project add <name> --host <alias> --path <absolute-remote-path>
vpsctl project show <name>
```

Before declaring the task complete, `vpsctl project show <name>` must succeed. If deployment happened before profiling, add the initial deployment record:

```bash
vpsctl change add <name> --kind deploy --summary "Initial deployment of <name>"
```

Do not skip profiling because runtime, service, domain, or command details are incomplete. Add those fields later with `vpsctl project update`.

## Host-only workflow

For work that is genuinely about a host rather than a deployed project:

```bash
vpsctl context --host <alias>
vpsctl exec <alias> "<read-only-command>"
```

Do not refresh an entire host merely to update one known project.

## Mutation and verification

Use recorded mutations for existing projects:

```bash
vpsctl apply <project> --kind <kind> --summary "<summary>" "<command>"
```

`apply` records successful and failed attempts because a failed command may have partially changed the remote system. It stores the summary, type, time, result, and payload SHA-256, but not the command body.

After modification, run a targeted check such as service status, container status, a health endpoint, or a specific file metadata query. Do not claim success when validation fails or was not run.
