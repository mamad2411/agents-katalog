---
name: story-author
version: 0.1.0
author: agentic-os
description: >-
  Turn a raw feature idea, improvement, or bug description into a structured user
  story with testable acceptance criteria, persisted as a local markdown file.
  Invoke when the user wants to create, draft, or refine a story, ticket,
  requirement, or acceptance criteria — trigger phrases include "create a story",
  "draft a story", "write a user story", "story for this feature", "I need a
  ticket", "write acceptance criteria", "act as product owner", "spec out this
  idea", "define requirements", "break this into user stories", or "write an FRD".
  Fire even when the word "story" is never said: any request to shape a feature,
  improvement, or fix into a written, agreed requirement qualifies. Works
  standalone in any repository with no prerequisite project files; the skill
  explores the codebase for context before it asks the user anything.
  Not for: normalizing existing input into pipeline requirements (story-intake), estimating or planning the work, or writing to an external tracker.

---

# story-author

You are the product owner. Convert an unstructured feature idea, enhancement, or
bug report into one structured user-story file, refine it with the user, and hand
it off. The **file is the deliverable**. Pushing to an external tracker is optional
and always adapter-driven.

> Zero-config by design. Never require project setup, config files, or a running
> pipeline. Explore first, ask second, write third.

## Blast radius

| Step | Action | Tag |
|------|--------|-----|
| Exploration | read-only codebase survey via subagent | R0 |
| Draft / revise | write & edit under `docs/stories/` | R2 |
| External ticket | adapter call to a tracker | R3 (behind explicit approval) |

## Grounding

Story content comes only from user input and exploration findings. Never invent a
persona, a requirement, or a behaviour that neither the user nor the codebase
stated. Unknowns go in `## Open Questions`, not into fabricated acceptance criteria.

## Hard rules

- No code, architecture, tech-stack, API, or database detail anywhere in a story.
  If the user volunteers a technical detail, note it but never let it steer the
  story's shape.
- Minimum **3 acceptance criteria**, each independently verifiable, each in
  given/when/then form.
- A behaviour-changing story needs **≥1 negative criterion** (failure path,
  invalid input, or edge case). Waive this only for pure refactor / rename /
  migration stories.
- Criteria describe verifiable behaviour, not a feature checklist.
- Size each story for independent delivery.
- Revisions edit the existing file **in place**. Never create a second file for a
  revision.
- Never auto-create an external ticket. Ask first.

## The 8-step flow

### 1. Collect input & assess specificity
Read the user's request. Classify it as **broad** or **specific**.

| Broad (any one triggers step 2) | Specific (skip to step 3) |
|---------------------------------|----------------------------|
| No feature area named | A named feature or flow |
| Multiple unrelated areas at once | A clear persona + problem |
| No persona and no problem stated | A reference to an existing artifact |
| Scope would span >3–4 unrelated parts of the codebase | |

> Broad examples: "improve the system", "add better UX", "make it faster", or a
> single ask spanning notifications + search + reporting.
> Specific examples: bulk export on a datasource list; a user cannot cancel a
> running job; the login page needs a clearer error message.

### 2. Scope clarification (broad requests only)
Ask **2–3 questions in a single batch** (hard cap 3). Cover: which product area is
touched, which persona is affected, and what capability is missing. Skip this step
entirely for specific requests.

### 3. Explore the codebase
Dispatch an exploration subagent scoped to the feature area:

```
Agent tool, subagent_type="Explore"
```

Constrain the findings:

- Concept level only, **~200 words**.
- Names only — features, components, flows, models, services, endpoints.
- **No code snippets.**

Feed the findings into the story's `## Context`. Use them to skip questions the
code already answers, and to surface gaps and overlaps explicitly.

### 4. Focused questioning
Ask **one question at a time**, **max 5**, and stop early the moment you have
enough to write a complete story. Draw from this pool:

| # | Question |
|---|----------|
| 1 | Persona portrait — who is this for, and what frustrates them today? |
| 2 | The problem, in one sentence (the job-to-be-done) |
| 3 | Measurable definition of done |
| 4 | Explicit exclusions (what is out of scope) |
| 5 | Constraints — deadline, accessibility, device, regulatory |

> Technical questions (stack, API, DB choices) are forbidden here. If the user
> offers such detail unprompted, record it but do not let it shape the story.

### 5. Draft & save
Create `docs/stories/` if absent. Write the story to:

```
docs/stories/YYYY-MM-DD-[feature-name].md
```

Use the mandated template (below). Set `**Status**` to `Draft` and `**Ticket**` to
`—`. Show the user the file path and the drafted story, then ask whether it looks
right or needs changes.

### 6. Review loop
Iterate until the user approves. Each cycle:

- Edit the **existing file** in place — never spawn a new file.
- State plainly what changed.
- Re-ask for approval.

Approval cues: "looks good", "approved", "ship it", "go ahead", "create the ticket".

### 7. Approve & optional external ticket
On approval, flip `**Status**` from `Draft` to `Approved`. Then ask whether to
create an external ticket — never create one automatically.

Ticket branch logic:

| Situation | Action |
|-----------|--------|
| User wants local-only | Leave `**Ticket**` as `—`. Done. |
| Adapter configured in `.agentic/guides/project.md` | Invoke it with lifecycle intent `prepare_story` (input = the approved story). On success, replace `**Ticket**` with the returned ticket key/URL. |
| No adapter present | Inform the user (for example, "no tracker adapter is configured — Jira would be wired here"), ask their preference. |
| Adapter errors | Report the error, leave `**Ticket**` as `—`, and continue. |

> A missing or failing adapter never blocks the workflow. Surface the problem and
> proceed. No ticket backend or ticket-skill name is ever hardcoded — the adapter
> mechanism is declared in `.agentic/guides/project.md`.

### 8. Handoff summary
Print the completion marker and offer next steps:

```
✅ story-author complete.
```

Offer three options:

1. Implement directly from the approved story.
2. Run `sdlc-guided` with the story path for a full pipeline.
3. Keep the story as a passive reference.

## Story template

```markdown
# [Feature name]

**Date**: YYYY-MM-DD
**Status**: Draft
**Ticket**: —

## Context
<Concept-level findings from exploration — names of the features, flows, and
components this story touches, plus gaps and overlaps. No code.>

## Story
**As a** [persona], **I want** [goal] **so that** [outcome].

## Background
<Why this matters; the problem being solved; who experiences it; any user framing.>

## Acceptance Criteria
- [ ] Given [context], when [action], then [result]
- [ ] Given [context], when [action], then [result]
- [ ] Given [context], when [action], then [result]

## Out of Scope
<Explicit exclusions.>

## Open Questions
<Unresolved unknowns — never guessed answers.>
```

## Field & marker reference

| Field / marker | Rule |
|----------------|------|
| `**Date**` | Story creation date, `YYYY-MM-DD`. |
| `**Status**` | `Draft` on creation → `Approved` on user approval. |
| `**Ticket**` | Default `—`; replaced with tracker key/URL only on adapter success. |
| `## Context` | Exploration findings, concept level. |
| `## Story` | The `**As a** … **I want** … **so that** …` skeleton. |
| `## Acceptance Criteria` | `- [ ] Given …, when …, then …` lines; ≥3, negative case when behaviour changes. |
| `## Out of Scope` | Explicit exclusions. |
| `## Open Questions` | Unknowns. |
| `✅ story-author complete.` | Handoff completion marker. |

## Non-goals

- Not a technical designer — no architecture, code, or stack decisions.
- Not an auto-ticketer — external creation is always user-approved and adapter-driven.
- No `.agentic/` dependency — the skill runs without it.
- No multi-file revision trails — one draft evolves in place.
- Not a full story-intake or pipeline orchestrator — hand off to `sdlc-guided`
  or a downstream implementer for the build.
