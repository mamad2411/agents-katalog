---
name: feature-adoption-diagnosis
description: "Diagnose why a feature isn't getting adopted. Most features fail not because they're bad ideas but because of discoverability, onboarding, or positioning problems. Use when a shipped feature has low usage, a popular feature is declining, or deciding whether to kill, improve, or reposition something."
---

# Feature Adoption Diagnosis

Figure out why a feature isn't getting used — and what to do about it.

## How to use

- `/feature-adoption-diagnosis` Apply adoption diagnosis constraints to this conversation.
- `/feature-adoption-diagnosis <feature>` Diagnose adoption for the described feature.

## Constraints

### The Adoption Funnel
Every feature has its own funnel: Awareness → Discovery → First Use → Repeated Use → Habitual Use
- MUST identify which stage is failing before proposing fixes
- NEVER assume low usage means the feature is bad. It might be invisible.

### Stage Diagnosis

**Awareness failing**: user doesn't know it exists
- Check: where is it in the UI? Was it announced? Can new users discover it during onboarding?
- This is a marketing problem, not a product problem.

**Discovery failing**: user knows it exists but hasn't tried it
- Check: is there a clear trigger to try it? Is the first interaction effortless? Does it require behavior change?
- Reduce activation energy. Make the first interaction zero-friction.

**First use failing**: tried once, didn't come back
- Check: did the first experience deliver value? Was it confusing? Did it match expectations?
- Fix the empty state, simplify the flow, or set better expectations.

**Repeated use failing**: used a few times, not a habit
- Check: is it useful once or ongoing? Does it integrate into workflow? Any triggers to use again?
- Either add recurrence triggers or accept it's a point-solution feature.

### Root Cause Analysis
- Wrong audience: built for users who aren't your core. Check WHO is using it.
- Wrong timing: introduced too early or too late in the user journey
- Incremental value too low: improvement over existing way isn't big enough to justify switching
- Too complex: requires too much learning or configuration for the value delivered
- Not integrated: works in isolation but doesn't connect to the user's workflow

### Response Decision
MUST choose one:
- Double down: feature is valuable, problem is discovery or UX. Invest in visibility and ease.
- Refine: concept is right, execution needs work. Simplify or adjust target.
- Reposition: feature does something valuable but it's marketed or placed wrong.
- Sunset: low awareness, low first use, low repeat, no strong segment signal. Kill it.

### Metrics to Track
- Adoption rate: % of eligible users who tried it at least once
- Activation rate: % of first-time users who reached the feature's aha moment
- Retention rate: % who used it again within 30 days
- Impact on product retention: do feature adopters retain better overall?

### Anti-Patterns
- Assuming low adoption means the feature should be killed without diagnosing the stage
- Adding more features to compensate for poor adoption of existing ones
- Measuring adoption without segmenting by user type
- Shipping and forgetting — features need post-launch investment to drive adoption
