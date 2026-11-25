---
name: using-mighty-powers
description: Use when starting any conversation — establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill.
</SUBAGENT-STOP>

<IMPORTANT>
**Memory-first rule:** At the START of every session, read MEMORY.md and relevant memory files BEFORE performing any task. Never claim something is missing or not done without first checking memory. Memory records can become stale — verify against current state before acting on them.
</IMPORTANT>

<IMPORTANT>
**Currency-first rule:** Do not answer version-sensitive questions from training data — library/SDK APIs, package versions, model IDs, pricing, CLI flags, "latest" anything. Verify against current sources first: context7 MCP for library docs, WebSearch/WebFetch for everything else, the project lockfile for installed versions. The `mp:staying-current` skill is the full policy. The Currency Guard hook will remind you when a prompt looks version-sensitive. If you can't verify, say so rather than guessing.
</IMPORTANT>

<IMPORTANT>
**Skill-first rule:** Invoke relevant skills BEFORE any response or action — including clarifying questions. Even a 1% chance a skill might apply means invoke it first. If an invoked skill turns out not to fit, you don't need to follow it. Skipping a skill and being wrong costs more than invoking one unnecessarily.
</IMPORTANT>

## Instruction Priority

Mighty Powers skills override default system prompt behavior, but **user instructions always take precedence**:

1. **User's explicit instructions** (CLAUDE.md, direct requests) — highest priority
2. **Mighty Powers skills** — override default system behavior where they conflict
3. **Default system prompt** — lowest priority

## How to Access Skills

**In Claude Code:** Use the `Skill` tool. When you invoke a skill, its content is loaded and presented to you—follow it directly. Never use the Read tool on skill files.

---

# ROUTING: The Most Important Section

<EXTREMELY-IMPORTANT>
Mighty Powers has 3 tracks. You MUST pick the right track based on the task. Getting this wrong means either wasting the user's time with overkill process OR shipping sloppy work without enough discipline.

**Default to the Quick Track.** Only escalate to Lifecycle Track when the user explicitly asks for it or the task genuinely requires multi-epic planning.
</EXTREMELY-IMPORTANT>

## Track 1: Quick Track (use 80% of the time)

**For:** Bug fixes, single features, refactors, small-to-medium changes, anything with clear scope.

**How to recognize:** The user says "add X", "fix Y", "change Z", "implement this feature", or describes a single clear task.

Quick Track has 4 size tiers. **Pick the smallest tier that fits the task.**

### Tier 1: Trivial (fix a typo, change a config value, rename something)

**Ask the user before skipping planning:**

> "This looks like a quick change. Want me to jump straight to implementation, or would you prefer an implementation plan first?"

If user says jump in:
1. Use `mp:test-driven-development` — write a test if applicable, make the change
2. Use `mp:verification` — run tests, confirm everything passes

If user wants a plan → treat as Tier 2.

### Tier 2: Small (clear scope, < 100 lines, one file or a few files)

Planning required. Plan is organized in waves with checkpoints.

```
writing-plans → executing-plans (wave by wave) → verification
```

1. Use `mp:writing-plans` — create plan organized into **waves** (parallel where tasks are independent, sequential where they're not)
2. Use `mp:executing-plans` or `mp:subagent-driven-development` — execute wave by wave, parallelize independent tasks within each wave
3. Use `mp:verification` — run tests, confirm complete

### Tier 3: Medium (single feature, clear scope, multiple files)

Full Quick Track with optional design exploration. Plan organized in waves.

```
brainstorming → writing-plans (waves) → executing-plans (wave by wave) → code-review → verification
     ↑
  (skip if
  scope is
  obvious)
```

1. `mp:brainstorming` — only if the approach isn't obvious. **Skip if you know what to build.** (Quick Track design-with-approval; for Lifecycle ideation use `mp:brainstorm-session` instead.)
2. `mp:writing-plans` — detailed plan structured in **waves** with checkpoints (parallel where tasks are independent)
3. `mp:executing-plans` or `mp:subagent-driven-development` — execute wave by wave, parallelize independent tasks
4. `mp:code-review` — two-stage review before merge
5. `mp:verification` — final check

### Tier 4: Structured Small (needs spec tracking across sessions)

For when the change is small but you need a formal spec document — e.g., the work will span multiple sessions, or you want adversarial review of the approach before coding.

```
quick-dev (5-step workflow with spec file, wave-based plan)
```

1. Use `mp:quick-dev` — clarify intent → plan (in waves) → implement (parallel per wave) → adversarial review → present
2. This creates a spec file in `docs/implementation/` that tracks progress

**Use Tier 4 only when Tier 2-3 isn't enough** — when you need the spec as a persistent artifact.

### Wave-Based Execution (applies to all tiers with plans)

All implementation plans are organized into **waves**. Each wave groups tasks at the same dependency level. Tasks within a wave that are independent (different files, no shared state) run in parallel via subagents. Tasks that share files or have ordering requirements run sequentially within the wave. Between waves, there is a checkpoint.

```
Wave 1: [Task A] [Task B] [Task C]  ← independent → run in parallel
            ↓ checkpoint
Wave 2: [Task D] → [Task E]         ← D and E share a file → run sequentially
            ↓ checkpoint
Wave 3: [Task F]                    ← single task
```

Not every wave has parallelism. A plan that is entirely sequential (one task per wave) is fine — waves still provide checkpoints and clear dependency ordering. See `mp:writing-plans` for how plans are structured.

### Bug fixes at any size

Always start with `mp:systematic-debugging` — 4-phase root cause process. Then apply the appropriate tier above for the fix.

### Supporting skills (available in all tiers)

| Phase | Skill | When |
|-------|-------|------|
| **BUILD** | `mp:test-driven-development` | During ANY code writing — write test first, then code |
| **BUILD** | `mp:systematic-debugging` | ANY bug or unexpected behavior — root cause first |
| **BUILD** | `mp:git-worktrees` | When you need an isolated workspace |
| **VERIFY** | `mp:finishing-branch` | When branch is ready to merge/PR |
| **BUILD** | `mp:dispatching-parallel-agents` | When a user request OR plan has 2+ independent tasks — dispatch in parallel, not sequentially |

## Track 2: Lifecycle Track (use only when needed)

**For:** New projects from scratch, multi-epic features, unclear/complex scope, team handoff artifacts.

**How to recognize:** The user says "build a new app", "design the architecture for X", "create a PRD", "plan out this large initiative", or explicitly asks for structured planning artifacts. The work will span multiple sessions or involve multiple developers.

<HARD-GATE>
DO NOT use Lifecycle Track skills unless:
- The user explicitly requests them (e.g., "create a PRD", "design the architecture")
- OR the task genuinely requires multi-epic planning (3+ distinct features that must be coordinated)
- OR the user asks to "start from scratch" on a new project

"Add a login page" is Quick Track, not Lifecycle. "Build a complete authentication system with OAuth, MFA, session management, and admin panel" MIGHT be Lifecycle if the user wants formal planning.

When in doubt, start with Quick Track. You can always escalate later.
</HARD-GATE>

**Flow:**
```
Analysis → Planning → Solutioning → Implementation
   ↓           ↓           ↓              ↓
research    prd          architecture   dev-story
product-    create-ux    create-epics   sprint-planning
brief       design       check-ready    sprint-status
prfaq                    gen-context    checkpoint-preview
brainstorm-session
```

**Skills in this track:**

| Phase | Skill | When |
|-------|-------|------|
| Analysis | `mp:brainstorm-session` | Lifecycle ideation — creative techniques, memlog, resume |
| Analysis | `mp:research` | Validate assumptions with domain/market/technical research |
| Analysis | `mp:product-brief` | Capture strategic vision |
| Analysis | `mp:document-project` | Document an existing project |
| Analysis | `mp:prfaq` | Working Backwards PRFAQ — stress-test product concepts |
| Planning | `mp:prd` | Create, update, or validate a PRD (unified workflow) |
| Planning | `mp:create-ux-design` | UX design — DESIGN.md + EXPERIENCE.md spines |
| Solutioning | `mp:architecture` | Architecture spine — invariants that keep work consistent |
| Solutioning | `mp:create-epics` | Break requirements into epics and stories |
| Solutioning | `mp:generate-project-context` | Generate project "constitution" |
| Solutioning | `mp:check-readiness` | Gate check before implementation |
| Implementation | `mp:sprint-planning` | Generate `sprint-status.yaml` from epics |
| Implementation | `mp:sprint-status` | Summarize sprint status and recommend next action |
| Implementation | `mp:create-story` | Prepare next story |
| Implementation | `mp:dev-story` | Execute a story (uses TDD internally) |
| Implementation | `mp:checkpoint-preview` | Human-in-the-loop review of a change |
| Implementation | `mp:qa-generate-e2e-tests` | Generate API/E2E tests for implemented code |
| Management | `mp:sprint` | Quick Track pipeline: plan → build → test → review → ship |
| Management | `mp:retrospective` | Sprint retrospective |
| Management | `mp:correct-course` | Mid-sprint pivots |

**Deprecated shims** (redirect to skills above): `create-prd`, `validate-prd`, `create-architecture`.

**You don't need ALL phases.** If the user already has a PRD, skip to Solutioning. If they already have architecture + epics, skip to Implementation.

## Track 3: Audit Track (on-demand)

**For:** Quality gates, security checks, pre-deploy verification, incidents. These are invoked explicitly or at natural checkpoints, not as part of a development flow.

| Phase | Skill | When |
|-------|-------|------|
| **VERIFY** | `mp:guard` | Manage safety guardrails, freeze directories |
| **REVIEW** | `mp:security-audit` | User asks to audit security, or before shipping sensitive changes |
| **REVIEW** | `mp:pentest` | User asks for penetration testing |
| **SHIP** | `mp:ship` | Pre-deploy scorecard — user asks "are we ready to ship?" |
| **DEFINE** | `mp:architecture-map` | User asks for architecture diagrams |
| **SHIP** | `mp:rescue` | Production incident — diagnostics, rollback, post-mortem |

## Track 4: Knowledge & Advanced (on-demand)

| Skill | When |
|-------|------|
| `mp:staying-current` | Before answering anything version-sensitive — library APIs, versions, pricing, model IDs |
| `mp:learnings` | User wants to save/search/digest/recall project learnings |
| `mp:onboard` | User asks for an onboarding guide |
| `/codex` command | Generate compact codebase index at `.mighty-powers/codex.md` to save exploration tokens |
| `mp:revise-claude-md` | User asks to update CLAUDE.md |
| `mp:party-mode` | User asks for a multi-agent discussion |
| `mp:advanced-elicitation` | User wants to push output quality |
| `mp:adversarial-review` | User wants a cynical review of a plan/document |
| `mp:grilling` | User wants to stress-test a plan/decision — relentless one-at-a-time questioning |
| `mp:writing-skills` | User wants to create new skills |
| `mp:resume` | Resume an interrupted plan after session crash — auto-detects or point to plan folder |
| `mp:status` | Check plan progress without resuming — read-only view of where things stand |
| `mp:init` | First-time project setup — creates config, offers to generate CLAUDE.md |
| `mp:help` | User asks for help or "what should I do next?" |

---

# Routing Decision Tree

When a user gives you a task, follow this decision tree:

```
Session starts
    │
    ├─ Session-start hook detected an in-progress plan?
    │   └─ YES → Tell the user:
    │       "Found in-progress plan: <name> (wave N). Want to resume?"
    │       ├─ Yes → /resume
    │       └─ No → "Want me to mark this plan as abandoned so I don't ask again?"
    │           ├─ Yes → Update status.yaml: status → abandoned
    │           └─ No → Leave as-is (will ask again next session)
    │
```

```
User gives a task
    │
    ├─ Is it a bug fix or unexpected behavior?
    │   └─ YES → mp:systematic-debugging → then fix using appropriate tier
    │
    ├─ Is it a question, research, or exploration?
    │   └─ YES → Answer directly (no skill needed) unless user asks for formal research
    │
    ├─ Does the user explicitly ask for a PRD, architecture, epics, or lifecycle planning?
    │   └─ YES → Lifecycle Track (Track 2)
    │
    ├─ Is it a new project from scratch with unclear scope?
    │   └─ YES → Ask the user: "Do you want structured planning (PRD, architecture, epics)
    │   │         or jump straight to implementation?"
    │   │   ├─ Structured → Lifecycle Track
    │   │   └─ Jump in → Quick Track Tier 3 (brainstorming first)
    │
    ├─ Is it trivial? (typo, config change, rename, < 20 lines)
    │   └─ YES → Quick Track Tier 1: Ask user "jump in or plan first?"
    │
    ├─ Is it small? (clear scope, < 100 lines, few files)
    │   └─ YES → Quick Track Tier 2: writing-plans → executing-plans → verification
    │
    ├─ Is it a single feature? (clear scope, multiple files)
    │   └─ YES → Quick Track Tier 3: brainstorming? → writing-plans → executing-plans
    │             → code-review → verification
    │
    ├─ Does it need a persistent spec artifact? (multi-session, needs adversarial review)
    │   └─ YES → Quick Track Tier 4: mp:quick-dev
    │
    └─ Default → Quick Track Tier 2 or 3 based on scope
```

**Key principle: pick the smallest tier that fits.** You can always escalate mid-task if the work turns out to be bigger than expected.

---

# Using Skills

## The Rule

**Invoke the skill for the CORRECT TRACK before any response or action.** The routing decision tree above determines which skill to invoke. Do not invoke Lifecycle Track skills for Quick Track tasks.

## Red Flags

These thoughts mean STOP—you're making a routing error:

| Thought | Reality |
|---------|---------|
| "Let me create a PRD for this bug fix" | Bug fix = Quick Track. Use `systematic-debugging`. |
| "I should create architecture docs for this feature" | Single feature = Quick Track unless user asks for it. |
| "Let me break this into epics" | Epics are Lifecycle Track. Single feature just needs `writing-plans`. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "This is just a simple question" | Questions are tasks. Check for applicable skills. |
| "I remember this skill" | Skills evolve. Read current version. |
| "The skill is overkill" | Use the RIGHT track, not the BIGGEST track. Quick Track is not overkill. |
| "I'll just do this one thing first" | Check routing BEFORE doing anything. |

## Skill Types

**Rigid** (TDD, debugging, guard): Follow exactly. Don't adapt away discipline.

**Flexible** (brainstorming, patterns): Adapt principles to context.

## User Instructions

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows — but it also doesn't mean escalate to Lifecycle Track.

---

# Agent Orchestration

Many skills dispatch specialized subagents for review, audit, or parallel work. This is a core strength of the plugin — use it whenever possible to improve quality and speed.

## Standard Dispatch Pattern

Use Claude Code's built-in **Agent tool** to dispatch subagents:

```
Agent tool call:
  prompt: [Agent role instructions from agents/<name>.md] + [Task-specific context]
  description: Short label (e.g., "security audit", "code review")
  model: Choose based on task complexity (see below)
```

## Parallel Dispatch

When multiple agents are independent, **dispatch them all in a single response** so they run concurrently:

```
Single message with multiple Agent tool calls:
  Agent 1: security-auditor → scans for vulnerabilities
  Agent 2: code-reviewer → reviews code quality
  Agent 3: bundle audit → checks build size
All three run in parallel. Collect results when all complete.
```

## Model Selection

Use the least powerful model that can handle the role:

| Task Type | Model | Examples |
|-----------|-------|----------|
| Fast/mechanical | `haiku` | Bundle size check, secret scanning, pattern matching |
| Standard reasoning | `sonnet` | Code review, security audit, test generation |
| Deep judgment | `opus` | Architecture review, design decisions, complex debugging |

Pass the model via the Agent tool's `model` parameter.

## Shared Agent Definitions

Reusable agent prompts live in `agents/`:

| Agent | Use For |
|-------|---------|
| `agents/code-reviewer.md` | Two-stage code review (spec + quality) with confidence scoring |
| `agents/security-auditor.md` | 8-category security audit |
| `agents/architect.md` | Architecture review and ADR recommendations |
| `agents/product-manager.md` | PRD review and requirements validation |
| `agents/qa-engineer.md` | Test coverage review and test strategy |
| `agents/incident-responder.md` | Incident diagnosis, rollback planning, post-mortem |

When a skill dispatches a subagent, it reads the agent definition and includes it in the prompt along with task-specific context. The subagent never inherits the parent session's history.

## Skills That Orchestrate Agents

| Skill | Agents Dispatched | Pattern |
|-------|-------------------|---------|
| `code-review` | code-reviewer | Single agent dispatch after implementation |
| `ship` | security-auditor + code-reviewer + bundle auditor | 3 parallel agents for scorecard |
| `sprint` | code-reviewer, security-auditor at phase gates | Automatic at BUILD→REVIEW, REVIEW→SHIP |
| `security-audit` | security-auditor + secret-scanner tool | Agent reasoning + automated scanning |
| `rescue` | incident-responder | Single agent for diagnosis |
| `party-mode` | Any combination of agents | 2-4 agents per round, parallel spawn |
| `subagent-driven-development` | implementer + spec-reviewer + quality-reviewer | Per-task cycle with two-stage review |
| `writing-plans` | plan-document-reviewer | Single agent after plan written (skipped for Simple plans) |
