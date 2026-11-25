---
name: prompt-engineering
description: Prompt engineering knowledge base — technique taxonomy with decision tree, prompt template patterns and formatting conventions, OWASP LLM Top 10 security checklist, eval frameworks and testing guide, context engineering, structured output contracts, multi-agent orchestration patterns, cost optimization. Use when designing prompts, reviewing prompt quality, building AI features, creating AI assets, or auditing LLM security.
user-invocable: false
---

# Prompt Engineering

Comprehensive prompt engineering knowledge base. Provides actionable patterns, checklists, and guides for designing, securing, evaluating, and optimizing LLM prompts and agent systems.

## When to Use

- Designing or reviewing prompt templates (system, developer, user prompts)
- Building tool calling schemas and structured output contracts
- Evaluating prompt quality — accuracy, safety, cost, latency
- Auditing LLM security against OWASP LLM Top 10
- Designing multi-agent orchestration and handoff protocols
- Optimizing prompt cost and latency
- Creating or reviewing Windsurf AI assets (rules, workflows, skills — all are prompts)
- Setting up prompt versioning and observability

## When NOT to Use

- Implementing backend/frontend code (use `software-engineer` role + stack-specific role)
- Infrastructure and deployment (use `devops-engineer` role)
- Writing code tests (use `qa-engineer` role + `test-strategy` skill)
- Content writing (use `content-writer` role)
- Context pipeline design, memory engineering, agent harness, RAG architecture, multi-agent orchestration, production AI checklists → use `context-engineering` skill

## Key Concepts

### Prompt as System

A prompt is not a string — it is a **system** composed of:
1. **Instruction hierarchy**: System prompt > Developer prompt > User prompt > Retrieved content
2. **Context assembly**: What enters the context window, in what order, with what priority
3. **Output contract**: Schema, format, constraints, error handling, fallback behavior
4. **Tool interface**: Available tools, their schemas, permissions, composition patterns
5. **Guard rails**: Safety filters, refusal policies, output validators
6. **Versioning**: Immutable versions, deployment tags, audit trail

### Core Principles

1. **Eval-first**: Define how to measure before changing anything
2. **Simplest technique**: Zero-shot → few-shot → CoT → chaining. Escalate only when simpler fails
3. **Explicit over implicit**: Spell out constraints, output format, edge cases. Never assume the model "knows"
4. **Separation of concerns**: Instructions vs data vs examples — always delimited
5. **Grounding**: Prefer citations and verifiable data over unanchored claims
6. **Least privilege**: Minimal tool permissions per agent. HITL for high-impact actions
7. **Cost awareness**: Every token costs money and time. Compress, cache, route

## Resource Files

| File | Contents |
|---|---|
| `technique-guide.md` | Technique selector overview and reading map |
| `technique-guide-core.md` | Zero-shot, few-shot, CoT, self-consistency, constrained generation |
| `technique-guide-agentic.md` | ToT, ReAct, chaining, reflection, RAG, meta-prompting, provider guidance |
| `prompt-template-patterns.md` | Prompt structure overview and pattern index |
| `prompt-template-foundations.md` | Delimiters, system prompt architecture, few-shot formatting, CoT formatting |
| `prompt-template-contracts.md` | Output schemas, tool schemas, prompt registry, provider-specific adaptations |
| `security-checklist.md` | OWASP LLM Top 10 mapped to prompt-level mitigations with checklist |
| `eval-and-testing-guide.md` | Eval workflow overview and decision map |
| `eval-datasets-and-graders.md` | Dataset curation, grader types, grader selection |
| `eval-deployment-and-monitoring.md` | Regression gates, A/B testing, deployment rollout, monitoring |

## Integration

- **Follows rules**: `prompt-engineer` role (prompt system architecture, security, eval-first quality)
- **Used by workflows**: `ai-skills` skill (all assets are prompts), `feature-dev` skill (AI features), `code-review` skill (prompt quality review)
- **Companion skills**: `context-engineering` skill (context pipeline design, memory engineering, agent harness, RAG architecture, multi-agent orchestration, production checklists), `asset-validation` skill (AI asset format validation), `code-review` skill (review checklists)
- **Collaborates with roles**: `software-engineer` role (prompt integration), `qa-engineer` role (prompt regression tests), `product-manager` role (success metrics)
