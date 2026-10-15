---
name: deep-discovery
description: Use when the user asks for deep discovery, 100-question brainstorming, idea interrogation, architecture stress testing, strategy vetting, weakness finding, hole-poking, exhaustive exploration, planning or auditing Codex plugins or skills, or pre-commitment review of a design, plan, strategy, architecture, product, business idea, trading system, or problem space.
---

# Deep Discovery

A structured self-interrogation framework that exhaustively explores a topic through
100 sequential questions, each building on the previous answer. Designed to be
used in Codex as a skill for rigorous, sequential exploration before committing
to a design or decision.

## Preflight

1. Identify the topic, available context, focus, and starting point. If any of
   those are too ambiguous to run a useful interrogation, ask at most three
   clarifying questions before starting.
2. Choose the mode:
   - **Evaluation:** an existing design, architecture, strategy, or plan exists.
   - **Exploration:** the user is starting from scratch.
   - **Comparison:** the user is choosing between two or three options.
3. Choose the closest domain pattern: software architecture, code review,
   Codex plugin/skill creation, business/product, trading/financial, or general.
   Use `references/question-patterns.md` as the index, then read only the relevant
   reference file when domain-specific prompts would improve the run.
4. After enough context is available, run the process without further human
   input unless the user explicitly asks to participate.

## How It Works

The 100-question process is a **self-dialogue**: ask a question, answer it, then
ask the next question based on what the answer revealed. The questions naturally
progress through phases:

### Question Progression

| Phase | Questions | Focus |
|-------|-----------|-------|
| Foundation | Q1-Q10 | Goal, constraints, assumptions, what makes this unique |
| Mechanics | Q11-Q30 | How it works, components, data flow, dependencies |
| Stress Testing | Q31-Q50 | Edge cases, failure modes, what breaks first |
| Competitive Analysis | Q51-Q65 | What exists, what's different, what's the real edge |
| Feasibility | Q66-Q80 | Can this actually be built/done, what are the blockers |
| Refinement | Q81-Q90 | Improvements, optimizations, what was missed |
| Synthesis | Q91-Q100 | Final architecture, honest assessment, actionable output |

### Rules for Questions

1. **Q1 is always:** "What is the goal, and how do we get there?"
2. Each question MUST build on the previous answer; avoid random jumps.
3. Be brutally honest; surface problems instead of hiding them.
4. Challenge assumptions with questions like "Is that actually true?"
5. Go concrete, not abstract: use specific numbers and scenarios.
6. If an answer reveals a critical flaw, spend multiple questions exploring it.
7. The final 10 questions must synthesize everything into actionable output.
8. Do not abbreviate the run below 100 questions unless the user explicitly asks
   for a shorter version.

## Running the Process

Run the process in the current Codex conversation by default. If the user
explicitly asks to delegate the work to a sub-agent, use Codex's available
sub-agent mechanism and summarize the returned findings. Do not assume a
delegation tool is available, and do not refer to legacy tool names or custom
agent manifests from other harnesses.

### Prompt Template

Use this structure for the deep-discovery run:

```
Topic: [what we're exploring]
Context: [relevant background - what's already been decided, constraints, goals]
Focus: [what specifically to evaluate - architecture? strategy? feasibility?]
Starting point: [any existing design or proposal to interrogate, or "from scratch"]
Mode: [evaluation | exploration | comparison]
Domain pattern: [software architecture | code review | codex plugin/skill creation | business/product | trading/financial | general]

Do a rigorous 100-question self-brainstorm. Each question builds on the last.
Start with "What is the goal, and how do we get there?" and dig progressively
deeper through mechanics, stress testing, competitive analysis, feasibility,
and synthesis.

Be brutally honest. Find every weakness, every edge case, every failure mode.
Also identify what's strong and worth keeping.

At the end, provide:
1. Questions asked: 100
2. Domain pattern used
3. A numbered list of the top 10 critical issues found
4. A numbered list of the top 10 strengths
5. Specific changes recommended, with rationale
6. A revised proposal or architecture if the original needs significant changes
7. The honest bottom line: one paragraph, no sugar-coating
```

### Handling the Output

After completing the run:

1. **Extract the key findings** - summarize the top issues and strengths for the user.
2. **Present the revised architecture/proposal** if one was generated.
3. **Integrate findings** into the current design process.
4. Do NOT dump the full 100 Q&A into the conversation unless the user explicitly asks for it; summarize the insights.

## Variations

### Evaluation Mode

When an existing design/architecture/plan exists, focus the 100 questions on
interrogating that specific proposal. Include the full design and focus on
finding flaws, edge cases, and missing constraints.

### Exploration Mode

When starting from scratch (no existing proposal), the 100 questions should
build toward a complete design. The output should be a fully-formed proposal
that emerged from the questioning process.

### Comparison Mode

When choosing between 2-3 options, run a separate 100-question process for each,
then compare the findings. If the user explicitly asks for delegated or parallel
work and Codex exposes a suitable mechanism, these runs may be delegated.
Synthesize a side-by-side comparison of their top issues, strengths, and revised
proposals to present a clear recommendation to the user.

## Integration with Other Skills

- **Before brainstorming:** Run discovery to deeply understand the problem space
- **After brainstorming:** Run discovery to stress-test the proposed design
- **Before writing plans:** Run discovery to validate the architecture
- **During debugging:** Run discovery to exhaustively explore root causes

## Additional Resources

### Reference Files

- **`references/question-patterns.md`** - Index of available domain pattern files.
- **`references/software-architecture.md`** - Architecture and system design patterns.
- **`references/code-review.md`** - Patch, branch, and implementation review patterns.
- **`references/codex-plugin-creation.md`** - Codex plugin and skill planning/audit patterns.
- **`references/business-product.md`** - Business strategy and product patterns.
- **`references/trading-financial.md`** - Trading system and financial strategy patterns.
- **`references/general-pattern.md`** - Universal fallback pattern and discovery tips.
