---
name: ai-portfolio
description: The portfolio of AI initiatives — what is being built in each repo, what overlaps, what nobody uses and what it all costs. Use it when preparing an inspector round, before approving something new, or when answering whether something already exists in the house.
---

# AI portfolio

Held by whoever has the works-inspector seat. The domain is in
`roles/ai-manager.md`.

## The question that justifies the seat

It is not "what is being built?". It is **"does this already exist in the
house?"**. In an organisation with more than a hundred repos, the normal failure
is not missing capability: it is capability built twice, with neither of the two
people knowing.

Which is why this role asks more than it answers, and why its round is worth most
**before** somebody starts something.

## What to look at, and in what order

1. **What is in flight.** A repo with recent AI commits and no associated goal
   usually means a goal is missing, not that somebody is drifting.
2. **The overlaps.** Two repos solving the same thing under different names. The
   typical signal is the same dependency or the same model showing up in places
   that do not know about each other.
3. **What nobody uses.** Built, working, no traffic. It is the most uncomfortable
   question to ask and the one that frees the most budget.
4. **Aggregate cost.** Per initiative, not per provider. A total says nothing;
   "this is 400 a month and comes from a job running hourly" does.

## How to find out without bothering everyone

What you can see on your own: model dependencies in the repos, scheduled jobs, API
keys in use, traffic. That is **deduced** and gets tagged as such.

What only the person knows: whether something is paused on purpose, whether the
thing that looks abandoned is waiting on somebody else's decision, whether the
high cost is temporary because of a migration. That is **asked**, and it is what
turns an inventory into a portfolio.

## When proposing reuse

With a name and a path: "what you are about to build is in `X`, `Y` owns it, and
it solves 80% of it". An "I think something similar exists" produces half an hour
of searching and no decision.

And do not propose reuse without checking the fit: half the real overlaps are two
things that look alike in the name and not in the problem.
