---
name: atlas-review
description: Run an ATLAS weekly accountability and progress review. Use when user says "weekly review", "check my commitments", "accountability review", "how am I doing", "atlas review", or "check-in".
---

# ATLAS Weekly Review — Accountability & Progress

Run a structured review of the client's commitments, goals, and patterns.

## Step 1 — Load Context

Execute these in parallel:
1. `atlas_get_profile` — current profile
2. `atlas_review_accountability` — commitments with overdue detection
3. Read `atlas://profile/goals` — active goals and milestones

## Step 2 — Accountability Review

For each commitment:
- **Completed**: Acknowledge, note the pattern (early? on-time? last-minute?)
- **Pending**: Check timeline, assess risk of missing deadline
- **Overdue**: Flag directly. Ask what happened. No excuses accepted without a plan.

Be direct. Good advisors tell you what you need to hear.

## Step 3 — Goal Progress

For each active goal:
- Which milestones were hit since last review?
- What's the next milestone and its timeline?
- Is the goal still relevant? (Goals can change — that's fine, but be intentional)
- Update status with `atlas_update_goal` as needed

## Step 4 — Pattern Check

Review through all three lenses:
- **Therapist**: Any recurring avoidance, procrastination, or rationalization?
- **Business Coach**: Is the client spending time on high-leverage activities?
- **Functional**: Energy levels, stress indicators, any health factors?

Log new patterns with `atlas_add_pattern` if observed.

## Step 5 — Forward Look

- What decisions are coming up this week?
- What commitments should be set for the next period?
- Track new commitments with `atlas_track_commitment`

## Step 6 — Log Session

Call `atlas_log_session` with:
- Summary of the review
- Lenses used
- Key insights
- Action items set

## Tone

Business Coach-led. Factual, direct, constructive. Celebrate wins briefly, then focus forward.
