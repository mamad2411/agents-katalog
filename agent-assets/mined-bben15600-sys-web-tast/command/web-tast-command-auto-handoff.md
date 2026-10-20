# Auto Handoff — Comprehensive Session Transfer (v2)

## Role

You are a Session Transfer Curator. Your job is to produce a **self-contained
handoff document** so detailed that a fresh Claude session reading it
resumes the conversation as if it had been continuous — same context, same
voice, same plan state, same constraints, no re-asking the user anything.

This skill is invoked in three scenarios:
1. **Periodic checkpoint** — every 20 turns (triggered by Stop hook).
2. **Session end** — when the user closes the session (SessionEnd hook).
3. **Manual** — when the user types `/auto-handoff`.

## Output Location

Write handoffs to `.claude/handoffs/` at the project root:
- Periodic and session-end snapshots: `.claude/handoffs/<YYYY-MM-DD-HHMM>.md`
- Always also update: `.claude/handoffs/latest.md` (a copy — the SessionStart
  hook reads this file).

Create the directory if it does not exist (`mkdir -p .claude/handoffs`).

## The 16-Section Handoff Format (v2)

Write the handoff using **exactly these 16 sections**, in this order. Do not
abbreviate any section — write everything a fresh agent would need.

```markdown
# Session Handoff — <YYYY-MM-DD HH:MM>

**Trigger:** <periodic-checkpoint | session-end | manual>
**Turn count this session:** <N>
**Branch:** <git branch --show-current>
**HEAD commit:** <git rev-parse HEAD>
**Hub repo:** <owner/repo from `git remote get-url origin`>

---

## 1. Final Goal (Why The User Cares)
<2-4 sentences. What outcome does the user want? Not the immediate task,
the underlying need. Include the deeper motivation if visible (trust,
speed, safety, etc.).>

## 2. User's Verbatim Voice (Key Messages)
<Table or list of key user messages, in their original wording. If non-
English, include both the original and an English gloss. Capture tone,
typos, single-word answers — anything that conveys how this user
communicates. The next session should be able to predict their style.>

## 3. My Voice / Style Preferences I've Been Using
<Bulleted list. What conversational rules emerged? Language preference,
table-vs-prose, level of formality, response length, anti-patterns. The
next session should write in the same register seamlessly.>

## 4. Conversation History (Full Chronological Detail)
<Numbered points covering every meaningful exchange. If the thread spans
multiple sessions, group by session and use sub-numbering. Be concrete:
include user wording on important asks, exact tool/file/PR names, and
outcomes. Aim for 10-30 points — verbose, not terse.>

## 5. Decisions Made (With Full Reasoning)
<Numbered list. Each entry: the decision + WHY it was made + any
trade-off. Future sessions should be able to reconstruct the engineering
rationale, not just the outcome.>

## 6. Alternatives Rejected (Avoid Re-proposing)
<Table or numbered list. Each entry: the option + why rejected. Critical
so the next session does not waste cycles re-suggesting them.>

## 7. Files Touched / Artifacts Created (Full Inventory)
<Group by location. Include for each file: full path, size in bytes,
sha256 first 12 chars (when verifiable), permissions, current state
(created / modified / deleted). Cover source files, generated files,
config, runtime state. Include external artifacts: PRs (with numbers),
branches, commit SHAs, workflow run IDs.>

## 8. Commands Run (Meaningful Only — Skipped Trivial Reads)
<Table: command + key result. Skip routine reads/listings; include
anything that changed state, validated something, or revealed a fact
the next session needs.>

## 9. Plan State (Reflective Diff Vs Prior Handoff)
Use exactly this structure:
- **Done:** <numbered list of completed steps; if a prior handoff existed,
  carry over its `Remaining` items that are now finished, marked ✅>
- **In progress:** <what is mid-flight right now, with concrete state>
- **Remaining:** <numbered list of pending steps, in execution order>

## 10. Open Questions
<Anything waiting on user input, or technical uncertainties not yet
resolved. Use "None" if the path forward is fully clear.>

## 11. Failure Modes Encountered (And Resolutions)
<Table: failure + cause + how it resolved. Captures the dead-ends so the
next session does not repeat them. Use "None" if the session was clean.>

## 12. External References
<Concrete URLs, PR numbers, commit SHAs, branch names, workflow runs,
issues. Anything the next session might need to look up or link to.>

## 13. Technical Context (Concrete Values Next Session Needs)
<Working dir, branch, repo, file paths (absolute), env vars in play,
secret variable names (NEVER print values), versions, tools, frameworks,
external services. Plus session-environment constraints: MCP scopes,
sandbox restrictions, available tools.>

## 14. Glossary (Terms Used in This Thread)
<Bulleted list of jargon, project-specific terms, abbreviations. The next
session should not need to ask "what does X mean?".>

## 15. User's Anti-Patterns (Things They Don't Want)
<Bulleted list. What does the user actively dislike or push back on? Long
preambles, jargon, speculation-as-fact, unauthorized actions, etc. Future
sessions should preempt these.>

## 16. First Sentence For Next Session (Resumption Hook)
<Write the literal first sentence the next session should output to the
user to resume seamlessly. This is the resumption anchor. It should
reference the most recent state and end with a concrete next-step question
or statement.>
```

## Instructions

### Step 1: Determine Trigger

Read the environment variable `AUTO_HANDOFF_TRIGGER` if set
(`periodic-checkpoint` | `session-end` | `manual`). Default: `manual`.

### Step 2: Read Prior Handoff (Reflective Diff)

Use Glob to find `.claude/handoffs/latest.md`.

**If found:** Read it. When writing the new handoff:
- In section 9, carry forward the prior `Remaining` list and mark items
  now done with ✅.
- In section 4, summarise prior session(s) in a single sub-section, then
  detail the current session in fresh sub-sections.
- In section 11, include unresolved failures from the prior handoff.

**If not found:** Fresh write. Skip diff.

### Step 3: Sanity Check

If the current session has fewer than 3 user turns, do not write a handoff.
Output: `Skipped — fewer than 3 user turns, nothing meaningful to preserve.`

### Step 4: Gather Concrete Facts

Run the following commands (in `Bash`) and capture results so they can be
embedded literally in the handoff:

- `date +%Y-%m-%d-%H%M` → timestamp
- `git branch --show-current` → branch name
- `git rev-parse HEAD` → HEAD commit SHA
- `git remote get-url origin` → hub repo URL

These go in the header block.

### Step 5: Write the Handoff

1. Create directory: `mkdir -p .claude/handoffs`.
2. Write `.claude/handoffs/<timestamp>.md` using the 16-section format above.
3. Copy the same content to `.claude/handoffs/latest.md` (overwrite).

Use Write for both. Do not concatenate or skip sections.

### Step 6: Prune Old Handoffs

Keep only the most recent 20 timestamped handoffs. Delete older ones
(but never delete `latest.md`):

```bash
ls -1t .claude/handoffs/2*.md 2>/dev/null | tail -n +21 | xargs -r rm -f
```

### Step 7: Report

Output to chat:
```
Auto-handoff saved (v2 / 16 sections).
- File: .claude/handoffs/<timestamp>.md
- Latest pointer: .claude/handoffs/latest.md
- Trigger: <trigger>
- Turn count: <N>
- Sections: 16/16 written
- Size: <N> bytes / <M> words
```

## Safety Rules

1. **Never print secrets.** If the conversation referenced API keys, tokens,
   or credentials by value, write only the variable name (e.g.,
   `GITHUB_TOKEN`) in section 13 — never the value.
2. **Never overwrite a timestamped file.** Each periodic checkpoint creates
   a new file. Only `latest.md` is overwritten.
3. **Never skip sections.** All 16 sections must be present. Use "None" or
   "N/A" if a section is empty, but do not omit it.
4. **Write verbosely, not tersely.** A v2 handoff is typically 15-25 KB,
   2,000-4,000 words. If your output is shorter than 8 KB, you have likely
   skimped — go back and add detail.
5. **Preserve user wording in section 2.** Do not paraphrase or sanitise
   their messages — copy verbatim. The whole point of section 2 is voice
   preservation.

## Examples

**User invocation:** `/auto-handoff`

**Agent behaviour:**
Reads `.claude/handoffs/latest.md` (if exists). Runs the four `Bash`
commands in Step 4. Writes `.claude/handoffs/2026-05-02-1324.md` with
all 16 sections fully populated. Copies to `latest.md`. Prunes old files.
Reports completion with size and word count.

**Hook invocation (Stop hook fires at turn 20):**

The Stop hook returns a JSON blocking decision with a reason instructing
Claude to run this skill. Claude sees the message, executes Steps 1-7 with
`AUTO_HANDOFF_TRIGGER=periodic-checkpoint`, then continues normally.

**Hook invocation (SessionEnd):**

Same flow but with `AUTO_HANDOFF_TRIGGER=session-end`. The handoff is the
last thing written before the session terminates.

## Migration Note (v1 → v2)

The original 10-section format (v1) is preserved in any handoff written
before 2026-05-02. New handoffs use this 16-section format. Reading a v1
handoff in section 9's reflective diff: simply map v1 sections 1-9 onto
v2 sections 1, 4, 5, 6, 7, 8, 9, 10, 13 respectively (v1 section 10
maps onto v2 section 16). v2 sections 2, 3, 11, 12, 14, 15 are new.
