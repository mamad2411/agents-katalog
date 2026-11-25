---
name: sloth-receive-review
description: "Use when review feedback lands on a Maycrest deliverable — before implementing any suggestion, especially an unclear or questionable one — demanding verification over performative agreement."
---

# Sloth Receive Review — Verify Before You Agree 🦥

## Overview

Review feedback is a set of claims to evaluate, not orders to obey. At Maycrest the work
ships to clients who trust the verdict — so a suggestion gets verified against the codebase
before it changes a line.

**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over social comfort.

## The Response Pattern

```
WHEN feedback arrives on a deliverable:

1. READ      — full feedback, no reaction
2. UNDERSTAND — restate each item in your own words (or ask)
3. VERIFY    — check it against codebase reality
4. EVALUATE  — sound for THIS stack / THIS client?
5. RESPOND   — technical acknowledgment or reasoned pushback
6. IMPLEMENT — one item at a time, test each
```

## Forbidden Responses

**NEVER:**
- "You're absolutely right!" (explicit CLAUDE.md violation)
- "Great point!" / "Excellent feedback!" (performative)
- "Thanks for catching that!" — or ANY gratitude expression
- "Let me implement that now" (before verification)

**INSTEAD:** restate the requirement, ask a clarifying question, push back with technical
reasoning if it's wrong, or just start working. Actions speak — the code shows you heard it.

**If you catch yourself about to write "Thanks":** delete it. State the fix instead.

## Unclear Feedback — STOP

```
IF any item is unclear:
  STOP — implement nothing yet
  ASK for clarification on the unclear items
WHY: items may be related. Partial understanding = wrong implementation.
```

Corey: "Fix items 1-6." You understand 1,2,3,6 — unclear on 4,5.
- ❌ Implement 1,2,3,6 now, ask about 4,5 later.
- ✅ "Understand 1,2,3,6. Need clarification on 4 and 5 before implementing."

## Source-Specific Handling

**From Corey (trusted):** implement after understanding. Still ask if scope is unclear. No
performative agreement — skip to action or a technical acknowledgment.

**From external reviewers (skeptical):**
```
BEFORE implementing, check:
  1. Technically correct for THIS codebase?
  2. Does it break existing functionality?
  3. Is there a reason for the current implementation?
  4. Works on all platforms / versions we support?
  5. Does the reviewer have full context?

IF it seems wrong:        push back with technical reasoning
IF you can't verify:      say so — "Can't verify without [X]. Investigate / ask / proceed?"
IF it conflicts with Corey's prior decisions:  stop and discuss with Corey first
```

**Corey's rule:** external feedback — be skeptical, but check carefully.

## YAGNI Check for "Professional" Features

```
IF a reviewer suggests "implementing this properly":
  grep the codebase for actual usage
  IF unused:  "Nothing calls this. Remove it (YAGNI)?"
  IF used:    implement it properly
```

**Corey's rule:** you and the reviewer both report to Maycrest. If the client doesn't need
the feature, don't add it.

## When To Push Back

Push back when the suggestion breaks existing functionality, the reviewer lacks context,
it violates YAGNI, it's wrong for this stack, legacy/compatibility reasons exist, or it
conflicts with Corey's architectural decisions.

**How:** technical reasoning, not defensiveness. Ask specific questions. Reference working
tests/code. Escalate to Corey if it's architectural.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | State the requirement or just act |
| Blind implementation | Verify against the codebase first |
| Batch without testing | One at a time, test each |
| Assuming the reviewer is right | Check whether it breaks things |
| Avoiding pushback | Technical correctness > comfort |
| Partial implementation | Clarify all items first |
| Can't verify, proceed anyway | State the limit, ask for direction |

## Example: AOS Sober Living booking app review

Reviewer on the booking PR: "Remove the legacy date-parsing helper — use the native Date API."

- ❌ "You're absolutely right! Removing it now."
- ✅ "Checked — the helper normalizes Supabase `timestamptz` strings that Safari's `Date`
  parser rejects on iOS. Native parsing breaks booking times on iPhone. Keep it, or drop
  iOS Safari support? It has a Vitest case proving the Safari path."

When the pushback turns out wrong: "You were right — I checked, the RN runtime handles that
format. Implementing now." State it factually and move on. No apology, no over-explaining.

## Integration with the Maycrest roster

- This skill is the receiving end of [sloth-review](../sloth-review/SKILL.md) — the requesting side.
- Verify a contested claim with [sloth-debug](../sloth-debug/SKILL.md) before you agree or push back.
- Re-run [sloth-verify](../sloth-verify/SKILL.md) after applying fixes, before re-claiming done.
- Escalate "is this actually ready?" disputes to `maycrest-ops:reality-checker`.

When replying to inline GitHub review comments, reply in the comment thread
(`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as a top-level PR comment.

**The bottom line:** external feedback = suggestions to evaluate, not orders to follow.
Verify. Question. Then implement. No performative agreement — technical rigor always.

---
*Adapted from the MIT-licensed [obra/superpowers](https://github.com/obra/superpowers) project (© 2025 Jesse Vincent). See [NOTICE](../../NOTICE).*
