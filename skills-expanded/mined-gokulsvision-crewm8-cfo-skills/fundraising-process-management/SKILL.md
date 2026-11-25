---
name: fundraising-process-management
description: Plan and manage the end-to-end fundraising process — timeline, target list, outreach sequencing, pipeline tracking, round structure, and close coordination. Use when the user asks about planning a fundraise, building an investor target list, tracking a fundraising pipeline, or sequencing investor outreach.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, fundraising, investor-pipeline, round-structure]
related_skills:
  - fundraising-financials
  - cap-table-management
  - data-room-management
  - investor-relations
  - term-sheet-analysis
  - cash-forecasting
inputs_required:
  - company-stage-and-metrics-ARR-growth-team-size-cash-burn
  - target-round-amount-round-label-seed-A-B-ideal-valuation-range
  - runway-months-until-cash-runs-out-from-cash-forecasting
  - existing-investor-relationships-warm-contacts-board-members
deliverables:
  - fundraising-timeline-phase-by-phase-with-milestones
  - investor-target-list-tiered-and-scored
  - pipeline-tracker-and-outreach-sequence-plan
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Fundraising Process Management

Plan, execute, and track a fundraising round from inception to close. Build the target investor list, sequence outreach, manage the pipeline, coordinate diligence, and drive to term sheets. Goal: run a tight, fast process that generates competitive tension.

## Purpose

Fundraising is the highest-leverage activity a startup CEO can do — and the easiest to screw up. A badly timed, poorly sequenced, or unfocused raise can waste months and leave money on the table. This skill provides the playbook for running a disciplined process: the right timeline, the right targets, the right sequencing, and the right tracking so every investor meeting moves the process forward.

## When to Use

- "Plan our fundraise"
- "Build an investor target list"
- "Track our fundraise pipeline"
- "What's our fundraise timeline?"
- "Sequence our investor outreach"
- "When should we start fundraising?"

## Inputs Required

1. **Company stage & metrics** — ARR, growth rate, team size, cash on hand, monthly burn.
2. **Target round** — how much to raise, round label (Seed/A/B), ideal valuation range.
3. **Runway** — months until cash runs out at current burn (from `cash-forecasting`).
4. **Existing investor relationships** — warm contacts, board members who can make intros.

## Quick Reference

| Phase | Duration | Key Activity |
|---|---|---|
| 1. Preparation | Weeks 1-4 | Financial model, data room, pitch deck, target list |
| 2. Pre-outreach | Weeks 4-5 | Soft-sound friendly investors, refine pitch, secure warm intros |
| 3. Active outreach | Weeks 5-8 | Batch outreach (practice → top targets → fill pipeline) |
| 4. Diligence & term sheets | Weeks 8-11 | Partner meetings, data room, customer refs, term sheet negotiation |
| 5. Selection & negotiation | Weeks 11-12 | Compare terms, negotiate, select lead, syndicate |
| 6. Close | Weeks 12-14 | Legal docs, final diligence, sign, wire |
| **Total** | **~12-14 weeks** | First meeting to money in the bank |

## Procedure

### Fundraising Timeline

#### Phase 1: Preparation (Weeks 1-4)
  - Build/update financial model (`fundraising-financials`)
  - Assemble data room (`data-room-management`)
  - Refine pitch deck narrative
  - Build investor target list
  - Prep for Q&A

#### Phase 2: Pre-Outreach (Week 4-5)
  - Soft-sound 5-10 friendly investors (not top targets)
  - Gather feedback, refine pitch
  - Secure warm intros to top targets
  - Lock reference customers

#### Phase 3: Active Outreach (Weeks 5-8)
  - Launch to 15-25 investors in batches of 5-7
  - First batch: 5-7 high-quality but not top-3 (practice)
  - Second batch: 5-7 of your top targets (strongest pitch)
  - Third batch: 5-7 to fill pipeline gaps
  - Aim for 8-12 first meetings per batch
  - Track meeting → partner meeting → term sheet funnel

#### Phase 4: Diligence & Term Sheets (Weeks 8-11)
  - Partner meetings for progressing firms
  - Open data room access
  - Customer reference calls
  - Term sheet negotiation
  - Create competitive tension (ideally 2-3 term sheets)

#### Phase 5: Selection & Negotiation (Weeks 11-12)
  - Compare term sheets (`term-sheet-analysis`)
  - Negotiate final terms
  - Select lead investor
  - Syndicate remaining allocation

#### Phase 6: Close (Weeks 12-14)
  - Legal docs drafted and negotiated
  - Final due diligence
  - Board / shareholder approval
  - Sign and wire
  - Announce

### Critical Path

The two things that kill fundraise timelines:
1. **Financials not ready**: start the financial model 6 weeks before you plan to pitch.
2. **Cold outreach without intros**: warm intros have 5-10x the conversion rate. Spend 2 weeks lining them up.

### Investor Target List

#### Building the List

Score investors on:

| Attribute | Weight |
|---|---|
| Thesis fit (stage, sector, check size) | Must-have |
| Recent activity (deployed capital in last 6 months) | High |
| Portfolio conflicts | Auto-eliminate |
| Partner reputation / founder NPS | High |
| Warm intro availability | Medium |
| Value-add beyond capital (network, expertise) | Medium |
| Decision speed / reputation for ghosting | Medium |

#### List Structure

| Tier | Count | Description |
|---|---|---|
| A (Top targets) | 5-8 | Perfect fit, warm intro, top-tier firm |
| B (Strong targets) | 8-12 | Good fit, can get intro, solid firms |
| C (Fill the pipeline) | 5-8 | Decent fit, will take meeting, fallback |

#### Outreach Sequencing

Never blast all investors at once. Batch:

1. **Practice batch (3-5 investors)**: C-tier or friendly B-tier. Hone your pitch. Expect to iterate.
2. **Main batch (8-12)**: A and B-tier with warm intros. Your best pitch. Create a cluster of first meetings in 1-2 weeks.
3. **Mop-up batch (5-8)**: fill pipeline gaps if needed.

### Pipeline Tracking

Track every investor through the funnel:

| Investor | Firm | Tier | Intro Source | First Meeting | Partner Meeting | Diligence Started | Term Sheet? | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| Sarah | a16z | A | Board intro | Apr 10 ✓ | Apr 18 ✓ | Apr 22 | — | In diligence | Enthusiastic |
| Mark | XYZ | B | Cold email | Apr 12 ✓ | — | — | — | No response after meeting | — |

#### Funnel Math

Typical conversion rates:
- First meeting → Partner meeting: 30-40%
- Partner meeting → Term sheet: 20-30%
- Term sheet → Close: 70-80%

So to get 2-3 term sheets, you need:
- 8-12 partner meetings
- Which needs 20-30 first meetings
- Which needs 30-40 initial outreaches

### Round Structure Decisions

#### How much to raise?

- **18-24 months of runway** is the standard target.
- Calculate: (Monthly net burn × desired months) + buffer (20%).
- Too little = raising again in 12 months = bad look. Too much = excessive dilution.

#### Valuation expectations

- **Seed**: often uncapped or capped SAFE. If priced, $8-15M typical for strong teams.
- **Series A**: 10-25x forward ARR. $10-50M typical for SaaS.
- **Series B**: 8-15x forward ARR. $50-200M+.

#### Syndicate strategy

- **Lead**: the investor who prices the round, takes the board seat, does the work. Usually takes 60-80% of the round.
- **Followers**: fill the rest, fewer rights, no board seat.
- **Strategic angels**: small checks from relevant operators.

## Output Format

- Fundraising timeline (phase-by-phase with milestones)
- Investor target list (tiered, scored)
- Outreach sequence plan
- CRM-ready pipeline tracker
- Round structure recommendation (amount, valuation range, syndicate plan)
- Meeting prep checklist per investor

## Done Criteria

The skill is complete when:
1. Fundraising timeline is produced with all 6 phases, milestones, and deadlines
2. Investor target list is built with A/B/C tiers, scored on fit and warm-intro availability
3. Outreach sequence plan is defined (practice batch, main batch, mop-up batch)
4. Pipeline tracker is set up with funnel stages and conversion targets
5. Round structure is recommended (amount, valuation range, syndicate strategy)
6. Critical path items (financial model readiness, warm intros) are flagged

## Pitfalls

- **Starting fundraising with < 6 months of runway**: investors can smell desperation. It kills negotiating leverage. The best time to raise is when you don't need to.
- **Blasting all investors at once**: if 20 investors all get the same email on the same day, they all respond (or don't) simultaneously — leaving no room to iterate. Batch outreach creates a natural cadence.
- **Cold outreach without warm intros**: warm intros have 5-10x the conversion rate of cold emails. Spend 2 weeks lining them up before the main batch goes out.
- **Letting the process drag**: a fundraise that goes past 12 weeks loses momentum. Investors assume others passed. Set a target close date and hold the team to it.
- **Not creating competitive tension**: if only one investor is in diligence, they can lowball. Always try to get 2-3 term sheets in parallel.

## Verification

Can you answer "when does each phase of the fundraise start and end?" from the timeline? Is the investor target list tiered with warm-intro sources identified? Does the pipeline tracker show conversion at each stage? Are critical path items (financial model, warm intros) on a deadline? If not, the fundraise plan is incomplete.

## Example

**User prompt**: "Plan our fundraise."
**What should happen**: Assess current runway and metrics to determine the optimal timing, build the 6-phase timeline with milestones and deadlines, create the investor target list scored by fit and warm-intro availability, design the batch outreach sequence, set up the pipeline tracker, and recommend round structure (amount, valuation range, syndicate strategy).

**User prompt**: "Build an investor target list."
**What should happen**: Research investors with thesis fit for the company's stage and sector, score each on the defined attributes (fit, activity, warm intro availability, reputation), eliminate portfolio conflicts, tier into A/B/C groups, and produce the list with warm-intro sources and recommended outreach order.

## Linked Skills

- Financial model & metrics → `fundraising-financials`
- Cap table & dilution → `cap-table-management`
- Data room setup → `data-room-management`
- Term sheet comparison → `term-sheet-analysis`
- Investor comms → `investor-relations`
- Cash & runway → `cash-forecasting`
