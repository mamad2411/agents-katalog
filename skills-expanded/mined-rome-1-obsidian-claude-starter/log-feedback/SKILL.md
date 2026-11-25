---
name: log-feedback
description: Captures friction with the vault's own system (a wrong or stale instruction in AGENTS.md, a template missing a field, a skill that fired when it should not have or gave bad guidance, a correction the user made to an agent's work) and fixes the cause, not just the instance; appends to System/agent-feedback.md and, when the fix is clear, edits the skill, template or rule in the same pass. Use when the user says "remember this for next time", "don't do that again", "that instruction is wrong", "update the skill", "log this", corrects the same kind of mistake twice, runs /log-feedback, or when you notice an instruction here contradicting what actually works.
argument-hint: "[what went wrong, and where]"
---

# Log feedback

When the user corrects an agent, two things need fixing: the output in front of you, and whatever produced it.
Fixing only the first means the same mistake comes back next session.

## 1. Pin it down

Get a concrete pointer, not an impression:

- What happened (the output, or the instruction that misled).
- Where it came from: a line in `AGENTS.md`, a section of a skill, a template field, the writing guide, or nowhere (a gap).
- What should have happened instead.

If you cannot name a source or a gap, ask one question to find it.

## 2. Fix the instance

Correct the note, reply or file the user is unhappy with, if that has not been done.

## 3. Find the general lesson

Ask: what rule, if it had been written down, would have prevented this, and does that rule hold beyond this one case?
Prefer a rule that generalizes ("cut any qualifier the sentence survives without") over a patch for one word ("don't say 'very'").

## 4. Route it

| The lesson is about... | Put it in |
|---|---|
| How a specific workflow should run | That skill's `SKILL.md` (a step, a check, or a sharper trigger in the `description`) |
| A field or section a note type needs | The template in `System/Templates/` and [[System/vault-schema]] |
| How prose should read | `System/writing-guide.md`, under "Your additions", with an example |
| How agents should behave in this vault | `AGENTS.md`. Keep it short; it loads every session |
| How agents should behave everywhere | The user's global rules (see `System/global-agent-rules.md`); propose the edit, since that file lives outside the vault |
| Unclear, or needs the user to decide | Only the log entry below |

Make small, additive edits. Do not rewrite a skill or a rule file wholesale to fix one thing.
For edits to `AGENTS.md` or global rules, show the user the diff before saving.

## 5. Log it

Append one line to `System/agent-feedback.md` under `## Entries`:

- Fixed now: `- YYYY-MM-DD [where] what went wrong; fixed in <file> [status: applied]`
- Not fixed: `- YYYY-MM-DD [where] what went wrong, and the proposed fix [status: open]`

When resolving an older open entry, append a new line (`- YYYY-MM-DD [re: YYYY-MM-DD entry] applied | declined: ...`) instead of editing it.

## 6. Commit

Commit the fix and the log line together, e.g. `vault: feedback - meeting-notes asks for owners instead of guessing`, if the user has agreed to agent commits.
