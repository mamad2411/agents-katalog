---
name: highlight-action-items
description: "Place actionable next steps prominently and distinguish owners, deadlines, and unresolved dependencies."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["action-items", "task-management", "top-loading", "productivity", "executive-brief", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Highlight Action Items at the Top (Top-Loaded Next Steps) (AI Skill)

## Overview
When an AI generates an analysis or meeting recap, it naturally places next steps at the very bottom (*"In conclusion, we should remember to..."*). When executives or team members skim the message on mobile, the actionable tasks are buried beneath paragraphs of context and easily missed.

The **Top-Loaded Action Item Protocol** inverts this structure: force the model to render a bold, prioritized **Action Item Callout Block** at the very top of the response, followed by the supporting analysis.

---

## Buried Actions vs. Top-Loaded Clarity

```
┌─────────────────────────────────────────────────────────────┐
│                 Buried vs. Top-Loaded Layout                │
│                                                             │
│  Buried at Bottom (Standard AI Response):                   │
│  • 4 paragraphs of background context & analysis            │
│  • Skimmed and forgotten by busy teammates                  │
│  • "Oh by the way, Dave needs to deploy by 5 PM"            │
│                                                             │
│  Top-Loaded Next Steps (The Action-First Protocol):         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ ⚡ TOP PRIORITY ACTIONS (Review in 5 Seconds):        │  │
│  │ 1. [DAVE] Deploy hotfix to staging by 3:00 PM EST     │  │
│  │ 2. [LISA] Ping client to confirm SLA waiver by 4:00 PM│  │
│  └───────────────────────────────────────────────────────┘  │
│  • Followed below by supporting context and data tables     │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Top-Loaded Action Prompt Templates

### Pattern 1: The Top-Loaded Executive Action Directive
Use for project recaps, strategy documents, or incident analyses:

```markdown
Analyze the attached project notes / incident log: [INSERT TEXT].

Response Structure Requirements:
1. **SECTION 1: IMMEDIATE ACTION ITEMS (Top-Loaded)**:
   Place at the very beginning inside a Markdown callout or bold numbered list:
  - Format: `[ ] [OWNER] - [EXACT TASK] (Deadline: [TIME / DATE])`
2. **SECTION 2: EXECUTIVE SUMMARY (Max 3 bullets)**
3. **SECTION 3: SUPPORTING ANALYSIS & CONTEXT**

Do NOT bury action items at the end of the response.
```

---

### Pattern 2: The Fast Slack Sync Format

```markdown
Turn these notes into a team update ready for Slack:
- Begin with a 3-item "🚨 REQUIRED ACTIONS BY TODAY" section tagging `@Owner`.
- Follow with a short 2-bullet background context.
```

---

## Real-World Case Study

### Scenario: Post-Incident Outage Summary

#### Default AI Output (Actions Buried at End)
> *"At 14:22 UTC, our primary database CPU spiked to 100% due to an un-indexed query on the orders table. The on-call engineer restarted the replica, which mitigated the issue by 14:45 UTC. We lost approximately $4,200 in cart checkouts during the window. Moving forward, the backend team should remember to add indexes to the foreign keys, and DevOps should configure Prometheus alert thresholds before Friday..."*
> 
> ❌ *(The critical task of adding indexes and setting up alerts is buried in a wall of text).*

#### Top-Loaded Action Protocol Output

> ### ⚡ IMMEDIATE ACTION ITEMS (Priority Post-Mortem Tasks)
> - [ ] **[BACKEND - DAVE]** Add composite index on `orders(customer_id, created_at)` and deploy to production *(Deadline: Today, 5:00 PM UTC)*.
> - [ ] **[DEVOPS - LISA]** Lower Prometheus database CPU alert threshold from 95% to 80% *(Deadline: Tomorrow, 12:00 PM UTC)*.
> - [ ] **[FINANCE - MARK]** Issue credit vouchers for the 14 affected customer checkout carts *(Deadline: Thursday, 5:00 PM UTC)*.
> 
> ---
> 
> ### 📊 Incident Breakdown & Root Cause
> - **Outage Duration**: 23 minutes (14:22 - 14:45 UTC).
> - **Financial Impact**: ~$4,200 in delayed checkouts (all orders recoverable).
> - **Root Cause**: Table scan on 12M rows triggered by a missing index on the checkout webhook query.

---

## Key Benefits
- 🎯 **100% Task Visibility**: Team members see their names and tasks in the first 2 inches of screen space.
- 📱 **Mobile Optimized**: Reviewers reading on phones never need to scroll to know what they are accountable for.
- ⏱️ **Instant Meeting Follow-Up**: Copy the top block straight into Slack or Jira in 2 seconds.
