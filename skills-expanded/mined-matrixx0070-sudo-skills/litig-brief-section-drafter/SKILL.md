---
name: litig-brief-section-drafter
version: 1.0.0
description: Draft a section of a legal brief — statement of facts, argument, or standard of review — with proper structure and disciplined citation.
author: matrixx0070
tags: [litigation, brief-writing, motions, citation, appellate]
capabilities: []
---

## When to use
Use this when you need to draft a discrete section of a brief and want a clean structure and citation discipline. It covers the statement of facts, the standard of review, and argument sections built on a CRAC/IRAC skeleton. Good for motion practice and appellate briefs alike.

**Not for:** building the underlying timeline (see litig-chronology) or logging privileged documents (see litig-privilege-log-review).

## Method
1. Identify the section and its job: facts narrate neutrally-but-favorably with record cites; standard of review states the lens; argument persuades.
2. **Decision point:** If drafting the statement of facts, cite the record (declaration, exhibit, deposition) for every factual assertion; if drafting argument, lead each point with your conclusion, then rule, application, and conclusion (CRAC).
3. State the correct standard of review (de novo, abuse of discretion, clear error, substantial evidence) tied to the ruling being challenged.
4. Marshal authority: bind with mandatory precedent first, then persuasive; parenthetically explain each key case.
5. **Decision point:** If adverse controlling authority exists, address and distinguish it rather than omit it (candor duty); if only persuasive authority cuts against you, weigh whether to preempt.
6. Enforce citation discipline: pincites for every proposition, accurate quotations, correct signals, and verified good law.
7. ATTORNEY-ESCALATION gate: Route the drafted section to a supervising attorney for review before it is filed.

## Example
> Drafting the argument for a summary-judgment opposition, you open each point with the conclusion ("A genuine dispute exists on causation"), state the Celotex/Anderson standard, apply the deposition testimony with pincites, and distinguish the one controlling case against you, then route the section to the supervising attorney before filing.

## Pitfalls
- **Uncited facts:** Any factual assertion without a record cite is vulnerable to being struck or ignored.
- **Burying the conclusion:** Leading with rule instead of your position weakens persuasion.
- **Ignoring adverse authority:** Candor rules require disclosing directly adverse controlling precedent.
- **Stale citations:** Failing to verify a case is still good law risks citing overruled authority.

## Output format
```
BRIEF SECTION: [Statement of Facts | Standard of Review | Argument]
Heading (argumentative, one line)
CRAC:
  Conclusion: [...]
  Rule: [authority + pincite]
  Application: [facts + record cites]
  Conclusion: [...]
Adverse authority addressed: [case | distinction]
Attorney review: [name | date | status]
```

## Reference
Persuasive argument sections commonly follow CRAC/IRAC and use point headings that state a conclusion. The duty of candor (ABA Model Rule 3.3) requires disclosing legal authority in the controlling jurisdiction known to be directly adverse and not disclosed by the opponent. Citation form generally follows The Bluebook (or ALWD, or a court's local citation rules); provide a pincite for every proposition and use signals (see, cf., but see) accurately. Verify every authority remains good law (e.g., via a citator) before filing. Summary-judgment argument typically invokes the Celotex/Anderson/Matsushita trilogy under FRCP 56; standards of review differ by procedural posture and court. Formatting, length limits, and citation conventions vary by jurisdiction and local rule; confirm the governing rules. General information, not legal advice.
