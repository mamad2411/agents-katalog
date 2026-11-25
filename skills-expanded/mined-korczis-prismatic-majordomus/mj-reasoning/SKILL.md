---
name: mj-reasoning
description: "Majordomus reasoning: The advisors and what they can do now; Check that reasoning stays provider-independent; Why a decision was made; What an uncertainty calls for; Record a reasoning step; The session's reasoning state."
argument-hint: "[request]"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: module:reasoning; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Majordomus `reasoning`

The capabilities the Majordomus registry declares in its module `reasoning`. Choose the one that answers the request below — or, without one, the person's last request about `reasoning` — call it through its MCP tool, and report what it answers, as it answered:

$ARGUMENTS

| Capability | What it is | MCP tool | Command line | Effect |
|---|---|---|---|---|
| `reasoning.advisors` | The advisors and what they can do now | `majordomus_reasoning_advisors` | `majordomus reasoning advisors` | reads |
| `reasoning.check` | Check that reasoning stays provider-independent | `majordomus_reasoning_check` | `majordomus reasoning check` | reads |
| `reasoning.explain` | Why a decision was made | `majordomus_reasoning_explain` | `majordomus reasoning explain` | reads |
| `reasoning.plan` | What an uncertainty calls for | `majordomus_reasoning_plan` | `majordomus reasoning plan` | reads |
| `reasoning.record` | Record a reasoning step | `majordomus_reasoning_record` | `majordomus reasoning record` | changes |
| `reasoning.status` | The session's reasoning state | `majordomus_reasoning` | `majordomus reasoning status` | reads |

A capability that *changes* something runs only when the person asked for that change: call it once, and if it is refused or its outcome is not known, report that as it is and do not try again by another way. One that *reads* may be called whenever the request needs it.

Without the Majordomus MCP server attached, run the command line form from the repository root; `--help` shows its arguments. What each capability accepts and answers is defined once, in its declaration: `majordomus capabilities describe <id>`, or the MCP tool's own description. This file is derived from the registry and says nothing the declarations do not.
