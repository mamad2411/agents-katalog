---
name: agent-experience-ax-devex-evolution
description: Framework for designing Agent Experience (AX) - the evolution of developer experience for AI coding agents. Use when [building AI coding environments, designing agent-friendly codebases, creating AI development workflows, implementing agent safety boundaries, onboarding AI agents to repositories].
---

# Agent Experience (AX): The Evolution of Developer Experience

## Core Concept

Agent Experience (AX) is the discipline of designing the layer between a model and a real codebase: the context, tools, permissions, tests, and review loops that tell the agent what matters, what it can touch, and how it knows it worked. As AI coding agents become regular contributors to repositories, we must stop optimizing only prompts and start engineering their environments.

The shift from DX to AX follows a simple first-principles question: How do we build a fast, secure, and deterministic feedback loop for agents?

## The Seven Core Tenets of AX

### 1. Context Is Onboarding
Developer onboarding was a seasonal event. With agents, onboarding happens at the start of every single task. Repository instructions, setup commands, component APIs, schemas, and known failure modes shape what the agent sees, tries, ignores, and verifies.

**Principle**: Agent context must be minimal, transparent, and tested.
- **Minimal**: Global context stays thin and points back to the code itself
- **Transparent**: A reviewer can easily audit which rule, skill, or setup note shaped the work
- **Tested**: Team skills are self-explanatory enough that the agent invokes them at the right time

**Anti-pattern**: Accumulating a graveyard of skills, `AGENTS.md` rules, stale definitions, and hidden tool instructions. When an agent makes a bad choice, the human reviewer must debug a massive, non-deterministic input history.

### 2. The Environment Is Part of the Prompt
LLMs are inherently non-deterministic. Because their cognitive engine is probabilistic, the rest of their execution environment must be aggressively deterministic.

The environment is literally part of the prompt. Dependency versions, local scripts, environment-variable shapes, seed data, auth setups, browser access, and local services determine what the agent can observe and correct.

**Critical insight**: "I couldn't run the tests locally, but this should work" is a massive DX red flag when a human says it. When an agent does it, we tend to just hope for the best. A human developer who hits a missing environment variable will stop and investigate. An agent will route around the failure, change the wrong file, and ship a guess with a polite commit message.

**Requirement**: Agents must have a reliable, consistent, observable workspace before their output can be trusted.

### 3. No Handoffs Without Verification
Agents shouldn't stop at generating code. They need to prove their work.

We're currently trading the friction of writing code for the exhausting cognitive load of reviewing it. If a developer has to spend thirty minutes manually QA-ing an agentic PR, the agent didn't save time. It just shifted the labor.

**Principle**: The agent should do more verification work before handoff. Its completed task should present evidence:
- Tests run
- Screenshots captured
- Browser flows checked
- Logs inspected
- Accessibility trees reviewed
- Edge cases explored

**Golden rule**: Spend tokens before spending reviewer attention. Tokens are cheap, pretty much unlimited, and run 24/7. Senior developer focus is precious, expensive, and burns out. If an agent can check its own work in a closed loop, it should.

### 4. Safety Needs to Be Deterministic
Good DX made dangerous actions hard. Good AX needs to make dangerous actions impossible.

Agents act quickly, literally, and at scale. A prompt like "Make sure not to mess with the database!" doesn't help. Prompts are easily bypassed. Safety must be structural:
- Sandboxing
- Scoped credentials
- File and network limits
- Separate development and production data
- Environment-variable approval gates
- Human-in-the-loop validation for high-risk actions

**Key insight**: Any time an agent drops a database, the question is "Why did your system allow for that? Why did the agent have that access?"

As agents move beyond developers, non-technical teammates will start using them. Safety can't depend on whether a PM or marketer understands what `rm -rf`, OAuth scopes, or production environment variables can do. The sandbox must be the absolute security boundary.

### 5. Model Routing as Boring Infrastructure
We spend too much time on the weekly frontier model horse race. The real questions for teams are:
- Who can access agents?
- Against what systems?
- With what context?
- Under what review process?
- Through which model route?
- And with what audit trail?

Model routing should be boring in the best possible way. Cheap, fast models handle low-risk summarization, triage, classification, scaffolding, or routine review support. Deterministic syntax validation belongs to linters, typecheckers, and test runners. Expensive reasoning models are reserved for harder multi-file judgment work.

Good governance belongs directly inside the agent path. Admins see usage and costs, reviewers see execution evidence, and teams have flexibility to switch providers without rewriting application logic.

### 6. Design Systems and Code Architecture Are the Agent's Best Source of Truth
Your codebase isn't just for human maintainability anymore. For an agent to execute tasks reliably, the codebase must be the most accurate record of how the product actually works.

If your codebase is messy—if the docs say one thing, the components do another, and Storybook is three versions behind—the agent will synthesize that confusion into elegant-looking garbage.

**Principle**: Design using classic software engineering principles:
- Deep modules with thin public interfaces
- Typed APIs
- Predictable routing
- Clean directory structures

This is progressive disclosure for machines. By keeping implementation details hidden behind clean interfaces, we lower the cognitive load on the agent, which translates directly to lower token usage and fewer logic errors.

The same applies to design systems. The more your codebase forces the agent to reuse human-made components, tokens, and accessibility patterns, the less likely the output is to become generic sludge. The agent shouldn't be inventing a custom button when your team's button is right there.

### 7. Agents Become Cross-Functional Glue
Agent experience starts with developers, but it's actually an organizational coordination engine.

When agents make Version 1 of a feature cheap to generate, they don't solve Version 2, 3, or 4. Without a shared workspace, the developer becomes a high-priced human router who copies visual feedback from Slack, translates it back to the agent's prompt interface, runs the workspace locally, and manually manages the branch.

**Better approach**: Move away from pre-code abstractions toward shared iteration around live product surfaces. With interactive preview deployments and role-aware controls, a designer, marketer, or PM can talk to the agent directly inside a safe, bounded preview. They can test responsive states, iterate on copy, or tweak layouts on a branch preview, while developers retain ownership over architecture, safety, and system integration.

The developer is no longer the copy-paste bottleneck; they are the platform engineer who owns the system design.

## The Golden Rule

**LLMs should do the glue work. People should do the interesting work.**

If humans are copying feedback between tools, re-explaining repo context, manually checking whether the agent broke the obvious thing, policing stale docs, and cleaning up generic output while the model makes the creative decisions, the system is upside down.

Good agent experience gives creative people more room to use judgment, taste, architecture, strategy, care, and craft.

## Implementation Checklist

- [ ] Audit agent context: Is it minimal, transparent, and tested?
- [ ] Verify environment determinism: Can the agent reliably run tests, compile, and seed data?
- [ ] Implement verification before handoff: What evidence does the agent present?
- [ ] Establish structural safety: Sandboxing, scoped credentials, approval gates
- [ ] Set up model routing governance: Usage tracking, cost visibility, provider flexibility
- [ ] Clean codebase for agent readability: Typed APIs, clean interfaces, current docs
- [ ] Create shared preview environments for cross-functional collaboration
- [ ] Define review workflows that respect the agent's evidence presentation

## Alignment with A-Tech Values

- **Open-source AI**: AX principles apply equally to open-weight models running locally
- **Data privacy**: Structural safety boundaries protect user data from agent overreach
- **Practical implementation**: Every tenet has concrete implementation steps
- **Developer sovereignty**: AX elevates developers to platform engineers, not replaces them