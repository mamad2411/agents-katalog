---
name: deliverable-qa
description: QA a client deliverable, report, or presentation against consulting quality standards before it goes out. Use when asked to review, QA, proofread, or sanity-check anything client-facing. Usage - /deliverable-qa path/to/deliverable
---

# Deliverable QA

Review the specified deliverable against consulting quality standards and produce a structured QA
assessment. This is an internal review meant to improve quality before the deliverable reaches
the client. It is a second reviewer, never the last one.

## Input

`$ARGUMENTS` is the path to the deliverable (`.md`, `.docx`, `.pptx`, `.pdf`, or `.xlsx`). If no
path was given and the deliverable was drafted earlier in this conversation, say so and offer to
review it anyway, but note that a review of your own draft is weaker than a cold read. For a
genuinely fresh read, the user can save the draft to a file and either run `/clear` and this skill
again, or ask for the `second-reviewer` subagent.

## QA Dimensions

Assess the deliverable across these five dimensions:

### 1. Executive Clarity
- Does the document lead with the "so what"? Would a C-suite reader understand the key message in 30 seconds?
- Are recommendations concrete and actionable, not just observations?
- Is the language free of jargon that requires insider knowledge?

### 2. Logical Structure
- Does the argument flow? Does each section connect to the one before and after?
- Are conclusions supported by evidence presented in the document?
- Is there a clear narrative thread from problem to finding to recommendation?

### 3. Accuracy & Completeness
- Are any key sections missing (for example, no risk section, no next steps)?
- Are data points cited or attributed? Flag any that appear unverified.
- Are there internal inconsistencies (a number in a table that does not match the text, a RAG
  color that does not match the narrative)?

### 4. Client-Readiness
- Is the formatting professional and consistent?
- Are there any placeholders, TODOs, `[NEEDS INPUT]` markers, or draft language that was not removed?
- Does it name any other client, or carry a sensitive detail that should not travel?
- Is the tone appropriate for the stated audience?

### 5. Actionability
- After reading this, does the client know what to do next?
- Are next steps specific, with named owners and dates?
- Would a client who has not been in the room understand what is being asked of them?

## Output Format

**Overall Readiness:** [✅ Ready / ⚠️ Needs Revision / 🚫 Not Ready]

**Strengths:** 2 to 3 things the document does well

**Issues Requiring Revision:**
| # | Issue | Dimension | Severity | Recommendation |
|---|---|---|---|---|

Severity: High (blocks delivery) / Medium (should fix before sending) / Low (nice to have)

**Quick Wins:**
- Up to 3 small edits that would noticeably improve quality with minimal effort

**Outside my ability to verify:**
- Anything the review could not check, such as whether a quoted figure is current or whether a
  technical claim is correct. The delivery lead routes these to someone who can.

Be specific and constructive. Point to the page, slide, or paragraph. Do not rewrite the
deliverable unless asked; the owner decides what changes.
