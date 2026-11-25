---
name: learn-from-lessons
description: Lessons this person's past agent sessions taught — principles, rules and project facts, each linked to the transcript turns it came from. Use before a risky or recurring step (pushing, PRs, deploys, spending API credit, writing paper prose, reporting results), when starting in a project you have not seen this session, or right after the person corrects you. Also when they ask about "lessons", "dream", or memory from past sessions.
---

# learn-from-lessons

Lessons are **predictions** from this person's own transcripts: "in this situation, doing X avoids a correction".
Follow them unless the person says otherwise now; if they conflict, the person wins — mention it in one line.

Levels: `principle` (few, always apply) → `rule` (one situation) → `instance` (one project or tool).
Each lesson lists `scenarios` (`writing-paper`, `coding`, `release-deploy`, `cost-resources`, `reporting`, …) and a
`strength` (`must` = the person once stopped or reverted an agent over it).

## Always

Principles are in the injected index (between `learn-from-lessons` markers in CLAUDE.md/AGENTS.md); keep them in mind.

## Before a risky or recurring step

Search with the current scenario — before pushing or opening a PR, spending credit or launching paid runs, writing
paper prose, and reporting results:

```bash
lessons search "<what you are about to do>" --cwd --context "<the person's request>"   # infers the scenario
lessons search "<...>" --cwd --scenario release-deploy --level instance                # explicit; adds project facts
```

Open a hit's file and follow its **Do**. `--all` also shows unverified candidates — treat those as hints.
MCP equivalents: `search_lessons`, `get_lesson`, `list_principles`, `infer_scenario`.

## After

- A lesson should have covered a correction, or proved wrong: say so in one line.
- No lessons yet, or a week of new sessions: suggest `lessons dream` (it calls a model — ask first), then
  `lessons inject --target CLAUDE.md --scenario <s>` (a diff; `--apply` writes it).

Do not edit lesson files from inside a task, and never copy secrets into one.
