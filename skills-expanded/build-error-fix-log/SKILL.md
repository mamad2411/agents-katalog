---
name: build-error-fix-log
description: Keeps an Error Fix Log for one error in a prototype, with the error in plain words, what you did just before it, the fewest steps that bring it back, one change per attempt with its result, when to rewind to a save point and the line where you stop and ask an engineer. Use for "run build-error-fix-log", "it broke and the message means nothing to me", "what does this error mean", "every fix breaks something else", "help me reproduce this error", "should I rewind", "when do I stop and ask an engineer", part of the Claude for Product Builders Pack by 90n.
---

# Error Fix Log

## When To Use
It broke, the message means nothing to you, and the last three fixes each broke something else. Open a log for that one error before you try a fourth. It answers: what exactly happens, can you make it happen again, what has been tried, and when do you stop?

## When Not To Use
If nothing is broken and you are planning the build, use First Working Version. If your question is about the whole prototype rather than one error, write an Engineering Review Request instead.

## Inputs
- The exact error message, copied, with names, emails and keys masked
- What you did just before it appeared, and the last save point that worked
If you have none of this, I start from your description of what you saw on screen and mark the output as a first draft.

## Approach
The method is the minimal reproducible example from the Stack Overflow help centre (stackoverflow.com/help/minimal-reproducible-example), with checkpoints and rewind from the Claude Code docs (code.claude.com/docs/en/checkpointing). You do not need to understand the code to describe a symptom exactly and to notice whether it came back. This is a way to read an error and reproduce it, not a way to become the person who fixes all of them. The failure it prevents: an afternoon of "try this instead", changes stacked on each other, and no working state left to return to.

## Workflow
1. Ask up to three questions: what is the exact message, what did you do just before, and what is your stop line (a number of failed attempts or an amount of time)? You set the stop line now, before attempt one. Mask before you paste: messages and logs can hold names, emails or keys, so replace them with [name], [email], [key].
2. Read it. Claude restates the message in plain words: what was being attempted and what failed. Where it is guessing, it says so, and the guess is logged as a guess.
3. Reproduce it. Claude reduces the case; you confirm the symptom on screen each time. The help page asks for three things: minimal (as little as possible that still shows the same problem), complete (everything someone else needs to see it), reproducible (tried again and it happens again). If it does not come back, write "not reproduced" and stop changing things.
4. One change per attempt, each logged with its result as you saw it on screen. Three changes at once hide which one mattered, and which one broke the next thing.
5. Rewind when an attempt makes it worse. `/rewind` lists earlier prompts and can restore the code, the conversation or both. Two limits from the docs: changes made by shell commands are not tracked, and it is not version control. If a rewind cannot get back to a working state, go to the last save point.
6. Hold the stop line. When you reach it, stop and take the log to an engineer. The log is what makes that conversation short.

## Output Format
```markdown
# Error Fix Log
Prototype: [name] | Build step: [n] | Opened: [date] | Stop line: [n failed attempts or time, set before attempt 1]
## The error
| Item | Entry |
|---|---|
| Exact message (masked) | [text] |
| In plain words | [what was attempted, what failed, what is a guess] |
| What I did just before | [action] |
| Last save point that worked | [commit or dated folder copy] |
## Steps that bring it back
[Numbered steps, as few as still show it.] Tried again on [date]: [it came back / not reproduced]
## Attempts
| No. | The one change | Result I saw on screen | Anything else that changed |
|---|---|---|---|
| [1] | [change] | [same error / different error / gone] | [none / what] |
## Rewinds and restores
[When], restored [code / conversation / both / save point] from [prompt or save point]. Back to a working state: [yes / no].
## For the engineer
[What I was building, the steps above, the attempts so far, and my one question.]
## Decision
[Builder, by role] stops at the stop line and takes this log to [engineer, by role] by [date]; the engineer decides whether the fix is worth making in a prototype.
```

## Done When
- The message is quoted exactly and masked
- The steps were run again and the result is written down
- Every attempt holds one change and one observed result
- The stop line is dated before the first attempt, and the note for the engineer is filled in once it is reached

## Quality Bar
- "Gone" means you ran the steps again and did not see it, not that Claude says it is fixed.
- No attempt disables a check, removes a rule from the rules file or adds a real key to get past the message.
- An error that mentions keys, sign-in or permissions is not yours to work around: check with your engineering or security lead.
- Stopping at the stop line is the method working, not a failure of the builder.
- This is a way to read and reproduce an error and to know when to stop; it is not a promise that every error can be fixed without an engineer.

## Next
Run build-sample-data-plan (Sample Data Plan) before any data goes into the working version.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
