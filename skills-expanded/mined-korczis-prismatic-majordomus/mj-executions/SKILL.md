---
name: mj-executions
description: "Majordomus executions: Ask an execution to stop; Demonstrate an execution; An execution's event history; One execution; List executions; The live channel's contract; Start a capability as an execution."
argument-hint: "[request]"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: module:executions; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Majordomus `executions`

The capabilities the Majordomus registry declares in its module `executions`. Choose the one that answers the request below — or, without one, the person's last request about `executions` — call it through its MCP tool, and report what it answers, as it answered:

$ARGUMENTS

| Capability | What it is | MCP tool | Command line | Effect |
|---|---|---|---|---|
| `executions.cancel` | Ask an execution to stop | `majordomus_execution_cancel` | `majordomus executions cancel` | changes |
| `executions.demonstrate` | Demonstrate an execution | `majordomus_demonstrate_execution` | — | reads |
| `executions.events` | An execution's event history | `majordomus_execution_events` | `majordomus executions events` | reads |
| `executions.get` | One execution | `majordomus_execution` | `majordomus executions show` | reads |
| `executions.list` | List executions | `majordomus_executions` | `majordomus executions list` | reads |
| `executions.protocol` | The live channel's contract | `majordomus_execution_protocol` | `majordomus executions protocol` | reads |
| `executions.start` | Start a capability as an execution | `majordomus_execution_start` | `majordomus run` | changes |

A capability that *changes* something runs only when the person asked for that change: call it once, and if it is refused or its outcome is not known, report that as it is and do not try again by another way. One that *reads* may be called whenever the request needs it.

Without the Majordomus MCP server attached, run the command line form from the repository root; `--help` shows its arguments. What each capability accepts and answers is defined once, in its declaration: `majordomus capabilities describe <id>`, or the MCP tool's own description. This file is derived from the registry and says nothing the declarations do not.
