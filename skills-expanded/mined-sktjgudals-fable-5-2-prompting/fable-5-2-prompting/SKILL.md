---
name: fable-5-2-prompting
description: Use when writing, auditing, or migrating a system prompt, CLAUDE.md, skill, agent file, memory file, or harness for Claude Fable 5.2 or Claude Mythos 5.2, or when a Fable 5.2 agent stops before the task is done, asks for approval it does not need, goes silent during long turns, starts too many subagents, bolts new code onto old structure, thinks before trivial replies, writes choppy reports, or returns stop_reason "refusal".
---

# Prompting Claude Fable 5.2

Unofficial skill. Source: Anthropic's "Prompting Claude Fable 5.2" guide, read on 2026-11-12:
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2
If the guide and this skill disagree, the guide is right.

## Core rule

Fix only behaviors that someone has observed. Apply one change at a time, then measure its effect and its token cost on the user's own tasks. Most fixes here have a cost. Do not paste all of them into a prompt.

Use the guide's wording for each fix (in `references/prescriptions.md`). Do not invent replacement wording when the guide supplies one. Quote the guide's measured cost, not an estimate based on the length of the added text. Where the guide gives no text or no figure, say so plainly and do not fill the gap with a guess.

## Mode 1: symptom lookup

| Observed behavior | Fix | Measured cost |
|---|---|---|
| Turn ends with "remaining work" or "want me to continue?" | "Finishing work" block. It removes most "want me to continue?" endings but not "remaining work" endings | About 30% more output tokens |
| Agent withholds routine steps or asks for unneeded approval | Remove stale caution; name the exact actions that need approval | None measured |
| Agent adds to old structure instead of consolidating | Ownership sentence | 70-80% more output tokens, unrequested changes |
| Silent during long tool runs | Check `thinking.display` first, then a harness reminder or a prompt line | Reminder: no notable rise. Opener-and-recap text: about 20% more output tokens |
| Too many subagents | Remove standing delegation lines, then rewrite the subagent tool description | None; this lowers cost |
| Slow or costly on trivial requests | Lower `effort` for that turn. Prompt text does not stop thinking at `medium` or above | None |
| Final report is dense or hard to follow | "Communicating clearly" block | None measured |
| `stop_reason: "refusal"` | Read `stop_details.category`; remove any request to write reasoning in the response | None |

Give the user: the exact text, where it goes, the measured cost, when not to use it, and what to keep (confirmation for risky or irreversible actions). Read `references/prescriptions.md` for all of these.

## Mode 2: audit

1. Ask which files the model reads: system prompt, CLAUDE.md, skills, agent files, memory, notes, tool descriptions.
2. Read each file. Check every line against `references/audit-checklist.md`.
3. Report one row per instruction line, including the lines to keep: the line, verdict (remove, rewrite, test, keep), the reason from the guide, and the proposed text.
4. State which findings are certain from the guide and which need the user's own test.
5. Do not edit the files. The user decides.

An audit finds lines that the guide names as a risk. Recommend removing or rewriting such a line even when the user reported no behavior, but still one change at a time. Recommend added text (Mode 1) only for a behavior the user reported. If you cannot ask the user which files to read, audit the files you were given and list the open questions. When a line needs a rewrite and the guide gives no replacement wording, write a draft and label it as a draft.

## Rules for every answer

- Changes to `system`, `tools`, or earlier messages apply in new conversations only. A request that resumes an earlier conversation can return a 400 error. See `references/api-harness.md`.
- Do not carry over effort settings from Fable 5.1 or Opus 5.5. Start at `high` and run the effort sweep again.
- A scope rule ("no drive-by refactors") does not cancel the ownership sentence. Leave the sentence out when the user wants minimal changes.
- The model treats "never" as absolute. Rewrite it with a scope and a reason, or as "ask before".

## References

- `references/prescriptions.md`: exact text, placement, cost, and limits for each fix.
- `references/audit-checklist.md`: the lines to find in prompts written for earlier models.
- `references/api-harness.md`: effort levels, progress display, preserved thinking, refusals. Read it when the user builds on the API.
