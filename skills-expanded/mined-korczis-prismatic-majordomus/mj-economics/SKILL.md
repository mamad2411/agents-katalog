---
name: mj-economics
description: "Majordomus economics: Refuse unsupported economics claims; Explain one economics metric; Recorded benchmark runs; Token economics summary; Each task's delivery economics."
argument-hint: "[request]"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: module:economics; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Majordomus `economics`

The capabilities the Majordomus registry declares in its module `economics`. Choose the one that answers the request below — or, without one, the person's last request about `economics` — call it through its MCP tool, and report what it answers, as it answered:

$ARGUMENTS

| Capability | What it is | MCP tool | Command line | Effect |
|---|---|---|---|---|
| `economics.check` | Refuse unsupported economics claims | `majordomus_economics_check` | `majordomus economics check` | reads |
| `economics.explain` | Explain one economics metric | `majordomus_economics_explain` | `majordomus economics explain` | reads |
| `economics.runs` | Recorded benchmark runs | `majordomus_economics_runs` | `majordomus economics runs` | reads |
| `economics.summary` | Token economics summary | `majordomus_economics` | `majordomus economics summary` | reads |
| `economics.tasks` | Each task's delivery economics | `majordomus_economics_tasks` | `majordomus economics tasks` | reads |

A capability that *changes* something runs only when the person asked for that change: call it once, and if it is refused or its outcome is not known, report that as it is and do not try again by another way. One that *reads* may be called whenever the request needs it.

Without the Majordomus MCP server attached, run the command line form from the repository root; `--help` shows its arguments. What each capability accepts and answers is defined once, in its declaration: `majordomus capabilities describe <id>`, or the MCP tool's own description. This file is derived from the registry and says nothing the declarations do not.
