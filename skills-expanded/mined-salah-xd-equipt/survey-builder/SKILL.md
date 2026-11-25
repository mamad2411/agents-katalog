---
name: survey-builder
description: "Creates customer feedback surveys with strategically ordered questions, response scales, and analysis frameworks for measuring satisfaction, gathering product feedback, or validating new ideas. Use when a user needs to collect customer feedback, wants to run a Net Promoter Score survey, or needs to validate a product idea before building it."
allowed-tools: Read Write Glob mcp__claude_ai_Notion__notion-create-database mcp__claude_ai_Notion__notion-create-pages mcp__claude_ai_Notion__notion-search
metadata:
  author: Salah-XD
  version: "1.0"
---

# Survey Builder

## When to Use This Skill

Use this skill when you need to:
- Create a customer satisfaction (CSAT) or Net Promoter Score (NPS) survey
- Build a product feedback survey to improve an existing offering
- Design a market validation survey before building a new product or feature
- Write a post-purchase survey for an e-commerce store or digital product
- Construct a churn exit survey to understand why customers are leaving
- Collect structured feedback from clients, students, members, or event attendees

**DO NOT** use this skill for:
- Academic or scientific research surveys (different methodology and IRB requirements)
- Medical or psychological assessments (regulated instruments)
- Employee engagement or HR surveys (different legal and privacy considerations)
- Quizzes, tests, or assessments with right/wrong answers
- Polls with a single question (just write the question directly)

---

## Quick Reference: Survey Capabilities

| Feature | Details |
|---------|---------|
| Survey types | 6 templates (CSAT, NPS, Product Feedback, Market Validation, Post-Purchase, Churn Exit) |
| Question types | 6 formats (Multiple Choice, Rating Scale, Open-Ended, Yes/No, Matrix/Grid, Ranking) |
| Response scales | 3 validated scales (Likert 5-point, NPS 0-10, Satisfaction emoji) |
| Question budget | 8-12 default, max 15 with justification |
| Analysis frameworks | NPS calculation, CSAT scoring, thematic analysis, response rate benchmarks |
| Output formats | Markdown document, optional Notion question bank database |

## Quick Reference: Survey Types

| Type | Questions | Ideal Length | Best Timing | Anchor Question |
|------|-----------|-------------|-------------|-----------------|
| **Customer Satisfaction (CSAT)** | 6-10 | 3-5 minutes | 24-48 hours after interaction | "How satisfied are you with your experience?" (1-5) |
| **Net Promoter Score (NPS)** | 5-8 | 2-3 minutes | 14-30 days after purchase or onboarding | "How likely are you to recommend us?" (0-10) |
| **Product Feedback** | 8-12 | 5-7 minutes | After 2+ weeks of active usage | "How well does this product meet your needs?" (1-5) |
| **Market Validation** | 8-10 | 4-6 minutes | Before building; target ideal customer profile | "How would you solve this problem today?" (open-ended) |
| **Post-Purchase** | 6-8 | 3-4 minutes | 3-7 days after delivery or completion | "How satisfied are you with your purchase?" (1-5) |
| **Churn Exit** | 5-7 | 2-3 minutes | Within 24 hours of cancellation | "What is the primary reason you are leaving?" (multiple choice) |

## Quick Reference: Question Types

| Type | Format | When to Use | Example |
|------|--------|-------------|---------|
| **Multiple Choice** | Select one from a list | Categorize responses, force clear answers | "How did you hear about us?" with 5 options |
| **Rating Scale (1-5)** | Numbered scale with labels | Measure intensity of sentiment | "How easy was the checkout process?" 1=Very Difficult, 5=Very Easy |
| **Rating Scale (0-10)** | Numbered scale, NPS format | Net Promoter Score questions only | "How likely are you to recommend us to a friend?" 0=Not at all, 10=Extremely likely |
| **Open-Ended** | Free text response | Capture nuance, stories, suggestions | "What is one thing we could improve?" |
| **Yes/No** | Binary choice | Screen or filter, confirm simple facts | "Did your order arrive on time?" |
| **Matrix/Grid** | Rate multiple items on same scale | Compare features or attributes efficiently | Rate satisfaction with: support, speed, quality (each 1-5) |
| **Ranking** | Drag to order or number preferences | Prioritize features or preferences | "Rank these features by importance: A, B, C, D" |

## Quick Reference: Response Scales

**Likert 5-Point (satisfaction, agreement, ease):**

| Score | Satisfaction Label | Agreement Label | Ease Label |
|-------|--------------------|-----------------|------------|
| 1 | Very Dissatisfied | Strongly Disagree | Very Difficult |
| 2 | Dissatisfied | Disagree | Difficult |
| 3 | Neutral | Neither Agree nor Disagree | Neutral |
| 4 | Satisfied | Agree | Easy |
| 5 | Very Satisfied | Strongly Agree | Very Easy |

**NPS 0-10:**

| Range | Category | Meaning |
|-------|----------|---------|
| 0-6 | Detractors | Unhappy, may churn or leave negative reviews |
| 7-8 | Passives | Satisfied but unenthusiastic, vulnerable to competitors |
| 9-10 | Promoters | Loyal, will refer others and drive growth |

**Formula:** NPS = % Promoters - % Detractors (range: -100 to +100)

**Satisfaction Emoji Scale (lightweight, mobile-friendly):** 1=Very Unhappy (angry face), 2=Unhappy (sad face), 3=Okay (neutral face), 4=Happy (smiling face), 5=Love It (heart-eyes face). Use only if the user specifically requests a lightweight mobile-first survey.

**DEFAULT: Likert 5-point for CSAT, NPS 0-10 for NPS, emoji scale only on explicit request.**

---

## Core Workflow

EVERY SURVEY STARTS WITH A CLEAR GOAL BEFORE A SINGLE QUESTION IS WRITTEN -- A SURVEY WITHOUT A DEFINED PURPOSE PRODUCES DATA NOBODY CAN ACT ON.

### Step 1: Strategy

Gather these details before writing any questions:

1. **Survey goal** -- what decision will this data inform? (required)
2. **Survey type** -- CSAT, NPS, Product Feedback, Market Validation, Post-Purchase, or Churn Exit (default: infer from goal)
3. **Target respondent** -- who is taking this survey? (required)
4. **Distribution method** -- email, in-app popup, link on website, social media, QR code (default: email)
5. **Question count budget** -- how many questions max? (default: 8-12)
6. **Incentive** -- discount code, entry into a drawing, free resource, none (default: none)
7. **Existing data** -- does the user already have feedback, reviews, or support tickets to reference?

If the user provides items 1 and 3, proceed with defaults for the rest.

**Brief template for vague requests:**

```
I'll build your survey. Quick details needed:

1. What decision will this survey inform? (e.g., improve onboarding, validate a new feature)
2. Who is taking the survey? (e.g., paying customers, free trial users, newsletter subscribers)
3. How will you send it? (email, in-app, link, social media -- default: email)
4. Max number of questions? (default: 10)
5. Any incentive for completing it? (discount, raffle, free resource -- default: none)
```

**GATE: Do not proceed until you have: survey goal AND target respondent.**

### Step 2: Build

Write questions following survey science principles in this exact order:

1. **Start with a screening or warmup question** -- easy, non-threatening, builds momentum
2. **Group questions by topic** -- do not jump between themes
3. **Place the anchor question early** -- CSAT or NPS core question in position 2-4
4. **Put sensitive or hard questions in the middle** -- pricing, complaints, competitor usage
5. **End with an open-ended question** -- "Is there anything else you would like to share?"
6. **Demographics last** -- only if needed, and explain why you are asking

**Question writing rules -- apply to EVERY question:**

- One concept per question. Never double-barreled ("How satisfied are you with our product and support?")
- Neutral wording. Never leading ("How much did you love our new feature?")
- Balanced response scales. Include negative, neutral, and positive options
- Include "N/A" or "Prefer not to say" where the question may not apply to all respondents
- Keep questions under 25 words
- Avoid jargon, abbreviations, and internal terminology
- Use "you" and "your" -- direct and personal
- Default to required questions. Mark optional questions explicitly.

**For each question, specify:**

```
Q[#]: [Question text]
Type: [Multiple Choice / Rating Scale 1-5 / Rating Scale 0-10 / Open-Ended / Yes/No / Matrix / Ranking]
Options: [List response options if applicable]
Required: [Yes / No]
Logic: [Skip logic or branching if applicable, otherwise "None"]
```

### Step 3: Present

Show the complete survey for approval with:
- Survey title and introduction text (what the survey is about, estimated completion time, incentive if any)
- All questions numbered with types, options, and logic
- Thank-you/completion message
- Total estimated completion time

**GATE: Do not write files or create Notion databases until the user approves the survey.**

### Step 4: Deliver

After approval, deliver in one or both formats:

**Format A: Markdown document (always)**

Save to `survey/` (or user-specified path):

```
survey/
├── survey.md                # Complete survey with all questions
└── analysis-framework.md    # How to interpret results
```

**Format B: Notion question bank (if user requests)**

1. Call `notion-search` to find the target page
2. Call `notion-create-database` with 8 properties: Question Text (title), Question Number (number), Question Type (select: Multiple Choice, Rating Scale 1-5, Rating Scale 0-10, Open-Ended, Yes/No, Matrix, Ranking), Response Options (rich_text), Required (checkbox), Logic Notes (rich_text), Survey Section (select: Warmup, Core, Sensitive, Closing, Demographics), Status (select: Draft, Approved, In Use, Retired)
3. Call `notion-create-pages` to add all questions as rows
4. Confirm creation with the user

**Always include the analysis framework with delivery:**

- How to calculate the primary metric (NPS score, CSAT percentage, etc.)
- Response rate benchmarks by channel
- How to analyze open-ended responses (thematic coding)
- When to act vs. when to collect more data

---

## Analysis Framework

### NPS Calculation

```
Total responses: [N]
Promoters (9-10):  [count] = [%]
Passives (7-8):    [count] = [%]
Detractors (0-6):  [count] = [%]

NPS = % Promoters - % Detractors

Interpretation:
  -100 to 0:   Needs urgent attention
  1 to 30:     Good, room to improve
  31 to 50:    Strong
  51 to 70:    Excellent
  71 to 100:   World-class
```

### CSAT Calculation

```
CSAT Score = (Number of satisfied responses / Total responses) x 100

"Satisfied" = respondents who selected 4 or 5 on a 1-5 scale

Interpretation:
  Below 60%:   Poor — investigate immediately
  60-70%:      Below average — prioritize improvements
  70-80%:      Average — identify quick wins
  80-90%:      Good — maintain and optimize
  Above 90%:   Excellent — protect what is working
```

### Response Rate Benchmarks

| Channel | Average Rate | Good Rate | Actions to Improve |
|---------|-------------|-----------|-------------------|
| Email (existing customers) | 10-15% | 20-30% | Personalize subject line, send from a person not a brand |
| In-app popup | 15-25% | 30-40% | Trigger after positive action, keep under 5 questions |
| Post-purchase email | 5-10% | 15-20% | Send within 3-7 days, offer incentive |
| Link on website | 1-3% | 5-10% | Prominent placement, clear value proposition |
| Social media | 1-5% | 5-10% | Use stories/polls for single questions, link for full surveys |

### Open-Ended Response Analysis

1. Read all responses once without categorizing
2. Identify recurring themes (aim for 5-8 categories)
3. Code each response to one or more themes
4. Count frequency per theme
5. Pull 2-3 representative quotes per theme
6. Rank themes by frequency and business impact
7. Present as: Theme name, frequency count, sample quotes, recommended action

---

## Example 1: Post-Purchase CSAT Survey for an Online Course

**User request:** "I sell a $297 online course on freelance copywriting. 50 students per cohort. I want to measure satisfaction and figure out what to improve for the next cohort."

**Step 1 (Strategy):** Goal: improve course content for next cohort. Type: Post-Purchase. Target: students who completed the course. Distribution: email. Budget: 10 questions. Incentive: early access to bonus module.

**Step 2 (Build):**

```
SURVEY: Freelance Copywriting Masterclass — Student Feedback
Estimated time: 4-5 minutes
Incentive: Complete this survey for early access to the bonus portfolio-building module.

Q1: Which best describes your experience level when you started the course?
Type: Multiple Choice
Options: Complete beginner / Some experience (under 1 year) / Intermediate (1-3 years) / Advanced (3+ years)
Required: Yes
Logic: None

Q2: Overall, how satisfied are you with the Freelance Copywriting Masterclass?
Type: Rating Scale 1-5
Options: 1=Very Dissatisfied, 2=Dissatisfied, 3=Neutral, 4=Satisfied, 5=Very Satisfied
Required: Yes
Logic: None

Q3: How likely are you to recommend this course to a friend or colleague?
Type: Rating Scale 0-10
Options: 0=Not at all likely, 10=Extremely likely
Required: Yes
Logic: None

Q4: Rate your satisfaction with each of the following:
Type: Matrix/Grid (1-5 scale: Very Dissatisfied to Very Satisfied)
Items:
  - Course content and curriculum
  - Video lesson quality
  - Assignments and exercises
  - Community and peer interaction
  - Instructor responsiveness
Required: Yes
Logic: None

Q5: Which module was most valuable to you?
Type: Multiple Choice
Options: Module 1: Copywriting Fundamentals / Module 2: Finding Clients / Module 3: Writing Sales Pages / Module 4: Email Sequences / Module 5: Pricing and Proposals / Module 6: Building a Portfolio
Required: Yes
Logic: None

Q6: Which module needs the most improvement?
Type: Multiple Choice
Options: Module 1: Copywriting Fundamentals / Module 2: Finding Clients / Module 3: Writing Sales Pages / Module 4: Email Sequences / Module 5: Pricing and Proposals / Module 6: Building a Portfolio / None — all modules were strong
Required: Yes
Logic: None

Q7: Have you landed a freelance copywriting client since completing the course?
Type: Multiple Choice
Options: Yes, one client / Yes, multiple clients / Not yet, but actively pitching / Not yet, still building my portfolio / I was already freelancing before the course
Required: Yes
Logic: If "Not yet, but actively pitching" or "Not yet, still building my portfolio" -> show Q8

Q8: What is the biggest obstacle preventing you from landing your first client?
Type: Open-Ended
Required: No
Logic: Only shown if Q7 = "Not yet" options

Q9: What is one specific change that would make this course significantly better?
Type: Open-Ended
Required: Yes
Logic: None

Q10: Is there anything else you would like to share about your experience?
Type: Open-Ended
Required: No
Logic: None

THANK YOU MESSAGE:
Thank you for your feedback! Your responses will directly shape the next cohort's experience. Check your email within 48 hours for early access to the bonus portfolio-building module.
```

**Step 4 (Delivery):** Two files saved to `survey/`. Analysis framework included with CSAT calculation (target: 80%+), NPS calculation, module comparison matrix, and thematic coding guide for Q8, Q9, Q10.

---

## Example 2: Market Validation Survey for a New SaaS Idea

**User request:** "I want to build a client portal tool for freelancers. Before I start coding, I need to know if freelancers would actually pay for this. I have a newsletter with 2,000 subscribers who are freelancers."

**Step 1 (Strategy):** Goal: validate demand and willingness to pay before building. Type: Market Validation. Target: freelancers on email list. Distribution: email. Budget: 8 questions. Incentive: none (keep it pure).

**Step 2 (Build):**

```
SURVEY: Client Management for Freelancers — Quick Research
Estimated time: 3-4 minutes

Q1: What type of freelance work do you primarily do?
Type: Multiple Choice
Options: Design and creative / Writing and content / Development and tech / Consulting and strategy / Marketing and ads / Other (please specify)
Required: Yes
Logic: None

Q2: How do you currently share deliverables and updates with clients?
Type: Multiple Choice (select all that apply)
Options: Email attachments / Google Drive or Dropbox links / Project management tool (Asana, Trello, etc.) / Custom-built portal or website / I have no consistent system
Required: Yes
Logic: None

Q3: How satisfied are you with your current method of sharing work with clients?
Type: Rating Scale 1-5
Options: 1=Very Dissatisfied, 2=Dissatisfied, 3=Neutral, 4=Satisfied, 5=Very Satisfied
Required: Yes
Logic: None

Q4: How often do clients ask you for a status update that you have already provided?
Type: Multiple Choice
Options: Never / Rarely (once a month or less) / Sometimes (a few times a month) / Often (weekly) / Constantly (multiple times a week)
Required: Yes
Logic: None

Q5: If a tool existed that gave each client a branded portal with project status, shared files, invoices, and a message thread in one place, how interested would you be?
Type: Rating Scale 1-5
Options: 1=Not at all interested, 2=Slightly interested, 3=Moderately interested, 4=Very interested, 5=Extremely interested
Required: Yes
Logic: If 1 or 2 -> skip to Q8

Q6: What is the maximum you would pay per month for a client portal tool?
Type: Multiple Choice
Options: $0 (would only use if free) / $9-19/month / $20-39/month / $40-59/month / $60+/month
Required: Yes
Logic: Only shown if Q5 = 3, 4, or 5

Q7: Which feature would matter most to you in a client portal?
Type: Ranking
Items: Branded portal with my logo / File sharing and version history / Invoice and payment tracking / Project status timeline / Client messaging thread
Required: Yes
Logic: Only shown if Q5 = 3, 4, or 5

Q8: Is there anything else you would like to share about how you manage client work?
Type: Open-Ended
Required: No
Logic: None

THANK YOU MESSAGE:
Thank you for sharing your experience! Your input is shaping a tool built specifically for freelancers like you. I will share updates as the project develops.
```

**Step 4 (Delivery):** Two files saved to `survey/`. Analysis framework includes: interest score distribution (Q5), willingness-to-pay histogram (Q6), feature priority ranking (Q7), validation thresholds (proceed if 40%+ rate Q5 as 4 or 5 AND median WTP is $20+/month).

---

## Anti-Patterns

- **DO NOT** write leading questions. "How much did you love our product?" assumes a positive response. Write: "How satisfied are you with our product?"
- **DO NOT** create surveys longer than 15 questions without explicit justification from the user. Every question beyond 12 drops completion rates by approximately 5-10%.
- **DO NOT** use double-barreled questions. "How satisfied are you with our product and customer support?" measures two things. Split into two questions.
- **DO NOT** put demographic questions first. Demographics feel invasive as openers and increase abandonment. Place them last, and only include demographics that are necessary for analysis.
- **DO NOT** use unbalanced scales. A scale with "Terrible, Bad, Okay, Good, Great, Amazing, Outstanding" is biased toward positive responses. Use balanced options: equal negative and positive with a neutral midpoint.
- **DO NOT** make every question required. Open-ended and sensitive questions should be optional. Mandatory open-ended questions produce garbage responses like "N/A" and "nothing."
- **DO NOT** use jargon or internal language. "How would you rate our NPS touchpoint optimization?" means nothing to a customer. Write in the language your respondents actually use.
- **DO NOT** include "Other (please specify)" on every multiple choice question. Only add it when the list genuinely cannot cover all possibilities. Overuse signals lazy question design.
- **DO NOT** skip the analysis framework. A survey without a plan for interpreting results produces a spreadsheet of data nobody reads.

---

## Recovery and Troubleshooting

### User Cannot Articulate the Survey Goal

1. Ask: "What decision will you make differently based on the survey results?"
2. If still vague, offer the three most common goals for their business type:
   - "Are you trying to (a) measure satisfaction, (b) improve a specific product, or (c) validate a new idea?"
3. Pick the one they confirm and proceed
4. **If 3 clarification rounds produce no clear goal:** "A survey without a clear goal produces data you cannot act on. Let us pause and define what you want to learn before writing questions."

### User Wants More Than 15 Questions

1. Explain the tradeoff: "Each question beyond 12 drops your completion rate by 5-10%. A 20-question survey may get half the responses of a 10-question survey."
2. Offer to split into two shorter surveys sent at different times
3. Prioritize: "Which 5 questions are most critical to your decision? Let us start there and add only what is essential."
4. **Maximum hard cap: 20 questions.** Beyond this, refuse and explain why.

### User Wants to Survey People They Have No Access To

1. Clarify distribution: "How will you reach these respondents? Do you have their email, or are they in a community you can post to?"
2. If no access: suggest building the audience first (email list, social following, community membership)
3. Offer to create the survey now and hold it until distribution is solved
4. **DO NOT promise response rates for audiences the user cannot reach.**

### Notion Page Not Found

1. Ask the user for the exact page title
2. Try `notion-search` with a shorter keyword
3. Confirm the Notion integration has access to that page
4. **After 3 failed searches:** "I cannot locate that page. Please verify the page exists in Notion and that the integration has access. Check Settings > Connections."

### User Wants to Edit an Approved Survey

1. Read the existing survey file with `Read`
2. Make requested changes
3. Re-verify question order follows survey science principles (warmup first, anchor early, sensitive in middle, open-ended and demographics last)
4. Re-present the updated survey for approval
5. Overwrite the file on second approval

### Low Response Rate After Launch

Advise the user: shorten to 5-7 questions, personalize the invitation with their first name, send from a person not a brand, send Tuesday-Thursday 10am-2pm in the recipient's timezone, add an incentive if none exists, follow up once after 5-7 days with non-responders, and test the survey themselves to verify it takes under 5 minutes.

---

## Pre-Delivery Checklist

Run this checklist before delivering any survey. **DO NOT SKIP ANY ITEM.**

| Check | What to Verify |
|-------|----------------|
| Goal defined | Survey has a clear, stated purpose tied to a decision |
| Question count | Within budget (default 8-12, max 15 unless justified) |
| Question order | Warmup first, anchor early, sensitive middle, open-ended and demographics last |
| No double-barreled | Every question measures exactly one concept |
| No leading language | All questions are neutrally worded |
| Balanced scales | Equal positive and negative options with neutral midpoint |
| N/A option | Included where a question may not apply to all respondents |
| Open-ended optional | Free-text questions are not marked as required (except the main feedback question) |
| Logic correct | Skip logic and branching conditions are accurate |
| Introduction text | Survey has a title, purpose statement, time estimate, and incentive (if any) |
| Thank-you message | Survey ends with a completion message |
| Analysis framework | Delivery includes how to calculate metrics and interpret results |
| File saved | Write tool confirmed successful save |
| Notion database | Created and populated if user requested (verify with search) |

```
Pre-Delivery Checklist:
  [x] Survey goal clearly defined
  [x] Question count within budget
  [x] Question order follows survey science
  [x] No double-barreled questions
  [x] No leading language
  [x] Balanced response scales
  [x] N/A options where appropriate
  [x] Open-ended questions marked optional
  [x] Skip logic verified
  [x] Introduction text complete
  [x] Thank-you message included
  [x] Analysis framework delivered
  [x] File saved successfully
  [x] Notion database created (if requested)
```
