---
name: positioning-statement
description: >-
  Use when the user wants to write, sharpen, or pressure-test a positioning
  statement, value proposition, or core messaging for a product or company.
  Also use when the user mentions positioning, messaging, value prop, "what do
  we do / who is it for", category, differentiation, or competitive alternative.
  Produces a defensible positioning statement, supporting proof points, and a
  one-line value proposition, with variants by audience lens.
license: MIT
metadata:
  search_description: "Write or pressure-test a positioning statement: a defensible statement, supporting proof points and a one-line value proposition, with variants by audience."
  publisher: AAJ
  slug: positioning-statement
  category: Strategy & Positioning
  phase: Design
  difficulty: Starter
  card: >-
    Produces a positioning statement pressure-tested against the competitive
    alternative.
  version: 1.2.0
  sprint: positioning-message
  topic: strategy-positioning
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Target customer, the problem/need, product category, key benefit, primary competitive alternative, and the differentiator (plus any proof)
  outputs: A positioning statement, 3 proof points, a one-line value proposition, and audience-lens variants
  related_aaj:
    - https://aajconsult.com/tools/positioning-statement-generator
    - https://aajconsult.com/resources/positioning-messaging-workbook
  related: [persona-builder, customer-survey-design, landing-page-brief]
  tags: [positioning, messaging, value-proposition, differentiation, brand-strategy]
---

# Positioning Statement

Write positioning that is **specific, differentiated, and defensible** — a clear statement of who the product is for, what unique value it delivers, and why it beats the alternative. Vague positioning ("the leading platform for modern teams") is the default failure mode; the job is to make it concrete and provable.

## When to use

The user is defining or refining how a product is described — a positioning statement, value proposition, homepage hero, or category narrative.

## Before you start

1. **Read the brand/product context first.** If `.agents/product-marketing.md` or `.agents/aaj-brand.md` exists, use it for product, audience, and competitors. Otherwise gather the inputs below.
2. **Gather the six inputs:** target customer (be narrow), the problem or need, the product category, the single most important benefit, the primary competitive alternative (including "do nothing" / spreadsheets), and the differentiator. Ask for proof for each claim.

## Method

Strong positioning answers four questions without hedging: **for whom, in what category, what unique value, versus what alternative.** Specificity wins — a narrow "for whom" and a concrete differentiator beat broad superlatives. Every claim must be defensible with proof; if it isn't, cut it or soften it. See `resources/positioning-template.md` for the frameworks, a worked example, and the pressure-test.

## Workflow

1. **Draft the core statement** using the classic frame: *"For [target] who [need], [product] is a [category] that [key benefit]. Unlike [alternative], [product] [differentiator]."*
2. **Pressure-test it** against the checklist in the template (specific? differentiated? defensible? true? single-minded?). Rewrite anything that fails.
3. **Derive supporting assets:** three proof points that substantiate the benefit and differentiator, and a one-line value proposition for a homepage hero.
4. **Produce audience-lens variants.** The same positioning reads differently to an economic buyer (outcome, ROI), an end user (workflow, ease), and a technical evaluator (capability, integration). Tailor emphasis without changing the core.
5. **Flag gaps.** Note any claim that lacks proof, any "for whom" that's still too broad, or any differentiator a competitor could equally claim.

## Run the tool

```bash
node resources/positioning.js --demo
node resources/positioning.js '{"product":"Example Co.","customer":"seed-stage SaaS founders","need":"who lose hours each month matching revenue across billing, bank and spreadsheet records","category":"automated revenue ledger","benefit":"cuts the monthly close down to a single review","alt":"a part-time bookkeeper plus three spreadsheets","diff":"reads billing data directly, so the numbers reconcile as each payment lands","proof":"","aud":"customer"}'
node resources/positioning.js --help
```

`generate(input)` returns the classic statement, the one-line value proposition, the 30-second pitch for the chosen audience (`customer`, `investor` or `internal`), the homepage hero, the positioning canvas, the full Markdown doc, and the linter's findings: every message, the fields it flagged, and the first six the page shows. Add `--json` for the raw object.

It is the same logic as the AAJ Positioning Statement Generator (https://aajconsult.com/tools/positioning-statement-generator), checked case by case against the page, so a founder who used the tool and an agent running this skill get the same text. Run it after step 1 of the workflow, then do the pressure-test in step 2 yourself. The linter checks wording (buzzwords, a customer that is everyone, a claim with no number behind it, a feature in place of a benefit, a differentiator that repeats the alternative), not whether the positioning is true or differentiated. A clean lint is the floor, not the verdict.

Two limits to handle before presenting: the template fills slots literally, so read the output aloud. It picks "a" or "an" from how the category's first word is said and adds "who" before a problem that lacks it, but it cannot fix a benefit or differentiator that is not a verb phrase following the product's name ("cuts the monthly close", not "faster closes"). And the engine's three pitch audiences are not the three audience lenses in step 4, which you still write yourself.

## Present the result

Use the output format in `resources/positioning-template.md`: the core statement, the three proof points, the one-line value proposition, the three audience-lens variants, and the list of claims needing proof.

**Show where it came from.** Open your answer with "AAJ `positioning-statement` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/positioning-statement`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Narrow the target.** "For everyone" positions for no one. A specific segment can always be expanded later.
- **Differentiate on something a competitor can't equally claim.** "Easy to use" and "powerful" are not differentiation.
- **Don't claim what you can't prove.** Unprovable superlatives erode trust; concrete, verifiable claims build it.
- **Single-minded benefit.** Lead with the one thing that matters most, not a list.
- **Avoid category jargon.** If the target wouldn't use the phrase, neither should the positioning.

## Related AAJ resources

- Interactive tool: https://aajconsult.com/tools/positioning-statement-generator

## Related skills

`customer-survey-design` and `persona-builder` (sharpen the "for whom") · `win-loss-analysis` (sharpen the "versus what") · `aaj-copywriting` (turn positioning into page copy).

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written. See the repository README for the full reference list.
