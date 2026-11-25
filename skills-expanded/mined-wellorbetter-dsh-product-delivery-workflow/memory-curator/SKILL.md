---
name: memory-curator
description: Curate safe cross-session project memory candidates from approved workflow evidence without storing secrets, transcripts, source dumps, or private data.
user-invocable: true
---

# Memory Curator

Extract durable memories from approved artifacts only. Store candidates under `.opencode/memory/candidates/` with scope, statement, source, confidence, date, review date, and invalidation condition. Never store secrets, raw transcripts, source dumps, personal data, or unverified assumptions. Keep project memories isolated by repository. Do not promote candidates or alter prompts/configuration without explicit human approval.
