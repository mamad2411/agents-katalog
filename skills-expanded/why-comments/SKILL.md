---
name: why-comments
description: "Use when comments narrate what the code already says (`// increment the counter`) or when surprising, load-bearing code has no explanation. Deletes the narration, keeps and sharpens comments that record a non-obvious why — the workaround, the spec quirk, the ordering constraint — and adds a why where one is missing."
---

# Why Comments

## The failure mode this fixes

Comments fail in two opposite directions. Agents (and tired humans) write narration — `// loop over the users`, `// call the API` — that restates what the code already says, goes stale the moment the code changes, and trains every reader to skip comments entirely. Meanwhile the *one* thing a comment can do that code can't — record **why** — goes unwritten: why the retry is 3 and not 5, why this runs before that, why the obvious approach was tried and reverted. Six months later someone "simplifies" the workaround and reintroduces the bug it guarded against.

This skill inverts the ratio: delete the *whats*, keep and sharpen the *whys*, and add a why where surprising code has none.

## When to Use This Skill

- A file is full of comments that just narrate the next line
- Load-bearing or surprising code (a magic value, an odd ordering, a deliberately "wrong-looking" approach) has no explanation
- You're reviewing AI-generated code — agents over-narrate and under-justify
- `explain-back` flagged a chunk `UNJUSTIFIED` and the justification, once found, should be written down
- A comment and the code beneath it disagree (the comment went stale)

**Don't use when:** the comments are API documentation (docstrings, JSDoc, godoc) — those describe a contract for consumers and are a different job, judged by different rules. And don't add a why where the code is genuinely self-evident; a comment on the obvious is noise wearing a justification.

## Instructions

### 1. Classify every comment in scope

Walk the comments and tag each one:
- **WHAT** — restates the code (`// check if the user is active` above `if (user.isActive)`)
- **WHY** — states a reason, constraint, or history the code can't show (`// gateway rate-limits at 10 rps; see INC-482`)
- **CONTRACT** — docstring/API documentation for consumers → out of scope, leave it
- **CORPSE** — commented-out code → that's `delete-this` territory; version control already remembers it
- **STALE** — describes code that no longer matches → either fix it to the current truth or delete it; a wrong comment is worse than none

### 2. Delete the WHATs

Remove narration outright. If a WHAT comment exists because the code underneath is unclear, the fix is the code, not the comment — usually a better name (`name-things`) or a small extraction. The comment was a crutch; replace the leg, don't decorate the crutch.

### 3. Keep and sharpen the WHYs

A surviving why must state the actual constraint, not gesture at it:
- Name the force: the spec quirk, the upstream bug, the perf cliff, the incident
- Link the evidence where it exists (ticket, incident, vendor doc, benchmark)
- Say what breaks if someone "fixes" it — that's the sentence that stops the well-meaning revert

> Bad: `// don't change this`
> Good: `// keep the 250ms floor: the gateway silently drops sub-250ms retries (vendor ticket #4821); removing it re-opens INC-482`

### 4. Add a why where surprising code has none

Scan for code that would make a new reader stop — magic values, deliberate no-ops, order-dependent calls, an approach that looks worse than the obvious one. Each gets one line of why. If you can't find the why (git blame, history, asking), don't invent one — flag it `UNJUSTIFIED` exactly as `explain-back` would, and surface it to the human.

### 5. Match the project's voice

If `CONTEXT.md` records conventions (comment density, ticket-link format, language), follow them. A repo that links incidents as `INC-123` shouldn't get prose paragraphs.

## Output format

```
DELETED (narration — code already says it)
  - <file:line> — "<comment>" (restates the code)

KEPT & SHARPENED (real whys)
  - <file:line> — before: "<vague>"  →  after: "<constraint + evidence + what breaks>"

ADDED (surprising code that had no why)
  - <file:line> — why: <the constraint, one line>

UNJUSTIFIED (no why found — needs a human)
  - <file:line> — <what's surprising and what was checked (blame, history)>
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| Narrating the next line | Restates the code, rots on the next edit, and teaches readers to skip all comments — including the load-bearing ones. |
| `// don't touch this` with no reason | A warning without a why gets ignored or, worse, obeyed forever after the constraint is gone. |
| Inventing a plausible why | A confident wrong justification is worse than `UNJUSTIFIED` — it ends the investigation at the wrong answer. |
| Fixing unclear code with a comment | If the code needs narration to be readable, fix the names or the structure. The comment is the symptom. |
| Deleting a why you don't understand | That comment may be the only record of the constraint. Verify it's obsolete before it goes. |

## Mental Model

> Code says what; comments owe you why. Delete every comment the code can say itself, and make the survivors carry the one thing code never can — the reason.
