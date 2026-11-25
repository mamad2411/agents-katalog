---
name: anti-slop
description: "Use when reviewing your own tool-call sequence (or another agent's) for wasteful patterns — re-reading a file you just edited, repeated reads of the same path, bash echo for plain communication. Surfaces concrete patterns to avoid, not vague style advice."
aliases: [no-slop, slop-watch, tool-call-hygiene]
category: quality
tags: [hooks, hygiene, post-tool-use, autonomous-loops]
version: 1.0.0
---

# Anti-Slop Skill

Use this skill when you want to audit a recent stretch of tool calls
(your own, an agent's, or a session replay log) for wasteful patterns
that burn context and time without producing work. The goal is to
**surface concrete violations**, not give vague style advice.

This skill is paired with the `anti-slop` PostToolUse hook, which
emits the same warnings to stderr in real time when
`EVOKORE_ANTISLOP_HOOK=true` (or via a protection profile that
enables it). Both surfaces share the same definitions of "slop"
below.

## Trigger

Apply this skill when:

- About to start a new pass and want to check whether the previous
  segment was wasteful.
- Reviewing a long autonomous-loop transcript before merging or
  summarizing.
- Triaging why a session is slow or feels confused.
- Operating with `EVOKORE_ANTISLOP_HOOK=true` and you see a stderr
  advisory and want to understand the underlying rule.

Do **not** apply it as a blocking gate. The hook is warning-only by
design, and so is the skill.

## The patterns

### Pattern A — Re-read after edit

> Reading a file immediately after `Edit` / `Write` / `MultiEdit`
> succeeded on it.

The Edit/Write tools error if the change failed; on a clean response
the file already matches your `new_string` and the harness tracks
file state for you. Re-reading just to "verify" burns context with
no new information.

**What to do instead:** trust the edit. If you genuinely need to see
a different region you didn't pre-load, read **only** the new offset/limit
range. Do not re-read the whole file.

### Pattern B — Repeated reads of the same path

> Three or more consecutive `Read` calls on the same path with no
> Edit/Write between them.

This usually means you're looking for something you already saw and
have lost track of, or you're paging through the file inefficiently.
Either way, the third read costs you context that the first two should
have answered.

**What to do instead:** scroll back in your own context to find the
prior read. If you need a different range, jump there directly with
`offset`/`limit` instead of re-reading from line 1.

### Pattern C — Bash echo / printf for plain communication

> A `Bash` call whose entire purpose is to emit a string the user or
> agent could read directly.

Anthropic's guidance is explicit: *"Communication: Output text
directly (NOT echo/printf)"*. Wrapping a sentence in `bash -c "echo
hello"` adds a tool call, a roundtrip, and a permission prompt, while
producing the same bytes you could have just typed.

**What to do instead:** put the sentence in your assistant message.

## How to apply this skill

When asked to audit a stretch of tool calls (or when reviewing your
own past N invocations):

1. Walk the recent calls in order. Track `lastTouched[file] = tool`
   for each Edit/Write/Read.
2. For each `Read`, check whether the most recent prior touch on
   that file was an Edit/Write — flag pattern A if so.
3. Slide a 3-call window over the sequence; if all three are `Read`
   with the same file path, flag pattern B.
4. For each `Bash`, if the command is bare `echo …` / `printf …`
   with no redirection, pipe, or expansion, flag pattern C.

Report each violation with: pattern name, the offending call(s),
and one-line remediation. Do **not** propose process changes,
re-architectures, or "next steps" — the value of this skill is the
small, falsifiable callouts.

## Output format

```json
{
  "violations": [
    {
      "pattern": "read_after_edit" | "repeated_reads" | "bash_echo_for_output",
      "file": "<path>",          // when relevant
      "command": "<bash cmd>",   // for pattern C only
      "advice": "<one-line fix>"
    }
  ],
  "clean": <bool>
}
```

Set `clean: true` when no patterns matched. Keep `violations` empty
in that case rather than omitting the key.

## What this skill is NOT

- Not a style guide. It does not flag verbosity, parallelism choices,
  or commit-message taste.
- Not a blocker. The hook always exits 0; the skill always returns a
  report.
- Not a complete coverage of "slop". It deliberately ships with three
  conservative patterns where the cost is unambiguous and the fix is
  one line. Add new patterns only when you can describe them in a
  one-sentence trigger and a one-sentence fix.

## Related

- `scripts/anti-slop.js` — the runtime detectors used by both this
  skill and the hook.
- `scripts/hooks/anti-slop.js` — fail-safe wrapper for PostToolUse.
- `EVOKORE_ANTISLOP_HOOK` env var — opt in to live stderr warnings.
- `EVOKORE_PROTECTION_PROFILE` — umbrella switch (Fix 2) that may
  enable the hook as part of a coordinated profile.
