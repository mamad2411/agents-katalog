---
name: analytical-prompts
description: Eight copy-paste prompts for deeper AI thinking — replacing "summarize this" with prompts that extract strategic insights, turn information into action plans, surface hidden assumptions, compare opposing views, distil for a specific role, build reusable frameworks, extract contrarian takeaways, and identify leverage points. Use when the user has content (article, report, meeting notes, strategy doc, research) and wants real analysis rather than a summary. Source: @smarterwithai.news "Stop Asking AI to Summarise — 8 Better Prompts for Real Thinking."
---

# Analytical Prompts — 8 Better Prompts for Real Thinking

Source: @smarterwithai.news "Stop Asking AI to 'Summarise' — 8 Better Prompts for Real Thinking."

> Stop asking AI to summarize. These 8 prompts extract strategic value instead.

## The 8 prompts

---

### 01 — Extract Strategic Insights

Turn noise into signal: identify the decisions this information informs.

```
Act like a strategy consultant. Identify the 5 most valuable insights from the content below and explain what decisions each one informs.

[PASTE CONTENT HERE]
```

---

### 02 — Turn Info Into Action

Convert information into a concrete plan with owners and metrics.

```
Translate this into a 5-step action plan with clear owners, quick wins, and measurable results.

[PASTE CONTENT HERE]
```

---

### 03 — Surface Hidden Assumptions

Find the invisible logic holding the argument together — and what happens if it's wrong.

```
Reveal the unstated assumptions or blind spots shaping this argument and what changes if they're wrong.

[PASTE CONTENT HERE]
```

---

### 04 — Compare Opposing Views

Map the real disagreement: where perspectives align vs. where they conflict.

```
Map this idea against two competing perspectives. Show where they align, where they differ, and which context fits each.

[PASTE CONTENT OR STATE THE IDEA HERE]
```

---

### 05 — Distil for a Specific Role

Filter a complex piece down to what actually matters for one decision-maker.

```
Filter this through the lens of a [ROLE — e.g. marketer / founder / engineer / investor]. Only include what matters most for their decisions.

[PASTE CONTENT HERE]
```

Common roles to substitute:
- Marketer → reach and conversion
- Founder → cash flow and growth
- Engineer → feasibility and scale
- Investor → return and risk
- Operations lead → process and bottleneck
- Customer → price and value

---

### 06 — Build a Reusable Model

Extract the repeatable framework hidden in the text so it can be applied again.

```
Extract the repeatable framework hidden in this text. Label each stage, its input, and its output.

[PASTE CONTENT HERE]
```

---

### 07 — Extract Contrarian Takeaways

Find the insight that smart, well-informed people would push back on.

```
Find insights that would challenge smart peers. Keep them credible but unexpected. Write each as a sharp one-liner.

[PASTE CONTENT HERE]
```

---

### 08 — Identify Leverage Points

Find where small actions create outsized results.

```
Highlight the 3 leverage points where small actions could create outsized results. Explain why each one matters.

[PASTE CONTENT HERE]
```

---

## When to reach for each prompt

| If you want to… | Use prompt |
|---|---|
| Know what to do next | 02 (Action Plan) |
| Stress-test a plan or argument | 03 (Hidden Assumptions) |
| Understand a disagreement | 04 (Opposing Views) |
| Brief a specific person | 05 (Distil for Role) |
| Build a repeatable process | 06 (Reusable Model) |
| Find non-obvious insights | 01 (Strategic Insights) or 07 (Contrarian) |
| Prioritize where to focus | 08 (Leverage Points) |

## Combine with multi-agent-debate

For high-stakes analysis, run Prompt 03 (Hidden Assumptions) first to surface weaknesses, then use `multi-agent-debate` to stress-test the full argument.

## Related skills

- **multi-agent-debate**: Adversarial 3-round system for high-stakes decisions
- **business-decision-frameworks**: Structured tools for the action-planning step
- **business-intelligence-report**: Package the output of these prompts into a formal report
- **ai-research-analyst**: Use for sourcing before running Prompt 01 or 07
