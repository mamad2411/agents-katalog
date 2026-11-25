---
name: just-stop
description: Stops "just one more" small tweaks that add scope without changing the outcome. Use when named (just-stop), or when about to implement extra polish, cleanup, or drive-by fixes beyond the stated goal.
---

# just-stop

True craft is knowing when to stop. "One more small change" is usually how scope dies by a thousand cuts.

## When to apply

- User names this skill (`just-stop`)
- You are about to add "a few small tweaks," polish, cleanup, or drive-by fixes after the goal is already met
- A change is justified as "while we're here" or "this will help overall" but is not required for the stated outcome

## What matters

Identify the true goal / end state. Then ask:

1. Does this change move that goal from unmet → met?
2. Or does it only make an already-met goal nicer?

If (2), stop. Say what you'd tweak and leave it optional.

This is not anti-quality. Necessary fixes still ship. Nice-to-haves wait.

## Operating rules

- **Goal first**: Restate the required outcome in one line before adding work.
- **Challenge extras**: When you or the user propose another change, classify it as required vs optional. Be explicit.
- **Ship at the value cliff**: Stop where further work turns into icing — renames for taste, comment churn, speculative refactors, decorative CSS, "improve README a bit," extra error paths nobody asked for.
- **Necessary still means necessary**: Bugs that block the goal, broken verification, or missing DoD items are not "just one more." Fix those.
- **Offer, don't sneak**: If optional tweaks are genuinely valuable, list them after you're done. Don't implement them by default.

## Response shape

When stopping yourself or the user:

```
Done for the goal: [one line]

Optional (not doing unless you want them):
- [tweak]
- [tweak]
```

When something is truly required:

```
Still required:
- [change] — [why the goal fails without it]
```

## Anti-patterns

- Implementing polish after DoD / acceptance already passes
- Batching unrelated cleanup into a finished task
- Treating taste differences as defects
- Expanding a fix into a rewrite
- Confusing "helpful" with "necessary"
