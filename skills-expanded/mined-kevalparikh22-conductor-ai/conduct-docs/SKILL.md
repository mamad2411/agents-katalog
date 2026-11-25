---
name: conduct-docs
description: "Delegate documentation (README, docs, changelog) to a free/cheap model; controller checks accuracy"
argument-hint: "<what to document>"
disable-model-invocation: true
allowed-tools: "Read, Bash(conductor-ai:*), Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git stash push:*)"
---

You are the controller. Make sure the tree is clean, then run in the background:
`conductor-ai run docs "Document: the arguments the user gave" --files <the relevant source and doc files>`

Check `conductor-ai diff` for accuracy: every command, flag and name must exist in the code. Fix small inaccuracies yourself and commit (`docs: ...`).
