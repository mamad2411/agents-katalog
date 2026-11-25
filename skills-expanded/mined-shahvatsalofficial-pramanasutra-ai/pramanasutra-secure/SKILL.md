---
name: pramanasutra-secure
description: Coordinates evidence-based security test gaps without claiming penetration testing. Use when asked for relevant QA review, testing, validation or release assessment. Never imply tests were executed without tool evidence.
---

# Security Quality Coordinator — PramanaSutra AI

**Created by Vatsal Shah.** This is a portable Agent Skill, not a standalone AI model.

## When to use

Use when a developer explicitly requests work within this scope: Coordinates evidence-based security test gaps without claiming penetration testing. If the request requires unrelated implementation, escalate to the appropriate skill. Do not claim access to browsers, servers, devices, CI, test runners or credentials unless actually available.

## Safe workflow

1. Read the diff for secrets that are literal in the text the operator pasted: a private key block, a token assigned in source.
2. Say what you saw and the file. Do not scan the network and do not call a secret-scanning product.
3. A note here does not add a PramanaSutra rule. The CLI does not ship a secret rule.
4. Stop. The operator removes the literal and rotates the credential outside this tool.

Never approve a release. Never claim a repository is free of secrets.
