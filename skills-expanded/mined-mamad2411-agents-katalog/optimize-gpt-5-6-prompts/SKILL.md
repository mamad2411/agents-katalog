---
name: optimize-gpt-5-6-prompts
description: Review, simplify, migrate, and create prompts, tool descriptions, agent instructions, or prompt stacks for GPT-5.6 and the GPT-5.6 family. Use when a user provides a prompt and asks to optimize, critique, streamline, rewrite, upgrade, or adapt it for GPT-5.6, or explicitly invokes this skill to improve an existing prompt or draft one from scratch. Do not trigger merely because prompt text appears in unrelated code or documentation without an intent to create, evaluate, or change prompting behavior.
---

# Optimize GPT-5.6 Prompts

## Start from the user's outcome

Determine whether the request is to diagnose, optimize, migrate, or draft from scratch. Identify the intended user-visible result, success criteria, required evidence, permission boundaries, output contract, and true invariants before changing wording.

Read [references/gpt-5-6-guidance.md](references/gpt-5-6-guidance.md) for the detailed review criteria. Read only the sections relevant to the request. Treat it as prompting guidance, not as a source for current API limits, pricing, parameters, or feature availability; retrieve current official OpenAI documentation when those facts matter.

## Review an existing prompt

1. Preserve the goal, factual claims, requested language, artifact type, hard constraints, and required output shape.
2. Find the smallest set of material problems: repetition, contradictions, obsolete scaffolding, vague outcomes, missing completion criteria, unnecessary process rules, irrelevant tools, weak stopping conditions, or unsupported claims.
3. Distinguish true invariants from judgment calls. Keep absolute language only for genuine safety, permission, policy, evidence, business, or schema requirements.
4. Prioritize changes by expected behavioral impact. Do not rewrite merely to impose a preferred style.
5. When behavior may change, recommend representative evals and isolate changes so results remain attributable.

If the prompt is already effective, say so and make only targeted changes.

## Draft a prompt from scratch

Infer safe, low-impact details from context. Ask only for missing information that would materially change the result. Use the smallest useful subset of:

- Role or context
- Personality and collaboration style
- Goal
- Success criteria
- Constraints and approval boundaries
- Tools and routing rules
- Output contract
- Stop, retry, fallback, or abstention rules

State outcomes and decision rules instead of over-prescribing steps. Add examples only when they change behavior.

## Return the result

For an optimization request, default to:

1. **Key findings** — name only consequential issues.
2. **Prioritized recommendations** — explain the highest-impact changes first.
3. **Optimized prompt** — provide a complete, usable revision unless the user requested advice only.
4. **Important changes and validation** — summarize meaningful tradeoffs and suggest focused evals when warranted.

Adapt this structure to the request. Preserve the user's requested format when it conflicts with the default.

## Guardrails

- Do not weaken safety, privacy, policy, evidence, business, approval, or destructive-action constraints.
- Do not invent model capabilities, parameters, product facts, metrics, citations, or evaluation outcomes.
- Surface contradictions that require a material user decision instead of silently choosing a different objective.
- Stop once the result satisfies the stated outcome and constraints. Do not add unrelated requirements or speculative sections.
