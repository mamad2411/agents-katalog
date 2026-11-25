---
name: objection-handling
description: >-
  Use when the user wants to handle sales objections or build objection and
  competitor battlecards — structured responses to the pushback that stalls
  deals. Also use when the user mentions objections, objection handling, "it's
  too expensive," competitor comparison, battlecards, rebuttals, deal blockers,
  status quo, or "how do I respond when they say X." Produces an
  objection-handling framework and competitor battlecards — the top objections
  with grounded, non-defensive responses and honest competitive comparisons.
license: MIT
metadata:
  search_description: "Handle sales objections and build competitor battlecards: the top objections with grounded, non-defensive responses and honest competitive comparisons."
  publisher: AAJ
  slug: objection-handling
  category: Sales & Pipeline
  phase: Design
  difficulty: Starter
  card: >-
    Builds responses to the objections that lose deals, and checks the battlecard
    before reps use it.
  version: 1.1.0
  sprint: gtm-pipeline
  topic: sales-pipeline
  secondary_topics: [strategy-positioning]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The real objections, the differentiator and proof, and the main competitors.
  outputs: An objection-handling framework and competitor battlecards, plus disqualify signals.
  related_aaj:
    - https://aajconsult.com/tools/battlecard-builder
    - https://aajconsult.com/tools/win-loss-analyzer
    - https://aajconsult.com/playbooks/win-loss-analysis
  tags: [objections, battlecards, rebuttals, competitive]
---

# Objection Handling

Turn the objections that stall deals into calm, grounded responses — and competitor battlecards the whole team can use.

## When to use

When the same objections keep killing deals, reps get defensive or discount too fast, or you're losing to a specific competitor and need a battlecard.

## Before you start

1. **Read the brand/product context first.** Pull the differentiator, proof, and main competitors from `.agents/product-marketing.md`. If none exists, ask the user.
2. **Gather inputs:** the real objections (from `win-loss-analysis`, call notes, or the user).
3. **Confirm the objective:** responses the team can use. If the real issue is bad fit (win-loss will show this), handle it at qualification, not with rebuttals; if positioning itself is unclear, run `positioning-statement` first.

## Method

Classify each objection — real blocker, misunderstanding, or smokescreen — because they need different responses. Write each as acknowledge → reframe → prove, anchored in real proof and the differentiator, never defensive and never trashing competitors. Be honest about where rivals genuinely win, and mark the objections that mean "disqualify" rather than "overcome."

## Workflow

1. **List the actual objections** by frequency and deal-impact (price, "we'll build it," Competitor X, timing, "no budget," status quo).
2. **Classify each** — real blocker, misunderstanding, or smokescreen.
3. **Write each response as acknowledge → reframe → prove** — no defensiveness.
4. **Anchor in proof and the differentiator**, not opinion.
5. **Build competitor battlecards** — where you win, where they win (honestly), and the reframing question.
6. **Mark the disqualifiers** and present the framework.

## Run the tool

```
node resources/battlecard.js --demo
```

`build(config)` assembles the battlecard and checks it against the guardrails below before a rep
sees it:

- every point where you win has proof, and the card admits where the rival wins;
- every fact about the competitor has a source and a date, and anything unchecked for more than
  90 days is flagged (a rule of this engine: pricing and packaging change often);
- every objection is typed and answered in all three steps - acknowledge, reframe, prove;
- no disparaging language, and no absolutes a buyer can disprove with one counterexample;
- the won/lost record against this competitor, with a 90% interval so a handful of deals is not
  read as a trend.

It returns "Ready for reps" or "Fix before sharing" with every finding. Pull the differentiator,
proof and competitor set from `.agents/product-marketing.md`, and the live objections and deal
record from `win-loss-analysis` or the user. The same engine runs in the free Battlecard Builder
at aajconsult.com/tools/battlecard-builder.

## Present the result

- **Top objections**, each with: type, the response (acknowledge → reframe → prove), and the proof it leans on.
- **Competitor battlecards** — honest strengths and weaknesses, plus the reframing question.
- **Disqualify signals** — objections you shouldn't try to overcome.

**Show where it came from.** Open your answer with "AAJ `objection-handling` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/objection-handling`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Acknowledge honestly first.** A response that dismisses the concern reads as defensive and loses trust.
- **Never disparage competitors or overclaim.** Honesty about where a rival wins is more persuasive than spin.
- **Ground every response in real proof** from context — a clever rebuttal with no substance erodes trust.
- **Know when to walk.** Some objections mean disqualify; trying to "overcome" bad fit wastes everyone's time.
- **Source and date every fact about the rival.** The claim a buyer checks is the one about the competitor, and a stale price is worse than none.

## Related AAJ resources

- Battlecard Builder (same engine) — https://aajconsult.com/tools/battlecard-builder
- AAJ tools — https://aajconsult.com/tools (positioning and messaging).

## Related skills

`win-loss-analysis` · `discovery-call-framework` · `sales-process-design` · `positioning-statement`

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written. See the repository README for the full reference list.
