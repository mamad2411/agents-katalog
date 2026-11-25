---
name: matz-psychological-targeting
description: "Design or audit consent-based psychological personalization using Sandra Matz's public research; use when connecting audience needs, digital signals, message or product fit, and recipient outcomes."
---

# Psychological Targeting

Based on Sandra Matz's public method. Not affiliated with or endorsed by Sandra Matz.

## When to use

Use this skill to design or review a personalized invitation, recommendation, campaign, or behavior support intervention when psychological needs could change what people receive. It also applies when someone proposes personality inference from digital traces or claims that tailored messages improve decisions. Start with a concrete audience and goal, rather than a dataset looking for a use. Matz distinguishes gaining psychological insight from using it to influence choices, and describes both helpful and exploitative applications. [S1] [S2]

Produce a psychological personalization decision brief, including usable variants or recommendations and a plan to evaluate them. For an audit, describe the existing system in the same fields and identify necessary corrections. The package translates public research into an operational workflow; its controls are implementation recommendations, not a questionnaire, clinical diagnostic method, legal assessment, or verbatim protocol published by Matz. Source attribution and evidence limits live in [references/method.md](references/method.md).

## Procedure

1. **Set the decision boundary.** Read method rule M1 in [references/method.md](references/method.md). Identify the recipient's stated goal, sponsor objective, intended behavior, context, and decision owner. State conflicts and missing information. Do not equate a sponsor's sales target with a recipient benefit. Use the brief fields in [templates/output-template.md](templates/output-template.md).

2. **Separate insight from influence.** Follow M2 in [references/method.md](references/method.md). Write what the system would estimate and what it would change. Require separate evidence for signal validity and intervention effectiveness; accurate prediction alone establishes neither permission nor benefit.

3. **Screen the proposed use.** Apply M3 in [references/method.md](references/method.md). Redirect designs that exploit vulnerability, discriminate, or covertly steer critical civic choices. Offer a transparent route using volunteered preferences, consistent facts, and recipient control. Document the reason rather than drafting an exploitative variant.

4. **Inventory evidence and permission.** Use M4 in [references/method.md](references/method.md) and the signal table in [templates/output-template.md](templates/output-template.md). Distinguish deliberate self-presentation from incidental traces. Record provenance, purpose, permission, retention, and expected use; do not interpret public availability as consent to profiling.

5. **Choose the smallest useful signal.** Apply M5 in [references/method.md](references/method.md). Prefer a volunteered goal or current preference when sufficient. Select a trait only when its connection to this offer changes a decision. Preserve uncertainty and avoid treating a temporary preference as a permanent personality label.

6. **Check inference validity.** Consult M6 in [references/method.md](references/method.md). Specify the reference measure, population, age of evidence, subgroup limitations, and fallback for missing or unreliable signals. If validation is absent, mark the proposal as a hypothesis and keep a generic route available.

7. **Choose the fit strategy.** Use M7 in [references/method.md](references/method.md). Decide whether to adapt a message for a fixed audience, select a genuinely suitable product or experience, or combine both. Explain the mechanism. Use the two illustrations in [examples/worked-examples.md](examples/worked-examples.md) when the distinction is unclear.

8. **Draft comparable alternatives.** Follow M8 in [references/method.md](references/method.md). Produce a generic baseline and supported variants. Adapt framing or presentation while preserving facts, price, limitations, and available choices. Ask whether independent readers would perceive the intended difference without needing personality labels.

9. **Build recipient controls.** Apply M9 in [references/method.md](references/method.md). Supply a plain explanation, preference correction, personalization off switch, and access to alternatives. Specify how unnecessary collection is avoided. Consider local processing when architecture is in scope; do not claim it guarantees privacy.

10. **Plan a credible comparison.** Use M10 in [references/method.md](references/method.md) and the evaluation fields in [templates/output-template.md](templates/output-template.md). Predefine mechanism, primary outcome, baseline, allocation, observation period, and harm limits. Compare matched and mismatched conditions only when appropriate and ethical.

11. **Review outcomes and revise.** Apply M11 and M12 in [references/method.md](references/method.md). Separate attention, action, and recipient welfare; inspect differences across segments. Choose proceed, revise, generic fallback, or stop. State inconclusive evidence plainly and never promise a universal uplift.

12. **Deliver the reviewed brief.** Complete [templates/output-template.md](templates/output-template.md), then pass [checklists/review-checklist.md](checklists/review-checklist.md). Mark unresolved deployment conditions and cite only supported methodological claims using [references/sources.md](references/sources.md). A finished brief does not itself authorize collection, experiments, or publication.

## Files in this skill

- [SKILL.md](SKILL.md): Entry point, applicability, and the agent's main loop.
- [references/method.md](references/method.md): Detailed rules, evidence limits, expert warnings, and edge cases.
- [references/sources.md](references/sources.md): Eight fetched public sources and their specific contributions.
- [examples/worked-examples.md](examples/worked-examples.md): Two invented before-and-after illustrations with rule explanations.
- [templates/output-template.md](templates/output-template.md): Fill-in decision brief with field guidance and evaluation plan.
- [checklists/review-checklist.md](checklists/review-checklist.md): Pass/fail review criteria, common failures, and practical fixes.
