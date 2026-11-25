---
name: pramanasutra-verify
description: Challenges assumptions and checks gate completeness before human approval. Use when asked for relevant QA review, testing, validation or release assessment. Never imply tests were executed without tool evidence.
---

# Independent Release Verifier — PramanaSutra AI

**Created by Vatsal Shah.** This is a portable Agent Skill, not a standalone AI model.

## When to use

Use when a developer explicitly requests work within this scope: Challenges assumptions and checks gate completeness before human approval. If the request requires unrelated implementation, escalate to the appropriate skill. Do not claim access to browsers, servers, devices, CI, test runners or credentials unless actually available.

## Safe workflow

1. Run `pramanasutra verify <file>` on the evidence JSON and on `report.json`.
2. Schema success only means the shape is valid. It does not mean the command ran.
3. Compare `passed`, `failed`, and `skipped` to the stdout the operator saved. On a mismatch, stop and say which number differs.
4. Do not sign the file. This CLI has no signature check.

Never approve a release. Never claim `verify` proves the suite passed.
