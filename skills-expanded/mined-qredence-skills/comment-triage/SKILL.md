---
name: comment-triage
description: "Reads all open comments on a file and triages them into categories (needs a design change, needs a decision/answer, already resolved but not marked, out of scope) so a designer can work through feedback efficiently. Use when a file has accumulated many comments and it's unclear what still needs action."
---

# Comment Triage

## Purpose
Turn a pile of open file comments into a clear, prioritized action list.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- A file has many open comments and it is unclear which still need action
- Before starting a revision pass, to plan the work from feedback received

## Required Inputs
- The file (and page/frame scope, if the whole file is too broad) to triage
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Group comments by action needed, not by chronology. Identify duplicates and blocked questions.

## Workflow
1. Read every open (unresolved) comment along with the specific layer/area it is attached to.
2. Classify each comment: "Needs a design change" (a concrete change is being requested), "Needs a decision/answer" (a question that needs a reply, not necessarily a design change), "Appears already addressed" (the design has since changed in a way that seems to resolve the comment -- flag for the commenter to confirm rather than resolving it unilaterally), or "Out of scope / won't do" (a reasonable request that's out of scope for this piece of work, to be explicitly acknowledged rather than silently ignored).
3. For "Needs a design change" comments, group related ones together (multiple comments about the same underlying issue) so they can be addressed in one pass.
4. Note comment age/thread length as a signal for what might need more urgent attention (a long back-and-forth thread often signals unresolved disagreement worth resolving directly rather than in comments).
5. Draft a brief reply for "Appears already addressed" and "Out of scope" comments explaining the status, ready for the designer to review and post rather than posting automatically.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Never resolve/close another person's comment automatically -- only draft the reply and flag it as ready to post.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: Four sections (Needs design change [grouped], Needs a decision, Appears already addressed, Out of scope) each listing the comment, its author, and the location.
