---
name: mj-lifecycle
description: "Majordomus lifecycle: The records a clone receives; Every open episode; What each provider's adapter declares; What the store needs somebody to do; The commit this process is answering about."
argument-hint: "[request]"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: module:lifecycle; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Majordomus `lifecycle`

The capabilities the Majordomus registry declares in its module `lifecycle`. Choose the one that answers the request below — or, without one, the person's last request about `lifecycle` — call it through its MCP tool, and report what it answers, as it answered:

$ARGUMENTS

| Capability | What it is | MCP tool | Command line | Effect |
|---|---|---|---|---|
| `lifecycle.closed` | The records a clone receives | `majordomus_lifecycle_closed` | — | reads |
| `lifecycle.episodes` | Every open episode | `majordomus_lifecycle_episodes` | — | reads |
| `lifecycle.providers` | What each provider's adapter declares | `majordomus_lifecycle_providers` | — | reads |
| `lifecycle.recovery` | What the store needs somebody to do | `majordomus_lifecycle_recovery` | — | reads |
| `lifecycle.runtime` | The commit this process is answering about | `majordomus_lifecycle_runtime` | — | reads |

A capability that *changes* something runs only when the person asked for that change: call it once, and if it is refused or its outcome is not known, report that as it is and do not try again by another way. One that *reads* may be called whenever the request needs it.

Without the Majordomus MCP server attached, run the command line form from the repository root; `--help` shows its arguments. What each capability accepts and answers is defined once, in its declaration: `majordomus capabilities describe <id>`, or the MCP tool's own description. This file is derived from the registry and says nothing the declarations do not.
