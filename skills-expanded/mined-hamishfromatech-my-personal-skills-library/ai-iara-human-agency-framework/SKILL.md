---
name: ai-iara-human-agency-framework
description: Apply the AI-IARA framework to design AI systems that cultivate six essential human capacities before artificial conditions erode them. Covers Intentionality, Awareness, Resilience, Authenticity, and Adaptability as engineering specifications. Use when building AI products where human agency, psychological safety, and wellbeing are design requirements.
---

# AI-IARA Framework: Cultivating Human Agency

## Overview

Published in 2026 in the Journal of Positive Psychology, the AI-IARA framework identifies six interconnected human capacities essential for wellbeing under algorithmic conditions. Unlike frameworks that treat AI as a neutral tool, AI-IARA recognizes that AI systems actively shape human psychological states—and provides engineering specifications to ensure they expand rather than erode agency.

For A-Tech, this is a design philosophy, not just a compliance checklist. It turns the "pro-worker AI" debate into concrete product requirements.

## The Six Capacities

### 1. Intentionality
The capacity to act with purpose and direction rather than being nudged by algorithmic defaults.

**Engineering Specifications:**
- Make default settings visible and explainable, not hidden in terms of service
- Allow users to articulate their goals and have the AI align with them, not replace them
- Provide "intention checks" before autonomous actions: "You asked for X—here's what I'm about to do"

**A-Tech Application:**
- A-Coder: Before generating code, agent asks: "You said you want a caching layer. I can implement in-memory, Redis, or CDN. Which aligns with your intent?"
- Be Practical: Playbook quizzes confirm reader's actual goal before recommending solutions

### 2. Awareness (Mindfulness)
The capacity to maintain metacognitive monitoring of one's own thinking while using AI.

**Engineering Specifications:**
- Design pauses and reflection moments into AI workflows
- Surface when the AI is making assumptions vs. working from explicit user input
- Provide cognitive load indicators so users know when they're offloading too much thinking

**A-Tech Application:**
- A-Coder: After 3 consecutive AI-generated commits, prompt: "You've accepted all suggestions. Want to review the architecture yourself before continuing?"
- Be Practical: Chapter checkpoints require readers to articulate what they learned before advancing

### 3. Resilience
The capacity to recover from AI errors, setbacks, or cognitive overload without disengagement.

**Engineering Specifications:**
- Design graceful degradation: when AI fails, the user still has productive paths forward
- Provide "cognitive slack" — easy recovery from over-reliance on AI assistance
- Build error recovery as learning moments, not just bug fixes

**A-Tech Application:**
- A-Coder: When agent produces broken code, show the reasoning trace and ask user to identify the error—turning failure into skill-building
- Builder's Club: Community support structure for builders whose AI projects fail; "scar story" culture

### 4. Authenticity
The capacity to maintain genuine self-expression and values rather than converging on AI-generated homogenization.

**Engineering Specifications:**
- Provide style/personality controls that preserve user voice rather than smoothing it out
- Detect and flag when user outputs are becoming more "AI-average" over time
- Support idiosyncratic approaches, not just optimal ones

**A-Tech Application:**
- A-Coder: "Voice preservation" mode that learns user's coding style and resists standardizing to common patterns
- Be Practical: Encourage readers to adapt playbooks to their specific context rather than copying exactly

### 5. Relatedness (the missing I-A-R-A connection)
The original acronym is I-A-R-A (Intentionality, Awareness, Resilience, Authenticity) but the framework also emphasizes:
- **Adaptability:** The capacity to learn and evolve with AI rather than being displaced by it
- **Relatedness:** SDT's third need—genuine connection and belonging in human-AI systems

**Engineering Specifications:**
- Create space for human-to-human interaction alongside human-AI interaction
- Design AI as a connector between people, not just a replacement for them
- Support community learning and shared problem-solving

**A-Tech Application:**
- Builder's Club: AI-assisted collaboration tools that surface complementary skills between members
- Be Practical: Peer review and discussion features rather than solo consumption

### 6. Adaptability
The capacity to learn new competencies as AI capabilities evolve.

**Engineering Specifications:**
- Scaffold learning rather than eliminating it
- Gradually reduce assistance as user competence grows
- Surface "what you learned" summaries after AI-assisted tasks

**A-Tech Application:**
- A-Coder: "Learning mode" where AI explains why it made each suggestion, not just what it suggested
- Be Practical: Skill-building progression that intentionally phases out playbook dependency

## The Engineering Translation

The AI-IARA framework is notable because it translates psychological science directly into engineering specifications:

| Psychological Capacity | Design Requirement | Anti-Pattern |
|------------------------|-------------------|--------------|
| Intentionality | Goal-articulation interfaces | Hidden defaults that optimize for engagement |
| Awareness | Metacognitive pause prompts | Continuous flow that prevents reflection |
| Resilience | Graceful degradation paths | All-or-nothing dependency on AI functioning |
| Authenticity | Voice preservation controls | Output standardization to "best practice" |
| Relatedness | Human-to-human connection features | AI as sole interface, replacing community |
| Adaptability | Scaffolded learning with fade-out | Permanent AI crutch, never building user skill |

## A-Tech Values Alignment

| Value | AI-IARA Alignment |
|-------|-------------------|
| **Open-Source AI** | Inspectable systems allow users to verify intentionality and authenticity controls |
| **Data Privacy** | Awareness of what data shapes AI outputs; user control over context preserves autonomy |
| **Financial Freedom** | Resilience and adaptability prevent user displacement; tools augment rather than replace human value |
| **Practical Implementation** | Each capacity has concrete UI patterns and measurable outcomes |

## Implementation Checklist

- [ ] Add goal-articulation step before major AI-assisted actions
- [ ] Design reflection prompts at natural cognitive breakpoints
- [ ] Build graceful degradation for all AI-dependent features
- [ ] Implement voice/personality preservation controls
- [ ] Create human-connection features alongside AI automation
- [ ] Add learning-mode toggle that explains AI reasoning
- [ ] Measure user agency perception with standardized instruments

## Metrics

| Metric | Target | Measurement Approach |
|--------|--------|---------------------|
| Intentionality score | >4.0/5.0 | Self-report: "I feel my goals drive the AI, not the other way around" |
| Awareness index | >3.5/5.0 | Behavioral: frequency of context review before accepting output |
| Resilience recovery | <30 seconds | Time to productive path after AI error |
| Authenticity preservation | >80% similarity | User style fingerprint consistency over time |
| Relatedness engagement | >40% of sessions | Include human-to-human interaction |
| Adaptability gain | +20% skill score | Pre/post competence assessment on AI-assisted tasks |

## Related Skills
- `self-determination-theory-developer-motivation` — Intrinsic motivation through autonomy, competence, relatedness
- `context-maxxing-cognitive-agency` — User control over informational environment
- `digital-nudging-ethical-persuasion` — Ethical choice architecture preserving agency

## Date Researched
2026-05-29 | Daily Research Process | A-Tech Research Division
