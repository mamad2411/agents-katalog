---
name: lean-canvas
description: Brainstorm a Lean Canvas of the hub cell by cell, find the riskiest assumptions it rests on, and write each as a claim at assumption with a Test Card (hypothesis, test, metric, threshold, deadline) that a value check can compare a signal with.
---

# Brainstorming a Lean Canvas

A Lean Canvas is a set of guesses about a business. The work is to find the guesses the business depends on most and
knows least about, and to say for each how it would be shown true or false.

## 1. Read what is there

- `canvas__read` with the canvas: every claim, its status, its test card and its evidence. Do not propose a claim the
  canvas holds already, in other words.
- `canvas__signals`: the keys the project measures. A test card whose metric is one of them is checked by the hub
  without anyone's work.
- `srs__search` and `srs__read`, when the project keeps SRS documents: the use cases say what the product does, and
  for whom.

## 2. List the assumptions, cell by cell

| Cell | Ask |
|---|---|
| problem | Which problem do the customers have, how often, and what do they do about it today? |
| customer_segments | Who has the problem, and who are the first customers to reach (the early adopters)? |
| unique_value_proposition | Why would they choose this over what they do now, in one sentence? |
| solution | Which feature answers each problem? |
| channels | How do customers find it and get it? |
| revenue_streams | Who pays, how much, and how often? |
| cost_structure | What does it cost to build, run and sell? |
| key_metrics | Which numbers show the business is working? |
| unfair_advantage | What can others not copy or buy easily? |

Write each assumption as one claim the evidence could prove wrong: "Corner shops reorder stock at least weekly", not
"Shops like convenience".

## 3. Rank them

Rank by impact (how much of the business falls if it is false) and by risk (how little evidence there is). Propose
the riskiest first, at most ten in one brainstorm. Set the confidence: `low` for a guess, `medium` for a guess with
some support, `high` only with evidence a member gave you.

## 4. Write a Test Card for each

| Field | What to write |
|---|---|
| `hypothesis` | We believe that ... (the claim, as something that can be false) |
| `test` | To verify that, we will ... (an interview round, an experiment, a measure the product already takes) |
| `metric` | the signal key that measures it, as `canvas__signals` lists it; `feedback` when judged pieces of feedback count; leave it out when nothing measures it yet |
| `aggregate`, `window_days` | how the hub sums the signal: `mean` over 14 days, `count` over 30 |
| `comparator`, `threshold` | what the aggregate must reach: `>=` 0.3 |
| `min_samples` | how many values make the result count |
| `deadline` | the day by which the test should have an answer, YYYY-MM-DD |

A test card needs at least a hypothesis and a test. A claim moves to testing only with a hypothesis, a test and a
deadline.

## 5. Make or propose them

- In chat: one `canvas__edit` with every new claim (`cell`, `text`, `confidence`, `test_card`), and a reason that
  quotes what the member asked. They apply at once.
- In a task run: one `canvas__propose` with every new claim, a reason, and `synthetic` true when any rests on
  simulated users or personas.

Never set a status on a new claim: it starts as an assumption. Never propose or set validated.
