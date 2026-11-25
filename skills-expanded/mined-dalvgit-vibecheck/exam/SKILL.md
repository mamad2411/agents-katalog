---
name: exam
description: Examine the human on the code they are about to push. Use when a push is blocked by vibecheck, or when the user asks to be vibechecked. Reads the outgoing diff, asks 2-4 multiple-choice questions about it via AskUserQuestion, grades them, and unlocks the push on a pass.
allowed-tools: Bash, Read, Grep, AskUserQuestion
---

# vibecheck: the exam (Claude Code)

An agent wrote this code; the human is about to put their name on it. Your job is to find out
whether they understand what they're shipping. **You are the examiner, not the candidate** —
never answer, hint, or narrow the options. `AskUserQuestion` is the only way to collect an
answer here.

This file is only the Claude Code *delivery* wrapper. The instructions that decide whether the
exam is any good — what to ask, the altitude, fair distractors, how to grade, the one rule —
live in the shared guide. **Read it before writing questions and follow it:**

```
"$GATE" --guide
```

## 0. Find the gate

Every blocked push prints the gate's absolute path on its last line. Use that. If you're run
without a block message (the user just asked to be vibechecked), try
`"${CLAUDE_PLUGIN_ROOT}/hooks/gate.sh"`, and failing that:

```
ls ~/.claude/plugins/*/vibecheck*/hooks/gate.sh 2>/dev/null || find ~/.claude -name gate.sh -path '*vibecheck*' 2>/dev/null | head -1
```

## 1. Read the diff

```
"$GATE" --diff
```

This is exactly the diff the gate hashes — **do not substitute your own `git diff`**, or the
receipt won't match and the push stays blocked. If it's empty, say so and stop. Use Grep to read
surrounding code (callers, etc.) where a question needs it.

Read `.vibecheck.toml` if it exists: `questions` (default 3) and `pass` (`all` | `majority`,
default `all`).

## 2. Write the questions

Follow `"$GATE" --guide`. In short: find the 2–4 *ideas* the change rests on and test what
follows from them; state the change plainly and make them reason out the consequence; every
distractor actually wrong and distinguishable; never quiz absent code or line-level trivia.

## 3. Administer via AskUserQuestion

Ask all questions in a **single `AskUserQuestion` call** — one per `questions` entry. The human
answers; you cannot.

**Every question carries the way out.** Make the **last option of every question** a plain,
first-class escape — same wording each time:

> - …(the substantive answers)…
> - **Skip the vibecheck — push without answering**

That leaves **three substantive options** per question (one correct, two wrong — the guide's
rules apply to those). The point: the human can bail at the *very first* question, or any
question, without reading the rest. If they pick the skip option on **any** question, that is a
skip — honor it immediately (`--skip`) and do not grade.

Do not reveal the correct answer, hint at it, or react to answers until everything is in.

## 4. Grade and record

Score per `pass` (`all` = every question; `majority` = more than half). For how to handle a
fail, a skip, or pushback, follow the guide — be helpful on a fail, take a skip at face value,
believe them when a question was unfair.

- **Pass:** `"$GATE" --pass`, then retry the push and report the score plainly.
- **Skip** (picked from the exam, or said at any point): `"$GATE" --skip`, immediately, no
  guilt-tripping. Then retry the push.
- **Fail:** issue no receipt; explain what the code actually does, name the hunks worth reading,
  and offer the three doors (try again / skip / go read).

## The one rule

Never answer for the human, and never issue a receipt they didn't earn. You *could* forge it —
you have a shell — which is exactly why it matters that you don't. See the guide's closing lines.
