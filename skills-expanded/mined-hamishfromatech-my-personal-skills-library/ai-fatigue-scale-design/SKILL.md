---
name: ai-fatigue-scale-design
description: A validated, multi-dimensional AI Fatigue Scale and conceptual framework for measuring the strain users experience from sustained human-AI interaction. Covers the five dimensions (cognitive, emotional, social, operational, and information overload), the 15-item measurement instrument, antecedents (system, user, and contextual factors), consequences (reduced AI engagement, discontinuance), and design countermeasures. Use when measuring user fatigue in AI products, designing engagement retention, building wellbeing dashboards for AI tools, or diagnosing why users abandon AI features. NOT for acute developer overload from managing too many agents (use ai-brain-fry-defense) or decision-density fatigue from agentic coding (use coding-agent-decision-fatigue-mitigation).
---

# AI Fatigue Scale Design

## Overview
AI fatigue is a measurable, multi-dimensional form of strain arising from sustained interaction with AI systems. A validated 15-item scale now exists to measure it, moving the conversation from anecdote to instrument — enabling product teams to detect fatigue before it drives disengagement or abandonment.

## When to Use
- Measuring user fatigue in AI-powered products (chatbots, copilots, recommendation systems, AI writing tools)
- Designing engagement and retention strategies that account for fatigue as a churn driver
- Building wellbeing / cognitive-load dashboards for AI tools
- Diagnosing why users reduce or abandon AI feature usage over time
- Researching the human side of human-AI interaction at scale
- NOT for acute developer overload from concurrent agent management (use `ai-brain-fry-defense`)
- NOT for the decision-density crisis in agentic coding (use `coding-agent-decision-fatigue-mitigation`)
- NOT for review fatigue specifically (use `ai-review-fatigue-mitigation`)

## Core Process / Workflow

### 1. Understand the five dimensions of AI fatigue

| Dimension | What it measures | Example item theme |
|---|---|---|
| **Cognitive** | Mental effort required to understand, interpret, and verify AI output | "I find it mentally exhausting to interpret AI responses" |
| **Emotional** | Affective strain from frustration, disappointment, or dependency on AI | "I feel frustrated when AI doesn't meet my expectations" |
| **Social** | Strain from AI-mediated interactions replacing or mediating human contact | "I feel isolated relying on AI instead of people" |
| **Operational** | Effort to manage, configure, maintain, and troubleshoot AI tools | "Keeping AI tools configured and working is a burden" |
| **Information overload** | Overwhelm from the volume of AI-generated content and outputs | "I'm overwhelmed by the amount of information AI provides" |

### 2. Identify the antecedents (what causes AI fatigue)

**System factors**
- Low output quality / unreliability / hallucinations
- Opaque reasoning (lack of explainability)
- High interaction frequency required
- Poor error recovery

**User factors**
- Low AI literacy / expertise
- High expectations unmet by reality
- Personality traits (e.g., low tolerance for ambiguity)

**Contextual factors**
- High-stakes tasks (healthcare, finance) amplifying verification burden
- Mandatory AI use (organizational mandate removes user agency)
- Time pressure

### 3. Track the consequences

| Consequence | Signal | Metric |
|---|---|---|
| Reduced engagement | Lower session frequency, shorter sessions | Session count, session duration trend |
| Discontinuance | Users stop using AI features entirely | Feature abandonment rate |
| Critical engagement | Users use AI but with increasing skepticism/friction | Negative sentiment trend, support tickets |
| Knowledge avoidance | Users avoid AI-generated information | "Prefer human source" selection rate |

### 4. Apply the design countermeasures

**Reduce cognitive load**
- Progressive disclosure of AI reasoning (show confidence, not full chain-of-thought)
- Pre-validated output summaries before detailed breakdowns
- Consistent output schemas to reduce interpretation effort

**Reduce emotional strain**
- Calibrated expectations (don't oversell capabilities)
- Graceful failure with honest "I'm not sure" responses
- User agency preservation (always offer a non-AI path)

**Reduce operational burden**
- Auto-configuration and sensible defaults
- Self-healing tool states (recover from errors without user intervention)
- Reduce required touchpoints per task

**Reduce information overload**
- Output curation (rank, summarize, filter — don't dump)
- Asynchronous delivery options (batch results rather than stream)
- "Just-in-time" information instead of "just-in-case"

**Reduce social strain**
- Position AI as augmentation, not replacement, of human interaction
- Preserve human-to-human channels alongside AI-mediated ones
- Design for "AI + human" collaboration, not "AI instead of human"

### 5. Build a fatigue monitoring loop

```
Measure (15-item scale, quarterly)
    ↓
Segment by dimension (which fatigue type is highest?)
    ↓
Map to antecedents (system, user, or context?)
    ↓
Apply targeted countermeasure
    ↓
Re-measure (track delta)
    ↓
Correlate with engagement/retention metrics
```

### 6. The privacy-first measurement approach

The scale measures self-reported strain — no biometric data, no behavioral surveillance required. This aligns with A-Tech's privacy-first values: fatigue detection via direct user feedback, not inferred from keystroke dynamics or scroll patterns.

| Approach | Privacy cost | A-Tech alignment |
|---|---|---|
| Self-report scale (quarterly pulse) | None — voluntary disclosure | ☑ Privacy-first |
| Behavioral inference (typing cadence, dwell time) | High — continuous surveillance | ✗ Not aligned |
| Biometric (EEG, GSR, eye tracking) | Very high — bodily data | ✗ Not aligned |

## A-Tech Applications

| Product | Application |
|---|---|
| **A-Coder** | Measure developer AI fatigue quarterly; track whether agentic features increase or decrease fatigue vs. autocomplete; design cooldown prompts when fatigue scores rise |
| **Be Practical** | Module on "Recognizing AI Fatigue" — teach learners to self-diagnose and apply countermeasures; frame fatigue management as a core AI-era skill |
| **Builder's Club** | Community fatigue pulse survey; open-source the scale as an MCP tool so any AI product can measure fatigue; publish privacy-first fatigue monitoring as a competitive differentiator |

## References
- See [references/ai-fatigue-scale-evidence.md](references/ai-fatigue-scale-evidence.md) for the study details, scale items, and cross-references to adjacent skills.