---
name: session-compress
description: |
  Compress the current session into a dense, reloadable summary. Extracts key decisions,
  files modified, lessons learned, and open questions. Saves to ~/.claude/sessions/compressed/.
  Designed for loading at next session start to restore context without full transcript replay.
triggers:
  - /compress
  - /session-compress
  - compress session
  - save compressed session
---

# Session Compress

Compress the current conversation into a dense, structured summary that can be reloaded at the start of the next session to restore context without replaying the full transcript.

## Process

### 1. Review Full Conversation History

Scan the entire session from start to current message. Identify:

- Decisions made and the reasoning behind each
- Files created, modified, or deleted
- Approaches attempted (both successful and failed)
- Open questions, blockers, or unresolved issues
- The exact next step if work were to continue

### 2. Extract and Categorize

Organize findings into these categories:

**Decisions** -- What was decided and why. Include the alternatives considered and the rationale for the choice made. Each decision should be a single line that someone unfamiliar with the session could act on.

**Files** -- Every file touched during the session with its current status (created, modified, deleted, unchanged-but-referenced). Group by directory when there are many.

**Failed Approaches** -- What was tried and did not work, with a brief explanation of why it failed. This prevents the next session from repeating the same mistakes.

**Lessons** -- Anything learned during the session that should persist: gotchas, undocumented behavior, useful patterns discovered, corrections received from the user.

**Open Questions** -- Unresolved issues, decisions deferred, or blockers that need attention. Include enough context that the question makes sense without the full transcript.

**Next Step** -- The single most important action to take when work resumes. Be specific: not "continue working on X" but "implement the validation logic in src/validators/input.ts using the schema defined in step 3."

### 3. Compress to Structured Markdown

Write the summary using this template. Aim for less than 2000 tokens total. Be dense -- every word should carry information.

```markdown
# Session Summary — {YYYY-MM-DD HH:mm}

## Context
{One sentence: what was the goal of this session}

## Decisions
- {decision}: {reasoning}

## Files Touched
- `{path}` — {created|modified|deleted}: {what changed}

## Failed Approaches
- {approach}: {why it failed}

## Lessons
- {lesson}

## Open Questions
- {question}

## Next Step
{Specific next action}
```

### 4. Save the Compressed Summary

Create the compressed sessions directory if it does not exist:

```bash
mkdir -p ~/.claude/sessions/compressed
```

Save the summary to `~/.claude/sessions/compressed-{YYYY-MM-DD-HHmm}.md` using the current date and time.

### 5. Display Summary Card

After saving, display a summary card to the user:

```
+------------------------------------------+
|  Session Compressed                      |
|                                          |
|  Decisions:      {n}                     |
|  Files touched:  {n}                     |
|  Failed paths:   {n}                     |
|  Lessons:        {n}                     |
|  Open questions: {n}                     |
|                                          |
|  Saved to: ~/.claude/sessions/           |
|    compressed-{YYYY-MM-DD-HHmm}.md      |
|                                          |
|  Load next session:                      |
|    "Resume from compressed session"      |
+------------------------------------------+
```

Use `cc_celebrate` to mark completion.

## Guidelines

- **Density over completeness.** A compressed summary that fits in 1500 tokens and captures the essential context is better than a 5000-token transcript replay.
- **Actionable over descriptive.** "Use Zod schema validation on the input endpoint" beats "We discussed validation approaches."
- **Decisions need reasoning.** "Chose SQLite over Postgres: single-user app, no concurrent writes needed" -- without the reasoning, the next session might revisit the decision.
- **Failed approaches are valuable.** They prevent wasted time in the next session. Always include why something failed, not just that it did.
- **Next step must be specific.** The person (or AI) loading this summary should be able to start working immediately without re-reading anything else.
