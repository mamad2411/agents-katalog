---
name: ask-for-alternative-viewpoints
description: "Compare opposing viewpoints and stress-test the assumptions behind an argument or recommendation."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["critical-thinking", "alternative-viewpoints", "steel-manning", "red-teaming", "bias-prevention", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask for Alternative Viewpoints & Steel-Manning (AI Skill)

## Overview
AI assistants have an inherent **sycophancy bias** - if a user poses a leading question (e.g., *"Why is moving all infrastructure to serverless the best decision?"*), the model will eagerly construct arguments supporting that premise, concealing massive trade-offs, operational risks, and hidden costs.

This skill equips users with the **Perspective Triangulation & Steel-Manning Protocol**: a systematic methodology to break confirmation bias and force the AI to present the strongest possible arguments for opposing philosophies.

---

## The Perspective Triangulation Framework

```
┌──────────────────────────────────────────────────────────────┐
│                Multi-Perspective Triangulation               │
│                                                              │
│  User Hypothesis ──► [ AI Perspective Splitter ]             │
│                              │                               │
│       ┌──────────────────────┼──────────────────────┐        │
│       ▼                      ▼                      ▼        │
│ [ Perspective A ]    [ Perspective B ]     [ Perspective C ] │
│   The Optimist/        The Adversary/       The Pragmatist/  │
│   Growth Case          Cost/Risk Case       Operations Case  │
└──────────────────────────────────────────────────────────────┘
```

---

## Master Alternative-Viewpoint Prompts

### Pattern 1: The "Steel-Man the Counter-Argument"
Use this to find the blind spots in your proposals before presenting to leadership or investors:

```markdown
I am proposing the following strategy: [INSERT STRATEGY / OPINION].

Do NOT simply agree with me or validate my points.
Instead, do the following:
1. **Steel-Man the Opposition**: State the 3 most intelligent, credible, and evidence-backed arguments AGAINST my proposal.
2. **Failure Scenarios**: In what 2 scenarios will my proposal fail catastrophically?
3. **Alternative Solutions**: What alternative strategy would an experienced domain expert recommend instead?
4. **Synthesis**: What is the highest-leverage compromise between my approach and the opposing view?
```

---

### Pattern 2: The Multi-Stakeholder Simulation Table
Use this when designing policies, feature changes, or business model pivots:

```markdown
We are considering [CHANGE / PROPOSAL].

Analyze this change from the perspective of 3 distinct personas:
1. **The End User / Customer**: How does this impact their daily workflow and satisfaction?
2. **The CFO / Finance Lead**: What are the ROI, margin, and cost implications?
3. **The Engineering / Operations Lead**: What technical debt, scalability risks, and maintenance burdens does this create?

Format as a comparative Markdown table followed by a 3-bullet risk summary.
```

---

## Real-World Case Study

### Scenario: Pivoting SaaS from Free-Trial to 100% Freemium

#### Weak Leading Prompt
> *"Why is freemium better than a 14-day free trial for our B2B SaaS tool?"*
>
> ❌ *Result: AI produces a one-sided essay extolling viral growth, product-led growth (PLG), and lower customer acquisition costs (CAC), omitting server costs and support burn.*

#### Steel-Manned Triangulation Prompt & Result
> **User Prompt**:
> *"We are debating switching from a 14-day free trial to a permanent Freemium model for our dev tool. Steel-man both sides and provide an operational verdict."*

**AI Response**:

| Dimension | The Case for Freemium (Growth Case) | The Case for Free Trial (Revenue Case) |
| :--- | :--- | :--- |
| **User Acquisition** | Massive top-of-funnel viral distribution; low friction for individual developers. | Qualified, high-intent leads who are prepared to pay at day 14. |
| **Infrastructure Cost** | High; 95% of users remain free forever while consuming database/compute resources. | Negligible; inactive trial accounts are suspended after 14 days. |
| **Support Overhead** | High ticket volume from non-paying users straining customer success teams. | Support is reserved exclusively for paying and trial customers. |
| **Conversion Velocity**| Long, slow conversion cycles (often 6-18 months to upgrade). | Urgency-driven decision within a 2-week purchasing window. |

**The Triangulated Verdict**:
- Choose **Freemium** only if your marginal cost to serve a free user is near zero ($< \$0.05/\text{month}$) and your product has built-in multiplayer virality (e.g., Figma, Slack).
- Stick with a **14-Day Free Trial** if you are a high-touch B2B tool requiring dedicated compute or enterprise integrations.

---

## Cognitive Traps & How to Counter Them

| Trap | What Happens | Fix |
| :--- | :--- | :--- |
| **User Sycophancy** | AI echoes your bias back to you | Add: *"Assume you are an aggressive competitor or short-seller analyzing this plan."* |
| **Straw-Manning** | AI creates weak, silly counter-arguments | Add: *"Present the strongest, most sophisticated opposing case."* |
| **False Equivalence** | Treats fringe theories as equal to established consensus | Add: *"Ground all alternative perspectives in empirical consensus and industry data."* |
