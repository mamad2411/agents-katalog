---
name: first-marketing-hire
description: >-
  Use when the user is hiring their first marketer or first head of marketing
  and wants to define the role, run a fair interview process and choose on
  evidence. Also use when the user mentions a marketing hire scorecard,
  interview questions for a marketer, a take-home or work-sample task, an
  interview debrief, comparing candidates, a marketer's first 90 days, or
  "who should our first marketing hire be". Produces a weighted role
  scorecard, a paid take-home brief and rubric, interview questions tied to
  competencies, a 90-day plan, and a hire, no-hire or more-evidence call.
license: MIT
metadata:
  search_description: "Hire your first marketer on evidence: a weighted role scorecard, a paid take-home and rubric, interview questions, a 90-day plan, and a clear hire call."
  publisher: AAJ
  slug: first-marketing-hire
  category: Growth, Retention & RevOps
  phase: Design
  difficulty: Starter
  card: >-
    Writes the first marketer's scorecard, then scores the panel's evidence and calls hire, no-hire or more evidence.
  version: 1.0.1
  topic: ops-ai-team
  secondary_topics: [gtm-growth-planning]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The stage, the channel that already brings in most customers, what the hire must own in months 1 to 6, competencies with weights and must-haves, and each interviewer's 1-4 ratings with an evidence note per competency
  outputs: A role scorecard, a paid take-home brief with rubric, interview questions by stage tied to competencies, a first-90-days plan, and per candidate a weighted score, must-haves below bar, ratings without evidence, interviewer disagreements and a hire, no-hire or more-evidence call
  related_aaj:
    - https://aajconsult.com/templates/first-marketing-hire-kit
    - https://aajconsult.com/blog/first-marketing-hire
    - https://aajconsult.com/tools/marketing-leadership-cost-comparator
    - https://aajconsult.com/blog/fractional-cmo-vs-inhouse-marketing-team
  related: [marketing-leadership-model, marketing-budget-planning, campaign-orchestrator, brand-product-context]
  tags: [first-marketing-hire, hiring, scorecard, interview, take-home, work-sample, first-90-days, team-design]
---

# First Marketing Hire

A first marketing hire goes wrong in one of two ways: a senior leader who expects a team and a
budget that do not exist, or a junior coordinator who expects direction nobody has time to give.
Both come from hiring before the job is written down. This skill writes the job first (what the
hire must own by month six, the one deep skill behind the channel that already works, and the few
must-haves), then holds every candidate to that page, counting only ratings that carry evidence.

## When to use

The user has decided to hire (or is close) and needs the role defined, the process designed, or
the candidates compared. If the user is still deciding whether to hire at all, or between a hire,
a fractional leader and an agency, run `marketing-leadership-model` first.

## Before you start

1. **Read the brand/product context first.** If `.agents/product-marketing.md` (or
   `.agents/aaj-brand.md`) exists, take the ICP, buyer, channels and stage from it. If not, ask.
2. **Check there is something to amplify.** Three signals: retention in one segment, one channel
   that produces customers at a cost the company can afford, and founder time as the constraint.
   If one is missing, say so and stop; a hire will not create product-market fit.
3. **Find the working channel from data.** Ask where the last 10 to 20 customers came from (CRM
   source fields, and asking the customers). The deep skill to hire for is the one behind that
   channel, not the one the founder wishes worked. If no channel stands out, the company is not
   ready to hire for depth.
4. **Name what is missing.** "We have ___, and we are missing ___." Strategy missing and
   execution missing need different hires.

## Method

**Generalist with one deep skill.** For a seed-stage first hire, AAJ's view is a hands-on
generalist with depth in the working channel, with senior strategy kept by a founder or a
fractional leader. This is practice, not research; say so if asked. At Series A or B, with
channels proven and budget to hire under them, the role may be a head of marketing who has built
a team.

**Outcomes before competencies.** Write what the hire must own at months 1, 3 and 6. Derive the
competencies from those outcomes. Keep must-haves to four or fewer.

**Evidence or it does not count.** Ratings are 1 to 4 with no middle (1 strong no, 2 no, 3 yes,
4 strong yes). Every rating needs an evidence note: what the candidate said or did. The engine
leaves a rating without a note out of the score and flags notes under four words as thin.

**One voice per interviewer.** Each interviewer's ratings on a competency are averaged first, so
someone who rated the same thing at three stages does not outvote the panel.

**The call, in this order (AAJ's rules, labelled as such):**

```
1. A must-have below its bar (default 3), with the panel agreeing      -> NO-HIRE
2. A must-have with no evidenced rating, or interviewers >= 2 apart    -> MORE-EVIDENCE
3. Evidenced ratings cover < 80% of the weight                         -> MORE-EVIDENCE
4. Weighted score below the hire line (default 3.0)                    -> NO-HIRE
5. Otherwise                                                           -> HIRE (then references)
```

A must-have below its bar but with the panel 2 or more apart is more evidence, not a no: the
panel saw different people. If nobody clears the bar, re-open the search rather than lower it.

**Paid work sample.** Every finalist gets the same short, paid project on the company's real
situation, capped in hours, scored against a rubric written before any answers are read, then a
30-minute debrief in which one assumption changes.

**First 90 days follow Diagnose, Design, Execute.** Days 1 to 30 learn (customers, sales calls,
tracking, win and loss notes); 31 to 60 fix the foundations (messaging, tracking, targets); 61 to
90 grow one channel (experiments, weekly report, the next channel to test). Agree the day-90
targets in writing before the candidate signs.

## Workflow

1. **Profile.** Fill in the role table, the month 1 to 6 outcomes and the competency list from
   `resources/kit-template.md` (Section 1). Run the engine on the role alone (leave out `candidates`) to see
   the profile warnings (too many must-haves, no channel focus, no outcomes).
2. **Take-home.** Write the brief and the rubric (Section 2) before the role is posted.
3. **Questions.** Pick questions per stage from Section 3; every question carries a competency
   code. Drop any question that maps to no competency.
4. **Score.** After each stage, collect each interviewer's ratings with evidence notes, before
   the panel talks. Run the engine.
5. **Resolve.** Act on the next steps it returns: get the example behind unevidenced ratings, put
   split interviewers in one room with their notes, cover unrated must-haves in the next stage.
   Re-run.
6. **Decide and onboard.** Present the call, then hand over Section 4 (first 90 days) and run
   Section 5 (offer checklist).

## Run the tool

```bash
node resources/hire-scorecard.js --demo
node resources/hire-scorecard.js '<json-config>'
node resources/hire-scorecard.js --help
```

`run({ role, candidates })` returns the normalised role (weights as shares, warnings, a stage
note), and per candidate: the weighted score (evidenced ratings only) and the score including
unevidenced ratings, evidence coverage of the weight, per-competency scores with each
interviewer's mean, the flags (must-haves below bar, no evidence, thin evidence, disagreements,
unrated, unknown competencies), the call with reasons, and next steps. The demo is three fictional
candidates for AAJ's fictional running case, Example Co.

## Reference

- `resources/kit-template.md`: the full kit in fill-in form (signals check, role scorecard,
  take-home brief and rubric, 17 interview questions across four stages tied to competencies
  C1 to C7, first-90-days plan, offer checklist). Same content as the downloadable Word kit at
  https://aajconsult.com/templates/first-marketing-hire-kit.
- `resources/hire-scorecard.js`: the scoring engine. Its rules are named constants at the top of
  the core block.

## Present the result

1. **The profile**: outcomes by month, competencies with weights, must-haves and bars, and any
   profile warnings.
2. **The decision table**: one row per candidate with weighted score, must-haves below bar,
   disagreements, ratings without evidence, and the call.
3. **What to do next** per candidate, in the engine's words.
4. **For the hire**: the reference question on the deep skill, then the day-90 targets and the
   offer checklist.

**Show where it came from.** Open your answer with "AAJ `first-marketing-hire` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/first-marketing-hire`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **No salary figures from memory.** Point the user to public wage data for the location (for
  example, US Bureau of Labor Statistics state and area wage data) and have them enter their own.
- **No legal verdicts.** Interview-question limits, pay-range disclosure, reference and
  background checks, employment status and equity terms differ by state and country. Tell the
  user to check them with counsel; never say a process "is compliant".
- **Do not let the total rescue a missed must-have.** A strong weighted score with a must-have
  below its bar is still a no.
- **Do not average away a disagreement.** Two interviewers 2 points apart are reporting
  different evidence; resolve it before scoring it.
- **Do not hire for a channel that has not been tested.** Test first, then hire to scale it.
- **Fictional examples stay labelled fictional.** Example Co. is not a client.

## Related AAJ resources

- The kit as a Word download: https://aajconsult.com/templates/first-marketing-hire-kit
- When to hire, who to hire and what they do first: https://aajconsult.com/blog/first-marketing-hire
- Hire, fractional or agency on your own numbers: https://aajconsult.com/tools/marketing-leadership-cost-comparator
- The trade-offs by stage: https://aajconsult.com/blog/fractional-cmo-vs-inhouse-marketing-team

## Related skills

`marketing-leadership-model` · `marketing-budget-planning` · `campaign-orchestrator` · `brand-product-context`

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written. See the repository README for the full reference list.
