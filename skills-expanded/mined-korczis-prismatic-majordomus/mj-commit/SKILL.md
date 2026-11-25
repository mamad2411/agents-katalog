---
name: mj-commit
description: "Majordomus commit: Judge a range of history; What the working tree would commit; The scope vocabulary; Judge one commit message."
argument-hint: "[request]"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: module:commit; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Majordomus `commit`

The capabilities the Majordomus registry declares in its module `commit`. Choose the one that answers the request below — or, without one, the person's last request about `commit` — call it through its MCP tool, and report what it answers, as it answered:

$ARGUMENTS

| Capability | What it is | MCP tool | Command line | Effect |
|---|---|---|---|---|
| `commit.history` | Judge a range of history | `majordomus_commit_history` | `majordomus commit history` | reads |
| `commit.plan` | What the working tree would commit | `majordomus_commit_plan` | `majordomus commit plan` | reads |
| `commit.scopes` | The scope vocabulary | `majordomus_commit_scopes` | `majordomus commit scopes` | reads |
| `commit.validate` | Judge one commit message | `majordomus_commit_validate` | `majordomus commit validate` | reads |

A capability that *changes* something runs only when the person asked for that change: call it once, and if it is refused or its outcome is not known, report that as it is and do not try again by another way. One that *reads* may be called whenever the request needs it.

Without the Majordomus MCP server attached, run the command line form from the repository root; `--help` shows its arguments. What each capability accepts and answers is defined once, in its declaration: `majordomus capabilities describe <id>`, or the MCP tool's own description. This file is derived from the registry and says nothing the declarations do not.
