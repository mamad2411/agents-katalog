---
name: clarify-question
description: Use a fresh task profile and a four-level policy to turn material ambiguity into a precise, self-contained prompt without asking the user to make technical choices the agent can investigate.
version: 2.2-public
---

# Clarify Question

Use this skill when a request reaches Level 3 under
`method/clarification-policy.md`, when the user explicitly asks to refine a
question, or when a task must become a self-contained handoff.

## Role

Your job is to discover the smallest set of user decisions that materially
changes the work. Ask about goals and tradeoffs; investigate technical details
yourself. Once the request is clear, produce a precise handoff prompt.

Do not execute the original task while running this skill unless the user
explicitly switches to execution. Do not turn clarification into authorization.

## Step 0: Load The Task Profile

Follow `method/profile-context.md` before deciding what the user may need help
clarifying:

1. Read the current conversation.
2. Load the configured base profile and only relevant Markdown memory.
3. Separate confirmed preferences from agent inference.
4. Record source, freshness, and confidence for conclusions that affect the questions.
5. If sources conflict, follow the documented precedence and expose the conflict.

No profile entry is evidence that the user is unfamiliar with a domain. Upgrade
only when there is a concrete hidden choice that could change the result.

## Four-Level Boundary

- Level 1: execute directly. Do not invoke this skill.
- Level 2: state one key reversible assumption, then continue without a full clarification round.
- Level 3: explain why a decision matters, then ask 1-3 concise questions.
- Level 4: stop the side effect and request explicit authorization. This skill
  may clarify the target or scope, but its output is never authorization.

When more than one rule matches, the highest valid level wins.

## Ambiguity Checklist

- Real goal: what decision or action is this meant to support?
- Scope: time, geography, audience, quantity, platform, version, or budget.
- Input materials: files, links, data, examples, screenshots, or prior decisions.
- Output shape: short answer, report, checklist, code change, plan, script, or handoff.
- Success criteria: what counts as done?
- Risk boundaries: publishing, spending money, account actions, destructive edits, private data, or external messages.
- Freshness: whether facts, prices, laws, APIs, product features, or policies need current verification.

## Unknown Blind Spots

Unknown blind spots are important choices the user may not know to mention.
Check for them proactively, especially when the task profile indicates limited
experience in the current domain. Examples include:

- an audience or distribution decision that changes the design;
- a human-review boundary that changes the workflow;
- a cost, latency, quality, or automation tradeoff;
- a privacy, permission, publication, or rollback consequence;
- a compatibility constraint that cannot be repaired cheaply later.

Do not ask "Which database, framework, or API do you want?" merely because the
user is not technical. Inspect the project, compare viable options, and translate
the technical difference into a decision the user can make.

## Question Design

1. Ask only questions whose answers would materially change the result.
2. Keep each round to 1-3 questions.
3. Put the recommended option first when a bounded choice is useful.
4. Explain the consequence of each option in plain language.
5. Resolve from existing files, tools, or current sources before asking the user.
6. If a safe default is reversible, state it and continue at Level 2.

## User Versus Agent Responsibility

Ask the user to decide:

- the business outcome and intended audience;
- success criteria;
- cost, speed, quality, and automation tradeoffs;
- which steps require human review;
- whether a gated side effect is authorized.

The agent should investigate:

- current code, data, and project conventions;
- libraries, APIs, runtime constraints, and existing tools;
- verifiable cost, safety, compatibility, and freshness facts;
- implementation details that do not alter the user's product intent.

## Final Output Format

```text
Good, the request is clear enough. Here is the precise version:

**Refined Prompt**

<Put the self-contained prompt here. Include background, constraints, inputs, output format, and acceptance criteria.>

**Suggested Execution Surface**

<Recommend one primary agent/tool and at most one backup. Explain briefly why.>

**Assumptions And Gates**

<List any remaining assumptions. Name every side effect that still needs explicit authorization.>

**Confirmation**

Does this match what you want to ask?
```

## Routing Guidance

- Local code changes, tests, repository edits, and repeatable scripts: use a coding agent in the relevant workspace.
- Long-form research with current facts: use a research-capable agent with web access and cite sources.
- Large local files or media: use a runtime that can read those files directly.
- Browser actions behind login: use a browser-capable agent only after the user authorizes account access.
- External messages, publishing, payments, destructive edits, and API calls that can spend money require explicit user authorization.

## Anti-Patterns

- Answering the original question instead of clarifying it.
- Asking too many questions at once.
- Recommending a tool before understanding the task.
- Assuming private skills, private accounts, or private project history exist.
- Hiding unresolved assumptions in the refined prompt.
- Treating a refined prompt, selection, or profile preference as permission to perform a gated action.
