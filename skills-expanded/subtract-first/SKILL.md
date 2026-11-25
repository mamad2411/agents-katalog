---
name: subtract-first
description: "Use when work was just rejected as too much, too busy, confusing, or 'still not right' — a UI, a doc, an API, an over-built PR — and the instinct is to add something to fix it. Removes one thing and re-shows before adding anything, makes one change per look, and keeps a clean way back to the last accepted state."
---

# Subtract First

## The failure mode this fixes

The work gets rejected — "too busy," "I'm not following it," "still mid" — and the agent answers by adding. An explanatory panel for the confusing dashboard. A summary section for the document nobody finished. A wrapper and an option for the API that felt awkward. Every addition competes with what was already there, so the next round is worse, and the round after that is worse again.

The compounding version: three or four revisions get stacked before anyone looks. By the time the verdict is "this is worse than where we started," the changes are tangled together and the only clean exit is reverting all of it.

"It isn't working" is almost never a request for more. It's a report that something already present isn't earning its place. This skill makes removal the first move, and one look per change the rhythm.

## When to Use This Skill

- Feedback says the work is too much, cluttered, confusing, or just "not it," without naming a missing piece
- You're about to answer a rejection with a new element, section, option, or explanation
- A second round of feedback is harsher than the first — the additions are the problem
- Several revisions are queued up and none has been looked at yet
- A reviewer says a PR does too much

**Don't use when:** the feedback names a specific missing thing ("there's no legend," "it doesn't handle refunds") — add that, and only that. And not for a first draft nobody has reacted to; there's no signal yet to subtract against.

## Instructions

### 1. Read the rejection as a statement about what exists

Before proposing anything, restate the feedback as a claim about the current work: which parts would the reader not miss? "I'm not following the story" means the existing pieces aren't worth reading in their current number or order — not that a narrator is missing.

### 2. Remove one thing and re-show

Pick the weakest element — the panel nobody would ask for, the section that restates another, the parameter with one caller — and take it out. Show the result. A removal is cheap to judge and cheap to undo, and it often turns out to be the whole fix.

### 3. One change per look

Make a single change, then get it looked at before making the next. A verdict on one change is information; a verdict on five tangled changes is a coin flip about which one did the damage.

### 4. Don't explain the work inside the work

Captions, helper text, a "how to read this" block, a paragraph justifying the design — these are additions wearing a disguise. If the thing needs a guide to be understood, the thing is the problem. Fix or remove what's confusing instead of annotating it.

### 5. Keep a way back

Commit (or otherwise checkpoint) the last accepted state and each step after it. If two rounds in a row land worse, stop patching forward and return to the last state that was accepted, then try a different removal from there.

## Output format

```
FEEDBACK (restated as a claim about what exists)
  <what the reader would not miss>

REMOVED
  - <element> — why it wasn't earning its place

CHANGED (one, since the last look)
  - <the single change>

WAY BACK
  last accepted state: <commit / checkpoint>

NOT ADDED
  - <the addition you were tempted to make> — held until the removal is judged
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| Answering "too much" with more | The new element competes with everything already there. The complaint was about the total. |
| Stacking revisions before a look | Four changes, one verdict. Nobody can tell which change hurt, so all four get reverted. |
| The explanatory layer | A caption or guide added to justify the confusing part. Now there are two things to read. |
| Patching forward from a rejected state | Each fix inherits the previous round's mistakes. Go back to the last accepted state. |
| Subtracting the specific thing they asked for | If the feedback named a missing piece, add it. This skill is for unnamed dissatisfaction. |

## Mental Model

> When the work is rejected, the fix is usually already in it, buried. Take something away and look again before you reach for anything new.
