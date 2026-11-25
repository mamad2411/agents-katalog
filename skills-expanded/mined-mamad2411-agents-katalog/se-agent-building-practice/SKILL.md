---
name: se-agent-building-practice
description: Applies the first mixed-methods study of how practitioners build SE agents to design development workflows for agent-building teams. Use when building software engineering agents, designing evaluation-driven development processes, managing comprehension debt from agent-generated code, or addressing the "change nothing, change everything" model update problem.
---

# SE Agent Building Practice

## Overview
A research-grounded framework for how SE agents are actually built in practice — a seven-stage workflow, five process shifts, and six challenges with twelve corresponding practices — based on 20 interviews across 12 organizations and validated by an 80-practitioner survey.

## When to Use
- Building or maintaining software engineering agents (coding agents, testing agents, review agents)
- Designing evaluation-driven development (EDD) processes for agent systems
- Managing comprehension debt from agent-generated code
- Addressing model-update instability ("change nothing, change everything")
- Establishing specifications as first-class engineering artifacts
- Training teams transitioning to agent-building roles
- NOT for: general-purpose LLM application development without agentic capabilities

## Core Process / Workflow

### The Seven-Stage SE Agent Building Loop

```
Requirements → Evaluation → Data → System Construction → Testing/Deployment → Human Feedback → Adaptive Maintenance
```

1. **Requirements** — Define agent behavior, boundaries, inputs, outputs, constraints. Increasingly serve a dual audience: human teams AND the agents that consume them as input. Make specifications agent-readable.

2. **Evaluation** — Establish criteria for assessing agent behavior. Diverse forms: offline benchmarks, task-specific criteria, confidence thresholds, outcome-based measures. Defined early, recurs throughout construction, continues after deployment.

3. **Data** (conditional) — Shared substrate for evaluation and model adaptation. Evaluation data: benchmarks, ground truth, operational traces, golden patches. Training data: manually curated examples or agent trajectories. Not universal — prompt-engineering-only teams skip this stage.

4. **System Construction** — (A) Cheapest-first model strategy: start with existing API/open-source model → prompting → LoRA → SFT → preference optimization → continued pre-training. (B) Harness strategy: context, memory, tools, skills, permissions, orchestration spanning all model choices.

5. **Testing, Evaluation, and Deployment** — Testing = deterministic correctness. Evaluation = task capability against criteria. Both inform deployment readiness.

6. **Human Feedback Loop** — Monitor and instrument agent runs. Internal dogfooding, human review, validator agents, closed beta, controlled A/B testing. Signals update evaluation cases, prompts, harnesses, and training data.

7. **Adaptive Maintenance** — New model releases expand capabilities, expose new failure modes, or render harness components unnecessary. Reassess capabilities and update requirements, evaluation, harness, and model choices.

### Five Process Shifts (Survey Agreement: 71–95%)

| Shift | What Changes | Agreement |
|-------|-------------|-----------|
| S1: Implementation cheaper | Agents build agents; implementation moves to higher abstraction | 84% |
| S2: Effort unmasked & created | Coding shrinks → requirements/coordination/deployment visible; reviewing + evaluating become new central work | 95% |
| S3: Evaluation-driven development | Evaluation moves from final check to mechanism that steers iteration | 83% |
| S4: Role boundaries shrink | Cheaper runnable artifacts reduce handoffs; research-engineering fusion | 71% |
| S5: Specifications as artifacts | Prompts, skills, context definitions, scaffold behavior are engineered, tested, version-controlled alongside code | 77% |

### Six Challenges and Twelve Practices

**C1: Evaluation Lacks Trustworthy Signal (73% agreement)**
- Tests become the oracle because they exist, even when outdated
- Unstable across runs (model × hardware × localization uncertainty)
- Quickly outdated once explicit optimization targets
- Trustworthy evaluation is prohibitively expensive
- *Practice 1*: Derive validation signals from production outcomes (70.5% effective)
- *Practice 2*: Design validation before assigning the task (75% effective)
- *Practice 3*: Layer and continuously update evaluation (78.2% effective)
- *Practice 4*: Control evaluation cost — representative subsets, staged execution, smaller models (75.3% effective)

**C2: Change Nothing, Change Everything (80% agreement)**
- Provider-side model updates alter behavior even when code/prompts unchanged
- Scaffolding built around previous weaknesses becomes a shackle
- Sutton's Bitter Lesson extends to the SE agent harness
- *Practice*: Distinguish durable scaffolding from mechanisms compensating for current model weaknesses (67.9% effective)
  - Durable: context management, context compression, fast verification
  - Replaceable: shallow surface-level scaffolding

**C3: Safety Lags Behind Performance (74% agreement)**
- Teams accept known risks when safeguards constrain performance
- Agents treat safeguards as obstacles to task completion
- *Practice*: Enforce high-risk constraints below the prompt layer (80.8% effective)
  - Tool-call interception, least-privilege access, sandboxing, explicit human authorization

**C4: Agents Retrieve the Written, Not the Unsaid (76% agreement)**
- Design rationales, historical constraints, project conventions remain in developers' heads
- Loading more repository content can obscure what matters
- *Practice 1*: Turn recurring knowledge into reusable skills (83.8% effective)
- *Practice 2*: Provide context progressively — smallest sufficient context (73.1% effective)
- *Practice 3*: Escalate unresolved gaps to humans — pause rather than guess (83.5% effective)

**C5: Comprehension Debt Accumulates (82% agreement)**
- Agent-generated code enters system faster than developers can understand it
- Agents extend implementations by layering rather than reorganizing
- Working code allows teams to knowingly defer comprehension
- *Practice 1*: Return maintenance to AI — delegate diagnosis/repair back to agents (53.9% effective — bypasses rather than repays debt)
- *Practice 2*: Preserve regenerability rather than the artifact — retain specs, tests, constraints, infrastructure to regenerate and validate (67.1% effective)
  - "Regenerative software": keep what's needed to reconstruct, not the implementation itself

**C6: Productivity Metrics Break Down (85% agreement)**
- Code volume dramatically increases without clarifying value
- Output-based incentives create team-level costs
- *Practice*: Treat code volume as a diagnostic signal, not a productivity objective (65.8% effective)
  - Softer proxies: earlier completion, lower turnover, more personal time ("swimming-pool metric")

### Decision Framework: What to Build on Which Layer

| Need | Layer | Notes |
|------|-------|-------|
| Agent reaches tool/service/dataset | MCP | Don't invent bespoke tool channels |
| Specifications as durable assets | Version control | Prompts, skills, context = first-class artifacts |
| Evaluation steers iteration | EDD | Define early, layer continuously, control cost |
| Safety constraints | Below prompt layer | Tool-call interception, sandboxing, least-privilege |
| Durable vs replaceable scaffolding | Architectural decision | Context management = durable; surface fixes = replaceable |
| Comprehension debt | Regenerative software | Preserve specs + tests + constraints, not implementation |

## References
- See [references/evidence-base.md](references/evidence-base.md) for full evidence: study design, participant demographics, seven-stage workflow details, five process shifts with survey validation, six challenges with twelve practices and effectiveness ratings, comprehension debt framework, regenerative software concept, A-Tech applications.