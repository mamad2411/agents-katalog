---
name: mj-continuity
description: "Majordomus continuity: This device's identity, and its label; Whether and how a published handover can be resumed here; Publish this checkout's newest handover for another machine; Every published handover the local store admits; Resume a handover another machine published; What the lifecycle is…"
argument-hint: "[request]"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: module:continuity; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Majordomus `continuity`

The capabilities the Majordomus registry declares in its module `continuity`. Choose the one that answers the request below — or, without one, the person's last request about `continuity` — call it through its MCP tool, and report what it answers, as it answered:

$ARGUMENTS

| Capability | What it is | MCP tool | Command line | Effect |
|---|---|---|---|---|
| `continuity.device` | This device's identity, and its label | `majordomus_continuity_device` | `majordomus continuity device` | changes |
| `continuity.plan` | Whether and how a published handover can be resumed here | `majordomus_continuity_plan` | `majordomus continuity plan` | reads |
| `continuity.publish` | Publish this checkout's newest handover for another machine | `majordomus_continuity_publish` | `majordomus continuity publish` | changes |
| `continuity.records` | Every published handover the local store admits | `majordomus_continuity_records` | `majordomus continuity records` | reads |
| `continuity.resume` | Resume a handover another machine published | `majordomus_continuity_resume` | `majordomus continuity resume` | changes |
| `continuity.state` | What the lifecycle is holding | `majordomus_continuity` | — | reads |
| `continuity.status` | Where this device stands in the work published from every device | `majordomus_continuity_status` | `majordomus continuity status` | reads |
| `continuity.sync` | Exchange published handovers with a git remote | `majordomus_continuity_sync` | `majordomus continuity sync` | changes |

A capability that *changes* something runs only when the person asked for that change: call it once, and if it is refused or its outcome is not known, report that as it is and do not try again by another way. One that *reads* may be called whenever the request needs it.

Without the Majordomus MCP server attached, run the command line form from the repository root; `--help` shows its arguments. What each capability accepts and answers is defined once, in its declaration: `majordomus capabilities describe <id>`, or the MCP tool's own description. This file is derived from the registry and says nothing the declarations do not.
