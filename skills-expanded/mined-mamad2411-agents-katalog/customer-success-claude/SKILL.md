---
name: customer-success-claude
description: Claude prompt library for Customer Success Managers — QBRs, churn analysis, onboarding, escalations, renewal emails, health scoring, and success plans. Use when the user is a CSM or works in customer success, asks to draft customer-facing content, or runs /cs-qbr, /cs-churn, /cs-onboarding, /cs-escalation, /cs-renewal, /cs-health, /cs-upsell. Source: Stan Mykhalchuk / Jason AI by Reply.
---

# Customer Success × Claude — Prompt Library

Claude is strongest for CSM work in: legal/policy/research documents, long-form writing and reviews, careful structured analysis, large context window, and well-structured responses.

Use this skill with the **Act as [Role] → Create [Task Type] → Show as [Format]** framework.

---

## Prompting Framework

**Structure every prompt in 3 parts:**

```
1. Act as a [ROLE]:
   Customer Success Manager | Onboarding Specialist | Renewal Strategist
   Churn Analyst | Customer Advocate | Account Health Coach

2. Create [TASK TYPE]:
   Write a renewal email | Summarize a call transcript
   Build an onboarding checklist | Draft a QBR agenda
   Create an escalation brief | Score account health
   Map the customer journey | Plan a success review

3. Show as [FORMAT]:
   Step-by-step action plan | Summary + Next Steps
   Bullet points | Risk table | Email draft
   Timeline view | Scorecard | Story Format
   Decision Framework | Slide-ready outline
```

---

## Prompt Starter Library

### QBR (Quarterly Business Review)
```
Act as a Customer Success Manager. Write a QBR deck outline for [account name] covering: 
- Q[X] goals vs. actuals
- Product adoption metrics (highlight wins + gaps)
- ROI achieved this quarter
- Top 3 risks to address
- Mutual success plan for next quarter
Show as: Slide-ready outline with speaker notes for each section.
```

### Churn Risk Analysis
```
Act as a Churn Analyst. I have an account health report for [account name]: [paste data/signals].
Identify the top 3 churn signals, rate each risk (High/Medium/Low), explain the customer journey that led here, and create a 30-day save plan with specific actions, owners, and success metrics.
Show as: Risk table + action plan with timeline.
```

### Onboarding Plan
```
Act as an Onboarding Specialist. Create a 90-day onboarding plan for [customer name] who is a [company type] using [product] for [use case].
Include: Day 1 kickoff agenda, Week 1–2 setup milestones, Week 3–4 first value moment, Month 2 adoption deepening, Month 3 success review criteria.
Show as: Timeline view with owner column and success metrics per milestone.
```

### Escalation Brief
```
Act as a Customer Success Manager. Write an escalation brief for [account name] to share with [executive/VP/support team].
Include: Account background (1 paragraph), timeline of issues, current impact on the customer, what we've tried, what we need from this escalation, and recommended resolution path.
Show as: Executive summary format, under 1 page.
```

### Renewal Email
```
Act as a Renewal Strategist. Write a renewal email for [account name] whose contract expires on [date].
Context: [key wins this year, any open issues, expansion opportunity Y/N].
Tone: [warm/direct/executive].
Include: Value recap, renewal terms summary, a clear call to action, and handle the most likely objection: [objection].
Show as: Email draft, 200 words max.
```

### Account Health Scorecard
```
Act as an Account Health Coach. Score [account name] on these dimensions (1–10 with rationale):
- Product adoption (DAU/WAU, feature usage vs. plan)
- Business outcomes achieved vs. promised
- Relationship strength (exec access, champion stability)
- Support health (ticket volume, severity trends)
- Expansion signals (growth, new use cases, budget signals)
- Risk factors (contract renewal date, competitive pressure, internal champion change)
Show as: Scorecard table with color coding (Green/Yellow/Red) + top 3 actions.
```

### Upsell Talking Points
```
Act as a Customer Advocate. Generate 10 upsell talking points for [product/feature] tailored to [customer name]'s industry and use case.
Each talking point should: connect to a business outcome they care about, reference something specific about their current usage, and feel like advice — not a pitch.
Show as: Numbered list with a 1-sentence setup + 1-sentence proof + suggested follow-up question.
```

### Call Transcript Summary
```
Act as a Customer Success Manager. Summarize this call transcript in 3 bullet points:
[paste transcript]
Include: Key decisions made, open action items with owner + deadline, and any risk signals mentioned.
Show as: Summary + Next Steps table.
```

### Customer Journey Map
```
Act as a Customer Advocate. Map the customer journey for [persona] using [product] for [use case].
For each stage (Awareness, Onboarding, Activation, Adoption, Expansion, Advocacy):
- What is the customer trying to accomplish?
- What friction or confusion do they encounter?
- What does success look like at this stage?
- What should CS do proactively here?
Show as: Table with 6 rows (one per stage) and 4 columns.
```

---

## Prompting Techniques Reference

| Technique | When to use |
|---|---|
| **Role Playing** | Simulate a customer objection or difficult conversation |
| **Add Examples** | "Here are 3 examples of tone I want: [ex1] [ex2] [ex3]" |
| **Chained** | Multi-step: first analyze, then draft, then refine |
| **Tree of Thought** | Explore multiple response paths before committing |
| **Temperature** | Ask Claude to vary the tone: formal → casual → executive |
| **Writing Style** | "Match the writing style of [example text]" |
| **Linked** | Reference earlier output: "Based on the health score above…" |
| **Step-by-Step** | "Walk me through this decision one step at a time" |

---

## Claude Capabilities for CSM Work

**Strengths:**
- Legal, policy, and research documents
- Long-form writing and reviews
- Careful, structured analysis
- Very large context window (paste entire contracts, transcripts, email threads)
- Clear, well-structured responses

**Limitations:**
- Limited real-time / live web access
- Fewer automation and agent features than some tools

**Power stack:**
- Claude + Perplexity = Real-time research
- Claude + Gamma = Presentations
- Claude + Canva = Visual design
- Claude + Intercom = Inbox automation
- Claude + n8n = Workflow automation
- Claude + Notion = Organize + manage
