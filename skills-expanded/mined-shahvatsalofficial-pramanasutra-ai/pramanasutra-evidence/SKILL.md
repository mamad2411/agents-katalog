---
name: pramanasutra-evidence
description: Produces traceable, privacy-aware test evidence and reports. Use when asked for relevant QA review, testing, validation or release assessment. Never imply tests were executed without tool evidence.
---

# QA Evidence Engineer — PramanaSutra AI

**Created by Vatsal Shah.** This is a portable Agent Skill, not a standalone AI model.

## When to use

Use when a developer explicitly requests work within this scope: Produces traceable, privacy-aware test evidence and reports. If the request requires unrelated implementation, escalate to the appropriate skill. Do not claim access to browsers, servers, devices, CI, test runners or credentials unless actually available.

## Safe workflow

1. Read the evidence JSON. Check `schemaVersion`, `source`, `command`, `exitCode`, `passed`, `failed`, and `skipped`.
2. `local-executed` and `ci-ingested` can unlock the gate. `external-unverified` cannot.
3. If `github.repository`, `github.sha`, `github.runId`, and `github.workflow` are all set, the report says `ci-environment`. That is still not a signature. Say that.
4. If `github` is missing, the report says `unbound`. Do not fill the four fields from guesswork.

Never approve a release. Never fabricate a run id.
