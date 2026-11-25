---
name: intent
description: >-
  Captures an idea as an intent before any story: brainstorms with whoever has it until it
  is concrete (problem, outcome, constraints), then writes
  docs/architecture/intents/<slug>.md for the product owner. Run with /ddd-ts-kit:intent.
argument-hint: "[the idea in plain words, or nothing to be asked]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - AskUserQuestion
  - Bash(npx ddd-ts-kit list)
  - Bash(npx ddd-ts-kit list *)
  - Bash(git *)
  - Bash(gh pr create *)
---

# Capture an intent

Idea: `$ARGUMENTS`

You help the person who has the idea write it down in their own words, before anyone designs
anything. You decide nothing about the solution: an intent says what is wrong, what would be
true once it is solved, and how its author would see it. Reading costs:
[../start/token-economy.md](../start/token-economy.md). It runs from Claude Code, Cowork or
claude.ai with a git connector; the template is also filled by hand.

## 1. Make the idea concrete

Ask what an analyst would ask, a few questions at a time, with AskUserQuestion where the host
can ask (Claude Code, Cowork, claude.ai); where it cannot, list them under `## Open questions`
and go on with what the idea says:

- the problem: who meets it, when, how it shows today, what it costs;
- the outcome: what the author would see once it is solved, never how to build it;
- the people and systems: who uses it, which part of the product, which outside system;
- the constraints: a rule of the business, a regulation, a deadline, a system that cannot change;
- the acceptance: one line per outcome the author could observe for themselves.

Stop when each section can be written in two or three sentences the author recognises as
theirs. A solution the author offers is written as a constraint or an open question, never as
the outcome.

## 2. Map the systems

Inside a bootstrapped project (a `ddd-ts-kit.config.json` is here), `npx ddd-ts-kit list` names
the bounded contexts: write under `## Affected users and systems` those the idea touches, by
those names, and say when it touches none (a new context is a strategic decision of the owner,
taken in the story or in `docs/architecture/plan.md`, never here). Outside the project, write
the systems as the author names them.

## 3. Write it, then hand it to the owner

Copy [../story/intent-template.md](../story/intent-template.md) to
`docs/architecture/intents/<slug>.md` (the slug from the title, lower case, hyphens), fill every
section, `Author: <name> (<role>). Status: draft.` in the header. Commit it on a branch and open
a pull request where you can (`git`, `gh pr create`, or the connector of the host); otherwise
give the file to whoever does. Tell the author: the product owner corrects it in that pull
request and accepts it by setting `Status: accepted`; the merge is the acceptance; the next step
is then `/ddd-ts-kit:story <code> docs/architecture/intents/<slug>.md`, which seeds the story
from the intent (`story-scope --from` refuses an intent that is not accepted).

## What an intent is not

Not a backlog, not a ticket: a project whose tracker is the source of truth writes the key of
the ticket in the intent and the path of the intent in the ticket, and `## Origin` of the story
carries both. Not a design: the contexts, the aggregates and the routes are the story's.
