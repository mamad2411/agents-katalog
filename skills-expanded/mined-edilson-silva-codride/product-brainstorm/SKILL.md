---
name: product-brainstorm
description: Structured, adversarial brainstorm for a product or business decision
---

# Product Brainstorm

This skill runs a structured brainstorming session for a product, feature, or business decision.

The user's request should name the topic — a product idea, a feature, or a business/technical decision with business impact. If it's too vague to work with ("brainstorm something"), ask what problem or opportunity is being explored before proceeding.

## Phase 1: Context

Before brainstorming, you should:

1. **Read the relevant master docs** (if they exist): `docs/business-context/PRODUCT_STRATEGY.md`, `docs/business-context/CUSTOMER_PERSONAS.md`, `docs/business-context/COMPETITIVE_LANDSCAPE.md`, and any project PRD.
2. **Understand the topic**: is this a new product? A new feature? A technical decision with business impact? A strategic pivot?
3. **Ask the human for initial context**: What problem are we trying to solve? What triggered this discussion (customer pain, opportunity, competition)? Are there known constraints (time, budget, technical resources)? How mature is this idea (early, half-formed, nearly ready)?

## Phase 2: Divergent exploration

Your job here is to **expand the thinking**:

**Socratic questioning** — ask 5-7 provocative questions that challenge assumptions: "Why solve this now?" "What if we do nothing — what's the opportunity cost?" "Who else has tried this, and why did they succeed or fail?" "What's the riskiest bet here?" "How does this connect to the long-term vision?"

**Generate alternatives** — for the topic, produce at least 3 different approaches, each with: description, 3-5 pros, 3-5 cons, estimated effort (High/Medium/Low), estimated impact (High/Medium/Low), key risks, and the assumptions that need to hold for it to work.

**Trade-off analysis** — for each alternative, map trade-offs across dimensions like speed vs. quality, scope vs. depth, innovation vs. predictability, cost vs. differentiation, short-term vs. long-term.

**Stakeholder analysis** — for each alternative, consider impact on customers/users, the engineering team (implementation complexity), the business team (goal alignment), and partners/integrations (external dependencies).

## Phase 3: Structured convergence

**Decision matrix**: build a comparison across criteria such as strategic alignment, technical feasibility, customer impact, expected ROI, and delivery speed. Ask the human which weights matter for this decision.

**Risk analysis**: for the top 2-3 alternatives, assess technical risk, market risk, operational risk, and strategic risk.

**"What if...?" scenarios**: explore extremes — half the time, double the budget, a competitor ships this tomorrow, this fails completely.

## Phase 4: Grounded recommendation

1. Synthesize what emerged: summarize the key insights, highlight patterns.
2. Make a recommendation: which alternative, why (grounded in the discussion), and what the next actions are.
3. Identify information gaps: what still needs validating, what research/experiments should happen next.

## Phase 5: Documentation

Save the session to `docs/business-context/brainstorm/<topic-slug>-<YYYY-MM-DD>.md`, containing: context, each alternative explored (with the structure above), the trade-off comparison, the risk matrix, the scenarios explored, the recommendation with its rationale and key assumptions, next steps, open questions, and the main learnings from the session.

⛔ **After documenting the session, stop and ask the human for feedback. Don't automatically move on to implementation or PRD creation — wait for the human to decide the next step.**

## Tools

During brainstorming, you can and should:
- Use web search (or Perplexity, if available) to research benchmarks, market trends, and similar use cases.
- Use Context7 to check how other companies/products solved similar problems.
- Consult the master docs to stay strategically aligned.
- Check `COMPETITIVE_LANDSCAPE.md` and `CUSTOMER_PERSONAS.md` to validate fit.

## Operating principles

- **Be provocative, not agreeable** — challenge ideas, including the human's.
- **Question assumptions** — "why do we assume that?"
- **Present counter-arguments** — for every pro, show a con.
- **Force prioritization** — "if you could only do one, which would it be?"
- **Validate with data**, not just intuition, when possible.
- **Think in extremes** — explore both optimistic and pessimistic scenarios.
- **Connect to context** — always reference the master docs and strategy.
- **Document the reasoning** — the "why" matters more than the "what".

Don't: agree quickly without questioning, accept the first solution as final, ignore real constraints, make assumptions without validating them, or skip documenting the session.

## Fits into the rest of the pipeline as

```
product-brainstorm "add real-time notifications"       # structured exploration → decision
product-collect "implement push notifications via WebSockets"   # if we proceed, collect detailed requirements
product-validate "notifications against architecture"  # validate against master docs
product-spec "PRD: notification system"                # write the spec
engineer-context feat/real-time-notifications           # start implementation
engineer-architecture feat/real-time-notifications       # design it
```
