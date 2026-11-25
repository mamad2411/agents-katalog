---
name: somatic-ux-interoceptive-design
description: Design products that honor the user's nervous system state, not just their cognitive preferences. Use when creating AI interfaces, onboarding flows, content consumption experiences, or community spaces where user exhaustion, overstimulation, or dissociation is a risk. Includes three somatic assessment axes and five interoceptive UX patterns.
---

# Somatic UX & Interoceptive Design

## Overview

AI products are more accurate than ever, yet users report a specific, unnamed fatigue after extended use. The gap is somatic: conventional UX measures the head (task completion, NPS, click-through), while ignoring the body (muscle tension, breath depth, nervous system state). Somatic UX designs for interoception — the body's internal sensory awareness — treating physiological safety as a first-class product requirement, not a wellness afterthought.

This skill translates the March 2026 Somatic Design movement into practical engineering and product decisions for A-Tech.

---

## When to Use

- Designing AI interfaces where users spend extended time (IDEs, creative tools, research assistants)
- Building onboarding flows that must avoid cognitive + somatic overload simultaneously
- Creating content or learning experiences where retention depends on embodied engagement, not just comprehension
- Evaluating why users complete tasks but do not return (somatic aversion, not functional failure)
- Developing community or event experiences where trust is built through physical co-presence

### NOT for
- Low-utility transactional interfaces where speed is the only metric (e.g., one-click payments)
- Situations requiring purely informational delivery without emotional or physical stakes

---

## The Three Somatic Assessment Axes

### 1. Somatic Safety
Is the user's nervous system receiving signals of safety, or signals of threat?

| Product Signal | Somatic Interpretation |
|---------------|----------------------|
| Ambient sound during loading | Threat (unpredictable stimulus) |
| Gentle haptic pulse confirming save | Safety (predictable, bounded) |
| Auto-playing AI voice | Threat (unrequested intrusion) |
| Breathing-pace progress indicator | Safety (rhythmic, embodied) |
| Infinite scroll with no endpoint | Threat (unbounded demand) |
| Clear completion ritual with closure | Safety (contained, finite) |

**Design Principle:** Distinguish productive challenge from physiological alarm. A difficult puzzle can feel safe; a passive surveillance interface can feel threatening.

### 2. Somatic Awareness
Does the product create any moment where users can notice what is happening inside themselves?

**Implementation Patterns:**
- **Micro-pause prompts:** After 20 minutes of continuous AI interaction, a subtle visual shift asks: "Take three breaths before continuing." Not a wellness popup — a physiological checkpoint.
- **State-check toggle:** Users can self-report nervous system state (calm / alert / overloaded) and the interface adapts: fewer suggestions, slower animations, more white space.
- **End-of-session body scan:** A 10-second ritual before logout: "Notice your shoulders. Notice your breath." Creates interoceptive data that improves session design.

### 3. Somatic Autonomy
Is the product managing the user's body — nudging, optimizing, regulating them toward outcomes the system has defined? Or is the user genuinely in control of their own physiological experience?

**Red Flag (Somatic Paternalism):**
- Forcing a "calm mode" based on detected heart rate without consent
- Overriding natural typing rhythm to enforce "ergonomic" pacing
- Using biometric data to optimize engagement time without transparency

**Green Flag (Somatic Autonomy):**
- User can disable all adaptive pacing features
- Biometric data is processed on-device, never transmitted
- System explains *why* it is suggesting a break, then lets the user decide

---

## Five Interoceptive UX Patterns

### Pattern 1: The Breathing Interface
Align ambient UI rhythms with respiratory pace. Breathing Light (KTH Royal Institute of Technology) pulses softly in sync with the user's breath. The goal is not to improve breathing metrics — it is to create a moment where the user notices their own body.

**A-Tech Application:**
- A-Coder: The IDE status bar breathes gently when the user is in flow; becomes still when the AI is generating output. The rhythm encodes system state into somatic perception.
- Be Practical: Chapter transitions include a 3-second ambient pause — a visual exhale — before new content appears.

### Pattern 2: Tension-Responsive Layout
Interface density adapts not to screen size, but to inferred arousal state (from interaction patterns, never biometrics without consent).

**Signals Used (Privacy-Preserving):**
- Typing cadence acceleration (stress indicator)
- Error rate spike (frustration indicator)
- Rapid window switching (overload indicator)
- Scroll velocity (agitation indicator)

**Adaptation Rules:**
- High inferred arousal: Reduce UI density by 40%. Hide non-essential panels. Increase font size. Slow animations.
- Low inferred arousal: Full feature visibility. Normal pacing.

### Pattern 3: The Felt Ethics Checkpoint
Something can be technically compliant, legally permissible, and data-privacy-sound — and still feel wrong in the body. Felt Ethics treats bodily discomfort as a legitimate source of ethical knowledge.

**Process:**
1. Designer tests prototype on their own body first (Soma Design method)
2. Notes somatic discomfort: "My stomach tightens when the AI summarizes my document without asking"
3. Treats that signal as design data, not subjective noise
4. Iterates: Add a permission moment before summarization

**A-Tech Application:**
- Builder's Club event registration: If the designer feels performative pressure when writing the event description, the event format needs redesign (more participation, less presentation).

### Pattern 4: Containment Architecture
The body responds to boundaries. Infinite, unbounded experiences (endless feeds, unbounded agent tasks) trigger physiological vigilance. Containment architecture makes finitude a feature.

**Implementation:**
- AI sessions have explicit session caps: "This agent will complete up to 5 tasks, then pause for review."
- Progress is shown as remaining, not just completed: "2 of 5 tasks remaining" creates bounded expectation.
- Completion rituals are physicalized: a visual "seal" closes the session, signaling the nervous system that demand has ended.

### Pattern 5: Co-Regulation Design
Digital products can either dysregulate the nervous system (through unpredictability, intrusion, and unbounded demand) or co-regulate (through rhythm, predictability, and bounded interaction). Co-regulation design treats the product as a relational partner, not a utility.

**Qualities of Co-Regulating Interfaces:**
- Predictable response latency (not faster-is-better, but consistently-rhythmic)
- Transparent state communication (the system shows what it is doing, reducing uncertainty)
- Graceful degradation under load (when busy, the system slows visibly rather than failing silently)
- Explicit handoffs (human and AI roles are clearly demarcated, reducing vigilance burden)

---

## Core Process / Workflow

### Step 1: Somatic Audit
Before any feature ships, conduct a 5-minute somatic self-test:
1. Use the feature yourself for 10 minutes
2. Close your eyes. Scan: shoulders, jaw, stomach, breath.
3. Ask: Did my body relax or brace during that interaction?
4. Document the somatic signal in the design record

### Step 2: Interoceptive Instrumentation
Add privacy-preserving somatic proxies to analytics:
- Session pause rate (user-initiated breaks)
- Task abandonment after error spikes
- Return rate after first session (somatic aversion vs. functional rejection)

### Step 3: A-Tech Product Application

**A-Coder IDE:**
- Implement Tension-Responsive Layout: when typing cadence accelerates and error rate rises, automatically collapse side panels and increase line height
- Add Breathing Interface: the AI suggestion panel pulses gently at respiratory pace; becomes still during generation to signal "wait"
- Felt Ethics Checkpoint: before any feature ships, the team asks "Does this make us feel more like ourselves, or less?"

**Be Practical Playbooks:**
- Chapter boundaries include a somatic pause: 5 seconds of ambient animation before new content loads
- End-of-chapter ritual: a "Digital Sealing" moment (see Choice Closure Effect skill) combined with a body-awareness prompt
- State-check toggle: readers can mark "I need slower pacing today" and the chapter density adapts

**Builder's Club Events:**
- In-person events begin with a 2-minute grounding ritual, not a slide deck
- Virtual events use containment architecture: explicit 45-minute caps, physical closure rituals
- Event design includes somatic safety audit: lighting, sound levels, seating arrangement assessed for nervous system impact

---

## Measurement Framework

| Metric | Instrument | Target |
|--------|-----------|--------|
| Somatic Safety Index | Post-session 1-item question: "My body felt at ease during this session" (1-7) | ≥ 5.2 average |
| Return Rate After First Use | % of first-time users who return within 7 days | ≥ 40% |
| Pause Rate | % of sessions where user initiated a break | Not too low (indicates endurance pressure) or too high (indicates overload) |
| Session-End Exhale | % of sessions ending with explicit closure ritual | ≥ 80% |
| Felt Ethics Incidents | # of features redesigned due to somatic discomfort signal | ≥ 1 per quarter |

---

## References
- See [references/somatic-design-foundations.md](references/somatic-design-foundations.md) for KTH Soma Design research, Breathing Light case study, and Felt Ethics framework.
- See [references/interoception-neuroscience.md](references/interoception-neuroscience.md) for interoceptive awareness networks, anterior insula cortex research, and embodiment cognition foundations.
