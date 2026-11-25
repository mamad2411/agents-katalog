---
name: sop-builder
description: "Builds standard operating procedures from a conversational interview about any business process and publishes the structured SOP to Notion. Use when a user wants to document a repeatable process, onboard team members, or systematize operations they currently do from memory."
allowed-tools: Read Write Glob mcp__claude_ai_Notion__notion-create-pages mcp__claude_ai_Notion__notion-search mcp__claude_ai_Notion__notion-fetch
metadata:
  author: Salah-XD
  version: "1.0"
---

# SOP Builder

## When to Use This Skill

Use this skill when:
- A user says they want to document a process, workflow, or procedure
- Someone is onboarding a team member and needs written steps for a recurring task
- A user mentions they do something "from memory" and wants it systematized
- A business owner wants to delegate a task but has never written it down
- A user asks to create an SOP, runbook, playbook, or process document

**DO NOT** use this skill for:
- One-time project plans (those are project briefs, not SOPs)
- Strategy documents or high-level business plans
- Technical documentation for software APIs or codebases

## How It Works

EVERY SOP MUST BE BUILT FROM THE USER'S ACTUAL PROCESS, NOT FROM ASSUMPTIONS OR GENERIC TEMPLATES. THE INTERVIEW PHASE IS MANDATORY.

---

### Phase 1: Interview — Extract the Process

Conduct a structured interview to pull the real process out of the user's head. Ask these questions in order, waiting for answers between each group. **Do not skip this phase.**

**Group 1 — Context (ask all at once):**

1. What is this process called? (Use their words — that becomes the SOP title.)
2. What triggers this process? What event or request kicks it off?
3. Who performs this process? (A specific role, the user themselves, a VA, a team?)
4. How often does it happen? (Daily, weekly, per client, on-demand?)

**Group 2 — Steps (ask after Group 1 is answered):**

5. Walk me through the process from start to finish. What is the very first thing you do?
6. What happens next? (Repeat until they say "that's it" or describe the final output.)
7. Are there any decision points where the process branches? (e.g., "If the client says X, do Y. If they say Z, do W.")
8. What tools, software, or accounts are needed at each step?

**Group 3 — Failure modes (ask after Group 2 is answered):**

9. Where do mistakes usually happen? What goes wrong most often?
10. What does a successful outcome look like? How do you know this process was done correctly?
11. Is there anything you always forget or wish someone had told you the first time?

**GATE: Do not proceed to Phase 2 until you have answers to at least questions 1-6 and 10.** If the user cannot answer a question, note it as "TBD" in the SOP and flag it for follow-up.

**If the user struggles to articulate steps:** Ask them to describe the last time they performed this process. Concrete recent memory is easier to extract than abstract process descriptions. Say: "Think about the last time you did this. What did you open first? What did you click on?"

---

### Phase 2: Structure — Organize into SOP Format

Transform the interview answers into a structured SOP with these exact sections:

#### SOP Document Structure

```
# [Process Name] — Standard Operating Procedure

## Purpose
One sentence: what this process accomplishes and why it matters.

## Scope
Who this applies to, when it applies, and what it covers/excludes.

## Roles & Responsibilities
| Role | Responsibility |
|------|---------------|
| [Role] | [What they do in this process] |

## Prerequisites
- [ ] [Tool, access, or setup required before starting]
- [ ] [Account, credential, or permission needed]

## Procedure

### Step 1: [Action verb] [what]
[1-3 sentences of detail]
- Tool: [specific software/tool used]
- Time estimate: [how long this step takes]

> **Decision point:** If [condition], go to Step 1a. Otherwise, continue to Step 2.

#### Step 1a: [Branch action]
[Detail for the branch path]
[Return to main flow: "After completing, continue to Step 2."]

### Step 2: [Action verb] [what]
[Continue pattern...]

## Common Mistakes & How to Avoid Them
| Mistake | Impact | Prevention |
|---------|--------|------------|
| [What goes wrong] | [What happens] | [How to prevent it] |

## Success Criteria
- [ ] [Observable outcome that confirms success]
- [ ] [Quality check or verification step]

## Revision History
| Date | Version | Author | Changes |
|------|---------|--------|---------|
| [Today] | 1.0 | [User] | Initial version |
```

**Formatting rules:**
- Every step starts with an action verb (Send, Open, Click, Create, Review, Confirm)
- Decision points use blockquote callout format with bold "Decision point:" prefix
- Time estimates are optional but encouraged — include them if the user provided timing info
- Keep each step to 1-3 sentences of detail maximum
- Number steps sequentially even when branches exist (1, 1a, 1b, 2, 3, 3a, 4)

---

### Phase 3: Review — Present for Approval

Present the complete structured SOP to the user in the chat. Then ask:

1. "Does this match how you actually do it? Are any steps missing or out of order?"
2. "Are the decision points accurate? Did I capture the branching correctly?"
3. "Anything you want to add to the common mistakes section?"

**GATE: Do not publish to Notion until the user explicitly approves.** Acceptable approvals: "looks good", "yes", "approved", "ship it", "publish it", or similar affirmative.

If the user requests changes, make them and re-present the updated SOP. **If the user requests more than 3 rounds of revisions, pause and ask:** "It seems like the process might still be evolving. Would you like to finalize what we have now and mark specific sections as 'needs refinement,' or do you want to keep iterating?"

---

### Phase 4: Publish — Create the Notion Page

After user approval, publish the SOP to Notion.

**Step 1:** Search for an existing SOP location in Notion.

Use `mcp__claude_ai_Notion__notion-search` to find a page or database named "SOPs", "Standard Operating Procedures", "Processes", or "Playbooks".

If found, create the new SOP as a child of that page. If not found, ask the user: "I could not find an SOP section in your Notion workspace. Where should I create this page? You can give me the name of an existing page to put it under, or I can create it at the top level of your workspace."

**Step 2:** Create the Notion page.

Use `mcp__claude_ai_Notion__notion-create-pages` with the structured SOP content. Format the content using Notion block types:

- **Headings** for section titles (heading_1 for SOP title, heading_2 for sections, heading_3 for steps)
- **Tables** for Roles & Responsibilities, Common Mistakes, and Revision History
- **To-do blocks** for Prerequisites and Success Criteria checkboxes
- **Callout blocks** for Decision points
- **Numbered list items** for step sub-details
- **Dividers** between major sections

**Step 3:** Confirm publication.

After the page is created, report back: "Your SOP for [Process Name] has been published to Notion under [parent page name]. Here is what was created: [brief summary of sections and step count]."

---

## Concrete Examples

### Example 1: Client Onboarding SOP

**User says:** "I need to document my client onboarding process. I keep forgetting steps and my VA has no idea what to do."

**Phase 1 interview produces:**

```
Trigger: New client signs contract
Who: VA handles most of it, I do the kickoff call
Frequency: 2-4 times per month

Steps extracted:
1. Receive signed contract from DocuSign notification
2. Create client folder in Google Drive using the template
3. Add client to project management tool (Asana)
4. Send welcome email with onboarding questionnaire
5. Schedule kickoff call (30 min) via Calendly
6. Review questionnaire responses before the call
7. Conduct kickoff call — confirm goals, timeline, deliverables
8. Create project timeline in Asana based on kickoff
9. Send follow-up email with timeline and next steps
10. Add client to monthly check-in calendar

Decision point: If client hasn't returned questionnaire 48 hours
before kickoff call, send a reminder. If still no response,
call without it and fill it in live.

Common mistakes:
- Forgetting to create the Drive folder (causes chaos later)
- Sending the wrong Calendly link (personal vs. client)
- Not reviewing questionnaire before the call (looks unprepared)

Success criteria:
- Client has a Drive folder, Asana project, and scheduled kickoff
  within 24 hours of contract signing
- Follow-up email sent within 2 hours of kickoff call
```

**Phase 2 structures this into the full SOP format with 10 numbered steps, 1 decision branch, 3 common mistakes in the table, and 2 success criteria.**

**Phase 3 presents it. User says:** "Looks good but add a step about checking if they need a custom invoice before the welcome email."

**Phase 4 publishes to Notion under the user's "SOPs" page.**

---

### Example 2: Order Fulfillment SOP

**User says:** "I sell physical products and my fulfillment process is a mess. I need to write it down so my new hire can handle it."

**Phase 1 interview produces:**

```
Trigger: New order notification from Shopify
Who: Fulfillment assistant (new hire)
Frequency: 10-30 orders per day

Steps extracted:
1. Check Shopify orders dashboard every morning at 9 AM
2. Print packing slips for all unfulfilled orders
3. Pull items from inventory shelves using packing slip
4. Verify item count and condition (no damage, correct variant)
5. Pack items with branded tissue paper and thank-you card
6. Weigh package and print shipping label via ShipStation
7. Mark order as fulfilled in Shopify
8. Drop packages at UPS by 4 PM for same-day processing

Decision point: If an item is out of stock, check backstock room.
If still unavailable, email the customer with an estimated restock
date and offer a refund or substitute. Mark the order as "on hold"
in Shopify with a note.

Decision point: If order is international, use customs form
template in ShipStation. Add product descriptions and declared
values.

Common mistakes:
- Shipping the wrong variant (size/color) because packing slip
  wasn't double-checked
- Missing the 4 PM UPS cutoff and delaying delivery by a day
- Forgetting to mark as fulfilled in Shopify, causing duplicate
  shipments from confusion
- Not including thank-you card (hurts unboxing experience)

Success criteria:
- Every order placed before 9 AM ships the same business day
- Zero wrong-item shipments per week
- Every package includes branded insert
```

**Phase 2 structures this into the full SOP format with 8 numbered steps, 2 decision branches (out of stock, international orders), 4 common mistakes in the table, and 3 success criteria.**

**Phase 3 presents it. User approves without changes.**

**Phase 4 publishes to Notion. Finds an existing "Warehouse Operations" page and creates the SOP as a child page.**

---

## Anti-Patterns

- **DO NOT skip the interview and generate a generic SOP.** Every SOP must come from the user's actual answers. A generic "client onboarding" SOP from your training data is useless — it won't match their tools, their team, or their edge cases.
- **DO NOT assume steps the user did not mention.** If their process has a gap (e.g., they never mentioned a quality check), ask about it in the interview. Do not silently insert steps.
- **DO NOT create 30-step SOPs for simple 5-step processes.** Match the SOP complexity to the process complexity. A process that takes 10 minutes to perform should not produce a 3-page SOP.
- **DO NOT use vague language in steps.** "Handle the client request" is not an SOP step. "Open the support inbox in Zendesk and reply using the First Response template" is an SOP step.
- **DO NOT combine multiple processes into one SOP.** If the user describes a process that clearly contains two distinct workflows (e.g., "onboarding and offboarding"), split them into separate SOPs.
- **DO NOT publish to Notion without explicit user approval.** Phase 3 review is mandatory.

---

## Recovery

### Notion API Fails
If `mcp__claude_ai_Notion__notion-create-pages` fails:
1. Report the error to the user clearly: "Notion publishing failed. Here's the error: [error details]."
2. Offer to save the SOP as a local Markdown file instead: write it to the user's current working directory as `[process-name]-sop.md`.
3. Offer to retry the Notion publish once the user has verified their Notion connection.

**If Notion fails 3 times, stop attempting and default to local file output.** Tell the user: "Notion publishing is not working right now. I have saved your SOP as a local Markdown file. You can copy it into Notion manually, or we can try publishing again later."

### User Cannot Articulate the Process
If the user gives vague or incomplete answers during the interview:
1. Ask them to describe the last specific time they performed the process: "Think about the last time you did this. Walk me through what you did, step by step."
2. If still vague, offer to start with a rough draft based on what they have given, marking unclear sections with "[NEEDS DETAIL]" callouts.
3. If after 3 attempts the user still cannot describe the process, suggest: "This process might not be ready to document yet. Consider performing it one more time and taking notes as you go. Then we can turn those notes into an SOP."

### Process Is Too Complex
If the interview reveals a process with more than 20 steps or more than 5 decision branches:
1. Suggest breaking it into sub-processes: "This looks like it is actually 2-3 separate procedures. Want me to split it into [Sub-process A], [Sub-process B], and [Sub-process C] with a master overview that links them?"
2. If the user insists on one document, create it but add a "Quick Reference" section at the top with a simplified numbered checklist (steps only, no detail) for daily use, followed by the full detailed version below.

### SOP Already Exists in Notion
If `mcp__claude_ai_Notion__notion-search` finds an existing SOP with the same or similar name:
1. Fetch the existing SOP using `mcp__claude_ai_Notion__notion-fetch` and show the user a brief comparison.
2. Ask: "An SOP called [name] already exists in your Notion. Do you want to replace it with this new version, or create this as a separate document (e.g., '[name] v2')?"
3. Proceed based on the user's choice.

---

## Pre-Publish Checklist

Before delivering the final SOP (whether to Notion or local file), verify:

- [ ] Every step starts with an action verb
- [ ] All decision points have both branches specified (if X, do Y; otherwise, do Z)
- [ ] Tools and software mentioned are specific (not "project management tool" but "Asana")
- [ ] Common mistakes section has at least 2 entries
- [ ] Success criteria are observable and measurable (not "client is happy" but "follow-up email sent within 2 hours")
- [ ] No placeholder text like [TBD] remains unless flagged for intentional follow-up
- [ ] SOP title matches the user's own name for the process
