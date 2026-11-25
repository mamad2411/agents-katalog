---
name: retrospective
description: Facilitates project and sprint retrospectives using structured frameworks like Start/Stop/Continue, 4Ls, and Sailboat, producing actionable improvement plans with owners and deadlines. Use when a user wants to learn from a completed project, improve team processes, run a post-mortem, or reflect on what went well and what did not after any initiative.
allowed-tools: Read Write Bash(mkdir:*)
---

# Retrospective

## When to Use This Skill

- User just finished a project, launch, sprint, or initiative and wants to reflect
- User says "retrospective" or "retro" or "post-mortem" or "lessons learned" or "what went wrong"
- User wants to improve their process for next time
- User is running a team retro and needs a framework and facilitator guide
- User is a solopreneur reflecting on a quarter, campaign, or client engagement

## Core Principle

A RETROSPECTIVE IS NOT A BLAME SESSION — IT IS A LEARNING SESSION. Every output must end with SPECIFIC ACTIONS that have OWNERS and DEADLINES. Insights without action items are just venting.

## Workflow

### Phase 1: Choose the Framework

Select the right retrospective framework based on context:

| Framework | Best For | Duration | Complexity |
|-----------|----------|----------|------------|
| **Start/Stop/Continue** | Quick retros, small teams, solopreneurs | 30 min | Low |
| **4Ls** (Liked/Learned/Lacked/Longed For) | Emotional processing, creative teams | 45 min | Medium |
| **Sailboat** | Visual thinkers, identifying blockers vs drivers | 45 min | Medium |
| **5 Whys** | Single-issue deep dives, incident post-mortems | 30 min | Low |
| **Timeline** | Long projects (3+ months), complex initiatives | 60 min | High |

Default to **Start/Stop/Continue** unless the user specifies otherwise or the context calls for a different framework.

### Phase 2: Set the Context

Gather from the user:

1. **What is being reviewed?** (project, sprint, quarter, campaign, client engagement)
2. **Time period?** (start and end dates)
3. **Who was involved?** (solo, team, client + team)
4. **What was the original goal?** (what were you trying to achieve)
5. **Was the goal achieved?** (fully, partially, not at all)
6. **What are you hoping to get from this retro?** (improve process, prevent repeats, celebrate wins)

### Phase 3: Run the Retrospective

**Framework 1: Start/Stop/Continue**

```
START / STOP / CONTINUE RETROSPECTIVE
=======================================
Project: [Name]
Period: [Start] to [End]
Goal: [Original goal]
Outcome: [Achieved / Partially / Not achieved]

START (things we should begin doing):
1. [Action we did not do but should have]
2. [New practice to adopt]
3. [Missing process that caused problems]

STOP (things we should stop doing):
1. [Activity that wasted time or caused harm]
2. [Habit or pattern that did not work]
3. [Process that added friction without value]

CONTINUE (things that worked and we should keep):
1. [Practice that contributed to success]
2. [Tool or process that saved time]
3. [Behavior or habit worth reinforcing]
```

**Framework 2: 4Ls**

```
4Ls RETROSPECTIVE
==================
Project: [Name]

LIKED (what went well, what we enjoyed):
1. [Positive experience or outcome]
2. [Something that felt good during the process]

LEARNED (new insights or knowledge gained):
1. [Something we now know that we didn't before]
2. [Skill or capability developed]

LACKED (what was missing or insufficient):
1. [Resource, information, or support that was absent]
2. [Process or tool gap]

LONGED FOR (what we wished we had):
1. [Ideal state or resource that would have helped]
2. [Change that would improve next time]
```

**Framework 3: Sailboat**

```
SAILBOAT RETROSPECTIVE
========================
Project: [Name]

WIND (what propelled us forward):
1. [Force or factor that accelerated progress]
2. [Tailwind we should harness again]

ANCHOR (what held us back):
1. [Blocker or drag on progress]
2. [Friction that slowed us down]

ROCKS (risks or dangers we hit or avoided):
1. [Problem that materialized]
2. [Risk we navigated successfully]

ISLAND (our destination — where we're heading):
1. [The vision or goal for next time]
2. [What success looks like going forward]
```

**Framework 4: 5 Whys (for single-issue deep dives)**

```
5 WHYS ANALYSIS
================
Issue: [The specific problem that occurred]

Why 1: Why did [problem] happen?
  Because: [First-level cause]

Why 2: Why did [first-level cause] happen?
  Because: [Second-level cause]

Why 3: Why did [second-level cause] happen?
  Because: [Third-level cause]

Why 4: Why did [third-level cause] happen?
  Because: [Fourth-level cause]

Why 5: Why did [fourth-level cause] happen?
  Because: [ROOT CAUSE]

ROOT CAUSE: [The fundamental issue to address]
FIX: [Specific action to prevent recurrence]
```

### Phase 4: Extract Action Items

Every retrospective must produce action items in this format:

```
ACTION ITEMS
=============

Priority | Action                           | Owner    | Deadline   | How We'll Know It's Done
---------|----------------------------------|----------|------------|------------------------
HIGH     | [Specific action from retro]     | [Name]   | [Date]     | [Observable outcome]
HIGH     | [Specific action from retro]     | [Name]   | [Date]     | [Observable outcome]
MEDIUM   | [Specific action from retro]     | [Name]   | [Date]     | [Observable outcome]
LOW      | [Specific action from retro]     | [Name]   | [Date]     | [Observable outcome]

REVIEW DATE: [When to check if actions were completed — 2 weeks out]
```

Rules for action items:
- Maximum 5 action items per retro (more than 5 means nothing gets done)
- Every action has an owner (even for solo retros — "me" is valid)
- Every action has a deadline within 30 days
- Every action has a success criterion (how do you know it is done)

### Phase 5: Document and Close

Save the retrospective in a clean format and provide a closing summary:

```
RETROSPECTIVE SUMMARY
======================
Project: [Name]
Date of Retro: [Date]
Participants: [Names]

ONE-LINE VERDICT: [Single sentence capturing the overall takeaway]

TOP WIN: [The best thing that happened]
TOP LESSON: [The most important thing learned]
TOP ACTION: [The highest-priority change to make]

Full retro document: [saved to file]
Action item review date: [Date]
```

## Example 1: Solopreneur — Post-Launch Retrospective

**Context:** Dana launched a $297 digital course. Goal was 50 sales in the first week. Actual: 23 sales ($6,831 revenue).

```
START / STOP / CONTINUE RETROSPECTIVE
=======================================
Project: "Content Systems" Course Launch
Period: Jan 6 - Jan 19, 2026
Goal: 50 sales in launch week ($14,850 revenue)
Outcome: 23 sales ($6,831) — 46% of target

START:
1. Build a waitlist 60 days before launch (not 14 days).
   Only had 340 email subscribers at launch. Industry
   benchmark is 2-5% conversion, so 340 subs = 7-17 sales max.
   Hit 23 because of social, but email was underbuilt.
2. Create a dedicated sales page earlier. Used a Gumroad
   listing for the first 3 days. Conversion jumped from 1.2%
   to 3.8% after moving to a proper sales page on Day 4.
3. Record video testimonials from beta testers BEFORE launch.
   Had 6 beta testers who loved it but only got 2 written
   testimonials. Video would have been much more compelling.

STOP:
1. Launching on a Monday. Open rates were lowest Mon-Tue.
   Best engagement came Wed-Thu. Launch next time on Tuesday
   evening so the big push hits Wednesday inboxes.
2. Sending 6 emails in 5 days. Got 12 unsubscribes (3.5%
   of list). Scale back to 4 emails over 7 days.
3. Spending launch week creating bonus content. Should have
   been 100% on promotion. Bonuses should be done pre-launch.

CONTINUE:
1. Instagram Stories countdown — generated 35% of traffic
   to sales page. Stories with face-to-camera performed 3x
   better than graphics-only.
2. Early-bird pricing ($247 for first 48 hours). 14 of 23
   sales came in the first 48 hours. Urgency worked.
3. DM outreach to warm contacts. Sent 40 personalized DMs.
   8 converted (20% conversion). Highest-converting channel.

ACTION ITEMS
=============

Priority | Action                                      | Owner | Deadline   | Done When
---------|---------------------------------------------|-------|------------|-------------------
HIGH     | Start building waitlist for next launch      | Dana  | Feb 15     | Landing page live, lead magnet active
HIGH     | Build proper sales page template (reusable)  | Dana  | Feb 28     | Template in WordPress, tested on mobile
HIGH     | Collect 4 video testimonials from buyers     | Dana  | Mar 1      | 4 videos recorded, edited, on sales page
MEDIUM   | Create email launch sequence (4 emails/7 day)| Dana  | Mar 15     | Sequence drafted in ConvertKit
LOW      | Test Tuesday evening launch timing           | Dana  | Next launch| Open rate data compared to Monday launch

REVIEW DATE: March 1, 2026

RETROSPECTIVE SUMMARY
======================
ONE-LINE VERDICT: The product was validated but the launch infrastructure was underbuilt — email list too small, sales page too late, and promotion calendar too compressed.

TOP WIN: DM outreach converted at 20% — highest ROI channel by far
TOP LESSON: Launch success is determined 60 days before launch day, not during launch week
TOP ACTION: Start the next waitlist now, aiming for 1,000 subscribers before opening cart
```

## Example 2: Agency Team — Sprint Retrospective

**Context:** A 4-person marketing agency just finished a 2-week sprint delivering a rebrand for a client. Deadline was met but the team worked overtime.

```
SAILBOAT RETROSPECTIVE
========================
Project: TechFlow Rebrand Sprint
Period: Jan 27 - Feb 7, 2026
Team: James (lead), Sara (design), Mike (copy), Lin (dev)
Goal: Deliver full rebrand (logo, guidelines, website) in 2 weeks
Outcome: Delivered on time, client approved with minor revisions.
         Team worked 15+ hrs overtime total.

WIND (what propelled us forward):
1. Daily 15-min standups kept everyone aligned. Zero
   miscommunication on deliverables after Day 3.
2. Sara's design system approach — created reusable
   components on Day 2, which saved 6+ hours on website
   mockups later in the sprint.
3. Client was responsive. Average feedback turnaround
   was 4 hours (vs. typical 24-48 hours).

ANCHOR (what held us back):
1. Scope was unclear for the first 3 days. The brief said
   "rebrand" but didn't specify: logo refresh or full redesign?
   Website pages: 5 or 12? Lost 8 hours to rework after
   clarification on Day 3.
2. Mike started copywriting before Sara finalized the brand
   voice. Had to rewrite 40% of website copy when tone shifted
   from "corporate" to "approachable." Wasted 5 hours.
3. No one owned the timeline. James assumed Lin was tracking
   milestones. Lin assumed James was. Deadlines were vague
   until Day 5 panic.

ROCKS (risks we hit):
1. Lin got sick on Day 8-9. No backup developer. Website
   build stalled for 2 days, forcing overtime in the final
   3 days to catch up.
2. Client added 3 additional pages on Day 6 ("can you also
   do the blog and careers page?"). James said yes without
   adjusting the timeline. This added 6 hours of unplanned work.

ISLAND (where we're heading):
1. Every sprint starts with a locked scope document signed
   by the client. No mid-sprint additions without timeline
   extension.
2. Dependency mapping: copy waits for brand voice, dev waits
   for approved mockups. No parallel work on dependent tasks.

ACTION ITEMS
=============

Priority | Action                                      | Owner | Deadline   | Done When
---------|---------------------------------------------|-------|------------|---------------------
HIGH     | Create sprint kickoff template with scope    | James | Feb 14     | Template in Notion, used on next project
         | lockdown checklist                           |       |            |
HIGH     | Add dependency map to project setup:         | James | Feb 14     | Dependency chart added to Asana template
         | brand voice > copy, mockups > dev            |       |            |
HIGH     | Assign timeline owner explicitly at kickoff  | James | Feb 14     | Role listed in kickoff template
MEDIUM   | Cross-train Lin and Sara on basic dev tasks   | Lin   | Mar 1      | Sara can push content updates to staging
MEDIUM   | Add scope change process: new request =       | James | Feb 21     | Process documented, shared with clients
         | new timeline discussion, not automatic yes   |       |            |

REVIEW DATE: February 21, 2026

RETROSPECTIVE SUMMARY
======================
ONE-LINE VERDICT: We delivered, but overtime was caused by preventable issues — unclear scope, wrong task sequencing, and no change management process.

TOP WIN: Daily standups and Sara's component system saved the sprint from being late
TOP LESSON: Scope must be locked before work begins — "yes" to a client mid-sprint costs the team hours
TOP ACTION: Create a sprint kickoff template that locks scope, maps dependencies, and assigns a timeline owner
```

## Recovery and Fallback

- If the user is doing a solo retro and feels awkward talking to themselves, frame it as a written exercise: "Write your answers, I'll organize and challenge them"
- If the team is defensive or blaming, redirect: "We're analyzing the process, not the people. What in our PROCESS allowed this to happen?"
- If the retro produces more than 5 action items, force-rank them and keep only the top 5. Say: "If we could only fix 3 things, which 3 would prevent the most pain?"
- If the user says "everything went fine," probe deeper: "What would you do differently if you had to do it again with half the time?" and "What almost went wrong but didn't?"
- If the user has never run a retro before, default to Start/Stop/Continue (simplest framework) and keep it to 30 minutes

## Constraints

- **NEVER produce a retro without action items** — insights without actions are just complaints
- **ALWAYS limit action items to 5 maximum** — more than 5 guarantees none get done
- **ALWAYS include a review date** — action items without follow-up accountability decay within days
- **ALWAYS include owners and deadlines** for every action item
- Default to Start/Stop/Continue unless specified otherwise
- Keep the retro document under 2 pages
- For team retros, include a facilitator guide with timing
- Never assign blame to individuals — analyze processes and systems
- Include at least one "CONTINUE" or "WIN" — retros that are 100% negative demoralize teams
