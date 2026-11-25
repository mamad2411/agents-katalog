---
name: technical-communication
description: Use this skill when explaining technical concepts to non-technical stakeholders, writing for mixed audiences, presenting technical decisions to leadership, translating business requirements into technical specs, or communicating complexity clearly. Trigger on keywords: explain to stakeholders, non-technical, executive summary, business language, translate tech, present to leadership, communicate to PM.
---

# Technical Communication

## The Core Problem
Technical people communicate for accuracy. Non-technical people communicate for decisions. These are different goals requiring different approaches.

**Rule:** Lead with impact, follow with mechanism. Never the reverse.

---

## Audience-First Framework

Before writing or speaking, answer:
1. Who is the audience? (developer, PM, executive, client)
2. What decision do they need to make?
3. What do they already know?
4. What do they care about? (reliability, cost, speed, risk)

Then adapt every word to those answers.

---

## Explaining Technical Concepts

### The Analogy Method
Find a familiar concept that shares the same structure:
```
Cache → A sticky note on your desk vs going to the filing cabinet
API → A restaurant menu — you order, the kitchen delivers, you don't see the kitchen
Microservices → A food court vs a single restaurant kitchen
```

### The Why-Before-What Pattern
```
WRONG: "We need to implement Redis caching."
RIGHT: "Our API is responding slowly under load. 
        Caching the most frequent DB queries in Redis 
        would cut response time by ~70% at minimal cost."
```

Always lead with the problem and impact, then the solution.

---

## Writing for Different Audiences

### For Executives
- One paragraph max per topic
- Lead with business impact (cost, risk, user experience)
- No acronyms without expansion
- Include a clear recommendation

### For Product Managers
- Connect every technical decision to user or product impact
- Flag trade-offs that affect timeline or scope
- Be clear about what you need from them (decision, info, approval)

### For Other Developers
- Be precise and specific
- Include relevant context (why, not just what)
- Reference code, docs, or tickets directly

---

## The BLUF Format (Bottom Line Up Front)

For all written technical communication:
```
[One sentence: what you want them to know or do]

[2-3 sentences: context and reasoning]

[Optional: details, alternatives, risks for those who want depth]
```

Busy people read the first line and stop. Make that line count.

---

## Technical Decision Communication

When presenting a technical decision to non-developers:
```
SITUATION: [current state and why it's a problem]
RECOMMENDATION: [what you propose]
IMPACT: [what this achieves in business terms]
TRADE-OFFS: [what we give up or risk]
COST/EFFORT: [time, money, resources needed]
DECISION NEEDED: [what you need from them]
```
