---
name: adaptive-digital-nudging-llm-architecture
description: Applies a software architecture for adaptive digital nudging systems that uses LLM-driven reasoning to integrate multi-dimensional user modeling (cognitive mode, behavioral stage, attention capacity) with ethical compliance as structural architectural guardrails. Use when building adaptive nudging systems, designing LLM-powered behavioral intervention platforms, when you need ethical compliance enforced structurally rather than as implementation detail, or when creating digital nudging systems for regulated domains (EU AI Act, GDPR, DSA).
---

# Adaptive Digital Nudging Systems with LLM-Driven Reasoning

## Core Finding

A software architecture that uses behavioral theory through explicit architectural decisions, treating ethics and fairness as structural guardrails rather than implementation details. The architecture implements sequential processing layers with cross-cutting evaluation modules enforcing regulatory compliance. Validation with 13 software architects confirmed requirements satisfaction and domain transferability. An LLM-powered proof-of-concept in residential energy sustainability demonstrated feasibility through evaluation with 15 users, achieving high perceived intervention quality and measurable positive emotional impact.

Based on Santilli, Alipour & Tourchi Moghaddam (Syddansk Universitet, SAGAI-ICSA 2026). First architecture to integrate multi-dimensional user modeling with ethical compliance as architectural concerns for adaptive nudging.

## The Three Architectural Challenges

### i) Multi-Dimensional Runtime Adaptation
Effective nudging requires simultaneous consideration of:
- Cognitive mode (System 1 vs. System 2 thinking)
- Behavioral stage (pre-contemplation through maintenance, Transtheoretical Model)
- Attention capacity (high/medium/low cognitive load)
- Quality attributes (acceptability, effectiveness, fairness, transparency, etc.)

**Tension**: Tight coupling enables coordinated responses but creates brittleness; loose coupling improves maintainability but complicates adaptation.

### ii) Non-Negotiable Ethical Constraints as Architectural Guardrails
The EU AI Act, GDPR Article 22, and Digital Services Act impose hard constraints on automated decision-making systems. These are not optional features but mandatory architectural properties that must hold across all execution paths.

**Challenge**: How to enforce ethical boundaries structurally, such that no component can generate non-compliant nudges regardless of user state or system evolution?

### iii) Quality Attribute Conflicts Requiring Explicit Prioritization
- Transparency increases trust but may trigger reactance
- Personalization improves effectiveness but raises fairness concerns
- Simplification aids low-attention users but limits information for analytical thinkers

These conflicts demand architectural tactics with documented rationale and trade-offs.

## The Architecture

### Three Core Processing Layers + Two Cross-Cutting Modules

```
┌─────────────────────────────────────────────────────────────────┐
│                     CROSS-CUTTING: EVALUATION                    │
│  Fairness Monitor │ Ethics Compliance │ Outcome Tracker          │
└─────────┬───────────────────┬───────────────────┬──────────────┘
          │                   │                   │
┌─────────▼───────────────────▼───────────────────▼──────────────┐
│  LAYER 3: NUDGE INTELLIGENCE                                     │
│  Strategy Optimizer │ Nudge Generator │ UI Adaptation            │
└─────────┬───────────────────┬───────────────────┬──────────────┘
          │                   │                   │
┌─────────▼───────────────────▼───────────────────▼──────────────┐
│  LAYER 2: USER MODELING                                          │
│  Cognitive Mode │ Behavioral Stage │ Attention Capacity        │
└─────────┬───────────────────┬───────────────────┬──────────────┘
          │                   │                   │
┌─────────▼───────────────────▼───────────────────▼──────────────┐
│  LAYER 1: DATA CAPTURE                                           │
│  Context Tracker │ Behavioral Collector                        │
└─────────────────────────────────────────────────────────────────┘
          │
┌─────────▼─────────────────────────────────────────────────────────┐
│                     CROSS-CUTTING: ADAPTATION                     │
│  Explainability │ Adaptive Dashboard │ User Feedback              │
└───────────────────────────────────────────────────────────────────┘
```

### Layer 1: Data Capture
- **Context Tracker**: device type, location, time-of-day from session timestamps
- **Behavioral Collector**: clicks, hesitation times, navigation patterns, facial emotions (via FaceAPI), energy consumption, usage hours

### Layer 2: User Modeling (LLM-Driven)
Three parallel components using LLM classifiers:
- **Cognitive Mode**: System 1 vs. System 2 (analyzes interaction velocity; high clicks + long hesitation = analytical)
- **Behavioral Stage**: Transtheoretical Model mapping (pre-contemplation → contemplation → preparation → action → maintenance)
- **Attention Capacity**: high/medium/low (from contextual factors; influences UI and message complexity)

### Layer 3: Nudge Intelligence
- **Strategy Optimizer**: LLM with user profile data, selects optimal intervention from 68-strategy taxonomy via constraint-satisfaction prompting
- **Nudge Generator**: LLM creates message content, enforcing regulatory constraints via Ethics and Fairness prompts
- **UI Adaptation**: LLM dynamically adjusts font size (12-20px), colors, chart type based on cognitive state

### Cross-Cutting: Evaluation Module
- **Fairness Monitor**: Injects "Bias Mitigation" system prompt into every LLM call; non-discrimination + vulnerable user protection
- **Ethics Compliance**: Enforces EU AI Act + GDPR constraints via mandatory LLM prompt guardrails
- **Outcome Tracker**: Records every intermediate step (raw signals → profiling → strategy → message) + emotional states

### Cross-Cutting: Adaptation Module
- **Explainability**: Generates natural language "Transparency Explanation" of decision logic
- **Adaptive Dashboard**: Interactive environment for monitoring/modifying appliance states
- **User Feedback**: "thumbs up/down" feedback informing future strategy optimization

## Four Key Architectural Decisions

### AD1: Sequential Pipeline vs. Event-Driven Architecture
- **Decision**: Three sequential layers with per-user session processing
- **Rationale**: Deterministic reasoning chains; User Modeling completes before Strategy Optimization; ensures causal consistency, reasoning transparency, provenance tracking
- **Trade-offs**: Gains = clear provenance, easier debugging, compliance auditability; Costs = no intra-user parallelization, increased latency

### AD2: Side-Mounted Evaluation vs. Embedded Validators
- **Decision**: Ethics Compliance as side-mounted module intercepting all Nudge Intelligence outputs
- **Rationale**: Separation of concerns — nudge generation focuses on effectiveness, ethics audits all outputs. Interceptor pattern ensures no nudge reaches users without validation.
- **Trade-offs**: Gains = consistent enforcement, evolvability, independent testability, regulatory evidence; Costs = additional latency, potential bottleneck

### AD3: LLM-Driven Reasoning vs. Rule-Based Classification
- **Decision**: User Modeling components use LLMs rather than rule-based systems
- **Rationale**: Behavioral constructs require contextual interpretation of multiple weak signals. LLMs handle ambiguous cases (e.g., high clicks but short duration).
- **Trade-offs**: Gains = robustness to edge cases, expressiveness, adaptability via prompt engineering; Costs = controlled non-determinism, explainability challenges, API latency (200-500ms), vendor dependency

### AD4: Backend-Driven UI Adaptation vs. Client-Side
- **Decision**: Backend generates structured "UI Context" payloads; frontend renders
- **Rationale**: Attention capacity and cognitive mode affect information processing. Backend determines what adaptations; frontend determines how to render.
- **Trade-offs**: Gains = personalization, reduced cognitive load, privacy protection; Costs = frontend complexity, consistency challenges

## Validation Results

### Architect Evaluation (N=13 Software Architects)
- Mean rating: **4.62/5** across all items (strong agreement)
- UI Adaptation: 4.85 (highest)
- Explainability: 4.38 (lowest — identified for improvement)
- 61.5% rated "Highly Transferable"; 38.5% "Transferable with modifications"
- Key qualitative insight: "I like that ethics is not inside the nudge generator. That's a recipe for unexpected behaviors. Having it as a separate point makes it testable and auditable." (P3)

### User Evaluation (N=15 Participants)
**Perceived quality**:
- Nudge Quality: 4.73/5 (73.3% rated 5)
- Explanation Quality: 4.27/5 (40% rated 5, 46.7% rated 4)

**System classifications across 15 sessions**:
- Cognitive mode: 73.3% intuitive, 26.7% analytical
- Behavioral stage: 40% pre-contemplation, 26.7% contemplation, 33.3% action
- Attention capacity: 66.7% high, 20% medium, 13.3% low

**Emotional impact (facial expression analysis)**:
- Pre-nudge happiness: 0.000170 (predominantly neutral)
- Post-nudge happiness: 0.000500 (mean increase 0.000330)
- All participants showed positive changes → interventions well-received, not perceived as manipulative

## Literature Synthesis Foundation

The architecture is grounded in a systematic literature review (21 primary studies from 707 papers):
- **68 nudging strategies** spanning information provision, social influence, defaults/positioning, feedback, timing
- **11 quality attributes**: acceptability, awareness, effectiveness, fairness, healthfulness, helpfulness, intrusiveness, motivation, transparency, trustworthiness, user impact
- **3 user profiling dimensions**: cognitive mode, behavioral stage, attention capacity

## Practical Application Framework

### When to Use This Architecture
1. **Regulated nudging domains**: Healthcare, finance, energy — where EU AI Act, GDPR, DSA compliance is mandatory
2. **Multi-dimensional personalization**: When nudges must adapt to cognitive state, behavioral stage, AND attention simultaneously
3. **Ethical nudging systems**: When structural enforcement of ethical boundaries is required (not just post-hoc auditing)
4. **LLM-powered behavioral platforms**: When using LLMs for cognitive reasoning in adaptive systems

### Implementation Checklist
1. Define user profiling dimensions (cognitive mode, behavioral stage, attention)
2. Select nudging strategy taxonomy (68-strategy reference available)
3. Implement sequential pipeline: Data Capture → User Modeling → Nudge Intelligence
4. Add side-mounted Evaluation module with Fairness Monitor + Ethics Compliance
5. Implement Explainability for transparency reports
6. Use LLMs for cognitive reasoning with low temperature (0.3) for classification tasks
7. Inject bias mitigation and ethics prompts into every LLM call
8. Track all execution steps for audit trails

## Cross-References

- `behavioral-psychology-and-nudging/nudge-theory-choice-architecture` — foundational nudge theory
- `behavioral-psychology-and-nudging/llm-iterative-nudge-personalization` — LLM-personalized nudges
- `behavioral-psychology-and-nudging/llm-agent-nudge-sensitivity` — LLM nudge brittleness
- `ai-agents-and-workflows/mcp-stateless-core-2026` — stateless agentic architecture
- `cognitive-science-and-ux/cognitive-load` — cognitive load theory
- `cognitive-science-and-ux/curiosity-progression-marketing` — progressive disclosure
- `privacy-and-trust/consent-fatigue-progressive-permissioning` — consent design

## A-Tech Alignment

- **Open-source AI**: Open-source code available (github.com/tiziasan/Adaptive-Digital-Nudging-System); uses LLMs but architecture is LLM-agnostic
- **Data privacy**: Backend-driven UI adaptation protects interaction data; ethics compliance enforced structurally
- **Financial freedom**: Modular architecture enables solo founders to build adaptive nudging systems
- **Practical implementation**: Validated with 13 architects + 15 users; reproducible; transferable across domains

## Source

Santilli, T., Alipour, M., & Tourchi Moghaddam, M. (2026). Designing Adaptive Digital Nudging Systems with LLM-Driven Reasoning. Accepted at SAGAI-ICSA 2026. Syddansk Universitet, Odense, Denmark. Code: github.com/tiziasan/Adaptive-Digital-Nudging-System