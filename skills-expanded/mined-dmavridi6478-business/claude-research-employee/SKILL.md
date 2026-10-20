---
name: claude-research-employee
description: An 8-step, source-grounded method for having Claude produce a trustworthy competitor/product comparison report instead of a confident-sounding but unverified one — give it one narrow question, name the exact competitors, define the comparison fields up front, set hard research rules (official sources only, cite every price/feature, mark missing data as "not found", never fill a gap with a guess), build the comparison table, investigate open hypotheses separately from proven facts, human-check the evidence before approving, and save the workflow as a reusable brief. Use when the user needs a competitor comparison, pricing/feature research, or any "compare N options" report and the accuracy of prices/features/sources actually matters.
---

# Build a Claude Research Employee (8 steps)

Original content compiled from a "Build Your First Claude AI Research
Employee" social carousel. The worked example (comparing three Notion
productivity templates) generalizes to any "compare N named things" research
task.

## Step 1 — Give it one job

Start with a specific question, not an open-ended "research the market."

Worked example: compare 3 Notion productivity templates. Summarize their
offers, prices, and included features.

## Step 2 — Choose your competitors/subjects by name

Name the exact things to compare and give the official link for each —
don't make Claude guess which product you mean:

- Thomas Frank — Ultimate Brain — thomasjfrank.com/brain
- Easlo — Second Brain — easlo.co/templates/second-brain
- Gridfiti — Life OS — shop.gridfiti.com

Provide official product links; if a page is inaccessible, paste its content
directly rather than letting Claude guess at it.

## Step 3 — Define what to compare

Pick the same fields for every subject so the comparison is apples-to-apples:

1. Who it's for
2. What it does
3. Listed price
4. What's included

Add a source link and check-date to every entry — a price without a
retrieval date is already stale advice.

## Step 4 — Set the research rules

State these explicitly before Claude starts pulling data — this is the step
that actually determines whether the report is trustworthy:

- Use official sources.
- Cite every price and feature.
- Mark missing details as "Not found."
- Separate facts from hypotheses.

**Never fill a gap with a guess.** A confidently-invented number is worse
than a visible blank, because a blank gets checked and a confident guess
doesn't.

## Step 5 — Build the comparison

Have Claude assemble the table from steps 2–4 into one output — this is the
"Competitor Report" deliverable itself, not a separate step to prompt for
again.

## Step 6 — Find what to investigate

Separate proven facts from open questions the report surfaces but can't
answer from public sources alone — label these as hypotheses to validate,
not conclusions:

- Would beginners prefer a smaller kit?
- Would a role-specific version be useful?
- What setup help do buyers need?

These are ideas to validate with real users, not proven market gaps —
don't let a research report quietly launder a guess into a stated fact.

## Step 7 — Check the evidence

Before treating the report as final, a human reviews it against a short
checklist:

- Open every source.
- Confirm prices and included features.
- Check for missing or outdated details.
- Keep facts and hypotheses separate.

**A human approves the final report** — this step is not optional and not
delegable back to Claude; it's the check on everything steps 1–6 produced.

## Step 8 — Save the workflow

Keep three reusable pieces so the next comparison doesn't start from zero:

- Research instructions (steps 3–4, as a template)
- Comparison format (the table shape from step 3)
- Source checklist (step 7)

Next time: update the competitor links and rerun the brief. It stays a
repeatable workflow with human review included, not a one-off report.

## Reusing this pattern

The discipline that transfers to any comparison task (tools, vendors, hiring
candidates on paper, pricing plans) is steps 3–4 and 7: fixed fields per
subject, explicit sourcing rules stated before research starts, and a human
evidence-check before anyone acts on the output. Skipping the rules in step 4
is how an AI-generated comparison quietly turns an unverified number into a
cited "fact."

Distinct from `build-claude-ai-employee` (same account, different job): that
skill is a general method for turning any repeatable task into a reusable
prompt; this one is specifically about a *sourced, verifiable* comparison
report, where steps 4 and 7 (research rules, human evidence-check) are the
whole point.
