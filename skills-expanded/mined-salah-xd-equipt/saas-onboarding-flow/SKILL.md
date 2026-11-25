---
name: saas-onboarding-flow
description: "Designs SaaS user onboarding flows with activation milestones, tooltip sequences, and success metrics. Use when building or improving new user onboarding experiences."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# SaaS Onboarding Flow

## When to Use This Skill

Use this skill when you need to:
- Design a new user onboarding flow for a SaaS product
- Improve activation rates by restructuring the first-time user experience
- Define activation milestones and measure onboarding success
- Create tooltip sequences, welcome emails, and progress indicators

**DO NOT** use this skill for customer support documentation, feature tutorials for existing users, or sales demo scripts. This is for new user activation flows only.

---

## Core Principle

ONBOARDING ENDS WHEN THE USER EXPERIENCES THE PRODUCT'S CORE VALUE — EVERY STEP BEFORE THAT MOMENT MUST REDUCE FRICTION AND ACCELERATE TIME-TO-VALUE.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Product description** | "What does your SaaS product do in one sentence?" | No default — must be provided |
| **Core value moment** | "What is the 'aha moment' — the action where users first feel the value?" | No default — must be provided |
| **Current signup-to-activation rate** | "What percentage of signups reach your core value moment?" | Unknown — establish baseline |
| **Onboarding type** | "Product-led (self-serve), sales-assisted, or hybrid?" | Product-led |
| **User persona** | "Who is your primary user? Role, tech savviness, urgency level." | Small business owner, moderate tech skills |
| **Current pain points** | "Where do users currently drop off or get stuck?" | Unknown — design from scratch |

**GATE: Confirm the brief before mapping the flow.**

---

## Phase 2: Map the Flow

### Activation Milestone Framework

Define 3-5 milestones between signup and core value moment:

```
## Activation Milestones

1. **Signup Complete** — Account created, email verified
2. **Profile Setup** — Essential settings configured (name, company, preferences)
3. **First Action** — User performs the primary product action once
4. **Core Value** — User experiences the "aha moment" for the first time
5. **Habit Loop** — User returns and repeats the core action within 7 days
```

### Flow Map

For each milestone, define:
- **Trigger:** What initiates this step
- **Action:** What the user needs to do
- **UI Element:** Tooltip, modal, checklist, or email
- **Fallback:** What happens if the user does not complete this step within 24/48/72 hours

Present the flow map as a structured document.

**GATE: Confirm milestones and flow before writing detailed copy.**

---

## Phase 3: Write

Draft all onboarding copy and sequences:

### In-App Elements

- **Welcome modal:** 1 sentence of welcome, 1 sentence of what to do first, 1 CTA button
- **Progress checklist:** 3-5 items visible in a sidebar or dashboard widget
- **Tooltips:** Max 2 sentences each. Point to the specific UI element. Include a "Got it" dismissal.
- **Empty states:** For every blank screen the user sees, write helpful placeholder copy with a CTA

### Email Sequence

Design a 5-email onboarding sequence:

| Email | Timing | Subject Focus | CTA |
|-------|--------|---------------|-----|
| Welcome | Immediately | Confirm signup, set expectations | Complete profile |
| Quick Win | Day 1 | Guide to first action | Do [core action] |
| Value Story | Day 3 | Customer success story | Return to product |
| Progress Check | Day 5 | Acknowledge progress or re-engage | Complete next milestone |
| Activation Push | Day 7 | Final nudge toward core value moment | [Specific action] |

### Copy Rules

- **Action-oriented:** Every piece of copy tells the user exactly what to do next
- **Benefit-first:** Explain WHY before HOW
- **Short:** Tooltips under 20 words, modals under 50, emails under 150
- **No jargon:** Use the user's language, not internal product terms

---

## Phase 4: Polish

### 1. Metrics Dashboard

Define the metrics to track onboarding success:

```
## Onboarding Metrics

- **Signup-to-Activation Rate:** % of signups who reach core value moment
- **Time-to-Value:** Median time from signup to first core value moment
- **Milestone Completion Rates:** % completing each milestone
- **Drop-off Points:** Where users abandon the flow
- **Day 7 Retention:** % of users returning within first week
- **Email Engagement:** Open and click rates for each onboarding email
```

### 2. A/B Test Suggestions

Provide 3 testable hypotheses:
- Test removing one onboarding step to see if activation improves
- Test reordering milestones (quick win first vs. profile first)
- Test tooltip vs. checklist format for in-app guidance

### 3. Quality Checklist

```
## Onboarding Flow Checklist

- [ ] Core value moment is clearly defined and measurable
- [ ] 3-5 milestones bridge signup to activation
- [ ] Every step has a clear CTA (user always knows what to do next)
- [ ] Fallback emails exist for users who stall at each milestone
- [ ] Empty states have helpful copy, not blank screens
- [ ] Tooltips are under 20 words each
- [ ] Welcome email sends immediately (not hours later)
- [ ] Progress indicator is visible throughout onboarding
- [ ] No step requires more than 2 minutes to complete
- [ ] Day 7 retention metric is defined and trackable
```

---

## Example

**Product:** Project management tool for freelancers
**Core value moment:** User creates their first project and adds a task

**Welcome modal:**
"Welcome to TaskFlow. Let's set up your first project in under 2 minutes — you will see exactly how TaskFlow keeps your freelance work organized. [Create My First Project]"

**Tooltip (on project creation page):**
"Name your project after your client or gig. You can rename it anytime. [Got it]"

---

## Anti-Patterns

- **Too many steps before value** — if activation requires 8 steps, users will not finish. Cut to 3-5.
- **Asking for information you do not need yet** — defer profile fields that are not essential to the first value moment.
- **No fallback for stalled users** — if someone does not complete step 2, they need a nudge. Design the rescue path.
- **Tooltip overload** — more than 3 tooltips in sequence feels like a tutorial, not guidance. Space them out.
- **Generic welcome email** — "Welcome to [Product]!" with no next step wastes your best engagement window.

---

## Recovery

- **No activation data exists:** Start with qualitative — interview 5 recent signups about their first experience. Use their language in the flow.
- **Core value moment is unclear:** Look for the action most correlated with retention. If unsure, pick the action paying customers do most.
- **Product is complex:** Break onboarding into "quick start" (3 steps to first value) and "advanced setup" (optional deeper configuration).
- **User drops off at signup:** Simplify to email-only signup. Defer everything else to post-login.
