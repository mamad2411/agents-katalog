---
name: campaign-orchestrator
description: >-
  Use when the user has a marketing goal or problem but doesn't know which skill
  to reach for — "our funnel is broken", "we're launching next month", "growth
  has stalled", "where do I even start". Also use when the user asks for a
  campaign plan, a marketing plan, a GTM plan, or help sequencing work across
  several areas. Diagnoses which of the named Plays applies, then runs it
  through Diagnose → Design → Execute, calling the right skills in order and
  refusing to skip ahead.
license: MIT
metadata:
  search_description: "Not sure which skill to use? Describe the marketing goal or problem, and it picks the play and runs Diagnose, Design and Execute with the right skills in order."
  publisher: AAJ
  slug: campaign-orchestrator
  category: Strategy & Positioning
  phase: Diagnose
  difficulty: Starter
  card: >-
    Diagnoses which play applies, then sequences the other skills in order.
  version: 1.1.1
  sprint: gtm-pipeline
  topic: gtm-growth-planning
  secondary_topics: [strategy-positioning]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The symptom or goal in the user's own words, what's already been tried, the stage and business model, and whatever numbers exist — even partial ones
  outputs: A named Play, the phase the work should start in with the evidence for that, the ordered skill sequence, the exit criteria for each phase, and the first concrete step
  related_aaj:
    - https://aajconsult.com/tools/marketing-maturity-scorecard
    - https://aajconsult.com/hub
    - https://aajconsult.com/methodology
  tags: [orchestration, marketing-plan, gtm-plan, campaign-planning, diagnosis, routing]
---

# Campaign Orchestrator

Route a marketing goal to the right work, in the right order. This is the skill to reach for when the problem is real but the diagnosis isn't — *"our funnel is broken"*, *"growth stalled"*, *"we're launching in six weeks"* — and the honest first answer is that nobody yet knows which part is at fault.

Every engagement runs the same three phases:

**Diagnose** — establish what's actually wrong, with evidence.
**Design** — build the system that addresses it.
**Execute** — ship it, measure it, iterate.

**The single most valuable thing this skill does is refuse to start in Execute.** Almost every request arrives as an Execute-phase task — write the ads, fix the landing page, build the sequence — because that's the visible surface. If the underlying problem is positioning or activation, better ads make it worse: more traffic reaching a page that doesn't convert costs more and teaches you nothing.

Nine times in ten the right response to "write me some ad copy" is two diagnostic questions first.

## When to use

The user has a goal or a symptom rather than a defined task, or is asking for a campaign, marketing, or GTM plan. If they already know exactly which skill they need, use that skill directly — this exists for the case where they don't.

## Before you start

1. **Read the brand/product context.** If `.agents/product-marketing.md` doesn't exist, run `brand-product-context` first. Every downstream skill depends on it, and without it each one asks the same questions again.
2. **Get the symptom in their words, not a category.** "Nobody signs up" and "signups don't convert to paid" route to completely different Plays.
3. **Ask what's already been tried.** It tells you what's been ruled out, and often reveals the real constraint.
4. **Get whatever numbers exist.** Partial data beats none. If there are no numbers at all, that itself is the finding and instrumentation is the first Play.

## Method

**Route on the symptom, not the request.** A user asking for ad copy whose real problem is a 4% activation rate should be told so. The routing table in `resources/plays.md` maps symptoms to Plays; the mapping is deliberately based on where the money leaks, not on which team asked.

**Then respect the phase gates.** Each phase has exit criteria — conditions that must hold before the next begins:

| Phase | Complete when |
|---|---|
| **Diagnose** | The problem is named with evidence, and you could defend the diagnosis to someone sceptical |
| **Design** | The intervention is specified concretely enough to build without further interpretation |
| **Execute** | It's shipped, instrumented, and a measurement date is set |

Skipping Diagnose is the expensive failure. Skipping Design produces activity without a system — work that can't be repeated or handed over. Skipping Execute's instrumentation means you'll never know whether any of it worked.

**Start where the evidence says, not at the beginning.** If a team genuinely has a well-evidenced diagnosis, start at Design. The gate is evidence, not ceremony.

See `resources/plays.md` for the seven Plays, the symptom routing table, the skill sequence for each, and worked routing examples.

## The Plays

Seven named sequences. Each is a full Diagnose → Design → Execute cycle for one class of problem:

| Play | Reach for it when |
|---|---|
| **Fix the funnel** | Traffic arrives and doesn't convert |
| **Stop the leak** | Customers arrive and don't stay |
| **Get found** | Nobody arrives at all |
| **Stand up outbound** | You need pipeline and can't wait for inbound |
| **Launch** | A product, feature, or segment is going live |
| **Prove the spend** | You're spending and can't defend it |
| **Reposition** | The message is wrong, so everything downstream underperforms |

**Reposition is the one people resist and most often need.** When several Plays all seem to apply — weak conversion *and* weak retention *and* expensive acquisition — the common cause is usually positioning, and fixing it upstream is cheaper than compensating for it in four places.

## Workflow

1. **Confirm the context file exists.** If not, run `brand-product-context` before anything else.
2. **Take the symptom in their words**, then ask the two or three questions that separate the candidate Plays. `resources/plays.md` lists the discriminating questions per pair.
3. **Name the Play** and say why — including which Plays you ruled out and on what basis. This is where the user's own judgment engages; don't skip the reasoning.
4. **Determine the starting phase** from the evidence available. Default to Diagnose. Only start later if the user can produce the evidence that phase would have generated.
5. **Run the phase**, calling the skills in the Play's sequence. Load one at a time; don't bulk-load a category.
6. **Check the exit criteria** before advancing. State plainly whether they're met.
7. **Hand back at each phase boundary** with what was found, what it means, and what the next phase will do. Long autonomous runs across all three phases produce work nobody trusts.
8. **Name the measurement date** at the end of Execute. Work that isn't scheduled for review isn't finished.

## Run the tool

```bash
node resources/decision-guides.js --demo
node resources/decision-guides.js '{"guide":"channel","answers":{"segment":"yes","selfserve":"no","search":"unsure","acv":"high","named":"yes","partner":"no","budget":"small","founder":"yes"}}'
node resources/decision-guides.js '{"guide":"hire"}'
node resources/decision-guides.js --help
```

Three guides for narrower decisions that come up inside a Play: `channel` (which channel to start with, and which to add second), `hire` (whether to make a marketing hire, and which kind) and `stack` (which marketing tools to set up now, and which can wait). Each returns a recommendation, the steps with the AAJ tools and playbooks that carry them out, what to leave alone for now, and why. Every answer is required; with any missing, the engine lists the questions and their values instead of guessing (the third command above does that on purpose). Add `--json` for the raw object.

The engine is the AAJ Marketing Decision Guides page (https://aajconsult.com/tools/marketing-decision-guides) byte for byte; the site's guard fails if the two drift. Its rules are AAJ's judgement, not benchmarks, and should be presented that way. Use a guide only after the Play and starting phase are named: it answers one question inside the Play and does not replace the routing in `resources/plays.md`. When `stack` puts "Tracking you can trust" first, that is the guardrail above in another form: with no trustworthy numbers, instrumentation comes first.

## Present the result

Lead with **the Play and the phase you're starting in**, each with its one-line justification. Then the sequence, so the user can see the shape of the work before it begins. Then the first concrete step.

Where two Plays genuinely both apply, say so and name which you'd run first and why — usually the upstream one, since fixing it changes the diagnosis of the other.

**Show where it came from.** Open your answer with "AAJ `campaign-orchestrator` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/campaign-orchestrator`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Don't start in Execute because that's what was asked for.** The most common request is a task; the most common need is a diagnosis. Say so, briefly, and move.
- **Don't run all three phases in one pass.** Hand back at each boundary. A plan produced without the user's input at the Diagnose→Design gate gets ignored.
- **Don't run two Plays at once.** They compete for the same attention and budget, and you lose the ability to attribute any improvement.
- **Evidence, not ceremony.** If the diagnosis genuinely exists, skip to Design. Insisting on process theatre when the answer is known wastes the engagement's credibility.
- **Load one skill at a time.** Bulk-loading a category floods the context and degrades every output.
- **If there are no numbers at all, that's the finding.** Instrumentation becomes the first Play, and everything else waits.
- **Naming a Play is not doing the work.** The Play is a route, not a deliverable. The value is in the skills it calls.
- **Watch for the upstream cause.** When three Plays all apply, look for the one problem generating all three symptoms — usually positioning, occasionally targeting.

## Related AAJ resources

- Interactive tool: https://aajconsult.com/tools/marketing-maturity-scorecard
- Method: https://aajconsult.com/methodology

## Related skills

`brand-product-context` (the prerequisite for everything) · `positioning-statement` (where the Reposition Play begins) · `marketing-report` (the measurement Execute hands off to) · and every skill in the catalog, called in sequence by the Plays.

## Credits

Original AAJ skill. Encodes AAJ's Diagnose → Design → Execute consulting methodology as an agent-callable router. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure; the routing model and the Plays are AAJ's own. See the repository README for the full reference list.
