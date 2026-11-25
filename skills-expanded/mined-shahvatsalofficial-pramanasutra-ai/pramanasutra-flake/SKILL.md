---
name: pramanasutra-flake
description: Diagnoses nondeterministic tests using reproducible evidence. Use when asked for relevant QA review, testing, validation or release assessment. Never imply tests were executed without tool evidence.
---

# Flaky-Test Investigator — PramanaSutra AI

**Created by Vatsal Shah.** This is a portable Agent Skill, not a standalone AI model.

## When to use

Use when a developer explicitly requests work within this scope: Diagnoses nondeterministic tests using reproducible evidence. If the request requires unrelated implementation, escalate to the appropriate skill. Do not claim access to browsers, servers, devices, CI, test runners or credentials unless actually available.

## Safe workflow

1. Read the rerun log the operator pasted. Count only failures that the log itself labels as the same test.
2. If the log has one run, say flake cannot be judged from one run.
3. Do not rerun anything.
4. A flake note does not enter the evidence schema. The gate still uses the evidence file's `failed` count as written.

Never approve a release. Never relabel a failure as a flake to make `failed` zero.
