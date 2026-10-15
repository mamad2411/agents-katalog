---
name: spec-fortify
description: Examine a project spec after its decisions have been explored to find contradictions, gaps, accidental complexity, and other issues. Use as the final step in the spec-driven workflow to strengthen the spec before implementation begins.
---

# Spec Fortify

Use this skill for the fortification phase of the spec-driven workflow.

## Instructions

You are reviewing a project spec after its decisions have been resolved.

The user will reference a spec file. Read it in full.

## Check For

1. **Contradictions.** Do any resolved decisions conflict with each other or
   violate a stated constraint? Flag which decision to reopen.

2. **Gaps.** Is there something the resolutions assume but never explicitly
   decided? Add new pending decisions to the spec.

3. **Accidental complexity.** Read all resolutions as a whole. Is the total
   complexity proportional to the summary? Flag anything that crept in across
   sessions that nobody would have chosen deliberately. Suggest what to
   simplify or reopen.

4. **Security risks.** Do the current decisions introduce obvious security
   concerns, unsafe defaults, or unclear trust boundaries? Flag anything that
   needs an explicit decision or constraint.

5. **Scaling risks.** Scaling here means the system's ability to maintain
   acceptable performance and reliability as request volume, concurrency, or
   data size increases. Only flag concerns that are concrete and plausible
   from the spec as written.

6. **Verification steps.** Do the current decisions make clear how the
   implementation will be verified? Flag anything that leaves test coverage,
   runtime validation, or behavior checks too vague to plan confidently.

## Update the Spec

Don't add review notes or commentary to the spec file. If the review surfaces
something actionable, apply it directly to the spec with the user's approval.

Actionable changes include:

- adding a new pending decision
- reopening a resolved decision
- adding or clarifying a constraint
- moving explicitly deferred nice-to-haves into `Future Ideas`
