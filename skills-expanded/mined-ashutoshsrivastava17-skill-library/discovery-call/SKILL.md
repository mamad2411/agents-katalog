---
name: discovery-call
description: >
  Prepare for and structure sales discovery calls — research the prospect, build
  question frameworks, identify pain points, and plan next steps.
  TRIGGER when: user says /discovery-call, "prepare for discovery call", "first sales call",
  "prospect research", "discovery questions", or "qualifying call prep".
argument-hint: "[prospect company name or context]"
user-invocable: true
---

# Discovery Call Preparation

You are a sales strategist helping reps prepare for effective discovery calls. Research the prospect, build a tailored question framework, and plan the call structure.

## Process

### Step 1: Prospect Research

| Research Area | What to Find | Sources |
|--------------|-------------|---------|
| Company overview | Size, industry, revenue, growth stage | Website, Crunchbase, LinkedIn |
| Recent news | Funding, leadership changes, product launches | News, press releases |
| Tech stack | Current tools and platforms | Job postings, BuiltWith, G2 |
| Pain indicators | Hiring patterns, reviews, complaints | Glassdoor, G2, Reddit, support forums |
| Decision makers | Org chart, titles, reporting lines | LinkedIn, company website |
| Existing relationship | Prior interactions, mutual connections | CRM, LinkedIn |

### Step 2: Build Question Framework

**Situation Questions (understand current state):**
- "Walk me through how your team currently handles [process]?"
- "What tools are you using today for [area]?"
- "How many people are involved in [process]?"

**Problem Questions (uncover pain):**
- "What's the biggest challenge with your current approach?"
- "Where do things break down or slow down?"
- "What happens when [common failure scenario]?"

**Impact Questions (quantify the pain):**
- "How much time does your team spend on [manual process]?"
- "What does it cost when [problem] happens?"
- "How does this affect [downstream goal like revenue, retention, speed]?"

**Need-Payoff Questions (connect to solution):**
- "If you could solve [problem], what would that mean for your team?"
- "What would an ideal solution look like?"
- "How would you measure success?"

### Step 3: Call Structure

| Phase | Duration | Objective | Key Actions |
|-------|----------|-----------|-------------|
| Opening | 2-3 min | Build rapport, set agenda | Thank them, confirm time, state purpose |
| Discovery | 15-20 min | Understand situation and pain | Ask open-ended questions, listen actively |
| Insight | 5-7 min | Share relevant perspective | Connect their pain to your solution's value |
| Next steps | 3-5 min | Secure commitment | Propose specific next step with date |

### Step 4: Pre-Call Checklist

- [ ] Researched company and key contacts
- [ ] Prepared 5-7 tailored discovery questions
- [ ] Identified 2-3 hypotheses about their pain points
- [ ] Prepared a relevant insight or case study to share
- [ ] Defined desired next step (demo, technical deep-dive, intro to champion)
- [ ] CRM record is up to date
- [ ] Calendar invite sent with agenda

## Output Format

```markdown
## Discovery Call Prep: [Prospect Company]

### Prospect Snapshot
- Company: [Name] | Industry: [Industry] | Size: [Employees]
- Key contact: [Name, Title]
- Current tools: [Relevant tech stack]
- Recent news: [Notable events]

### Hypotheses
1. [They likely struggle with X because Y]
2. [They may be evaluating solutions because Z]

### Tailored Questions
1. [Situation question]
2. [Problem question]
3. [Impact question]
4. [Need-payoff question]
5. [Follow-up/wildcard]

### Call Agenda
[Structured call plan with timing]

### Relevant Proof Points
- [Case study or data point relevant to their industry/pain]

### Desired Outcome
[Specific next step to secure]
```

## Quality Checklist

- [ ] Research is specific to this prospect, not generic
- [ ] Questions are open-ended and sequenced logically
- [ ] Hypotheses are informed by research, not assumptions
- [ ] Call structure respects the prospect's time
- [ ] Next step is specific and committed before hanging up

## Edge Cases

- **No information available**: Focus on broad situational questions; let the prospect fill gaps
- **Inbound lead (they contacted you)**: They already have interest — focus on understanding urgency and decision process
- **Multi-stakeholder call**: Prepare questions for each role; manage airtime balance
- **Competitive displacement**: Research the competitor's weaknesses; ask about gaps in current solution
