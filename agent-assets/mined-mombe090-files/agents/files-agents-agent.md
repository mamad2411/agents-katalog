# Pi Global Agent Instructions

This file is loaded by Pi at startup for all sessions.

## Available Agent Personas

Agent persona files live in `~/.pi/agent/agents/`. Load them on demand when the user
invokes a persona or when the task clearly matches one:

- **REVIEWER** — Tech lead code reviewer (read-only PR review). Load `~/.pi/agent/agents/REVIEWER.md`.
- **FLUXCD** — Flux CD GitOps specialist. Load `~/.pi/agent/agents/FLUXCD.md`.
- **BEASTMODE3.1** — Full-capability engineering mode. Load `~/.pi/agent/agents/BEASTMODE3.1.md`.

## Skills

Skills are discovered from `~/.pi/agent/skills/`. Use `/skill:<name>` to load one explicitly,
or let Pi load them automatically when a task matches. Each skill wrapper references the
canonical body in `~/.skills/<name>/SKILL.md`.

## General Principles

- Prefer editing existing files over creating new ones.
- Use tools available in context; avoid unnecessary tool calls.
- Be concise and direct. No unnecessary filler or praise.
