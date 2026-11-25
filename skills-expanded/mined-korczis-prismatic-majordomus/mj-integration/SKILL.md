---
name: mj-integration
description: "Majordomus integration: What cleanup would do; The integration audit trail; Why one pull request is where it is; Proof that a dry run moves nothing; The integration queue; How long CI takes; The trains of stacked pull requests."
argument-hint: "[request]"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: module:integration; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Majordomus `integration`

The capabilities the Majordomus registry declares in its module `integration`. Choose the one that answers the request below — or, without one, the person's last request about `integration` — call it through its MCP tool, and report what it answers, as it answered:

$ARGUMENTS

| Capability | What it is | MCP tool | Command line | Effect |
|---|---|---|---|---|
| `integration.cleanup` | What cleanup would do | `majordomus_pull_requests_cleanup` | — | reads |
| `integration.events` | The integration audit trail | `majordomus_integration_events` | `majordomus prs events` | reads |
| `integration.explain` | Why one pull request is where it is | `majordomus_pull_request_explain` | `majordomus prs explain` | reads |
| `integration.prove_dry_run` | Proof that a dry run moves nothing | `majordomus_pull_requests_prove_dry_run` | `majordomus prs prove-dry-run` | reads |
| `integration.queue` | The integration queue | `majordomus_pull_requests` | `majordomus prs status` | reads |
| `integration.timings` | How long CI takes | `majordomus_ci_timings` | — | reads |
| `integration.trains` | The trains of stacked pull requests | `majordomus_pull_request_trains` | `majordomus prs trains` | reads |

A capability that *changes* something runs only when the person asked for that change: call it once, and if it is refused or its outcome is not known, report that as it is and do not try again by another way. One that *reads* may be called whenever the request needs it.

Without the Majordomus MCP server attached, run the command line form from the repository root; `--help` shows its arguments. What each capability accepts and answers is defined once, in its declaration: `majordomus capabilities describe <id>`, or the MCP tool's own description. This file is derived from the registry and says nothing the declarations do not.
