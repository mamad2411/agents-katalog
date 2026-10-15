---
name: polygres-cli
description: Use the Polygres CLI to authenticate, select and inspect projects, obtain safe Postgres connection information, open psql, manage Runtime API keys, import CSV, TSV, JSON, or JSONL data through safe local preparation and the CSV import API, apply migrations, configure graph, vector, or text retrieval, and check project or retrieval readiness. Use whenever a user asks an AI coding agent to set up, operate, automate, or troubleshoot a managed Polygres project.
---

# Polygres CLI

Operate a user's Polygres project through the installed `polygres` command.
Treat the CLI as the operational and security boundary. Do not call private
control-plane routes or infer undocumented request payloads.

## Start safely

1. Run `polygres --version` and `polygres --help` when availability or command
   compatibility is unknown.
2. If the command is missing, tell the user how to install `polygres-cli` and
   let them approve or perform the installation. Do not install packages
   silently.
3. Run `polygres whoami` before a mutation when identity or active organization
   is uncertain. Use `polygres login` when authentication is required.
4. Resolve the project with `polygres projects list`, an explicit `--project`,
   or `polygres projects use <project>`. State the resolved project before a
   destructive, secret-producing, or schema-mutating operation.
5. Prefer `polygres --json ...` for output the agent must parse. Treat stdout as
   the JSON channel and stderr as diagnostics.

If bundled examples differ from the installed `--help`, follow the installed
command surface and explain the version mismatch. Never guess a replacement.

## Route the request

Read only the references needed for the task:

| User intent | Reference |
| --- | --- |
| Login, logout, identity, organization, project selection or status | `references/authentication-and-projects.md` |
| Environment, Postgres metadata, `psql`, Runtime API keys | `references/database-and-keys.md` |
| CSV, TSV, JSON, JSONL/NDJSON, import jobs | `references/data-imports.md` |
| Migration list/apply and SQL safety | `references/migrations.md` |
| Graph, vector, text, retrieval readiness | `references/retrieval.md` |
| JSON output, polling, exit codes, retry and recovery | `references/automation-and-errors.md` |

## Execute an operation

1. Classify the request as read-only, mutating, destructive,
   schema-mutating, or secret-producing.
2. Load the relevant reference and validate local inputs.
3. Resolve authentication and project context.
4. For a mutation, show the target project, affected resource, important
   options, and reversibility.
5. Obtain explicit approval when required.
6. Run the narrowest documented command.
7. Retain project, job, migration, configuration, key, and request IDs from the
   result.
8. Report only the observed terminal state. If work is still running, say so
   and provide the status command.

## Require consent

Obtain explicit user approval before:

- `replace_existing` imports;
- applying a SQL migration;
- creating a generated TSVector column;
- revoking a Runtime API key;
- deleting vector or text configurations;
- any command that uses `--yes`;
- any other operation that is destructive or difficult to reverse.

Add `--yes` only after approval for that exact operation and target.

## Protect secrets

- Never request, retrieve, store, log, or pass a native database password.
- Let `psql` prompt the user for the database password.
- If an agent terminal cannot maintain an interactive TTY, give the user the
  passwordless command or ask them to run `polygres db psql` directly.
- Never ask a user for `POLYGRES_ACCESS_TOKEN`. It is a development and test
  override, not a public authentication workflow.
- Warn before `polygres keys create <name>` because the Runtime API-key secret
  is shown once and can enter terminal or agent history.
- Offer to let the user run key creation in their own terminal so the secret
  does not enter the agent transcript.
- Never place tokens, keys, or passwords in source files, examples, command
  arguments, logs, or final summaries.

## Prepare non-CSV data locally

For TSV, JSON, and JSONL/NDJSON, read `references/data-imports.md` and use
`scripts/prepare_import.py`. Resolve the script path from this skill directory
instead of assuming the repository contains `scripts/`.

The converter is local-only and produces a reviewed CSV artifact. It does not
call Polygres. Never silently flatten nested JSON, rename columns, or collapse
null and empty-string values without explaining the result and obtaining the
required approval.

Do not present SQL migrations as a generic row-import mechanism. Do not call
the backend SQL-import or `pg_dump` routes because those commands are not in
the current public CLI.

## Handle failures

Use `references/automation-and-errors.md` to interpret exit codes. In
particular:

- Fix validation before retrying exit `2`.
- Reauthenticate on exit `3`.
- Explain missing permission on exit `4`.
- Resolve missing resources on exit `5`.
- Resolve conflicts or ambiguous project selection on exit `6`.
- Respect rate-limit guidance on exit `7`.
- Treat exit `8` as remote failure or timeout.
- Install or hand off a missing local dependency such as `psql` on exit `9`.

After an import or provisioning timeout, check the known resource or job status
before resubmitting. A timed-out client does not prove the server operation
failed.
