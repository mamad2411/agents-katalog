---
name: wf-guru
description: PROACTIVELY use when the user asks how repository source code or project documentation works — locating behavior, explaining pipelines, architecture, specs, framework scripts, indexing, chunking, retrieval, or MCP tools. Not for wave lifecycle commands (Plan change, Implement wave, Close wave, etc.).
---

# Wavefoundry Guru (skill — optional native surface)

Canonical rules for **all** hosts: `AGENTS.md` § **Codebase and documentation questions (auto-Guru)** and `docs/agents/guru.md`.

## Trigger

Use this skill for **code** and **documentation** Q&A. Skip when the user is running a wave lifecycle shortcut from `docs/prompts/index.md`.

## Instructions

1. Read `AGENTS.md` § **Codebase and documentation questions (auto-Guru)**.
2. Read and follow `docs/agents/guru.md` (classification, retrieval loop, Pass 3, citations).
3. Attach the `wavefoundry` MCP server via your host's project-local registration (see the `AGENTS.md` MCP table; Codex loads it automatically from the committed `.codex/config.toml`).
4. Prefer **`code_ask`** and **`docs_search`** over ad-hoc search when MCP is available.
5. Complete Pass 3 validation before answering; never paraphrase only the `code_ask` `answer` field.

## Notes

- Operators do not need to say **Guru**; this skill is the default path for code/doc questions.
- Explicit shortcut **Guru** remains in `docs/prompts/index.md`.
