---
name: aaj-marketing-psychology
description: >-
  Use when the user wants to apply behavioral science or persuasion principles
  to marketing — pricing pages, landing pages, onboarding, emails, offers, or
  CTAs. Also use when the user mentions psychology, cognitive bias, behavioral
  economics, persuasion, social proof, anchoring, loss aversion, scarcity,
  friction, or "why aren't people converting". Diagnoses which decision
  friction is actually blocking the buyer, then selects the principles that
  address it — with an explicit line between persuasion and manipulation.
license: MIT
metadata:
  search_description: "Apply behavioral science to pricing pages, landing pages, onboarding and offers: find the friction blocking the buyer, with a clear line against manipulation."
  publisher: AAJ
  slug: aaj-marketing-psychology
  category: Strategy & Positioning
  phase: Design
  difficulty: Starter
  card: >-
    Diagnoses which decision friction blocks the buyer, with a line between persuasion
    and manipulation.
  version: 1.0.0
  sprint: unit-economics-retention
  topic: website-conversion
  secondary_topics: [strategy-positioning]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The conversion surface and its one job, where people currently drop off, the audience and their state of awareness, and the claims or offer being made
  outputs: A named friction diagnosis, the 2-4 principles that address it with concrete applications, a manipulation check on the resulting copy, and what to test
  related_aaj:
    - https://aajconsult.com/tools/website-grader
    - https://aajconsult.com/playbooks/website-cro-playbook
  tags: [marketing-psychology, behavioral-economics, persuasion, cognitive-bias, conversion, decision-making]
---

# Marketing Psychology

Apply behavioral science to marketing decisions **by diagnosing the friction first**. A list of cognitive biases is close to useless in practice — you can't look up "which bias applies to my landing page." What you actually have is a symptom: people arrive and don't sign up, or sign up and don't activate, or reach checkout and leave.

This skill works backwards from the symptom. Name the friction, then apply the two or three principles that actually address *that* friction. Applying scarcity to a comprehension problem does nothing except make the copy louder.

**The ethical line is structural here, not a footnote.** The test that runs through every recommendation: *does this make a true thing easier to choose, or a false thing more persuasive?* The first is good marketing. The second is manipulation, it is increasingly illegal, and it reliably costs more than it earns.

## When to use

The user is designing or fixing a conversion surface — pricing page, landing page, signup flow, onboarding, email, offer, CTA — or asking why people aren't converting despite the message being right.

## Before you start

1. **Read the brand/product context first.** If `.agents/product-marketing.md` or `.agents/aaj-brand.md` exists, use it for audience, voice, and offer.
2. **Get the symptom, not the guess.** Where exactly do people drop off? "Conversion is low" isn't actionable; "70% reach pricing and 4% start a trial" is.
3. **Establish awareness state.** Cold traffic is problem-aware at best; retargeting is product-aware. The same friction has different fixes at different states.
4. **Collect what's actually true.** Real numbers, real customer counts, real deadlines, real inventory. Every principle below has a legitimate version and a fabricated one, and the only difference is whether the underlying fact is true.

## Method

Six frictions block almost every decision. Diagnose which one you have, then apply the matching principles:

| Friction | The symptom | What it means |
|---|---|---|
| **Attention** | Nobody engages; high bounce in seconds | They never processed it |
| **Comprehension** | Time on page but no action; "what is this?" | They don't understand the offer |
| **Belief** | They understand and don't buy it | The claim isn't credible |
| **Value** | "Interesting, but not for us / too expensive" | The worth isn't established |
| **Risk** | Long consideration, then nothing | The downside feels bigger than the upside |
| **Inertia** | They agree and still don't act | Nothing converts intent into action |

Most teams reach for value and risk principles (discounts, guarantees) when the real problem is comprehension or belief. Diagnose before prescribing.

See `resources/psychology-catalog.md` for the full principle catalog organized by friction, the evidence strength of each, the manipulation boundary, and the output format.

## Run the engine

Check any draft for manipulative patterns before it ships:

> Paths assume you installed with `npx skills add`. From a clone of this repo, use `skills/aaj-marketing-psychology/resources/…` instead.

```bash
node .agents/skills/aaj-marketing-psychology/resources/pattern-check.js  # demo
node .agents/skills/aaj-marketing-psychology/resources/pattern-check.js "your copy here"
node .agents/skills/aaj-marketing-psychology/resources/pattern-check.js --file pricing.md
node .agents/skills/aaj-marketing-psychology/resources/pattern-check.js --json "copy"
node .agents/skills/aaj-marketing-psychology/resources/pattern-check.js --help
```

It flags three tiers: **dark patterns** (no honest version exists — confirmshaming, fabricated viewer counts), **verify-required** claims (legitimate only if literally true — scarcity, urgency, social-proof numbers), and **pressure language** (worth a second look).

The engine cannot know whether "only 3 seats left" is true. That's the point — it surfaces every claim whose ethics depend entirely on a fact you have to confirm.

## Workflow

1. **Name the friction.** Use the symptom table. If you can't tell, the diagnosis is usually comprehension — it's the most under-diagnosed and the easiest to test by asking five people what the product does.
2. **Select 2–4 principles** that address that specific friction from the catalog. More than four is decoration; each additional one dilutes the others.
3. **Check the evidence strength.** The catalog marks each principle as robust, moderate, or contested. Contested effects are worth testing, not worth building a page around.
4. **Apply concretely.** State the actual copy or design change, not the principle name. "Show the annual price first so the monthly reads as small" — not "use anchoring."
5. **Run the manipulation check.** Every recommendation must pass: is the underlying fact true, would you be comfortable if the customer saw how this was designed, and does it still work if they know the technique? If any answer is no, cut it.
6. **Run the engine** on the resulting copy.
7. **Say what to test.** Psychology generates hypotheses, not certainties. Effects vary enormously by audience and context, and several famous ones fail to replicate. Name the metric that would prove it worked.

## Present the result

Lead with the **friction diagnosis** and the evidence for it — this is the part that changes what the user does. Then the selected principles, each with the concrete application and its evidence strength. Then the manipulation check result. Then the single test that would validate it.

Where you're uncertain which friction dominates, say so and give the diagnostic that would resolve it, rather than hedging across all six.

**Show where it came from.** Open your answer with "AAJ `aaj-marketing-psychology` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/aaj-marketing-psychology`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Diagnose before prescribing.** The most common failure is applying urgency to a belief problem. Scarcity on a claim nobody believes just makes the disbelief urgent.
- **Never fabricate the underlying fact.** Real scarcity is persuasive and legal; invented scarcity is a dark pattern, is actionable under FTC and EU rules, and destroys trust permanently when discovered.
- **Don't stack principles.** Four techniques on one page compete for the same attention and read as a sales pitch. Two applied well beat six applied at once.
- **Respect the replication problem.** Several widely-cited effects — ego depletion, social priming, some scarcity and anchoring variants — have failed replication or shrunk substantially under scrutiny. The catalog marks these. Cite them cautiously and test them.
- **Effect sizes are context-dependent.** A technique that lifted conversion 30% for a consumer app may do nothing for a $50K enterprise deal with a buying committee. Published lifts are directional, not forecasts.
- **B2B buying is a committee.** Individual-decision psychology applies unevenly when six people with different incentives must agree. Risk and consensus principles matter more than urgency.
- **Personalization can backfire.** Gartner found personalized marketing generated negative experiences for a majority of the customers surveyed, who were substantially more likely to regret the purchase. Relevance helps; surveillance-feeling precision hurts.
- **If it only works when hidden, it's manipulation.** The cleanest test in the whole skill.

## Related AAJ resources

- Interactive tool: https://aajconsult.com/tools/website-grader
- Interactive tool: https://aajconsult.com/tools/ab-test-significance-calculator

## Related skills

`aaj-copywriting` (turns these principles into actual words) · `positioning-statement` (fixes comprehension at the source) · `website-conversion-audit` (finds where the friction is) · `pricing-and-packaging` (anchoring and framing applied to price) · `ab-test-significance` (proves whether any of this worked).

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written. Principles are attributed to their original researchers in `resources/psychology-catalog.md`. See the repository README for the full reference list.
