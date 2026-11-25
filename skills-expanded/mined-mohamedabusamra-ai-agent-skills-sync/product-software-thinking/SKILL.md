---
name: product-software-thinking
description: Apply product-first thinking to software decisions — validate before building, let user goals drive technical choices, ship small, and measure impact. Use when planning features, making architecture decisions, scoping work, or when the tension between engineering and product needs resolving.
---

# Product & Software Thinking

Drawn from: *Design of Everyday Things* (Norman), *Theory of Fun* (Koster), *Art of Game Design* (Schell), *Design Sprint* (Banfield), *The Laws of Simplicity* (Maeda), and the intersection of software engineering with product development.

## The Core Question Before Any Technical Decision

> **"Are we building the right thing, or just building the thing right?"**

Building it right (engineering quality) matters — but only after confirming the right thing is being built. Always validate the problem before investing in the solution.

**Ask before scoping any feature:**
1. What user problem does this solve? Can you state it in one sentence from the user's perspective?
2. What is the smallest version that proves whether this solves the problem?
3. What would users do differently if this didn't exist? If the answer is "nothing much" — stop.
4. How will we know if it worked? (Define success before building, not after)

## Validate Before Building

From Design Sprint (Banfield) and iterative design (Fullerton):

```
Idea → Paper sketch → User test (5 people) → Decision → Build → Ship → Measure
```

Never:
```
Idea → 3 months of engineering → Ship → Discover nobody wanted it
```

**Minimum viable test:**
- A paper sketch can reveal 80% of design problems
- A Figma prototype can reveal the rest before a line of code is written
- 5 user tests reveal ~85% of usability issues
- If you can't describe how you'll test whether this feature worked — you're not ready to build it

## User Goals Drive Technical Decisions

Norman's principle: design for the user's mental model, not the system's internal model.

**When making a technical decision, map it to user impact:**

| Technical choice | User impact question |
|---|---|
| Add a new API endpoint | Does this enable a user action they couldn't do before? |
| Refactor a service | Does this make the user experience faster or more reliable? |
| Add a database index | Does this reduce latency the user perceives? |
| Choose microservices vs monolith | Which helps us ship user value faster and more reliably? |
| Add abstraction layer | Does this reduce the chance users experience bugs? |

**Abstraction for its own sake has no user value. Complexity has a cost: slower delivery, more bugs, harder onboarding.**

## Progressive Disclosure: Match Complexity to User Readiness

From Maeda (Laws of Simplicity) and Schell (challenge-skill balance):

Never show all features to all users at once. Reveal complexity as users grow into it.

```
New user:    Show 3 core actions. Hide everything else.
Engaged user: Reveal intermediate features as they demonstrate readiness.
Power user:   Expose full capability — keyboard shortcuts, bulk actions, APIs.
```

**Apply in software:**
- Default settings should be the right choice for 80% of users
- Advanced options exist but are not visible by default
- Error messages should be simple for end users, detailed in logs for developers
- API responses: sensible defaults with opt-in for extended data

## Ship Small, Learn Fast

```
Large batch → Long feedback loop → Wrong direction for months
Small batch → Fast feedback loop → Course-correct weekly
```

**Sizing rule:** If a feature takes more than 2 weeks to build, it can almost certainly be split into two or more pieces that each deliver independent user value.

**The right question when scoping:**
- "What's the smallest version of this that a real user could use?"
- Not: "What's the full vision?"

**Phasing principle:**
```
Phase 1: Make it work (users can do the thing)
Phase 2: Make it right (clean up the implementation)
Phase 3: Make it fast (optimise only where users feel the pain)
```
Never skip Phase 1 to get to Phase 3.

## Engagement Loops (from Game Design)

Every product has engagement loops — understanding them prevents building features that look good but don't retain users.

**Core loop:** The repeated action cycle. Keep it tight and rewarding.
```
Action → Immediate feedback → Sense of progress → Motivation to repeat
```

**When designing a feature, trace the loop:**
- What action does the user take?
- What immediate feedback do they get? (If none — add it)
- What sense of progress or value do they receive?
- What motivates them to return?

**If you can't trace the loop, the feature is probably a solution looking for a problem.**

## Intrinsic Value Over Artificial Engagement

From Koster (Theory of Fun):

- **Intrinsic:** Users return because the product genuinely solves a problem or creates real value
- **Extrinsic:** Users return because of streaks, badges, notifications, fear of losing progress

Extrinsic hooks are brittle. When the reward stops, the behaviour stops.

**Build for intrinsic value first:**
- Does the product make users better at something they care about?
- Does it save them real time or real effort?
- Would users pay for it if all the gamification was removed?

Extrinsic mechanics (streaks, notifications) are fine as onboarding aids — not as the core value proposition.

## The Build-Measure-Learn Filter

Before adding any feature to a roadmap:

```
Build  → What is the smallest thing we can build to test this?
Measure → How will we measure whether it worked? (metric, before/after)
Learn  → What decision will we make based on the result?
```

If you can't answer all three — the feature is not ready to be built.

## Product vs Engineering Tensions — How to Resolve Them

| Situation | Right call |
|---|---|
| PM wants feature fast, engineer wants it clean | Ship the feature with acceptable quality; schedule the cleanup as tech debt with a concrete date |
| Engineer wants to refactor before adding feature | Refactor only the parts you're touching; don't refactor the world before shipping value |
| Disagreement on what users want | Run 5 user interviews or a 1-week design sprint before deciding |
| Feature is technically complex but user-simple | Invest in the engineering — user simplicity is worth technical complexity |
| Feature is technically simple but adds UI clutter | Reject or defer — user simplicity is worth delaying features |

## Code Quality Is a Product Decision

Bad code is not just a technical problem — it's a product problem:
- Slow feature delivery → users wait longer for value
- Bugs → users lose trust
- Hard to onboard new engineers → fewer people building for users
- No tests → fear of change → product stagnates

From Clean Code: **code is read 10x more than it is written.** Write for the next engineer, who is also a product investment.

## Decision Checklist Before Building Anything

- [ ] Can I state the user problem in one sentence without mentioning technology?
- [ ] Have we validated this with at least one real user or a sketch test?
- [ ] Is this the smallest version that delivers real value?
- [ ] Do we have a metric to know if it worked?
- [ ] Does this fit the core loop — does it make the product more valuable to return to?
- [ ] Are we solving for intrinsic value, not just adding engagement mechanics?
- [ ] What does this NOT do? (Scope is defined by exclusion as much as inclusion)
