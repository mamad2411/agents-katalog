---
name: landing-page
description: Write, build, repair or audit landing, pricing, campaign and waitlist pages from evidence-backed positioning, claims and proof. Use when page copy, positioning or conversion needs work.
license: MIT
---

# Landing page

Produce a coherent marketing page for one audience and one primary decision. Own the page-level argument: what the visitor must understand, believe and do. Preserve the product's existing brand, voice and implementation system unless evidence supports changing them.

## Keep the boundary clear

This skill owns the argument, the copy and the page. Route adjacent work:

- Use the `mobile-first` skill for a measured responsive audit or repair after the page structure is sound.
- Use the `performance-diagnosis`, `social-sharing` or `remove-ai-slop` skill when that is the requested outcome.
- Use the `ui-copy` skill for in-product language: form states, errors, notifications and accessible names behind the CTA.
- Use the `product-experiments` skill to implement, run or analyze a test this skill designs.

A broader design system, application workflow or component library is out of scope. Say so, keep the landing-page portion here, and do not redesign the product around the page.

When a routed skill is unavailable, handle the necessary portion here, but do not claim evidence you could not inspect.

## Choose the working mode

Infer the narrowest mode from the request and existing project:

- **Copy:** find the defensible claim, then write or rewrite positioning, proof, objections and CTA language. No layout or code changes unless asked. Triggers include "rewrite the copy", "the hero is generic", "our positioning is vague".
- **Build:** create and implement a new page or substantial section, copy included.
- **Repair:** change an existing page whose message, structure, proof or conversion path is underperforming.
- **Audit:** return evidence-backed findings without changing files. Covers the user's page, a competitor's page or a reference page.
- **Handoff:** produce an implementation brief or sequenced prompts because another person or agent will execute the work.

State the selected mode and scope in one sentence. Do not offer the modes as a menu. "Fix my landing page" with no further signal is Repair; narrow to Copy when the structure is sound and the words are the problem.

## Recover evidence before asking

Inspect the supplied brief, repository, live page, analytics, search data, customer language, sales and support questions, product states, brand tokens and in-scope reference sites. Separate observed facts from assumptions.

Resolve from evidence when possible:

- the visitor, their entry context, awareness and the job they are trying to complete;
- the page job: category introduction, alternative, campaign response, feature evaluation, pricing decision, waitlist signup;
- the single primary action and any legitimate secondary path;
- the differentiated claim and the proof available to support it;
- implementation constraints, visual system and required states;
- how success will be measured after release.

Ask only about missing choices that change the result: an unknown primary action, a choice between materially different business promises, contradictory reference directions, or permission to replace a consequential conversion flow. Batch at most three short questions. Continue with labeled assumptions when the choice is reversible. Missing facts become content requirements, never invented copy.

## Find the defensible claim

Read [references/claim-first.md](references/claim-first.md) before Copy or Build mode, or any Repair that changes the core proposition. Skip it for a bounded wording fix that leaves the claim intact.

Write a compact page brief before writing or implementing:

1. **Visitor:** who arrives and what they already know.
2. **Decision:** the primary action and the commitment it requires.
3. **Claim:** a specific, defensible reason to choose this product now.
4. **Proof:** the strongest available evidence and its provenance.
5. **Objections:** the few uncertainties that genuinely block the decision.
6. **Measurement:** the event or outcome that would show the page is working.

Generate several plain claim shapes that vary the strategic frame, not just the wording. Run the swap test on each: replace the product with its closest alternative. A line that survives unchanged is generic. Add mechanism, buyer, constraint or evidence, or cut it.

Record every material claim in the claim and proof ledger. It is the single source for what the page may say. If the claim or proof is missing, do not compensate with decorative design or stronger adjectives. Surface the gap and either request the input or build an honest lower-commitment page.

## Hold the proof line

These hold even when the user asks directly:

- **No invented proof.** No customer counts, logos, testimonials, ratings, rankings, statistics, "trusted by" lines, case results or press mentions without a source the user supplied or you inspected. A request like "add 'trusted by 10,000 teams'" without evidence becomes a content requirement plus an honest alternative line.
- **No broadened proof.** A result from one customer, period or segment is not a general outcome. Keep scope and limits beside the claim.
- **No manufactured urgency.** No fake scarcity, countdowns, "only 3 left" or deadlines the business does not enforce.
- **No predicted lift.** Never promise a conversion change or quote a percentage from another product's test.
- **No copied expression.** Learn from a competitor's structure and evidence; do not copy its distinctive language, artwork or brand assets.

Placeholders must be visibly labeled as placeholders and must not ship as customer evidence.

## Compose and write

Read [references/architecture.md](references/architecture.md) when choosing the page shape, section set or order. Choose sections because each advances the visitor's decision. Order them by the visitor's largest unresolved uncertainty, not a fixed hero, features, testimonials, FAQ template.

- Put the product and its consequence in the first viewport; avoid category-only headlines.
- Use concrete domain nouns, actions, mechanisms, constraints and observable results. Keep technical detail the buyer needs.
- Use customer language when it is representative and accurately sourced.
- Keep the existing voice. Headline length, casing, feature-first or benefit-first order and humor are contextual choices, not rules.
- Make each CTA state its destination, result or commitment. Repeat the primary action where renewed intent makes sense.
- Place price, security, compatibility and cancellation facts beside the decision they affect, not only in a FAQ.
- Let content determine layout. Do not require cards, gradients, display fonts, animation or a particular radius system.

Read [references/guide.md](references/guide.md) only when choosing a narrative shape, diagnosing a recurring copy failure or designing a messaging experiment.

## Design experiments with restraint

Propose a test only when the claim choice stays uncertain after evidence. Test one material hypothesis at a time: audience framing, problem versus outcome, mechanism visibility, proof placement or commitment language. Keep offer, layout, traffic and CTA destination stable. State hypothesis, primary measure, guardrail, audience, sample or runtime limit and decision rule. Do not declare a universal winner from one product's result.

## Implement within the project

Reuse sound components, tokens, assets, routing, analytics and test conventions. Do not install a new framework or motion library only to achieve a landing-page style.

Build meaningful states: narrow and wide layouts, loading or unavailable product evidence, form success and failure, keyboard focus, reduced motion and long copy. Protect personal information and secrets in screenshots or fixtures.

When the work changes an existing funnel, preserve event semantics or document the migration. Authorization to edit the page is not authorization to deploy, launch an experiment, change paid traffic or publish.

## Audit

Read [references/review.md](references/review.md) for lenses, severity and the evidence-capture protocol. Read [references/evidence.md](references/evidence.md) before asserting standards, performance thresholds or conversion research.

For a competitor or reference page, follow the capture protocol in review.md: record URLs, capture date, viewport and device, auth state, locale and states covered. Label each finding as visible evidence, user-provided behavior, sourced fact or inference. Never infer conversion, retention, revenue, strategy or sentiment from UI alone. Turn findings into transferable principles with fit conditions, not a copy list.

In Audit mode, change nothing. Report missing evidence separately from writing defects.

## Verify

1. Map every material claim to product behavior, a source, a scoped assumption or a labeled content requirement. Confirm nothing was invented or broadened.
2. Run the swap test on the headline and major propositions. Explain any generic line kept.
3. Trace the visitor's questions through the section order. Cut repeated promises that add no mechanism, proof or decision support.
4. Confirm each CTA's text, destination and actual commitment agree.
5. Check terminology against the product UI, pricing and docs.

For implemented work, also:

6. Run the repository's build, typecheck, lint and relevant tests.
7. Render narrow, tablet and desktop widths plus 200% zoom. Check text overflow with long copy.
8. Exercise the primary action, forms, errors, navigation and keyboard path.
9. Verify links, analytics events, metadata, share previews and performance in proportion to risk.

Compare the result with the brief. Report observed gaps rather than declaring success from section presence.

## Deliver

**Copy mode:** the page brief, the claim and proof ledger, the message architecture with the question each section answers, the copy deck labeled by section and component, CTA destinations and commitment, content and proof still required, excluded claims, and optional variants only when they test a stated hypothesis. For a targeted rewrite, give before and after lines with the reason for each.

**Build, Repair, Handoff:** the page or brief, then the visitor, decision, claim and proof used; material structure and design decisions; what changed and what was directly verified; assumptions, missing evidence and production work still needing authorization; the post-release measurement plan.

**Audit:** the verdict and top three causes, the capture record, an evidence table ranked by effect on comprehension, trust, action, accessibility and performance, strengths to preserve, and the smallest coherent repair sequence.
