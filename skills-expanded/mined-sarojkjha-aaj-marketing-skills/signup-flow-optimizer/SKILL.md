---
name: signup-flow-optimizer
description: >-
  Use when the user wants to improve a signup, registration, trial-start or
  checkout flow — reducing form fields, cutting steps, or fixing where people
  abandon. Also use when the user mentions signup conversion, form abandonment,
  trial start rate, registration flow, checkout friction, or "people visit and
  don't sign up". Scores the flow's friction, ranks what to remove by what it's
  worth, and specifies the rebuilt flow.
license: MIT
metadata:
  search_description: "Improve a signup, trial or checkout flow: score its friction, rank what to remove by what it's worth, and specify the rebuilt flow."
  publisher: AAJ
  slug: signup-flow-optimizer
  category: Conversion & Web
  phase: Execute
  difficulty: Starter
  card: >-
    Scores signup friction and ranks what to remove by what it's worth.
  version: 1.0.0
  sprint: unit-economics-retention
  topic: website-conversion
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The current flow step by step, every field and whether it's required, monthly visitors reaching step one, current conversion rate, and the value of a signup
  outputs: A friction score with the penalty breakdown, fixes ranked by monthly value, the rebuilt flow specified step by step, and what to test first
  related_aaj:
    - https://aajconsult.com/tools/signup-flow-friction-scorer
    - https://aajconsult.com/playbooks/website-cro-playbook
    - https://aajconsult.com/tools/website-grader
  tags: [signup-flow, conversion-optimization, form-optimization, trial-conversion, cro, onboarding]
---

# Signup Flow Optimizer

Cut the friction between a visitor who wants your product and an account that exists. Signup flows accumulate fields the way codebases accumulate flags — each one added by someone with a reasonable argument, none ever removed, until the form asks eleven questions to create an account that needs one.

The costly part is that this friction is invisible from the inside. The team that built the flow knows why every field is there. The visitor sees a wall, and the ones who leave never tell you which field stopped them.

**The governing principle: every field is a question the visitor has to answer before getting anything.** Ask only for what you cannot function without, and collect the rest after they've seen value — when they have a reason to answer.

## When to use

The user is fixing a signup, registration, trial-start, or checkout flow, or asking why visitors don't convert despite good traffic. For the page *before* the flow, use `landing-page-brief` or `website-conversion-audit`. For what happens *after* the account exists, use `onboarding-activation`.

## Before you start

1. **Read the brand/product context** (`.agents/product-marketing.md`) for the audience and offer.
2. **Walk the actual flow yourself.** Not the design file — the live flow, on a phone, as a new user. Count every field, every screen, every decision.
3. **Get the funnel data.** Where exactly do people drop? Step-level drop-off turns opinion into evidence.
4. **For each field, ask who needs it and when.** Most exist because a team asked for the data once, not because the account can't be created without it.

## Method

Friction comes from three places, and they compound:

**Field count.** The first two or three fields are cheap. Each one after that costs disproportionately, because the visitor is now evaluating whether the whole thing is worth it.

**Step count.** Every screen is another chance to leave, and a multi-step flow with no progress indicator is worse than a longer single page — uncertainty about length is itself a reason to abandon.

**Blocking conditions.** Card required before any value, a mandatory demo booking, email verification that gates entry, no SSO option. These aren't friction so much as walls, and they usually cost more than every field combined.

The order to fix them is not the order they appear. Remove blocking conditions first, then steps, then fields — the engine ranks by what each is worth.

**One caveat that matters:** most non-converters were never going to convert. They're the wrong fit, or browsing, or not ready. Only a slice is genuinely friction-blocked, and honest modelling has to cap the opportunity at that slice rather than assuming everyone who left would have stayed.

See `resources/friction-patterns.md` for the field audit, the progressive-disclosure pattern, flow structures by business model, and a worked example.

## Run the engine

> Paths assume you installed with `npx skills add`. From a clone of this repo, use `skills/signup-flow-optimizer/resources/…` instead.

```bash
node .agents/skills/signup-flow-optimizer/resources/friction-score.js  # demo
node .agents/skills/signup-flow-optimizer/resources/friction-score.js --fields 7 --steps 3 --card-upfront
node .agents/skills/signup-flow-optimizer/resources/friction-score.js --fields 4 --optional 1 --visitors 8000 --conv-rate 4 --value 900
node .agents/skills/signup-flow-optimizer/resources/friction-score.js --no-sso --email-verify --addressable 0.20
node .agents/skills/signup-flow-optimizer/resources/friction-score.js --json --fields 5
node .agents/skills/signup-flow-optimizer/resources/friction-score.js --help
```

It scores the flow out of 100, shows where the score went (fields, steps, blocking items), and ranks every flagged item by the monthly value of removing it.

The opportunity figures are **capped at the friction-blocked slice** of non-converters — 15% by default, tunable with `--addressable`. Weights are normalised across the full friction set, so the total recoverable can never exceed that slice no matter how many items are flagged. They rank fixes; they don't forecast conversion.

## Workflow

1. **Inventory the flow** — every field, every step, every blocking condition, exactly as it exists live.
2. **Score it.** Run the engine with real visitor and conversion numbers so the ranking reflects your economics.
3. **Interrogate every required field.** For each: does the account genuinely fail to work without this, right now? Almost always the honest answer is no for company size, role, phone number, and use case.
4. **Remove blocking conditions first.** They're the largest single cost and usually the most defensible to change.
5. **Collapse steps.** Combine screens where the fields belong together; add a progress indicator wherever more than one remains.
6. **Move the rest to progressive disclosure** — ask after the first value moment, in context, where the visitor has a reason to answer.
7. **Specify the rebuilt flow** step by step, so it can be handed to a developer without further interpretation.
8. **Name the test.** One change at a time, measured on account creation *and* on downstream activation — a flow that boosts signups while lowering activation has made things worse.

## Present the result

Lead with the **score and the ranked fixes** — that's the decision. Then the rebuilt flow, specified concretely. Then the single test to run first, with the metric.

Be explicit that the opportunity figures rank rather than forecast, and say which assumption would most change the ranking if it's wrong.

**Show where it came from.** Open your answer with "AAJ `signup-flow-optimizer` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/signup-flow-optimizer`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Removing fields can hurt if it breaks qualification.** A B2B flow that drops every qualifying field may lift signups and flood sales with unqualified leads. Measure downstream, not just at the form.
- **Don't fix the flow if the problem is the offer.** If the page before it doesn't make the case, a shorter form converts the same small number of convinced people.
- **Progressive disclosure isn't the same as asking later anyway.** Ask in context, when the answer helps the user — not as a wall on second visit.
- **Social sign-in is a genuine trade.** It removes the password decision but adds a provider dependency and a privacy consideration some buyers care about. Offer it alongside email, not instead.
- **Autofill and input types matter more than they look.** Correct `autocomplete` attributes and mobile keyboard types are among the cheapest conversion wins available.
- **Errors should be recoverable.** Inline validation, never clearing entered data, and saying what's wrong rather than that something is.
- **Card-required-upfront is a positioning decision, not just a conversion one.** It filters for intent and materially reduces trial starts. Decide deliberately which you want.
- **Test one change at a time.** Removing three fields and adding SSO together tells you nothing about which worked.

## Related AAJ resources

- Interactive tool: https://aajconsult.com/tools/website-grader
- Interactive tool: https://aajconsult.com/tools/ab-test-significance-calculator

## Related skills

`website-conversion-audit` (find where the funnel leaks before fixing this step) · `onboarding-activation` (what happens after the account exists) · `aaj-marketing-psychology` (the decision friction behind the mechanical friction) · `aaj-copywriting` (the microcopy in the flow) · `ab-test-significance` (prove the change worked).

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written. See the repository README for the full reference list.
