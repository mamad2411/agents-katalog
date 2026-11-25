---
name: employee-handbook
description: "Creates employee or contractor handbooks with company policies, expectations, benefits, communication guidelines, and operational procedures in a professional yet approachable tone. Use when a user is hiring their first employee, onboarding contractors, scaling their team, or needs to formalize workplace policies."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Employee Handbook

## When to Use This Skill

Use this skill when:
- A user is hiring their first employee or contractor and needs written policies
- A business owner wants to formalize workplace expectations before scaling
- Someone is onboarding remote contractors and needs communication norms, deliverable standards, and payment terms documented
- A user asks for a team handbook, employee manual, contractor agreement guide, or company playbook
- An existing handbook needs to be rewritten or modernized

**DO NOT** use this skill for:
- Employment contracts or legal agreements (those require an attorney)
- Job descriptions or job postings (use the job-posting skill)
- SOPs for specific business processes (use the sop-builder skill)
- Independent contractor classification guidance (that is a legal/tax question)

---

## Core Principle

A HANDBOOK IS NOT A LEGAL CONTRACT — IT IS AN OPERATIONAL GUIDE THAT SETS CLEAR EXPECTATIONS SO EVERYONE KNOWS HOW WORK GETS DONE, WHAT IS EXPECTED, AND WHERE TO FIND ANSWERS.

---

## Phase 1: Gather — Collect Company Context

Ask these questions in two groups, waiting for answers between each group. **Do not skip this phase.**

**Group 1 — Basics (ask all at once):**

1. What is your company name?
2. How many people are on your team right now? (Include yourself.)
3. What is your work arrangement? (Remote, hybrid, or in-office?)
4. What industry are you in?
5. Are you hiring employees, contractors, or both?

**Group 2 — Specifics (ask after Group 1 is answered):**

6. Do you have any existing policies or documents you want incorporated? (If yes, ask the user to share them or paste the text.)
7. What state or country are your team members based in? (This determines which compliance notes to flag.)
8. What tools does your team use for communication and project management? (Slack, Asana, email, etc.)
9. What are your standard working hours or availability expectations?

### Handbook Type Selection

After gathering answers, recommend one of three handbook types. **Default to Contractor Handbook** unless the user's answers clearly indicate otherwise.

| Handbook Type | Best For | Typical Length |
|---------------|----------|---------------|
| **Full Employee Handbook** | W-2 employees, businesses with 3+ staff, compliance-heavy industries | 15-25 pages |
| **Contractor Handbook** | 1099 contractors, freelancers, remote teams, solopreneurs scaling | 5-10 pages |
| **Team Playbook** | Culture-focused teams, creative agencies, early-stage startups | 5-8 pages |

Present the recommendation: "Based on what you have described, I recommend a [type]. Here is why: [one sentence]. Does that sound right, or would you prefer a different format?"

**GATE: Do not proceed to Phase 2 until you have the company name, work arrangement, and employee/contractor distinction confirmed.** If the user skips questions, note the gaps and ask once more. If they still decline, proceed with reasonable defaults and flag assumptions with bold markers in the handbook.

---

## Phase 2: Structure — Select Sections

Present the full section menu to the user with a recommended set pre-selected based on their handbook type.

### Section Menu

| # | Section | Employee | Contractor | Playbook |
|---|---------|----------|------------|----------|
| 1 | Welcome and Company Overview | Yes | Yes | Yes |
| 2 | Mission, Vision, and Values | Yes | Optional | Yes |
| 3 | Employment/Engagement Terms | Yes | Yes | No |
| 4 | Work Schedule and Availability | Yes | Yes | Yes |
| 5 | Communication (tools, response times, meeting norms) | Yes | Yes | Yes |
| 6 | Project Management and Deliverables | Optional | Yes | Yes |
| 7 | Time Off and Leave Policies | Yes | No | No |
| 8 | Compensation and Payment | Yes | Yes | No |
| 9 | Equipment and Tools | Yes | Optional | No |
| 10 | Confidentiality and Intellectual Property | Yes | Yes | Optional |
| 11 | Code of Conduct | Yes | Yes | Yes |
| 12 | Performance and Feedback | Yes | Optional | Yes |
| 13 | Termination and Offboarding | Yes | Yes | No |
| 14 | Acknowledgment Page | Yes | Yes | Optional |

Present this as a checklist: "Here are the sections I recommend for your [type]. Let me know if you want to add or remove any before I start writing."

**GATE: Do not proceed to Phase 3 until the user approves which sections to include.** Acceptable approvals: "looks good," "yes," "go for it," or similar affirmative. If the user wants custom sections not on this list, add them.

---

## Phase 3: Write — Draft Each Section

Write each approved section following these rules:

1. **Plain language only.** No legalese, no jargon. Write like a competent manager explaining policies to a new team member over coffee.
2. **Specific over vague.** "Respond to Slack messages within 4 business hours" beats "Respond to messages promptly."
3. **Flag legal review areas.** Any section touching compliance, termination, non-competes, or benefits must include a bold note: **"Have an employment attorney review this section before distributing."**
4. **Consistent tone.** Professional but human. Firm on expectations, warm on culture.
5. **Use the user's actual tools and details.** If they said they use Slack and Asana, write "Post daily standups in the #standups Slack channel" — not "Use your communication tool."

### Section Writing Templates

#### 1. Welcome and Company Overview

Open with a warm welcome, a 2-3 sentence company description using the user's actual details, and a short "How to Use This Handbook" note directing questions to a specific person or channel. Set the tone immediately: "This is a guide, not a legal contract."

#### 5. Communication

Build a table of the user's actual tools with columns for Tool, Purpose, and Expected Response Time. Follow with 4-5 bullet-point communication norms (default to async, use threads, no after-hours expectations, meetings require agendas). End with core availability hours.

#### 10. Confidentiality and Intellectual Property

Define what is confidential (client lists, pricing, strategies, internal communications). State IP ownership clearly. List 3-4 practical rules (do not share client info externally, do not use company strategies for personal projects, when in doubt ask). **Flag for attorney review.**

#### 14. Acknowledgment Page

Include: confirmation of receipt, statement that the handbook is not a contract, company's right to update policies, signature lines for both team member and company representative with name/signature/date fields.

### Legal Disclaimer

Include this on the first or second page of every handbook:

```markdown
> **Disclaimer:** This handbook is an internal guide and does not
> constitute a legal contract, guarantee of employment, or binding
> agreement. Policies may be updated at any time with notice.
> Consult a qualified employment attorney to ensure compliance
> with federal, state, and local laws applicable to your business.
```

**GATE: Present the complete handbook to the user before saving to file. Do not save until the user reviews and approves.** If the user requests changes, make them and re-present. **If the user requests more than 3 rounds of revisions, pause and ask:** "We have been through several rounds — would you like to finalize what we have and mark remaining items for future revision, or keep iterating?"

---

## Phase 4: Deliver — Save and Advise

After user approval:

1. **Save the handbook** as a single markdown file with a table of contents at the top. Write it to the user's current working directory as `[company-name]-handbook.md` (lowercase, hyphens for spaces).
2. **Include the table of contents** with anchor links to each section.
3. **Add the legal disclaimer** on the first page.
4. **Include the acknowledgment page** as the final section.
5. **Post-delivery advice:**
   - "Have an employment attorney review this handbook before distributing it to your team, especially sections on termination, leave policies, confidentiality, and IP."
   - "Revisit this handbook every 6-12 months as your team and policies evolve."
   - "Keep a signed copy of the acknowledgment page for each team member."

---

## Concrete Examples

### Example 1: Remote Digital Agency — Contractor Handbook

**User says:** "I run a 5-person remote design agency. Everyone is a contractor. I need something that covers how we communicate, how projects work, and when they get paid."

**Phase 1 gathers:**
- Company: Pixel Bridge Design
- Team: 5 contractors (3 designers, 1 copywriter, 1 project manager)
- Work arrangement: Fully remote, US-based
- Industry: Creative/design agency
- Tools: Slack, Figma, Asana, email

**Phase 2 selects:** Sections 1, 3, 4, 5, 6, 8, 10, 11, 13, 14 (10 sections, Contractor Handbook)

**Phase 3 writes the handbook. Here are three complete sections:**

---

**Section 5 — Communication:**

## Communication

### Tools We Use

| Tool | Purpose | Expected Response Time |
|------|---------|----------------------|
| Slack | Day-to-day team communication | Within 4 business hours |
| Email | Client-facing communication only | Within 24 business hours |
| Asana | Project tasks, deadlines, deliverables | Check and update daily |
| Figma | Design collaboration, comments | Respond to tagged comments within 24 hours |

### Communication Norms

- Default to Slack for internal conversations. Use email only for client communication.
- Reply in threads to keep channels organized. Do not start new threads for ongoing conversations.
- Post daily status updates in #project-updates by 11 AM ET: what you finished yesterday, what you are working on today, any blockers.
- No after-hours response expected. Messages sent outside business hours can wait until the next business day.
- If you need something urgently during business hours, use the @here mention in Slack. Reserve @channel for true emergencies (client deadline at risk, system outage).

### Meetings

- Weekly team sync: Mondays at 10 AM ET, 30 minutes, Zoom. Attendance required.
- Client calls: scheduled by the project manager. You will get at least 24 hours notice.
- All meetings have a written agenda posted in the Slack thread beforehand. If there is no agenda, the meeting is canceled.

---

**Section 8 — Compensation and Payment:**

## Compensation and Payment

### Payment Terms

- Invoices are due on the 1st and 15th of each month (semi-monthly).
- Submit your invoice via email to accounting@pixelbridgedesign.com by end of day on the invoicing date.
- Payment is processed within 5 business days of invoice receipt via direct deposit (ACH).
- If an invoice has errors, we will notify you within 2 business days and process the corrected amount on the next pay cycle.

### Invoice Requirements

Every invoice must include:
- Your full legal name and business name (if applicable)
- Invoice number (sequential)
- Billing period covered
- Itemized list of hours worked or deliverables completed
- Agreed hourly rate or project rate
- Total amount due

### Rate Changes

Rate adjustments are discussed during quarterly reviews. Any rate change takes effect at the start of the next billing period, not retroactively.

---

**Section 6 — Project Management and Deliverables:**

## Project Management and Deliverables

### How Projects Work

1. The project manager creates an Asana project with all tasks, deadlines, and assignees.
2. Each task includes a brief, reference files, and a due date. If any of these are missing, flag it in Slack before starting.
3. Move your tasks through the Asana board as you work: To Do, In Progress, In Review, Done.
4. When a deliverable is ready for review, move it to In Review and tag the project manager in an Asana comment with a link to the file.

### Deadlines

- Internal deadlines are set 48 hours before the client deadline. This gives time for revisions.
- If you cannot hit a deadline, notify the project manager in Slack at least 24 hours before the due date — not on the due date.
- Missed deadlines without advance notice will be addressed in your next feedback session.

### Revisions

- Client revision rounds are part of the project scope. The project manager will communicate revision requests via Asana with clear notes.
- If a revision request is unclear, ask for clarification before starting work. Do not guess at what the client wants.
- Scope creep (requests that go beyond the original brief) should be flagged to the project manager immediately. Do not fulfill out-of-scope requests without approval.

---

### Example 2: Local Retail Shop — Employee Handbook

**User says:** "I own a small bakery with 3 part-time employees. I need a basic handbook that covers schedules, time off, and how I expect them to behave at work."

**Phase 1 gathers:**
- Company: Sweet Elm Bakery
- Team: 3 part-time W-2 employees (bakers and counter staff)
- Work arrangement: In-office (storefront)
- Industry: Retail food/bakery
- Location: Austin, Texas
- Tools: Group text for scheduling, Square POS system

**Phase 2 selects:** Sections 1, 4, 7, 8, 9, 11, 12, 13, 14 (9 sections, Full Employee Handbook)

**Phase 3 writes the handbook. Here are three complete sections:**

---

**Section 4 — Work Schedule and Availability:**

## Work Schedule and Availability

### Store Hours

Sweet Elm Bakery is open Tuesday through Sunday, 7 AM to 3 PM. The store is closed on Mondays.

### Shifts

- **Opening shift:** 5:30 AM - 11:30 AM (includes prep and baking before doors open)
- **Closing shift:** 10:00 AM - 4:00 PM (includes cleanup and closing duties after doors close)
- Schedules are posted every Friday for the following week in the team group text. Check it before the weekend.
- If you need to swap a shift, find your own replacement and notify the manager via text. Both the original and replacement employee must confirm.

### Attendance

- Arrive at least 10 minutes before your shift starts to put on your apron and wash hands.
- If you are going to be late, text the manager immediately — do not wait until after your shift was supposed to start.
- Two no-call/no-shows in a 90-day period will result in a written warning. A third will result in termination.

---

**Section 7 — Time Off and Leave Policies:**

## Time Off and Leave Policies

### Paid Time Off (PTO)

- Part-time employees accrue PTO at a rate of 1 hour for every 30 hours worked, up to 48 hours per year.
- PTO can be used for any reason — sick days, personal days, appointments, rest.
- Request PTO at least 7 days in advance by texting the manager. Requests less than 7 days out will be approved only if coverage is available.
- PTO does not roll over to the next calendar year. Use it or lose it.

### Sick Days

- If you are sick, do not come to work. We serve food — this is non-negotiable.
- Text the manager before 4 AM for an opening shift or before 8 AM for a closing shift.
- You do not need a doctor's note for absences of 1-2 days. Three or more consecutive sick days require a doctor's note before returning.

### Holidays

Sweet Elm Bakery is closed on Thanksgiving, Christmas Day, and New Year's Day. These are unpaid days off unless you have PTO to cover them.

**Have an employment attorney review this section before distributing. Texas labor laws and local Austin ordinances may require specific leave provisions.**

---

**Section 11 — Code of Conduct:**

## Code of Conduct

### General Expectations

- Treat every customer, coworker, and vendor with respect. No exceptions.
- Show up on time, ready to work, in clean attire and with a positive attitude.
- Keep your phone in the back room during your shift. Personal calls and texts happen on breaks only.
- If a customer complains, listen first, apologize, and offer a solution (free replacement, refund, or manager involvement). Never argue with a customer on the floor.

### Food Safety

- Wash your hands before handling food, after touching your face, after using the restroom, and after handling cash or cleaning supplies.
- Wear gloves when assembling or packaging food items. Change gloves between tasks.
- If you see a food safety concern (expired ingredient, unclean surface, temperature issue), stop and report it to the manager immediately. Do not serve anything you would not eat yourself.

### Prohibited Conduct

The following will result in immediate termination:
- Theft of any kind (product, cash, equipment, or time)
- Showing up to work under the influence of alcohol or drugs
- Harassment, discrimination, or bullying of any team member or customer
- Intentional violation of food safety protocols

---

## Anti-Patterns

**NEVER do these when writing a handbook:**

- **DO NOT provide specific legal advice.** A handbook is not a legal document. Always flag compliance-sensitive sections with "Have an employment attorney review this section before distributing." You are not a lawyer and this skill does not replace one.
- **DO NOT use threatening or punitive language.** "Violators will be subject to disciplinary action up to and including termination" is fine. "You WILL be fired if you do X" is not. The tone should be firm and clear, not hostile.
- **DO NOT write policies so vague they are unenforceable.** "Employees should dress appropriately" tells no one anything. "Wear clean, closed-toe shoes and a provided apron during all shifts" is a policy.
- **DO NOT skip the confidentiality and IP section.** Even a 3-person bakery has recipes, supplier contacts, and pricing information worth protecting. Every handbook gets this section unless the user explicitly removes it.
- **DO NOT mix employee and contractor terminology.** Using terms like "employee benefits" or "required work hours" for contractors can create legal misclassification risk. Contractors have "engagement terms" and "availability expectations," not "employment terms" and "mandatory schedules." **This distinction is legally critical.**
- **DO NOT copy-paste generic handbook templates from your training data.** Every handbook must reflect the user's actual company, tools, policies, and culture — not a generic Fortune 500 template.
- **DO NOT include policies the user did not ask for or confirm.** If the user has no drug testing policy, do not invent one. If they did not mention a dress code, ask before adding one.
- **DO NOT write in legalese.** "Notwithstanding the foregoing provisions" has no place in a small business handbook. Write in plain English that a new hire can understand on their first day.
- **DO NOT assume US-based employment law applies.** Always ask where the team is located and flag that compliance varies by jurisdiction.

---

## Recovery

### User Cannot Articulate Their Policies

If the user says "I do not really have set policies" or gives vague answers:

1. Ask scenario-based questions instead: "What happens if someone needs a day off tomorrow? What do you do?" Their answer IS the policy — you just need to formalize it.
2. If they truly have no policies for a section, propose a reasonable default: "Most businesses your size do X. Want me to use that as a starting point?" Then let them adjust.
3. If after 3 attempts they still cannot provide input for a critical section (compensation, termination), mark it with a bold **"[NEEDS YOUR INPUT]"** callout and move on to the next section.

### Employee vs. Contractor Confusion

If the user is unsure whether their team members are employees or contractors:

1. Do not classify for them — this is a legal and tax determination.
2. Say: "Whether someone is an employee or contractor depends on factors like how much control you have over their work, who sets their schedule, and whether they work for other clients. I recommend checking with an accountant or employment attorney to make sure your classification is correct."
3. Ask: "For now, which term do you use when you talk about your team? I will write the handbook to match, and you can adjust after getting legal guidance."

### Handbook Scope Creep

If the user keeps adding sections or requests during Phase 3:

1. After the third unplanned addition, pause: "We have added a few sections beyond the original outline. Want me to keep going, or finalize what we have and create a v2 later with the additional sections?"
2. If the handbook exceeds 25 pages, recommend splitting: "This is getting long enough that people might not read it. Want me to split it into a core handbook (the essentials) and a supplemental policies document?"

### User Wants Legal Guarantees

If the user asks "Is this legally compliant?" or "Can I use this as-is?":

1. Be direct: "I cannot guarantee legal compliance because employment law varies by location, industry, and team size. This handbook is a strong operational foundation, but you should have an employment attorney review it before distributing it — especially the sections on termination, leave, confidentiality, and IP."
2. Never say "yes, this is legally compliant." That is legal advice and you are not qualified to provide it.

### Missing Information Mid-Write

If you reach a section during Phase 3 that requires information the user did not provide in Phase 1 (e.g., you need specific PTO accrual rates for the leave section):

1. Pause writing and ask the specific question: "For the time-off section, how much PTO do you want to offer? Common options for part-time employees are 1 hour per 30 hours worked, or a flat 5 days per year."
2. If the user does not know, offer the most common default for their business size and type, and mark it for their review.

---

## Pre-Delivery Checklist

Before saving the final handbook file, verify:

- [ ] Every section uses the user's actual company name, tools, and details — not generic placeholders
- [ ] Employee vs. contractor language is consistent throughout (no mixing)
- [ ] Compliance-sensitive sections are flagged for attorney review
- [ ] Legal disclaimer appears on the first or second page
- [ ] Acknowledgment page is included as the final section
- [ ] Tone is professional but human — no legalese, no threatening language
- [ ] Table of contents with anchor links is at the top
- [ ] All policies are specific and actionable (no vague "as appropriate" language)
- [ ] File is saved as `[company-name]-handbook.md` in the user's working directory
