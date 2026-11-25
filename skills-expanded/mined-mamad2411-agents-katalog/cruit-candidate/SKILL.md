---
name: cruit-candidate
description: Create and maintain a Cruit candidate profile and submit evidence packets for AI-native developer requests. Use when the user wants to join Cruit, publish or refresh a profile, answer an evidence request, submit scrubbed agent-work evidence, or set up weekly profile updates.
---

# Cruit — Candidate Skill

## Load instructions

The canonical instructions are bundled with this skill:

```text
INSTRUCTIONS.md
```

Read that file first on every run and follow it. If it cannot be loaded, stop and tell
the user the Cruit candidate instructions are unavailable.

## Safety rules

- Do not publish source code, secrets, `.env` files, private keys, email addresses,
  phone numbers, street addresses, or private contact details.
- Never upload unsanitized coding-agent transcripts; only submit scrubbed excerpts the
  user approved.
- Confirm with the user before reviewing folders, publishing a profile, submitting an
  evidence packet, or setting up automation.
