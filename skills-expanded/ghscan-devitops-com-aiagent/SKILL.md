---
name: chat
description: Basic resumable multi-turn Q&A against the configured model (a minor convenience feature).
entrypoint: skill:build
model: default
version: 0.1.0
---

# Chat

A minimal conversational skill built on `dspy.Predict` + `dspy.History`. aiagent
is not a chat framework — this exists so `aiagent chat` works for quick Q&A, with
multi-turn history persisted per session so a conversation can be resumed
(`aiagent chat --session <name>`). History is optional, so `aiagent run chat
--text "..."` also works single-shot. For anything substantive, use `run` /
`optimize` / `eval`.
