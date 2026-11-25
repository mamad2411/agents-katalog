---
name: mj-rules
description: "Majordomus rules: What this test proves; Every rule against the proof there is for it; What proves this rule."
argument-hint: "[request]"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: module:rules; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Majordomus `rules`

The capabilities the Majordomus registry declares in its module `rules`. Choose the one that answers the request below — or, without one, the person's last request about `rules` — call it through its MCP tool, and report what it answers, as it answered:

$ARGUMENTS

| Capability | What it is | MCP tool | Command line | Effect |
|---|---|---|---|---|
| `rules.proves` | What this test proves | `majordomus_rule_proves` | `majordomus rules proves` | reads |
| `rules.report` | Every rule against the proof there is for it | `majordomus_rules` | `majordomus rules report` | reads |
| `rules.show` | What proves this rule | `majordomus_rule` | `majordomus rules show` | reads |

A capability that *changes* something runs only when the person asked for that change: call it once, and if it is refused or its outcome is not known, report that as it is and do not try again by another way. One that *reads* may be called whenever the request needs it.

Without the Majordomus MCP server attached, run the command line form from the repository root; `--help` shows its arguments. What each capability accepts and answers is defined once, in its declaration: `majordomus capabilities describe <id>`, or the MCP tool's own description. This file is derived from the registry and says nothing the declarations do not.
