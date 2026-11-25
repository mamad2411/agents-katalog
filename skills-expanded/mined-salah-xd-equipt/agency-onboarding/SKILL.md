---
name: agency-onboarding
description: "Creates a complete client onboarding system for agencies and service providers, including welcome email sequence, intake questionnaire, kickoff meeting checklist, and communication guidelines. Use when a user runs an agency, consultancy, or service business and needs to standardize how new clients are brought on board."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Agency Onboarding

## When to Use This Skill

Use this skill when:
- A user runs an agency, consultancy, coaching practice, or service business and wants to standardize client onboarding
- Someone says their onboarding is "different every time" or they keep forgetting steps
- A user needs welcome emails, intake forms, kickoff agendas, or communication guidelines
- A service provider is scaling and needs a repeatable system before they can delegate

**DO NOT** use for internal employee onboarding, SaaS product onboarding, one-time project kickoffs, or sales/proposal workflows.

---

## Core Principle

A CLIENT'S FIRST 14 DAYS DETERMINE WHETHER THEY STAY FOR 14 MONTHS. EVERY COMPONENT MUST REDUCE UNCERTAINTY, BUILD CONFIDENCE, AND SET EXPECTATIONS BEFORE THE CLIENT HAS TO ASK.

---

## Phase 1: Gather -- Interview About Current Onboarding

Conduct a structured interview before building anything. **No interview, no onboarding system.**

**Group 1 -- Business Context (ask all at once):**
1. What type of service business do you run? (marketing agency, design studio, consulting firm, coaching practice)
2. What are your core services? List the 2-4 main things clients hire you for.
3. What does your typical client look like? (Industry, size, budget range, decision-maker role)
4. How many new clients do you onboard per month?

**Group 2 -- Current Process (ask after Group 1):**
5. Walk me through what happens today from "yes" to real work beginning.
6. How long does onboarding currently take?
7. What information do you need from a new client before you can start?
8. Do you have a kickoff meeting? What do you cover?

**Group 3 -- Pain Points and Tools (ask after Group 2):**
9. Where does onboarding break down most often?
10. What tools do you use for communication, project management, and files?
11. Have clients expressed confusion or frustration in their first two weeks?
12. Anything you wish every new client understood before work begins?

**GATE: Do not proceed to Phase 2 until you have answers to at least questions 1-3, 5, 7, and 9.**

**If the user has no existing process:** Skip questions 5-6. Instead ask: "If you could wave a magic wand, what would a perfect first two weeks look like for a new client?" Build from their answer plus the service type defaults below.

---

## Service Type Reference

| Service Type | Typical Intake Needs | Kickoff Focus | Default Cadence |
|-------------|---------------------|---------------|----------------|
| **Marketing Agency** | Brand guidelines, ad account logins, analytics access, past campaigns, audience docs | Goals/KPIs, reporting cadence, approval workflows | Weekly status, monthly strategy |
| **Design Studio** | Brand assets, style guide, competitor refs, content/copy, image assets | Creative direction, revision process, milestones | Milestone check-ins, 48h feedback windows |
| **Consulting Firm** | Org charts, financials, strategic plans, stakeholder list | Scope confirmation, stakeholder alignment, data access | Biweekly check-ins, monthly steering committee |
| **Coaching Practice** | Goals, challenges, scheduling prefs, past coaching experience | Session structure, homework, communication boundaries | Weekly sessions, async messaging between |

---

## Phase 2: Build Components

Build all four components in sequence. Present each as you go.

### Component 1: Welcome Email Sequence (3 Emails)

**Email 1 -- Welcome and Confirmation (Day 0, immediately after signing)**
- Warm welcome (1-2 sentences, genuine, not corporate)
- What happens next (3-bullet numbered list of next 7 days)
- Team introduction (name + title + what they handle)
- Single CTA: reply to confirm receipt

Length: 150-200 words.

Example opener for a marketing agency:

```
Subject: Welcome to Apex Digital -- here's what happens next

Hi Rachel,

We are thrilled to have Greenfield Hotels on board. Your goals around
increasing direct bookings by 30% are exactly the kind of challenge
we love solving.

Here is what happens over the next 7 days:
1. Within 24 hours: our onboarding questionnaire (15 min to complete)
2. Within 3 days: your kickoff call scheduled with the full team
3. By day 7: finalized project timeline and communication plan

Your account team:
- Sarah Chen, Account Manager -- your day-to-day contact
- Marcus Rivera, Lead Strategist -- owns campaign strategy
- Aisha Johnson, Project Coordinator -- keeps timelines on track

Reply to confirm you received this and flag anything that has changed.

Looking forward to the work ahead,
James
```

**Email 2 -- Intake Questionnaire (Day 1)**
- Why you need this info (1 sentence)
- Time estimate and specific deadline
- What happens with their answers
- Single CTA: link to questionnaire

Length: 80-120 words.

**Email 3 -- Kickoff Prep (Day 4-5, one day before kickoff)**
- Meeting details (date, time, duration, link)
- Agenda preview (3-5 bullets)
- What to bring/prepare
- Single CTA: confirm attendance

Length: 100-150 words.

**CRITICAL: Tailor every email to the user's actual service type, team, and tools. Never deliver emails with unfilled placeholders.**

---

### Component 2: Intake Questionnaire

Three sections. **15-20 questions maximum.**

**Section 1 -- Business Context (universal):**
Company name/website, primary and secondary contacts, business description, target audience, top 3 goals for next 6-12 months.

**Section 2 -- Project Specifics (tailored by service type):**

- **Marketing agency:** Current channels and performance, top competitors, brand guidelines, past campaigns, budget range, key metrics
- **Design studio:** Brand assets (logo, colors, fonts), style references (5 loved, 3 disliked), deliverable formats, content status per page, approval process
- **Consulting firm:** Org structure, previous engagements, key stakeholders, available data, known constraints, success definition
- **Coaching practice:** What prompted coaching now, biggest challenge, what they have tried, accountability style, scheduling preferences

**Section 3 -- Logistics (universal):**
Preferred communication channel, availability, timezone, credentials/access to share, upcoming deadlines, anything else.

Format as clean Markdown with numbered questions grouped under section headers.

---

### Component 3: Kickoff Meeting Agenda and Checklist

**Default agenda: 45 minutes.**

| Time | Topic | Led By | Outcome |
|------|-------|--------|---------|
| 0:00-0:05 | Welcome and introductions | Account Manager | Everyone knows names and roles |
| 0:05-0:15 | Review questionnaire and confirm priorities | Strategist/Lead | Validated understanding of goals |
| 0:15-0:25 | Proposed approach, timeline, milestones | Strategist/Lead | Client agrees on direction |
| 0:25-0:35 | Communication plan: cadence, channels, approvals | Account Manager | Mutual working agreement |
| 0:35-0:40 | Open Q&A | All | Client questions resolved |
| 0:40-0:45 | Recap action items and next steps | Account Manager | Both sides know what happens next |

**Internal Pre-Kickoff Checklist:**

24 hours before:
- [ ] Questionnaire responses reviewed by all attending team members
- [ ] Client research complete (website, social, competitors)
- [ ] Proposed timeline drafted and ready to present
- [ ] Meeting link tested, calendar invite confirmed

Within 24 hours after:
- [ ] Follow-up email sent with recap and action items
- [ ] Project timeline created in project management tool
- [ ] Recurring meetings scheduled
- [ ] Client added to all relevant tools and channels

Adjust agenda timing and topics to the service type. A coaching kickoff focuses on session structure and goals; a design studio kickoff needs creative direction exploration (extend to 60 min).

---

### Component 4: Communication Guidelines

One-page document setting expectations for both sides. **This is the single most important component for preventing scope creep and frustration.**

Must include:

1. **Response times per channel** -- table with channel, response time, and best use case
2. **Emergency definition** -- what qualifies as urgent and what does not
3. **Meeting cadence** -- recurring meetings with frequency, duration, attendees, and purpose
4. **Feedback and approval process** -- how deliverables are reviewed, feedback window, what "approved" means, consequences of missed deadlines
5. **Escalation path** -- step 1 (Account Manager), step 2 (Director/Owner), with time commitments
6. **Business hours and boundaries** -- days, times, timezone, holiday policy

**Defaults when user does not specify:**

| Setting | Default |
|---------|---------|
| Email response | 24 business hours |
| Chat response | 4 business hours |
| Emergency response | 2 hours |
| Feedback window | 2 business days |
| Business hours | Mon-Fri, 9 AM - 5 PM, user's timezone |

---

## Phase 3: Review -- Present for Approval

Present all four components in order. After each, ask: "Does this look right? Anything to change?"

After all four: "All components are ready. Should I save them as files, or adjust anything first?"

**GATE: Do not proceed to Phase 4 until the user explicitly approves.** If the user requests more than 3 revision rounds on a single component, pause: "We have been going back and forth on this one. Want me to save what we have and mark uncertain sections with [REVISIT] tags so you can refine after testing with a real client?"

---

## Phase 4: Deliver -- Write to Organized Files

Write all components to this structure:

```
onboarding-system/
  welcome-emails/
    01-welcome-and-confirmation.md
    02-intake-questionnaire-email.md
    03-kickoff-prep.md
  intake-questionnaire.md
  kickoff-meeting/
    agenda.md
    pre-kickoff-checklist.md
  communication-guidelines.md
  README.md
```

The README includes: what each file contains, the onboarding timeline (Day 0-14), and how to use the system with a new client.

**Confirm delivery:** "Your onboarding system has been saved to [path]. Here is what was created: [list components with key stats]. To use it: when a new client signs, open the welcome-emails folder and send Email 1 immediately. Follow the timeline from there."

---

## Concrete Examples

### Example 1: Marketing Agency -- New Retainer Client

**User:** "I run a 6-person digital marketing agency. Every onboarding is chaotic."

**Phase 1:** SEO, paid ads, content. B2B SaaS clients, $3K-8K/month. Uses Slack, Asana, Google Drive. Pain: clients never send logins at once, kickoff calls run long, no one owns week one.

**Phase 2:** Welcome emails reference Slack invite, Asana board, and credentials (GA4, Google Ads, Meta, CMS). Questionnaire covers channels, competitors, analytics access, campaign data, brand guidelines. 45-min kickoff on KPIs, reporting, approval workflows. Comms: Slack 4h, email 24h, weekly status, monthly strategy, escalation to owner after 48h.

**Phase 3:** User adds a sales team involvement question. **Phase 4:** 7 files to `onboarding-system/`.

### Example 2: Web Design Studio -- Website Project Client

**User:** "Two-person studio. Clients never have content ready."

**Phase 1:** Custom websites, $5K-15K. Small business owners. Uses email, Figma, Webflow, Drive. Pain: content takes weeks, design direction never aligned upfront.

**Phase 2:** Emails emphasize content deadlines (design pauses without content). Questionnaire: 5 sites they love + why, 3 they dislike, brand assets, content status per page. 60-min kickoff for creative direction, sitemap, revision policy (2 rounds included). Comms: email only, 24h response, Figma comments, 3-day feedback windows.

**Phase 3:** User clarifies revision policy: "Additional rounds at $150/hr, 2h minimum." **Phase 4:** 7 files written.

---

## Anti-Patterns

- **DO NOT overwhelm Day 1.** The email sequence is spread across 5-7 days for a reason. Sending everything on Day 0 causes clients to shut down and ignore it all. One email, one ask, one day.
- **DO NOT skip the questionnaire.** Kickoff calls that double as intake interviews run 90+ minutes and waste everyone's time. If the client has not completed the questionnaire, delay the kickoff -- do not skip the form.
- **DO NOT leave communication expectations vague.** "We will be in touch" is not a plan. Specify response times, meeting cadence, feedback windows, escalation path, and emergency definitions. Vague expectations are the top cause of client dissatisfaction in the first 30 days.
- **DO NOT reuse the same system across service types.** A coaching onboarding looks nothing like an agency onboarding. Always tailor to the service type.
- **DO NOT build on assumptions.** If the user did not mention a tool, do not insert one. Every component must reflect the user's actual business from Phase 1.
- **DO NOT create 30+ question intake forms.** Cap at 15-20 questions. Split into primary (pre-kickoff) and follow-up (post-kickoff) if needed.

---

## Recovery

- **User has no existing process:** Use service type defaults from the reference table. Present as "Here is what I recommend based on what similar businesses do" and let them modify.
- **Client does not complete the questionnaire:** Build a contingency: Day 3 reminder email, Day 5 personal follow-up offering a 10-min call to complete it together, kickoff becomes intake interview if still incomplete (flag that this adds 7-10 days to start).
- **Solo operator or two-person team:** Remove role-based language, reduce meeting cadence to biweekly, simplify escalation. Keep emails and questionnaire at full depth.
- **User wants additional components** (client portal, contract template, project timeline): Build the core four first. Then add extras as separate files in the same directory.
- **If 3 revision rounds fail:** Stop and save with [REVISIT] tags. Say: "Real-world feedback from your next client will tell you more than another editing round."

---

## Pre-Delivery Checklist

- [ ] All four components present (welcome emails, questionnaire, kickoff agenda, communication guidelines)
- [ ] Emails tailored to user's service type, tools, and team structure
- [ ] Questionnaire has 15-20 questions max with service-specific sections
- [ ] Kickoff agenda has time allocations, topic owners, and outcomes
- [ ] Communication guidelines specify response times, channels, cadence, feedback windows, and escalation
- [ ] No unfilled placeholders remain
- [ ] Email sequence spans 5-7 days (not all on Day 0)
- [ ] System matches team size (solo-friendly if applicable)
- [ ] README includes onboarding timeline and usage instructions
