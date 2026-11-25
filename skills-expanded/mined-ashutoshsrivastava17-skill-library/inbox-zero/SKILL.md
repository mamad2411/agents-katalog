---
name: inbox-zero
description: >
  Implement inbox zero workflows including triage rules, folder and label
  systems, response templates, delegation criteria, and processing schedules
  to keep email and messages under control permanently.
  TRIGGER when: user says /inbox-zero, "clean up my inbox", "too many emails",
  "email management", "inbox overload", "I have thousands of unread emails",
  or "help me manage my email".
argument-hint: "[email volume, role, or specific pain points]"
user-invocable: true
---

# Inbox Zero

You are an email productivity specialist helping people take permanent control of their inbox. Design a complete inbox zero system: triage rules, organization structure, response templates, delegation criteria, and sustainable processing habits.

## Process

### Step 1: Assess the Current State

Understand the scale of the problem before designing the system:

| Assessment Item | How to Determine |
|---|---|
| Current inbox count | Total unread and read messages sitting in the inbox |
| Daily incoming volume | Average emails received per day (check over last 30 days) |
| Daily sent volume | Average emails sent per day |
| Time spent on email | Estimated hours per day processing email |
| Email types breakdown | What percentage is actionable, FYI, automated, spam/noise |
| Accounts managed | Number of email accounts (work, shared, alias) |
| Other inboxes | Slack DMs, Teams messages, project tool notifications |
| Current organization | Existing folders, labels, rules, or filters |
| Pain points | What specifically about email is the problem (volume, finding things, response time) |

**Email volume classification:**

| Volume | Daily Emails | System Complexity Needed |
|---|---|---|
| Light | Under 30 | Simple: triage + 3-4 folders |
| Moderate | 30-75 | Standard: full folder system + templates + filters |
| Heavy | 75-150 | Advanced: aggressive filtering + delegation + SLA rules |
| Extreme | 150+ | Enterprise: assistant support, auto-routing, multi-pass triage |

### Step 2: Design the Triage System

Every email gets one of five actions. No email stays in the inbox without a decision:

**The 5-Action Triage Framework:**

| Action | Rule | Time Limit | Where It Goes |
|---|---|---|---|
| **Delete/Archive** | Not actionable, not reference-worthy | 2 seconds | Archive or trash |
| **Do** | Takes under 2 minutes to complete | 2 minutes | Reply, then archive |
| **Delegate** | Someone else should handle this | 1 minute | Forward, then move to "Waiting" |
| **Defer** | Takes more than 2 minutes; you must do it | 30 seconds | Move to "Action" with a due date |
| **Designate** | Reference material you may need later | 15 seconds | Move to appropriate reference folder |

**Triage decision tree:**

```
New email arrives
├── Is it spam or irrelevant? → DELETE
├── Is it FYI only, no action needed?
│   ├── Might I need it later? → DESIGNATE (reference folder)
│   └── No future value → ARCHIVE
├── Does it require action?
│   ├── Can someone else do it? → DELEGATE (forward + "Waiting" folder)
│   ├── Can I do it in under 2 minutes? → DO IT NOW → ARCHIVE
│   └── Takes more than 2 minutes → DEFER ("Action" folder + task list)
```

### Step 3: Build the Folder/Label System

Keep the structure minimal. More folders means more decisions and more maintenance:

**Recommended folder structure:**

| Folder/Label | Purpose | Processing Rule |
|---|---|---|
| **Inbox** | Temporary holding only — process to zero | Empty by end of each processing session |
| **@Action** | Emails requiring your action (deferred items) | Review daily; clear within 48 hours |
| **@Waiting** | Emails you are waiting on someone else for | Review 2x per week; follow up if stale |
| **@Read** | Long-form content to read when time allows | Review weekly; delete if unread after 2 weeks |
| **Archive** | Everything that has been processed | Search when needed; never browse |
| **Reference** (optional sub-labels) | Material you will definitely need again | Organize by project or topic if volume warrants |

**Folder design principles:**

| Principle | Rule |
|---|---|
| Fewer is better | Maximum 7 active folders; archive everything else |
| Action-based, not topic-based | Folders describe what to do, not what it is about (search handles topics) |
| No "Miscellaneous" folder | If you cannot name the folder, archive it |
| Review cadence for each folder | Every folder must have a defined review frequency or it becomes a graveyard |
| Archive is the default destination | When in doubt, archive. Search is faster than browsing folders. |

**Label/tag taxonomy (for Gmail or systems supporting labels):**

| Label Category | Labels | Color |
|---|---|---|
| Status | @Action, @Waiting, @Read | Red, Yellow, Blue |
| Priority | P1-Urgent, P2-This-Week, P3-Low | Red, Orange, Gray |
| Project (optional) | Project-X, Project-Y | Green variants |
| Role (optional) | Manager, IC, Committee | Purple variants |

### Step 4: Create Automated Filters and Rules

Reduce triage effort by auto-sorting predictable email:

| Rule | Condition | Action | Example |
|---|---|---|---|
| Auto-archive | From: [automated system], Subject: matches pattern | Skip inbox, apply label, archive | CI/CD notifications, calendar RSVPs |
| Auto-label | From: [specific sender] or To: [specific list] | Apply label, keep in inbox | Emails from your manager get P1 label |
| Newsletter sort | From: [newsletter senders] | Skip inbox, apply "Read" label | Industry newsletters batched for reading |
| Notification filter | From: [tool notifications] | Skip inbox, apply tool label, archive | Jira, GitHub, Confluence notifications |
| VIP filter | From: [CEO, manager, key stakeholders] | Keep in inbox, apply "VIP" label, star | Ensures critical emails are seen first |

**Filter audit checklist:**
- Review filters quarterly; delete stale ones
- Never auto-delete — always auto-archive (you might need it later)
- Test filters with a 1-week trial before trusting them
- Keep a master list of all active filters

**Common high-volume sources to filter:**

| Source | Typical Volume | Recommended Action |
|---|---|---|
| CI/CD pipeline notifications | 20-50/day | Auto-archive; review only on failure |
| Calendar invites and RSVPs | 5-15/day | Auto-archive accepted/declined |
| Jira/ticket updates | 10-30/day | Label by project; skip inbox |
| All-hands/company-wide emails | 1-3/day | Label "FYI"; skip inbox |
| Marketing/newsletter | 5-10/day | Label "Read"; skip inbox |
| Automated reports | 3-10/day | Label "Reports"; skip inbox; review weekly |

### Step 5: Build Response Templates

Reduce time spent composing repetitive replies:

| Template Name | Use Case | Template |
|---|---|---|
| **Acknowledge** | You received it and will respond later | "Thanks for sending this. I'll review and get back to you by [date]." |
| **Delegate** | Forwarding to the right person | "Looping in [name] who owns this area. [Name], could you take a look?" |
| **Decline meeting** | Meeting you should not attend | "Thanks for the invite. I don't think I'd add value here — could you send me the notes/decision afterward?" |
| **Request info** | You need more before you can act | "Before I can move forward, I need: 1) [specific item] 2) [specific item]. Could you share these by [date]?" |
| **Close the loop** | Wrapping up a thread | "This is resolved — [brief summary of outcome]. Archiving this thread. Reopen if needed." |
| **Say no** | Declining a request | "I appreciate you thinking of me. I can't take this on given my current commitments. I'd suggest [alternative person or approach]." |
| **Batch response** | Answering multiple questions | "Answering your questions inline below: [use inline replies]" |

**Template design rules:**
- Keep templates under 3 sentences
- Always include a specific next step or deadline
- Personalize the first line; template the rest
- Store templates in your email client's quick-reply feature, not in your head

### Step 6: Establish Processing Schedules

Define when and how to process email to prevent all-day grazing:

**Processing schedule by volume:**

| Volume | Processing Sessions | Duration Each | Schedule |
|---|---|---|---|
| Light (<30/day) | 2x per day | 15 min | 9:00 AM, 3:00 PM |
| Moderate (30-75/day) | 3x per day | 20 min | 9:00 AM, 12:30 PM, 4:00 PM |
| Heavy (75-150/day) | 3-4x per day | 30 min | 8:30 AM, 11:00 AM, 2:00 PM, 4:30 PM |
| Extreme (150+/day) | 4x per day + delegation | 30-45 min | 8:00 AM, 10:30 AM, 1:30 PM, 4:30 PM |

**Processing session protocol:**

| Step | Action | Time |
|---|---|---|
| 1 | Scan for VIP and urgent emails first | 2 min |
| 2 | Process each remaining email using the 5-Action framework | 1-2 min each |
| 3 | Apply labels, move to folders, archive processed items | Ongoing |
| 4 | Update task list with deferred items | 2 min |
| 5 | Inbox should be at zero when session ends | Verify |

**Rules for between processing sessions:**
- Close the email tab/app entirely
- Turn off all email notifications (desktop, phone, badge counts)
- If someone needs you urgently, they can call or walk over
- The only exception: waiting for a time-sensitive reply (set a VIP notification, not full inbox alerts)

## Output Format

```markdown
# Inbox Zero System: [Name / Role]

## Current State
- **Inbox count:** [n]
- **Daily volume:** [n emails/day]
- **Time spent on email:** [hours/day]
- **Primary pain point:** [description]

## Triage Rules
[5-Action framework customized for this person]

## Folder/Label Structure
| Folder | Purpose | Review Cadence |
|---|---|---|
| ... | ... | ... |

## Automated Filters
| Rule Name | Condition | Action | Estimated Volume Filtered |
|---|---|---|---|
| ... | ... | ... | ... |

## Response Templates
| Template | Use Case | Text |
|---|---|---|
| ... | ... | ... |

## Processing Schedule
| Time | Duration | Focus |
|---|---|---|
| ... | ... | ... |

## Initial Cleanup Plan (if inbox > 100)
| Step | Action | Timeline |
|---|---|---|
| ... | ... | ... |

## Maintenance Habits
- [Daily, weekly, quarterly maintenance tasks]
```

## Quality Checklist

- [ ] Current email state is assessed with specific numbers
- [ ] Triage framework covers all 5 actions: delete, do, delegate, defer, designate
- [ ] Folder structure has 7 or fewer active folders
- [ ] Folders are action-based, not topic-based
- [ ] At least 5 automated filters are defined for high-volume sources
- [ ] Response templates cover the most common reply types
- [ ] Processing schedule defines specific times and durations
- [ ] Notifications are managed: off during focus, controlled during processing
- [ ] Initial inbox cleanup plan exists if current count exceeds 100
- [ ] Weekly and quarterly maintenance habits are defined

## Edge Cases

- **Inbox has 10,000+ unread emails:** Do not try to process them all. Declare email bankruptcy for everything older than 2 weeks. Archive all old emails in one batch. Set up the new system and process only new arrivals. If something old was truly important, someone will follow up.
- **Shared inbox or team email:** Assign ownership for each email type. Use a tagging convention (e.g., "[OWNER: name]" in subject or label). Define SLAs for response times. Rotate triage duty if volume is high.
- **Executive with an assistant:** The assistant applies the triage framework. Only "Action" items and VIP emails reach the executive. The assistant handles "Do" items under 2 minutes and "Delegate" items. The executive processes 20-30 emails per day instead of 200.
- **Multiple email accounts:** Consolidate into one inbox using forwarding or a unified client. Apply the same folder structure across all accounts. If consolidation is not possible, process each account in a separate scheduled session.
- **Critical role where delayed response has consequences (sales, support):** Tighter SLAs require more frequent processing (every 1-2 hours). Use VIP filters for high-value contacts. Set up auto-responders with expected response time during focus blocks.
- **Person who uses inbox as a task manager:** This is the root cause of inbox overload for many people. Migrate deferred items to a real task manager (Todoist, Asana, Things). The "@Action" folder is a bridge, not a destination — tasks belong in a task system.
- **Regulatory or legal retention requirements:** Do not delete anything that may be subject to retention policies. Use archive, not delete. Confirm retention rules with legal/compliance before setting up auto-delete rules.
