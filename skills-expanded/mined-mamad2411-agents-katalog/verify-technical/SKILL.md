---
name: verify-technical
description: Use for a technical incident, disputed diagnosis, bug fix, or claim that a change works. Reproduce, isolate, test competing causes, and repeat the original check before reporting verification.
argument-hint: "[symptom, diagnosis, or change to verify]"
---

# Verify technical work

Use the tools and repository instructions available in the current workspace.
This workflow supplies no provider access and never authorizes a destructive
probe, deployment or external message.

1. **Define the claim.** State the symptom, affected process/environment/version,
   expected result and the observation that would establish success. Separate
   repair, local verification, deployment and production verification.
2. **Reproduce or inspect.** Run the narrowest safe reproduction, or inspect
   current evidence if reproduction is unavailable. Record the command/check,
   result and scope in the conversation. An unavailable reproduction is a gap.
3. **Compare causes.** Keep two or three plausible explanations. For each,
   identify a discriminating observation. Test the strongest supported causes;
   stop broadening when the evidence is sufficient for the requested scope.
4. **Change the owning layer.** Inspect applicable instructions and consumers
   first. Make the smallest justified change. Do not change unrelated settings
   to make the reproduction disappear.
5. **Repeat the original check.** Use the same input and affected environment
   after the change. Where possible, demonstrate fail-before/pass-after. A new
   test that never exercised the failure does not establish that it is fixed.
6. **Check the boundary.** Run relevant regression checks and required repo gates.
   A local pass does not establish CI, deployment or another machine's state.
   Verify those separately only when they are in the requested scope.
7. **Reconcile corrections.** When new evidence changes the diagnosis, revisit
   dependent recommendations. If the user disputes a claim, recheck the evidence
   before agreeing or defending it. Do not replace one unsupported cause with
   another.

Do not require new tool calls to repeat still-valid, directly checked evidence.
Keep failed, partial and unavailable checks visible. File excerpts and sampled
rows establish only the portion observed, including when no warning is emitted.

Before drafting, check every material assertion, including intermediate bridges:
could a plausible alternative explain the observation while that assertion is
false? If the evidence cannot distinguish it, keep it as a hypothesis or leave
it unresolved. Focus on alternatives that affect the requested conclusion;
do not hedge a directly supported narrow fact because of merely imaginable doubts.

For example, unspecified passing tests establish a test pass, not that the
incident was exercised or fixed locally. An older build does not establish that
a particular patch is absent; inspect its contents or deployment identity.
If a bridge is removed, restate the verdict on surviving evidence or downgrade
it too. A correct verdict does not excuse an unsupported reason.

Lead with the supported conclusion and uncertainty. Preserve that same scope in
short status labels, summaries and follow-ups. End substantive diagnoses
or verification claims with:

- **Checked:** actual checks, outcomes and scope; explicitly say none if none ran.
- **Gap:** unresolved causes, unavailable checks or untested environments.
- **Next:** the smallest useful check or action, or none within the agreed scope.

This is an advisory workflow and model-written summary, not an independent
accuracy certificate. Use claim-fidelity for a detailed claim-by-claim audit.
