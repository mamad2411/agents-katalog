---
name: workshop-handout
description: "Creates workshop handout materials with exercises, reference sheets, templates, and post-workshop action items."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Workshop Handout

## When to Use This Skill

Use this skill when you need to:
- Create handout materials for a live or virtual workshop
- Build exercise worksheets, reference sheets, and templates for participants
- Design post-workshop action plans that extend learning beyond the session
- Produce printable or digital companion documents for training events

**DO NOT** use this skill for full course materials, slide decks, or standalone workbooks. This is for supplementary handout materials that accompany a live workshop.

---

## Core Principle

A WORKSHOP HANDOUT IS NOT A TRANSCRIPT OF YOUR TALK — IT IS THE TOOL PARTICIPANTS USE DURING THE SESSION AND THE REFERENCE THEY KEEP AFTER, CONTAINING ONLY WHAT THEY NEED TO DO THE EXERCISES AND IMPLEMENT THE LEARNING.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Workshop topic** | "What is the workshop about?" | No default — must be provided |
| **Workshop duration** | "How long is the session?" | 90 minutes |
| **Key exercises** | "What hands-on activities will participants do during the workshop?" | No default — must be provided |
| **Audience** | "Who is attending and what do they already know?" | Solopreneurs, beginner level |
| **Format** | "Printable PDF, digital fillable, or both?" | Digital fillable PDF |

**GATE: Confirm the brief before proceeding.**

---

## Phase 2: Structure

### Handout Architecture

```
1. Cover page — workshop title, date, facilitator name, logo
2. Agenda overview — session flow with timing
3. Key concepts — reference definitions and frameworks (one page max)
4. Exercise worksheets — one per hands-on activity
5. Templates — fill-in tools participants use during or after
6. Resource list — recommended tools, books, links
7. Action plan — post-workshop implementation steps
8. Notes page — blank space for personal notes
```

### Exercise Worksheet Design

Each exercise gets its own page:

```
## Exercise [N]: [Title]
**Time:** [X minutes]
**Objective:** [What participants will produce]

### Instructions
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Workspace
[Fill-in area with prompts, boxes, or lines]

### Example
[Completed example showing what good output looks like]
```

**GATE: Present the handout structure for approval.**

---

## Phase 3: Write

### Content Rules

- **White space is essential** — handouts need room for writing, not wall-to-wall text
- **Instructions must stand alone** — a participant who zones out for 30 seconds should be able to read the handout and catch up
- **One exercise per page** — never split an exercise across pages
- **Reference content is minimal** — only include what is needed during the session, not everything you know about the topic
- **Templates are pre-formatted** — provide structure (headers, labels, boxes) not blank pages

### Key Concepts Page

Limit to 5-8 concepts maximum:

```
| Concept | Definition | When to Use |
|---------|-----------|-------------|
| [Term] | [One sentence] | [Context] |
```

### Post-Workshop Action Plan

```
## Your 7-Day Action Plan

**Today:** [One immediate action to take while motivation is high]
**This week:**
- [ ] [Action 1 — specific and measurable]
- [ ] [Action 2]
- [ ] [Action 3]
**This month:** [Bigger implementation goal]
**Need help?** [Contact info or community link]
```

---

## Phase 4: Polish

### 1. Print-Ready Check

```
- [ ] All pages work in black and white (no color-dependent elements)
- [ ] Font size is 11pt minimum for body, 14pt for headers
- [ ] Margins are at least 0.75 inches for binding or hole-punching
- [ ] Exercise worksheets have adequate fill-in space
- [ ] Page count is reasonable (target: 8-15 pages for a 90-min workshop)
```

### 2. Digital Optimization

- Fillable form fields for all exercise areas
- Clickable links in the resource section
- Bookmarked sections for easy navigation
- File size under 5MB for easy email distribution

### 3. Facilitator Notes

Provide a separate facilitator version with:
- Timing cues for each exercise
- Answers or example outputs for exercises
- Common participant questions and responses
- Transition scripts between sections

---

## Example 1: "Build Your Content Calendar" Workshop (2 hours)

```
Handout contents:
- Content pillar brainstorm worksheet
- Monthly calendar template (fill-in grid)
- Headline formula reference sheet
- Platform-specific posting guide (one page)
- 30-day action plan
```

## Example 2: "Price Your Services" Workshop (90 min)

```
Handout contents:
- Cost calculation worksheet
- Competitor research template
- Value-based pricing formula reference
- Price presentation script template
- Implementation checklist
```

---

## Anti-Patterns

- **Information overload** — cramming everything you know onto the handout overwhelms participants. Curate ruthlessly.
- **No fill-in space** — a handout with no room to write is a brochure, not a working tool.
- **Exercises without examples** — participants freeze when they do not know what "done" looks like.
- **No post-workshop action items** — the handout's value drops to zero if it goes into a drawer after the session.
- **Tiny fonts to fit more content** — if you need to shrink the font, you need to cut content instead.
- **Color-dependent designs** — many participants print in black and white. Design accordingly.

---

## Recovery

- **User has no defined exercises:** Ask "What should participants walk away having created?" Work backward from the deliverable to design 2-3 exercises.
- **Workshop is too short for a full handout:** Create a one-page reference sheet plus a post-workshop action email instead.
- **User wants to include everything from the talk:** Limit to concepts that participants need to reference during exercises. Everything else can go in a follow-up email.
- **Digital-only audience:** Skip print formatting. Use a Notion page or Google Doc with interactive elements instead of PDF.
