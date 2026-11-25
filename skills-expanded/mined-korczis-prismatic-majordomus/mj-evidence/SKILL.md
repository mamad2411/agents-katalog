---
name: mj-evidence
description: "Majordomus evidence: What proves this claim; Every claim against the evidence recorded for it; What this test proves."
argument-hint: "[request]"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: module:evidence; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Majordomus `evidence`

The capabilities the Majordomus registry declares in its module `evidence`. Choose the one that answers the request below — or, without one, the person's last request about `evidence` — call it through its MCP tool, and report what it answers, as it answered:

$ARGUMENTS

| Capability | What it is | MCP tool | Command line | Effect |
|---|---|---|---|---|
| `evidence.claim` | What proves this claim | `majordomus_evidence_claim` | `majordomus evidence claim` | reads |
| `evidence.report` | Every claim against the evidence recorded for it | `majordomus_evidence` | `majordomus evidence show` | reads |
| `evidence.test` | What this test proves | `majordomus_evidence_test` | `majordomus evidence proves` | reads |

A capability that *changes* something runs only when the person asked for that change: call it once, and if it is refused or its outcome is not known, report that as it is and do not try again by another way. One that *reads* may be called whenever the request needs it.

Without the Majordomus MCP server attached, run the command line form from the repository root; `--help` shows its arguments. What each capability accepts and answers is defined once, in its declaration: `majordomus capabilities describe <id>`, or the MCP tool's own description. This file is derived from the registry and says nothing the declarations do not.
