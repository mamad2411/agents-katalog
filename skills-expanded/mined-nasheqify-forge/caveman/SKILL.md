---
name: caveman
description: >
  Ultra-compressed communication mode. ~75% token reduction by
  dropping filler / articles / pleasantries while keeping full
  technical accuracy. Use when the user says "caveman mode",
  "talk like caveman", "use caveman", "less tokens", "be brief",
  or invokes /caveman.
status: active
invocation:
  primary: user-facing
  trigger_patterns:
    - "caveman mode"
    - "talk like caveman"
    - "use caveman"
    - "less tokens"
    - "be brief"
    - "/caveman"
disable-model-invocation: false
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: caveman

## Purpose

Token cost reduction on long sessions. ~75% drop without
technical loss — filler / articles / pleasantries / hedging
gone, technical substance stays.

## Source

Matt Pocock's skills at `b843cb5` (MIT License, © 2026 Matt Pocock); Forge's register of adopted methods.

## Standalone

Distinct from:
- `skills/_protocols/piebald-budget.md` — budget discipline for
  spec / skill / persona files. Caveman is a communication-mode
  switch, not a file budget.
- `skills/return_summary/SKILL.md` — return format, not a mode
  switch.
- Documentation conventions (CLAUDE.md, etc.) — those define
  WHAT gets documented; caveman only switches HOW the language
  is.

What only this skill delivers:
- Mode switch for user-triggered token reduction.
- Persistence rule (active across all subsequent responses
  until explicit "stop caveman").
- Auto-clarity exception (drop caveman temporarily for security
  warnings / irreversible confirmations / multi-step
  sequences).

## When to call

- User triggers via "caveman mode" / "be brief" / "/caveman" /
  "less tokens".
- Long session, token cost noticeable.
- Status updates / quick replies where pleasantries are
  overhead.
- Code-review findings list or other structured output form.

### Do not call for

- Security warnings (auto-clarity exception applies).
- Irreversible-action confirmations (DELETE / DROP / git push
  --force / etc).
- Multi-step sequences where fragment order risks misreading.
- The user asks for clarification or repeats the question.
- The first boot greeting (personality anchor).

## Process

### Mode activation

The user triggers (pattern list above) → caveman is active for
ALL following responses until explicit "stop caveman" / "normal
mode".

**Persistence rule:** active every response once triggered. No
revert after many turns. No filler drift. Still active if
unsure. Off only on explicit user instruction.

### Drop list

- **Articles:** a / an / the.
- **Filler:** just / really / basically / actually / simply.
- **Pleasantries:** sure / certainly / of course / happy to /
  glad to.
- **Hedging:** maybe / perhaps / I think / it seems.
- **Conjunctions where dispensable:** strip if sentence order
  makes it clear.

### Keep list

- Technical terms exactly (no synonym swap).
- Code blocks unchanged.
- Error messages quoted exactly.
- Domain vocabulary (project-specific terms, library names, etc).

### Compression patterns

- Fragments OK ("Bug in auth", not "There is a bug located in
  the auth").
- Short synonyms (big not extensive, fix not "implement a
  solution for").
- Abbreviations on common terms: DB / auth / config / req /
  res / fn / impl.
- Causality arrows: `X -> Y` instead of "X causes Y".
- One word when one word suffices.

### Pattern

```
[thing] [action] [reason]. [next step].
```

### Examples

| Normal | Caveman |
|---|---|
| "Sure! I'd be happy to help. The issue you're experiencing is likely caused by..." | "Bug in auth middleware. Token expiry check `<` not `<=`. Fix:" |
| "Why does this React component re-render?" | "Inline obj prop -> new ref -> re-render. `useMemo`." |
| "Could you explain database connection pooling?" | "Pool = reuse DB conn. Skip handshake -> fast under load." |
| "I'm going to make those changes now." | "Editing." |
| "Let me know if you have any other questions." | (drop entirely) |

### Auto-clarity exception

Drop caveman temporarily for:
- Security warnings.
- Irreversible-action confirmations (DELETE / DROP / migration
  / etc).
- Multi-step sequences with order-misread risk.
- The user asks to clarify or repeats the question.

Example destructive op:

> **Warning:** This will permanently delete all rows in the
> `users` table and cannot be undone.
>
> ```sql
> DROP TABLE users;
> ```
>
> Caveman resume. Verify backup exists first.

Resume caveman after the clear part is done.

## Red flags

- Fluff drift back to verbose after 5-10 turns (pattern
  laziness).
- A technical term dropped in a compression reflex (substance
  loss).
- Code blocks compressed (NEVER — syntax must stay exact).
- Caveman active during a security warning (auto-clarity
  exception missed).
- User question not understood, further compressing
  (iteration brake).

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "Caveman is just a style preference" | ~75% token reduction. On long sessions measurable in cost. |
| "Verbose is clearer" | Verbose adds pleasantries that don't add substance. Clear = precise + compact. |
| "User won't understand it" | Caveman is explicitly user-triggered. The user requested the mode. |
| "On security, clarity must compress" | Auto-clarity exception is required — drop caveman for warnings. |
| "Fragments are rude" | User-triggered, not standard. Smart-caveman, not caveman. |

## Contract

### INPUT
- **Required:** user trigger (pattern list above).
- **Optional:** domain context (project name + domain
  vocabulary stays).
- **Context:** no cross-refs needed — the mode switch is
  self-contained.

### OUTPUT
**DELIVERS:**
- Active mode until "stop caveman".
- Compressed responses per the persistence rule.
- Auto-clarity drops on security / irreversible / multi-step.

**DOES NOT DELIVER:**
- No content loss — substance stays.
- No code compression — syntax exact.
- No mode persistence across sessions (boot resets to normal).

**ENABLES:**
- Long-session token-cost reduction.
- Quick status updates without pleasantry overhead.
- Structured output lists (findings / tasks / etc) without
  filler.

### DONE
- Mode trigger recognized.
- Compression active from the trigger turn on.
- Persistence across all subsequent responses.
- Auto-clarity exception active in destructive / security /
  multi-step cases.
- Mode off on explicit user instruction.

### FAIL
- **Retry:** pattern drift recognized → re-tighten compression
  on the next turn.
- **Escalate:** the user complains about loss of clarity →
  mode off, clarification.
- **Abort:** the user says "stop caveman" / "normal mode" →
  revert.

## See also

- `skills/return_summary/SKILL.md` — separate format skill, NOT
  a mode switch.
- `skills/_protocols/piebald-budget.md` — file-budget
  discipline (orthogonal).
