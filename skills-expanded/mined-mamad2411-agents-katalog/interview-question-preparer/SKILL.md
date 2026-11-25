---
name: interview-question-preparer
description: Prepare an evidence-backed blog/media interview preparation brief for a specified person by researching public context, reflecting on information sufficiency, and writing the final Markdown deliverable.
---

# Interview Question Preparer

Use this Skill when the task is to prepare a serious blog-style or media-style
interview brief for a specified person, author, founder, maintainer, or project
owner. This is for a published article or long-form conversation, not a hiring
interview, recruiting screen, or candidate evaluation.

## Workflow

1. Clarify the interview target, audience, and intended article angle from the
   task input.
2. Research public context before drafting. Search broadly first, then browse
   only the most relevant pages.
3. Keep compact notes for source URLs, source titles, and why each source is
   relevant.
4. Reflect on information sufficiency:
   - what is well-supported by public evidence;
   - what is weak, ambiguous, or missing;
   - whether any supplied affiliation, organization, work, role, or alias is
     contradicted or not supported by the sources;
   - whether another search or browse step is needed before finalizing.
5. Draft grouped article interview questions that connect the person, project,
   product philosophy, technical tradeoffs, community adoption, business
   context, personal narrative, tensions, and future direction.
6. Write the final Markdown deliverable to the requested workspace path.
7. After writing or revising the requested file, read file back from the
   workspace when a workspace read capability is available, then include a
   concise validation checklist in the final response so the verifier can
   inspect the written content against the task criteria.

## Output Requirements

The final Markdown file must include:

- title;
- target and audience;
- story/interview angle;
- source notes with URLs or source labels;
- sufficiency reflection;
- grouped blog/media interview questions;
- at least eight concrete questions;
- a short closing section for optional follow-up probes.

## Boundaries

- Do not invent biographical facts when public evidence is weak.
- Mark weak assumptions explicitly.
- Source notes must be specific: include a URL, title, or clear source label,
  plus one sentence explaining why that source matters to the interview angle.
- If the user's wording implies an affiliation or relationship that sources do
  not support, mark it as uncertain or contradicted instead of repeating it as
  fact.
- When public evidence is sparse, state low confidence, list unknowns, and use
  clarifying or exploratory questions rather than invented biography.
- When names, aliases, or same-name people are ambiguous, preserve the user's
  original wording and explain the disambiguation choice.
- When multiple targets are supplied, include target-specific questions for
  each target and comparative article questions that connect them.
- Prefer questions that can elicit original insight from the interviewee, not
  generic product promotion.
- Do not frame the deliverable as a job interview, hiring guide, candidate
  assessment, or recruiting screen.
- If the task asks for a file, use the workspace file-writing capability and
  report the written path.
- If the task is correcting a previously written file, prefer reading the file
  before deciding whether to patch or fully rewrite it.
