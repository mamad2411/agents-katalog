---
name: agent-contract
description: Write, refresh, or audit a repo's CLAUDE.md onboarding contract so future sessions start from it instead of re-exploring. Use when a repo has no CLAUDE.md and will be worked in again, when asked to update or check it, when its paths or commands have gone stale, and after any change to layout, commands, or conventions. Runs scripts/verify_claude_md.py.
---

# agent-contract

A good `CLAUDE.md` pays back more tokens than anything else in a repo. It is read once per session and replaces the exploration that would otherwise happen every session. A stale one is worse than none, because it is trusted and wrong.

## Auditing an existing file

```bash
python <skill>/scripts/verify_claude_md.py
```

It reports dead path references, commands that no longer exist in `package.json` or the `Makefile`, how far the freshness date has drifted from the last commit, and whether the file has outgrown its ceiling. Fix what it finds before trusting anything else in the file.

Flags: `--max-lines N` to change the ceiling (default 200), `--file PATH` for a non-standard location, `--json`.

## Writing a new one

Start from [repo-scout](../repo-scout/SKILL.md), whose map is most of the input:

```bash
python <skill>/../repo-scout/scripts/repo_scout.py
```

Then follow the section order in [references/format.md](references/format.md). Read that file when writing or restructuring, not for a small edit.

The short version of the format:

1. One-line purpose and a `Last verified` date.
2. What the project is, in two or three paragraphs, including the framing that is not derivable from the code.
3. A vocabulary table, when the domain has terms a newcomer would guess wrong.
4. An architecture map: the tree, annotated inline, only to the depth that matters.
5. What is authoritative versus archived, when the repo has superseded generations.
6. Conventions, meaning the rules a session would otherwise violate.
7. Commands.
8. Gotchas.

## The ceiling is the point

Every line costs tokens in every future session. Target under 200 lines.

When a section grows past that, it belongs in `docs/`, and `CLAUDE.md` keeps a one-line pointer. Deep methodology, deploy steps, and API detail are the usual candidates. The contract's job is to route, not to contain.

A section that only restates the file tree is not earning its lines, `repo-scout` regenerates that on demand for free.

## What actually belongs in it

Write what a session cannot derive by reading the code:

- Why the architecture is the way it is, and which parts are load-bearing.
- Decisions already made and rejected, so they do not get re-litigated.
- Rules with consequences: what must never be edited, what must stay in sync.
- Which directory is current when several look plausible.

Do not write API documentation, function-by-function descriptions, or a changelog. Those go stale fastest and the code is authoritative.

## Refreshing

Update the affected section, do not rewrite the file. Bump the `Last verified` date only when you have actually checked the claims, not merely edited nearby text. A date that lies is the failure mode this whole file exists to prevent.

Prose follows [prose-guard's rules](../prose-guard/references/rules.md).
