---
name: daily-summary
description: End-of-day summary of what I did with the career-agent tool. Auto-generates a record of artifacts created/modified, open loops, patterns across the day, and concrete next steps, then asks me to add anything missed. Saves to $PERSONAL/career/daily-log/YYYY-MM-DD.md. Use when I say "wrap up the day", "summarize today", "EOD summary", or similar end-of-session prompts.
---

# Daily Summary

## When to use
At end of day, when the user wants a record of what happened in this tool and what's still open. Trigger phrases: "wrap up the day", "summarize today", "EOD", "end of day".

For morning briefings on yesterday's carryover, use `morning` instead.

## What it produces
A markdown file at `$PERSONAL/career/daily-log/YYYY-MM-DD.md` (today's date, ISO format) with the sections below. `$PERSONAL` is the personal-docs sibling directory defined in `CLAUDE.md`; resolve it once at the start of the session. **Omit any section that has nothing real to report** — don't fill with placeholder text or generic advice.

### Section 1: What I did
Artifact-level log of today's activity. Detect by:
- Scanning `$PERSONAL/applications/` for files with mtime = today
- Reading the conversation transcript for skill invocations and concrete decisions
- Checking for new/modified entries in `$PERSONAL/career/coding-log.md`, `$PERSONAL/career/story-bank.json`, etc.

Examples:
- "Analyzed Stripe Staff Payments Job Description → `$PERSONAL/applications/stripe/staff-payments/role.md`"
- "Generated tailored resume for Anthropic MTS role → `$PERSONAL/applications/anthropic/mts/resume.pdf`"
- "Mock interview (Google E5 style, 45 min) — verdict: lean hire, weak on graphs"
- "Practiced 3 sliding-window problems — struggled on minimum-window-substring"

Each bullet should reference a concrete file path or specific outcome, not a vague "we discussed X."

### Section 2: Open loops
Work started today (or earlier) that isn't finished. Detect by (all paths under `$PERSONAL`):
- `role.md` exists with no `resume.md` next to it → tailored resume not yet built
- Mock interview happened but no follow-up practice on noted weak areas
- A role analyzed but no decision recorded ("save", "skip", "stretch")
- TODO-style notes in `role.md` files

Cite the specific file each open loop refers to.

### Section 3: Patterns from today
**Include this section only if ≥2 similar activities happened today.** Look for cross-cutting signal:
- Recurring required skills across multiple Job Descriptions ("3 of 3 Job Descriptions flagged distributed systems depth")
- Recurring weakness across problems ("hesitated on 2 graph traversal problems")
- Comp range observations across postings

If only 1 activity happened, **skip this section entirely**. Forced patterns from a sample of 1 are noise.

### Section 4: Next steps
Concrete actions, each tied to a specific artifact or upcoming event. NOT vague career advice.

Good examples:
- "Build tailored resume for Stripe Staff ($PERSONAL/applications/stripe/staff-payments/)"
- "Practice 2 medium graph problems before Friday's Anthropic onsite"
- "Add 'conflict with stakeholder' STAR story — gap revealed in today's mock"

Bad examples (don't write these):
- "Keep applying"
- "Stay focused on practice"
- "Review your resume"

## Workflow

1. **Auto-generate** the summary from file mtimes and the conversation transcript. Don't ask the user any questions up front.
2. **Write** the file to `$PERSONAL/career/daily-log/YYYY-MM-DD.md`. If the file already exists (user invoked the skill twice today), append a `## Updated at HH:MM` block instead of overwriting — preserves the earlier record.
3. **Print** the full summary to the terminal so the user can review.
4. **Ask once at the end:** *"Anything I missed — decisions, recruiter calls, applications submitted outside Claude, or anything else worth recording?"* Append their freeform response under `## Additional notes`. If they say no, skip and finish.

## File format

```markdown
---
date: 2026-05-11
artifacts_created: 2
artifacts_modified: 1
---

## What I did
- ...

## Open loops
- ...

## Patterns from today
(only if ≥2 similar activities)

## Next steps
- ...

## Additional notes
(only if user added context after the prompt)
```

## Anti-patterns

- **Don't motivate or cheerlead.** No "great progress today", no productivity scores. CLAUDE.md is clear: no padding.
- **Don't turn this into an application tracker.** Pipeline state (stages, dates applied, outcomes) is tracked optionally on each `role.md`. Daily summaries reflect what happened today, not pipeline state.
- **Don't fake precision.** No "you spent 2 hours on coding" — that can't be measured reliably. No "you're 30% through your search" — meaningless.
- **Don't include sections with no real content.** If there are no open loops, omit the section. Empty sections are noise.
- **Don't dredge up old context.** Only today's activity + actionable open loops. Stale items belong in `morning`, not here.
