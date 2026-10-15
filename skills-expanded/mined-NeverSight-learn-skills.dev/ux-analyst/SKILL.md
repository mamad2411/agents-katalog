---
name: ux-analyst
description: "Transform prototype demos from visual representations into behavioral semantics. Use when users provide Figma designs, HTML demos, screenshots, videos, or any UI mockups and need them converted into structured UX flow documents. Trigger on requests like analyze UX, convert demo to flows, write UX-FLOWS, describe user interactions, map screen behaviors, understand page transitions, ux分析, 写 UX 流程, 页面行为分析, 用户流程语义化, or translate prototype to behavior."
---

# UX Analyst

Transform prototype demos from "visual representation" into "behavioral semantics". This skill translates UI mockups into executable behavioral specifications that engineers and other AI agents can use to implement features.

<HARD-GATE>
Do not write `prd/UX-FLOWS.md` until at least one visual or behavioral input has been provided (Figma, screenshot, video, HTML demo, or wireframe).
If no visual input exists, ask the user to provide one before proceeding.
If input exists but the scope (which pages/screens to cover) is unclear, ask one clarifying question first.
</HARD-GATE>

## When to Use

Use this skill when:
- User provides Figma links, screenshots, videos, or HTML demos
- User wants to understand how pages/screens behave
- Converting visual designs to implementation requirements
- Before writing SPEC or technical implementation
- Any request to analyze or document user interactions and flows

## Workflow

1. Check what visual/behavioral inputs are available (Figma, screenshots, video, HTML, PRD)
2. If no visual input exists, ask the user to provide one before proceeding
3. If scope is unclear (too many screens, ambiguous priority), ask one question to narrow it
4. Analyze inputs — extract page purposes, entry/exit conditions, key actions, states
5. Write `prd/UX-FLOWS.md` to disk (and `prd/SCREEN-INVENTORY.md` if scope warrants it)
6. Report file path(s) and ask if any page behavior needs clarification

## Input

This skill accepts:
- PRD (optional but recommended for context)
- Figma designs or links
- HTML/CSS demos
- Screenshots
- Videos of interactions
- User flow diagrams
- Wireframes

## Output Documents

Generate these documents in `prd/` directory (or user-specified location):

1. **Required**: `prd/UX-FLOWS.md` - Main behavioral specification
2. **Optional**: `prd/SCREEN-INVENTORY.md` - Screen/Page inventory if the system has many screens

## UX-FLOWS.md Structure

### 1. Document Overview

Briefly describe:
- What this document covers
- Number of key screens/pages
- High-level user journey

### 2. Screen/Page Definitions

For **each key screen/page**, document:

#### 2.1 Page Purpose
- What is this page's goal?
- Who uses it?
- What business problem does it solve?

#### 2.2 Entry Conditions
- How does user arrive at this page?
- What must be true before this page is accessible?
- Any authentication/authorization requirements?
- Any prerequisite states (e.g., "must have completed step 1")?

#### 2.3 Exit Conditions
- What triggers leaving this page?
- Where does user go next?
- Are there multiple exit paths?

#### 2.4 Key Actions (Business-Level)

**NOT just "click submit button"** - describe the business semantics:

| Action | When Enabled | State Change | Failure Handling | Success Behavior | Recovery |
|--------|--------------|--------------|------------------|-------------------|----------|
| Submit form | All required fields filled | Advances to "pending_review" | Show validation errors | Redirect to list page | Resume from last saved draft |
| Delete item | User has delete permission | Marks as "archived" | Show error toast, keep page | Refresh list, show success toast | None (soft delete) |
| Approve request | Request in "pending" state | Advances to "approved" | Show error with reason | Navigate to next item | Can revert within 24h |

For each action, always specify:
- **When Enabled**: Under what conditions can this action be triggered?
- **State Change**: Does this action advance/modify the business state?
- **Failure Handling**: What happens on failure? What error messages?
- **Success Behavior**: What happens on success? Page redirect? Toast? State update?
- **Recovery**: Can interrupted flows be resumed?

#### 2.5 User-Visible States

Document all states the user can see:
- Loading states (what shows while fetching?)
- Empty states (what if no data?)
- Error states (what if something fails?)
- Success states (what confirms completion?)
- Draft/In-progress states (can user save and return later?)

#### 2.6 Blocking Conditions

What prevents user from proceeding?
- Permission checks
- Prerequisites not met
- Business rule blocks (e.g., "cannot submit after deadline")
- System unavailability
- Rate limiting

For each blocking condition:
- What triggers the block?
- What does user see?
- How to resolve?

#### 2.7 Error/Exception Scenarios

What can go wrong and how is it communicated?
- Network errors
- Validation failures
- Permission denied
- Concurrent modification conflicts
- Timeout scenarios
- Service unavailable

For each error:
- User-facing message
- Whether action can be retried
- Whether data is preserved
- Any compensation action needed

## Writing Principles

### DO: Write Behavior, Not UI

**Bad:**
- "Click the Submit button"
- "The form has Name and Email fields"
- "Show a success message"

**Good:**
- "Submit button becomes enabled only when all required fields have valid values and no validation errors exist"
- "Upon submission, advances order to 'pending_review' state; on failure, displays field-level validation errors and preserves all entered data"
- "On success, displays toast notification for 3 seconds, then redirects to /orders with success filter applied"

### DO: Include State Transitions

For each action that changes state, document:
```
Action: Submit Order
Pre-condition: All required fields valid AND order total > 0
Post-state: draft → pending_review
Side effects:
  - Order number generated
  - Confirmation email queued
  - Inventory reserved for 15 minutes
```

### DO: Define Entry/Exit Criteria

Every page should answer:
- How do I get here? (entry)
- What happens next? (exit)
- What blocks me? (blocking)

### DON'T: Describe Layout Details

Focus on behavior, not:
- "Button is in top-right corner"
- "The form uses a two-column layout"
- "Card has shadow and rounded corners"

### DON'T: Use Generic Actions

Be specific about what each action does:
- "Process submission" - what exactly happens?
- "Show message" - what message, in what context?
- "Save data" - where, with what validation?

## SCREEN-INVENTORY.md (Optional)

Use when system has many screens. Structure:

### Screen List

| Screen ID | Screen Name | Route/URL | Primary User Role | Purpose |
|-----------|-------------|------------|-------------------|---------|
| S1 | Order List | /orders | Customer | View and manage orders |
| S2 | Order Detail | /orders/:id | Customer | View order details |
| S3 | Order Edit | /orders/:id/edit | Customer | Modify order |
| S4 | Order Create | /orders/new | Customer | Create new order |

### Navigation Map

Document how screens connect:
```
S1 (List) → S2 (Detail) → S3 (Edit)
S1 (List) → S4 (Create)
S2 (Detail) → S3 (Edit)
```

## Completion Criteria

- [x] Every key screen has clear purpose documented
- [x] Entry conditions specified for each screen
- [x] Exit conditions specified for each screen
- [x] All key actions documented with:
  - When enabled (preconditions)
  - State changes (if any)
  - Failure handling
  - Success behavior
  - Recovery options
- [x] User-visible states documented
- [x] Blocking conditions identified
- [x] Error scenarios covered
- [x] No generic "click X" descriptions - all are business-level behaviors
- [x] Pages are业务流程 nodes, not just UI screenshots

## Output Location

Default: `prd/UX-FLOWS.md` and `prd/SCREEN-INVENTORY.md`

Follow user's specified location if provided.

**Always write to disk. Do not output UX files only in the conversation.**
