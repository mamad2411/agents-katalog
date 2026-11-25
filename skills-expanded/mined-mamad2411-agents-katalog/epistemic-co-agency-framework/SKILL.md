---
name: epistemic-co-agency-framework
description: Design AI-assisted knowledge work that preserves and strengthens human epistemic agency through structured co-agency. Based on 2026 research on epistemic co-agency and learning with machines. Use when building educational AI tools, research assistants, collaborative knowledge platforms, or any product where human understanding must deepen alongside AI capability. NOT for pure automation where human judgment is intentionally removed.
---

# Epistemic Co-Agency Framework

## Overview

The dominant framing of human-AI interaction — augmentation vs. replacement — is incomplete. A 2026 systematic review in Computers and Education: Artificial Intelligence proposes a third paradigm: **epistemic co-agency**, where humans and machines construct knowledge together through structured collaboration rather than one-sided delegation. The framework distinguishes three modes of interaction (Epistemic Augmentation, Replacement, and Co-Agency) and provides design principles for sustaining human cognitive agency in AI-assisted knowledge work.

This skill operationalizes the co-agency framework for A-Tech products, ensuring that A-Coder, Be Practical, and Builder's Club tools make users more capable of independent knowledge construction, not merely more efficient at consuming AI outputs.

## When to Use

- Building educational AI tools where the goal is deep learning, not just answer retrieval
- Designing research assistants for knowledge workers who must retain independent reasoning
- Creating collaborative knowledge platforms where human and AI contributions are interdependent
- Evaluating whether an AI product is making users more knowledgeable or merely more dependent
- Developing governance frameworks for AI-assisted decision-making in professional contexts

NOT for:
- Pure automation systems where human judgment is intentionally removed (e.g., background image resizing)
- Time-critical emergency systems where deliberation is not possible
- Low-stakes information retrieval where speed is the sole metric

## The Three Modes of Human-AI Epistemic Interaction

| Mode | Human Role | AI Role | Risk | Opportunity |
|------|-----------|---------|------|-------------|
| **Epistemic Augmentation (EA)** | Instrumental access and provisional scaffolding | Tool that extends human cognitive reach | Dependency without deepening | Amplified capability with maintained agency |
| **Epistemic Replacement (ER)** | Minimal or ceremonial oversight | Primary knower and decision-maker | Cognitive atrophy; skill loss | Efficiency in well-defined domains |
| **Epistemic Co-Agency (ECA)** | Active co-constructor of knowledge | Partner with explicit epistemic contribution | Design complexity; slower initial speed | Synergistic knowledge deeper than either alone |

**The prevailing commercial paradigm (EA → ER drift):** Most AI tools begin as augmentation but drift toward replacement as users habituate to fluency. Co-agency is the intentional design stance that prevents this drift.

## Core Principles of Epistemic Co-Agency

### Principle 1: Symmetric Epistemic Contribution
Both human and AI make explicit, contestable contributions to the knowledge being constructed. The AI does not present conclusions; it presents structured reasoning that the human can modify, reject, or build upon.

**Implementation:**
- AI outputs include explicit reasoning traces, not just conclusions
- Humans can edit AI reasoning steps and see downstream effects
- Both human and AI contributions are labeled and versioned

### Principle 2: Generative Tension
Co-agency requires moments of productive disagreement where the human and AI hold different views. These tensions are not bugs to resolve but features that deepen understanding.

**Implementation:**
- AI presents alternative interpretations, not just consensus views
- System flags moments where human input diverges from AI prediction
- Disagreement is preserved in the knowledge record, not smoothed over

### Principle 3: Epistemic Transparency
The user can trace how any piece of knowledge was constructed, who (human or AI) contributed what, and what assumptions underpin the conclusion.

**Implementation:**
- Full provenance tracking for all knowledge artifacts
- Assumption logs that users can inspect and challenge
- Epistemic confidence levels for every claim (not just binary true/false)

### Principle 4: Agency-Building Over Efficiency
The primary design metric is whether the user can perform the task independently after the AI interaction, not whether the task was completed faster with AI.

**Implementation:**
- Post-interaction reflection prompts that require the user to articulate what they learned
- Graduated autonomy: AI scaffolding reduces as user competence increases
- Independence checks: periodic tasks completed without AI assistance

## The Five Design Patterns

### Pattern 1: The Socratic Dialogue Interface
Instead of question → answer, the interaction follows a structured inquiry:

1. User poses a problem
2. AI asks clarifying questions (not provides answers)
3. User refines their understanding through response
4. AI offers multiple reasoning paths, not a single solution
5. User selects, modifies, or rejects each path
6. Joint conclusion is constructed through iterative refinement

**A-Tech Application:**
- A-Coder: Architecture decision dialogues where the AI asks "What constraints matter most?" before proposing solutions
- Be Practical: Playbook chapters that pose Socratic questions before revealing frameworks

### Pattern 2: The Epistemic Ledger
A running record of every human-AI knowledge construction session:

| Session | Human Contribution | AI Contribution | Constructed Knowledge | Independence Check |
|---------|-------------------|-----------------|------------------------|-------------------|
| 2026-06-08 | Identified customer segment | Suggested 3 interview protocols | Validated interview guide | Can run interviews without AI prompt |

**Purpose:** Makes epistemic dependency visible before it becomes irreversible.

### Pattern 3: Graduated Scaffolding
AI support is explicitly tiered and reduces as user competence grows:

| Stage | AI Role | Human Role | Transition Trigger |
|-------|---------|-----------|-------------------|
| Novice | High scaffolding: explains concepts, suggests next steps | Follows guidance, asks clarifying questions | Completes 3 tasks without help |
| Competent | Medium scaffolding: flags risks, offers alternatives | Makes own decisions, uses AI as sounding board | Teaches another person the skill |
| Expert | Low scaffolding: provides edge-case data, novel connections | Leads the interaction, AI amplifies reach | Publishes independent work |

**Anti-pattern:** The AI never reduces scaffolding, creating permanent dependency.

### Pattern 4: The Disagreement Matrix
For any significant recommendation, present a structured matrix of human-AI disagreement:

| Dimension | AI Position | Human Position | Evidence | Resolution |
|-----------|-------------|----------------|----------|------------|
| Priority | Speed first | Maintainability first | Past refactoring costs | Human decides; AI notes tradeoff |
| Risk tolerance | Accept 5% failure rate | Accept 1% failure rate | Business impact analysis | Human decides; AI adjusts design |
| Architecture | Microservices | Modular monolith | Team size and expertise | Human decides; AI implements chosen path |

**Purpose:** Makes epistemic disagreement a first-class design element, not a problem to eliminate.

### Pattern 5: The Independence Pulse
Periodic checks where the user must complete a related task without AI assistance:

- Weekly: 15-minute unassisted coding challenge
- Monthly: Write a design document from scratch
- Quarterly: Teach a peer the skill you've been practicing with AI

**Purpose:** Prevents the gradual drift from augmentation to replacement by requiring demonstrated independence.

## A-Tech Product Applications

### A-Coder (IDE)
- **Socratic Architecture Mode:** Before generating code, the agent asks structured questions about constraints, priorities, and risk tolerance
- **Epistemic Ledger Dashboard:** Per-project view showing what the developer has learned vs. what they have delegated
- **Graduated Autonomy Settings:** User sets their desired scaffolding level; system reduces it as competence metrics improve
- **Independence Mode:** Scheduled sessions (user-defined frequency) where AI assistance is disabled; flow-state metrics measured to ensure productivity is maintained

### Be Practical (Playbooks)
- **Co-Agency Chapter Design:** Each chapter includes human-AI co-construction exercises, not just AI-generated summaries
- **Epistemic Reflection Prompts:** After each major concept, readers answer: "Explain this in your own words. What would you do differently?"
- **Peer Teaching Requirement:** Readers must teach one chapter concept to another person before unlocking advanced modules
- **Assumption Challenge:** Every framework includes an "assumptions under stress" section where readers identify when the framework breaks

### Builder's Club
- **Open-Source Epistemic Co-Agency Toolkit:** Community-maintained libraries for provenance tracking, assumption logging, and independence checking
- **Co-Agency Design Reviews:** Peer review of AI-assisted projects includes assessment of whether the human deepened their knowledge
- **Independence Badges:** Members earn recognition for demonstrating unassisted capability in domains where they previously used AI heavily
- **Knowledge Construction Events:** Community workshops where human-AI pairs solve problems and document their co-construction process

## Measurement Framework

| Metric | Definition | Target |
|--------|-----------|--------|
| Epistemic Transparency Score | % of AI-generated outputs with full reasoning trace and assumption log | ≥ 90% |
| Generative Tension Rate | % of sessions where human and AI held different views that were preserved | ≥ 30% |
| Graduation Velocity | Time to advance from novice → competent → expert scaffolding level | ≤ 8 weeks per stage |
| Independence Pulse Pass Rate | % of unassisted tasks completed successfully | ≥ 75% |
| Post-Interaction Articulation | % of users who can explain AI-assisted output in their own words | ≥ 80% |
| Epistemic Ledger Trend | Direction of independence capability over 90 days | Increasing |

## Ethical Boundaries

- Never design for permanent dependency as a retention strategy
- Never obscure AI contribution to knowledge construction
- Never penalize users for choosing unassisted workflows
- Never use co-agency data (reasoning traces, assumption logs) for surveillance or performance evaluation without explicit consent
- Always enable full data export of epistemic ledger for user portability

## Relationship to Existing Skills

- `scaffolded-cognitive-friction` — Co-agency is the positive complement: structured friction that builds capability rather than merely defending against surrender
- `cognitive-surrender-defense` — Co-agency prevents surrender by design, not just detects it
- `ai-iara-human-agency-framework` — The six human capacities (Intentionality, Awareness, Resilience, Authenticity, Relatedness, Adaptability) are the target outcomes of co-agency design
- `generation-then-comprehension` — Co-agency operationalizes the comprehension half of the generation-then-comprehension loop

## References
- See [references/epistemic-co-agency-research.md](references/epistemic-co-agency-research.md) for the full Computers and Education: Artificial Intelligence paper extraction, the three-mode taxonomy, and the six design principles.
- See [references/learning-with-machines-synthesis.md](references/learning-with-machines-synthesis.md) for the broader 2026 research landscape on human-AI knowledge construction, including the Sage Journals commentary on strengthening human epistemic agency.

## Sources
- Goel, et al. — "Learning with machines: Toward a theory of epistemic co-agency" (Computers and Education: Artificial Intelligence, June 2026, 100573)
- Sage Journals — "Strengthening Human Epistemic Agency in the Symbiotic Learning Era" (2026): AI prompt protocols for enhancing human-AI knowledge co-construction
- arXiv:2603.21735 — "Defending Epistemic Sovereignty via Scaffolded AI Friction" (March 2026): Foundational HCI research on cognitive agency surrender
- Springer — "How AI is rewiring the human brain: the generational transformation of cognition and knowing" (2026): Epistemic environments for cognitive sovereignty
