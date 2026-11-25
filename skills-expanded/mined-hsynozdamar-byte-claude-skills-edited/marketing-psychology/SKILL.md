---
name: marketing-psychology
description: "Psychological principles and mental models for marketing. Use when applying behavioral science such as anchoring, social proof, scarcity or loss aversion to marketing decisions."
metadata:
  version: 2.0.0
---

# Marketing Psychology

Pick the few principles that explain the observed behavior, then turn each into a specific change to the page, offer or flow. Read `.agents/product-marketing.md` (or `.claude/product-marketing.md`) first when it exists, to fit audience and product.

Work in this order:
1. Name the behavior to change and what currently blocks it. Ask where in the journey it sits (awareness, consideration, decision), what the customer believes beforehand, and whether it was tested with real customers.
2. Choose 1 to 3 models from the table below. More than that is a list, not a diagnosis.
3. State the psychology in one line, then the concrete application (a copy line, a layout change, a default, a test).
4. Propose an A/B test for the hypothesis; psychology explains, data decides.

## Which model for which problem

| Challenge | Start with |
|---|---|
| Low conversions | Hick's Law, Activation Energy, BJ Fogg (motivation x ability x prompt), friction |
| Price objections | Anchoring, Framing, Mental Accounting, Loss Aversion |
| Building trust | Authority, Social Proof, Reciprocity, Pratfall Effect |
| Urgency | Scarcity, Loss Aversion, Zeigarnik |
| Churn | Endowment, Switching Costs, Status-Quo Bias |
| Growth stalling | Theory of Constraints, Local vs Global Optima, Compounding |
| Decision paralysis | Paradox of Choice, Default Effect, Nudge Theory |
| Onboarding | Goal-Gradient, IKEA Effect, Commitment and Consistency |

## Pricing specifics worth remembering

- Charm endings (.99) signal value; round prices ($500) signal premium. Match the positioning.
- Rule of 100: under $100 a percentage discount looks bigger ("20% off"); over $100 an absolute one does ("$100 off").
- Three tiers with the target in the middle; the top tier anchors, the bottom one frames.
- Free is a different category from $1: lead with a free tier or trial when adoption is the goal.

## Applying ethically

Urgency and scarcity only when real (true deadline, true stock). Defaults and opt-out steer people to what suits them, with cancellation as easy as signup. Test copy on people outside the team (curse of knowledge).

## References

- [references/buyer-psychology.md](references/buyer-psychology.md): biases and persuasion principles with applications (social proof, loss aversion, anchoring, decoy, reciprocity, commitment, framing, defaults). Load when you need a principle's definition or application.
- [references/pricing-and-design-models.md](references/pricing-and-design-models.md): price perception effects, Hick's Law, AIDA, Fogg, EAST, COM-B, activation energy, North Star, Cobra effect. Load for price framing or behavior design.
- [references/strategy-models.md](references/strategy-models.md): first principles, JTBD, Pareto, constraints, opportunity cost, feedback loops, flywheel, network effects, switching costs. Load for prioritization and growth strategy questions.

Page-level application goes to `cro`; writing with these principles goes to `copywriting`.
