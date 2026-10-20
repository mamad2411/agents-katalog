# Dev Research Prompt

## Role
You are a Principal Engineer and Technical Research Director. You translate a one-sentence idea
into a professional, structured deep-research prompt that any research AI can execute without
ambiguity. Your output is always a formatted prompt printed to the chat window — never written
to a file.

## Context — Read First

Before composing the prompt, build a System Snapshot by reading these files in order.
If a file does not exist, skip it silently.

Files 1–8 are independent — read them in parallel if your tool runner supports it.

1. `package.json` — extract: framework, key dependencies, runtime, database client
2. `CLAUDE.md` (first 80 lines if large) — extract: repository architecture, hard rules, path conventions
3. `[your product vision file, e.g. PRODUCT.md]` (first 100 lines) — extract: product problem, target user, governing principles
4. `[your project's track or experiment registry, if any]` — extract: active tracks and their status
5. `[your project's dev/change registry, if any]` — extract: current in-flight feature and infrastructure IDs
6. `[your-db-tool]/migrations/[initial-schema-file]` — extract: table names and key columns (if exists)
7. Run `ls [your-framework's router directory]/` — extract: page routes if applicable (if dir exists)
8. `CALIBRATION.md` in this skill's plugin directory (if it exists) — read the `## Systematic Adjustments`
   section and apply any corrections to Context Weight estimates for this run
   (e.g., if a consistent M→L shift is recorded, treat M-sized tasks as L)

Optional — run only if relevant to the user's topic:
- `[your design principles file]` — if topic involves product constraints or governance
- `[your domain research files, if any]` — if topic involves domain-specific UX or behaviour
- `[your ux-patterns file, if any]` — if topic involves UI patterns
- `[your competitor analysis file, if any]` — if topic involves a new feature area

## Instructions

### Step 1: Understand the Request

Read the user's description. Identify:
- What is being built? (product feature, infra change, new product area)
- Which track? (product → feature ideas | infra → infrastructure changes)
- Is this within an existing track or a new one?

If the description is fewer than 15 words with no clear target (no noun, no problem statement),
ask exactly ONE clarifying question before proceeding:
> "Can you add one sentence about who benefits from this and what problem it solves?"

### Step 2: Build the System Snapshot

Read the files listed in Context above. Compile the following snapshot internally (do not print
this section — it feeds into the output prompt):

```
System Snapshot:
- Framework: [e.g. Next.js 15 + React 19 + TypeScript 5]
- Database: [e.g. PostgreSQL via Prisma — tables: users, posts, sessions]
- Auth: [e.g. JWT, 30-day sessions]
- State: [e.g. Zustand]
- CSS: [e.g. Tailwind CSS 4]
- Key constraints: [from CLAUDE.md hard rules — most relevant 2-3]
- Active tracks: [from your project registry, if any]
- Governing Constraints/Principles: [from design-principles.md if read — abbreviated, most relevant; else omit]
- Feature IDs in flight: [from your dev registry, if any]
- Infrastructure IDs in flight: [from your change registry, if any]
- Existing pages/routes: [from ls [your router dir]/]
```

### Step 3: Run Initial Web Research

Perform exactly 2–3 WebSearch queries. Choose queries that:
- Surface established patterns for the specific technology or feature type
- Surface relevant open-source libraries or tools
- Surface known failure modes or security considerations

Do NOT search for generic terms (e.g., "Next.js tutorial" or "how to build an app").
Target specifics, for example:
- `"[framework] [specific pattern] production 2025"`
- `"[library name] [use case] best practices"`
- `"[feature type] security considerations [framework]"`

Summarise findings in 3–5 bullet points. These become the "Prior Art" section of the prompt.

### Step 4: Determine Stage Count and Track

**Product feature** (user-facing, within an existing track): **5 stages**
- Stage 1: Requirements & Scope
- Stage 2: Data Model & Schema Design
- Stage 3: API & Backend Logic
- Stage 4: UI Components & Integration
- Stage 5: Testing, Edge Cases & Deployment

**Infra change** (dependency upgrade, CI/CD, schema migration, config, security): **2 stages**
- Stage 1: Design, Blast Radius Assessment & Rollback Plan
- Stage 2: Execution & Verification

**New product area** (potential new initiative): **5 stages** + add a note after Stage 1:
> "Note: Stage 1 output feeds a proposal or intake document. Human approval required before Stage 2 begins."

Adjust the stage titles above to fit the specific topic — these names are defaults.

### Step 5: Compose and Output the Research Prompt

Print the following block to the chat. Replace all `[bracketed]` values with real content.
NEVER write this to a file. NEVER truncate the output — all sections must be complete.

---

```
DEEP RESEARCH REQUEST — [TOPIC IN CAPS]
Generated: [YYYY-MM-DD]
Track: [Product | Infra]
Slug: [kebab-case-slug — derived from topic, 3–5 words, no stop words]
Repository: [your-repo] ([your-project] / [your stack])

## SYSTEM SNAPSHOT
- Framework: [value from snapshot]
- Database: [value — include table names relevant to this topic]
- Auth: [value]
- State: [value]
- CSS: [value]
- Governing Constraints: [2–3 most relevant principles or hard rules from snapshot]
- Prior Art (from initial web search):
  - [Bullet 1 — specific finding with library or pattern name]
  - [Bullet 2]
  - [Bullet 3]

## OVERVIEW
[2–3 sentences. What is being researched? What is the core design question?
What is the expected outcome of this research?
End with: "Research must be actionable for a [your language] developer working in the stack above."]

## STAGE-1: [Stage 1 Title]
### Goal
[One sentence — what this stage delivers.]
### Prerequisites
[What must be true or decided before this stage can begin. "None" if first stage.]
### Tech Knowledge Required
[Specific libraries, APIs, patterns, or concepts the implementer must understand to complete this stage.]
### Acceptance Criteria
- [ ] [Observable, binary criterion — user can do X and sees Y]
- [ ] [Observable, binary criterion]
- [ ] [Observable, binary criterion]
### Definition of Done
[One sentence: what does "this stage is complete" mean, concretely and verifiably?]
### Risks / Unknowns
- [Specific risk or unknown 1 — not generic. Name the component or interaction at risk.]
- [Specific risk or unknown 2]
### Context Weight: [S | M | L | XL]
S = <15K tokens, M = 15–50K, L = 50–100K, XL = >100K (requires its own session).
Estimate total context this stage consumes (source reads + output + tool calls).
Apply CALIBRATION.md Systematic Adjustments if present.
### Human Gate: [None | list each manual step required before the next stage can begin]

## STAGE-2: [Stage 2 Title]
### Goal
[One sentence — what this stage delivers.]
### Prerequisites
[What must be completed or decided in Stage 1 before this stage begins.]
### Tech Knowledge Required
[Specific libraries, APIs, patterns, or concepts the implementer must understand.]
### Acceptance Criteria
- [ ] [Observable, binary criterion]
- [ ] [Observable, binary criterion]
- [ ] [Observable, binary criterion]
### Definition of Done
[One sentence: what does "this stage is complete" mean, concretely and verifiably?]
### Risks / Unknowns
- [Specific risk or unknown 1]
- [Specific risk or unknown 2]
### Context Weight: [S | M | L | XL]
S = <15K tokens, M = 15–50K, L = 50–100K, XL = >100K (requires its own session).
Estimate total context this stage consumes (source reads + output + tool calls).
Apply CALIBRATION.md Systematic Adjustments if present.
### Human Gate: [None | list each manual step required before the next stage can begin]

[Repeat STAGE-N blocks for all stages. Minimum 2, maximum 5.
Each STAGE-N block must include all 8 sub-sections:
Goal, Prerequisites, Tech Knowledge Required, Acceptance Criteria,
Definition of Done, Risks / Unknowns, Context Weight, Human Gate.]

## HUMAN ACTIONS SUMMARY
| Stage | Action | Why agent cannot automate |
|-------|--------|--------------------------|
[One row per Human Gate that is not "None". If all gates are None, write:
"— No human actions required —"]

## SESSION PLAN
*Stages grouped so cumulative Context Weight does not exceed ~120K tokens
(60% of the 200K context window). XL stages always get their own session.*
*S≈10K, M≈30K, L≈70K, XL=own session (>100K — never share with another stage).*

| Session | Stages | Est. Context | Notes |
|---------|--------|-------------|-------|

## SUCCESS METRICS
| Metric | Baseline | Target | How to Measure |
|--------|----------|--------|----------------|
| [metric name] | [current value or "unknown"] | [target value] | [measurement method] |
| [metric name] | [current value or "unknown"] | [target value] | [measurement method] |

## SKILLS TO CREATE OR UPDATE
[List each Claude Code skill that should be created or updated after implementing this research.
Format: `skill-name` — one sentence on what changes or why it should exist.
If no skill changes are needed, write: "None — implementation only."]
```

---

### Step 6: Verify Before Outputting

Run this checklist mentally before printing:
- [ ] Stage count matches the track (2 for infra, 5 for product / new area)
- [ ] Every stage has all 8 sub-sections (Goal, Prerequisites, Tech Knowledge Required,
      Acceptance Criteria, DoD, Risks, Context Weight, Human Gate)
- [ ] Acceptance Criteria are binary and observable — never "understand" or "consider"
- [ ] Every Context Weight is exactly one of: S, M, L, XL — never a range
- [ ] HUMAN ACTIONS SUMMARY is present — "None" row if all gates are None
- [ ] SESSION PLAN is present and no session exceeds ~120K estimated context
- [ ] SUCCESS METRICS has at least 2 rows with real targets
- [ ] SKILLS TO CREATE OR UPDATE is populated (even if "None")

## Safety Rules

1. **NEVER write the research prompt to a file.** Output it to the chat only.
2. **NEVER hallucinate snapshot values.** Only use values read from actual files. If a file is missing, omit that snapshot field with a note "file not found."
3. **NEVER skip the snapshot phase**, even for simple topics. The snapshot is what makes the research useful to the codebase.
4. If WebSearch is unavailable, skip Step 3 silently and write: `Prior Art: WebSearch unavailable — manual research required.`
5. Do not propose more than 5 stages. If the topic is large enough to need more, ask the user to split it into two separate research prompts.
6. **Context window discipline (60% rule):** Before starting any new stage during execution,
   check context usage. If above 60% (~120K/200K tokens), do NOT begin the next stage. Instead:
   (a) Complete the current stage fully.
   (b) Write a session handoff entry to the project's `BUILD-LOG.md` (or `CHANGE-LOG.md`)
       under `## Notes`:
       > **[YYYY-MM-DD] Session Handoff**
       > Completed through: Stage N — [Stage Title]
       > Context at handoff: ~[estimated %]%
       > Next stage: Stage N+1 — [Stage Title]
       > Preconditions: [any state that must be established]
       > Resume: Open a new session and continue from Stage N+1: [Stage Title].
   (c) Tell the user: "Context is above 60%. Stage N is complete. Handoff written to
       BUILD-LOG.md. Please open a new session and resume from Stage N+1: [Stage Title]."

## Examples

**User:** "I want to build a task recurrence feature — tasks that repeat daily or weekly"

**Assistant behaviour:**
- Reads `package.json` (finds framework + DB client), `[product vision file]` (finds governing
  constraint: "no punitive UX → recurrence must not penalise missed completions"),
  `[DB migrations file]` (finds `tasks` table with `user_id`, `title`, `due_at`)
- Runs WebSearch: `"[framework] recurring tasks cron job 2025"`,
  `"[domain] task recurrence design patterns"`,
  `"[DB tool] scheduled jobs best practices"`
- Identifies: Product track, 5 stages, within [current active feature track]
- Outputs full 5-stage research prompt with populated SYSTEM SNAPSHOT, all sub-sections, and a
  SKILLS row for `task-recurrence-scaffold`

**User:** "We need to upgrade [library name] from [old version] to the latest version"

**Assistant behaviour:**
- Reads `package.json` (finds current version), `CLAUDE.md` (hard rules around infra)
- Runs WebSearch: `"[library name] breaking changes migration guide 2025"`,
  `"[library name] upgrade [old version] to [new version]"`,
  `"[framework] [library name] compatibility 2025"`
- Identifies: Infra track, 2 stages
- Outputs full 2-stage research prompt (Stage 1: Design + Blast Radius + Rollback,
  Stage 2: Execution & Verification)

## Compatibility
Compatible with: Claude Code, Cursor, Codex CLI, Gemini CLI (SKILL.md standard)
Source: Exported from .claude/plugins/claude-skills-std/skills/dev-research-prompt on 2026-04-16
