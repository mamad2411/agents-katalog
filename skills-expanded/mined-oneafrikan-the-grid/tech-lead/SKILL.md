<!--
  SKILL.md — Tech Lead operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about Claude Code-only features unless explicitly noted.
  Stack-specific commands are NOT here — they live in stacks/<stack>/ overlays.
  Injection points are marked: `STACK: ...`
-->

# Skill: Tech Lead

## Invocation

```
/tech_lead <feature description>
```

Or invoked by another orchestrator passing a feature request directly.

---

## Step 1 — Understand the request

Before writing any PRD or spawning any specialist, confirm:

| Question | Why it matters |
|---|---|
| What is the user-facing goal? What problem does this solve? | Grounds the PRD in outcomes, not features |
| Who is the target user? | Shapes acceptance criteria |
| Are there existing patterns to follow in the codebase? | Prevents reinventing conventions |
| What are the constraints? (timeline, tech stack, dependencies) | Scopes the PRD |
| What does success look like? How will we measure it? | Defines acceptance criteria |
| Who else needs to be informed or involved? | Surfaces cross-team dependencies |

**Rule:** If requirements are unclear after ONE round of clarifying questions, escalate to the human. Do not proceed with major assumptions.

**Rule:** If the feature takes less than ~4 hours total, skip multi-agent coordination and use a single agent. Multi-agent overhead is not worth it for small tasks.

---

## Step 2 — Architecture analysis

Think through the system before writing the PRD.

**Data flow**
- Where does data originate?
- How does it move through the system?
- What transformations happen along the way?
- Where does it land?

**Components / modules**
- What new modules/pages/services are needed?
- What existing components can be reused?
- What new endpoints or jobs are required?
- Any new data model changes?

**Dependencies**
- What existing code is affected?
- External services to integrate?
- New packages or infra needed?

**Security**
- What auth/permissions are required?
- Is sensitive data involved?
- What is the blast radius if this is exploited?

**Performance**
- Scaling considerations?
- Large datasets?
- Real-time requirements?

For decisions with long-term implications, write an ADR (see ADR template below) before proceeding.

<!-- STACK: stack-specific architecture patterns injected here (e.g. file conventions, ORM choices, framework patterns) -->

---

## Step 3 — Write the PRD

Save to: `output/<project>/PRD.md`

### PRD template

```markdown
# PRD: <Feature Name>

## Overview
<!-- One paragraph: what this feature does and why it matters. -->

## Problem statement
<!-- What can users not do today? What breaks without this? -->

## User stories
<!-- Format: "As a <user>, I want to <action> so that <outcome>." -->

## Scope

### In scope
<!-- Explicit list of what is included. -->

### Out of scope (future)
<!-- Explicit list of what is NOT included this iteration. -->

## Technical approach

### Architecture
<!-- Diagram or description of data flow, components, services. -->

### Data model changes
<!-- New tables, fields, schema migrations required. -->
<!-- STACK: stack-specific ORM / migration syntax injected here -->

### External dependencies
<!-- New services, credentials, env vars required. -->

## Tasks

### <!-- SPECIALIST_ROLE_1 --> tasks (~N hours estimated)
<!-- List tasks. Each task = 2-8 hours, independently testable, clear deliverable. -->
- [ ] Task description → deliverable: <file or PR or test>

### <!-- SPECIALIST_ROLE_2 --> tasks (~N hours estimated)
- [ ] Task description → deliverable: <file or PR or test>

### Testing tasks (~N hours estimated)
- [ ] Task description → deliverable: <test file or coverage report>

## Acceptance criteria

### Functional
- [ ] <Observable user-facing behaviour>

### Non-functional
- [ ] <Performance, accessibility, mobile, etc.>

### Security
- [ ] <Auth, data protection, input validation checks>

## Dependencies

### External
<!-- Third-party services, credentials, configs needed before work starts. -->

### Internal
<!-- Existing code, components, or PRDs that must exist first. -->

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| <risk> | Low/Med/High | Low/Med/High | <how to handle it> |

## Success metrics
<!-- How will we know this shipped successfully? Measurable where possible. -->

## Verification command
<!-- The single command (or short sequence) that proves the feature works. -->
<!-- STACK: stack-specific test/run command injected here -->
```

---

## Step 4 — Hand off to specialists

Handoff is **asynchronous and file-based** — never a live spawn. Per the Signal
Protocol (see AGENTS.md): append the task to `signals/→<agent>.md`, or open a PR
and notify via webhook. The specialist picks it up on its own next run.

Create a GitHub PR (or equivalent), or write the signal file, with the following body:

```markdown
## Task: <Role> — <Feature Name>

### Agent
<!-- [FILL] Which agent picks this up -->
Assigned to: <specialist-agent-id>

### PRD
<!-- [FILL] Link or path to PRD -->
PRD: output/<project>/PRD.md (Section: <section name>)

### Tasks
<!-- [FILL] Numbered list of tasks for this agent -->
1. Task one
2. Task two

### Relevant file paths
<!-- [FILL] Files the specialist must read before starting -->
- `<path/to/file>` — <why it matters>

### Constraints
<!-- [FILL] Hard rules the specialist must follow -->
- <constraint>

<!-- STACK: stack-specific constraints injected here -->

### Definition of done
<!-- [FILL] Specific, verifiable completion criteria -->
- [ ] All PRD acceptance criteria met (Section: "Acceptance criteria")
- [ ] Tests written and passing
- [ ] Verification command passes: `<command>`
- [ ] PR description updated with what changed and why

### Webhook trigger
<!-- [FILL] URL or mechanism to notify Tech Lead on completion -->
Notify: <webhook-url or mention @tech-lead>
```

---

## Step 5 — Monitor and review

While specialists work:
- Track progress via agent status or PR list.
- Review PRs when marked ready: read the diff, check for pattern adherence, security, edge cases.
- Coordinate if specialist roles need to sync (e.g. frontend needs an API contract before it can proceed).
- If a specialist is blocked, unblock or escalate to human (don't let blockers sit).

**Code review focus (Tech Lead pass):**
- [ ] Patterns consistent with established conventions?
- [ ] Security: auth/authz checks present? Input validated?
- [ ] Edge cases handled (empty state, error state, missing data)?
- [ ] Tests cover the acceptance criteria?
- [ ] No dead code or orphaned imports from this change?
- [ ] PR is small and focused, or is it a sprawling change that should be split?

---

## Step 6 — Release gate: two independent reviewers

Docs-only means only `*.md` files under `docs/`. Docs-only and draft work is exempt from this gate.

Once implementation is complete, run the gate. A QA pass alone is not a release pass.

1. **Build one packet.** PRD path, PR or diff range, verification command, acceptance criteria. Both reviewers get the same packet. Spawn the `qa-engineer` role with this packet:

```
Review <feature> feature.
PRD: output/<project>/PRD.md
PRs: #<frontend-pr> (<role>), #<backend-pr> (<role>)
Key test scenarios: [copy from PRD acceptance criteria]
Verification command: <command>
```

2. **Spawn both reviewers in one message.** Spawn the `qa-engineer` and `security-reviewer` roles (the roles, never the same-named wired skill), each in a fresh context, with the same packet. Each reviewer does not see the other reviewer's verdict: neither brief mentions the other reviewer's output.
3. **Read both verdicts verbatim.** qa-engineer returns PASS or BLOCK. security-reviewer returns a severity table: no open Critical or High finding in it is PASS, anything else is BLOCK. Medium and Low findings are reported but do not block. Do not re-rate findings.
4. **Both must pass.** If both PASS, report "gate passed" with both evidence blocks (command and output). The human still approves production.
5. **Any BLOCK: fix and re-run.** Forward the findings verbatim to the owning specialist for one fix batch, then re-run both reviewers with fresh agents. Maximum 3 rounds; a third BLOCK stops and escalates to the human with all rounds.
6. **Missing reviewer.** If either role is unavailable, or has not run, say so; the gate is not passed.

---

## Step 7 — Post-ship documentation

After successful deploy:
- Update `MEMORY.md → Active work` to mark feature complete.
- Log key decisions in `MEMORY.md → Recent decisions`.
- File any new ADRs that emerged during implementation.
- For incidents: write incident report to `output/<project>/incidents/<date>-<slug>.md`.

---

## ADR template

Save to: `output/<project>/architecture/ADR-<NNN>.md`

```markdown
# ADR-<NNN>: <Decision title>

## Status
<!-- Proposed | Accepted | Deprecated | Superseded by ADR-XXX -->

## Context
<!-- What is the situation that forced this decision? What options were considered? -->

## Decision
<!-- What was decided and why. Be specific. -->

## Consequences

### Positive
<!-- Benefits of this choice. -->

### Negative
<!-- Costs, risks, or constraints introduced. -->

## Date
<!-- YYYY-MM-DD -->
```

---

## Output file layout

```
output/<project>/
├── PRD.md                        # Product requirements (primary source of truth)
├── architecture/
│   ├── DECISIONS.md              # Running summary of all architecture decisions
│   ├── ADR-001.md                # Individual ADRs
│   └── system-design.md          # Architecture overview / diagrams
├── tasks/
│   ├── <role-1>/                 # Detailed specs per specialist role
│   └── <role-2>/
└── incidents/
    └── <date>-<slug>.md          # Post-mortems
```

---

## Parallelisation guidance

| Condition | Action |
|---|---|
| Frontend and backend tasks are independent | Spawn both simultaneously |
| Backend API contract is unknown | Unblock frontend by agreeing on contract first, then spawn |
| Task < 4 hours total | Use a single agent — skip multi-agent overhead |
| Task > 4 hours AND parallelisable | Multi-agent wins; coordinate via PRD |

---

## Task sizing rules

Good tasks:
- **2–8 hours** of specialist work
- **Independently testable** (can verify without other tasks being complete)
- **Clear deliverable** (you know exactly when it is done)
- **Parallelisable** where possible (frontend/backend can proceed simultaneously)

Bad tasks:
- "Build the auth system" — too big, not independently testable
- "Fix stuff" — no clear deliverable or acceptance criterion
