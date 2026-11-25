---
name: mj-convergence
description: "Majordomus convergence: Is any work held where it can be lost?."
argument-hint: "[request]"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: module:convergence; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Majordomus `convergence`

The capabilities the Majordomus registry declares in its module `convergence`. Choose the one that answers the request below — or, without one, the person's last request about `convergence` — call it through its MCP tool, and report what it answers, as it answered:

$ARGUMENTS

| Capability | What it is | MCP tool | Command line | Effect |
|---|---|---|---|---|
| `convergence.report` | Is any work held where it can be lost? | `majordomus_convergence` | `majordomus convergence` | reads |

A capability that *changes* something runs only when the person asked for that change: call it once, and if it is refused or its outcome is not known, report that as it is and do not try again by another way. One that *reads* may be called whenever the request needs it.

Without the Majordomus MCP server attached, run the command line form from the repository root; `--help` shows its arguments. What each capability accepts and answers is defined once, in its declaration: `majordomus capabilities describe <id>`, or the MCP tool's own description. This file is derived from the registry and says nothing the declarations do not.
