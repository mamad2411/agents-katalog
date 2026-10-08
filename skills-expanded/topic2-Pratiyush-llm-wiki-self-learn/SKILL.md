---
name: self-learn
description: Extract reusable patterns from recent sessions, propose framework improvements, and (with approval) update the framework docs. This is the dogfooding meta-loop — the project learns from its own usage. Use when the user says "learn from this", "what did we learn", "extract lessons", "update the framework", "add this to steering rules", or after completing any substantial feature or debugging session.
---

# self-learn

## What this skill does

Closes the **Dogfooding Meta-Loop** from the Open Source Framework v4.1.

Every non-trivial session on a framework-driven project produces lessons: patterns that worked, patterns that failed, gotchas hit, decisions made. Most tools let those lessons evaporate. This skill captures them, runs a quality gate, and proposes framework updates.

**It is the reason the framework evolves.** Framework v4.0 → v4.1 was a `self-learn` pass that folded llmwiki's learnings back into the parent Open Source Framework.

## When to invoke

- User says "learn from this session", "what did we learn", "extract lessons", "distill this"
- After a substantial feature ships (especially if it required multiple debugging loops)
- At the end of a project phase — before moving to the next phase
- When the user fixes a bug that was caused by a missing framework rule
- When the user finds a pattern that should apply across projects
- At the end of a "monthly verification" pass (Phase 8 Maintain)

Do NOT invoke when:

- The session is trivial (single file change, typo fix)
- The session is still in progress (wait until the user says "done")
- The learnings are obvious or already codified in the framework

## Workflow

1. **Gather context.** Read:
   - The recent session transcript (`raw/sessions/<project>/<latest>.md` or Obsidian session notes)
   - `_progress.md` to know the current phase
   - `tasks.md` to see what shipped
   - `docs/framework.md` to know the current framework state
   - `CHANGELOG.md` for what's already been logged

2. **Extract candidate lessons.** Look for:
   - **Failed attempts** — "X didn't work because Y" → candidate rule
   - **Surprising wins** — "X worked and I wouldn't have guessed" → candidate pattern
   - **Repeated debugging loops** — "I hit X three times this week" → candidate hard rule
   - **Decisions** — "I chose X over Y because Z" → candidate Project Type addition
   - **Hints the user gave** — "we need to always do X" → candidate steering rule
   - **Gaps in the roadmap** — items discovered during execution that weren't in the plan

3. **Score each candidate** on two axes:
   - **Generality**: does this apply only to this project, or to any project of this type, or to all projects? (project → type → framework)
   - **Confidence**: how many data points? (1 occurrence = anecdote, 2 = pattern, 3+ = rule)

4. **Propose updates** grouped by destination:

   | Destination | When to update it |
   |---|---|
   | `.kiro/steering/<rule>.md` (project-specific) | 2+ data points in this one project |
   | `docs/framework.md` in the project repo | Learning applies to all projects of this type |
   | `.framework/Framework.md` (personal Obsidian copy) | Cross-cutting rule that applies to all open-source projects |
   | `CHANGELOG.md` | Every update gets logged as framework version bump |
   | New skill under `.claude/skills/` | Repeatable workflow that warrants its own invocation |
   | New phase in the pipeline | If the learning is about a missing step |

5. **Show the diff to the user before applying anything.**

6. **With approval, apply the changes:**
   - Write the new steering rule / framework section / skill
   - Bump the framework version (e.g. v4.1 → v4.2) if the update is non-trivial
   - Update `CHANGELOG.md` with a `## vX.Y` entry describing what was learned
   - Append a one-line note to `_progress.md` in the Learning Log section

7. **Report** what changed, with line counts and a list of destination files.

## Output format

```
## Self-learn report: <project> / <date>

### Sources consulted
- <file 1>
- <file 2>

### Candidate lessons (scored)

| # | Lesson | Generality | Confidence | Destination |
|---|---|---|---|---|
| 1 | <lesson> | project \| type \| framework | 1 \| 2 \| 3+ | <file> |
| 2 | ... | ... | ... | ... |

### Proposed updates

**1. .kiro/steering/page-format.md — add rule**
```diff
+ ## New rule from self-learn
+ <content>
```

**2. docs/framework.md — new section under Phase 5.5**
```diff
+ ### New QA check from self-learn
+ <content>
```

### Approval needed

Apply all proposed updates? (y/n)
```

## Hard rules

1. **Never update the framework silently.** Always surface the diff and ask.
2. **Never invent a learning from one data point.** If confidence is 1, mark it as a draft and wait for a second occurrence.
3. **Respect the framework hierarchy.** Project → Type → Framework. Don't promote a project-specific learning to a cross-cutting rule without 3+ data points across projects.
4. **Version-bump the framework** (e.g. v4.1 → v4.2) on any update to `docs/framework.md`. Update `CHANGELOG.md` in sync.
5. **Never touch code** as part of self-learn. This skill only touches docs, steering files, and framework versioning. Code changes go through the normal PR flow.
6. **Dogfood itself.** Self-learn should produce a session transcript that future self-learn passes can read.

## Example outcomes (from llmwiki's own history)

- Framework v4.0 → v4.1: added **Phase 1.25 Research** after discovering that cloning 15 reference repos up-front prevented 3+ hours of rework during Phase 3 Structure.
- Added **`.llmwikiignore`** rule after hitting sessions containing contract data that shouldn't enter the wiki.
- Added **live-session detection** (`<60 min`) after the converter read a file mid-write and produced a truncated markdown.
- Added **"no AI co-authored-by"** rule to `.kiro/steering/contributing-rules.md` after a first-run slip.

Each of these started as a single session observation and got promoted to a framework rule after the second or third occurrence.

## Related skills

- `project-maintainer` — runs the phase gates that surface the "we hit this 3 times" patterns.
- `llmwiki-query` — to look back at past sessions and count occurrences of a pattern.
- `llmwiki-sync` — to make sure the latest session is available before running self-learn.
