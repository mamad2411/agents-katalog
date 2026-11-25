---
name: architecture
version: 1.0.0
description: Evaluate and design system architecture and API design
uses:
  - analysis/deep-analysis
  - planning/strategic-planning
requires:
  tools: []
  env: []
security:
  risk_level: read
  capabilities:
    - file:read
  requires_approval: false
---

# Architecture

Evaluate and design system architecture and API design. This skill covers both assessing existing architecture and designing new systems — structure, patterns, trade-offs, and decisions.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `architect` is invoked, you (the agent) apply the methodology below using your reasoning capabilities. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it.

## When to Use

- Designing a new system, module, or feature from scratch
- Evaluating existing architecture for issues or improvement opportunities
- Making technology or pattern choices (database, queue, API style, etc.)
- Designing APIs (REST, GraphQL, internal interfaces)
- Assessing scalability, reliability, or maintainability
- Recording architectural decisions (ADRs)

## Methodology

### 1. Clarify Requirements

Before designing, understand:
- **Functional**: What must the system do?
- **Non-functional**: Performance targets, availability, scalability, security
- **Constraints**: Technology, budget, timeline, team size, legacy systems
- **Stakeholders**: Who uses this? Who maintains it? Who pays for it?

### 2. Analyze the Current State (If Existing System)

Map what exists:
- **Components**: What are the main pieces? How do they interact?
- **Data flow**: How does data move through the system?
- **Dependencies**: What depends on what? (internal and external)
- **Pain points**: Where are the bottlenecks, failures, or maintenance burdens?
- **Strengths**: What works well? (don't break what isn't broken)

### 3. Identify Architectural Patterns

Select patterns appropriate to the problem:

| Pattern | Good For | Trade-off |
|---------|----------|-----------|
| **Layered** | Clear separation of concerns | Can lead to unnecessary indirection |
| **Event-driven** | Loose coupling, async processing | Harder to debug and trace |
| **Microservices** | Independent deployment, scaling | Operational complexity |
| **Monolith** | Simple deployment, easy debugging | Scaling entire unit |
| **Plugin/Extension** | Extensibility without core changes | Plugin API maintenance burden |
| **Pipeline** | Data transformation chains | Each stage must handle errors |
| **Repository** | Central data access | Can become a bottleneck |

### 4. Design the Architecture

For each component:
- **Responsibility**: What does it do? (single responsibility)
- **Interface**: How do others interact with it? (API contract)
- **Data**: What data does it own? What does it share?
- **Dependencies**: What does it depend on? (minimize)
- **Failure mode**: What happens when it fails? (graceful degradation)

### 5. Design APIs

For each interface:
- **Contract**: Input types, output types, error types
- **Versioning**: How will the API evolve?
- **Consistency**: Naming conventions, response format, error format
- **Idempotency**: Can operations be safely retried?
- **Documentation**: Is the API self-describing?

### 6. Evaluate Trade-offs

Every architectural decision has trade-offs. Document them:

```
Decision: [what was decided]
Context: [why this decision was needed]
Options considered:
  - Option A: [pros] / [cons]
  - Option B: [pros] / [cons]
Chosen: [which option and why]
Consequences: [what follows from this decision]
```

### 7. Record as ADR

Architectural Decision Records persist the reasoning:
- **Title**: Short descriptive name
- **Status**: Proposed, Accepted, Deprecated, Superseded
- **Context**: What's the situation and constraints?
- **Decision**: What was decided?
- **Consequences**: What follows? (both positive and negative)

## Output Format

```
## Architecture: [System/Feature]

### Requirements
- Functional: [key requirements]
- Non-functional: [performance, availability, scalability]
- Constraints: [technology, budget, timeline]

### Current State (if applicable)
- Components: [list]
- Pain points: [list]
- Strengths: [list]

### Proposed Architecture
- Pattern: [selected pattern and why]
- Components:
  | Component | Responsibility | Interface | Dependencies |
  |-----------|---------------|-----------|-------------|
  | [name] | [what it does] | [API] | [what it needs] |

### API Design
- Style: [REST/GraphQL/RPC/internal]
- Key endpoints/methods: [list]
- Error handling: [approach]

### Trade-offs
| Decision | Chosen | Alternative | Why |
|----------|--------|-------------|-----|
| [decision] | [option] | [other options] | [reasoning] |

### ADR
- Title: [decision title]
- Status: [proposed/accepted]
- Decision: [what was decided]
- Consequences: [positive and negative]
```

## Quality Criteria

- Requirements are clarified before design begins
- Current state is understood before proposing changes
- Pattern selection is justified (not just "it's modern")
- Trade-offs are explicitly documented
- APIs are consistent, versioned, and documented
- Failure modes are considered for each component
- ADRs capture the reasoning (not just the decision)
- Design is as simple as possible (but no simpler)

## Common Mistakes

- **Over-engineering**: Building for scale you don't have. Start simple, evolve when needed. A monolith is fine until it isn't.
- **Resume-driven architecture**: Choosing technologies because they're trendy, not because they solve the problem. Boring technology is often the right choice.
- **Ignoring non-functional requirements**: Designing only for features while ignoring performance, security, and reliability. These are harder to add later.
- **No trade-off documentation**: Making decisions without recording why. When the next person asks "why did we use X?", there should be an answer.
- **Designing APIs without consumers in mind**: APIs should be designed for the caller's convenience, not the implementer's. Think from the outside in.
- **Tight coupling disguised as microservices**: If services can't be deployed independently or share a database, they're a distributed monolith — the worst of both worlds.
- **Not considering failure modes**: Every dependency can fail. If the design doesn't handle failures gracefully, it will handle them ungracefully in production.

## Completion

Architecture work is complete when:
- Requirements are understood and documented
- Current state is assessed (if applicable)
- Architecture is designed with justified pattern choices
- APIs are designed consistently
- Trade-offs are documented
- Failure modes are addressed
- ADR is recorded
