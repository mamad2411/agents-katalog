---
name: start-next-issue
description: Suggests the next GitHub issue to work on from a PRD breakdown, confirms it with the user, and initiates the pre-implementation discussion.
---

# Start Next Issue

Select the next issue to work on from a PRD breakdown, confirm it with the user, and begin the discussion before implementation.

## Process

### 1. Determine the next issue

- Review the list of open issues from the PRD breakdown.  
- Suggest the next issue in order (backend-first, then frontend linked to completed backend).  
- Highlight any dependencies (for frontend issues, reference the related backend issue).
- Review the list of closed issues from the PRD breakdown. Read the closing comment of each closed issue.

### 2. Confirm with the user

Present the suggested issue with:

- **Title**  
- **Issue number**  
- **Type** (backend / frontend)  
- **Blocked by** (if any)  
- **Related backend issue** (for frontend)  
- **Summary of what the issue builds**

Ask the user:

- Does this issue make sense to start now?  
- Do you agree with the suggested order?  

Wait for user confirmation before proceeding.

### 3. Initiate discussion

Once confirmed, start a structured pre-implementation discussion:

1. **Objective:** Confirm the expected outcome of the issue.  
2. **Backend:** Discuss endpoints, schema, architecture, tools, or libraries.  
3. **Frontend:** Discuss layout, components, interactions, and libraries (if applicable).  
4. **Important decisions / trade-offs:** Any critical design choices or limitations.  
5. **Questions / uncertainties:** Open points to clarify before coding.  

Interview the user relentlessly about every aspect of this plan until you reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. Prioritize decisions that block other decisions (e.g. data model before API shape, API shape before UI). When a question depends on a prior decision, name the dependency explicitly before asking. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

If the user is unsure how to answer, offer 2–3 concrete options and clearly label which one you recommend. Do not accept "I don't know" and advance.

The interview is complete when every major branch has a decision (or an explicitly noted open question) and you can state the full design back without gaps. At that point, stop asking and produce a wrap-up summary with three sections: decisions made (with brief rationale), assumptions accepted, and open questions still requiring resolution.

#### NEVER
NEVER accept "I'll figure that out later" — require a decision or explicitly mark it as an open question before moving on.
NEVER ask multiple questions in a single turn — one question, then wait for the answer.
NEVER let the user redirect to implementation details until all design branches are resolved.

### 4. Mark issue as ready

- Once discussion is complete, mark the issue as ready to start coding.  
- For frontend issues, ensure the related backend issue is completed or reference it.  

No coding begins until this step is fully completed and agreed upon.
