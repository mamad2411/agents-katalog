---
name: interview-question-bank
description: "Creates role-specific interview question banks with behavioral, situational, and technical categories for structured hiring interviews."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Interview Question Bank

## When to Use This Skill

Use this skill when you need to:
- Build a role-specific interview question bank organized by category
- Create behavioral, situational, and technical questions for a hiring interview
- Design questions that reveal real competency versus rehearsed answers
- Standardize interview questions across multiple interviewers or hiring rounds

**DO NOT** use this skill for hiring scorecards (use hiring-scorecard), job descriptions, or interview scheduling. This is for creating the questions themselves.

---

## Core Principle

THE BEST INTERVIEW QUESTIONS REVEAL HOW A CANDIDATE ACTUALLY BEHAVES, NOT HOW WELL THEY INTERVIEW — BEHAVIORAL QUESTIONS ABOUT PAST ACTIONS PREDICT FUTURE PERFORMANCE BETTER THAN HYPOTHETICALS.

---

## Phase 1: Role Requirements

Define what the questions need to assess.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Role title** | "What role are you hiring for?" | No default |
| **Key competencies** | "What are the top 3-5 skills or traits this role requires?" | No default |
| **Employment type** | "Full-time, part-time, or contractor?" | Contractor |
| **Interview stages** | "How many interview rounds? (screen, technical, final)" | 2 rounds |
| **Culture priorities** | "What working style or values matter most?" | Self-starter, communicative |
| **Deal-breakers** | "What would immediately disqualify a candidate?" | No default |

**GATE: Confirm competencies before building the question bank.**

---

## Phase 2: Build Question Bank

Create categorized questions mapped to competencies.

### Question Categories

**Behavioral Questions (STAR format):**
Ask about past behavior. Best predictor of future behavior.
Format: "Tell me about a time when..."

**Situational Questions:**
Present a hypothetical relevant to the role.
Format: "How would you handle..."

**Technical/Skill Questions:**
Test specific knowledge or ability.
Format: "Walk me through..." or practical assessment.

**Culture/Values Questions:**
Assess working style and alignment.
Format: "Describe your ideal..." or "What matters most to you about..."

### Question Bank Template

```
## Interview Question Bank: [Role Title]

---

### Competency 1: [Competency Name]

**Behavioral:**
1. "Tell me about a time you [relevant scenario]. What was the situation, what did you do, and what was the result?"
   - *Listen for:* [Specific evidence of competency]
   - *Red flag:* [Vague answers, blame-shifting, no measurable outcome]

2. "Describe a situation where [challenge related to competency]. How did you handle it?"
   - *Listen for:* [What good looks like]
   - *Red flag:* [What bad looks like]

**Situational:**
3. "Imagine you are [scenario relevant to role]. What would your approach be?"
   - *Listen for:* [Structured thinking, relevant tools/methods]
   - *Red flag:* [No framework, just buzzwords]

**Technical:**
4. "[Role-specific skill question or mini-task]"
   - *Listen for:* [Depth of knowledge, practical application]
   - *Red flag:* [Surface-level answers, cannot explain reasoning]

---

### Competency 2: [Competency Name]

**Behavioral:**
5. "Tell me about a time you [scenario]."
   - *Listen for:* [Evidence]
   - *Red flag:* [Warning sign]

...

---

### Culture Fit

**Values:**
9. "Describe your ideal working relationship with a manager or client."
   - *Listen for:* Alignment with your management style and communication norms

10. "What does accountability look like to you?"
    - *Listen for:* Ownership mindset, proactive communication about challenges

11. "When you disagree with a decision, what do you do?"
    - *Listen for:* Constructive pushback, willingness to commit after discussion

---

### Closing Questions

12. "What questions do you have for me about the role or the business?"
    - *Listen for:* Thoughtful questions that show research and genuine interest
    - *Red flag:* No questions, or only questions about pay and time off

13. "Is there anything we did not cover that you want me to know?"
    - *Listen for:* Self-awareness, relevant strengths they want to highlight
```

**GATE: Present the question bank for review.**

---

## Phase 3: Interview Guide

Organize questions into interview stages.

### Stage-by-Stage Question Assignment

```
## Interview Flow

### Stage 1: Screen (20-30 min)
**Goal:** Confirm basic fit, motivation, and availability
**Questions:**
- [Culture question 1]
- [Behavioral question for top competency]
- [Logistical questions: availability, rate, start date]
- [Closing question]

### Stage 2: Deep Dive (45-60 min)
**Goal:** Assess core competencies in depth
**Questions:**
- [Behavioral question for competency 1]
- [Behavioral question for competency 2]
- [Situational question]
- [Technical question or mini-task]
- [Culture question 2]
- [Closing question]

### Stage 3: Final (30 min) — if applicable
**Goal:** Validate decision, address remaining concerns
**Questions:**
- [Situational question for remaining competency]
- [Questions addressing any concerns from previous rounds]
- [Candidate's questions about the role]
```

### STAR Assessment Guide

Train interviewers to listen for all four STAR elements:

```
## STAR Response Evaluation

| Element | What to Listen For | If Missing |
|---------|-------------------|-----------|
| **Situation** | Specific context — when, where, what was happening | Ask: "Can you set the scene?" |
| **Task** | Their specific role or responsibility | Ask: "What was your role?" |
| **Action** | What THEY did (not the team) | Ask: "What specifically did YOU do?" |
| **Result** | Measurable outcome | Ask: "What was the result? Any numbers?" |
```

---

## Phase 4: Maintain

Keep the question bank relevant and effective.

### Post-Interview Calibration

After each hire, review:
- Which questions best predicted the candidate's actual performance?
- Which questions did not differentiate between candidates?
- Are any questions getting rehearsed answers? (Retire and replace them)

### Question Bank Updates

- Add new questions when new competencies become important
- Retire questions that every candidate answers the same way
- Refresh situational questions with current, relevant scenarios
- Review annually for legal compliance (avoid questions about protected characteristics)

### Legal Guardrails

Never ask about:
- Age, marital status, children, or family planning
- Religion, national origin, or immigration status
- Health conditions or disabilities
- Arrest record (conviction may be asked in some jurisdictions)
- Any protected characteristic not relevant to job performance

---

## Anti-Patterns

- **Leading questions** — "You are a self-starter, right?" telegraphs the answer. Ask "Tell me about a time you identified and solved a problem without being asked."
- **Hypothetical-only interviews** — "What would you do if..." reveals idealized behavior. "What did you do when..." reveals actual behavior.
- **Same questions for every role** — a developer and a marketer need different questions. Customize to the competencies.
- **Not listening for red flags** — candidates who say "we" for everything may be taking credit for team work. Probe for individual contribution.
- **Asking too many questions** — depth on 5-6 questions beats surface coverage of 15. Allow follow-up probing.

---

## Recovery

- **All candidates give similar answers:** The questions are too common. Add role-specific scenarios or mini-tasks that require demonstration, not just description.
- **Interviewer is not sure what "good" looks like:** Define the ideal answer for each question before the interview. Compare responses against that standard.
- **User is hiring for the first time:** Start with 3 behavioral questions + 2 culture questions + 1 closing question. That is enough for a strong 30-minute screen.
- **Candidate gives short answers:** Prompt with "Can you walk me through that in more detail?" or "What happened next?" Use silence — most people will fill it.
- **User needs to assess a skill that is hard to interview for:** Add a paid trial task or short project. Real work reveals more than any question.
