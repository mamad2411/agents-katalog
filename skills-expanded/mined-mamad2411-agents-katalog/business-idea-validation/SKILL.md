---
name: business-idea-validation
description: Validate startup and business ideas with founder/company feasibility gates, realistic market research, specialist/regulatory checks, investment requirements, and go/no-go recommendations before building landing pages or MVPs.
---

# Business Idea Validation

Use this portable skill when a user wants to validate a startup or business idea realistically. The goal is to decide the next evidence-based action: customer interviews, landing-page test, concierge validation, specialist diligence, capital planning, pause, or no-go.

## Rules

1. Run the founder/company reality gate before deep research unless the user already supplied the needed context.
2. Do not recommend a landing page by default; use it only for low-risk, reachable, testable offers.
3. Hard-gate specialist-heavy ideas early. Regulation, insurance, safety, professional advice, trust, or capital intensity can block or reshape validation.
4. Separate market desirability from ability to execute. A real market does not mean this founder/company can win.
5. Browse for current facts when facts can drift: laws, regulations, pricing, competitors, market data, incentives, and channel rules.
6. Name uncertainty, missing evidence, costs, and no-go triggers explicitly.
7. Treat software as cheap, but trust, expertise, compliance, distribution, and operations as costly until proven otherwise.

## Tracks

Classify the idea before external research:

| Track | Use When | Next Step |
| --- | --- | --- |
| `landing-page-test` | Low regulation, low trust burden, clear buyer, simple fulfillment. | Interviews, landing page, deposits, concierge demo. |
| `concierge-validation` | Value needs trust or customization but can be manually delivered. | Sell manually first; productize repeated workflow later. |
| `specialist-led-diligence` | Legal, medical, financial, construction, safety, insurance, certification, or licensed professionals matter. | Confirm specialist path, budget, risk, and legal boundaries before GTM. |
| `capital-intensive-diligence` | Hardware, property, infrastructure, inventory, or operational setup dominates cost. | Validate financing path and staged proof before demand research depth. |
| `marketplace-liquidity-diligence` | Two-sided supply/demand or trust marketplace. | Test wedge, cold start, supply quality, demand frequency, and referral economics. |
| `pause-or-no-go` | Founder lacks budget, access, credibility, legal path, or reachable customers. | Stop, narrow, or find missing partner/capital before research. |

## Workflow

1. **Intake**
   - Load `references/00-founder-reality-gate.md`.
   - Ask only questions that change the route or gate result.
   - Output the selected track, assumptions, blockers, and allowed next step.

2. **Research**
   - Load `references/01-method-stack.md` and `references/02-research-protocol.md`.
   - Use the minimum research depth that can change the decision.
   - Keep verified facts, inference, and source quality separate.

3. **Risk Gates**
   - Load `references/03-gates-and-kill-criteria.md`.
   - Apply gates for founder fit, customer pain, market wedge, legal/specialist feasibility, distribution, economics, and evidence quality.

4. **Specialist Branch**
   - Load `references/05-regulated-specialist-ventures.md` when the idea touches regulated or high-trust domains.
   - Require specialist access, estimated cost, liability boundaries, and forbidden activities before recommending build or launch.

5. **Output**
   - Load `references/04-output-templates.md`.
   - Produce a concise memo or dossier with verdict: `Go`, `Conditional Go`, `Pause`, or `No-Go`.
   - If file output is requested, use `scripts/scaffold_dossier.py`.

## Common Mistakes

- Starting with competitor research before founder/company feasibility.
- Treating a landing page as universally cheap validation.
- Using broad TAM as proof of reachable market.
- Assuming AI removes non-software costs.
- Ignoring professional liability, trust, credentialing, insurance, or specialist access.
- Giving `Conditional Go` without naming the exact missing evidence and cheapest test.
