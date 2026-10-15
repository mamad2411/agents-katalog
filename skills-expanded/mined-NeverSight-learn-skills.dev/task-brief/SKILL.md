---
name: task-brief
description: "Use this skill to turn a raw user request into a structured, model-agnostic task brief before executing. Invoke whenever the request is complex, multi-step, cross-domain, ambiguous, or will be handed off to another model or agent. Also trigger when the user says things like 'help me figure out what I need', 'I'm not sure how to ask this', 'I want to do X but I don't know where to start', 'take this and make it clearer', or when the task mixes multiple goals or domains. Do NOT trigger for simple one-line requests with clear intent (e.g., 'fix the typo on line 42', 'rename this variable')."
---

# Task Brief

## Overview

Turn a raw natural-language request into a structured task brief that any execution model can act on without reading the original message.

**This skill is a task specification normalizer.** Its job is to surface the real goal, fill in missing constraints, and decide how to proceed. It does not do design-stage routing or design decomposition (that belongs to `design-orchestrator` and the specialized design skills), write implementation steps (that's `writing-plans`), or execute the task itself.

The value is straightforward: a well-formed brief reduces misunderstanding, prevents wasted work on the wrong sub-problem, and makes the task portable — another model, agent, or human can pick it up cold.

---

## When to Use

**Trigger on:**
- Requests with multiple sub-goals or unclear priority order
- Requests that span domains (e.g., data + UI + API)
- Requests where the stated problem may not be the real problem
- Requests that will be delegated to another model or agent
- Requests where missing context would cause the executor to make large assumptions
- When the user explicitly asks for clarification of their own request

**Do NOT trigger on:**
- Single, unambiguous actions ("delete this function", "run the tests")
- Requests where the intent is clear and the execution path is obvious
- Follow-up messages that clarify an existing task in progress

If in doubt: ask yourself whether an executor seeing only the brief (not the original message) would be able to start work immediately. If yes, the brief is good enough and you probably don't need to go deeper.

---

## Complexity Tiers

Before writing the brief, classify the request into one of three tiers. This determines how much structure to apply and whether to ask a question first.

| Tier | Signal | Response |
|------|--------|----------|
| **Direct** | Single goal, clear scope, no missing critical info | Write brief, set Execution Mode to `direct`, proceed immediately |
| **Clarify** | One critical unknown — a missing parameter, ambiguous intent between 2+ interpretations, OR a stated goal that may be inaccurate (solution-as-goal, symptom-as-goal, scope anomaly) | Write brief, surface the ambiguity explicitly, ask exactly one question, set mode to `clarify-first` |
| **Structured** | Multiple goals, cross-domain, high ambiguity, or handoff needed | Write full brief, set mode to `structured-handoff` or `decompose` |

For Tier 1 (Direct), the brief can be short — 3-4 fields is fine. Don't pad it.

**Tier 2 has three distinct sub-cases — handle them differently:**
- *Missing parameter*: you know the goal, just lack one detail. Write User Goal normally, list the unknown in Core Questions, ask for the missing value.
- *Ambiguous intent*: the goal itself could mean two substantially different things. In User Goal, write both interpretations explicitly as **Interpretation A** and **Interpretation B**. Ask the user to choose — do not pick one silently.
- *Inaccurate goal*: the user stated a solution, a symptom, or an oddly scoped target — not the real intent. Detect three signals:
  1. **Solution-as-goal**: user names a specific technique ("add Redis caching") rather than the problem it solves. Ask: "What problem are you trying to solve?"
  2. **Symptom-as-goal**: user describes an error state ("fix timeout errors") rather than a desired outcome. Ask: "What's the expected behavior?"
  3. **Scope anomaly**: the scope boundary doesn't match the problem's natural boundary — too narrow (retry one endpoint when the whole service is flaky) or too broad. Ask: "Is this issue limited to this area, or does it appear elsewhere?"

  When detected, write User Goal with your best guess at the *actual* underlying goal, flag it as an assumption, and ask one clarifying question. Do not execute on the literal stated goal without confirming.

  Before writing the brief, do a quick search of the codebase for context — check relevant files, existing patterns, or error logs. A brief grounded in code-level facts produces sharper clarifying questions than one based purely on inference from the user's words.

---

## Output: Task Brief

Always output the brief in this format. Omit fields that are genuinely not applicable (mark as `N/A` only if the field is relevant but unknown).

```
## Task Brief

**Task Type:** [analysis | transformation | generation | investigation | orchestration | other]

**User Goal:**
[1-2 sentences. State the real intent, not the surface request. Start with a verb. E.g., "Identify which API endpoints are missing authentication middleware and produce a prioritized fix list."]

**Core Questions:**
- [What must be answered to complete this task?]
- [Include only questions whose answer changes execution — not exhaustive sub-tasks]

**Success Criteria:**
- [How will the executor know the task is done?]
- [Prefer observable outcomes: "a working script", "a diff applied", "a ranked list with rationale"]

**Constraints:**
- Scope: [data source, file range, system boundary, etc.]
- Format: [output language, file type, response length, etc.]
- Risk: [what must not be broken, changed, or leaked]
- Other: [time range, locale, performance budget, etc.]

**Assumptions:**
- [State what you're inferring because the user didn't specify. Keep it short.]

**Execution Mode:** [direct | clarify-first | structured-handoff | decompose]

**Deliverables:**
- [Concrete artifact 1]
- [Concrete artifact 2]
```

---

## Compression Rules

These rules govern how to convert a raw message into the brief. The goal is to preserve intent while removing noise.

**Keep:**
- The underlying goal (what the user actually wants to happen in the world)
- Constraints that eliminate whole categories of solutions
- Domain context that changes how the task should be approached

**Remove:**
- Filler phrases ("I was thinking maybe...", "not sure if this is the right way but...")
- Redundant restatements of the same goal
- Reasoning the executor doesn't need to act

**Convert (vague → actionable):**
- "make it better" → identify the specific dimension: performance, readability, UX, security
- "something's wrong" → specify what behavior is observed vs. expected
- "soon" / "quickly" → ask for a concrete deadline if it affects approach
- "the usual format" → infer from context or flag as an assumption
- "add Redis to the API" → ask: what performance problem is this solving? (solution-as-goal — reframe to underlying problem)

**When intent is ambiguous:**
- If a request has two or more substantially different valid interpretations, do not pick one and proceed — surface the ambiguity in User Goal as "Interpretation A: … vs Interpretation B: …"
- Ask one question that forces a choice between the interpretations, not an open-ended "what do you mean?"
- Keep Deliverables as "deferred until intent confirmed" rather than leaving them blank or guessing

**Don't over-correct:**
- Preserve the user's framing when it carries intent
- Don't introduce goals or constraints the user didn't imply
- If you're unsure whether a detail is essential, keep it and mark it as an assumption

---

## Execution Modes

| Mode | When to use |
|------|-------------|
| `direct` | All info present, single goal, executor can start immediately |
| `clarify-first` | One critical unknown — a missing parameter, an ambiguous goal with 2+ interpretations, or a goal that may be inaccurate (solution/symptom/scope signal); ask only that one question |
| `structured-handoff` | Task is complex but well-scoped; brief is complete enough for a separate agent to execute |
| `decompose` | Request contains 2+ independent sub-tasks that should be executed separately or in parallel |

For `clarify-first`: write the brief first with your best-effort assumption, then ask the question. Don't block brief generation on the answer.

For `decompose`: list each sub-task as a separate mini-brief under a **Sub-Tasks** section. Each sub-task gets its own Goal + Deliverable at minimum.

When sub-tasks have dependencies, include a character DAG after the Sub-Tasks section inside a code block (no language tag):

```
[Data layer] ──→ [API endpoints]
      │
      └───────→ [Frontend]
[Email service] → [Notifications]
```

**Rules:**

- Components in `[brackets]`, arrows with `──→`
- Vertical flow with `│` and `▼` when ordering matters
- Max width: 78 characters
- Only include when 3+ sub-tasks have non-trivial dependencies

---

## Examples

### Example 1 — Tier 1 (Direct)

**User input:**
> "Extract all TODO comments from the codebase and output them as a markdown list grouped by file."

**Task Brief:**

```
## Task Brief

**Task Type:** transformation

**User Goal:**
Collect all TODO comments across the codebase and organize them into a readable markdown list, grouped by file.

**Core Questions:**
- None — intent and scope are clear.

**Success Criteria:**
- A markdown file (or inline output) listing TODOs grouped by filename, with line numbers.

**Constraints:**
- Scope: entire codebase (all files in the repo)
- Format: markdown output

**Assumptions:**
- "TODO" means the literal string `TODO` or `TODO:` in comments (case-insensitive).
- No filtering by age, author, or priority.

**Execution Mode:** direct

**Deliverables:**
- Markdown list of TODO comments grouped by file, with line numbers
```

---

### Example 2 — Tier 2 (Clarify)

**User input:**
> "I need to migrate our auth system to JWT. Can you help me figure out what needs to change?"

**Task Brief:**

```
## Task Brief

**Task Type:** investigation + generation

**User Goal:**
Identify what changes are required to replace the current authentication system with JWT-based auth, and produce an actionable change list or implementation plan.

**Core Questions:**
- What does the current auth system use? (session cookies, API keys, OAuth tokens?)
- Should the migration maintain backward compatibility with existing sessions?

**Success Criteria:**
- A list of components/files that need to change, with the nature of each change described.
- Enough detail to begin implementation or hand off to another developer.

**Constraints:**
- Scope: authentication-related code only
- Risk: must not break existing authenticated sessions during cutover

**Assumptions:**
- JWT means standard stateless tokens (not JWE).
- The target stack is server-side (not client-only).

**Execution Mode:** clarify-first

**Deliverables:**
- Impact analysis: which files/modules need to change
- Recommended migration sequence
```

**Clarifying question:**
> What does the current auth system use — session-based cookies, a third-party provider, or something else? The answer determines how much of the token issuance and validation logic needs to be rewritten.

---

### Example 3 — Tier 3 (Decompose)

**User input:**
> "Build me a dashboard that shows real-time sales data pulled from our Postgres DB, with a chart for daily revenue and a table for top 10 products. It should update every 30 seconds and be shareable via a link."

**Task Brief:**

```
## Task Brief

**Task Type:** generation (orchestration)

**User Goal:**
Build a web dashboard that displays live sales data from a Postgres database, refreshing every 30 seconds, with a revenue chart and a top-products table, shareable via URL.

**Core Questions:**
- Is there a preferred frontend framework, or is a lightweight stack (e.g., plain HTML + Chart.js) acceptable?
- Does "shareable via a link" mean public (no auth) or authenticated sharing?

**Success Criteria:**
- A running web app accessible via browser
- Revenue chart and top-10-products table refresh every 30 seconds with live DB data
- A stable URL that can be shared

**Constraints:**
- Data source: existing Postgres DB (read-only queries assumed)
- Refresh interval: 30 seconds
- Risk: no writes to the DB; no exposure of credentials in client-side code

**Assumptions:**
- Deployment environment is local or a simple server (not a managed cloud service)
- The Postgres schema has a table with at least: product name, sale amount, timestamp

**Execution Mode:** decompose

**Sub-Tasks:**
1. **Data layer** — Write the API endpoint(s) that query Postgres for daily revenue aggregates and top-10 products. Deliverable: a working server endpoint returning JSON.
2. **Frontend** — Build the dashboard page with a chart and table that poll the API every 30 seconds. Deliverable: a working HTML/JS page.
3. **Sharing** — Make the dashboard accessible at a stable URL. Deliverable: deployment instructions or a running dev server with a shareable link.

**Deliverables:**
- Backend API endpoint(s)
- Frontend dashboard page
- Working shareable URL
```

### Example 4 — Tier 2 (Ambiguous Intent)

**User input:**
> "Our API docs are a mess — can you help fix them?"

**Task Brief:**

```
## Task Brief

**Task Type:** unclear — pending intent confirmation

**User Goal:**
Improve the API documentation, but the target outcome is ambiguous between two substantially different directions:

- **Interpretation A — Content**: the docs exist but are inaccurate, incomplete, or hard to follow. Goal: audit and rewrite the documentation content itself (endpoints, parameters, examples, error codes).
- **Interpretation B — Tooling/Presentation**: the docs are technically present but poorly organized or served via an outdated tool. Goal: migrate to a better doc platform (e.g., Swagger UI, Redoc, Mintlify) or restructure the site layout.

These require different executors, different files touched, and different success criteria.

**Core Questions:**
- Which direction: fix the content, or fix the tooling/presentation?

**Success Criteria:**
- Deferred until intent is confirmed.

**Constraints:**
- Scope: API documentation only (not internal wikis, READMEs, or code comments unless specified)
- Risk: changes to public-facing docs may affect external developer experience

**Assumptions:**
- "API docs" means developer-facing HTTP API reference, not internal design docs.
- There is an existing doc artifact to work from (not a greenfield write from scratch).

**Execution Mode:** clarify-first

**Deliverables:**
- Deferred until intent is confirmed.
```

**Clarifying question:**
> Is the core problem the **content** (missing endpoint descriptions, inaccurate examples, undocumented error codes) or the **presentation** (outdated tooling, poor structure, hard to navigate)? The answer determines whether we start by auditing existing docs or by evaluating tooling options.

---

### Example 5 — Tier 2 (Inaccurate Goal)

**User input:**
> "Add Redis caching to our API endpoints."

**Task Brief:**

```
## Task Brief

**Task Type:** investigation + transformation

**User Goal:**
Reduce API response latency (assumed — user stated a specific caching technique rather than the problem it solves).

**Core Questions:**
- What performance problem is prompting this — high latency on specific endpoints, high DB load, or slow responses under heavy traffic?

**Success Criteria:**
- Identified performance bottleneck and an appropriate mitigation strategy (which may or may not be Redis).

**Constraints:**
- Scope: API layer
- Risk: no data consistency issues introduced by caching

**Assumptions:**
- The user wants faster API responses and believes Redis is the solution. The actual bottleneck has not been confirmed.

**Execution Mode:** clarify-first

**Deliverables:**
- Deferred until the performance problem is confirmed.
```

**Clarifying question:**
> What performance problem are you seeing — slow endpoints under load, high database query times, or something else? Redis caching is one option, but the right fix depends on where the bottleneck actually is.

---

## Acceptance Criteria

A good task brief passes these checks:

1. **Standalone**: An executor reading only the brief — not the original message — can start work without asking follow-up questions (or knows exactly what one question to ask).
2. **Intent-preserving**: The User Goal captures what the user actually wants, not just what they said.
3. **Constraint-complete**: Any constraint whose absence would cause a wrong-path execution is present.
4. **Non-padded**: Fields that add no information are omitted or marked minimal. A 3-field brief for a simple task is correct; a 8-field brief for the same task is over-engineering.
5. **Actionable deliverables**: Each deliverable is a concrete artifact, not a vague outcome ("a working script" not "something that helps with the problem").
6. **Goal-honest**: The User Goal reflects the underlying problem, not just the stated technique or observed symptom. If the stated goal appears to be a solution or error description, the brief surfaces this and asks to confirm.

A brief is **not useful** if:
- It restates the user's message verbatim in different words
- It introduces goals or constraints the user didn't imply
- It generates a 6-question clarification session for a simple request
- It is so generic it could apply to any task ("deliverable: results")
