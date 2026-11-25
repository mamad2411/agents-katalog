---
name: model-cost-optimizer
description: Finds the cheapest model that passes YOUR eval for a given job — define the job, tier candidate models frontier/mid/cheap/local, run the same eval per tier from cheapest up, pick the lowest passing tier. Use when the user says "which model should I use", "this is getting expensive", "can a cheaper model do this", "downgrade the model", or is assigning a model to a recurring agent task. Don't use for building the eval itself — that's agent-eval-harness, and it must exist first.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Agent Mastery, Cost, Models, Evals, Optimization]
    related_skills: [agent-eval-harness, context-budget-manager, budget-guardrails]
---

# Model Cost Optimizer

The course's first law: the right model is the cheapest brain that passes YOUR eval — not the smartest one available, not the one with the best vibes. This skill makes that choice mechanical: same eval, every tier, cheapest first, pick the lowest passer. The iron rule: never optimize cost before the eval exists, because without an eval "cheaper worked fine" just means "nobody measured the damage."

## When to Use

- Assigning a model to a recurring job (a skill, a Paperclip agent role, a cron/blueprint task).
- A working setup feels overpowered ("do I really need frontier for email triage?").
- Monthly spend review flags a job as a top cost line (pair with `budget-guardrails`).
- **Not for:** writing the eval (`agent-eval-harness` — go there first if none exists), or shrinking per-call token usage (`context-budget-manager` — do that before blaming the model tier).

## Quick Reference

| Tier | Examples (fill with current lineup) | Rough cost | Typical fit |
|---|---|---|---|
| Frontier | top Claude/GPT/Gemini flagship | $$$$ | multi-step reasoning, high-stakes writing, agentic planning |
| Mid | the flagship's smaller sibling | $$ | solid drafting, summarization, structured extraction |
| Cheap | mini/flash/haiku class | $ | classification, routing, formatting, simple Q&A |
| Local | small open model on own hardware | ~$0/call | private data, unlimited-volume simple tasks |

| Action | Rule |
|---|---|
| Order of testing | Cheapest plausible tier first, ladder UP only on FAIL |
| Decision | Lowest tier that PASSES the eval wins — full stop |
| Cost delta | Report $/run and projected $/month for chosen vs. frontier |

## Procedure

1. **Precheck: does the eval exist?** — locate `evals/<task-name>.md` with committed rubric + threshold. If missing, STOP and run `agent-eval-harness` first. This step has no workaround; a cost decision without an eval is a guess wearing a spreadsheet.
2. **Define the job's stakes** — one line: what breaks if quality slips (annoyance? money? reputation? safety?). High-stakes jobs (money movement, external comms, security decisions) set a floor: never below mid tier regardless of eval results, and note this in the verdict.
3. **List candidates per tier** — name one concrete model per tier from the currently available lineup, with $/1M input and output tokens from the provider's live pricing page (prices move; look them up, don't recall them). Skip tiers that are obviously implausible, but write down why you skipped them.
4. **Estimate volume** — runs/month × avg tokens/run (measure one real run, don't guess). This turns per-call deltas into a real monthly number — the difference between tiers is often the difference between $2 and $200/month.
5. **Run the eval, cheapest first** — execute the FULL saved eval (fresh sessions, same rubric) on the cheapest plausible tier. PASS → it's your answer; run one tier up only as a sanity reference if stakes warrant. FAIL → record which cases failed and ladder up one tier. Repeat until a tier passes.
6. **Pick the lowest passing tier** — mechanically. "The frontier output felt nicer" is not a criterion the rubric scored. If nicer matters, that's a missing rubric criterion — go amend the eval via `agent-eval-harness` and re-run, don't freestyle the decision.
7. **Report and wire it in** — fill the template below, get the user's confirm, then set the model in the skill/agent config. Log the decision + eval date so the next reviewer knows what evidence backed it.
8. **Set a re-check trigger** — re-run this procedure when: the eval changes, the model lineup changes, or a downstream failure traces back to model quality. Note the trigger in the report.

## Output Template

```
## Model choice: <task/skill name> — <date>
Eval: evals/<task-name>.md (threshold <n>/<total>) | Volume: ~<runs>/mo

| Tier | Model | Eval result | $/run | $/month |
|---|---|---|---|---|
| Cheap | <model> | FAIL (2/5) | $0.002 | $0.40 |
| Mid | <model> | PASS (5/5) | $0.02 | $4.00 |
| Frontier | <model> | not run — mid passed | $0.15 | $30.00 |

CHOSEN: <tier — model>
Savings vs frontier: $<n>/month (<x>%)
Stakes floor applied: <none | mid-tier floor because [reason]>
Re-check when: eval changes | lineup changes | quality incident
```

## Pitfalls

- **Optimizing before the eval exists** — picking cheap on price alone, discovering quality rot weeks later in production. Recovery: freeze the model change, build the eval with `agent-eval-harness`, re-run this procedure properly; if cheap already shipped, eval it retroactively before deciding it gets to stay.
- **Testing frontier first** — its polished output becomes the anchor and every cheaper model "feels worse" regardless of rubric. Recovery: cheapest-first order is part of the method; if you anchored, blind yourself to which output came from which tier and re-score against the rubric only.
- **Eval passes, production fails** — the cheap tier passed but real traffic is messier than the 5 cases. Recovery: add the failing real-world inputs as new eval cases, re-run the ladder; the eval getting harder over time is the system working.
- **Stale pricing math** — cost table built on remembered prices that changed last quarter. Recovery: re-pull pricing from provider pages at decision time, recompute $/month, re-check the verdict still holds.
- **Ignoring the stakes floor** — a cheap model passes the eval for outbound payment emails, and one hallucinated sentence costs more than a year of frontier calls. Recovery: apply step 2's floor for high-stakes jobs and record it; cost optimization ends where blast radius begins (see `budget-guardrails`).

## Verification

- [ ] Eval file existed (with pre-committed threshold) before any cost decision
- [ ] Every tested tier ran the FULL eval under identical conditions
- [ ] Chosen tier = lowest passing tier, or a written stakes-floor override explains why not
- [ ] $/run and $/month computed from live pricing and one measured real run
- [ ] Decision, eval date, and re-check triggers logged where the next person will find them
