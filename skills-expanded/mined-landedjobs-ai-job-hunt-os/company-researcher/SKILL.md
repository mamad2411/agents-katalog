---
name: company-researcher
description: Use when the user names a company they are applying or interviewing with, asks whether a startup is safe to join, wants to know if a company's AI claims are real, or needs talking points and questions before a call.
---

# Company Researcher

Produce the brief a well-connected friend would give: what the company actually does, whether it is financially and operationally credible, whether its AI is real, and what to say in the room. Candidates should diligence a startup like a junior investor because they are investing years of their career. High-profile startup failures repeatedly show that famous investor logos are weak evidence; operating artifacts are stronger evidence.

## What you need

Company name (plus URL if obscure), the target role, and the stage: about to apply, screen scheduled, or onsite scheduled. Depth scales with stage. If you have web access, research live. If not, say so and ask the user to paste the about page, JD, and recent news, then work from that.

## Process

### Step 1: The business in plain words
What they sell, to whom, and what the buyer pays for. If you cannot state it in two sentences, that is a finding, and "how do you make money" becomes a great interview question.

### Step 2: Survival math (borrow the VC lens)
- **Runway estimate**: last raise (amount, date) minus elapsed burn. Rough burn proxy: headcount × fully loaded cost, plus compute for AI companies. State it as an estimate with the inputs shown.
- **Capital efficiency**: if revenue is real, the diagnostic question is "how much net burn per dollar of net new ARR?" Do not apply a universal stage benchmark without a current, comparable source. The user can ask a softened version: "How has the plan changed since the last raise?"
- A company 18+ months past its last raise with no revenue story hires differently than one fresh off a round. Say which pattern this is.
- If cash, burn, or revenue are unknown, write "unknown," recommend the user ask, and never invent runway. Diligence reduces risk; it does not eliminate private-company opacity.

### Step 3: The four-artifact AI-washing test
Classify AI-native vs AI-forward vs AI-washed using artifacts, not branding (regulators now fine companies for fake AI claims; candidates should apply the same skepticism):
1. **Engineering blog**: do they publish real technical decisions?
2. **Eval methodology**: do they describe how they measure model quality?
3. **Model/data ownership**: is it honestly stated (own models, fine-tunes, or API layer)? API-layer is fine; hiding it is not.
4. **Production customer outcome**: named customers with concrete results?

Also run the **hiring-mix check**: a "frontier infra" company hiring mostly sales with a thin engineering core does not match its claim. Many eval/agent/infra roles = the work is real.

### Step 4: The team and the moment
Recent 6 months: launches, big customers, layoffs, leadership changes. Who leads the org this role sits in; their public writing. Open-roles pattern: a cluster of similar openings means a funded push; a lone re-posted role can mean churn. Check a layoffs tracker before believing a hiring spree.

### Step 5: Sources and their weights
Levels.fyi for compensation and level comparables. Blind and Glassdoor for repeated themes only; anonymous sentiment is not fact, and one review is an anecdote. LinkedIn headcount graph for growth and the engineering-vs-GTM mix. Engineering blog, GitHub org, changelog, and status page for the AI-washing test. Label every claim in the brief: measured, reported, or anecdote.

## Output format

1. **Two-line summary** (business + stage)
2. **Survival math**: runway estimate with inputs, momentum, risks, all dated
3. **AI classification** with the four artifacts checked
4. **The team you would join**: known facts vs what to verify in the room
5. **Talking points**: 3 specific references (a launch, a blog post, a design decision) that show real research; specific beats flattering
6. **Questions to ask them**: 3-5, at least one that surfaces something the user genuinely needs (runway, roadmap ownership, why the role is open). Phrase red flags as questions: "How has the plan changed since the last raise?" extracts more than an accusation.
7. **Red flags, if any**: stated plainly, sourced, dated

## Hard rules

- Date every claim; "raised $40M" means nothing without "in March 2026."
- Separate verified facts from inference from anecdote, explicitly, every time.
- If research surfaces something serious (quarterly layoffs, founder controversy, Builder.ai-pattern claims), lead with it. The user is choosing where to spend years.
