---
name: model-selection-router
description: >-
  Route every AI job to the cheapest model that survives review, and stop
  defaulting to the frontier out of habit. Use whenever someone asks "which
  model should I use", "is the expensive model worth it", "should we switch
  models", "a new model came out — do we move?", "the benchmark says X is
  best", "we're overpaying for AI", "what should our default model be", or
  wants help with model routing, tiering, or per-task model assignment. Also
  fires on: choosing reasoning-effort settings, building a personal eval set,
  fighting a bad corporate default model with evidence, triaging an agent/tool
  launch, or spec'ing a whole job for an expensive frontier run. Covers
  three-tier routing (daily driver / cheap workhorse / frontier) plus
  specialists, the seven job-classification questions, benchmark-interpretation
  discipline, 30-minute and one-week eval protocols, and the five-question
  new-launch filter. If a model name appears before the work has been
  described, this skill applies.
---

# Model Selection Router

## Purpose

Most teams route AI work by habit: one model for everything, chosen once, defended by loyalty. The result is a double tax — frontier prices paid for workhorse jobs, while genuinely hard work gets under-specified prompts that waste the premium anyway.

This skill inverts the order of operations: **describe the work first, then pick the intelligence.** It gives you a job-classification method, three-tier routing with escalation rules, a discipline for reading benchmarks without being fooled by them, lightweight eval protocols run on your own work, a briefing format that makes expensive models pay off, and a triage filter for new launches. Everything is model-agnostic by design — the method survives model churn; the examples don't have to.

Run **work-shape-triage** first if the open question is whether this work should go to a model at all; this skill assumes the answer is yes and decides *which* one. For token spend dashboards and cost governance once routing is in place, see **agent-ops-governance** (same pack).

## Core model

### The three tiers plus specialists

Every recurring job lands in one of three tiers, with specialists layered on as needed (framework synthesized from practitioner reports, 2026):

1. **Daily driver** — a strong general model on a good work surface. Reserved for unclear, mixed, taste-heavy, high-judgment work where you don't yet know the shape of the answer. This is your thinking partner, not your assembly line.
2. **Cheap workhorse** — the fat middle of routine artifacts: decks, summaries, support replies, standard code changes, extraction, first drafts. The test rule: **if you can describe what "good" looks like before the run starts, and you can review the result quickly, try the cheap route.** A mediocre cheap draft is fixable in minutes.
3. **Frontier model** — earns its premium only when being *directionally* wrong is expensive: when the shape of the artifact is itself the problem. A missed problem-shape costs hours or days; that is what you are buying insurance against, not marginally nicer prose.

**Specialists** attach to any tier for three add-ons: *senses* (vision, audio, PDF parsing), *sources* (live web, archives, CRM, repo access), and *hands* (file edits, test runs, browser action). Once a job needs one of these, the harness and integration matter more than raw model quality.

Corporate overlay: inside a company, the first routing filter is **permission**, not capability — sensitive or policy-restricted data stays in approved tools regardless of benchmark deltas.

### The seven job-classification questions

Before any model name enters the discussion, classify the job:

1. **Ambiguity** — is the task familiar and well-shaped, or ambiguous?
2. **Definable good** — can you write down what "good" looks like before the run?
3. **Inspectability** — can you check the result quickly, or is review itself expensive?
4. **Sensitivity** — is the data sensitive or policy-restricted?
5. **Modality** — does it need special inputs (audio, screenshots, video, live web, a repo)?
6. **Action** — does the system need to *act* (edit files, run tests, drive a browser)?
7. **Context location** — does the needed context already live where the model can reach it, or will you re-paste it every time?

Questions 1–3 pick the tier. Questions 4–7 pick the specialist, harness, and deployment surface. Answers of "ambiguous / can't define good / slow to review" push up-tier; "familiar / definable / fast to check" push down-tier.

### Benchmark-interpretation discipline

A model can top a strict benchmark suite and still be the wrong default. Rules for reading launch numbers (practitioner benchmark analyses, 2026):

- **Suite leader ≠ default.** Individual test results beat the average — a suite winner can lose specific task types (visualization, long-horizon operations) to a lower-average rival. Route by per-task results, never by leaderboard rank.
- **Split every job by failure mode** — source risk, visual risk, operational risk, review risk — and route and QA each slice separately.
- **Reasoning effort is part of model selection.** Maximum effort has been observed *underperforming* high effort on long-running work: heavier reasoning burns context, forces more compactions, and loses working state. Tiering rule: default to high; use extra effort for hard, bounded, verifiable problems; reserve max for narrow, high-value reasoning over a controlled source set. If max makes output slower and less useful, turn it down.
- **Four adoption risks** when a new leader appears: (a) visual/front-end regressions hiding behind text-benchmark gains; (b) effort sensitivity — the model may need retuned settings; (c) honest-vs-effective divergence — your evals must reward both truthful behavior (source discipline, flagging uncertainty) and effective behavior (shipping the artifact), because a model can score well on one while failing the other; (d) harness fit — the same weights behave differently across chat, agent, and API surfaces.

Keep model names in your routing table as dated examples, not commitments. As of mid-2026 the leaders change quarterly; a table that says "[frontier model of record] for problem-shaping, [current cheap workhorse] for drafts" with a review date outlives any single pick.

### The whole-job spec (for frontier runs)

Expensive models punish prompt-sized asks economically; they pay off on whole jobs. Brief them like a senior hire, with nine fields:

1. **Outcome** — name the finished artifact. If you can't, the job isn't ready for a frontier run.
2. **Source pack** — everything a skilled human would need: files, exports, examples of good.
3. **Tool access** — read / edit / run / draft-only; which systems are off-limits.
4. **Boundaries** — never-touch items, mid-run approval points, citation requirements.
5. **Work plan** — the inspection and verification order a careful person would follow.
6. **Cost route** — cheap models handle extraction, dedupe, and first passes; the expensive model gets synthesis, judgment, repair, and long runs.
7. **Review standard** — a written definition of good; models rise to an explicit bar.
8. **Proof trail** — what changed, what was read, what failed, what remains uncertain. Work without receipts is plausible, not done.
9. **Human gate** — a named approver, named before the run starts.

**The 70% diagnostic rule:** expect first runs to come back roughly 70% right. Treat every flaw as a diagnostic pointing at a specific spec field — a wrong artifact shape means field 1 was vague; a fabricated fact means field 2 or 8 was missing — tighten that field and rerun. Cost logic: compare the run against the work never getting done, not against a cheaper model.

### Context beats marginal intelligence

Evaluate any assistant or surface on four questions: what can it **see**, what can it **do**, what does it **remember**, and how do you **check** it. Weak answers mean perpetual re-briefing regardless of model IQ. A good-enough model inside the right context beats a better model outside it — which is why "switch to the new leader" is so often the wrong move.

## Workflow

Run these steps in order for a full routing setup; steps 4–5 alone answer "should we adopt model X?"

**1. Inventory current usage and spend.** List every recurring AI job for [your team/workflow]: what's produced, how often, which model handles it today, and monthly cost in licenses or tokens. Habit routing is invisible until written down — expect to find frontier-priced jobs that are pure workhorse material.

**2. Classify each recurring job** with the seven questions. Record the answers; they are the routing rationale you'll defend later.

**3. Assign tiers.** Apply the test rule — describable good + fast review → cheap workhorse; ambiguous or taste-heavy → daily driver; directionally-expensive-to-miss → frontier with a nine-field spec. Attach specialists where questions 5–6 demand senses, sources, or hands. Apply the permission filter before everything else.

**4. Build a personal eval set** of 3–5 tasks from your real work, ideally covering: one writing/synthesis task, one messy-data/reconciliation task, one coding task, one visual artifact, and one long-running stateful task. Score every candidate on: correctness, source discipline, review burden, time-to-accepted-artifact, cost, failure behavior, visual quality, and whether the model knew what it didn't know. Test effort settings explicitly, not just model identity. The acceptance question for every output: **would I have shipped this, and how many review minutes did it cost?** A cheap model that doubles review time is expensive; a specialist that fixes a missing input can beat a smarter generalist.

**5. Run the lightweight protocols** on candidate routes:
   - **30-minute test**: take one recurring artifact, run it through two routes (e.g., current default vs. cheap challenger), time the review, label each output *usable / repairable / rejected*, and note the failure mode.
   - **One-week test**: five real artifacts, two runs each; track model, source material, review minutes, acceptance, data sensitivity, and failure mode. Promote the cheap route only where review stays cheap.

**6. Set routing defaults and escalation rules.** Write the routing table down — job class, default route, effort setting, escalation trigger ("escalate to [frontier tier] when the draft misses the problem shape twice" is a rule; "when it feels off" is not). If you're fighting a bad organizational default, escalate with measurement, not opinion:
   - Pick one job that runs at least weekly, costs ≥30 minutes, has instantly judgeable output, and a real audience. Run it through default and challenger with identical inputs for one week.
   - Keep a **four-column log**: time spent, rework needed, quality 1–5 with a one-line reason, would-you-send-as-is (yes/no).
   - **Ask smaller than the evidence**: request one specialist license for one job class. Never propose ripping out the default — its procurement rationale was legitimate; you're adding a specialist for the slice it fails.
   - **Three altitudes**: IC→manager = the log plus one license request; manager→director = a time-boxed team pilot with report-back; director→exec = commissioned measurement of the top job classes company-wide, framed as removing an invisible distributed tax.

**7. Re-triage on every notable launch** with the five-question filter:
   1. Does it plug into tools you already use, or demand migration? (Migration is the costliest ask.)
   2. Can other agents and tools build on it, or is it closed? Infrastructure compounds; features commoditize.
   3. Does it own or access data you care about? Data access beats model quality — a mediocre agent with your full history beats a great agent with none.
   4. Is an ecosystem forming (marketplace, SDK, ship cadence)?
   5. Can you stack on top of it? Composable launches multiply; standalone ones merely add.

   Most launches fail the filter; the ones that pass earn an afternoon against your eval set from step 4. Then make a **layering decision, not a switching decision**: (a) stay in your default's direct product when the model is the center of the work; (b) pay for a wrapper running the *same* model when it delivers a data fabric you can't replicate; (c) adopt a different model only when the surrounding product fits the work shape better than marginal model quality matters. Switching costs are real — prompts don't transfer, memory doesn't port, team habits restart.

## Guardrails

- **Never route by leaderboard average.** Turning a suite winner into a procurement plan or personal default is the single most common selection failure. Route by per-task results and failure modes.
- **Never let a model self-certify its own work.** Self-assessments are systematically biased (some models oversell, others undersell), and models can hallucinate audit trails — claiming to have processed files they never read. For financial, legal, or reputational stakes, require cross-model peer review: one model audits the other's output. For data work, require source provenance, rejected-record lists, conflict tables, row-count checks, and a human review queue in the prompt itself. "Is this a real person?" remains a human check — planted trap records still slip past frontier models.
- **Don't assume max reasoning effort means best output**, especially on long-running work. Test effort settings as part of selection.
- **Don't assume the newest version wins every workload.** Capability shifts in releases are directed, not uniform — coding can improve while web research regresses. Believe your own eval when it disagrees with the launch narrative, and route regressed slices elsewhere.
- **Watch for literalness and silent cost shifts on upgrades.** A more literal model stops guessing your intent; the fix is clearer intent up front (what you're building, for whom, constraints, success criteria), not longer prompts. Tokenizer and adaptive-reasoning changes can raise real cost while sticker price holds — regression-test your prompt inventory before trusting the cost math.
- **Don't ask an execution-strong model to invent taste from a blank canvas.** For visual work, generate or supply a reference and have the model implement it faithfully; two-model workflows (one plans and critiques, one executes) beat single-model loyalty.
- **Availability is part of model quality.** Caps, latency, and downtime make a slightly-better model less valuable than a reliably-served one.
- **Measure accepted output, not activity.** Seats, tokens, and agent run-counts are vanity metrics; if agents generate work faster than review can absorb it, you've built a backlog machine.
- **Don't collapse model and harness into one judgment.** The same weights behave differently across chat, agent, and API surfaces; a strong model in a weak harness is a weak product.
- **Keep your assets portable.** Don't bet your architecture on one lab staying permanently ahead. The durable assets are your eval set, your routing table, your context stores, and your review gates — built so you can swap models without rebuilding. Run the exit test before deep adoption: who holds the accumulated context, can you export, inspect, revoke, and re-route it, keep sensitive parts local, and prove what the assistant saw and did?
- **Attribution note:** frameworks synthesized from practitioner reports (2026). Model names are dated examples; re-validate before quoting specifics.

## Suggested effort

- **Quick routing call on one job** (which tier does this go to?): run the seven questions and the test rule — 5 minutes, no tooling.
- **Adopting or rejecting a new model**: five-question filter (10 minutes) → if it passes, 30-minute test → if promising, one-week protocol. Total: under two hours of active attention spread over a week.
- **Full team routing setup** (steps 1–6): roughly half a day of inventory and classification plus a one-week measurement window. Revisit the routing table quarterly or on any launch that passes the filter — whichever comes first.
- **Fighting a corporate default**: one week of four-column logging on one job before saying anything. Evidence first; the ask stays smaller than the evidence.
