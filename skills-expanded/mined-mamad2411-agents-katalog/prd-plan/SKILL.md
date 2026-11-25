---
name: prd-plan
description: Create or audit a Product Requirements Document — the master plan that all sprints trace back to. Required before any sprint can be generated. Use when starting a new project, planning a product, or when asked to create/review a PRD.
---

# PRD Plan

Create, extend, or audit a Product Requirements Document. The PRD is the master document that every sprint traces back to. No sprint can be generated without a complete PRD.

---

## Gate

Before anything else, check that `RALPH.md` exists in the project root.

- **If RALPH.md is missing:** Stop immediately. Tell the user:
  > "RALPH.md not found. Run `/ralph-init` first to set up ralph in this project."
- **If RALPH.md exists:** Read it. Pull out the `Project.Name`, `Project.Type`, and `Documents.prd` path. Use these throughout — do not re-ask questions that RALPH.md already answers.

---

## Step 1: First Question

Ask exactly this:

```
What are you planning?

1. A new product from scratch
   A. I have a rough idea
   B. I have a detailed vision
   C. I just have a problem statement

2. A new feature for an existing project
   A. Small feature (1-2 sprints)
   B. Large feature (3+ sprints)
   C. Not sure yet

3. I have a PRD already
   A. It's in this repo
   B. I'll paste it in
   C. It's at a URL
```

The user can respond with shorthand like "1A", "2B", "3A" for quick selection.

---

## Path 1: New Product from Scratch

Deep structured conversation. Ask one question at a time. Wait for the answer before moving on. Use lettered options wherever possible so the user can reply quickly (e.g., "A", "1B", etc.).

### 1.1 Vision

```
What are you building?

A. A web application
B. A mobile app
C. A CLI tool
D. An API / backend service
E. A library or SDK
F. Something else: [please describe]
```

Then follow up:

- "What problem does this solve? Who has this problem today?"
- "Why does this need to exist? What happens if it doesn't get built?"
- "Is there a one-sentence summary? (e.g., 'Trello for pet owners' or 'CLI that generates database migrations from plain English')"

Capture the answers. You will use them to write the Overview section.

### 1.2 Users

```
Who are your target users?

A. Developers / technical users
B. Non-technical end users (consumers)
C. Business users / teams
D. Both technical and non-technical
E. Other: [please describe]
```

Then:

- "Describe 1-3 specific user personas. For each: who are they, what are they trying to accomplish, and what frustrates them today?"
- If the user is unsure, help them by suggesting personas based on the problem statement. Offer options:

```
Based on what you've described, here are some possible personas:

A. [Persona A] — [short description of goals and pain points]
B. [Persona B] — [short description of goals and pain points]
C. [Persona C] — [short description of goals and pain points]
D. All of the above
E. Different personas: [please describe]
```

### 1.3 Core Features

Walk through features one at a time. Start by asking:

- "What are the main things a user can DO with this product? List them out, even if rough."

For each feature the user mentions, dig in:

```
Let's define [Feature Name]:

1. What does this feature do in one sentence?
2. What are the key requirements?
   A. Must-have for v1
   B. Nice-to-have for v1
   C. Save for later
3. Are there any edge cases or constraints?
```

Keep going until the user says they've covered everything. Then confirm:

```
Here's what I have so far:

1. [Feature 1] — [summary] (v1)
2. [Feature 2] — [summary] (v1)
3. [Feature 3] — [summary] (later)
...

Does this look right? Anything to add, remove, or re-prioritize?
```

### 1.4 Scope & Non-Goals

```
What is this product explicitly NOT?

A. Not a replacement for [existing tool]
B. Not a platform — just a single-purpose tool
C. Not a multi-user system (single user only for v1)
D. Not handling [specific concern like payments, auth, etc.] in v1
E. Other boundaries: [please describe]
```

Then ask: "What features might people expect that you are intentionally leaving out of v1?"

Non-goals are critical. They prevent scope creep during sprints.

### 1.5 Data Model

```
What are the main "things" (entities) in your system?

For example, if you're building a task manager, the entities might be:
- User (email, name, role)
- Project (name, description, owner)
- Task (title, status, priority, assignee)

List your key entities with their most important fields.
```

If the user is unsure, derive entities from the features discussed earlier. Propose a model and ask for confirmation:

```
Based on your features, here's a suggested data model:

- [Entity 1]: [field1], [field2], [field3]
- [Entity 2]: [field1], [field2], [field3]
- Relationships: [Entity 1] has many [Entity 2], etc.

Does this look right? What's missing or wrong?
```

### 1.6 Tech Stack

First, check if there's already code in the project directory. If files exist, scan them to detect the stack (package.json, requirements.txt, go.mod, Cargo.toml, etc.) and confirm with the user.

If no code exists:

```
What tech stack are you planning to use?

Frontend:
A. React / Next.js
B. Vue / Nuxt
C. Svelte / SvelteKit
D. No frontend (API / CLI only)
E. Other: [please specify]

Backend:
A. Node.js / Express / Fastify
B. Python / FastAPI / Django
C. Go
D. Ruby / Rails
E. Other: [please specify]

Database:
A. PostgreSQL
B. SQLite
C. MongoDB
D. Supabase (Postgres + Auth + Realtime)
E. Other: [please specify]

Hosting:
A. Vercel
B. Railway / Render
C. AWS
D. Self-hosted
E. Not sure yet
```

### 1.7 Success Criteria

```
How will you know this product is working?

A. Users can complete [specific workflow] end-to-end
B. [Metric] reaches [target] (e.g., "100 signups in first month")
C. Replaces [existing manual process]
D. Passes all acceptance criteria in the PRD
E. Other: [please describe]
```

Ask for 2-4 concrete success criteria. They should be specific and verifiable, not vague ("users like it" is bad; "users can create and share a project in under 2 minutes" is good).

---

## Path 2: New Feature for Existing Project

Lighter conversation — most context already exists. The codebase IS the context.

### 2.1 Gather Context Automatically

Before asking any questions:

1. **Scan the codebase** — look at the directory structure, key files (package.json, README, src/ layout). Understand the existing stack, patterns, and architecture.
2. **Read existing docs** — check CLAUDE.md, AGENTS.md, README.md, and any existing PRD at the path specified in RALPH.md.
3. **Summarize what you found** to the user:

```
Here's what I see in your codebase:

- Stack: [detected stack]
- Structure: [key directories and patterns]
- Existing features: [what's already built]
- Current PRD: [exists / doesn't exist]

Does this look right? Anything I'm missing?
```

### 2.2 Define the Feature

```
What feature are you adding?

1. What does it do in one sentence?
2. Who benefits from this feature?
   A. Existing users — solves a pain point
   B. New users — lowers the barrier to entry
   C. Admin / power users
   D. Developers / API consumers
   E. Other: [please describe]
3. Why now? What's driving this?
```

### 2.3 Scope

```
What's included in this feature?

A. New UI screens / pages
B. New API endpoints
C. Database changes (new tables, new columns)
D. Changes to existing features
E. All of the above
F. Other: [please describe]
```

Then: "What is explicitly NOT included? What might someone expect that you're leaving out?"

### 2.4 Technical Approach

Based on the codebase scan, ask targeted questions:

- "Will this need new database tables or changes to existing ones?"
- "Which existing components / modules does this build on?"
- "Any new dependencies or services needed?"
- "Does this change any existing API contracts?"

### 2.5 Dependencies

- "What existing code does this feature depend on?"
- "Are there any features that must be built before this one?"
- "Does this feature block or affect any other planned work?"

### 2.6 Generate

Generate `docs/PRD.md` (or append a feature section to an existing PRD if one already exists). Use the same output format as Path 1, scaled down to the feature scope.

If appending to an existing PRD, add a new feature section following the existing numbering pattern.

---

## Path 3: Audit Existing PRD

### 3.1 Get the PRD

Based on the user's sub-choice:
- **3A (in this repo):** Read the file at the path in `RALPH.md` Documents.prd. If not set, ask for the path.
- **3B (paste it in):** Ask the user to paste the PRD content.
- **3C (at a URL):** Fetch the URL and read the content.

### 3.2 Completeness Checklist

Read the PRD and evaluate it against each criterion. Walk through gaps ONE AT A TIME — do not dump all issues at once.

**Checklist:**

```
Auditing your PRD against ralph's completeness checklist:

1. Problem / Vision
   - Does it clearly state what's being built?          [pass/fail]
   - Does it explain WHY it needs to exist?              [pass/fail]

2. Target Users
   - Does it identify who the users are?                 [pass/fail]
   - Does it include personas with goals/pain points?    [pass/fail]

3. Features
   - Does it list features with specific requirements?   [pass/fail]
   - Is each feature detailed enough to generate
     user stories from?                                  [pass/fail]
   - Are features numbered for reference?                [pass/fail]

4. Scope
   - Does it define non-goals (what's NOT included)?     [pass/fail]
   - Does it distinguish v1 from later versions?         [pass/fail]

5. Data Model
   - Does it define key entities and relationships?      [pass/fail]
   - Are fields and types specified?                     [pass/fail]

6. Tech Stack
   - Does it specify the technology choices?             [pass/fail]

7. Success Criteria
   - Does it define how to measure success?              [pass/fail]
   - Are criteria specific and verifiable?               [pass/fail]

8. Open Questions
   - Are unresolved questions captured?                  [pass/fail]
```

### 3.3 Fill Gaps

For each item that failed, ask the user the relevant question (using the same lettered-option format from Path 1). One gap at a time. Wait for the answer before moving to the next gap.

### 3.4 Rewrite

Once all gaps are filled, rewrite the PRD into ralph's standard format (see Output Format below). Show the user the rewritten version and ask for approval before saving.

---

## Output Format

Write the PRD to `docs/PRD.md` (or the path configured in RALPH.md Documents.prd).

Use this exact structure:

```markdown
# [Product/Feature Name]

## 1. Overview
[Problem statement and vision — what you're building and why it needs to exist.
Be specific. A reader should understand the product after reading just this section.]

## 2. Target Users
### Persona 1: [Name/Role]
- **Who they are:** [description]
- **Goals:** [what they want to accomplish]
- **Pain points:** [what frustrates them today]

### Persona 2: [Name/Role]
- **Who they are:** [description]
- **Goals:** [what they want to accomplish]
- **Pain points:** [what frustrates them today]

## 3. Features

### 3.1 [Feature Name]
[What this feature does in one sentence.]

**Requirements:**
- FR-3.1.1: [Specific, numbered requirement]
- FR-3.1.2: [Another requirement]
- FR-3.1.3: [Another requirement]

**Priority:** v1 / later

### 3.2 [Feature Name]
[What this feature does in one sentence.]

**Requirements:**
- FR-3.2.1: [Specific, numbered requirement]
- FR-3.2.2: [Another requirement]

**Priority:** v1 / later

### 3.3 [Feature Name]
...

## 4. Data Model

### [Entity Name]
| Field | Type | Description |
|-------|------|-------------|
| id | uuid / int | Primary key |
| [field] | [type] | [description] |

**Relationships:**
- [Entity A] has many [Entity B]
- [Entity B] belongs to [Entity A]

## 5. Tech Stack
- **Frontend:** [framework, language]
- **Backend:** [framework, language]
- **Database:** [database]
- **Hosting:** [platform]
- **Other:** [any other services, APIs, tools]

## 6. Non-Goals
[What this project will NOT include. This section is critical for preventing scope creep during sprint planning.]

- Will NOT [specific exclusion]
- Will NOT [specific exclusion]
- Will NOT [specific exclusion]

## 7. Success Criteria
[How you know the product is working. Must be specific and verifiable.]

- [ ] [Specific measurable criterion]
- [ ] [Specific measurable criterion]
- [ ] [Specific measurable criterion]

## 8. Open Questions
[Unresolved questions that need answers before or during implementation. Resolve these before generating sprints if possible.]

- [ ] [Question 1]
- [ ] [Question 2]
```

---

## Writing for Junior Developers

The PRD reader may be a junior developer or an AI agent executing stories. Therefore, every section must follow these rules:

1. **Be explicit and unambiguous.** "The system should handle errors" is too vague. "When the API returns a 4xx error, display the error message from the response body in a red toast notification that auto-dismisses after 5 seconds" is explicit.

2. **Avoid jargon or explain it.** If you must use domain-specific terms, define them the first time they appear. Example: "The system uses RBAC (Role-Based Access Control — users are assigned roles like 'admin' or 'viewer', and each role has specific permissions)."

3. **Provide enough detail to understand purpose and core logic.** Each feature section should answer: what does it do, why does it exist, and how should it behave in the common case.

4. **Number requirements for easy reference.** Every functional requirement gets a unique ID (FR-3.1.1, FR-3.2.3, etc.) so stories and acceptance criteria can reference them unambiguously.

5. **Use concrete examples where helpful.** Instead of "support various input formats," write "accept CSV, JSON, and XLSX files (see examples in /docs/examples/)."

6. **Define terms in context.** If the PRD says "the widget updates in real-time," clarify what real-time means: "within 500ms of the underlying data changing, without a page refresh (via WebSocket or Server-Sent Events)."

7. **State the obvious.** What's obvious to the product owner may not be obvious to the implementer. If a form has validation, list every validation rule. If a list is sorted, state the sort order.

---

## After Writing the PRD

Once the PRD is saved:

1. **Update RALPH.md** — set `Documents.prd` to point to the new PRD file path (e.g., `docs/PRD.md`).

2. **Confirm with the user:**

```
PRD saved to docs/PRD.md
Updated RALPH.md to point to the new PRD.

Next step: Run /new-sprint to generate your first sprint from this PRD.
```

3. **Note on acceptance criteria:** `/new-sprint` will translate your numbered requirements (FR-X.Y.Z) into acceptance criteria for each story. The PRD itself doesn't need to specify AC shape — but be aware that in v2, ACs are object-form (`{ text, humanGated? }`) and any requirement that needs the operator to take action on a third-party system (dashboards, real devices, app store portals) should be phrased so the sprint generator can flag it `humanGated: true`. State plainly when something needs human verification rather than burying it in passing prose.

3. **Do NOT start implementing.** The PRD is a planning document. Implementation happens through `/new-sprint` and the Ralph loop.

---

## Conversation Style

- Ask **one question at a time**. Do not dump all questions at once.
- Use **lettered options** wherever possible for quick responses.
- After each answer, **reflect it back** briefly ("Got it — you're building a CLI for...") before asking the next question.
- If the user gives a long freeform answer, **extract the structured data** from it and confirm.
- If the user says "I don't know" or "not sure," **suggest reasonable defaults** with options to override.
- Keep the conversation moving. Don't over-ask. If the user's initial description is detailed enough to cover a section, skip the questions for that section and confirm instead.

---

## Checklist

Before saving the PRD, verify:

- [ ] Overview clearly states what's being built and why
- [ ] At least 1 user persona with goals and pain points
- [ ] All features listed with numbered requirements (FR-X.Y.Z)
- [ ] Each feature marked as v1 or later
- [ ] Non-goals section defines clear scope boundaries
- [ ] Data model covers key entities with fields and relationships
- [ ] Tech stack is specified
- [ ] Success criteria are specific and verifiable
- [ ] Open questions are captured (even if none — state "None identified")
- [ ] Written clearly enough for a junior developer to understand
- [ ] RALPH.md Documents.prd path updated

If any item fails, go back and fill the gap with the user before saving.
