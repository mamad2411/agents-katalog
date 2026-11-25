---
name: mj-intents
description: "Majordomus intents: What a piece of work is bound to before it starts; Which work carries which criterion, and why each issue exists; Every intent, with its derived stage and verdict; Which intent a piece of work serves, or why it may not proceed; Propose an intent: what must become true; One…"
argument-hint: "[request]"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: module:intents; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Majordomus `intents`

The capabilities the Majordomus registry declares in its module `intents`. Choose the one that answers the request below — or, without one, the person's last request about `intents` — call it through its MCP tool, and report what it answers, as it answered:

$ARGUMENTS

| Capability | What it is | MCP tool | Command line | Effect |
|---|---|---|---|---|
| `intents.binding` | What a piece of work is bound to before it starts | `majordomus_intent_binding` | `majordomus intent binding` | reads |
| `intents.coverage` | Which work carries which criterion, and why each issue exists | `majordomus_intent_coverage` | `majordomus intent coverage` | reads |
| `intents.list` | Every intent, with its derived stage and verdict | `majordomus_intents` | `majordomus intent list` | reads |
| `intents.preflight` | Which intent a piece of work serves, or why it may not proceed | `majordomus_intent_preflight` | `majordomus intent preflight` | reads |
| `intents.propose` | Propose an intent: what must become true | `majordomus_intent_propose` | `majordomus intent propose` | changes |
| `intents.record` | One intent, with everything derived about it | `majordomus_intent_record` | `majordomus intent show` | reads |
| `intents.validate` | What the intent model refuses | `majordomus_intent_validate` | `majordomus intent validate` | reads |

A capability that *changes* something runs only when the person asked for that change: call it once, and if it is refused or its outcome is not known, report that as it is and do not try again by another way. One that *reads* may be called whenever the request needs it.

Without the Majordomus MCP server attached, run the command line form from the repository root; `--help` shows its arguments. What each capability accepts and answers is defined once, in its declaration: `majordomus capabilities describe <id>`, or the MCP tool's own description. This file is derived from the registry and says nothing the declarations do not.
