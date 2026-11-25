---
name: checkpoint-handoff
description: "Use before a context boundary on multi-session work — a compaction, the end of a long session, a handoff to another agent. Writes the resume state to a durable file: what's done, what's in flight, the ordered remaining tasks, the standing constraints verbatim, and the files to re-read first, so a cold session can continue without asking."
---

# Checkpoint Handoff

## The failure mode this fixes

Long projects outlive context windows. The session that planned the work is never the session that finishes it — compaction, restarts, and tomorrow all guarantee that. And when the boundary hits without preparation, the next session starts by *reconstructing* instead of working: re-deriving the plan, re-discovering which tasks were done, re-learning the constraint the user stated forcefully forty turns ago, and — worst — confidently redoing or undoing finished work because nothing recorded that it was finished.

Conversation memory is the wrong place for project state. Summaries compress; the exact rule ("never X, always Y"), the precise task ordering, and the "we already tried that, it fails because Z" knowledge are exactly what compression loses. The fix is mechanical: before the boundary, the state gets written to durable files, structured for a cold reader.

## When to Use This Skill

- The user says they're about to compact, or you notice the context getting heavy mid-project
- A session is ending with the project unfinished (i.e., almost every session of a real project)
- Work is being handed to another agent, a fresh session, or a parallel worker
- A phased plan is mid-flight — some tasks done, some in progress, some queued
- You were just asked "where were we?" — the skill fired one session too late

**Don't use when:** the task is single-session and will finish here; a checkpoint of a finished task is just a report. Don't checkpoint into the conversation itself — a summary message that will be compacted along with everything else is not a checkpoint.

## Instructions

### 1. Write to durable files, not to the chat

The checkpoint lives where compaction can't touch it: a working doc in the repo (`PLAN.md`, a project doc, whatever the project already uses), agent memory if available, a tracked task list. If a working doc already exists, *update it* — a trail of stale plan files is its own failure mode.

### 2. Record state as facts, not narrative

A cold reader needs ground truth, not the story: which tasks are **done** (with the evidence — suite green, run verified), what's **in flight** and exactly where it stopped, what's **queued** with explicit ordering and dependencies ("7B → 7D → 7C; 7C needs 7D's schema"). Convert every relative reference to absolute — "the bug from yesterday" is noise next week; name the file, the test, the commit.

### 3. Restate the standing constraints — verbatim, every time

Every project has rules that must survive every boundary: the invariants ("every number cited or derived"), the boundaries ("this feature mounts only under X, never Y"), the do-not-touch list, the user's explicit preferences. These are the highest-value, easiest-to-lose content in any summary. The checkpoint carries them word-for-word, even when "they were already written down last time" — the next session reads one doc, not an archaeology of five.

### 4. Point at the territory: files worth re-reading first

List the 3–7 files a fresh session should open before doing anything, with one line each on why. This converts an hour of cold exploration into two minutes of directed reading. Include the known traps: "tests in X fail pre-existing, not yours"; "the fixture's `year` field means duration, not calendar year."

### 5. Run the cold-reader test before declaring it done

Reread the checkpoint as someone with zero conversational memory. Can they tell what to do *first*? Would they redo anything that's finished? Would they violate a constraint that lives only in the chat? If any answer is wrong, the checkpoint isn't done. Then tell the user it's safe to compact.

## Output format

The working doc gets sections like:

```
## State as of <date>
Done (verified): <task — evidence>
In flight: <task — exact stopping point, next concrete action>
Queued: <ordered list with dependencies>

## Standing constraints (verbatim, survive every compaction)
- <rule 1> …

## Read first on resume
- <file> — <why / trap>

## Known failures & dead ends
- <thing already tried — why it doesn't work>
```

…then a one-line reply: "Checkpoint written to <file>. Safe to compact — next session starts at <task>."

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| The chat-summary checkpoint | a beautiful recap message that compaction eats along with everything else. |
| Narrative state | three paragraphs of journey, no task list a cold reader can execute. |
| Constraint decay | restating the plan but not the rules; the next session re-violates them within an hour. |
| Plan-file litter | a new `PLAN_v7_FINAL.md` per session instead of one living doc. |
| Checkpointing only at the end | by the time the context dies unexpectedly, it's too late; checkpoint at every natural boundary. |

## Mental Model

> Assume the next person to touch this work knows nothing you haven't written down — because that person is you, after compaction. The checkpoint is the only memory that survives; write it like the message in the lifeboat.
