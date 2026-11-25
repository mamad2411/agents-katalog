---
name: skill-hello
description: This is a sample skill that activates when the user says "hello"
metadata:
  version: 1.2.0
---

# skill-hello

This is a sample skill that activates when the user says "hello". It responds with a structured yaml response containing a greeting message in English, the current time retrieved from the system, and the exact version of this skill. You MUST read the `metadata.version` field from the frontmatter of this file (skills/skill-hello/SKILL.md) and use that value — do not guess or recall it from memory. The format must match the following schema:

```yaml
response:
  message: string
  time: string # ISO 8601 format, e.g. 2026-04-15T14:30:00Z
  version: string
```
