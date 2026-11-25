---
name: claude-code-team-builder
description: "Builds a complete AI development environment for a software project — agents, custom skills, CLAUDE.md project context, orchestration layer, and routing rules. Triggers when someone says 'set up a new project', 'build a team for [project]', 'create project setup', 'scaffold my AI team', or describes a client project and wants Claude Code configured for it. Produces a full .claude/ configuration with project context, agent routing, autonomous execution support, and slash commands tailored to the project's domain and workflow."
---

# Claude Code Team Builder

## What This Skill Produces

For any software project, this skill generates a complete `.claude/` directory:

```
.claude/
├── CLAUDE.md                              ← project context Claude reads every session
├── team.json                              ← orchestration + autonomy configuration
├── agents/
│   ├── orchestrator/AGENT.md              ← mandatory: plans, assigns, validates
│   ├── problem-solver/AGENT.md            ← mandatory: self-healing, task repair
│   ├── test-engineer/AGENT.md             ← mandatory: validates every feature
│   ├── documentation-writer/AGENT.md      ← mandatory: PRDs before development
│   └── [project-specific]/AGENT.md
├── skills/
│   ├── run/SKILL.md                       ← autonomous execution loop
│   ├── status/SKILL.md                    ← project state reporting
│   ├── dashboard/SKILL.md                 ← visual progress tracker
│   ├── dashboard/dashboard.html           ← the project's copy of the dashboard template
│   ├── deploy/SKILL.md                    ← workflow skill
│   ├── test/SKILL.md                      ← workflow skill
│   ├── review/SKILL.md                    ← workflow skill
│   └── [domain skills]/SKILL.md           ← project-specific
└── workspace/                             ← result files, progress.log, orchestrator_state.json
```

**CLAUDE.md** is the most important output — project context read at every session start: tech stack, domain concepts, agent routing, project completion criteria, available commands, and conventions.

**Agents** use the subfolder structure (`agents/[name]/AGENT.md`). Each agent carries its own handoff protocol. Four agents are mandatory on every project: orchestrator, problem-solver, test-engineer, documentation-writer.

**Skills** are three kinds:
- *Execution skills* — `/run`, `/status`, `/dashboard` — orchestration and monitoring
- *Workflow skills* — `/deploy`, `/test`, `/review`, `/migrate` — developer workflows
- *Domain skills* — tailored to what this project does (e.g., `/process-refund`, `/onboard-vendor`)

**team.json** controls orchestration behavior: autonomy mode, retry policy, and the self-healing pipeline.

**This skill does NOT create:**
- PRDs, architecture documents, or specs (the documentation-writer agent does that)
- Source code or project scaffolding (the dev agents do that)
- Any artifact outside `.claude/`

---

## Phase 1: Discovery

### Choose a mode — ALWAYS ask the user before doing anything else:

This is mandatory. Regardless of how the user triggers the skill — whether they say "set up a new project" or "build a team for my SaaS app" or paste a full project description unprompted — **always present the mode choice first.** Do not skip this step. Do not infer the mode from how the user started the conversation.

> "To set up your project, I can work in two ways:
> - **Paste mode**: Share everything you know — description, tech stack, requirements, constraints — and I'll infer the rest.
> - **Q&A mode**: I'll ask you questions one section at a time. More thorough, better output for complex projects.
>
> Which do you prefer?"

If the user already pasted a project description in their first message, still ask — they may want Q&A mode to fill in gaps they didn't think of. If they confirm paste mode, proceed with what they already shared.

### Paste mode
The user pastes a project description. Extract answers to the question bank from what they provide, then ask only for critical gaps — at most 3 follow-ups. If something is genuinely unclear, make a reasonable assumption and state it explicitly.

### Q&A mode
Ask questions from the question bank (`references/question-bank.md`) one section at a time. Present each section as a numbered list. Don't ask a question whose answer is already obvious from prior answers.

**Required to proceed (minimum viable discovery):**
1. What are you building? (type + purpose)
2. What's the tech stack? (frontend, backend, database)
3. What are the highest-risk or most complex technical areas?

Everything else can be inferred with reasonable defaults.

---

## Phase 2: Determine Agents

**Always include (mandatory):**
- `orchestrator` — plans, assigns tasks, validates results, drives the execution loop
- `problem-solver` — self-healing: rewrites failed tasks, splits complex tasks, fixes acceptance criteria
- `test-engineer` — validates every feature
- `documentation-writer` — PRDs before development, specs for client handoff

**Add based on tech stack and complexity:**

| Signal | Add |
|---|---|
| Web app with distinct UI and API | `frontend-developer` + `backend-developer` |
| Full-stack framework (Next.js, Nuxt, SvelteKit) | `fullstack-developer` (preferred for vertical slicing) |
| Data-heavy schema / complex queries | `database-architect` |
| Any deployment / CI/CD | `devops-engineer` |
| Client deliverable / payment code / sensitive logic | `code-reviewer` |
| Payments, billing, financial logic is central | `payments-engineer` (domain specialist) |
| Real-time / live streaming / WebSockets | `streaming-engineer` (domain specialist) |
| Existing client design system | `design-system-integrator` (domain specialist) |
| Auth, OAuth, compliance | `auth-security-engineer` (domain specialist) |
| ML, AI features, data science | `ml-engineer` (domain specialist) |
| iOS/Android/React Native | `mobile-developer` |

Team size: 5–6 agents for simple projects (4 mandatory + 1–2 dev), 6–8 for medium, 8–10 for complex multi-surface projects.

**Critical rule on agent descriptions:**
The `description` field is what Claude uses to route tasks. It must name the specific technologies and task types. A generic description like "backend API development" is useless. A good one says:

> "Next.js App Router API routes, Prisma ORM queries, and Stripe Connect webhook handling. Use for any server-side logic, database work, or payment processing on the TaskFlow project."

Every agent file must reference the project's name, stack, and domain.

**Model assignment by cognitive demand:**
Not every agent needs the same model. Assign based on the reasoning complexity of the work:

| Tier | Model | Agents | Why |
|---|---|---|---|
| Planning | sonnet (opus or fable for higher quality) | `orchestrator`, `problem-solver` | Task decomposition, failure diagnosis, and dependency reasoning require the strongest planning ability. Use fable for maximum quality, or opus as the middle ground, if the user's model balance allows it; otherwise sonnet. |
| Execution | sonnet | All developer agents, `devops-engineer` | Focused code generation within a well-defined scope. Sonnet handles this well. |
| Validation | sonnet (or haiku) | `test-engineer`, `code-reviewer`, `documentation-writer` | Checking criteria against output, reviewing code patterns, writing structured docs. Haiku is sufficient for simple validation tasks if the user wants to optimize cost. |

Ask the user during discovery (question 11) which profile they want:
- **Default**: sonnet for all agents
- **Cost-optimized**: validation agents drop to haiku
- **Balanced**: planning agents move up to opus
- **Quality-maximized**: planning agents move up to fable

Write each agent's model into the `model:` line of its frontmatter. That line is the only thing Claude Code reads to choose a subagent's model, so it's where the tier lives; there is no separate tier setting. To change a tier later, edit `model:` in every agent in that tier.

Write the alias (`fable`, `opus`, `sonnet`, `haiku`), not a full model ID. Each alias resolves to the latest model in its family, so generated agents don't go stale. Use a full ID such as `claude-opus-5-5` only if the user wants to pin a version.

`/run` runs the execution loop in the main session, so the loop itself uses the session's model. The planning tier covers the problem-solver, and the orchestrator whenever it runs as a subagent.

---

## Phase 3: Determine Skills

### Execution skills — always included:

| Skill | Purpose |
|---|---|
| `/run` | Autonomous execution loop with state reconciliation |
| `/status` | Project state reporting |
| `/dashboard` | Visual progress tracker (HTML) |

### Workflow skills — include when the condition is met:

| Skill | Include when |
|---|---|
| `/deploy` | Project has a deployment pipeline or hosting target |
| `/test` | Project has (or will have) automated tests |
| `/review` | Client project or code quality is a priority |
| `/migrate` | Project has a relational database |
| `/pr` | Project uses GitHub/GitLab and PRs |
| `/seed` | Project has database seed data for development |
| `/changelog` | Client expects release notes or versioned deliverables |

### Domain skills — derive from the project's key workflows:

Think: *"What multi-step task will this developer repeat many times?"*

Examples by domain:
- **E-commerce**: `/process-refund`, `/add-product`, `/sync-inventory`
- **SaaS / multi-tenant**: `/onboard-tenant`, `/audit-usage`, `/manage-subscription`
- **Marketplace**: `/approve-vendor`, `/process-payout`, `/handle-dispute`
- **Streaming/media**: `/check-stream-health`, `/rotate-cdn-keys`
- **Data/analytics**: `/generate-report`, `/run-pipeline`, `/validate-schema`
- **Auth-heavy**: `/audit-permissions`, `/rotate-keys`

Create 1–3 domain skills based on what the project actually does.

---

## Phase 4: Generate Files

### Generation rule: copy structural sections verbatim

Templates contain two kinds of content:
- **Placeholders** — text in `[brackets]` like `[Project Name]`, `[tech stack]`, `[test framework]`. Replace these with project-specific values.
- **Structural sections** — named blocks that define how agents and skills behave. These must be **copied verbatim** into the generated files. Do not paraphrase, shorten, summarize, or rewrite them in your own words.

Structural sections that must be copied verbatim from the templates:

| Template | Sections to copy verbatim |
|---|---|
| orchestrator | Task Sizing Rules, State Management, State Summarization, Execution Loop, Self-Healing Pipeline, Handoff Protocol |
| problem-solver | Self-Healing Workflow, Handoff Protocol |
| All other agents | Handoff Protocol |
| /run skill | Execution Loop (it points at the orchestrator's loop rather than repeating it) |
| /dashboard skill | How the dashboard works, Important |
| CLAUDE.md | Task Sizing (copy general rules, then add project-specific lines below them) |

**Why this matters:** These sections contain reasoning rules, not just descriptions. If the orchestrator gets a paraphrased summary instead of the full Task Sizing Rules, it can't reason about edge cases during replanning. If an agent gets a shortened Handoff Protocol, it may skip writing result files. The templates are precise because the rules need to be precise.

After replacing placeholders and copying structural sections, verify each generated file by checking that every structural section listed above is present and complete — not shortened, not reworded.

### 4A: Agent files (subfolder structure)

Create `.claude/agents/[name]/AGENT.md` for each agent. Use the templates in `references/templates/agents.md`. Replace all placeholders with project-specific content. Copy all structural sections verbatim per the rule above.

### 4B: Skill files

Create `.claude/skills/[skill-name]/SKILL.md` for each skill. Use the templates in `references/templates/skills.md`. Each skill should:
- Have a clear trigger description (the `description` frontmatter field)
- Walk through its workflow step by step
- Reference the project's actual commands, paths, and conventions
- Be short — workflow skills are usually 30–60 lines

### 4C: CLAUDE.md — the project brain

Use `references/templates/claude-md.md` as the structure. It must include:

1. **Project summary** — 2–3 sentences. What it is, who it's for, current status.
2. **Tech stack** — complete list
3. **Key domain concepts** — entities and business rules (3–8 concepts)
4. **Agent routing** — explicit rules with orchestrator as highest priority
5. **Available skills** — list of `/commands` with one-line descriptions
6. **Project conventions** — file structure, naming, what NOT to do
7. **Project completion criteria** — deterministic stopping point for the orchestrator
8. **Task sizing** — copy general rules from template verbatim, then add project-specific lines below them (per the generation rule above)
9. **Current focus** — placeholder the user updates as the project evolves

Keep CLAUDE.md under 130 lines. Dense but scannable.

### 4D: team.json

Write the orchestration settings to `.claude/team.json`:

```json
{
  "autonomy": {
    "mode": "supervised"
  },
  "retry_policy": {
    "max_retries": 4,
    "strategy": "classify-then-act",
    "simple_failure_retry": 1
  },
  "self_healing": {
    "enabled": true,
    "pipeline": ["simple-retry", "refine-instructions", "split-task", "reassign-agent", "escalate"],
    "invoke_problem_solver": "structural-failures-only"
  }
}
```

Do not create or edit `.claude/settings.json`. That file is Claude Code's own project settings (permissions, hooks, plugins, environment variables), an existing project may already have one, and Claude Code doesn't use the team builder's keys.

The `mode` field is the only switch for milestone pauses and escalation. It accepts three values:
- `"supervised"` — pauses for human review at every milestone boundary, and stops to ask when a task still fails after self-healing (default)
- `"autonomous"` — advances milestones on its own when acceptance criteria pass, and stops to ask only when a task still fails after self-healing
- `"strict-autonomous"` — never stops to ask; a task that still fails after self-healing is marked `skipped`

Models are not set here. Each agent's tier goes in its own `model:` frontmatter (see Phase 2).

### 4E: workspace directory and dashboard

Create `.claude/workspace/`. Copy `references/templates/dashboard.html` to two places in the project:
- `.claude/skills/dashboard/dashboard.html` — the project's own copy of the template. `/run` and `/dashboard` copy from here, because `references/templates/` exists only where the team builder is installed.
- `.claude/workspace/dashboard.html` — the page the user opens.

Do NOT generate dashboard HTML from scratch — always use the fixed template.

The orchestrator will populate the workspace with:
- `orchestrator_state.json` — persistent state across sessions
- `progress.log` — task transition log
- `dashboard.html` — fixed template, reads tasks.json and progress.log dynamically
- `[task-id].result.md` — individual agent result files

---

## Phase 5: Validate and Summarize

Before finishing, verify:
- ✅ All structural sections from templates are present and complete in generated files (see Phase 4 generation rule)
- ✅ `orchestrator` agent has: State Management, State Summarization, Task Sizing Rules, Execution Loop, Self-Healing Pipeline, Handoff Protocol — all verbatim
- ✅ `problem-solver` agent has: Self-Healing Workflow, Handoff Protocol — verbatim
- ✅ All other agents have: Handoff Protocol — verbatim
- ✅ Every agent uses subfolder structure (`agents/[name]/AGENT.md`)
- ✅ The orchestrator's `tools` include `Agent`, so it can hand tasks to other agents when it runs as a subagent
- ✅ Every agent description references this project's actual tech stack and domain
- ✅ CLAUDE.md Task Sizing has general rules plus project-specific lines
- ✅ CLAUDE.md includes agent routing, skill list, domain concepts, completion criteria, and conventions
- ✅ team.json includes autonomy, retry, and self-healing configuration, and `.claude/settings.json` was not created or changed
- ✅ Every agent's `model:` frontmatter matches its tier (planning, execution, validation) for the chosen model balance
- ✅ `.claude/skills/dashboard/dashboard.html` and `.claude/workspace/dashboard.html` are both exact copies of `references/templates/dashboard.html`
- ✅ Execution skills (`/run`, `/status`, `/dashboard`) included
- ✅ At least 2 workflow/domain skills created
- ✅ No PRDs, specs, architecture docs, or source code created
- ✅ Total files ≤ 25

Then summarize:
- What agents were created and why
- What skills were created and what they do
- What's in CLAUDE.md
- What autonomy mode is set and how to change it
- Suggested first action: run `/run --plan` to generate the task decomposition, review it, then `/run` to start execution

---

## Reference Files

- `references/question-bank.md` — full discovery question bank, organized by category
- `references/templates/agents.md` — agent file templates for each role (including orchestrator + problem-solver)
- `references/templates/skills.md` — skill file templates for execution, workflow, and domain skills
- `references/templates/claude-md.md` — CLAUDE.md structure template
- `references/templates/dashboard.html` — fixed dashboard template (copy into the project's dashboard skill and workspace, do not regenerate)
