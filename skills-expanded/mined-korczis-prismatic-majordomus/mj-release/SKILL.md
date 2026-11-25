---
name: mj-release
description: "Majordomus release: What the public contract did, and the smallest version it allows; The changelog; Whether the trunk's landed work is released; The version a landing allocates, and why; The version, and the one the contract requires next."
argument-hint: "[request]"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: module:release; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Majordomus `release`

The capabilities the Majordomus registry declares in its module `release`. Choose the one that answers the request below — or, without one, the person's last request about `release` — call it through its MCP tool, and report what it answers, as it answered:

$ARGUMENTS

| Capability | What it is | MCP tool | Command line | Effect |
|---|---|---|---|---|
| `release.analysis` | What the public contract did, and the smallest version it allows | `majordomus_release_analysis` | — | reads |
| `release.changelog` | The changelog | `majordomus_changelog` | — | reads |
| `release.currency` | Whether the trunk's landed work is released | `majordomus_release_currency` | — | reads |
| `release.next` | The version a landing allocates, and why | `majordomus_release_next` | — | reads |
| `release.version` | The version, and the one the contract requires next | `majordomus_release_version` | — | reads |

A capability that *changes* something runs only when the person asked for that change: call it once, and if it is refused or its outcome is not known, report that as it is and do not try again by another way. One that *reads* may be called whenever the request needs it.

Without the Majordomus MCP server attached, run the command line form from the repository root; `--help` shows its arguments. What each capability accepts and answers is defined once, in its declaration: `majordomus capabilities describe <id>`, or the MCP tool's own description. This file is derived from the registry and says nothing the declarations do not.
