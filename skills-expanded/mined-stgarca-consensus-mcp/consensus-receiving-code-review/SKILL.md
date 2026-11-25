<!-- Vendored from Superpowers (c) 2025 Jesse Vincent, github.com/obra/superpowers, v5.1.0 @ f2cbfbe, MIT. Adapted for consensus-mcp. -->
---
name: consensus-receiving-code-review
description: "Consensus-adapted: Use when receiving the sealed consensus panel findings, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation."
---

# Code Review Reception

> Consensus has precedence at decision gates (see the consensus bootstrap / consensus-workflow).

## Overview

Code review requires technical evaluation, not emotional performance.

**Core principle:** Weigh the SEALED consensus panel findings on merit. Verify before implementing. Ask before assuming. Technical correctness over social comfort.

**Consensus framing:** The findings you are receiving are the **sealed cross-family consensus panel** output (Workflow B), not a single reviewer's opinion. Weigh each finding on merit; record any dismissal with empirical evidence - **grep the cited content first.**

## The Response Pattern

```
WHEN receiving the sealed consensus panel findings:

1. READ: Complete sealed findings without reacting
2. UNDERSTAND: Restate each finding in own words (or ask)
3. VERIFY: Check against codebase reality - grep the cited content first
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment, or reasoned dismissal recorded WITH empirical evidence
6. IMPLEMENT: One item at a time, test each
```

## Weighing the Sealed Panel on Merit

The panel is cross-family and sealed, which raises the bar for dismissal but does not make it infallible.

```
FOR each sealed finding:
  1. grep the cited content FIRST - confirm the finding describes real code
  2. Check: Technically correct for THIS codebase?
  3. Check: Breaks existing functionality?
  4. Check: Reason for the current implementation?
  5. Check: Did the panel have full context?

IF a finding is correct:
  Implement it (no performative thanks - just fix it)

IF you dismiss a finding:
  Record the dismissal WITH empirical evidence (the grep output / test / cited lines).
  A dismissal without empirical evidence is not allowed - the sealed panel outweighs an unsupported objection.
```

## Forbidden Responses

**NEVER:**
- "You're absolutely right!" (explicit CLAUDE.md violation)
- "Great point!" / "Excellent feedback!" (performative)
- "Let me implement that now" (before verification)
- Dismissing a sealed finding with no grep / no evidence

**INSTEAD:**
- Restate the technical finding
- Ask clarifying questions
- Push back with technical reasoning AND empirical evidence if the finding is wrong
- Just start working (actions > words)

## Handling Unclear Findings

```
IF any finding is unclear:
  STOP - do not implement anything yet
  ASK for clarification on unclear items

WHY: Items may be related. Partial understanding = wrong implementation.
```

**Example:**
```
Sealed panel: "Fix findings 1-6"
You understand 1,2,3,6. Unclear on 4,5.

[x] WRONG: Implement 1,2,3,6 now, ask about 4,5 later
[ok] RIGHT: "I understand findings 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

## Evaluating Sealed Panel Findings

```
BEFORE implementing:
  1. grep the cited content FIRST
  2. Check: Technically correct for THIS codebase?
  3. Check: Breaks existing functionality?
  4. Check: Reason for current implementation?
  5. Check: Works on all platforms/versions?
  6. Check: Did the panel have full context?

IF a finding seems wrong:
  Push back with technical reasoning + the empirical evidence you gathered

IF you can't easily verify:
  Say so: "I can't verify this without [X]. Should I [investigate/ask/proceed]?"

IF a finding conflicts with prior architectural decisions:
  Stop and discuss first
```

**Rule:** The sealed cross-family panel is weighty - be skeptical, but check carefully, and never dismiss without evidence.

## YAGNI Check for "Professional" Features

```
IF the panel suggests "implementing properly":
  grep codebase for actual usage

  IF unused: "This endpoint isn't called. Remove it (YAGNI)?"
  IF used: Then implement properly
```

## Implementation Order

```
FOR multi-item findings:
  1. Clarify anything unclear FIRST
  2. Then implement in this order:
     - Blocking issues (breaks, security)
     - Simple fixes (typos, imports)
     - Complex fixes (refactoring, logic)
  3. Test each fix individually
  4. Verify no regressions
```

## When To Push Back (with recorded evidence)

Push back when:
- A finding breaks existing functionality
- The panel lacked full context
- It violates YAGNI (unused feature)
- It's technically incorrect for this stack
- Legacy/compatibility reasons exist
- It conflicts with architectural decisions

**How to push back:**
- Use technical reasoning, not defensiveness
- grep the cited content and quote it
- Reference working tests/code
- Record the dismissal WITH the empirical evidence in the consensus record

## Acknowledging Correct Findings

When a finding IS correct:
```
[ok] "Fixed. [Brief description of what changed]"
[ok] "Good catch - [specific issue]. Fixed in [location]."
[ok] [Just fix it and show in the code]

[x] "You're absolutely right!"
[x] "Great point!"
[x] "Thanks for catching that!"
[x] "Thanks for [anything]"
[x] ANY gratitude expression
```

**Why no thanks:** Actions speak. Just fix it. The code itself shows you heard the finding.

**If you catch yourself about to write "Thanks":** DELETE IT. State the fix instead.

## Gracefully Correcting Your Pushback

If you pushed back and were wrong:
```
[ok] "The panel was right - I checked [X] and it does [Y]. Implementing now."
[ok] "Verified this and the finding is correct. My initial understanding was wrong because [reason]. Fixing."

[x] Long apology
[x] Defending why you pushed back
[x] Over-explaining
```

State the correction factually and move on.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | State requirement or just act |
| Blind implementation | Verify against codebase first |
| Batch without testing | One at a time, test each |
| Assuming the panel is right | Check if it breaks things - grep first |
| Dismissing without evidence | Record dismissals WITH empirical evidence |
| Avoiding pushback | Technical correctness > comfort |
| Partial implementation | Clarify all items first |
| Can't verify, proceed anyway | State limitation, ask for direction |

## Real Examples

**Performative Agreement (Bad):**
```
Sealed panel: "Remove legacy code"
[x] "You're absolutely right! Let me remove that..."
```

**Technical Verification (Good):**
```
Sealed panel: "Remove legacy code"
[ok] "Grepped it... build target is 10.15+, this API needs 13+. Need legacy for backward compat. Current impl has wrong bundle ID - fix it or drop pre-13 support?"
```

**YAGNI (Good):**
```
Sealed panel: "Implement proper metrics tracking with database, date filters, CSV export"
[ok] "Grepped codebase - nothing calls this endpoint. Remove it (YAGNI)? Or is there usage I'm missing?"
```

**Unclear Item (Good):**
```
Sealed panel: "Fix findings 1-6"
You understand 1,2,3,6. Unclear on 4,5.
[ok] "Understand 1,2,3,6. Need clarification on 4 and 5 before implementing."
```

## GitHub Thread Replies

When replying to inline review comments on GitHub, reply in the comment thread (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as a top-level PR comment.

## The Bottom Line

**The sealed consensus panel = findings to weigh on merit, not orders to follow blindly - and not opinions to wave away.**

Grep the cited content. Verify. Question. Then implement, or dismiss WITH empirical evidence.

No performative agreement. Technical rigor always.
