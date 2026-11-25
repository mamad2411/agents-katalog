---
name: student-feedback-form
description: "Creates course evaluation forms with rating scales, open-ended questions, and improvement-focused categories for gathering actionable student feedback."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Student Feedback Form

## When to Use This Skill

Use this skill when you need to:
- Create a course evaluation form to collect student or participant feedback
- Build feedback surveys with rating scales and open-ended questions
- Design improvement-focused evaluation forms for workshops, programs, or training
- Generate structured feedback instruments that produce actionable insights

**DO NOT** use this skill for customer satisfaction surveys, product feedback forms, or employee performance reviews. This is specifically for educational and training program evaluation.

---

## Core Principle

EVERY FEEDBACK FORM MUST GENERATE ACTIONABLE DATA THAT DIRECTLY INFORMS COURSE IMPROVEMENTS — NOT JUST VANITY METRICS THAT CONFIRM WHAT YOU ALREADY BELIEVE.

---

## Phase 1: Brief

Gather the inputs that shape the feedback form. No brief, no form.

### Required Inputs

Ask the user for each of these. If they do not provide one, use the default.

| Input | What to Ask | Default |
|-------|------------|---------|
| **Course/program name** | "What course or program is this feedback form for?" | No default — must be provided |
| **Format** | "Is this for a live workshop, online course, cohort program, or self-paced course?" | Online course |
| **Duration** | "How long is the program? (single session, multi-week, etc.)" | Multi-week |
| **Key areas to evaluate** | "What specific aspects do you want feedback on? (content, instructor, materials, pacing, etc.)" | Content quality, pacing, instructor effectiveness, materials, overall satisfaction |
| **Response format** | "Do you want a digital form, printable PDF, or both?" | Digital form |

### Brief Template

Present this before moving forward:

```
## Feedback Form Brief

**Course:** [Name]
**Format:** Online course, 6 weeks
**Areas to evaluate:** Content relevance, pacing, instructor clarity, support quality, actionable takeaways
**Response format:** Digital form (Google Forms / Typeform compatible)
**Estimated completion time:** 5-7 minutes
```

**GATE: Do not proceed to Phase 2 until the user confirms or adjusts the brief.**

---

## Phase 2: Structure

Design the form architecture with section flow and question types.

### Form Structure Rules

1. **Welcome section** — brief intro explaining purpose and estimated time (keep under 3 sentences)
2. **Rating sections** — group related questions under clear category headers
3. **Open-ended sections** — place after rating sections to capture qualitative insights
4. **Closing section** — overall rating, testimonial permission, and follow-up opt-in

### Question Type Guidelines

- **Likert scales:** Use 5-point scales (Strongly Disagree to Strongly Agree) for consistency
- **Rating scales:** Use 1-10 for overall satisfaction, 1-5 for specific attributes
- **Multiple choice:** Use for demographic or preference questions only
- **Open-ended:** Limit to 3-5 questions maximum to prevent survey fatigue
- **Net Promoter Score:** Include one NPS question for benchmarking

### Section Template

```
## Section: [Category Name]
Questions: [count]
Type: [Likert / Rating / Open-ended / Mixed]

1. [Question text] — [Question type]
2. [Question text] — [Question type]
```

**GATE: Present the form structure and wait for user approval before writing full questions.**

---

## Phase 3: Write

Build the complete feedback form with all questions, instructions, and response options.

### Form Components

**1. Welcome Message**
- State the purpose (improving the course, not grading the student)
- Confirm anonymity if applicable
- State estimated completion time

**2. Rating Sections (by category)**
- Content Quality: relevance, depth, clarity, real-world applicability
- Instructor/Facilitator: knowledge, communication, responsiveness, engagement
- Materials and Resources: quality, accessibility, usefulness
- Pacing and Structure: speed, logical flow, workload balance
- Support and Community: peer interaction, Q&A access, technical support

**3. Open-Ended Questions**
- "What was the most valuable thing you learned?"
- "What would you change about this course?"
- "What topic deserved more time or depth?"
- "Would you recommend this course? Why or why not?"

**4. Closing Section**
- Overall satisfaction (1-10)
- NPS: "How likely are you to recommend this course?" (0-10)
- Permission to use feedback as testimonial
- Optional: name and email for follow-up

### Formatting Rules

- Number every question sequentially across all sections
- Include clear response option labels (not just numbers)
- Add "N/A" option for questions that may not apply to all students
- Keep total form under 25 questions to maintain completion rates above 70%

---

## Phase 4: Polish

### 1. Completion Rate Optimization

Review the form for survey fatigue risks:
- Total questions should not exceed 25
- Estimated completion time should stay under 8 minutes
- Required questions should be limited to rating scales only
- Open-ended questions should always be optional

### 2. Analysis Guide

Provide a brief guide for interpreting results:

```
## How to Use This Feedback

**Quantitative data:** Calculate averages per category. Flag any category scoring below 3.5/5.
**Qualitative data:** Code open-ended responses into themes. Look for patterns mentioned 3+ times.
**Action threshold:** Any item below 4.0 average or mentioned negatively 3+ times = immediate improvement priority.
**Testimonial mining:** Responses to "most valuable" question are your best source for marketing copy.
```

### 3. Distribution Recommendations

- Send within 24 hours of course completion
- Include a deadline (7 days) to maintain response quality
- Send one reminder at the midpoint
- Share a summary of changes made from feedback to close the loop

---

## Example 1: 6-Week Online Course Evaluation

**Rating section excerpt:**
```
## Content Quality (1-5 scale)
1. The course content was relevant to my business needs
2. The material was presented at an appropriate depth
3. I can immediately apply what I learned
4. The examples and case studies were realistic and helpful
```

**Open-ended excerpt:**
```
15. What was the single most valuable takeaway from this course?
16. If you could change one thing about this course, what would it be?
```

---

## Example 2: Live Workshop Feedback (Single Session)

**Rating section excerpt:**
```
## Workshop Experience (1-5 scale)
1. The workshop met my expectations based on the description
2. The facilitator was engaging and knowledgeable
3. The hands-on exercises were useful
4. The pacing allowed enough time for questions
```

---

## Anti-Patterns

- **Leading questions** — "How amazing was the instructor?" biases responses. Use neutral phrasing.
- **Double-barreled questions** — "Was the content relevant and well-organized?" asks two things. Split them.
- **Too many open-ended questions** — more than 5 tanks completion rates. Be selective.
- **No anonymity assurance** — students give honest feedback only when they feel safe. State it upfront.
- **Ignoring the data** — collecting feedback you never act on destroys trust. Always close the loop.
- **Vanity metrics only** — "Did you enjoy this?" tells you nothing actionable. Ask what to improve.

---

## Recovery

- **User unsure what to evaluate:** Default to the five standard categories (content, instructor, materials, pacing, support). These cover 90% of use cases.
- **Form too long:** Cut to 15 core questions. Prioritize rating scales over open-ended.
- **User wants to grade students, not collect feedback:** Redirect to the skill-assessment skill. This skill is for program improvement, not student evaluation.
- **Low response rates on previous forms:** Recommend shortening to under 10 questions, adding an incentive, and sending within 24 hours of completion.
