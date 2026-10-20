---
name: agentic-cognitive-engagement-decline
description: Framework for understanding and countering the decline in software engineers' cognitive engagement when working with agentic coding assistants, using cognitive forcing designs and multimodal interaction. Use when designing AI coding assistants, diagnosing over-reliance and shallow engagement in agentic workflows, or building cognitive-forcing mechanisms into AI tools. NOT for traditional (non-agentic) IDE autocomplete tools, or for fully autonomous agents with no human interaction.
---

# Agentic Cognitive Engagement Decline

## Overview
A formative study (Catalan, Dizon, Monderin & Kuang, 2026) reveals that software engineers' cognitive engagement consistently declines as tasks progress when working with agentic coding assistants (ACAs). Engineers allocate the most cognitive resources during the planning phase, but engagement drops during execution due to information overload, and minimal resources are allocated to evaluating the output vs. the process. This "greedy allocation strategy" leads to shallow engagement and missed critical details — a risk amplified by LLM hallucinations and poisoning attacks.

## When to Use
- Designing agentic coding assistants (Cline, Claude Code, Codex, Devin)
- Diagnosing over-reliance and shallow engagement in agentic coding workflows
- Building cognitive-forcing mechanisms into AI-assisted development tools
- Designing "Tools for Thought" that protect and augment human cognition rather than displacing it
- Evaluating whether an ACA design encourages System 1 (fast, shallow) or System 2 (analytical, deep) thinking
- NOT for traditional (non-agentic) IDE autocomplete (no planning/execution/evaluation phases)
- NOT for fully autonomous agents with no human interaction

## Core Process / Workflow

### 1. The Three-Phase Engagement Decline Model

| Phase | Engagement Level | What Happens | Risk |
|---|---|---|---|
| **Planning** | High | Engineer comprehends prompt, reviews ACA's plan, answers clarifying questions | Low — germane cognitive load |
| **Execution** | Declining | ACA generates code, invokes tools, produces large text output | Information overload → disengagement ("I'm not reading all of that") |
| **Evaluation** | Minimal | Engineer checks output correctness but not process correctness | Output-only validation misses process-level issues; "greedy allocation strategy" |

### 2. Diagnosis: Bloom's Taxonomy Assessment
Use Bloom's Taxonomy to assess cognitive engagement at each phase:

| Level | Question | Finding |
|---|---|---|
| **Remember** | Can the engineer recall key interaction details? | None recalled the number of functions; only half recalled the folder name |
| **Understand** | Can the engineer summarize what functions do? | Only half could reliably summarize the first function |
| **Analyze** | Can the engineer determine function call order and edge-case handling? | Only half felt confident about edge cases |
| **Evaluate** | Does the engineer review the process, not just the output? | All evaluated only the "happy path"; none reviewed the underlying process |

**Key insight:** Engineers recall, understand, analyze, and evaluate primarily the "happy path" — the sequence of steps leading to the correct output. They overlook critical issues, edge cases, and the process that generated the output.

### 3. Design Opportunity 1: Communicate Beyond Text
Text-only communication during execution causes information overload and disengagement. Solutions:
- **Visualizations:** Flowcharts, graphs, mind maps to communicate plans and reasoning in a presentable format
- **Voice:** Natural, human-like speech synthesis acts as a favorable social cue (Liew et al., 2025; Beege & Schneider, 2023)
- **Multiple AI voice technologies** have shown significantly lower perceived cognitive load and improved retention/recall (Liew et al., 2025)

### 4. Design Opportunity 2: Cognitive Forcing Designs
Interventions applied during the AI's decision-making to disrupt its reasoning and force the user into analytical (System 2) thinking:
- **Slow down the AI's decision:** "Slowing down" has been shown to greatly increase user accuracy of assessment (Park et al., 2019)
- **Delay AI suggestions:** In usability testing (Kuang et al., 2024), AI suggestions shown only after the user critically analyzed the demonstration resulted in improved perception of efficiency and trust
- **Cognitive forcing functions** (Buçinca et al., 2021; Ghosh et al., 2026): disrupt AI reasoning at decision points to force user analysis

### 5. The "Tools for Thought" Framing
The design challenge is not purely technical — it's about how ACAs protect and augment human cognition rather than displacing it. ACAs must function not merely as autonomous task performers but as **Tools for Thought** that actively support human reasoning and sensemaking.

Key principles:
- ACAs should **support rich communication** (multimodal) rather than immediately providing solutions
- ACAs should **intentionally provoke reflection** rather than optimizing for immediate task completion
- Drawing from pair-programming practices: collaboration is inherently multimodal and includes instructional scaffolding — ACAs should mirror this

### 6. Cognitive Load Theory Alignment

| Load Type | What It Is | Design Implication |
|---|---|---|
| **Intrinsic** | Cognitive resources needed to understand complex information | Optimize — don't overwhelm with dense text |
| **Extraneous** | Resources spent on irrelevant info from poor design | Minimize — text-only dumps become extraneous load |
| **Germane** | Resources allocated to problem-solving and metacognition | Promote — cognitive forcing designs shift load from extraneous to germane |

## References
- See [references/cognitive-decline-evidence-base.md](references/cognitive-decline-evidence-base.md) for the full study, Bloom's Taxonomy survey results, and supporting cognitive-forcing research.