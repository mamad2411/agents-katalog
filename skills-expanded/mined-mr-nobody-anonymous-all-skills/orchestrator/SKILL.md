---
name: orchestrator
version: 1.0.0
description: "When you're unsure which marketing skill to use, or when the user asks for general marketing help without a specific task. Also use when the user says 'help me with marketing,' 'what should I do next,' 'I'm stuck,' 'which skill should I use,' or 'marketing help.' This skill routes to the right specialized skill based on goals."
source: "https://github.com/robertbstillwell/marketing-skills"
source_repository: "robertbstillwell/marketing-skills"
source_path: "orchestrator/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Marketing Orchestrator

You help users figure out which marketing skill to use for their specific situation. You are a router, not an executor — your job is to understand the goal and point to the right skill.

## How to Use This Skill

1. **Understand the user's goal** — What outcome are they trying to achieve?
2. **Identify the workflow stage** — Research, Strategy, Content, SEO, or CRO?
3. **Route to the right skill** — Recommend the specific skill and why

---

## Quick Routing Guide

### "I need to understand my market/customer"
→ **Research Stage**
- `icp-builder` — Building ideal customer profiles
- `keyword-research` — Finding what people search for
- `marketing-psychology` — Understanding buyer behavior

### "I need to plan/decide what to do"
→ **Strategy Stage**
- `content-strategy` — What content to create
- `pricing-strategy` — How to price and package
- `launch-strategy` — How to launch a product/feature
- `marketing-ideas` — Tactical ideas and inspiration

### "I need to create something"
→ **Content Creation Stage**
- `copywriting` — Marketing copy for any page
- `write-landing` — High-converting landing pages
- `email-sequence` — Drip campaigns and sequences
- `lead-magnet` — Opt-in offers (guides, checklists)
- `social-content` — Social media posts
- `content-repurposing` — Turn 1 piece into many formats

### "I need help with SEO/traffic"
→ **Distribution Stage**
- `seo-audit` — Diagnose SEO issues
- `keyword-research` — Find keyword opportunities
- `programmatic-seo` — Build pages at scale
- `competitor-alternatives` — Comparison pages
- `paid-ads` — PPC campaigns

### "My page/flow isn't converting"
→ **CRO Stage**
- `page-cro` — Marketing page conversion
- `signup-flow-cro` — Registration flows
- `onboarding-cro` — Post-signup activation
- `form-cro` — Lead/contact forms
- `popup-cro` — Popups and modals
- `ab-test-setup` — Designing experiments

### "I need to improve existing work"
→ **Refinement**
- `copy-editing` — Improve existing copy
- `seo-audit` — Fix SEO issues
- `page-cro` — Improve conversions

---

## Decision Tree

```
What's your situation?
│
├─ "I don't know where to start"
│   └─ Do you have a product marketing context doc?
│       ├─ No → `product-marketing-context`
│       └─ Yes → `icp-builder` then `content-strategy`
│
├─ "I need to write something"
│   └─ What kind?
│       ├─ Landing page → `write-landing`
│       ├─ Any marketing page → `copywriting`
│       ├─ Email sequence → `email-sequence`
│       ├─ Social posts → `social-content`
│       └─ Lead magnet → `lead-magnet`
│
├─ "Something isn't working"
│   └─ What's not working?
│       ├─ Page not converting → `page-cro`
│       ├─ Signups dropping off → `signup-flow-cro`
│       ├─ Users not activating → `onboarding-cro`
│       ├─ Not ranking in search → `seo-audit`
│       └─ Copy feels weak → `copy-editing`
│
├─ "I need ideas"
│   └─ What kind?
│       ├─ Marketing tactics → `marketing-ideas`
│       ├─ Content topics → `content-strategy`
│       ├─ Keywords → `keyword-research`
│       └─ Psychology/persuasion → `marketing-psychology`
│
└─ "I need to plan something"
    └─ What are you planning?
        ├─ Content calendar → `content-strategy`
        ├─ Product launch → `launch-strategy`
        ├─ Pricing → `pricing-strategy`
        ├─ Referral program → `referral-program`
        └─ Free tool → `free-tool-strategy`
```

---

## Workflow Recommendations

### For a New Product/Feature:
1. `product-marketing-context` — Set foundation
2. `icp-builder` — Define target customer
3. `keyword-research` — Find search opportunities
4. `write-landing` — Create landing page
5. `launch-strategy` — Plan the launch

### For Improving Conversions:
1. `page-cro` — Audit the page
2. `copy-editing` — Improve the copy
3. `ab-test-setup` — Test changes
4. `analytics-tracking` — Measure results

### For Content Marketing:
1. `content-strategy` — Plan pillars and calendar
2. `keyword-research` — Find topics
3. `copywriting` — Write the content
4. `content-repurposing` — Atomize across formats
5. `seo-audit` — Optimize for search

### For Email Marketing:
1. `lead-magnet` — Create the opt-in offer
2. `email-sequence` — Write the sequence
3. `ab-test-setup` — Test subject lines

---

## When to Use Multiple Skills

Some tasks require multiple skills in sequence:

| Task | Skills to Chain |
|------|-----------------|
| Full landing page | `icp-builder` → `write-landing` → `page-cro` |
| Content piece | `keyword-research` → `copywriting` → `seo-audit` |
| Launch campaign | `launch-strategy` → `email-sequence` → `social-content` |
| Conversion fix | `page-cro` → `copy-editing` → `ab-test-setup` |

---

## Reference

For full skill descriptions and when to use each, see:
`/Users/hobson/.openclaw/workspace/SKILLS_INDEX.md`

---

*This orchestrator helps you find the right skill. Once identified, load that skill and follow its specific workflow.*
