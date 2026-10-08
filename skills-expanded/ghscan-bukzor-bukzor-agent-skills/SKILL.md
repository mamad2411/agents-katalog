---
label: BASIS
standing: user
why:
  - ../extension.md
---

# An Extension Declares the Chat Skill

An extension of the claim ledger declares `/llm-claims` as its
basis, and notes that the agent should use `/llm-claims-kb` if the
user wants persistence. It does not declare both: the extension
gains the same two modalities its basis already has, at no added
complexity, because the modality choice was never the extension's to
make.
