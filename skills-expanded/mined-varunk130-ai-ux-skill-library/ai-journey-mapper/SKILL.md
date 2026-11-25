---
name: ai-journey-mapper
description: 'Map human-AI interaction journeys - trust arcs, capability discovery paths, autonomy progression, and AI-specific touchpoints. Use when: AI user journey, human-AI interaction mapping, trust arc mapping, AI capability discovery, AI adoption journey, AI experience map.'
---

# AI Journey Mapper

Map the unique journeys users take when interacting with AI products - from first encounter through mastery. Unlike traditional journey mapping, AI journeys include trust arcs, capability discovery curves, mental model evolution, and the shifting balance of human-AI control. The PATHWAY framework captures what traditional journey maps miss.

## Core Principle

Traditional journey maps track what users DO. AI journey maps must also track what users BELIEVE - because the gap between what users believe the AI can do and what it actually can do is where every AI UX problem lives.

---

## The PATHWAY Framework

| Letter | Dimension | What to Map |
|---|---|---|
| **P** | Perception Evolution | How the user's mental model of the AI changes over time |
| **A** | Autonomy Gradient | How the balance of human vs. AI control shifts across the journey |
| **T** | Trust Arc | How trust rises, falls, and recovers through the experience |
| **H** | Help Moments | Where the user needs assistance understanding the AI (not just the product) |
| **W** | Wow Moments | Where the AI exceeds expectations and creates advocacy |
| **A** | Anxiety Points | Where the user feels uncertain, vulnerable, or out of control |
| **Y** | Yield Decisions | Where the user must decide: trust the AI, override it, or disengage |

---

## AI Journey Map Structure

An AI journey map extends the traditional CJM with AI-specific rows:

### Standard Rows (from traditional journey mapping)

| Row | Content |
|---|---|
| **Phases** | 4-6 stages of the AI adoption journey |
| **Actions** | What the user does at each phase |
| **Touchpoints** | Where interactions occur |
| **Pain Points** | Friction and frustration sources |
| **Opportunities** | Design improvement possibilities |

### AI-Specific Rows (unique to this skill)

| Row | Content | Why It Matters |
|---|---|---|
| **Mental Model** | What the user believes the AI can do at this phase | Misaligned mental models cause 80% of AI UX failures |
| **Trust Level** | High / Medium / Low / Broken - with the event that caused the change | Trust is the #1 predictor of AI adoption and retention |
| **Autonomy Balance** | Who is in control: User-led → Collaborative → AI-led | The shift from "I use the AI" to "the AI works for me" is the key transition |
| **Capability Awareness** | Percentage of AI capabilities the user has discovered | Most users discover < 30% of capabilities in the first month |
| **Verification Behavior** | How much the user checks AI outputs | Decreasing verification = growing trust (or dangerous complacency) |
| **Error Exposure** | What AI failures the user has encountered | Each error type reshapes the mental model differently |

---

## The Five Phases of AI Adoption

Every AI product journey follows these phases (though timing varies):

| Phase | User State | Mental Model | Typical Duration |
|---|---|---|---|
| **1. Encounter** | Curious but skeptical | "What can this thing do?" | First session |
| **2. Experiment** | Testing boundaries, low stakes | "Let me see if it's actually useful" | Days 1-7 |
| **3. Integrate** | Building the AI into real workflows | "This saves me time on specific tasks" | Weeks 2-6 |
| **4. Depend** | Relying on AI for critical tasks | "I can't imagine working without this" | Months 2-6 |
| **5. Advocate** | Recommending to others, pushing boundaries | "Everyone needs to use this" | Month 6+ |

### Phase-Specific Design Priorities

| Phase | Top Priority | Biggest Risk | Key Metric |
|---|---|---|---|
| Encounter | Impressive first interaction | Blank-screen paralysis | Time to first "wow" (target: < 60 seconds) |
| Experiment | Low-stakes exploration, quick wins | Single bad output kills momentum | Tasks completed in first 7 days |
| Integrate | Workflow fit, reliability | AI disrupts existing habits without clear benefit | Weekly active usage |
| Depend | Consistency, trustworthiness, advanced features | Catastrophic failure when user has removed manual fallbacks | NPS, daily active usage |
| Advocate | Shareability, team features, customization | User hits capability ceiling and stops growing | Referral rate, team adoption |

---

## Trust Arc Mapping

Trust is not linear. Map it as a curve with specific events that cause rises and falls.

### Trust Arc Template

```
Trust Level
High ─────────────────●──────────────●────────────────
                     ╱              ╲              ╱
Medium ────────●────╱────────────────╲────────────╱───
              ╱                      ╲          ╱
Low ────●────╱────────────────────────╲────●───╱──────
       ╱                              ╲  ╱
Zero ──●──────────────────────────────────────────────
       ↑     ↑        ↑               ↑    ↑    ↑
     First  First   First          First  Error  Trust
     use    success  "wow"         error  recovery rebuilt
```

### Trust Events to Map

| Event Type | Effect on Trust | How to Capture |
|---|---|---|
| **First successful output** | Sharp rise | Session recordings, time-to-first-action |
| **Capability surprise** | Moderate rise ("oh, it can do THAT?") | Feature discovery analytics |
| **Confident hallucination** | Sharp drop | Error reports, regeneration rate |
| **Graceful error recovery** | Moderate rise (even above pre-error levels) | Post-error engagement metrics |
| **Inconsistent results** | Gradual erosion | Repeated query analysis |
| **Productivity breakthrough** | Sustained high trust | Workflow integration metrics |
| **Public embarrassment** (shared AI error) | Severe, lasting drop | Support tickets, churn correlation |

---

## Capability Discovery Mapping

Track how users discover what the AI can do over time.

### The Discovery Curve

| Discovery Method | User Effort | Discovery Rate | Design Implication |
|---|---|---|---|
| **Core feature use** | Zero (it's the product) | 100% by Day 1 | Make the core unmissable |
| **Contextual suggestion** | Low (AI suggests it at the right moment) | 40-60% by Day 30 | Build smart suggestion triggers |
| **Exploration** | Medium (user tries something new) | 20-30% by Day 30 | Provide a "What else can you do?" surface |
| **Peer recommendation** | Variable (depends on community) | 10-20% by Day 30 | Build sharing and team features |
| **Documentation** | High (user reads help docs) | 5-10% by Day 30 | Don't rely on docs for discovery - supplement only |

### The Capability Discovery Map

For each AI capability, document:

| Capability | Discovery Phase | Discovery Trigger | % Users Who Discover It | Importance to Retention |
|---|---|---|---|---|
| Example: "Summarize long documents" | Experiment | Starter prompt suggestion | 72% | High |
| Example: "Generate charts from data" | Integrate | Contextual: user uploads CSV | 28% | Medium |
| Example: "Custom system prompts" | Depend | Power user exploration | 8% | Very High (for those who find it) |

---

## Autonomy Transition Mapping

Map how control shifts between user and AI across the journey:

| Phase | Control Model | User Role | AI Role | Design Pattern |
|---|---|---|---|---|
| Encounter | **User-led** | User decides everything | AI waits for instructions | Suggestion chips, guided prompts |
| Experiment | **User-led with AI assists** | User drives, AI offers help | AI suggests but doesn't act | "Would you like me to..." offers |
| Integrate | **Collaborative** | User and AI share control | AI handles routine, user handles judgment | Autonomy dial at Level 2-3 |
| Depend | **AI-led with user oversight** | User reviews and approves | AI proposes and executes with confirmation | Action previews, audit trails |
| Advocate | **Delegated** | User sets goals and boundaries | AI executes autonomously within bounds | Goal-setting interface, exception alerts |

---

## Running an AI Journey Mapping Workshop

### Workshop Agenda (Half-Day)

| Time | Activity | Output |
|---|---|---|
| 0:00-0:30 | Share user research: interviews, analytics, support tickets | Aligned understanding of current user experience |
| 0:30-1:15 | Map the standard journey rows (phases, actions, touchpoints, pain points) | Baseline journey map |
| 1:15-1:30 | Break | |
| 1:30-2:15 | Add AI-specific rows: mental model, trust level, autonomy balance | AI-enriched journey map |
| 2:15-2:45 | Plot the trust arc: identify trust events (rises and drops) | Trust arc overlay |
| 2:45-3:15 | Identify top 5 intervention points: where design can most improve the AI experience | Prioritized opportunity list |
| 3:15-3:30 | Assign owners and next steps | Action plan |

---

## Anti-Patterns

| Pattern | Why It Fails |
|---|---|
| Mapping the AI journey like a traditional software journey | Misses the trust arc, mental model evolution, and autonomy transitions that are unique to AI |
| Assuming trust is built once and stays | Trust is dynamic - a single hallucination at Month 6 can reset trust to Month 1 levels |
| Mapping only the happy path | AI journeys have more failure modes than traditional software. Map the error recovery paths explicitly |
| Treating all users as one persona | A technical user and a non-technical user have completely different AI adoption curves |
| Focusing only on the product journey | The AI journey extends beyond your product - how do users feel about AI in general? Prior AI experiences shape expectations |

---

## Quick Reference

| Task | Framework Element | Key Deliverable |
|---|---|---|
| Map an AI product's user journey | Full PATHWAY framework + AI-specific rows | AI journey map with trust arc and mental model evolution |
| Understand why users abandon AI products | Five Phases of AI Adoption | Phase-specific abandonment analysis |
| Improve AI feature discovery | Capability Discovery Map | Discovery rate by capability + trigger optimization plan |
| Design trust recovery after AI failure | Trust Arc Mapping + Trust Events | Trust recovery intervention design |
| Plan AI autonomy progression | Autonomy Transition Map | Phase-by-phase control model |

## Integration

Works with: `ai-onboarding-calibration` (onboarding as the first journey phase), `ai-trust-transparency` (trust events on the journey), `ai-agent-ux` (autonomy transitions), `ai-error-resilience` (error recovery as journey inflection points), `ai-feedback-loops` (feedback moments on the journey).
