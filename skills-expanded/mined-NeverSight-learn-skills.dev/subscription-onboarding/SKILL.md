---
name: subscription-onboarding
description: >
  Designs, audits, and optimizes onboarding and onboarding-to-paywall
  flows for consumer subscription apps. Use when onboarding, first-run
  experience, activation handoff, onboarding paywalls, personalization,
  permissions, or onboarding experiments are the primary product
  decision. When an app codebase is available, inspect the implementation
  before recommending changes. Reasons from product facts, first-party
  evidence, time-to-value, user intent, monetization model, and platform
  constraints rather than applying fixed funnels or benchmarks.
license: MIT
metadata:
  author: pol-cova
  version: "0.2.0"
---

# Subscription onboarding

Design the shortest credible path from user intent to product value, paid access when relevant, and durable activation. Challenge the proposed flow before optimizing it. Do not start by choosing screens.

## Scope

Use this skill when the primary decision concerns onboarding, first-run experience, onboarding-to-paywall, activation handoff, onboarding personalization, onboarding permissions, onboarding experiments, or paywall timing within onboarding.

Do not use it as the primary workflow for standalone pricing, standalone paywall copy or design, App Store optimization, lifecycle CRM, cancellation, win-back, reactivation, generic analytics, experiments unrelated to onboarding or activation, or general UX review. Keep adjacent work bounded to its effect on first-run and activation. Use a specialized skill when one exists.

## Inspect the product before advising

When a codebase is available, inspect the implementation before making substantive recommendations. Use focused inspection rather than reading the entire repository.

Follow this order:

```text
inspect codebase
-> understand the product
-> map current product behavior
-> inspect onboarding and monetization
-> inspect instrumentation
-> identify important unknowns
-> ask for decision-relevant metrics or details
-> analyze evidence
-> recommend changes
-> define measurement and experiments
```

Inspect relevant entry points, navigation, first-run state, onboarding views, authentication, paid feature boundaries, paywall and subscription integrations, offer eligibility, purchase and restore handling, permissions, notifications, persistence, analytics events, feature flags, product configuration, documentation, and tests.

Establish what the product actually does, its platforms, core action, current flow, and plausible first-value and activation events. Prefer implementation evidence over filenames, screenshots, category assumptions, or the user's shorthand. Surface conflicts between the implementation and the user's description.

Do not ask the user to explain facts available in the codebase. If repository access is unavailable, use supplied artifacts and label unverified product behavior accordingly.

## Build the product model

Before proposing a flow, record:

```text
Product:
Target user:
Primary job-to-be-done:
Acquisition promise:
Core product action:
Time-to-first-value:
Time-to-recurring-value:
Current onboarding:
Current monetization boundary:
Activation candidate:
Required product/platform constraints:
Known instrumentation:
Important unknowns:
```

Then express the value logic:

```text
Current state -> Desired state -> Obstacle -> Mechanism -> Evidence -> Offer -> Activation
```

Expose any unknown or implausible link before designing screens.

## Classify evidence by the question

Use these labels consistently:

- `FACT`: mechanically or operationally true product behavior, verified in implementation or supplied product facts.
- `CONSTRAINT`: a requirement imposed by safety, regulation, platform rules, technical limits, business economics, content rights, privacy, or security.
- `EXPERIMENTAL`: evidence from a randomized or credible causal experiment.
- `BEHAVIORAL`: first-party observational analytics about what users do. Do not treat association as causation.
- `QUALITATIVE`: usability, interview, survey, support, or observed-comprehension evidence, used mainly to understand why.
- `BENCHMARK`: external empirical evidence. Treat it as a prior, not a target or universal prescription.
- `INFERENCE`: a deduction from stated evidence. Name its premises.
- `HYPOTHESIS`: an unverified, testable claim.

Do not force every decision into one linear evidence hierarchy. Match the evidence to the question. Implementation can establish product behavior, qualitative work can explain confusion, behavioral data can show abandonment, and experiments can estimate causal effects.

For causal questions, prefer approximately:

```text
randomized first-party evidence
> credible quasi-experimental evidence
> first-party behavioral association
> comparable external observational evidence
> general industry patterns
> intuition
```

Never present a hypothesis as fact. Never let a benchmark override stronger first-party evidence without a specific reason. Read [source-quality-and-freshness.md](references/source-quality-and-freshness.md) when external evidence or current platform rules affect the recommendation.

## Ask for decision-relevant evidence

After understanding the product and inspecting its instrumentation, ask only for missing information that could change the decision. Prefer raw counts alongside rates.

When available, request:

- starts, completion and abandonment by stage;
- first-value attempts and successes;
- paywall views, trial starts, purchases, restores, and purchase failures;
- trial-to-paid, cancellation timing, refunds, retained subscribers, renewal, and revenue per eligible user;
- acquisition channel, campaign promise, geography, platform, and new, returning, or existing-subscriber status.

For an experiment, request control and variant definitions, eligible users per arm, assignment method, dates, raw funnel counts, primary metric, guardrails, trial duration, maturity window, and simultaneous product or pricing changes.

If the product has no established activation definition, propose candidates from the implementation as `HYPOTHESIS` and ask whether first-party evidence links them to retained use.

Do not require mature outcomes from a product too new to have them. If data does not exist, continue. State that the work is fact-led, qualitative, or hypothesis-led; identify high-confidence product, platform, UX, and deception issues; propose minimum instrumentation; and avoid invented benchmarks, lifts, retention, or significance.

## Classify time-to-value

Choose the closest class, then adapt it to the product:

- **Immediate value:** the core benefit can appear in the first session. Prefer promise, minimum setup, product action, result, then offer. Test whether onboarding can be removed.
- **Short setup before value:** relevant input or configuration is required. Collect only inputs that change output, setup, safety, or product state. Show the result promptly.
- **Delayed value:** the real outcome needs hours, days, or repeated use. Establish intent, a credible mechanism, necessary setup, and the next commitment. Do not fabricate an instant result.
- **Network or content-dependent value:** value depends on catalog fit, other users, collaboration, or marketplace density. Account for the strategic value of free participation before restricting access.

These are heuristics, not templates. Read [onboarding-archetypes.md](references/onboarding-archetypes.md) when category or value timing materially changes the structure.

## Decide whether onboarding is needed

Start from zero screens. Add a stage only if it:

- enables or accelerates first value;
- collects data that changes the experience, recommendation, setup, safety, content, or product state;
- resolves a real comprehension, trust, safety, or compliance barrier;
- prepares a contextual permission required by the next action;
- explains an offer whose value or terms would otherwise be unclear; or
- creates necessary commitment for a delayed-value product.

Candidate stages include promise, relevance, context, problem, desired outcome, personalization, setup, product experience, result, proof, commitment, offer, and activation. Do not treat this list as a sequence.

Prefer product evidence over feature explanation when value can be demonstrated. Defer nonessential setup. Use sensible defaults. Make optional education skippable.

Apply the deletion test: what important outcome becomes worse if this stage disappears? Remove it or test removal when there is no defensible answer.

Read [onboarding-principles.md](references/onboarding-principles.md) for screen-level decisions and [patterns-and-antipatterns.md](references/patterns-and-antipatterns.md) when reviewing persuasive devices.

## Design only justified stages

For each stage, specify:

1. purpose;
2. user belief or action it changes;
3. information shown or collected;
4. how collected data changes the product;
5. entry condition and next state;
6. skip, back, recovery, and accessibility behavior;
7. event instrumentation;
8. evidence labels and confidence;
9. consequence of removal;
10. whether product evidence can replace explanation.

For every onboarding question, record `answer -> downstream use`. Research or marketing segmentation alone does not make a question necessary in the critical path.

Do not use fake personalization, fabricated progress or loading, invented statistics, disguised ads, premature rating prompts, forced permission bundles, or manipulative pain amplification. Preserve strong stages instead of redesigning for novelty.

Use [onboarding-audit-template.md](assets/onboarding-audit-template.md) for a reusable audit.

## Connect onboarding to monetization and activation

Choose paywall timing from value timing, access model, intent, acquisition promise, and product economics. Do not assume hard paywall, freemium, trial, or onboarding paywall is universally best.

Make paid access, price, billing period, trial or introductory terms, renewal, dismissal behavior, restore behavior, and the next action clear. Keep the paywall consistent with the value story. Do not use it to hide an unclear mechanism or weak proof.

After purchase or onboarding, return the user to the motivating action. Define a product-specific activation event, its time window, and why it may predict retained value. Purchase is not activation unless evidence supports that relationship.

Read [monetization-and-paywalls.md](references/monetization-and-paywalls.md) for access-model decisions. For shipping-sensitive platform guidance, read [apple-platform-rules.md](references/apple-platform-rules.md) or [android-platform-rules.md](references/android-platform-rules.md) and verify the current official rules.

## Measure and experiment

Define event names, eligibility, denominators, properties, and observation windows. Pair a primary outcome with downstream guardrails. Read [experiments-and-metrics.md](references/experiments-and-metrics.md) for causal and statistical guidance.

For randomized onboarding experiments, use the eligible randomized population as the default denominator for the primary causal estimate. Report the intention-to-treat or eligible-user result alongside conditional funnel diagnostics. Onboarding completers, paywall viewers, trial starters, and users reaching later screens are treatment-affected groups. Conditioning on them can introduce selection bias.

When an experiment is justified, output:

- Hypothesis
- Control
- Variant
- Eligibility
- Unit of randomization
- Primary metric
- Guardrail metrics
- Expected mechanism
- Minimum practical effect
- Decision rule
- Important segments
- Known confounders
- Maturity window

Change one major causal idea at a time when the goal is learning. A test that changes pricing, design, trial duration, and sequence is a package comparison. Do not attribute its result to one component.

For weak samples, report uncertainty and minimum detectable effect considerations. Prefer gathering data or testing a larger justified contrast over declaring an unstable winner.

## Self-review

Before finalizing:

- verify that implementation inspection preceded recommendations when code was available;
- verify every stage has a necessary job and passes the deletion test;
- remove unused questions, repeated promises, premature asks, and fake progress;
- check that evidence labels match the questions they support;
- relabel unsupported causal claims as hypotheses;
- report eligible-user experiment outcomes before conditional diagnostics;
- check activation, retention, cancellation, refunds, renewal, and revenue;
- check platform, accessibility, and source freshness;
- state what should remain unchanged;
- list the highest-impact unknowns and the evidence that would resolve them.

## Output shape

Adapt detail to the request. For a full design or audit, provide:

1. inspected implementation and product model;
2. evidence table with type, source, confidence, and limits;
3. time-to-value and product logic;
4. keep, remove, change, or add decisions;
5. proposed flow with a reason for every stage;
6. monetization transition and activation handoff;
7. measurement plan;
8. experiment specifications;
9. risks, uncertainty, and unresolved questions.

Read [examples.md](references/examples.md) only when a worked example would improve calibration.
