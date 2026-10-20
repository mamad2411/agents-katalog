---
name: hackathon-in-a-box
description: Generate a tailored hackathon planning kit for customer organizers. Produces an organizer guide, agenda, participant guide, invite emails, use case prompts, judging rubric, and logistics checklist — all personalized to the customer's industry and goals.
user-invocable: true
model: opus
---

# Hackathon in a Box

Guided conversation that generates a complete, customer-branded hackathon planning kit. The output is designed for **customer organizers** who have never run a hackathon — not for the SA.

## Important

- All generated content is **customer-facing**. Do not include Databricks internal jargon, UCO references, SFDC stages, or SA playbook language.
- Personalize every document with the customer's company name, industry context, and specific goals.
- Keep the tone professional but energizing — this should make the organizer excited to run the event.

## Workflow

This is a **guided, multi-step conversation**. Complete each phase before moving to the next. Confirm with the user before generating each deliverable.

---

### Phase 1: Discovery

Gather the following information from the user. Ask conversationally — do not dump all questions at once. Group into 2-3 natural exchanges.

**Round 1 — Basics:**
- Customer / account name
- Industry vertical (e.g., financial services, healthcare, retail, manufacturing, energy, tech)
- Who is the customer-side organizer? (role, name if known)
- Hackathon duration: half-day (3-4 hrs), full-day (6-8 hrs), or multi-day (1.5-2 days)

**Round 2 — Focus & Audience:**
- Focus areas: AI agents, ML/data science, analytics/BI, data engineering, or open/mixed
- Expected number of participants (10-20, 20-40, 40+)
- Participant skill mix: mostly technical, mostly business, or mixed
- Databricks maturity: new (< 6 months), intermediate (6-18 months), or advanced (18+ months)

**Round 3 — Goals & Context:**
- What does the customer want to get out of the hackathon? (upskilling, POC acceleration, innovation, team building, executive visibility)
- Any specific problems or use cases they want teams to work on?
- Any constraints? (virtual vs. on-site, specific dates, budget concerns, workspace access)

After gathering all inputs, summarize the hackathon profile back to the user and confirm before proceeding.

---

### Phase 2: Generate Deliverables

Generate each deliverable one at a time. After each, ask: **"Does this look good, or would you like me to adjust anything before we move on?"**

Load the reference templates before generating:

```
Read: plugins/fe-workflows/skills/hackathon-in-a-box/resources/deliverable_templates.yaml
```

#### Deliverable 1: Organizer's Guide

A step-by-step guide for the customer organizer covering:

**Before the Hackathon (2-4 weeks out):**
- Define success criteria with stakeholders
- Secure executive sponsor
- Book venue / set up virtual platform
- Form planning committee (recommend 1 organizer per 15 participants)
- Set up communication channels (Slack/Teams channel, email list)
- Recruit mentors (internal + Databricks SMEs)
- Prepare workspace: clusters, datasets, starter notebooks
- Test participant access — zero build time lost on setup

**One Week Before:**
- Finalize teams or team formation strategy
- Send logistics email to all participants
- Run tech dry-run (workspace access, projector, wifi)
- Prepare printed materials (schedule, wifi info, judging criteria)
- Confirm food/beverage arrangements

**Day-Of Execution:**
- Kickoff: 30 min max — goals, teams, confirm access
- Building phase: circulate, unblock, guide toward success criteria
- Checkpoints at 1hr, midpoint, and 1hr before demos
- Demos: strict 5-min per team, working code only (no slides)
- Wrap-up: identify which prototypes advance, schedule follow-ups on the spot

**After the Hackathon:**
- Send thank-you email with highlights and photos
- Circulate survey within 24 hours
- Identify top prototypes for continued development
- Schedule follow-up sessions within 2 weeks
- Share success stories with leadership

#### Deliverable 2: Agenda / Run of Show

Generate a detailed, time-blocked agenda tailored to the chosen duration. Include:
- Session names, durations, and descriptions
- Who leads each session (organizer, Databricks, team leads)
- Break times, meals, and energy management
- Checkpoint moments and demo prep time

Adapt format based on duration:
- **Half-day (3-4 hrs):** Compressed — 15-min kickoff, 2-2.5 hrs build, 30-min demos
- **Full-day (6-8 hrs):** Full cycle — kickoff, ideation, build, checkpoint, build, demos, wrap-up
- **Multi-day (1.5-2 days):** Day 1: ideation + initial build. Day 2: build + demos + awards

#### Deliverable 3: Participant Guide

Written for hackathon attendees. Include:
- What is a hackathon (for first-timers) — keep it welcoming and low-pressure
- What to expect and what to bring
- How teams will be formed
- Available tools and platform access (Databricks workspace, datasets, starter notebooks)
- Tips for success: scope small, build an MVP, ask mentors for help early
- Demo format and time limits
- FAQ section

#### Deliverable 4: Communication Templates

Generate three email templates:

**a) Executive Sponsor Invite**
- Frame the hackathon as strategic investment in innovation
- Highlight expected outcomes (prototypes, upskilling, team building)
- Ask for visible sponsorship (opening remarks, judging panel, awards)
- Keep to 150-200 words

**b) Participant Invite**
- Exciting but informative — what, when, where, why
- Emphasize: no prior Databricks experience required (if maturity is low)
- Include registration link placeholder
- Keep to 200-250 words

**c) Week-Before Reminder**
- Logistics: time, location/link, what to bring
- Team assignments or team formation process
- Pre-work if any (account setup, reading materials)
- Contact info for questions
- Keep to 150-200 words

#### Deliverable 5: Use Case Prompts

Generate 3-5 industry-specific problem statements scoped to the hackathon duration. Each prompt includes:
- **Problem title** — clear and compelling
- **Business context** — why this matters (2-3 sentences)
- **Challenge statement** — what teams should build
- **Available data** — what datasets will be provided or can be used
- **Success criteria** — what a good demo looks like
- **Stretch goals** — for advanced teams

If the user provided specific use cases, incorporate those. Otherwise, generate prompts relevant to their industry and focus areas.

#### Deliverable 6: Judging Rubric

A scoring rubric with 5-6 criteria. Default criteria (customize based on goals):

| Criteria | Weight | Description |
|----------|--------|-------------|
| Business Impact | 25% | Does the solution address a real business problem? |
| Technical Execution | 25% | Is the prototype working? Is the code clean? |
| Innovation | 20% | Is the approach creative or novel? |
| Feasibility | 15% | Could this be deployed to production? |
| Presentation | 10% | Was the demo clear and compelling? |
| Collaboration | 5% | Did all team members contribute? |

Include a 1-5 scoring scale with descriptions for each level.

#### Deliverable 7: Logistics Checklist

A printable checklist organized by timeline:

- **4 weeks out:** Venue, budget, exec sponsor, dates
- **2 weeks out:** Workspace setup, datasets, mentor recruitment, communication plan
- **1 week out:** Tech dry-run, team formation, catering, printed materials
- **Day before:** Venue walk-through, signage, power strips, wifi test
- **Day of:** Registration table, name tags, projector check, food setup
- **Day after:** Survey, thank-you email, photo sharing, follow-up scheduling

---

### Phase 3: Package and Deliver

After all deliverables are approved:

1. Write each deliverable to a separate markdown file in `/tmp/hackathon-kit-<customer>/`:
   - `01-organizers-guide.md`
   - `02-agenda.md`
   - `03-participant-guide.md`
   - `04-email-templates.md`
   - `05-use-case-prompts.md`
   - `06-judging-rubric.md`
   - `07-logistics-checklist.md`

2. Tell the user the file paths and offer to:
   - Adjust any specific section
   - Convert to Google Docs for sharing (using the google-docs skill)
   - Generate a slide deck version of the agenda (using the google-slides skill)

---

## Reference Materials

The following internal Databricks resources informed this skill's best practices. These are for the SA's reference — do not share with customers or include in generated content:

- [Hackathon Workshop (Confluence)](https://databricks.atlassian.net/wiki/spaces/FE/pages/6005030992) — FY27 GTM play, module recipes, field takeaways
- [Hackathon in a Box (Confluence)](https://databricks.atlassian.net/wiki/spaces/~62834faabd640f0068acf90f/pages/3142910873) — Original datathon framework, judging criteria, grouping advice
- [Hackathon Guide (Confluence)](https://databricks.atlassian.net/wiki/spaces/~798274034/pages/4960387116) — Comprehensive event planning guide
- [Hackathon-in-a-Box Sales Guide](https://docs.google.com/presentation/d/1sIEiamGl8j8xWdWYRZIp2ItNQh12fieL2fDWKzmjO48) — Positioning and sales enablement
- [Hackathon Playbook](https://docs.google.com/presentation/d/1nXvToSdHUG48CmRqnAK2_hunLm_j7P--1WE1vktJiUw) — Example content and participant framing
- [IH-Hackathon-DeliveryGuide](https://docs.google.com/document/d/18JAT3hYxKg6rO7OET8mvHDtDl5ffn4OnIq_vLDtV9r0) — Ideation session + delivery framework
