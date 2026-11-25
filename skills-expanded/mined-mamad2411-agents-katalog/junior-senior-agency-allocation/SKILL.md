---
name: junior-senior-agency-allocation
description: Applies the first qualitative study of how junior and senior software engineers allocate agency with agentic AI tools to design team practices, mentorship pipelines, and code review processes for AI-mediated development. Use when designing onboarding for AI-native engineers, structuring prompt-and-code reviews (PCRs), managing agency erosion from AI tools, or evolving the junior-to-senior career pipeline in AI-mediated environments.
---

# Junior-Senior Agency Allocation in AI-Mediated Software Engineering

## Overview
A three-phase qualitative study (20 engineers: 10 juniors, 10 seniors) revealing how agency is preconfigured by company policies before individual preferences matter, how familiarity with task and tool drives divergent agency patterns, and how the junior-to-senior pipeline must evolve from gradual technical mastery to "earning judgment through deliberate restraint."

## When to Use
- Designing onboarding processes for AI-native junior engineers
- Structuring mentorship in AI-mediated development environments
- Designing prompt-and-code reviews (PCRs) as accountability mechanisms
- Managing agency erosion, imposter syndrome, and skill atrophy from AI tools
- Evolving the talent pipeline from "gradual responsibility increase" to "immediate accountability with guardrails"
- Deciding when AI agents vs human mentorship is appropriate for knowledge transfer
- NOT for: purely generative AI use cases without agentic capabilities (autonomous action)

## Core Process / Workflow

### The Agency Allocation Framework

**Layer 1: Organizational Preconfiguration**
Agency is configured before the first prompt is sent:
- Company policies: mandates, allow-lists, security constraints
- Tooling defaults: approved internal tools, prohibited non-company AI
- CI guardrails, data protection requirements
- "Use AI now" top-down push creates subtle agency loss

**Layer 2: Task Familiarity Drives Agency**

| Familiarity | Senior Pattern | Junior Pattern |
|-------------|---------------|----------------|
| High (familiar codebase/task) | Detailed delegation; small, reviewable diffs; iterative refinement | Constraint-based: small targeted edits, heavy verification, scope limiting |
| Low (unfamiliar codebase/task) | Strategic oversight: AI for idea generation, low-level tasks, understanding; separate design from code generation | Oscillation: over-reliance ↔ defensive resistance; scope control struggles |

### The Five-Stage Interaction Pattern Taxonomy

```
Active Collaboration → Guided Generation → Supervised Generation → Passive Supervision → Full Autonomy
```

Movement along this spectrum is driven by familiarity, trust calibration, and time pressure. The risk: juniors drift toward passive supervision under time pressure, creating comprehension debt.

### Three Evolving Practices

**1. Preserving Individual Agency**
- Incremental changes (small, test-bounded diffs)
- Interrupt and verify outputs
- Three non-negotiables: (a) interruptibility/override, (b) legible provenance with detailed verification, (c) small, test-bounded diffs
- "To remain autonomous is to be the author of one's reasons, not merely the approver of outputs."

**2. Evolving the Mentorship Pipeline**
- Senior role transforms into "Socratic guides and organizational anchors"
- Shift from answering coding questions (AI does this) to asking questions that develop junior judgment
- Junior growth reframes as "earning judgment through deliberate restraint"
- Pipeline transforms from gradual responsibility → "immediate accountability with guardrails"

**3. Prompt & Code Reviews (PCRs)**
- Accountability preserves agency
- Juniors document and justify 2-3 key prompts that shaped their solution
- Seniors oversee accountability, ensure juniors remain authors of their reasoning
- Selective, lightweight artifacts focusing on critical decision points

### When AI Can vs Cannot Be a Mentor

**AI as mentor (basic guidance):**
- Surface best practices and patterns
- Available fallback when seniors not around
- Basic questions requiring little context
- "A faster, more interactive Google and a rubber duck"
- Create messes faster to learn from

**Human mentorship required (irreplaceable):**
- Context-specific organizational knowledge ("why" questions)
- Critical thinking and judgment development
- System thinking and architectural decisions
- Failure anticipation
- Guardrails against AI's context blindness and overconfidence
- "At no point can you hand over your expertise. You're just handing over the workload."

### Key Findings: Junior-Senior Divide

| Dimension | Juniors | Seniors |
|-----------|---------|---------|
| Pre-AI instincts | AI-native: "the whole time I've been a software engineer, there has been AI" | Foundational instincts from pre-AI remain critical for steering tools |
| High familiarity | Constraint-based: break work into sub-steps, scope files first, crosscheck | Detailed delegation: arrive with plan, delegate only what fits, iterate |
| Low familiarity | Over-reliance or defensive resistance; "free-falling... spamming the agent button" | Strategic oversight: AI for ideas/low-level tasks, separate design from generation |
| Growth | Imposter syndrome, loss of ownership feelings; "It has my name on it, but I have no idea why it works" | Growth through trial-and-error, strong mental models, soft skills; "coding is the easiest part" |
| AI as mentor | First mentor for basic questions; reduces senior pinging | Positioned as one tool among many; "always there, but never in charge" |
| Skill concern | "Critical thinking muscle" atrophying; "what I do is go to Instagram" while agent buffers | Warn against skill degradation; "don't take it at face value. Do your research." |

### Practical Implementation: The PCR Process

```
1. Junior completes task with AI agent
2. Junior self-curates 2-3 key prompts that shaped the solution
3. Junior writes brief rationale for chosen approach
4. Senior reviews: code + prompts + rationale
5. Senior provides feedback on:
   - Code quality
   - Prompting strategy
   - Whether junior understood the AI's output
   - Whether AI changed anything unexpected
6. Patterns identified: over-reliance, better prompting strategies, incorrect AI suggestions accepted
```

**Senior review feedback categories:**
- Start with understanding (Ask mode before Act mode)
- Tighten prompts (merge related prompts, add detail)
- Prefer small, testable batches
- Proper use of modes and basic tools (grep, debuggers, logs)
- Constant vigilance (read diffs meticulously, call out AI errors)

## References
- See [references/evidence-base.md](references/evidence-base.md) for full evidence: three-phase study design, participant demographics, ACTA methodology, agency allocation patterns by familiarity, interaction pattern taxonomy, mentorship evolution, PCR design, imposter syndrome findings, A-Tech applications.