---
name: aclif
description: Read or change records in Salesforce, ServiceNow, DocuSign, Agentforce, or Google Workspace through the aclif CLI. Use when asked to query, create, update, or delete records on one of these platforms, to find out what an org holds, or to run a workflow against it.
---

# aclif

`aclif` is a command-line tool on your PATH. It reaches SaaS platforms with one grammar and one JSON envelope, and it is the only way you touch those platforms. Run its commands as a subprocess and parse the JSON on stdout. Credentials are configured on the host in environment variables or a profile; you never need a token and must not ask the user for one.

If the host built its own CLI from aclif, the binary has a different name and its own environment-variable prefix. Everything below is the same with that name in place of `aclif`.

## Workflow

1. `aclif discover --json` lists every provider and whether its credentials are configured. Run it once per session.
2. `aclif learn <provider> --json` returns the provider briefing: topics, key fields, query syntax, and auth paths. About 500 tokens.
3. `aclif <provider> <topic> <command> --schema` returns the flags, arguments, and safety metadata for one command. `--examples` returns runnable examples with the responses they produce. `--shape` returns the structure of a successful result. These flags return before the command executes, need no credentials, and skip required-flag validation, so `--schema` works without `--query`.
4. For a mutation, run the command with `--dry-run` first and show the user what would change.
5. Run the command. Parse stdout as JSON and branch on the exit code.

A first query on a new provider, end to end:

```bash
aclif learn salesforce --json
aclif salesforce data query --schema
aclif salesforce data query --query "SELECT Id, Name FROM Account WHERE Industry = 'Energy' LIMIT 20" --fields Id,Name --json
```

## Rules

- Read `--schema` before the first use of any command in a session. Do not guess flags. A bad flag returns `INVALID_USAGE` on stdout with exit code 2.
- Keep results small. Use `--fields` for the columns you need and `--truncate` for the row count. Run `--estimate` before a query that could return many records.
- Paginate with `_context.pagination.nextCommand`. It is the complete next command; run it as given. Do not construct offsets yourself.
- Before a delete, an update to a filtered set, or anything that runs code on the platform, read `blastRadius` and `requiresConfirmation` in `--schema`. A command that requires confirmation fails until `--confirm` is added. Add `--confirm` only after the user has approved that specific change.
- Never pass `--full`. It puts unmasked secrets in the output.
- On exit code 3 the credentials are missing or were rejected. Stop and tell the user. Do not retry and do not ask for a token.
- On any other failure, read `error.code`, `error.syntaxGuide`, and `error.workingExample`, correct the command, and retry once. `_context.relatedCommands` lists commands worth running next.
- The audit line on stderr is for the operator. Parse stdout only.

## Reading the result

| Field | Holds |
|---|---|
| `success` | `true` or `false` |
| `result` | the records or the provider's response |
| `_context.pagination` | `returned`, `total`, `hasMore`, and `nextCommand` |
| `_context.relatedCommands` | complete command strings worth running next |
| `error` | on failure: `code`, `message`, `syntaxGuide`, and where possible `workingExample` and `correctedValue` |

| Exit code | Meaning | What to do |
|---|---|---|
| 0 | success | parse stdout |
| 1 | API or runtime error | read `error.code`, correct, retry once |
| 2 | invalid usage | fix the flags; check `--schema` |
| 3 | credentials missing or rejected | stop and tell the user |
| 130 | interrupted | the operation may have partly completed |

The full flag list, the safety metadata contract, envelope examples, and the command topology for each provider are in [reference.md](reference.md).
