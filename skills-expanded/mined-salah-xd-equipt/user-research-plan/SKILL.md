---
name: user-research-plan
description: "Plans user research studies with recruitment, interview scripts, survey design, and insight synthesis frameworks. Use when gathering customer insights to inform decisions."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# User Research Plan

## When to Use This Skill

Use this skill when you need to:
- Plan a user research study with interviews, surveys, or usability tests
- Write interview scripts and survey questions for customer discovery
- Design a recruitment plan for finding the right research participants
- Create a framework for synthesizing research insights into decisions

**DO NOT** use this skill for market research (competitive analysis), analytics setup, or A/B test design. This is for qualitative and quantitative user research planning.

---

## Core Principle

USER RESEARCH IS NOT ABOUT CONFIRMING WHAT YOU ALREADY BELIEVE — IT IS ABOUT DISCOVERING WHAT YOU DO NOT KNOW. ASK OPEN QUESTIONS, LISTEN MORE THAN YOU TALK, AND LET THE DATA CHANGE YOUR MIND.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Research question** | "What decision will this research inform? What do you need to learn?" | No default — must be provided |
| **Method** | "Interviews, surveys, usability tests, or a combination?" | 5-8 user interviews |
| **Target participants** | "Who should we talk to? Role, behavior, demographics." | Current customers |
| **Timeline** | "When do you need results?" | 2-3 weeks |
| **Budget** | "Is there budget for participant incentives?" | $0 — rely on goodwill and relationships |
| **Decisions at stake** | "What will you do differently based on what you learn?" | No default — must be provided |

**GATE: Confirm the brief and research question before designing the study.**

---

## Phase 2: Study Design

### Research Method Selection

| Method | Best For | Sample Size | Time |
|--------|----------|-------------|------|
| **User interviews** | Understanding motivations, pain points, workflows | 5-8 | 2-3 weeks |
| **Surveys** | Quantifying opinions, preferences, demographics | 50-200+ | 1-2 weeks |
| **Usability tests** | Testing specific flows, finding UX friction | 5-7 | 1-2 weeks |
| **Card sorting** | Information architecture, navigation | 10-15 | 1 week |
| **Diary studies** | Understanding behavior over time | 5-10 | 2-4 weeks |

### Recruitment Plan

- **Who to recruit:** Define 3-5 screening criteria
- **Where to find them:** Customer list, social media, communities, user panels
- **How to ask:** Write a recruitment message (see Phase 3)
- **Incentives:** Gift cards, product credits, early access, or goodwill
- **Scheduling:** Provide a booking link with multiple time slots

### Study Timeline

```
Week 1: Recruit participants, finalize scripts/surveys
Week 2: Conduct sessions (aim for 2-3 per day max)
Week 3: Synthesize findings, present insights
```

**GATE: Confirm study design and recruitment plan before writing scripts.**

---

## Phase 3: Write Research Materials

### Interview Script Template

```
## Interview Script: [Research Topic]
**Duration:** 30-45 minutes
**Recording:** Ask permission before recording

### Intro (3 min)
- Thank them for their time
- Explain the purpose (learning, not selling)
- Confirm recording consent
- "There are no right or wrong answers"

### Warm-Up (5 min)
- Tell me about your role and what a typical day looks like
- How long have you been doing [relevant activity]?

### Core Questions (20-30 min)
1. Walk me through how you currently [task related to research question]
2. What is the hardest part about [task]?
3. Can you tell me about the last time [specific scenario]?
4. What have you tried to solve this problem?
5. If you could wave a magic wand, what would change?

### Product-Specific (if applicable, 5-10 min)
6. How did you first hear about [product]?
7. Show me how you use [feature] — talk me through it
8. What would you change about [product] if you could?

### Wrap-Up (2 min)
- Is there anything I should have asked but didn't?
- Would you be open to a follow-up if we have questions?
- Thank them and confirm incentive delivery
```

### Survey Design Rules

- Keep surveys under 10 questions (5-7 is ideal)
- Start with easy questions, save sensitive ones for later
- Mix question types: multiple choice, scale (1-5), and 1-2 open-ended
- Avoid leading questions ("How much do you love our product?")
- Test the survey with 2-3 people before sending

### Recruitment Message

```
Subject: Quick 30-min chat — your feedback shapes [Product]

Hi [Name],

I am working on [brief description of what you are improving] and would love to hear about your experience with [topic].

It is a casual 30-minute conversation — no sales pitch, just listening. [Incentive if applicable.]

Would any of these times work? [Booking link]

Thanks,
[Your name]
```

---

## Phase 4: Synthesize and Report

### Insight Synthesis Framework

After all sessions, organize findings:

1. **Themes:** Group similar responses into 3-5 themes
2. **Quotes:** Pull 2-3 verbatim quotes per theme
3. **Frequency:** Note how many participants mentioned each theme
4. **Surprises:** What did you learn that you did not expect?
5. **Recommendations:** 3-5 specific actions based on findings

### Research Report Template

```
## Research Summary: [Topic]

**Research question:** [What we set out to learn]
**Method:** [Interviews/surveys/etc.] with [N] participants
**Dates:** [Start] to [End]

### Key Findings

**Finding 1: [Theme]**
- [Summary of finding]
- [Supporting quote]
- [How many participants mentioned this]

**Finding 2: [Theme]**
...

### Surprises
- [Unexpected insight]

### Recommendations
1. [Specific action] — because [finding that supports it]
2. [Specific action] — because [finding that supports it]
3. [Specific action] — because [finding that supports it]

### Appendix
- Participant demographics
- Full question list
- Raw data (if applicable)
```

### Quality Checklist

```
## Research Plan Checklist

- [ ] Research question is specific and decision-oriented
- [ ] Method matches the question type (qualitative vs. quantitative)
- [ ] Recruitment criteria defined with 3-5 screening questions
- [ ] Interview script has open-ended questions (not yes/no)
- [ ] Survey is under 10 questions with no leading language
- [ ] Incentive plan is defined (even if $0)
- [ ] Recording consent process is documented
- [ ] Synthesis framework includes themes, quotes, and recommendations
- [ ] Research report template is ready before sessions begin
- [ ] Timeline accounts for recruitment, sessions, and synthesis
```

---

## Example

**Research question:** "Why do users create a project but never add tasks? What blocks them?"

**Interview question excerpt:**
"Walk me through the last time you created a new project in the app. What happened after you set it up? ... What stopped you from adding tasks right away?"

**Finding excerpt:**
"4 of 6 participants said they created the project 'to try it out' but got confused about whether to add tasks manually or import from another tool. They left to figure it out later and never came back."

---

## Anti-Patterns

- **Leading questions** — "Don't you think our dashboard is confusing?" guarantees biased responses. Ask "How do you find information in the dashboard?"
- **Too many participants** — 5-8 interviews surface 80% of insights. Do not delay decisions waiting for 50 interviews.
- **No research question** — "Let's just talk to users" produces interesting conversations and no actionable insights. Define the question first.
- **Ignoring surprises** — the most valuable insights are the ones you did not expect. Do not filter them out because they conflict with your plan.
- **Research without action** — if findings sit in a document and change nothing, the research was wasted. Tie every finding to a decision.

---

## Recovery

- **Cannot recruit enough participants:** Lower the target to 3-5. Three good interviews beat zero perfect ones. Also try recruiting from social media or communities.
- **Participants are not the right fit:** Stop mid-study and tighten screening criteria. Better to pause than collect unusable data.
- **Conflicting findings:** This is normal. Note the conflict, look for patterns in participant demographics, and design a follow-up study to resolve the ambiguity.
- **Stakeholder disagrees with findings:** Present raw quotes and let the data speak. Offer to run a follow-up with different participants if there is genuine concern about sample bias.
