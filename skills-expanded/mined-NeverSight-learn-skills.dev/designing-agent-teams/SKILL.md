---
name: designing-agent-teams
description: Designs, generates, and refines multi-agent coding teams with optimal model-to-role assignments for OpenCode and Claude Code. Produces reasoning documents and ready-to-paste configuration files. Triggers when creating a multi-agent setup for a codebase, starting a new project with an agent team, reviewing or improving an existing agent team configuration, deciding which AI model to assign to which agent role, or optimising cost/speed/quality tradeoffs across agents. Also triggers for subagent design, model routing, agent orchestration, model selection for coding agents, or comparisons of Opus vs Sonnet vs Haiku for different task types.
compatibility: Requires file read/write access and bash. Designed for Claude Code and OpenCode but output formats are portable.
---

# Designing Agent Teams

Generate multi-agent coding teams with optimal model assignments. Outputs a reasoning document (`AGENTS.md`) plus ready-to-paste configs for OpenCode and Claude Code.

## Determine the mode

1. **create-existing** — Analyse an existing codebase, generate a tailored agent team
2. **create-new** — From a project brief or tech stack, generate a starter agent team
3. **add** — Add one or more agents to an existing team (e.g., a new dependency or cross-cutting concern)
4. **review** — Evaluate an existing agent team config, suggest refinements

**Creating for an existing codebase?** → Follow "Gather inputs: existing codebase" below
**Starting a new project?** → Follow "Gather inputs: new project" below
**Adding agents to an existing team?** → Follow "Gather inputs: add" below
**Reviewing an existing team?** → Follow "Gather inputs: review" below

## Gather inputs

Gather what is available from the codebase and the user's request. If the user has not specified priorities, infer them from context (a solo side project likely values speed and cost; a team production app likely values quality). Do not block on missing information — use sensible defaults and note assumptions in AGENTS.md.

### Existing codebase

- Read the project's directory structure, package.json / config files, and README
- Identify languages, frameworks, key dependencies, monorepo structure, test setup
- Estimate complexity: file count, language diversity, architectural layers
- **Default priority if not stated:** balance cost and quality (the most common case)

### New project

- Extract tech stack, project type, and scope from the user's request
- If team size is not stated, assume solo developer
- **Default priority if not stated:** prototyping speed for new projects
- Note framework-specific tooling needs (e.g., CMS schemas, deployment pipelines)

### Add to existing team

- Read the existing agent configuration files (`.opencode/agents/`, `.agents/`, `CLAUDE.md`) to understand the current team: roles, models, tools, escalation paths
- Identify what the new agent needs to cover — this may come from the user's request (e.g., "I just added Supabase and need an agent for edge functions") or from detecting a new dependency/tool in the codebase
- Determine where the new agent fits in the existing orchestration: who delegates to it, who it escalates to, and what scope boundaries it needs to respect relative to existing agents
- Check for overlap — if an existing agent already covers the concern partially, consider expanding that agent's prompt instead of adding a new one

### Review

- Read the existing agent configuration files (check `.opencode/agents/`, `.agents/`, and `CLAUDE.md`)
- Identify which models are assigned where, what tools each agent has, scope definitions
- Apply the review checklist (below) to identify issues
- If the user has described specific pain points, prioritise those

## Design the agent team

Read `references/model-guide.md` for current model characteristics, pricing, and assignment heuristics.

Read the relevant config reference:

- `references/opencode-config.md` for OpenCode agent definitions
- `references/claude-code-config.md` for Claude Code subagent patterns

Apply these principles in order:

**1. Start from roles, not models.** Identify what agent roles the project needs before choosing models.

**2. Consider whether a team is needed at all.** A well-prompted single agent with a good spec handles many projects effectively. Multi-agent coordination adds the most value when a single agent's accuracy is below ~45% on the task, or when the project has clearly parallelisable work streams with independent file boundaries. For simple projects, a single Sonnet agent with a clear AGENTS.md spec may outperform a poorly-coordinated team.

**3. Assemble the core team, then bring in specialists.**

Think of the agent team like a human dev team: a small core that's always present, plus specialist consultants brought in based on the project's requirements.

**Core team (always present):**

- **Orchestrator** — the tech lead. Decomposes tasks, delegates, tracks dependencies, reviews results. Every team has one.
- **Coder** — the developer. Implements features and fixes within scoped boundaries.
- **Tester** — the QA engineer. Writes tests _independently from the coder_ to avoid confirmation bias. Separating test authorship from code authorship is the single highest-impact structural decision in a multi-agent team.

These three are present in every team this skill generates. They form the plan-implement-verify loop that the research consistently identifies as the minimum effective team.

**Specialist consultants (added per project):**

Bring in specialists based on what the project needs. Each should cover a cross-cutting concern that the core team would otherwise miss or handle inconsistently:

- **Accessibility reviewer** — for web projects; checks changes against WCAG, flags inaccessible patterns
- **Security auditor** — for auth-heavy, payment, or user-data projects; audits auth flows, input validation, dependencies
- **Performance reviewer** — for latency-sensitive or resource-constrained projects
- **Documentation writer** — for libraries, APIs, and long-lived projects; keeps docs in sync with changes
- **Platform specialist** — for projects using 3+ external platforms (e.g., Supabase, Stripe, Sanity) where a single agent's context window can't hold all the platform tools simultaneously

Prefer cross-cutting concern specialists (security, accessibility, performance) over tool-specific ones. Tool-specific agents are justified primarily by context window constraints, not domain expertise — if the project only uses one or two platforms, the coder can handle them with MCP access.

**4. Match cognitive demand to model tier.** See `references/model-guide.md` for the full heuristics. Summary:

- **Opus** — orchestration, architectural planning, complex debugging, pre-merge review
- **Sonnet** — code generation, independent test writing, feature implementation, standard refactoring
- **Haiku** — file exploration, boilerplate, docstrings, grep-style searches, simple edits

**5. Prevent write conflicts.** How strictly to scope write access depends on whether agents run in parallel or sequentially:

- **Parallel agents** (e.g., Claude Code Agent Teams, tmux worktrees): assign each agent to distinct directories or modules. Two agents writing to the same file simultaneously will overwrite each other's work. Use git worktree isolation where the platform supports it.
- **Sequential agents** (e.g., orchestrator delegates one task at a time): file conflicts are less likely since agents take turns, but still scope write access to what each agent actually needs. A tester should write to test directories, not source code. A docs agent should write to documentation files, not application logic.

In both cases, when a task genuinely crosses boundaries, the orchestrator should coordinate the handoff rather than giving multiple agents overlapping write access.

**6. Scope tools tightly.** Each agent gets only the tools it needs. A documentation agent does not need shell access. A file explorer does not need write permissions.

**7. Ground specialists in official sources.** Specialist agents for specific tools or platforms (e.g., Supabase, Vercel, Sanity, Netlify) should defer to authoritative sources rather than relying on the model's training knowledge, which may be outdated or incomplete. When designing a specialist agent:

- If the tool has an MCP server, include it in the agent's tool configuration and instruct the agent to use it for API lookups, schema queries, and platform operations.
- If the tool has official documentation, instruct the agent to consult it (via web fetch or a bundled reference) before generating platform-specific code.
- The agent's system prompt should explicitly state: use the official docs/MCP as the source of truth; do not guess at API signatures, configuration options, or platform behaviour.
- Check for available MCP servers at the tool's documentation site or the MCP registry. Common examples: Supabase, Stripe, Netlify, Sentry, Linear, GitHub, Notion.

**8. Design for escalation.** Build concrete escalation paths: test failures, error counts, or complexity markers trigger handoff from cheaper to more capable agents.

**9. Use deterministic quality gates.** Do not rely on an LLM to judge whether its own work is good enough. Quality gates should be automated and deterministic: linting, type-checking, test pass rates, build success. An LLM reviewer in a fresh context adds value for nuanced issues (security patterns, architectural fit), but the primary gate must be tooling, not judgment.

**10. Target the 70/20/10 split.** Roughly 70% Haiku, 20% Sonnet, 10% Opus by call volume. If more than 30% of calls go to Opus, re-examine whether those tasks genuinely need frontier reasoning.

## Generate outputs

All outputs go into the current working directory (the project repo root). The output structure is:

```
.agents/
├── AGENTS.md              # Team overview, orchestration, escalation map
├── orchestrator.md        # Core: always present
├── coder.md               # Core: always present
├── tester.md              # Core: always present
└── [specialist].md        # Specialists: added per project (e.g., accessibility.md, security.md)
.opencode/
└── agents/
    ├── orchestrator.md    # OpenCode agent config referencing .agents/orchestrator.md
    ├── coder.md           # OpenCode agent config referencing .agents/coder.md
    ├── tester.md          # OpenCode agent config referencing .agents/tester.md
    └── [specialist].md    # One per specialist
CLAUDE.md                  # Agent team section referencing .agents/*.md
```

The three core agent files (`orchestrator.md`, `coder.md`, `tester.md`) are always generated in both `.agents/` (full instructions) and `.opencode/agents/` (OpenCode config with frontmatter). Specialist files are added based on the project's requirements.

### .agents/ directory

Create `.agents/` in the project root if it does not exist.

**AGENTS.md** — the team-level document. Contains:

1. **Team overview** — purpose and project context
2. **Agent roster** — for each agent: role name, model, one-sentence rationale, link to its instruction file
3. **Orchestration pattern** — who calls whom, what triggers handoffs
4. **Cost projection** — estimated call distribution and relative cost
5. **Escalation map** — which agents escalate to which

If `.agents/AGENTS.md` already exists, read it first and update in place. In **add** mode, append the new agent(s) to the roster and update the orchestration, cost, and escalation sections. Do not rewrite descriptions of unchanged agents.

**Individual agent files** (e.g., `orchestrator.md`, `coder.md`, `tester.md`) — one file per agent. Each contains:

1. **Role** — what this agent does, in one paragraph
2. **Model** — which model tier and why
3. **Tools and scope** — what tools the agent has access to, what directories/files it can write to
4. **Escalation** — when to escalate, and to whom
5. **Instructions** — the agent's full operational instructions, including domain-specific guidance, conventions to follow, and any MCP servers or documentation URLs to consult

Keep each agent file under 500 words. The agent's capabilities come from the model and its tools, not from lengthy instructions.

### OpenCode configuration

Generate one markdown file per agent in `.opencode/agents/` per `references/opencode-config.md`. Each file has YAML frontmatter (description, mode, model, permissions) and a body that references the agent's `.agents/*.md` instruction file:

```markdown
---
description: Implements features and fixes within scoped boundaries
mode: subagent
model: anthropic/claude-sonnet-4-20250514
permission:
  edit: allow
  bash:
    "*": ask
---

You are the Coder. Read .agents/coder.md for your full instructions.
```

The orchestrator should be `mode: primary`. All other agents should be `mode: subagent`.

If `.opencode/agents/` already exists, read its contents first and merge new agent files. Preserve existing agents not being replaced. If `.opencode/agents/` does not exist, create it.

### Claude Code configuration

Write the agent team section into `CLAUDE.md` per `references/claude-code-config.md`. Each subagent definition should reference its `.agents/*.md` file:

```markdown
### @coder

Model: claude-sonnet-4-6
Instructions: See .agents/coder.md
```

If `CLAUDE.md` already exists, read it first. Append the agent team section under `## Agent Team` rather than overwriting. If `## Agent Team` already exists, replace that section only.

### What not to do

- Do not write outputs to `/mnt/user-data/outputs/` or any path outside the repo
- Do not overwrite existing config files without reading them first
- Do not remove existing agents or agent files unless explicitly asked
- Do not inline long instructions into `.opencode/agents/*.md` frontmatter or `CLAUDE.md` — use the `.agents/*.md` files

## Best practices

These patterns emerged from real-world use and significantly improved team effectiveness. They are recommendations, not requirements — adapt them to your project's needs. See `examples/taskflow/` for a worked example demonstrating all of these.

### Narrate delegations

The orchestrator should explain each handoff to the user: which agent is being called, why, and what it returned. Without narration, multi-agent workflows are a black box — the user sees a final result but has no idea what happened in between, making it hard to debug, trust, or improve the team.

Add this to the orchestrator's instructions:

> Before each delegation, explain which agent you are calling and why. After each agent returns, summarise what it found or did.

And reinforce it in the OpenCode config preamble:

> IMPORTANT: Before each delegation, explain to the user which agent you are calling and why. After each agent returns, summarise what it found or did.

### Dual-touchpoint specialists

Domain-critical specialists (accessibility, security, performance) are most effective when called at two points in the workflow:

1. **Early (planning)** — after context gathering but before implementation. The specialist assesses the proposed approach for risks and recommends mitigations. These recommendations are passed to the Coder as implementation guidance.
2. **Late (review)** — after implementation. The specialist reviews the actual code against domain criteria.

This is more effective than a single review gate at the end, because:

- Catching issues at planning time is cheaper than reworking implemented code
- The Coder gets actionable guidance upfront instead of discovering constraints through failed reviews
- The specialist's early assessment shapes the implementation rather than just judging it

Not every specialist needs two touchpoints. Use dual-touchpoint for concerns that are expensive to retrofit (accessibility, security). A documentation writer, for instance, only needs a late pass.

When using dual-touchpoint specialists, name them "Specialist" rather than "Reviewer" — "Reviewer" implies they only look at finished work and doesn't reflect the advisory role.

### Ordering quality gates

When multiple quality-gate agents run after implementation, order them by dependency:

1. **Tester** first — verifies functional correctness. If tests fail, the code will change, so there's no point reviewing it yet.
2. **Domain specialists** second — review working, tested code against domain criteria (accessibility, security, etc.).

This avoids wasted specialist reviews on code that's about to change due to test failures.

## Gotchas

- A coder agent that writes its own tests has confirmation bias — it tests what it thinks it implemented, not what it should have. An independent tester agent that generates tests from the spec, not from the code, catches significantly more edge cases.
- Multiple agents writing to the same files is the most common source of broken builds in parallel agent teams. For parallel setups, scope each writing agent to distinct directories. For sequential setups, the risk is lower but still scope write access to what each agent needs — a tester writing to source code is a sign of misconfigured scope.
- At 85% accuracy per step, a 10-step workflow succeeds only 20% of the time. Keep agent chains short and gate each step with deterministic checks (tests, linting, type-checking), not LLM self-evaluation.
- Specialist agents without access to official docs will confidently generate outdated or wrong API calls. A Supabase agent relying on training data might use deprecated RLS syntax or old client methods. Always wire in the MCP server or documentation URL and tell the agent to check before generating.
- Haiku has a smaller context window than Opus and Sonnet. An agent assigned to explore a large monorepo on Haiku may silently lose context. For large codebases, use Sonnet for exploration or split the search into smaller scoped calls.
- Opus tends to refactor code beyond the requested scope. System prompts for Opus-powered agents should explicitly constrain scope ("make only the changes described in the plan, do not refactor adjacent code").
- Agent system prompts that are too long waste context on every call. Keep them under 500 words — the agent's capabilities come from the model, not from lengthy persona descriptions.
- When merging into an existing `CLAUDE.md`, the file may contain project-specific instructions unrelated to agents. Only touch the `## Agent Team` section. Rewriting the whole file will destroy existing project configuration.
- When adding an agent in **add** mode, create a new `.agents/[name].md` file and a corresponding `.opencode/agents/[name].md` file, and add a reference in `CLAUDE.md`. Do not rewrite existing agent files.
- OpenCode and Claude Code handle subagent invocation differently. Do not assume one platform's patterns work on the other — always read the relevant config reference before generating.

## Review checklist

When reviewing a team (any mode), check for:

- **Missing core team member** — every team should have an orchestrator, coder, and independent tester; if any is missing, that's the first thing to fix
- **Missing independent tester** — if the coder writes its own tests, the team is missing the highest-impact structural decision
- **Overlapping write access** — in parallel setups, multiple agents with write access to the same directories will cause conflicts; in sequential setups, check that each agent's write scope matches its actual role
- **LLM-only quality gates** — if the only check before merge is another LLM reviewing, add deterministic gates (tests, linting, type-checks)
- **Unjustified agents** — every agent should cover a concern that would otherwise be missed; remove any that duplicate another agent's scope
- **Missing specialists** — if the project has accessibility, security, or compliance requirements, check whether dedicated reviewer agents are needed
- **Over-assignment to Opus** — tasks Sonnet handles equally well
- **Missing escalation paths** — Haiku agent stuck with no handoff route
- **Scope creep** — agent with tools or filesystem access it does not need
- **Redundant agents** — overlapping work that could consolidate
- **Context window pressure** — Haiku has a smaller context window than Opus/Sonnet
- **Would a single agent suffice?** — if the project is simple enough that one well-prompted agent handles it, a team adds overhead without value
