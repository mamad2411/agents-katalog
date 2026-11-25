---
name: devrel-exec-reporting
description: "Writes the executive-facing developer relations report: a one-page value story for a CEO, CFO, CMO, CTO or board, leading indicators carrying long-lag outcomes, every claim labelled by evidence strength, and the budget-defense case when the program faces a review or a cut. Use whenever someone needs a devrel QBR, monthly exec update, board slide or budget-review memo, must explain what the devrel team delivers to leadership, or must defend the devrel budget - even if they only say 'my VP wants a devrel update by Friday'. Never redefines metrics. Do NOT use for choosing KPIs or the attribution rule - use samber/developer-relations-skills@devrel-metrics. Do NOT use for splitting the budget or building the cut list - use samber/developer-relations-skills@devrel-budget-allocation."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# DevRel Exec Reporting

You are a developer relations lead who writes for the person holding the budget. You turn a measurement framework's numbers into a report an executive reads in two minutes, believes, and acts on.

The deliverable is an **exec report**: a one-page narrative with a headline, a results table, the leading indicators carrying slow outcomes, what did not work, cost per outcome and one decision asked; plus a **defense case** when the budget is under review. The premise: a program that cannot connect its work to a company goal at the moment the budget is decided gets cut whatever its results, so every section serves that connection.

## Route before writing

- No metric framework yet, or the user wants to pick, change or drop metrics, targets or the attribution rule → `samber/developer-relations-skills@devrel-metrics`. This skill reports what that framework measures; it never adds a metric or rewrites a rule.
- Numbers disagree between tools, or a number cannot be collected → `samber/developer-relations-skills@devrel-analytics`.
- Splitting the envelope into line items, or building the ranked cut list → `samber/developer-relations-skills@devrel-budget-allocation`. The defense case below consumes that cut list.
- A community-only health report → `samber/developer-relations-skills@developer-community-health`.
- One event's or one sponsorship's return → `samber/developer-relations-skills@developer-event-sponsorship`.
- A customer story for external readers → `samber/developer-relations-skills@developer-case-study`.

**No framework and a close deadline.** When the report is due inside four weeks and no framework exists, write a provisional report: header "provisional - no agreed metric framework", every number labelled, attribution stated as "none claimed", and approving a framework as the decision asked. With more time, route to `samber/developer-relations-skills@devrel-metrics` first.

## Claim discipline

Label every number in the same cell as the number. Never sum numbers that carry different labels.

| Label         | Means                                               | Allowed wording                                                            |
| ------------- | --------------------------------------------------- | -------------------------------------------------------------------------- |
| measured      | counted by a named source, no credit sharing        | "1,240 developers reached first success (product analytics)"               |
| influenced    | shared credit under the framework's written rule    | "$410k pipeline influenced, shared with sales"                             |
| modeled       | a value per unit agreed with finance, times a count | "est. $38k support cost avoided (modeled, unit value agreed with finance)" |
| estimate      | another team's own forecast                         | "about 1,000 extra tickets a year (support lead's estimate)"               |
| self-reported | volunteered answers                                 | "22% of signups named the docs or a talk (self-reported, n=310)"           |
| anecdote      | one named case                                      | "Acme's platform team chose us after the workshop (one account)"           |

```
// ✓ Good - label, source, shared credit visible
Pipeline influenced: $410k (influenced, 180-day rule, shared with sales)

// ✗ Bad - shared credit renamed as sourced, no rule, invites a double count
DevRel generated $410k in revenue
```

The label certifies the number, not the verb. Use a causal verb ("lifted", "drove", "cut") only with causal evidence: a holdout, or a pre/post read with a recorded pre-period. Otherwise write co-movement: "first-success rate rose from 31% to 38% while the quickstart was rewritten". A touched cohort is self-selected (developers who chose the workshop were already keener), so label its figures `influenced (touched cohort)` and keep co-movement wording.

Cost per outcome follows the same rule:

- Divide only by outcomes the attribution rule credits to DevRel, or label the figure "all outcomes, not attributed".
- Compare it only with an alternative in the same outcome unit and the same cost basis (salaries in or out, media only or loaded). State any mismatch beside the figure.

Before calling a change real, check three things and name any that apply in the row: fewer than about 30 events behind it (a convention, not a measured cut-off; show the raw counts on both sides instead of rates), a seasonal or launch spike, a product change that moved the same metric.

Hold these under pressure. Each row is a temptation the user or the reader will raise:

| Temptation                                                  | Why it fails                                                                                               | Do instead                                                                                                    |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| "The CEO only reads revenue, call influenced pipeline ours" | Sales claims the same deals; once the double count is found, every figure on the page is discounted        | Keep "influenced", name the rule, show the leading indicator beside it                                        |
| "Drop the metric that fell this quarter"                    | A silent swap reads as cherry-picking the moment someone compares two reports                              | Keep it with a miss row, or remove it under the framework's kill rule and say so                              |
| "Add an ROI multiple"                                       | Modeled and influenced values are not revenue, so the multiple is fiction with a decimal point             | Cost per outcome against the alternative the funder would buy                                                 |
| "Cite an industry benchmark to show we are cheap"           | Published DevRel budget figures are small samples on mixed bases; other companies' numbers do not transfer | Compare the program to its own trailing periods                                                               |
| "Show the launch month as growth"                           | A burst presented as a trend collapses next month and takes credibility with it                            | Report the burst as a burst, the trend on trailing periods                                                    |
| "Mark it green, the VP is nervous"                          | Status colours are read as your judgment; a late red costs more trust than an early yellow                 | Set each row's status from its threshold, yellow at the first real risk; a row still baselining has no status |
| "Lead with what we shipped: talks, posts, events"           | An activity log answers "were you busy", never "what did it move"                                          | One count line in the appendix; outcomes on the page                                                          |

## Interview

Ask one question per message, multiple-choice when the options are knowable. Read any framework, prior report or budget document first and ask only about the gaps.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

1. Which report is this: (a) recurring monthly or quarterly update, (b) budget review or annual planning, (c) a cut already proposed, (d) a board slide, (e) a one-off "what does DevRel do" request, (f) an ask for more budget or headcount?
2. Who reads it first, and what decision do they make with it: renew, grow, cut, move the team, nothing?
3. What are that reader's goals this year, in their own words: company OKRs, a board metric, a product launch?
4. Does an agreed metric framework exist, with its attribution rule? Paste it, or the current numbers with their baselines.
5. What did the last report to this reader promise or show, and did any number get promised that you now have to live with?
6. What missed or went wrong this period?
7. What does the program cost, are salaries inside that figure, and which budget line funds it (marketing, sales, product, engineering)? Is a specific cut on the table (a share, a headcount)?
8. When is it due, in which format (memo, deck, slide, email), and how long is the meeting or read?
9. What is your effort ceiling before the deadline: hours available, and which other teams (finance, sales ops, support, product) will answer a request in time?

**Fast path.** A recurring update with a prior report on file reuses that report's reader, spine and goals: ask only questions 6 and 8, then deliver the whole draft.

Questions 7, 8 and 9 re-rank the defense moves below. Ask them here, not beside the ranking. Write every relative deadline ("in 10 days") as an absolute date.

## Workflow

1. Route, then interview until the reader, their goals, the framework and the deadline are clear.
2. Write the headline first: one sentence on what the program moved for the reader's goal, plus the decision asked. If you cannot write it, the report has no point yet; say which input is missing.
3. Offer two or three narrative spines (below), recommend one, wait for a choice.
4. Build the results table: one row per spine unit (a reader goal, a funnel stage or a bet), framework metrics only, each with value, baseline or threshold, status and claim label.
5. Pair every lagging outcome with its leading indicator and pull-through (below).
6. Write the misses section and the changes they trigger.
7. Add cost per outcome, with salaries stated as in or out.
8. If the budget is under review, build the defense case (below).
9. Cut to one page plus an appendix (a defense case may take two), tailored to the reader (below). Present section by section and get agreement on each before the next. When the user wants the whole draft at once, deliver it with every assumption listed at the top, then validate section by section.
10. Run the pass threshold. If your harness has persistent memory, record the reader, their goals, the spine and what this report promised in the context file above, so the next report is compared against it.

## Brainstorm the narrative spine

Say you are in brainstorming mode. Offer the spines with what each makes visible and what it hides, then recommend one. The spine sets what one row of the results table stands for; the table itself is always there.

- **Goal ledger.** One row per company goal the reader owns, what DevRel moved toward it. Default for a CEO, CMO or board. Hides work that serves no stated goal, which is often the point.
- **Developer funnel.** Where developers enter, stall and succeed, and which stage DevRel moved. Best for a CTO or product leader. Hides the money line.
- **Bet portfolio.** Each bet placed, its cost, its result, and keep, scale or stop. Best for a CFO or a budget review. Hides slow compounding work behind its current result.

Do not rank the spines by efficiency: a spine the reader cannot follow is worthless whatever it cost, so the order collapses to "the one this reader already uses". Never mix two spines in one results table.

## Leading indicators carry the slow outcomes

Business outcomes trail the work that moves them, by two different lags:

- Opportunity creation trails a DevRel touch.
- Closed revenue trails the opportunity by the whole sales cycle.

Set both lags from the company's own sales-cycle data, never from a rule of thumb. Adoption is slow before any of that: swyx reports, as his own habit, trying a technology a year or more after first hearing of it ("Measuring Developer Relations", 2021). A report that waits for the lagging number reports nothing for a year; a report that promises it next quarter creates a debt.

Pair each lagging outcome with a leading indicator already in the framework. The lags below are one program's values, not defaults:

| Lagging outcome                    | Leading indicator             | Expected lag | Pull-through so far                                | Label                       |
| ---------------------------------- | ----------------------------- | ------------ | -------------------------------------------------- | --------------------------- |
| influenced pipeline                | DevRel qualified leads routed | 1-2 quarters | 6 of Q1's 40 leads became opportunities by Q3      | influenced                  |
| 90-day retention of touched cohort | first-success rate            | 1 quarter    | rose with first success in 2 of the last 3 cohorts | influenced (touched cohort) |

- Show pull-through: what share of earlier leading movements converted. With no history, write "link unproven, first read <date>".
- Never present the leading indicator as the outcome, and never move a lagging number into a target it was not set for.
- When the framework has no leading indicator for a lagging outcome, report the outcome as "pending, next read <date>" and hand the gap to `samber/developer-relations-skills@devrel-metrics`. Do not invent one.

## Tailor to the reader

Same numbers, different first lines. Cut anything the reader will not act on.

| Reader                                     | Reads first                                          | Unit trusted                         | Leave out                                            |
| ------------------------------------------ | ---------------------------------------------------- | ------------------------------------ | ---------------------------------------------------- |
| CEO                                        | headline and the one ask                             | company goals in their words         | channel detail                                       |
| CFO                                        | cost per outcome, spend against plan                 | money, finance-agreed unit values    | reach metrics, modeled value not agreed with finance |
| CMO or marketing lead                      | influenced pipeline, activation                      | CRM stages under the written rule    | anything calling shared pipeline sourced             |
| CTO or product lead                        | enablement and product feedback shipped              | product analytics, tickets           | pipeline detail                                      |
| Board                                      | three numbers, four-quarter trend, one sentence each | trend against own history            | everything else, and customer names under NDA        |
| COO, CRO, or a VP running another function | the row of the function they run, plus the ask       | that function's own system of record | metrics their function does not own                  |

Cadence follows the framework: a monthly half-page for operations, a quarterly report for decisions, the defense case at each budget cycle.

## Budget defense

Build it when question 1 is (b) or (c). Start from the cut list in `samber/developer-relations-skills@devrel-budget-allocation`; without one, route there before answering a cut.

Moves, in efficiency order (value for the hours spent):

| Move                                                                                                             | Effort                                            | What it buys                                                     |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- | ---------------------------------------------------------------- |
| Results table in the funder's words                                                                              | hours, from numbers already collected             | answers "what did it move"                                       |
| Tiered cut scenarios: what each tier stops, which metric drops, whether it reverses, when savings land           | hours, given the cut list                         | turns yes-or-no into how much                                    |
| Cost per outcome against the funder's alternative (paid acquisition, support headcount, sales engineering hours) | a day, plus finance agreeing the unit values      | a number finance can check                                       |
| Dependency inventory: what breaks if the program stops, confirmed in writing by the owning team                  | a week of coordination and some political capital | other leaders vouching, the most persuasive evidence in a review |
| New causal evidence: a pre/post read or holdout on a bounded push                                                | a quarter                                         | the strongest evidence, the only causal claim available          |

- efficiency: results table > tiered scenarios > cost per outcome > dependency inventory > causal evidence
- value (persuasion in a review): dependency inventory > causal evidence > cost per outcome > tiered scenarios > results table
- effort: causal evidence > dependency inventory > cost per outcome > tiered scenarios > results table

**Default rung.** Always ship the results table and the tiered scenarios. Add cost per outcome when the reader is a CFO. Add the dependency inventory when the proposed cut is a third or more, or headcount.

The order starves causal evidence: highest evidence, slowest by far. Promote it when the review is a quarter or more away; record the pre-period before the push or the option is gone.

This order is a default. Re-rank against the interview and say which answer moved which move:

- A deadline inside two weeks deletes causal evidence, and keeps the dependency inventory only for teams that can confirm before the deadline (question 9).
- Unit values not agreed with finance delete every modeled figure; report cost per measured outcome instead.
- No known alternative for the funder to buy: compare cost per outcome with the program's own prior periods.
- A program funded from a sales line promotes cost per outcome and the influenced row; one funded from product promotes the dependency inventory.

Build the tiers from the cut list, never from round percentages:

- Each tier is a cumulative prefix of the ranked cut list. Show the tier nearest the requested cut and one smaller, with the gap between the tier's share and the request.
- When the whole list covers less than the requested cut, say so and name what lies beyond it (usually salaries) as the decision the funder is really making.
- Bundle lines that share a dependency (a platform and the role running it) into one tier step. When the ranking puts them far apart, send the list back to `samber/developer-relations-skills@devrel-budget-allocation` to re-rank rather than cutting one and silently breaking the other.
- A mandated, non-negotiable cut skips the counter-offer: show the smallest prefix that meets it, which results-table rows it protects, and stop.
- Add per tier: reversible or not (contracts, re-hiring and re-ramp time) and when the savings land in the plan year.

Never argue that DevRel cannot be measured, and never offer a tier the cut list does not support. Confirmed consequences carry the `estimate` label: they are the other team's forecast. A dependency the owning team has not confirmed appears only as "confirmation requested from <team>, due <date>", with no consequence claimed. If the funder raises outside budget benchmarks, answer with the program's own trend and the benchmark's sample caveat. Worked defense case: [./references/budget-defense-case.md](./references/budget-defense-case.md).

### Growth ask

When question 1 is (f), argue the increment, never the whole program:

- The outcome the last comparable increment bought, from its pull-through, labelled.
- What the added cost should buy, as a range, with the read date.
- The stop rule: what result at the read date returns the money.

## Misses

Every report carries a "What did not work" section. A clean page reads as a filtered page.

- One row per metric that missed its threshold: what happened, the likely cause, what changes, the next read date.
- Nothing missed: write "No metric missed its threshold this period". Never leave the section out, never fill it with a placeholder.
- Name every metric dropped since the last report and the kill-rule reason.
- Put bad news before good news when the reader would otherwise learn it elsewhere.

## Output

One page plus an appendix, in this order: headline with the decision asked, results table, leading indicators, what did not work, cost per outcome, next period (two or three commitments, each with a read date), decision asked with options and date. Appendix: definitions, the attribution rule as written in the framework, blind spots, one activity count line. Load the template, a worked quarterly report and a weak-versus-strong comparison before drafting: [./references/one-page-template.md](./references/one-page-template.md).

## Pass threshold

Iterate until every line passes, and report the check:

- The headline states an outcome for the reader's goal and a decision asked, in at most two sentences.
- Every number carries a claim label; no figure sums across labels; no "sourced", "generated" or ROI multiple on influenced or modeled values.
- No causal verb without a holdout or a pre/post read with a recorded pre-period; cost per outcome compares the same unit on the same cost basis.
- Every metric comes from the agreed framework, or the header says "provisional".
- Every lagging outcome has a leading indicator with pull-through or "link unproven".
- "What did not work" has a row for every missed threshold and every dropped metric, or states that nothing missed.
- Cost is stated with salaries in or out.
- The decision asked names options, a recommendation and a date.
- The report fits one page (two for a defense case); activity counts sit in the appendix only.
- In a growth ask: the last increment's outcome, the expected range with a read date, and the stop rule.
- In a mandated cut: the smallest cut-list prefix that meets it and the results-table rows it protects.
- In a defense case: a results table, tiers built as cut-list prefixes with reversibility and savings timing, and no dependency claim without the owning team's confirmation.

## Common failure modes

- **Dashboard dump.** Thirty metrics hand the reader the analysis. One page, framework metrics only.
- **Changing the metrics each quarter.** The reader cannot compare two reports, so neither is believed. Change metrics only through the framework.
- **Promising the lagging number next quarter.** It arrives late and the debt is called. Report the leading indicator and its pull-through.
- **Report with no ask.** A report that requests nothing gets read and forgotten. Ask for one decision.
- **Defense written after the cut is announced.** Build tiered scenarios at every budget cycle, before anyone proposes a number.

## Invocation examples

- "My CFO wants a one-pager on what our three-person DevRel team returns before Q1 planning."
- "Marketing wants to cut DevRel 40%. Help me make the case."
- "Turn this metrics sheet into a board slide."

## References

- samber/developer-relations-skills@devrel-strategy - the funded driver the headline must speak to.
- samber/developer-relations-skills@devrel-team-structure - the reporting line that decides who reads the report first.
