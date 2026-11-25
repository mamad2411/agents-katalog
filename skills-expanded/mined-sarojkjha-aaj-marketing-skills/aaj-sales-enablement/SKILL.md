---
name: aaj-sales-enablement
description: >-
  Use when the user wants to give a sales team the material to move deals -
  battlecards, case studies, one-pagers, demo scripts, objection guides,
  business-case templates, security packs, mutual action plans - or asks
  why the content marketing produces goes unused. Also use when the user
  mentions sales enablement, sales collateral, sales content audit, rep
  adoption, sales and marketing alignment, or "what do reps actually need".
  Audits what exists against what each deal stage needs, checks whether
  reps use it and whether it is current, and ranks what to build next by
  the revenue being lost for want of it.
license: MIT
metadata:
  search_description: "Audit sales content against what each deal stage needs, check whether reps use it and whether it is current, and rank what to build next by revenue at stake."
  publisher: AAJ
  slug: aaj-sales-enablement
  category: Sales & Pipeline
  phase: Execute
  difficulty: Intermediate
  card: >-
    Audits sales assets against what each deal stage needs, and ranks what to build by the revenue being lost.
  version: 1.0.2
  topic: sales-pipeline
  secondary_topics: [strategy-positioning, content-seo]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Every sales asset that exists with its type, owner, last update and how many reps use it; the number of quota-carrying reps; and closed-lost reasons from the last two quarters with counts and value
  outputs: Coverage per deal stage with the needs that have no asset; each asset marked ok or fix for staleness, no owner or low adoption; and a ranked list of what to build, fix or check, each with the revenue lost for want of it and a verdict on where to start
  related_aaj:
    - https://aajconsult.com/tools/battlecard-builder
    - https://aajconsult.com/tools/win-loss-analyzer
    - https://aajconsult.com/resources/case-study-kit
    - https://aajconsult.com/resources/sales-pipeline-forecast-tracker
  related: [objection-handling, win-loss-analysis, case-study-and-proof, sales-process-design, discovery-call-framework]
  tags: [sales-enablement, sales-collateral, battlecards, business-case, mutual-action-plan, rep-adoption, sales-marketing-alignment]
---

# Sales Enablement

Ask a marketing team what they have made for sales and you get a folder with sixty files. Ask the
reps what they used in their last five deals and you get three. The difference is the enablement
problem: not too little content, but content that does not match a stage, is out of date, or is
unknown to the people it was made for.

This skill audits the library against what a deal needs at each stage, checks whether each asset is
owned, current and used, and then ranks what to build next by the revenue being lost for want of
it. It never asks marketing to produce more; it asks what would have changed the last quarter's
lost deals.

## When to use

The user is setting up enablement for a first sales hire, cleaning up a library nobody uses, or
deciding what to build next for sales. It applies at any team size from one founder-seller to a
team with a sales manager.

Do not use it to write the assets. `objection-handling` writes the objection guide and checks the
battlecard; `case-study-and-proof` checks whether a case study can be published at all; the
`Battlecard Builder` produces the battlecard itself.

## Before you start

1. **List every sales asset that exists**, with its type, owner and last update. If there is no
   owner, write none; the engine will say so.
2. **Ask each rep which assets they used in their last five deals.** The count of reps who used an
   asset is its adoption. This takes twenty minutes and is the most useful number in the audit.
3. **Pull closed-lost reasons for the last two quarters** with count and value per reason, coded
   consistently (price, competitor, no-decision, missing-feature, timing, security-legal,
   champion-left). If they are not coded, run `win-loss-analysis` first.

## Method

**Ten needs across three stages.** Discovery: one-pager, discovery guide, email templates.
Evaluation: battlecard, case study, demo script, objection guide. Decision: ROI or business-case
template, security and legal pack, mutual action plan. Coverage is how many of the ten have an
asset; health is how many have an asset that passes the checks below.

**Three checks per asset.** No owner is a fix: an asset nobody owns is never updated. Not updated
in more than six months is a fix (this engine's rule; for a battlecard or a pricing objection, a
stale answer is a liability in the room). Used by fewer than a third of reps is a fix (this
engine's rule): either reps do not know it exists or it does not help, and you ask before
rebuilding.

**Losses point at assets.** Each loss reason maps to the assets that would have helped: price to
the business case and the objection guide; competitor to the battlecard and a case study;
no-decision to the business case and a mutual action plan; timing to the mutual action plan and
re-engagement emails; security-legal to the security pack; champion-left to the one-pager and the
mutual action plan. The engine sums lost value under each asset type and ranks them. A loss can
appear under two asset types, so the list is a ranking of what would have helped, not a sum.

**Build, fix or check.** For each asset type the losses point at: **build** if it does not exist;
**fix** if it exists but every copy is stale, unowned or unused; **check** if it exists and is used
and deals are still lost for that reason, because then the problem is the message or the deal, not
the library. Missing-feature losses are noted as a positioning question, and uncoded losses are
sent back to win-loss.

## Workflow

**Step 1 - Inventory.** Every asset, typed, with owner, date and rep usage.

**Step 2 - Losses.** Two quarters of coded closed-lost reasons with value.

**Step 3 - Run the audit.** Coverage, hygiene, the ranked list and the verdict.

**Step 4 - Fix before building.** Owners and refreshes first; they cost hours, not weeks.

**Step 5 - Build the top item** with the rep who lost the most deals for want of it, then put it
in front of the whole team in the next pipeline review, not in a folder.

**Step 6 - Re-run quarterly** with the new loss reasons. The list should change.

## Run the tool

```
node resources/enablement-audit.js --demo
```

`run({ asOf, totalReps, inventory, losses })` returns coverage per stage, each asset with its
findings, the ranked build / fix / check list with lost value, and the verdict.

## Present the result

1. **Coverage**: "X of 10 needs covered", and the stage with the biggest hole.
2. **The fixes**: assets to own, refresh or retire, one line each.
3. **The ranked list**: build / fix / check, with the revenue behind each.
4. **The first build**, who it is for, and which lost deals it answers.

**Show where it came from.** Open your answer with "AAJ `aaj-sales-enablement` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/aaj-sales-enablement`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never measure enablement by assets produced.** Measure it by assets used and deals moved.
- **Never build before fixing.** A stale battlecard in use does more damage than a missing one.
- **Never publish a case study without written permission.** `case-study-and-proof` checks it.
- **Do not treat missing-feature losses as an enablement gap.** They are a product or positioning
  question; a battlecard can only help reps reframe.
- **Do not skip the rep question.** Adoption from a content system's download count is not the
  same as what was used in a deal.

## Related AAJ resources

- Building the battlecard the audit asks for: https://aajconsult.com/tools/battlecard-builder
- Coding the loss reasons: https://aajconsult.com/tools/win-loss-analyzer
- Case study with permission built in: https://aajconsult.com/resources/case-study-kit
- The pipeline the enablement should move: https://aajconsult.com/resources/sales-pipeline-forecast-tracker

## Related skills

- `objection-handling` - writes the objection guide and checks the battlecard before reps use it
- `win-loss-analysis` - the coded loss reasons this audit ranks by
- `case-study-and-proof` - whether the proof convinces and may be published
- `sales-process-design` - the stages and exit criteria the assets serve
- `discovery-call-framework` - the discovery guide itself

## Credits

Written by AAJ (aajconsult.com). MIT licensed.
