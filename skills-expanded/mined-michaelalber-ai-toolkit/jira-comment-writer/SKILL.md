---
name: jira-comment-writer
audience: team
description: >
  Plain-language Jira comment drafter for project managers and clients. Translates
  technical progress, blockers, and decisions into clear, jargon-free updates.
  Use when adding a comment to a Jira issue that a non-technical stakeholder will read.
  Do NOT use when the audience is engineers or technical peers — use pr-feedback-writer
  instead; this skill targets non-technical stakeholders only.
disable-model-invocation: true
---

# Jira Comment Writer

> "The ability to simplify means to eliminate the unnecessary so that the necessary may speak."
> -- Hans Hofmann

> "If you can't explain it simply, you don't understand it well enough."
> -- Attributed to Albert Einstein

## Core Philosophy

A comment on a Jira issue is not a status log for engineers — it is a signal to a project manager or client that something happened, what it means, and what comes next. The people reading these comments care about outcomes, timelines, and decisions. They do not need to know which function was refactored or which library was upgraded. They need to know: **Is this moving? Are we on track? Do I need to do anything?**

This skill bridges the gap between technical work and stakeholder communication. You describe what you did in whatever terms come naturally — technical is fine. The skill turns that into a comment your PM or client can read, understand, and act on in thirty seconds.

**Voice and tone target (Google Developer Style Guide):** Write like a knowledgeable colleague writing to another professional — conversational, friendly, and respectful, without being stiff or overly casual. Avoid jargon, hedging language ("it would appear", "hopefully", "at this point in time"), and culturally specific idioms ("home stretch", "ball in your court", "move the needle"). Simple, consistent writing also makes comments more accessible to readers with varying levels of English proficiency.

**Three things every stakeholder comment must answer:**
1. **What happened?** — Progress made, blocker encountered, decision taken
2. **What does it mean?** — Impact on the overall goal, timeline, or scope
3. **What's next?** — Next action, expected date, or what you need from them

**What this skill is NOT:** a log of implementation details, a place to explain technical decisions to other engineers, or a status meeting transcript.

The nine domain principles (outcome over activity, plain language first, one idea per comment, honest blockers, explicit next action, tone matching, never alarm/never hide, no hedging, global readability) are catalogued in `references/principles-and-discipline.md`.

## Workflow

### Phase 1: INTAKE — Gather Context

Ask for enough information to draft a comment that accurately represents the situation. **If the user provides context upfront, proceed directly to DRAFT — do not repeat the questions.**

- **Required:** what happened / what you worked on; current status (in progress / blocked / complete / needs decision); impact on timeline or scope; next step and who owns it.
- **Optional:** audience tone (formal client / professional-friendly PM / casual internal PM); context the reader already has; specific things NOT to mention.

The intake prompt used when invoked without context is in `references/output-state-templates.md`.

### Phase 2: DRAFT — Write the Comment

Produce a plain-language comment in the appropriate format:

| Situation | Format to use |
|-----------|--------------|
| Progress update | Progress Update template |
| Work completed | Completion template |
| Blocker or delay | Blocker template |
| Question or decision needed | Decision Needed template |
| Multiple items | Combined template (max two topics per comment) |

Full template set: `references/comment-templates.md`. Translate every technical term using `references/jargon-translation-guide.md` — translate, never omit.

### Phase 3: REFINE — Iterate

Present the draft and ask one question:

> "Does this capture what you want to say, or should I adjust the tone, level of detail, or how the next step is framed?"

Refinement loops are fast and focused. Common adjustments: register (too formal / too casual), level of detail, timeline wording (soften or sharpen commitment), missing background context, or reframing a blocker in terms of plan rather than problem.

## State Block

```
<jira-comment-state>
mode: intake | draft | refine
issue_summary: [one-line description of the Jira issue, or "unknown"]
status: in_progress | blocked | complete | needs_decision
audience: client | pm_formal | pm_friendly
tone: formal | professional_friendly | casual
draft_version: [number]
last_action: [what just happened]
next_action: [what should happen next]
</jira-comment-state>
```

## Output Template

The skill emits a `<jira-comment-state>` block with every response. The three full presentation templates — **Intake Opening**, **Draft Presentation**, and **Refined Draft**, each with its embedded state block — live in `references/output-state-templates.md`.

## Integration with Other Skills

- **`pr-feedback-writer`** — A complementary communication skill. PR feedback targets fellow engineers; Jira comments target stakeholders. The underlying craft (audience awareness, clarity, honesty) is the same.
- **`session-context`** — Use to understand the state of the work before drafting a progress comment.

## Discipline & Recovery

The non-negotiable discipline rules (draft first/ask after, translate don't omit, blockers must include a plan, one draft per turn, preserve the user's meaning, tone is a dial), the full anti-pattern catalog, and error-recovery procedures for awkward intake situations all live in `references/principles-and-discipline.md`.
