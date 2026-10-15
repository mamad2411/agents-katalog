---
name: stacksmith-plan
version: 1.0.0
description: "Planning gauntlet for any software project. Modes: ideate (define problem or vision), ceo (scope challenge), eng (architecture + convergence artifacts), design (UI quality review), auto (full run). Convergence artifacts — delivery-plan.md, AGENTS.md, CLAUDE.md, OpenSpec proposals — are built automatically at the end of eng. Trigger when planning a feature, starting a project, locking architecture, or reviewing scope before implementation."
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
  - WebSearch
---

## Command routing

Parse the user's invocation before doing anything else:

- `/stacksmith-plan ideate` -> run ideation mode
- `/stacksmith-plan ceo` -> run CEO mode
- `/stacksmith-plan eng` -> run engineering mode
- `/stacksmith-plan design` -> run design mode
- `/stacksmith-plan auto` -> run auto mode

If no mode is provided, ask which planning mode they want.

All timeline logs in this skill use:
- `skill: "stacksmith-plan"`
- `mode: "office-hours" | "plan-ceo" | "plan-eng" | "plan-design" | "autoplan"`

---

## Mode: `ideate`

### Preamble (run first)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")
echo "BRANCH: $_BRANCH"
echo "REPO: $_REPO"
_SLUG=$(git remote get-url origin 2>/dev/null | sed 's|.*[:/]\([^/]*/[^/]*\)\.git$|\1|;s|.*[:/]\([^/]*/[^/]*\)$|\1|' | tr '/' '-' | tr -cd 'a-zA-Z0-9._-' 2>/dev/null || basename "$PWD")
_DESIGN=$(ls -t ~/.mystack/projects/$_SLUG/*-$_BRANCH-design-*.md 2>/dev/null | head -1)
[ -n "$_DESIGN" ] && echo "DESIGN_DOC: $_DESIGN" || echo "DESIGN_DOC: none"
mkdir -p ~/.mystack/projects/$_SLUG
```

If `DESIGN_DOC` is not `none`: read it and offer to continue or start fresh.

### Mode selection

Ask via AskUserQuestion:

> "What are you working on? I can help you think through it."
>
> Options:
> - A) **Startup / product** - I'm building something people will pay for or use seriously
> - B) **Side project / learning** - hackathon, open source, personal tool, exploring an idea

### Mode A - Startup / Product

You are a demanding product advisor. Your job is to stress-test the idea and find the sharpest version, not validate what the user already thinks.

#### Phase 1 - Extract real pain

After the user describes what they want to build, ask at most 3 of these:

1. Pain sharpness - "What's the most painful moment in this workflow right now? Give me a specific example from last week, not a hypothetical."
2. Who suffers - "Who specifically has this problem? Name a real person if possible, not a persona type."
3. Current workaround - "What do they do today instead? Why isn't that good enough?"
4. Scope trap - "You described [large thing]. What's the 10% of that which solves 80% of the pain?"
5. Success metric - "How will you know in 2 weeks if this actually worked? What changes?"
6. Competitive honesty - "Why won't [the most obvious existing solution] fix this?"

After they answer: push back on their framing at least once. Say directly: "You said X, but what I'm actually hearing is Y. Is that right?"

#### Phase 2 - Reframe

State explicitly:
- 2-3 things the user did not realize they were describing
- 1-2 assumptions that might be wrong and what breaks if they are
- 1 completely different frame for the problem

Get agreement or pushback before continuing.

#### Phase 3 - Three implementation paths

| Path | Description | Effort (solo dev / with AI) | Risk | Choose if... |
|------|-------------|-----------------------------|------|--------------|
| **Narrow** | Smallest wedge that proves the hypothesis | Low / very low | Low | Hypothesis unvalidated |
| **Core** | The feature as described | Medium / low | Medium | Pain is confirmed real |
| **Bold** | Larger vision, fast execution | High / medium | High | You've shipped this type before |

State which path you recommend and the specific reason.

Anti-patterns:
- "Choose B because it covers 90% of the value" if A is only a bit more work
- "Defer edge cases to a follow-up" when the edge cases are cheap to reason through now

#### Phase 4 - Write design doc

Write to `~/.mystack/projects/<slug>/<date>-<branch>-design-<feature>.md`:

```markdown
# Design: [feature name]
_[date] - /stacksmith-plan ideate - [repo]:[branch]_

## Problem
[2-3 sentences: the real pain, who has it, why now]

## Reframe
[What the user said vs. what they were actually describing]

## Assumptions to validate
- [assumption 1] - risk if wrong: [consequence]
- [assumption 2] - risk if wrong: [consequence]

## Chosen approach
[Path name + why]

## Scope
**In:** [list]
**Out (explicitly):** [list]

## Success metric
[Measurable, 2-week horizon]

## Open questions
[Things to validate before or during build]

## Next step
Run `/stacksmith-plan ceo` to challenge scope, or `/stacksmith-plan eng` to lock architecture.
```

Tell the user: "Design doc saved. Run `/stacksmith-plan ceo` to challenge scope, or `/stacksmith-plan eng` to jump straight to architecture."

### Mode B - Side project / Builder

You are a brainstorming partner. Your job is to expand thinking and surface the most interesting version, not narrow it down.

#### Phase 1 - What's the vision?

Ask: "Tell me everything you're imagining - don't edit yourself yet."

After they describe: identify and name:
- the most interesting part of the idea
- the part that's technically novel or hard
- the part that could surprise you if it worked well

#### Phase 2 - Constraints inventory

Map the real constraints:
- **Time:** When do you want to have something working?
- **Tech:** What do you already know vs. what would you need to learn?
- **Fun factor:** What part of this do you actually want to build?

#### Phase 3 - Three directions

| Direction | Focus | Interesting because... | Effort |
|-----------|-------|------------------------|--------|
| **Minimal** | Core mechanic only | Proves the interesting part fast | Low |
| **Full vision** | Build the whole thing you described | Most satisfying if it works | High |
| **Twist** | Unexpected angle on the same idea | Could be more interesting | Medium |

No recommendation in this mode. Present all three as real options.

#### Phase 4 - Write design doc

Use the same format as Mode A, but:
- replace "Problem" with "Vision"
- replace "Success metric" with "Milestone: what does a working version look like?"
- add "Learning goals" if relevant

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-plan\",\"mode\":\"office-hours\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```

---

## Mode: `ceo`

### Preamble (run first)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")
_SLUG=$(git remote get-url origin 2>/dev/null | sed 's|.*[:/]\([^/]*/[^/]*\)\.git$|\1|;s|.*[:/]\([^/]*/[^/]*\)$|\1|' | tr '/' '-' | tr -cd 'a-zA-Z0-9._-' 2>/dev/null || basename "$PWD")
echo "BRANCH: $_BRANCH"
echo "REPO: $_REPO"
_DESIGN=$(ls -t ~/.mystack/projects/$_SLUG/*-$_BRANCH-design-*.md 2>/dev/null | head -1)
[ -z "$_DESIGN" ] && _DESIGN=$(ls -t ~/.mystack/projects/$_SLUG/*-design-*.md 2>/dev/null | head -1)
[ -n "$_DESIGN" ] && echo "DESIGN_DOC: $_DESIGN" || echo "DESIGN_DOC: none"
[ -f PLAN.md ] && echo "PLAN_FILE: PLAN.md" || echo "PLAN_FILE: none"
git log --oneline -10 2>/dev/null || true
grep -r "TODO\|FIXME\|HACK" -l --exclude-dir=node_modules --exclude-dir=.git . 2>/dev/null | head -10
```

If `DESIGN_DOC` is not `none`: read it. This is the source of truth.
If `PLAN_FILE` is `PLAN.md`: read it.
If both are `none`: ask the user to describe what they want to build.

### Pre-review system audit

Run before any review:

```bash
git log --oneline -20 2>/dev/null
git diff HEAD --stat 2>/dev/null | head -20
git stash list 2>/dev/null
cat TODOS.md 2>/dev/null | head -30
cat CLAUDE.md 2>/dev/null | head -20
```

Read any `ARCHITECTURE.md` or `docs/` files if they exist.

### Philosophy

You are not here to rubber-stamp the plan. You are here to:
- Find every landmine before it explodes
- Surface the 10-star version hiding in the plan
- Ensure the right scope is chosen before a single line of code is written

Critical rule: Never silently add or remove scope. Every scope change is an explicit opt-in via AskUserQuestion.

Prime directives:
1. Zero silent failures. Every failure mode must be visible. If a failure can happen silently, that is a critical plan defect.
2. Every error has a name. "Handle errors" is not acceptable. Name the specific exception, what triggers it, what catches it, what the user sees.
3. Data flows have shadow paths. Every flow has nil input, empty input, upstream error, and the happy path.
4. Interactions have edge cases. Double-click, navigate-away-mid-action, slow connection, stale state, back button.
5. Diagrams are mandatory. No non-trivial flow goes undiagrammed.
6. Everything deferred must be written down. TODOS.md or it does not exist.

### Step 0 - Mode selection (Nuclear Scope Challenge)

Read the plan. Then challenge the scope directly via AskUserQuestion:

> "I've read the plan. Before we go section by section, I want to challenge the scope.
> [1-2 sentences on what you observed about the scope: too big / too small / about right?]
>
> Which mode do you want for this review?"

Options:
- A) EXPANSION - Push scope up. Find the 10-star product hiding inside. Every expansion is an opt-in question.
- B) SELECTIVE EXPANSION - Hold baseline scope but surface expansion opportunities as individual opt-in questions.
- C) HOLD SCOPE - Make the plan bulletproof as-is. No additions, no cuts.
- D) REDUCTION - Cut ruthlessly. Find the minimum viable thing that achieves the core outcome.

After selection, commit to the mode. Do not silently drift.

### Ten-section review

Go through each section. For each: give `Problem / Weak / Strong` and one concrete improvement.

1. Problem clarity
- Is the pain specific and real, or vague and theoretical?
- Can you name the person who has this problem?
- Is "why now" articulated?

2. Who it's for
- Named, real person or vague persona?
- Do you know what they already tried?

3. Scope - what's in
- Is it the right size for available time?
- Does each item directly address the stated problem?
- EXPANSION only: surface 3 capabilities that could be included, each as a separate AskUserQuestion

4. Scope - what's explicitly out
- Is there a "not doing" list?
- Are there obvious things that could creep in?

5. Success metric
- Measurable within 2 weeks?
- Does it measure the outcome or just the output?

6. Assumptions
- What's assumed that has not been validated?
- What breaks if the top assumption is wrong?
- Flag any HIGH RISK assumption

7. 10-star version
- What does a truly great version of this look like?
- What would it take to get there from the current plan?

8. Minimum version
- What's the smallest thing you could ship tomorrow to learn something?

9. Failure modes and risks
- What's most likely to kill this?
- What's the fallback if the core assumption is wrong?
- Technical risks
- Adoption risks

10. Recommendation
- `SHIP AS-IS` / `REVISE FIRST` / `RECONSIDER ENTIRELY`
- One sentence of reasoning

### Scope decisions output

Write a scope decisions block to the design doc or `PLAN.md`:

```markdown
## CEO Review [date]
**Mode:** [EXPANSION / SELECTIVE / HOLD / REDUCTION]

### Scope decisions
**Accepted scope (added to plan):**
- [item] - reason

**Rejected scope (not doing):**
- [item] - reason

**Deferred to TODOS.md:**
- [item] - reason

### Section scores
1. Problem clarity: Strong/Weak/Problem - [one-line observation]
2. Who it's for: ...
[... all 10]

### Overall recommendation
[SHIP AS-IS / REVISE FIRST / RECONSIDER]
[One paragraph of reasoning]
```

Tell the user: "CEO review complete. Run `/stacksmith-plan eng` to lock architecture."

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-plan\",\"mode\":\"plan-ceo\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```

---

## Mode: `eng`

### Preamble (run first)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")
_SLUG=$(git remote get-url origin 2>/dev/null | sed 's|.*[:/]\([^/]*/[^/]*\)\.git$|\1|;s|.*[:/]\([^/]*/[^/]*\)$|\1|' | tr '/' '-' | tr -cd 'a-zA-Z0-9._-' 2>/dev/null || basename "$PWD")
echo "BRANCH: $_BRANCH"
echo "REPO: $_REPO"
_DESIGN=$(ls -t ~/.mystack/projects/$_SLUG/*-$_BRANCH-design-*.md 2>/dev/null | head -1)
[ -z "$_DESIGN" ] && _DESIGN=$(ls -t ~/.mystack/projects/$_SLUG/*-design-*.md 2>/dev/null | head -1)
[ -n "$_DESIGN" ] && echo "DESIGN_DOC: $_DESIGN" || echo "DESIGN_DOC: none"
[ -f PLAN.md ] && echo "PLAN_FILE: PLAN.md" || echo "PLAN_FILE: none"
[ -f Gemfile ] && echo "STACK:ruby"
[ -f package.json ] && echo "STACK:node"
[ -f requirements.txt ] || [ -f pyproject.toml ] && echo "STACK:python"
[ -f go.mod ] && echo "STACK:go"
[ -f Cargo.toml ] && echo "STACK:rust"
git log --oneline -15 2>/dev/null
cat TODOS.md 2>/dev/null | head -30
cat ARCHITECTURE.md 2>/dev/null | head -40
```

Read design doc and plan if they exist.

### Prime directives

1. Zero silent failures. Every failure mode must be visible.
2. Every error has a name. Name the specific exception, trigger, catcher, user-visible result, and whether it is tested.
3. Data flows have shadow paths: nil input, empty/zero input, upstream error, happy path.
4. Interactions have edge cases: double-click, navigate-away, slow connection, stale state, back button.
5. Diagrams are mandatory.
6. Deployments are not atomic. Plan for partial states, rollbacks, and feature flags.

### Step 1 - Read and understand the system

Run the system audit:

```bash
git log --oneline -20
git diff HEAD --stat 2>/dev/null | head -20
ls -d test/ tests/ spec/ __tests__/ 2>/dev/null
cat CLAUDE.md 2>/dev/null
```

Read all existing architecture docs before designing anything new.

### Step 2 - Architecture diagram

Draw an ASCII diagram showing:
- entry points
- data flow
- state transitions
- service boundaries
- trust boundaries
- storage

Example format:

```text
[Browser] --POST /api/payment--> [PaymentController]
                                   validate inputs
                                   [PaymentService] --> [Stripe API]
                                   [DB: payments] success/failure
                                   [EmailWorker] --> [Email]
                             (async)

Trust boundary: everything right of [PaymentController] is internal
State machine: pending -> processing -> succeeded | failed | refunded
```

### Step 3 - Error/rescue map (mandatory)

For every new operation that can fail, map:

| Operation | Exception/Error | Who catches it | What user sees | Tested? |
|-----------|-----------------|----------------|----------------|---------|
| Stripe charge | `Stripe::CardError` | PaymentService | "Card declined" + retry | Plan: yes |
| DB write | Connection timeout | ActiveRecord | 500 + alert | Plan: yes |
| Email send | SMTP failure | EmailWorker | Silent retry x3 | Plan: yes |

Anti-pattern: catch-all error handling such as `rescue StandardError` or `catch Exception` is a code smell. Call it out explicitly and require specific rescue clauses.

### Step 4 - Shadow path analysis

For every new data flow, trace all four paths:
- happy path
- nil/null/undefined input
- empty/zero/blank input
- upstream error

For each shadow path: does the plan handle it? If not, flag it.

### Step 5 - Edge cases: user interactions

For every user-facing interaction:

| Interaction | Edge case | Expected behavior | Covered in plan? |
|-------------|-----------|-------------------|-----------------|
| Form submit | Double-click | Debounce / idempotency key | ? |
| Long operation | User navigates away | Background job continues, result on return | ? |
| Payment flow | Browser closes mid-auth | Recoverable via pending state | ? |
| Any form | Session expires mid-fill | Graceful redirect, data preserved | ? |
| List view | 0 results | Empty state with CTA | ? |
| List view | 10,000+ results | Pagination enforced | ? |

Flag any `?` as a plan gap.

### Step 6 - Test matrix

| Test type | What to cover | Commands | Priority |
|-----------|---------------|----------|----------|
| Unit | Core business logic, every branch | `npm test` / `rspec` / `pytest` | P0 |
| Integration | DB/API contracts, error paths | same runner | P0 |
| E2E | Happy path + top 3 error paths | Playwright / Cypress / Capybara | P1 |
| Load | Estimated peak x3 | k6 / ab / wrk | P2 if prod |

Coverage goal: 100 percent of new code paths. Every branch in the architecture diagram needs a test.

Good test coverage means:
- behavior + edge cases + error paths
- not only happy paths
- not implementation-only tests

### Step 7 - Migration and deployment plan

If the change touches the DB or has a deployment dependency:

```bash
ls db/migrate/ 2>/dev/null | tail -5
ls migrations/ 2>/dev/null | tail -5
```

For each migration:
- Is it reversible?
- Can it run while old code is live?
- Does it lock tables?
- Does it require a data backfill?

Deployment order when old and new code must coexist:
1. Deploy migration
2. Deploy new code
3. Remove old compatibility code

### Step 8 - Write ENG.md

Write to project root:

```markdown
# Engineering Plan: [feature]
_[date] - /stacksmith-plan eng - [repo]:[branch]_

## Architecture
[ASCII diagram]

## Data flow
[Happy path]

## Error/rescue map
[Table]

## Shadow paths
[Per-flow analysis]

## Interaction edge cases
[Table]

## Test matrix
[Table]

## Migration plan
[If applicable]

## Implementation order
1. [First]
2. [Second]
3. [Third]

## Hidden assumptions (HIGH RISK flagged)
- [assumption] - risk: [consequence]
- HIGH RISK: [assumption] - would kill the feature if wrong

## Definition of done
- [ ] All tests pass (unit + integration + E2E)
- [ ] Every error path handled and tested
- [ ] Migration is reversible
- [ ] Deployed to staging, smoke-tested
- [ ] Docs updated
```

Tell the user: "ENG.md written. Establishing convergence artifacts now."

### Step 9 - Establish convergence artifacts (mandatory)

This step runs every time `eng` completes, whether it is a new project or an existing one.

Check for existing artifacts first:

```bash
[ -f delivery-plan.md ] && echo "DELIVERY_PLAN: exists" || echo "DELIVERY_PLAN: missing"
[ -f AGENTS.md ] && echo "AGENTS_MD: exists" || echo "AGENTS_MD: missing"
[ -f CLAUDE.md ] && echo "CLAUDE_MD: exists" || echo "CLAUDE_MD: missing"
cat delivery-plan.md 2>/dev/null | head -40
cat AGENTS.md 2>/dev/null | head -20
```

#### 9a - Create or update `delivery-plan.md`

Read [references/delivery-plan-guidelines.md](./references/delivery-plan-guidelines.md) before writing.

Use the phase, milestones, and implementation order from ENG.md to fill these required sections:

```md
# Delivery Plan

## Current Phase
## Stage Objective
## Active Workstreams
## Milestones
## Current Blockers
## Next Verifiable Output
## Next OpenSpec Change
## Decision Log
## Source Links
## Handoff Notes
```

Rules:
- State current phase in one line
- Keep it short enough that a new agent can scan it first and act second
- Must not become roadmap copy, launch copy, or a changelog dump

#### 9b - Create OpenSpec proposals for the active phase

Read [references/openspec-breakdown-guidelines.md](./references/openspec-breakdown-guidelines.md).

At phase kickoff: create the full proposal inventory before execution starts. Treat missing proposal coverage as non-convergent state.

Break implementation order items into small proposals — one verifiable result per proposal. Map each proposal to one milestone id. Name the first proposal directly in `delivery-plan.md` under `Next OpenSpec Change`.

**REQUIRED SUB-SKILL:** Use `openspec` for CLI commands, delta syntax, validation, and archive flow.

#### 9c - Create or update `AGENTS.md` and `CLAUDE.md`

Read [references/agent-context-files.md](./references/agent-context-files.md) first.

`AGENTS.md` must contain:
- required artifacts
- handoff expectations
- planning discipline
- update rules
- project-specific constraints

`CLAUDE.md` must contain only:

```md
Read `AGENTS.md` before doing any project work. Treat it as the project operating contract.
```

Do not duplicate the full contract in `CLAUDE.md`.

#### Convergence artifact contract

| Artifact | Must contain | Must not become |
|---|---|---|
| `delivery-plan.md` | phase, blockers, next output, next change | roadmap copy or changelog dump |
| OpenSpec proposals | fine-grained changes with one verifiable result each | one giant phase-level proposal |
| `AGENTS.md` | shared operating rules any agent can follow | a personal note file |
| `CLAUDE.md` | pointer to `AGENTS.md` | a second full operating manual |

#### Re-sync cadence

Re-run this step (or update the artifacts manually) after:
- phase changes
- milestone status changes
- blocker appears or clears
- handoff to another agent

Read [references/handoff-and-feedback-loop.md](./references/handoff-and-feedback-loop.md) for the expected loop.

#### Handoff checklist

Before handing off to another agent:
- [ ] State current phase
- [ ] State blocker or explicitly say none
- [ ] State next verifiable output
- [ ] State next OpenSpec change
- [ ] State decision delta since previous handoff
- [ ] Include source links for critical context
- [ ] Confirm `delivery-plan.md` was updated
- [ ] Confirm `AGENTS.md` is current
- [ ] Confirm `CLAUDE.md` points to `AGENTS.md`

Tell the user: "Convergence artifacts ready. Run `/stacksmith-review code` when you have a diff, or `/stacksmith-qa` after deploying to staging."

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-plan\",\"mode\":\"plan-eng\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```

---

## Mode: `design`

### Preamble (run first)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
echo "BRANCH: $_BRANCH"
[ -f PLAN.md ] && echo "PLAN_FILE: PLAN.md" || echo "PLAN_FILE: none"
find . -name "*.fig" -o -name "*.sketch" -o -name "DESIGN.md" 2>/dev/null | grep -v node_modules | head -5
```

Read `PLAN.md` if it exists. Ask for screenshots or mockups if not provided.

### Philosophy

You are a senior product designer who has strong taste and is willing to call out AI-generated slop.

What AI design slop looks like:
- generic hero sections with gradient backgrounds and floating 3D icons
- every section a full-width card with shadow on shadow on shadow
- labels like "Submit" instead of the specific action
- empty states that say "No data found" instead of guiding the user forward
- everything the same visual weight
- inconsistent spacing
- modals for things that should be inline
- tables with 8 or more equally wide columns

What great design looks like:
- one clear thing to look at first on every screen
- labels that say exactly what happens when clicked
- empty states designed as onboarding
- errors that tell you what to do next
- motion that explains state changes instead of decorating

### Step 1 - Rate each dimension

For each of the 10 dimensions, give a score from 0 to 10 and describe what a 10 would look like for this product:

| Dimension | Score | Current state | What 10 looks like here |
|-----------|-------|---------------|-------------------------|
| Hierarchy | ? | [describe] | One unmistakable primary action per screen |
| Whitespace | ? | | Elements breathe; nothing fights for space |
| Typography | ? | | Clear weights; size conveys importance only |
| Color | ? | | Semantic colors; each has a job; AA contrast |
| Consistency | ? | | Same component = same interaction everywhere |
| Copy | ? | | Every label names the action, not the widget |
| Empty states | ? | | Designed as onboarding, not error fallback |
| Error states | ? | | Human language; tells you what to do next |
| Motion | ? | | Purposeful only; explains state change |
| Mobile | ? | | One-thumb usable; touch targets >=44px |

### Step 2 - AI slop scan

Flag any present:
- labels: "Submit", "OK", "Cancel"
- empty states with no CTA or guidance
- errors like "An error occurred" or "Something went wrong"
- spacing off the 4px grid
- cards nested inside cards inside cards
- gradient on gradient color schemes
- no hierarchy
- inline-able flows forced into modals
- tables with more than 6 columns shown by default
- loading states that are only a spinner
- success states that only say "Success!" with no next step

### Step 3 - Interactive fixes (one question per decision)

For any dimension scoring poorly, or any slop flag raised, ask one AskUserQuestion before proposing a fix:

```text
[Re-ground: what screen/component we're discussing]

[Explain the problem plainly]

RECOMMENDATION: [Option X] because [one-line reason]

A) [Option]
B) [Option]
C) Show me both and I'll decide
```

Wait for each answer before moving on. Never batch multiple design decisions in one question.

### Step 4 - Write DESIGN.md (or update PLAN.md)

Write the design spec:

```markdown
# Design: [feature]
_[date] - /stacksmith-plan design - [branch]_

## Dimension scores
| Dimension | Score | Notes |
|-----------|-------|-------|
[table]

## Slop flags resolved
[list]

## Component spec

### [Component name]
- **Copy:** [exact labels, error messages, empty states, tooltips]
- **States:** default | hover | active | disabled | loading | error | empty
- **Mobile:** [specific behavior]
- **Touch target:** [size in px]

## Color tokens
| Token | Hex | Usage |
|-------|-----|-------|
| --color-primary | #... | Primary actions only |
| --color-danger | #... | Destructive actions, error states |
| --color-surface | #... | Card backgrounds |
| --color-border | #... | Dividers, input borders |

## Spacing scale
4px base grid: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64

## Typography scale
| Role | Size | Weight | Usage |
|------|------|--------|-------|
| Heading | 24px | 600 | Page titles |
| Body | 16px | 400 | Content |
| Label | 14px | 500 | Form labels, nav |
| Caption | 12px | 400 | Timestamps, metadata |

## Motion
| Trigger | Animation | Duration | Purpose |
|---------|-----------|----------|---------|
```

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-plan\",\"mode\":\"plan-design\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```

---

## Mode: `auto`

### Preamble (run first)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")
_SLUG=$(git remote get-url origin 2>/dev/null | sed 's|.*[:/]\([^/]*/[^/]*\)\.git$|\1|;s|.*[:/]\([^/]*/[^/]*\)$|\1|' | tr '/' '-' | tr -cd 'a-zA-Z0-9._-' 2>/dev/null || basename "$PWD")
echo "BRANCH: $_BRANCH"
echo "REPO: $_REPO"
_DESIGN=$(ls -t ~/.mystack/projects/$_SLUG/*-$_BRANCH-design-*.md 2>/dev/null | head -1)
[ -z "$_DESIGN" ] && _DESIGN=$(ls -t ~/.mystack/projects/$_SLUG/*-design-*.md 2>/dev/null | head -1)
[ -n "$_DESIGN" ] && echo "DESIGN_DOC: $_DESIGN" || echo "DESIGN_DOC: none"
[ -f PLAN.md ] && echo "PLAN_FILE: PLAN.md" || echo "PLAN_FILE: none"
git diff HEAD --name-only 2>/dev/null | grep -qiE '\.(tsx?|jsx?|vue|svelte|css|scss|html)$' && echo "UI_SCOPE=true" || echo "UI_SCOPE=false"
git log --oneline -10 2>/dev/null
```

If no design doc and no `PLAN.md`: "No plan file found. Run `/stacksmith-plan ideate` first to create one, then come back to `/stacksmith-plan auto`."

### The 6 decision principles

1. Choose completeness. Pick the approach that covers more edge cases and failure modes.
2. Boil lakes. Fix everything in the blast radius that is less than a day of work.
3. Pragmatic. If two options fix the same thing, pick the cleaner one.
4. DRY. If it duplicates existing functionality, reject it.
5. Explicit over clever. A 10-line obvious fix beats a 200-line abstraction.
6. Bias toward action. Flag concerns but do not block.

Conflict resolution by phase:
- CEO: completeness + boil lakes dominate
- Design: explicit + completeness dominate
- Eng: explicit + pragmatic dominate

### Decision classification

Every question you auto-answer is one of:
- Mechanical: one clearly right answer, auto-decide silently
- Taste: reasonable people could disagree, auto-decide but surface at the final gate
- User Challenge: both the primary analysis and an adversarial subagent agree the user's direction should change; never auto-decide

### Phase 0 - Intake

Capture restore point:

```bash
mkdir -p ~/.mystack/projects/$_SLUG
cp "$_DESIGN" ~/.mystack/projects/$_SLUG/stacksmith-plan-auto-restore-$(date +%Y%m%d-%H%M%S).md 2>/dev/null || true
```

Read context:

```bash
git log --oneline -15 2>/dev/null
cat TODOS.md 2>/dev/null | head -30
cat ARCHITECTURE.md 2>/dev/null | head -30
```

Read the design doc or `PLAN.md` in full.

Detect phases to run:
- CEO phase: always
- Design phase: only if `UI_SCOPE=true` or the plan mentions UI/frontend/components
- Eng phase: always

Tell the user: "Running `/stacksmith-plan auto`: CEO review -> [Design review ->] Eng review. Auto-deciding everything except premises and user challenges. Final gate at the end."

### Phase 1 - CEO review

Execute the full `ceo` mode in this skill and follow every section.

Override rule: Every AskUserQuestion in CEO mode is auto-decided using the 6 principles.

Two exceptions are not auto-decided:
1. Premise confirmation if the problem being solved is unclear or wrong
2. User Challenges when both primary review and adversarial analysis agree the direction should change

Auto-decide mode selection:
- clear, well-scoped features -> HOLD SCOPE
- too narrow -> SELECTIVE EXPANSION
- too broad -> REDUCTION
- new products or first versions -> EXPANSION

Log every decision in an audit trail, for example:

```text
[CEO] Auto-decided: Mode = SELECTIVE EXPANSION (principle 2: borderline blast radius)
[CEO] Auto-decided: Keep auth scope, defer password reset to TODOS (principle 3: pragmatic)
[CEO] Taste decision #1: API design - REST vs GraphQL (principles 3+5 suggest REST, but GraphQL is viable)
```

### Phase 2 - Design review (conditional)

Skip if there is no UI scope. Log: `[Design] Skipped - no UI scope detected.`

If running: execute the full `design` mode in this skill and follow every section.

Override rule: every AskUserQuestion auto-decided using explicit + completeness.

Auto-decide defaults:
- ambiguous labels -> more specific/action-oriented option
- layout questions -> clearer hierarchy
- both viable -> the one that requires fewer future decisions

### Phase 3 - Eng review

Execute the full `eng` mode in this skill and follow every section.

Override rule: every AskUserQuestion auto-decided using explicit + pragmatic.

Auto-decide defaults:
- test coverage questions -> always add tests
- architecture options -> most explicit, least abstraction
- edge case handling -> yes
- migration approach -> reversible preferred

Adversarial subagent (always run):

```text
Read the engineering plan being reviewed. Act as an adversarial engineer.
Find the top 3 issues the review might have missed: failure modes, hidden
assumptions, deployment risks, or scope that looks simple but isn't.
Output each as one sentence: "RISK: [description]"
```

If the adversarial subagent identifies risks not caught in the main review, add them as findings, auto-decide with the 6 principles, or escalate as a user challenge.

### Phase 4 - Final approval gate

Stop here and present all collected items to the user:

```text
## /stacksmith-plan auto Review Complete [date]

### Plan: [title]
[1-3 sentence summary]

### Phases run
- CEO Review: [N issues found, N auto-decided]
- Design Review: [N issues / skipped]
- Eng Review: [N issues found, N auto-decided]

### Decisions made: N total (M auto-decided, K taste, J user challenges)
```

User Challenges section when needed:

```text
### User Challenges - both analyses disagree with your stated direction

Challenge 1: [title] (from [CEO/Design/Eng])
You said: [original direction]
Both analyses recommend: [the change]
Why: [reasoning]
What we might be missing: [blind spots]
If we're wrong, the cost is: [downside of changing]

Your original direction stands unless you explicitly change it.
```

Taste Decisions section when needed:

```text
### Your Choices - taste decisions where you might disagree

Choice 1: [title] (from [CEO/Design/Eng])
Auto-decided: [what was chosen] - [which principle]
Alternative: [what was not chosen and why it is also viable]
Override with: "override choice 1: [your preference]"
```

Auto-decided summary (always show):

```text
### Auto-decided (N decisions - see plan file for full audit trail)
[3-5 most impactful, one line each]
```

AskUserQuestion options:
- A) Approve - accept all recommendations, write review logs, proceed to `/stacksmith-release prepare`
- B) Approve with overrides - specify which taste decisions to change
- C) Challenge one decision - ask about a specific auto-decision
- D) Revise plan - changes needed, re-run affected phases (max 3 cycles)
- E) Reject - start over

### On approval - write review logs

```bash
_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
mkdir -p ~/.mystack
echo "{\"ts\":\"$_TS\",\"skill\":\"stacksmith-plan\",\"mode\":\"plan-ceo\",\"branch\":\"$_BRANCH\",\"outcome\":\"success\",\"via\":\"autoplan\",\"commit\":\"$_COMMIT\",\"repo\":\"$_REPO\"}" >> ~/.mystack/timeline.jsonl
echo "{\"ts\":\"$_TS\",\"skill\":\"stacksmith-plan\",\"mode\":\"plan-eng\",\"branch\":\"$_BRANCH\",\"outcome\":\"success\",\"via\":\"autoplan\",\"commit\":\"$_COMMIT\",\"repo\":\"$_REPO\"}" >> ~/.mystack/timeline.jsonl
```

If design ran:

```bash
echo "{\"ts\":\"$_TS\",\"skill\":\"stacksmith-plan\",\"mode\":\"plan-design\",\"branch\":\"$_BRANCH\",\"outcome\":\"success\",\"via\":\"autoplan\",\"commit\":\"$_COMMIT\",\"repo\":\"$_REPO\"}" >> ~/.mystack/timeline.jsonl
```

Tell the user: "All reviews complete and logged. Run `/stacksmith-release prepare` when ready to create the PR."

### Important rules

- Never abort. The user chose auto mode.
- Full depth. "No issues found" is valid only after actually doing the analysis.
- Sequential. CEO -> Design -> Eng.
- Log every decision. No silent auto-decisions.

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-plan\",\"mode\":\"autoplan\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```
