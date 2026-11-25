---
name: brainstem
description: |
  Uses the user's RAPP Brainstem for agentic tasks, personal agents, memory,
  and installed RAPP capabilities. Use when the user says "use my Brainstem",
  "ask my Brainstem", "use RAPP", or requests an installed RAPP agent.
license: MIT
metadata:
  author: RAPP
  version: "0.2.1"
---

# RAPP Brainstem

1. Call `brainstem_status` before the first Brainstem operation.
2. If GitHub is not connected, tell the user to connect their GitHub account.
3. Call `brainstem` with the user's request in plain English.
4. Continue with the returned session ID when the task is conversational.
5. Never ask the user to paste a GitHub token.
6. Never claim success when Brainstem reports an agent or authentication error.
