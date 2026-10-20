---
name: intent-engineering-spec-driven
description: Translate product goals and user problems into structured intent specifications that both humans and AI agents can execute against. Covers intent engineering discipline, Spec-Driven Development lifecycle, and the OpenSpec framework. Use when designing agent-executable specs, building agentic features, or replacing ad-hoc prompting with durable intent infrastructure.
---

# Intent Engineering & Spec-Driven Development

## Overview

AI agents can build anything you ask for. The bottleneck is no longer code — it's knowing what to ask for with enough precision that agents don't guess. Intent engineering is the practice of translating user problems and product goals into structured, testable specifications that both humans can review and agents can execute against.

This skill provides the framework for replacing ephemeral prompting with durable intent infrastructure, with direct application to A-Tech's agentic products and Builder's Club curriculum.

## When to Use

- Designing agent-executable specifications for AI features
- Replacing ad-hoc prompting with structured intent specs
- Building products where AI execution quality depends on input clarity
- Training teams to write specs instead of tickets
- Creating durable artifacts that persist across agent sessions

## Intent Engineering Defined

### What It Is
Intent engineering is the practice of specifying what to build and why in a structured, testable format that both humans can review and agents can execute against.

### What It Is Not
- **Not prompt engineering:** One-time, ephemeral chat messages that disappear after the session
- **Not a PRD:** Narrative documents that describe intent but aren't machine-readable
- **Not a ticket:** Tracks work status, not the thinking behind the work

### The Five Elements of an Intent Spec
1. **Objective:** What problem are we solving and why does it matter?
2. **Observable Outcomes:** How will we know it worked? Specific, measurable success criteria.
3. **Constraints:** What must not happen? Boundaries on dependencies, performance, design patterns.
4. **Edge Cases:** What messy reality does the simple version ignore?
5. **Verification Criteria:** How do we confirm the output matches the intent before shipping?

## The Delegation Gap

### The Core Problem
Developers use AI in ~60% of their work but can fully delegate only 0–20% of tasks. The gap exists because prompts rarely provide what delegation requires:
- **Persistent context:** Prompts disappear after the session. The next agent — or the next developer — starts from zero.
- **Testable outcomes:** "Build a checkout flow" is a request, not a specification. Without explicit success criteria, verification becomes guesswork.
- **Explicit constraints:** Every real feature has boundaries: don't break the API, don't introduce a new dependency, keep response time under 200ms. Prompts rarely capture these. Agents rarely infer them.

### Intent as Delegation Protocol
An intent spec turns a vague request into something an agent can execute reliably. It is not more documentation — it is a delegation protocol.

## Spec-Driven Development (SDD) Lifecycle

### The Five-Step Loop
Based on the OpenSpec framework and industry practice:

#### 1. Explore
The AI reads the codebase to identify bottlenecks and architectural options without committing code.
- **Human role:** Define the problem space and success criteria
- **Agent role:** Discover constraints, identify risks, surface options
- **Output:** Options analysis with tradeoffs

#### 2. Propose
The AI scaffolds a change proposal. Humans review the proposal to catch logic errors early.
- **Human role:** Review and challenge assumptions
- **Agent role:** Generate proposal document with tasks, design rationale, and risk assessment
- **Output:** Approved proposal with task breakdown

#### 3. Refine
Human and AI iterate on the design until the "what" and "how" are perfectly clear.
- **Human role:** Clarify edge cases, tighten constraints, verify outcomes
- **Agent role:** Revise proposal based on feedback, flag unresolved ambiguities
- **Output:** Locked intent spec with zero known ambiguities

#### 4. Apply
The AI executes the code changes, checking off tasks one by one, strictly constrained by the agreed-upon spec.
- **Human role:** Monitor progress, intervene on anomalies
- **Agent role:** Implement against the spec, report deviations immediately
- **Output:** Implemented feature matching the spec

#### 5. Archive
Completed specs are merged into permanent documentation, and change artifacts are archived.
- **Human role:** Verify final output against spec, approve merge
- **Agent role:** Update living documentation, summarize changes
- **Output:** Updated codebase + archived spec for future reference

## Technical Implementation

### OpenSpec Framework
An open-source, CLI-driven framework that makes specifications "first-class citizens" alongside source code.

**Directory Structure:**
```
openspec/
  specs/           # Source of Truth — current system logic and constraints
    auth/spec.md
    billing/spec.md
  changes/         # Active Workspace — one subfolder per feature/bug fix
    feature-123/
      proposal.md
      tasks.md
      design.md
      specs/
```

**Key Technical Benefits:**
- **Context Hygiene:** Delta Specs describe only changes, reducing token usage and preventing catastrophic forgetting in long AI sessions
- **Deterministic Outputs:** Locking requirements before coding makes AI output predictable and reviewable
- **Verifiability:** Tasks linked to specific requirements enable validation that the AI built what was requested
- **Brownfield Friendly:** Designed for evolving existing codebases, not just greenfield projects

### Multi-Agent Coordination
Intent specs become even more critical when multiple agents collaborate:
- **Orchestrator agent** decomposes the objective across specialized agents
- **Each agent** receives its own sub-spec: what it owns, what success looks like, what it shouldn't touch
- **Synthesis agent** integrates outputs against the master spec's verification criteria

### Prompt-Driven vs. Intent-Driven Orchestration

| Dimension | Prompt-Driven | Intent-Driven |
|-----------|--------------|---------------|
| Context | Lives in the conversation | Persists in the spec |
| Success | "It runs" | Outcomes verified |
| Edge cases | Discovered in production | Defined upfront |
| Coordination | By improvisation | By specification |
| Reviewability | Ephemeral | Versioned and auditable |

## Quality Patterns

### The Comprehension Contract
Before accepting any agent output, the orchestrator must explain:
- What the code does
- Why it does it this way
- What could go wrong
- How to verify it works

If they cannot explain it, they do not delegate it — they refine the spec.

### The Checkpoint Protocol
For long-running agents, define explicit checkpoints requiring human approval:
- Architecture decision points
- External API integrations
- Database schema changes
- Security boundary crossings
- User-facing behavior changes

## A-Tech Applications

### A-Coder (IDE)
- **Intent Spec Generator:** Convert natural language feature requests into structured specs
- **Spec Validation:** Verify that specs contain all five required elements before execution
- **Living Documentation:** Auto-update specs as code changes, maintaining the Source of Truth
- **Checkpoint Gates:** Force spec review at defined architecture and security boundaries
- **Delta Spec Mode:** Generate minimal change specs for token-efficient agent execution

### Be Practical (Playbooks)
- **"Intent Engineering Fundamentals"** chapter covering the five elements and SDD lifecycle
- **"From Ticket to Spec"** playbook for product managers and engineers
- **"Multi-Agent Spec Decomposition"** advanced chapter for complex features
- **Spec templates** for common feature types (API endpoints, UI components, database migrations)

### Builder's Club
- **Intent engineering workshops:** Hands-on training in writing agent-executable specs
- **OpenSpec adoption track:** Community contribution to the open-source framework
- **Spec review exchange:** Members review each other's specs before agent execution
- **Certification:** "A-Tech Intent Engineer" credential for spec-writing proficiency

## Measurement Framework

| Metric | Definition | Target |
|--------|-----------|--------|
| Spec completeness | % of specs containing all five required elements | ≥ 95% |
| Agent execution accuracy | % of tasks completed correctly without spec revision | ≥ 85% |
| Spec revision rate | Average number of refine iterations before apply | ≤ 2 |
| Comprehension pass rate | % of outputs where orchestrator passes comprehension contract | ≥ 90% |
| Documentation freshness | % of specs current with codebase within 48 hours of merge | ≥ 95% |

## Ethical Boundaries

- **Specs are human-reviewed:** No agent executes against a spec that hasn't been human-approved
- **Transparency:** Teams can inspect the spec that generated any piece of code
- **Version control:** All specs versioned alongside code; no hidden intent changes
- **Accountability:** The spec author owns outcomes, even when agents executed the implementation
- **No spec laundering:** Do not use specs to conceal unethical features behind "neutral" requirements

## Cross-References
- See `ai-agents-and-workflows/agentic-coding-trends-2026` for the 8 macro trends shaping agentic coding
- See `developer-experience-and-flow/orchestrator-engineer-mindset` for hiring and training orchestrators
- See `developer-experience-and-flow/agentic-coding-workflow` for collaboration models and delegation intuition
- See `developer-experience-and-flow/supervisory-engineering-work` for the new work category of AI direction and evaluation

## Sources
- Pathmode — "Intent Engineering: The Discipline That Replaced Prompt Engineering" (pathmode.io, 2026)
- Jonathan Soh / Fission AI — OpenSpec Framework (LinkedIn, 2026)
- Anthropic — "2026 Agentic Coding Trends Report" (resources.anthropic.com)
- Ivan Chuikov / Claude Code — /simplify multi-agent refactoring architecture (LinkedIn, 2026)
- Simon Schulte — AutoPR proposal-phase workflow design (blog.neokil.de, 2026)
