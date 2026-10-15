---
name: discoveries-writing
description: Write and maintain DISCOVERIES.md files for agents. Use when creating a new DISCOVERIES.md, adding hard-won repo-specific findings, or reviewing whether a note belongs in agent memory instead of a changelog or TODO list.
license: MIT
metadata:
  author: kjanat
  version: "1.0"
---

# Discoveries Writing

Write `DISCOVERIES.md` as an agent memory file: a compact record of
non-obvious gotchas, surprising behaviors, and lessons that are expensive to
rediscover.

## Core Rule

Every entry should answer this question:

> "What would save the next agent from wasting time or making the same wrong
> assumption?"

If the answer is "not much", it does not belong in `DISCOVERIES.md`.

## What Belongs

- Repo-specific gotchas that are not obvious from reading the code
- Tooling quirks, parser/compiler/editor oddities, and integration traps
- Counterintuitive framework behavior discovered during debugging
- Hard constraints that look accidental until proven otherwise
- Proven fix patterns that resolve a recurring confusing failure mode

## What Does Not Belong

- Ordinary implementation progress notes
- Release summaries better suited for `CHANGELOG.md`
- TODOs, wishes, or speculative ideas
- Facts already obvious from code, tests, types, or official docs
- Long design docs or postmortems that belong elsewhere

## File Conventions

- File name: `DISCOVERIES.md` at repo root
- If `AGENTS.md` or `CLAUDE.md` exists, ensure it references `@DISCOVERIES.md`;
  add the reference if it is missing
- Audience: agents first, humans second
- Default heading: `# Discoveries`
- Organize by domain with `##` sections such as `Build & Tooling`,
  `Testing`, `Architecture`, or project-specific areas
- Use short bullets for simple findings; use short subsections when the lesson
  needs symptom/cause/fix context

## Entry Quality Bar

Keep entries:

- specific: name the exact behavior, tool, layer, or trigger
- surprising: capture what was unintuitive or misleading
- actionable: include the fix, workaround, or correct mental model
- durable: prefer truths likely to remain useful after the current task
- concise: enough context to prevent repeat debugging, no diary-style prose

## Writing Pattern

For most entries, use this shape:

```markdown
- Problem or surprising behavior. Cause or implication. Fix or takeaway.
```

When a single bullet is too compressed, expand to:

```markdown
### Topic

- Symptom: what failed or looked wrong
- Cause: what was actually happening
- Fix: what resolved it
- Scope: when this matters
```

## Section Strategy

- Prefer stable domain sections over dated chronology
- Add new sections only when multiple findings justify them
- Keep empty placeholder sections only if the repo already uses that pattern
- For one-off migrations or major upgrade notes, a dated or named section is
  acceptable if the cluster is coherent and likely to stay useful

## Style

- Write in direct technical prose
- Prefer concrete names over abstractions
- State the wrong assumption when that is the real trap
- Mention exact commands, file paths, versions, or node names only when they
  are part of the discovery
- Keep code snippets short and only when they clarify the fix

## Anti-Patterns

| Don't                                                | Why                                               |
| ---------------------------------------------------- | ------------------------------------------------- |
| Dump a debugging transcript                          | Too noisy; future agents need the conclusion      |
| Record every change made                             | That's changelog material, not discovery material |
| Keep stale discoveries after the code changed        | False lore is worse than missing lore             |
| Add generic best practices                           | The file should store repo-earned knowledge       |
| Overfit a note to one temporary branch or experiment | Future agents cannot trust it                     |

## Maintenance

- Add entries after resolving a confusing bug, failed assumption, or hidden
  constraint
- Update or delete entries when they stop being true
- Merge duplicate notes into one stronger statement
- Prefer editing an existing section over appending a new top-level heading

## Reading Order

| Task                          | Files to Read                                        |
| ----------------------------- | ---------------------------------------------------- |
| Create a new `DISCOVERIES.md` | `SKILL.md` + `references/example.md`                 |
| Add a new finding             | `SKILL.md`                                           |
| Review whether a note belongs | `SKILL.md` (`What Belongs` / `What Does Not Belong`) |
| Copy the house style          | `references/example.md`                              |

## In This Reference

| File                                | Purpose                               |
| ----------------------------------- | ------------------------------------- |
| [example.md](references/example.md) | Canonical template and entry examples |
