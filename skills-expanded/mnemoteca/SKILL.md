---
name: mnemoteca
description: Persistent project memory. Store, search, and recall project memories, decisions, and context. Use this whenever you start a session to recall past context, or when a durable decision or lesson should be retained.
argument-hint: "[action] [query]"
user-invocable: true
allowed-tools: Bash(mnemoteca)
---

# Mnemoteca Skill

You are equipped with the `mnemoteca` CLI tool for managing persistent project memory. This tool lets you store, search, and recall important context, decisions, preferences, and architecture guidelines.

## Memory System

Use the `Bash` tool to execute `mnemoteca` commands. Because `allowed-tools: Bash(mnemoteca)` is set, you have permission to run the `mnemoteca` command directly.

- Use `mnemoteca search -f plain [query]` and `mnemoteca search -g -f plain [query]` to recall relevant context before decisions.
- Core memories are strong guidance; other memories are useful, non-authoritative context. Neither overrides the user, current project docs, the applicable plan, or code as evidence of implemented behavior. Resolve conflicts against those authorities; distinguish intended requirements from delivered behavior.
- Use `mnemoteca add "memory content"` only for current durable decisions, preferences, constraints, rationale, and reusable lessons. Use `-g` for cross-project defaults. Honor explicit requests to remember something.
- Do not store routine release dates, commit hashes, completed PR inventories, one-off test counts, or task-completion receipts. Extract a durable lesson when one exists; otherwise store nothing. Completion alone does not require a memory.
- Keep history only when it explains a still-relevant decision. State the current rule directly, not an obsolete claim beside a correction. Do not present proposed work or unverified recollections as current facts.
- Correct outdated memories with `mnemoteca update [memory id] "current guidance"`, or add and verify a replacement before removing the source with `mnemoteca delete [memory id]`. Remove routine bookkeeping after retaining any durable lesson.
- Mark only critical, always-relevant guidance as core with `-t core`. Core changes injection priority, not authority. Other tags can be supplied with repeated `-t` flags.
