---
name: prd-writing
description: When the agent needs to write a PRD, product spec, feature specification, or requirements document — crisp specs that align a team in one read and define success before work starts.
department: Product
source: helm
---

# PRD Writing

You write PRDs the way the best PMs at Figma and Linear do: short enough to actually be read, precise enough that engineering doesn't guess, and honest about what's out of scope and what could go wrong.

## Operating principles

1. **A PRD is an alignment tool, not a novel.** 1–2 pages for most features; 4 max for a big surface. If it takes 20 minutes to read, it will be skimmed and the details will be re-litigated in Slack anyway.
2. **Problem before solution — with receipts.** The problem section cites evidence (support tickets, interview quotes, funnel data). A PRD whose problem section could be deleted without anyone noticing is a solution looking for a justification.
3. **Success is a number decided BEFORE building.** Primary metric + target + measurement window ("activation rate for new workspaces +5 pts within 60 days of GA"), plus guardrail metrics that must NOT regress (latency, churn, support volume).
4. **Non-goals are load-bearing.** The explicit "we are NOT doing X in this version" list prevents 80% of scope creep. Every stakeholder request that was cut goes here with one line of why.

## The template

1. **TL;DR** (3 sentences): problem, solution, success metric.
2. **Problem & evidence**: who hurts, how much, how we know. Segment sized.
3. **Goals & success metrics**: primary metric + target; guardrails; how measured (event names if analytics exist).
4. **Non-goals**: the cut list.
5. **Solution overview**: the user experience narrated as a flow ("Sara opens…, sees…, clicks…"); wireframe/mock references; states covered — empty, loading, error, permission-denied, edge (long names, 0 items, 10k items).
6. **Requirements**: numbered, testable statements ("R3: an invited member without a seat sees the upgrade prompt within the invite modal"). Each requirement is verifiable by QA without interpretation. Priority-tagged (P0 ship-blocker / P1 fast-follow).
7. **Open questions & risks**: what's undecided, who decides, by when; top 2 risks with mitigations.
8. **Rollout**: flag strategy, migration/backfill needs, comms (docs, changelog, sales enablement), kill criteria.

## Workflow

1. Interview the inputs: discovery evidence, design explorations, engineering constraints — BEFORE writing.
2. Draft the TL;DR and success metric first; if you can't, the thinking isn't done — go back to discovery.
3. Write the flow narrative with design; enumerate states (the error/empty states are where specs usually lie by omission).
4. Turn the narrative into numbered testable requirements; tag priorities with engineering in the room (P0 negotiation IS the estimation meeting).
5. Circulate for 48 h of async comments; resolve every thread into the doc (decisions, not comment graveyards); freeze scope for the build.

## Output contract

Deliver the full PRD per the template, plus: the requirement-numbering carried into tickets · a one-paragraph engineering-kickoff summary · the changelog/docs draft stub.

## Quality bar

- Every requirement testable; every metric has a number and a window; every open question has an owner and a date.
- An engineer who missed every meeting can build the right thing from this doc.
- Shorter than you wanted: if a section adds no decisions, delete it.
