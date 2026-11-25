---
name: write-the-claude-md
description: Use when an agent keeps relearning the codebase from a blank page every session and getting it confidently wrong. Reach for it when a founder says "write my CLAUDE.md", "the agent forgot how our system works again", "it reinvents the structure every time", "set up the master file", "do I need AGENTS.md and a Cursor rules file too", "keep memory across sessions", "it broke a rule nobody told it", or starts a repo and wants every session to begin where the last one stopped. Produces a populated master file (and its AGENTS.md / GEMINI.md / Cursor mirrors) holding the system inventory, principles, constraints, and decisions, plus a one-line session-end update ritual. Run during architect-before-code, before agentic-build-loop.
stage: architect
function: system
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Write the CLAUDE.md

A clever prompt dies the instant the context window clears. The agent forgets, reconstructs a theory
of your system from whatever it can see, and builds against that improvised theory, slightly
differently every session, until one repository houses three half-systems that almost agree. The
master file is the cure. It is the memory the model does not have: the one document read at the top
of every session so the work starts where you left it, not from a guess. Write it before the first
feature, not after the first regression.

## The method

Author one master file, mirror it to every platform, and keep it alive with a session-end ritual.
Full anatomy, worked before-and-after, and anti-patterns: [`references/master-file-anatomy.md`](references/master-file-anatomy.md).

### Step 1: Write the seven sections, and nothing else

The file earns its keep by being short and current. Include the standing context an agent would
otherwise guess; exclude anything that lives better in code or goes stale by Friday.

| Section | What it holds | Keep out |
|---------|---------------|----------|
| What this is | One paragraph: the product and its one closed loop. | Marketing copy. |
| System inventory | The four pillars named: Brain, Memory, Planning, Tools. | API keys, secrets. |
| Principles | The non-negotiable rules of this codebase. | Generic best practice the model already knows. |
| Constraints | The limits a newcomer would break by accident. | Anything enforced by a linter or test. |
| Decisions | Dated trade-offs made and why, newest first. | Decisions already reversed; prune them. |
| Glossary pointers | Links to the domain terms, not the definitions. | Full definitions that drift from source. |
| Update ritual | The one-line rule for keeping this file alive. | A changelog of every commit. |

### Step 2: Mirror it across every platform you use

The same source serves four runtimes. A rule in only one file is a rule the other three agents break.

| Platform | File it reads |
|----------|---------------|
| Claude Code | `CLAUDE.md` |
| Codex | `AGENTS.md` |
| Cursor | `.cursor/rules/<name>.mdc` |
| Gemini CLI | `GEMINI.md` |

Write the content once. Mirror the mirrors so they never disagree; a contradiction between them is
worse than no file, because each agent obeys a different one.

### Step 3: Install the session-end update ritual

At the end of every working session, add exactly one line naming the trade-off you just made. Not a
diff, not a diary. One decision, dated. This is the discipline that keeps the file true; without it,
the file rots into a confident, stale lie that misleads every session after.

## Output

- A populated **master file** (`CLAUDE.md`) with the seven sections filled for the founder's repo.
- The **platform mirrors** (`AGENTS.md`, `GEMINI.md`, `.cursor/rules/<name>.mdc`) carrying the same content.
- A documented **session-end update ritual**: one dated line per session, naming the trade-off made.
- Next: run `agentic-build-loop` to generate against the master file, never a blank page.

## Constraints

- A stale file is worse than none. Forbid shipping the file without the update ritual that keeps it true.
- Do not dump everything. The file is the standing context, not a changelog; anything a linter or test enforces does not belong here.
- Treat a model bump or prompt edit as load-bearing (CACE): if it changes behaviour, it earns a line in Decisions, not a silent commit.
- Stay theme-agnostic; the founder supplies the domain, you supply the structure.

## Dictionary

[context window](../../dictionary/02-context-and-sessions.md#context-window) ·
[CACE](../../dictionary/05-failure-modes.md#cace-changing-anything-changes-everything)

## Copy-paste version

> For non-coders: paste into any chatbot or no-code builder (Claude.ai, ChatGPT, Lovable, Bolt, v0).

```
Act as my lead systems engineer. Write the master memory file for my repo so every AI session starts
where the last one stopped instead of reinventing my codebase.
My product: [ONE_LINER]. Domain: [DOMAIN]. My closed loop: [INTELLIGENCE_LOOP].

Draft a CLAUDE.md with exactly these seven sections, short and current:
1. What this is: the product and its one closed loop, one paragraph.
2. System inventory: name the four pillars (Brain, Memory, Planning, Tools) for my product.
3. Principles: the non-negotiable rules of this codebase.
4. Constraints: the limits a newcomer would break by accident, including [CONSTRAINT] and [GUARDRAIL].
5. Decisions: dated trade-offs, newest first (seed it with today's).
6. Glossary pointers: the domain terms to link, not define.
7. Update ritual: the one-line rule for keeping this file alive.

Then produce the same content as mirrors named AGENTS.md, GEMINI.md, and .cursor/rules/project.mdc,
so Codex, Gemini, and Cursor obey the same rules. Keep them identical.

CONSTRAINTS: do not dump a changelog or anything a linter enforces; keep it the standing context only.
Treat any model or prompt change that alters behaviour as a Decisions entry, not a silent edit.

OUTPUT: the filled CLAUDE.md, the three mirrors, and a one-line session-end ritual I run every time.
```
