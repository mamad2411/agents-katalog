---
name: mj-worktree
description: "Majordomus worktree: The canonical worktree of a branch, made or found; One branch: where its worktree belongs and what is there; What it would take to bring every worktree home; Where this is, and whether that is where it belongs; The whole topology; How far a checkout is from the remote trunk…"
argument-hint: "[request]"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: module:worktree; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Majordomus `worktree`

The capabilities the Majordomus registry declares in its module `worktree`. Choose the one that answers the request below — or, without one, the person's last request about `worktree` — call it through its MCP tool, and report what it answers, as it answered:

$ARGUMENTS

| Capability | What it is | MCP tool | Command line | Effect |
|---|---|---|---|---|
| `worktree.create` | The canonical worktree of a branch, made or found | `majordomus_worktree_create` | `majordomus worktree ensure` | changes |
| `worktree.inspect` | One branch: where its worktree belongs and what is there | `majordomus_worktree_inspect` | `majordomus worktree inspect` | reads |
| `worktree.migration_plan` | What it would take to bring every worktree home | `majordomus_worktree_migration_plan` | `majordomus worktree migrate` | reads |
| `worktree.status` | Where this is, and whether that is where it belongs | `majordomus_worktree_status` | `majordomus worktree status` | reads |
| `worktree.topology` | The whole topology | `majordomus_worktrees` | `majordomus worktree topology` | reads |
| `worktree.trunk` | How far a checkout is from the remote trunk | `majordomus_worktree_trunk` | `majordomus worktree trunk` | reads |
| `worktree.uncommitted` | Uncommitted work in the linked worktrees, and what holds it | `majordomus_worktree_uncommitted` | `majordomus worktree uncommitted` | reads |

A capability that *changes* something runs only when the person asked for that change: call it once, and if it is refused or its outcome is not known, report that as it is and do not try again by another way. One that *reads* may be called whenever the request needs it.

Without the Majordomus MCP server attached, run the command line form from the repository root; `--help` shows its arguments. What each capability accepts and answers is defined once, in its declaration: `majordomus capabilities describe <id>`, or the MCP tool's own description. This file is derived from the registry and says nothing the declarations do not.
