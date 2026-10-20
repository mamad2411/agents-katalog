---
name: consensus-arbitration
description: "When two or more agents disagree on a decision they each own a piece of, drive the conflict to a single decision via a fixed arbitration rule — never let the conflict silently linger."
---

# Consensus & arbitration

Multi-agent systems often have silent disagreements that surface as inconsistent outputs to the user. This skill resolves them on purpose.

## When to invoke

- Two agents propose conflicting plans for the same task.
- A reviewer agent (e.g., `shadow-code-reviewer`) and the author agent disagree on whether to ship.
- Two roles each claim ownership of the same artefact (a doc, a ticket, a code path).

## The arbitration rule

In priority order:

1. **Hard policy beats opinion.** If a policy or compliance constraint applies, that wins. Cite the policy explicitly.
2. **The role with the closest scope wins.** A frontend-developer wins on UI choice; a backend-developer wins on schema choice; a security-specialist wins on threat model. If unclear, the manager (`crew-manager-pattern`) decides.
3. **Existing precedent beats novelty.** If the codebase / playbook already has a pattern for this, keep it. Novelty needs explicit user buy-in.
4. **If still unresolved, escalate to a human.** Frame the decision as a short, neutral writeup with the two options, the trade-off, and your default if no answer arrives by a deadline (see `clarification-checkpoints`).

## The arbitration write-up

Whichever agent is hosting the arbitration writes one message:

```
Decision: <one sentence>
Rule applied: <which of the rules above, or "human escalation">
Loser's concern preserved: <one sentence — what we lose by not picking the other option, so we can revisit later>
Owner: <agent or human that will execute the decision>
```

## Anti-patterns

- Letting the conflict linger and producing inconsistent outputs.
- Two agents quietly editing the same file with conflicting intents.
- Skipping the loser's-concern note — that's what catches regressions in retrospectives.
