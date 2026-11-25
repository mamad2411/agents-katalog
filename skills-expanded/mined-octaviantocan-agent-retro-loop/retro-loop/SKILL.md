---
name: retro-loop
description: "Retrospective loop for AI agents. Gathers recent session logs, extracts behavior-changing lessons, checks them against existing memory and skills, writes a review buffer, then applies safe non-conflicting memory or skill updates while asking before conflicts or risky changes."
version: 2026-04-30
triggers: ["retro", "retrospective", "lessons learned", "what did we learn", "self-improve", "review the last few hours"]
tools: [bash, read, write, edit, grep]
category: meta
---

# Retro Loop

Retro Loop turns recent agent sessions into durable behavior changes.

The core pattern is simple:

1. Gather recent session logs.
2. Extract concrete lessons from mistakes, corrections, surprises, and useful techniques.
3. Confront each lesson against existing memory, preferences, and skills.
4. Write a buffer with sources, confidence, and proposed changes.
5. Auto-apply safe non-conflicting updates.
6. Ask before conflicts, destructive changes, external actions, privacy-sensitive edits, or policy changes.

The important part is step 3. Most agents can summarize what happened. Fewer agents check whether the lesson is new, redundant, contradictory, or already encoded somewhere else.

## Inputs

- `--hours N`: session window. Default `4`.
- `--agents <csv>`: agent/session directories to inspect. Default depends on your installation.
- `--out <path>`: buffer file. Default `memory/working/RETRO_<UTC>.md`.
- `--review-only`: write the buffer but do not apply durable edits.
- `--ask`: ask before applying new or extending edits.

## Pipeline

### 1. Gather

Run `scripts/gather.sh <hours> <agents>` or your platform equivalent.

The gather step should return session transcript paths modified within the chosen window. Exclude low-level trajectory logs unless you need tool detail.

### 2. Read

Read the relevant turns from each transcript:

- user corrections
- assistant mistakes
- failed tool calls
- changes of plan
- successful patterns worth repeating
- preferences the human stated or implied

Avoid raw transcript dumping. Sample for signal.

### 3. Extract

For each candidate lesson, write:

- Lesson: one behavior-changing sentence.
- Source: session path or id plus rough turn/time.
- Category: mistake-correction, new-technique, preference-uncovered, tool-pattern, scope-failure, or communication-pattern.
- Confidence: solid, shaky, or one-shot.

Bias toward fewer, sharper lessons. Do not invent lessons to make the retro feel productive.

### 4. Confront

Search existing durable context before writing anything:

- semantic lessons
- user preferences
- topic/project/person memory files
- existing skills
- local operating instructions

Classify each lesson:

- NEW: no overlap.
- EXTENDS: refines an existing rule.
- CONFLICTS: contradicts an existing rule.
- REDUNDANT: already captured.

Conflicts are the point where the agent must slow down. Show both sides and ask for a decision.

### 5. Write the buffer

Use this shape:

```markdown
# Retro: <UTC timestamp>
Window: last <N>h. Sessions: <count>. Agents: <list>.

## Lessons
1. <lesson> [<category>, <confidence>]
   - Source: <session id/path> around <time/turn>
   - Status: NEW | EXTENDS <file:section> | CONFLICTS <file:section> | REDUNDANT
   - For EXTENDS: proposed merged text
   - For CONFLICTS: existing vs new, recommended winner, reason

## Skill changes proposed
- New skill: <name>, <why>
- Update skill: <name>, <what changes>
- None, because <reason>

## Memory file updates proposed
- <path>: <what to add/change>

## Open questions
- ...
```

### 6. Apply or ask

Default behavior:

- Auto-apply NEW and EXTENDS lessons, memory edits, and skill edits that are safe, non-destructive, and non-conflicting.
- Ask first for CONFLICTS, destructive changes, external actions, privacy-sensitive edits, or operating-policy changes.
- Use review-only mode when the human asks to inspect before applying.

### 7. Log the retro

Append a short line to the daily log or equivalent:

```markdown
- retro <UTC time>: <N> sessions reviewed, <M> lessons applied, skills changed: <list or none>
```

## Thorough mode

Use thorough mode for full-day retros or when the normal retro misses too much.

Required inputs:

- daily note or equivalent session digest
- recent session logs
- relevant long-term memory files
- relevant skills or operating rules

Required output:

- day shape
- concrete lessons with source and status
- mistakes and corrections
- open loops
- skill changes
- memory changes
- blockers or conflicts

A prose summary is not enough. The retro is not done until the buffer exists and safe applicable edits are applied or explicitly blocked.

## Safety gates

Never auto-apply:

- conflicting lessons
- destructive file operations
- external actions visible to other people
- private or sensitive data movement
- identity, safety, or red-line policy changes
- broad permission changes

## Adaptation notes

This skill assumes your agent has some form of:

- session transcripts
- durable memory files
- reusable skills or instruction files
- a place to write working buffers

If your platform uses different names, keep the loop and replace the paths.
