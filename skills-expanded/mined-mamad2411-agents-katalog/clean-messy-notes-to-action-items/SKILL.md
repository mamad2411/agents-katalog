---
name: clean-messy-notes-to-action-items
description: "Turn unstructured notes into action items with owners, deadlines, decisions, and unresolved follow-ups."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["meeting-notes", "action-items", "task-management", "productivity", "organization", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Turn Messy Notes into Assigned Action Items (AI Skill)

## Overview
During fast-paced meetings or brainstorming sessions, notes are scribbled in fragments (*"Dave check billing API, push release fri, talk to sarah re budget?"*). Leaving notes in this state leads to dropped tasks and confusion.

The **Action Item Parser Protocol** ingests raw, unformatted notes and separates them into 3 clean, unambiguous buckets: **Key Decisions Made**, **Assigned Action Items** (with strict ownership and deadlines), and **Open Questions**.

---

## The 3-Bucket Parser Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 The Action-Item Parser                      │
│                                                             │
│  [ RAW FRAGMENTED NOTES & SCRIBBLINGS ]                     │
│                           │                                 │
│                           ▼                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 1. DECISIONS: What was agreed on? (No action needed)  │  │
│  │ 2. ACTION ITEMS: [WHO] + [WHAT] + [BY WHEN] + [DOD]   │  │
│  │ 3. OPEN QUESTIONS: What is blocked or unowned?        │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Note Cleanup Prompt Templates

### Pattern 1: The Standard Action-Item Parser
Use this for team meetings, client calls, and sprint standups:

```markdown
Here are my raw, unedited meeting notes:
[PASTE RAW NOTES]

Parse these notes into the following 3 structured sections:

### 1. Key Decisions Made
- Bulleted list of final decisions agreed upon.

### 2. Action Items Table
Create a Markdown table with the following columns:
| Task / Deliverable | Owner | Deadline | Priority (P0 / P1 / P2) | Definition of Done |

### 3. Open Questions & Blockers
- Bulleted list of unresolved issues requiring follow-up.

Rules:
- If an owner or deadline is not explicitly named, label as `[UNASSIGNED]` or `[TBD]`.
- Convert vague verbs ("look into", "check") into concrete action deliverables ("Review API logs and document error rates").
```

---

### Pattern 2: The 60-Second Slack Sync Generator
Use to generate an instant team recap ready to paste into Slack:

```markdown
Convert these notes into a 5-line Slack recap message:
- Header with meeting topic & date
- 3 key takeaways
- Numbered action items tagging `@Owner`
- Next sync date
```

---

## Real-World Case Study

### Scenario: Product Team Sync Notes

#### The Raw Scribbled Notes
> *"talked with UX team. decided to kill the multi-step checkout and do 1-page. Dave needs to fix Stripe webhooks by thursday. Lisa updating figma designs by tomorrow noon so dev can start. we still dont know if marketing is ready with new copy? launch next monday maybe?"*

#### Parsed Output (Structured & Accountable)

### 1. Key Decisions Made
- **Checkout Flow**: Approved switch from multi-step checkout to a single-page checkout for the Q3 release.

### 2. Action Items Table
| Task / Deliverable | Owner | Deadline | Priority | Definition of Done |
| :--- | :--- | :--- | :--- | :--- |
| **Update Figma Checkout Designs** | Lisa | Tomorrow (12:00 PM) | P0 | Figma prototype updated and handed off to engineering team. |
| **Fix Stripe Webhook Handlers** | Dave | Thursday (5:00 PM) | P0 | Staging webhooks handle race conditions with zero 500 errors. |
| **Confirm Marketing Copy Readiness**| `[UNASSIGNED]` | Friday | P1 | Final checkout copy submitted and approved. |

### 3. Open Questions & Blockers
- **Marketing Copy Owner**: Who from marketing is providing the checkout micro-copy?
- **Launch Date Confirmation**: Target launch is Monday, pending confirmation of marketing copy and Dave's Thursday webhook fix.

---

## Benefits
- ⏱️ **Zero Dropped Balls**: Never lose an action item in disorganized notes again.
- 🎯 **Total Accountability**: Every task has a single owner and an explicit deadline.
- ⚡ **Instant Post-Meeting Recap**: Send the summary to your team 30 seconds after the call ends.
