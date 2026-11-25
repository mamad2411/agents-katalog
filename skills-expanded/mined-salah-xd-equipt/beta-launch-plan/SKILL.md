---
name: beta-launch-plan
description: "Plans beta launches with user recruitment, feedback collection, bug reporting, and iteration cycles. Use when preparing to launch a product or feature in beta."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Beta Launch Plan

## When to Use This Skill

Use this skill when you need to:
- Plan a structured beta launch for a new product or major feature
- Design user recruitment and selection criteria for beta testers
- Build feedback collection and bug reporting systems
- Define success criteria for graduating from beta to general availability

**DO NOT** use this skill for full product launches, alpha/internal testing plans, or QA test plans. This is for external beta launch planning only.

---

## Core Principle

A BETA IS NOT A SOFT LAUNCH — IT IS A STRUCTURED LEARNING PERIOD WITH DEFINED GOALS, SELECTED USERS, AND CLEAR EXIT CRITERIA.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Product/feature** | "What are you launching in beta?" | No default — must be provided |
| **Beta goals** | "What do you need to learn from this beta? Validate demand, find bugs, test UX?" | Validate core workflow and identify critical bugs |
| **Target beta size** | "How many beta users do you want?" | 20-50 users |
| **Beta duration** | "How long should the beta run?" | 4 weeks |
| **Ideal beta user** | "Describe your ideal beta tester — role, tech comfort, use case." | Early adopter, tolerant of bugs, willing to give feedback |
| **Known risks** | "What are you most worried about?" | Core functionality breaking under real usage |

**GATE: Confirm the brief before building the plan.**

---

## Phase 2: Plan

### Beta Timeline

```
## Beta Timeline

**Week -2 to -1: Pre-Launch**
- Finalize beta criteria and success metrics
- Build feedback collection system
- Recruit and select beta users
- Prepare welcome materials

**Week 1: Controlled Launch**
- Onboard first cohort (50% of total)
- Daily monitoring for critical issues
- First feedback check-in (Day 3)

**Week 2: Expand**
- Onboard remaining beta users
- First iteration based on Week 1 feedback
- Structured feedback survey

**Week 3-4: Iterate and Evaluate**
- Ship fixes and improvements
- Final feedback survey
- Evaluate against success criteria
- Decision: ship, extend, or pivot
```

### Success Criteria

Define measurable exit criteria:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Critical bugs | 0 unresolved | Bug tracker |
| Task completion rate | 80%+ | User testing |
| NPS score | 30+ | Survey |
| Active usage | 60%+ of beta users engaged weekly | Analytics |
| Feedback sentiment | Mostly positive | Qualitative review |

**GATE: Confirm timeline and success criteria before designing recruitment and feedback systems.**

---

## Phase 3: Execute

### Beta User Recruitment

**Application form fields:**
- Name and email
- Role and company size
- Current workflow for the problem the product solves
- Why they want to join the beta
- Availability for feedback (survey, call, async)

**Selection criteria:**
- Represents the target customer profile
- Has the problem the product solves
- Willing to commit to feedback schedule
- Mix of tech-savvy and average users

**Recruitment channels:**
- Email list announcement
- Social media post
- Existing customer base
- Community or forum post

### Feedback Collection System

**Structured feedback:**
- Weekly survey (5 questions max, takes under 3 minutes)
- End-of-beta survey (10 questions, comprehensive)
- Optional: 15-minute feedback call with 5-10 users

**Unstructured feedback:**
- In-app feedback widget (screenshot + text)
- Dedicated Slack channel or email thread
- Bug report form (steps to reproduce, expected vs. actual behavior)

**Bug Report Template:**
```
**What happened:**
**What you expected:**
**Steps to reproduce:**
1.
2.
3.
**Screenshot (if applicable):**
**Device/browser:**
```

### Communication Plan

- **Welcome email:** What to expect, how to report issues, feedback schedule
- **Weekly update:** What was fixed, what is being worked on, what to test next
- **Thank you email:** End of beta appreciation, what comes next, early access or discount offer

---

## Phase 4: Polish

### 1. Beta-to-Launch Decision Framework

```
## Go/No-Go Criteria

**Ship to GA if:**
- [ ] All critical bugs resolved
- [ ] Task completion rate exceeds 80%
- [ ] NPS is 30 or above
- [ ] No data loss or security issues
- [ ] Onboarding flow works without hand-holding

**Extend beta if:**
- [ ] 1-2 critical issues remain but are solvable in 1-2 weeks
- [ ] Usage is strong but feedback reveals UX confusion
- [ ] Need more data to validate a key assumption

**Pivot or kill if:**
- [ ] Core value proposition is not validated
- [ ] Beta users are not using the product despite reminders
- [ ] Critical technical limitation cannot be resolved
```

### 2. Beta User Appreciation

- Early access to the full product
- Founding user pricing or lifetime discount
- Public acknowledgment (with permission) in launch materials
- Priority access to future betas

### 3. Quality Checklist

```
## Beta Launch Checklist

- [ ] Success criteria defined with measurable targets
- [ ] Beta user application form is live
- [ ] Selection criteria documented
- [ ] Feedback collection system is set up (survey, widget, bug form)
- [ ] Welcome email drafted and scheduled
- [ ] Weekly update template created
- [ ] Bug report template provided to all beta users
- [ ] Go/no-go decision framework agreed on
- [ ] Beta appreciation plan defined
- [ ] Timeline has clear start, checkpoints, and end date
```

---

## Example

**Product:** AI-powered meeting note-taker for solopreneurs
**Beta size:** 30 users, 4 weeks

**Welcome email excerpt:**
"You are one of 30 people testing MeetingMind before anyone else. Over the next 4 weeks, use it in your real meetings. Things will break — that is the point. Report bugs with the red button in the bottom-right corner. Every Friday, you will get a 3-question survey. Your feedback directly shapes what we ship."

**Weekly survey:**
1. How many meetings did you use MeetingMind for this week? (number)
2. Did anything break or feel confusing? (text)
3. On a scale of 1-10, how useful was MeetingMind this week? (scale)

---

## Anti-Patterns

- **Too many beta users** — 200 beta users for a solo founder means 200 sources of feedback you cannot process. Start with 20-50.
- **No success criteria** — without exit criteria, beta runs indefinitely. Define what "done" looks like upfront.
- **Ignoring feedback** — collecting feedback without acting on it destroys beta user trust. Close the loop every week.
- **No communication cadence** — beta users who hear nothing assume the product is dead. Weekly updates are mandatory.
- **Treating beta as free marketing** — beta is for learning, not growth. Optimize for feedback quality, not user count.

---

## Recovery

- **Low beta signups:** Lower the barrier. Remove the application form and invite directly from your email list or social followers.
- **Beta users not providing feedback:** Shorten surveys to 2 questions. Offer a small incentive (gift card, extended trial).
- **Too many bugs to manage:** Triage ruthlessly. Fix critical (data loss, crashes) first. Acknowledge non-critical issues and timeline them.
- **Beta needs to extend:** Communicate transparently. Tell users why, what changed, and the new timeline.
