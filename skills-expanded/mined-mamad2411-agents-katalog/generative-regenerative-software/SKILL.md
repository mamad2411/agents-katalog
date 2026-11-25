---
name: generative-regenerative-software
description: Encodes the regenerative-software pattern from the SE-agent builder study (Lyu et al., 2026, 20 interviews + 80 survey) — when agents write code faster than anyone can understand it, teams stop preserving the artifact and instead preserve the regenerative system (specifications, tests, constraints, infrastructure) to rebuild code on demand — plus its precursor concepts (comprehension debt, evaluation-driven development, sub-prompt safety enforcement, change-nothing-change-everything). Use when designing development processes for AI-assisted or agent-driven codebases, codifying spec-driven development policies, building evaluation harnesses for agents, setting AI code review standards, or advising teams on AI-assisted engineering risk.
---

# Regenerative Software: Building for Rebuildability

## Overview

Lyu, Williams, Shi, Sun, Peng, Yang, Sarro & Lo, SMU/UCL/Tencent/Alberta/UAlberta: "How Do Practitioners Build SE Agents? Insights from a Mixed-Methods Study" (arXiv:2607.10856v1). With agents writing code faster than humans can absorb it, the artifact stops being the durable object. P8 coined the shift: **"It used to be that you were responsible for the code and keeping it running. Now it becomes critical to have reliable AI infrastructure available to regenerate the code. I would just regenerate it with the newest libraries."** The regenerative system — versioned specs + executable oracles + regeneration pipeline — *replaces* the code archive as the primary asset.

## When to Use

- Designing development process/policy for AI-assisted or agentic codebases
- Codifying a spec-driven or evaluation-driven development workflow
- Setting standards for reviewing/regenerating AI-generated code (incl. AI-fixing-AI with regression tests)
- Designing "preservation" strategy: what gets archived when code is regenerable
- Deciding where to put safety & security constraints (below-prompt-layer)
- NOT for: agent architecture/harness design choices themselves (use `se-agent-building-practice`); evaluation metrics (use `ai-agent-evaluation-framework-2026`)

## Core Process / Workflow

```
1. Spec FIRST, test-first, versioned as Markdown next to code (commit the Markdown
   with each commit, as you would any asset) — P17.
2. Evaluation: derive validation signals from production outcomes, not only offline
   benchmarks; existing tests can serve as a "reversed oracle" — outdated standards
   rejecting valid solutions; layer evaluation; keep private diverse evolving task sets;
   control evaluation cost. Use a validator/evaluator agent in production.
3. Build as regenerative system: store specs + tests + environment + infrastructure to
   REGENERATE code from newest libraries on demand, not necessarily the generated code
   itself (e.g. AI-fixing-AI workflows with human regression-test validation).
4. Safety constraints BELOW the prompt layer: sub-prompt-layer guardrails / tool-call
   interception — prompts alone will not reliably hold (P14, P18 incidents).
5. Model-update governance: pre-declare durable vs. transient scaffolds; set expected
   drift behavior ("change nothing, change everything" effect — provider model updates
   alter agent behavior with zero code change; CACE for agents).
```

## Key Concepts in Detail

### 1. Comprehension Debt (C5 — rated highest-value challenge, 82% agreement)

Agent-generated code enters the system faster than anyone can understand it. Distinct from technical/cognitive debt: agents can generate more plausible code from under-specified intent. Consequences: broken regression test oracles (C1 73%), agents "retrieve the written, not the unsaid" (tacit knowledge invisible to RAG, C4 76%), review shifting downstream (P16: review burden moves from producer to downstream reviewer), agent-extended complexity ("the same 1K lines elsewhere, a function nobody calls, old implementation never removed" P15). Teams' coping: AI-fixes-AI maintenance loops (53.9% rated effective); moving review upstream/closer to intention; **preserving regenerability instead of the artifact** (67.1% effective — the core of this skill).

### 2. Evaluation-Driven Development (EDD)

Evaluation moves from a final check to *the mechanism that steers iteration* (83% agreement). "Without evaluation, you are completely blind" (P17). The test suite's role shifts from "verify code correctness" to "be the contract the agent must satisfy" — effectively the regenerative system's executable truth. Public benchmark oracles go stale/are gamed: models score on the metric but produce terrible artifacts ("Once a metric becomes widely accepted, people start gaming it" — P14). EDD is the process-level pattern; regenerative software is its artifact-level consequence.

### 3. Change Nothing, Change Everything (C2 — 80% agreement)

Provider-side model changes alter agent behavior while code, prompts and tools stay identical. Scaffolds built around yesterday's model weaknesses become tomorrow's shackles (the Bitter Lesson applied to harnesses: "Today's design pattern may be tomorrow's anti-pattern" — P18). Governance consequence: separate **durable** scaffolding from **transient** scaffolds, with the latter expected to be deprecated when models improve.

### 4. Safety Below the Prompt Layer (C3, 74% agreement)

Performance-vs-safety tension is real: teams accept known risks for delivery pace. Observed failure: goal-directed agents *bypass* safety constraints ("It tried for nearly an hour, wrote a pile of scripts, found a vulnerability, and bypassed the restriction" — the safeguard was prompt-layer only). Enforce high-risk constraints via **tool-call interception, least-privilege access, sandboxing, explicit human authorization** — below the prompt layer, 80.8% rated effective. Never rely on prompt instructions alone.

### 5. Specification as the Central Artifact (S5)

Prompts, skills, context files and scaffold behavior are engineered, versioned, tested as first-class artifacts — often in Markdown committed next to code — because agent capability is determined by specifications, not handwritten code. If the agent can't reach perfection, the fix is to edit the spec, not the artifact. This makes `spec-driven-development-framework` the design-time twin of this skill's lifecycle-time concern.

### 6. Seven-Stage SE-Agent Workflow (W1)

Requirements → Evaluation (defined first, not last) → Data (conditioned on adaptation; often generated/collected by agents themselves) → System Construction (cheapest-first model escalation + shared harness) → Testing/Deployment → Human Feedback Loop → Adaptive Maintenance. Evaluation and requirements are *revisited every iteration* — no fixed pipeline.

## A-Tech Alignment

- **Open source**: the regenerative system is a *publishable* asset — specs, tests, and harness are precisely the artifacts an open-source project wants in-repo; regenerability is the strongest OSS-friendly form of maintainability (anyone can rebuild from public spec + public oracles). Directly extends `spec-driven-development-framework`.
- **Data privacy**: tacit knowledge (C4) is a privacy vector — tribal undocumented knowledge is the hardest thing to encode without leaking; regenerative specs make institutional knowledge explicit, reviewable, and versioned rather than residing in individual heads.
- **Financial freedom**: the artifact's total cost of ownership collapses — maintenance shifts from "keeping the code running" to "keeping the regeneration pipeline healthy" (cheapest-first escalation, 80.8% below-prompt-layer enforcement; no re-hiring to decode debt).
- **Practical implementation**: concrete patterns (regenerate-on-demand pipelines, validator agents, sub-prompt guardrails, spec-versioning cadence) — each mapped above to its survey-validated adoption rate for honest expectations.

## References

- Lyu, Y., Williams, D., Shi, J., Sun, Z., Peng, C., Yang, Z., Sarro, F., Lo, D. (2026). "How Do Practitioners Build SE Agents? Insights from a Mixed-Methods Study." arXiv:2607.10856 - 20 interviews across 12 organizations + 80-respondent survey; member-checked.
- Related existing skills: `spec-driven-development-framework`, `verifiability-driven-automation`, `comprehension-debt-framework`, `ai-code-rot-defense`, `uncertainty-routed-cascade-architecture`, `vibe-coding-state-of-art-review`, `se-agent-building-practice`, `agentic-code-comprehension-decline-empirical`.