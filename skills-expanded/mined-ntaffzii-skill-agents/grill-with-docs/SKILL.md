---
name: grill-with-docs
description: Planning interview skill that asks sharp questions before execution and turns decisions into durable project docs, domain language, PRDs, or ADR notes. Use when the user has an idea, feature, plan, product change, or unclear request that needs alignment before implementation.
---

# Grill With Docs

Use this skill before implementation when alignment matters.

## Workflow

1. Establish intent
   - Ask what outcome the user wants, who it is for, and what must not change.
   - Identify success criteria and failure modes.

2. Challenge scope
   - Find the smallest useful version.
   - Ask what can be deferred.
   - Surface hidden dependencies, permissions, data needs, and integration points.
   - Separate must-have, should-have, nice-to-have, and out-of-scope items when the request is large.

3. Build shared language
   - Name the domain concepts in the user's words.
   - Define ambiguous terms.
   - Prefer one precise term over repeated explanatory phrases.

4. Convert decisions into docs
   - Create or update lightweight docs only when they will help future sessions.
   - Use PRD for product behavior.
   - Use ADR for architectural decisions.
   - Use glossary/context docs for domain language.

5. End with an execution-ready brief
   - Goals
   - Non-goals
   - Decisions
   - Open questions
   - First implementation slice
   - Validation plan

## Question Rules

- Ask the fewest questions that unblock execution.
- Group related questions.
- Do not interview forever; once enough context exists, recommend a path.
- If the user is absent, make conservative assumptions and label them.

## Verification

- The brief has a clear goal and non-goals.
- Decisions are separated from open questions.
- The first implementation slice is small enough to execute.
- Any assumptions are labeled.

## Output Format

End with:

- Goals
- Non-goals
- Scope
- Decisions
- Open questions
- First implementation slice
- Validation plan
