---
name: side-project-planning
description: Use this skill when planning a side project, evaluating a product idea, scoping an MVP, thinking through monetization, or deciding what to build. Trigger on keywords: side project, MVP, product idea, monetize, build vs buy, startup idea, indie hacker, what should I build, validate idea.
---

# Side Project Planning

## The MVP Mindset

**Build the smallest thing that proves the core assumption.**

Most side projects fail not because of bad execution but because of unvalidated assumptions. The goal of an MVP is to test the riskiest assumption with the least effort.

---

## Idea Validation Framework

Before writing a line of code:

```
1. PROBLEM: Is this a real problem people have?
   - Talk to 5 potential users — do they describe this problem unprompted?

2. SOLUTION FIT: Does your solution actually solve it?
   - Can you describe it in one sentence they immediately understand?

3. WILLINGNESS TO PAY: Will people pay for it?
   - "Would you pay $X/month for this?" is very different from "Would you use this?"

4. DIFFERENTIATION: Why this, not the existing alternatives?
   - What's 10x better than what exists?

5. REACHABILITY: Can you reach the target users?
   - Do you know where they are? Reddit, Slack, conferences, Twitter?
```

---

## MVP Scoping Rules

For each feature, ask:
- Is this required for the core value proposition? If no → cut it
- Can this be manual/fake before automating? If yes → fake it first
- Does the user notice if this isn't perfect? If no → ship it rough

### The Concierge MVP
Before building the full system, manually do what the software would do:
- Validate demand before automating
- Understand the real workflow before encoding it
- Much faster to iterate on a manual process

---

## Monetization Models for Developer Tools/AI

| Model | Best When | Risk |
|---|---|---|
| Freemium | High volume, viral potential | Need large base for conversion |
| Subscription | Recurring value, ongoing use | Churn management |
| Usage-based | Variable usage patterns | Revenue unpredictability |
| One-time | Simple tools, no ongoing cost | No recurring revenue |
| B2B SaaS | Enterprise buyers, high value | Long sales cycles |

---

## Build vs Buy Decision

Build when:
- This is your core differentiator
- No existing solution fits well enough
- Building it teaches you something critical

Buy/use existing when:
- It's infrastructure (auth, payments, email)
- The time savings are significant
- Your users don't care who built it

---

## Project Health Checklist

Before investing more time in a side project:
- [ ] At least 3 real users (not friends being polite) use it regularly
- [ ] At least 1 person has paid or expressed clear willingness to pay
- [ ] You can explain the value in one sentence
- [ ] You still want to work on it after the initial excitement fades
- [ ] You have a realistic path to your first 100 users

---

## The Personality-Consistent AI Memory Layer (Example Application)

For your specific AI side project idea:
- **Core assumption to test:** Users want AI that remembers their preferences, style, and context consistently across conversations
- **Riskiest assumption:** Users will pay for this over using free ChatGPT memory
- **MVP:** A simple wrapper that stores and injects user context — no fancy UI needed to test the core value
- **Validation step:** 10 users using it for 30 days. Do they return? Do they pay $5/mo?
