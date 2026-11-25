---
name: research-journal
description: Use when finishing a research work session, after making a significant methodological decision, after a failed experiment or unexpected result, before a phase transition, or when the user explicitly asks to log/memo/remember the session — appends a structured narrative entry to docs/eureka/journal/ capturing decisions, failures, surprises, blockers, and next-session starting points
---

# Research Journal

## Overview

Research happens on the scale of weeks, months, and years — not hours. When you come back to a project after a gap, the WHAT is often still in the files (commits, results, designs) but the WHY is almost always gone. Why did we exclude that cohort? Why did we pick this baseline? What did we try that didn't work?

This skill captures the WHY in structured narrative entries, one per session, stored in `docs/eureka/journal/YYYY-MM-DD.md`. It is the **writer** counterpart to `eureka:whats-next`'s reader role — `whats-next` scans the journal to figure out where you left off; `research-journal` is what puts information into the journal in the first place.

**Core principle:** Commits capture the WHAT. The journal captures the WHY. Both are needed.

## When to Use

**Trigger this skill when:**

1. **Explicit user request** — "기록해둬", "log this", "memo", "remember this", "세션 정리", "오늘 한 거 정리해줘"
2. **Session wind-down signals** — "이제 그만", "내일 계속", "나 갈게", "쉬어야겠다", "그만 할게", "wrap up"
3. **Post-decision moments** — The user made a significant methodological choice and discussed the rationale during the session
4. **Post-failure moments** — An experiment or analysis produced unexpected results, and `eureka:systematic-troubleshooting` found a root cause
5. **Pre-phase transitions** — About to invoke a different Eureka skill that moves the project to a new phase (e.g., `research-brainstorming` → `hypothesis-first`)

**Do NOT trigger this skill when:**

- The session was pure Q&A with no decisions or work done
- The user is mid-execution and needs to keep working
- The user has explicitly declined journaling earlier in the conversation
- Only routine commands were run with no insight gained
- The session duplicates something already logged today (check the existing file first)

## What This Skill Is Not

This skill is **not** a transcript generator. Do not dump the conversation into the journal. The journal is a deliberate, curated record of what mattered — not everything that happened.

This skill is also **not** a replacement for:

| Artifact | Captures |
|---|---|
| `experiment-log.md` | Structured experiment records (N, seed, metric, pass/fail) |
| `docs/eureka/designs/` | Static research designs at brainstorming time |
| `docs/eureka/registrations/` | Frozen pre-registered hypotheses |
| `docs/eureka/audits/` | Manuscript-time claim audits |
| Git commit messages | What files changed and why mechanically |
| **This skill (journal)** | **Narrative WHY, decisions mid-project, failures with reasons, blockers, continuity hints** |

Each artifact serves a distinct purpose. The journal is the narrative layer that the others don't capture.

## Checklist

You MUST complete these steps in order:

1. **Determine journal file path** — `docs/eureka/journal/YYYY-MM-DD.md` (today's date in the project's timezone; use the date given in session context)
2. **Check if the file already exists** — if yes, you will append; if no, you will create it
3. **Scan session context** — what decisions were made, what failed, what was surprising, what's blocking, what should happen next
4. **Verify the session is journal-worthy** — if nothing of substance happened, tell the user and do not write an empty entry
5. **Draft the entry** using the template at `docs/templates/research-journal-entry.md`
6. **Identify cross-project insights** — scan the draft for lessons that would apply to other projects
7. **Show the draft to the user** for approval or edits
8. **Write (or append) to the journal file** after the user approves
9. **Optionally suggest promoting cross-project insights to Claude Code auto-memory** (do not write directly)
10. **Report the path** and mention that `eureka:whats-next` will read this on next session

## Step 1: Determine the File Path

The journal file is always `docs/eureka/journal/YYYY-MM-DD.md` where `YYYY-MM-DD` is today's date.

- If `docs/eureka/journal/` does not exist, create it.
- If `docs/eureka/journal/YYYY-MM-DD.md` does not exist, you will create it with a top-level date header.
- If it already exists, you will append a new `## HH:MM session` block below existing entries.

Check the current date via session context — do not guess.

## Step 2: Scan Session Context

Before drafting, identify the following from this conversation and the project state:

| Category | What to look for |
|---|---|
| **Worked on** | Actual work performed — files edited, analyses run, commits made, discussions had |
| **Decisions** | Methodological choices with rationale — why this approach, what alternatives were considered |
| **Failed attempts** | Things tried that didn't work, with likely reasons and "what to avoid next time" |
| **Surprises** | Results or behaviors that contradicted expectations (signal for further investigation) |
| **Insights** | Meta-level lessons — reusable in future sessions or other projects |
| **Blockers** | What's preventing progress right now |
| **Next session starts with** | Concrete first action when returning — the single most important field |

If none of these apply (session was trivial), go to Step 3.

## Step 3: Verify Journal-Worthiness

If after scanning the session context you have:

- No decisions
- No failures
- No surprises  
- No blockers
- No new insights
- A trivial "Next session" (e.g., "continue working")

Then the session is **not journal-worthy**. Tell the user:

> "This session was routine — no decisions or new insights worth journaling. Skipping. Let me know when there's something to capture."

Do not write an empty entry. A journal full of "nothing happened" entries is noise.

## Step 4: Draft the Entry

Use the template at `docs/templates/research-journal-entry.md` as the structure. The required sections are:

- `Worked on` (even if brief)
- `Next session starts with` (even if brief)

All other sections are optional — omit them if the category had nothing in it.

**Content rules:**

- Be specific, not vague. "Tried per-subject normalization, r went from 0.42 to 0.58" beats "improved normalization."
- Capture rationale, not just facts. "Chose X because Y" beats "chose X."
- Reference files and commits by path/hash when relevant.
- Keep each bullet to 1–3 sentences.
- Target total length: 10–25 lines of content. Over 50 lines means you are dumping the conversation.

## Step 5: Identify Cross-Project Insights

Re-read the draft and ask: "Would this insight apply to a different project, in a different field?"

Examples of cross-project insights:

- "Subject-level splits matter when scans are correlated within subject" (generalizable)
- "StandardScaler fit before split is a common leakage source" (generalizable)
- "Multi-start L-BFGS-B is required when the objective has flat plateaus" (generalizable)

Examples that are NOT cross-project (project-specific):

- "In this cohort, N=47 was insufficient for 3-way ANOVA" (specific)
- "Our baseline Model A gave r=0.42" (specific)
- "The preprocessing pipeline v2.4.0 fixed the alignment bug" (specific)

If any cross-project insight exists, mark it for Step 8.

## Step 6: Show the Draft

Present the draft to the user in a code block and ask:

> "Here's the journal entry I'd write for this session. Anything to edit, add, or remove before I save it?"

Wait for approval. If the user requests changes, revise and re-show. Do not force-write.

## Step 7: Write to File

After the user approves:

- If the file does not exist, create it with:
  ```markdown
  # YYYY-MM-DD

  <entry>
  ```
- If the file exists, append `<entry>` after existing content, with a blank line separator.

Use the exact template structure for the entry.

## Step 8: Suggest auto-memory Promotion (Optional)

If you identified cross-project insights in Step 5:

> "The insight '[insight]' looks reusable across projects. Want me to also note this in Claude Code's memory so future sessions (in any project) remember it?"

If the user approves, that insight should be added to Claude Code's auto-memory system via the normal mechanism (not directly written by this skill — auto-memory is managed by Claude Code, and this skill only surfaces candidates).

If the user declines or there are no cross-project insights, skip this step silently.

## Step 9: Report and Hand Off

End with:

> "Logged to `docs/eureka/journal/YYYY-MM-DD.md`. Next session `eureka:whats-next` will read this and pick up from '[next session starts with field]'."

## Template Reference

See `docs/templates/research-journal-entry.md` for the full template. The structure:

```markdown
## [HH:MM] Session — [one-sentence summary]

### Worked on
- [actual work done]

### Decisions
- **[Decision]**: [rationale, alternatives, why rejected]

### Failed attempts
- **[What was tried]**: [outcome], [likely reason], [avoid next time]

### Surprises
- [Expected X, got Y, probable explanation Z]

### Insights
- [Cross-project lessons worth remembering]

### Blockers
- [What's preventing progress right now]

### Next session starts with
- [Concrete first action when returning]

### References
- [Files touched, commits, result files]
```

Omit sections that are empty. Keep it tight.

## What to Capture vs What to Skip

**CAPTURE** (high signal for future you):

- Why a specific design choice (especially non-obvious ones)
- What was tried and didn't work, with likely reason
- Results that contradicted expectations
- Parameter/hyperparameter rationales beyond defaults
- Mid-session pivots and their reasons
- "I almost did X but realized Y" near-misses
- Summaries of decisions from collaborator conversations

**SKIP** (noise):

- Full conversation transcripts
- Routine commands (`git commit`, `pytest`, etc.)
- Metric values — those go to `experiment-log.md`
- Hypothesis content — that goes to `docs/eureka/registrations/`
- New study designs — those go to `docs/eureka/designs/`
- Today's TODO list — that's Claude's todos, not research narrative

**The principle**: the journal captures the WHY that no other file captures.

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "Nothing interesting happened today" | Even one decision is worth capturing. Three months later, "why did I pick this baseline?" is a real question. |
| "I'll remember this" | You will not. Every researcher says this. Every researcher is wrong. |
| "The commit message captures it" | Commits capture WHAT changed. The journal captures WHY. |
| "It's already in the design doc" | Designs are frozen at brainstorming time. Mid-project decisions are not in there. |
| "Too busy to journal" | Journaling takes 3 minutes. Re-loading lost context takes 30. |
| "I'll journal at the end of the week" | You will not. Details are lost within hours. |
| "This is over-engineering for a small project" | Research runs on month/year timescales. Even small projects outlive your short-term memory. |
| "My collaborators don't journal" | Their loss. You do not owe them your context loss. |

## Red Flags — STOP

These mean you are doing it wrong:

- Spending more than 5 minutes on a single journal entry — you are over-writing
- Copy-pasting full conversation blocks — journal is curated, not a transcript
- "Blockers: none" appearing in every entry — you are not looking carefully
- Insights section contains generic platitudes ("normalization is important") instead of project-specific lessons
- Writing an entry for a session with no decisions, failures, or surprises — skip it
- Entries getting longer over time (50+ lines) — tighten; less is more
- The user consistently rejects drafts — you are capturing the wrong things; ask what matters to them

## Anti-Patterns

| Anti-pattern | Fix |
|---|---|
| Journaling after every trivial action | Journal per session, not per commit |
| Transcribing the conversation | Curate, don't record |
| Omitting rationale, keeping only facts | The rationale IS the journal's purpose |
| Writing retrospectives weeks later | Same-day or not at all |
| Letting the journal become a to-do list | That's for TodoWrite, not the journal |
| Treating it as a personal diary | Keep it professional and project-focused |
| Auto-writing without user review | Always show the draft first |

## Integration

- **Called by:** `eureka:using-eureka` when any of the trigger conditions are detected
- **Read by:** `eureka:whats-next` (most recent entry, especially the "Next session starts with" field)
- **Complements:** `docs/eureka/records/experiment-log.md` (metric-focused), `docs/eureka/designs/` (design-time), `docs/eureka/registrations/` (pre-registered)
- **Suggests promotion to:** Claude Code auto-memory (user-level, cross-project)
- **Does NOT replace:** Any existing Eureka artifact — it is a narrative overlay

## Skill Type

**FLEXIBLE** — The writing style, length, and depth adapt to what actually happened in the session. The structure (date-based file, section headers, required `Worked on` + `Next session starts with` fields) is fixed.

The journal is the longest-lived memory in any Eureka project. Treat it accordingly: terse, specific, and always curated.
