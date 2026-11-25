---
name: senior-project-intelligence
description: Use when asked to set up or refresh the project memory in `.senior/`, after a material architecture or stack change, or when sessions keep rediscovering the same project facts. Not for small local edits that can be done from the files at hand.
---

# Project Intelligence

**Core rule:** store only facts that will save a future session from a mistake.

## Process

1. Read repository-level instructions.
2. If available, run `senior inspect` for deterministic stack facts.
3. Read only the entry points needed to understand architecture boundaries.
4. Separate durable facts from transient implementation details.
5. Run `senior init` to create `.senior/` when it does not exist yet.
6. Record a decision in `.senior/decisions.md` only when it constrains future work, dated and in one or two lines.

## Good durable facts

- language, framework, package manager;
- database/ORM and auth provider;
- deployment target and service boundaries;
- the canonical verification commands;
- conventions that are easy to violate;
- decisions such as "use Drizzle; do not introduce Prisma".

## Do not store

- secrets, credentials or personal data;
- raw conversation transcripts;
- temporary debugging hypotheses;
- large file inventories;
- facts that are obvious from one local file, unless they keep causing mistakes;
- volatile data that `senior inspect` can re-detect.

| If you notice yourself thinking… | Do this instead |
|---|---|
| "Let me map the whole repository first" for a local change | Read the files the task touches |
| "This might be useful someday" | Store it only if a future mistake depends on it |
| "I'll paste the env file so the next session has it" | Never; reference where configuration lives instead |

## Verification

Before finishing, confirm the stored context is accurate against the current repository, concise, free of secrets, and useful across sessions.
