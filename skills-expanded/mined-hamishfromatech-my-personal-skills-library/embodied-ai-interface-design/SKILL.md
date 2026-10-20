---
name: embodied-ai-interface-design
description: Design interfaces that bridge digital cognition with physical presence, leveraging Hamish's lived experience with Functional Neurological Disorder (FND) to create adaptive systems that respond to body state, environmental context, and embodied needs. Use when building AI products for accessibility, neurodivergent populations, remote presence, or any interface where the body is not an afterthought. NOT for standard screen-based UI without embodied dimension.
---

# Embodied AI Interface Design

## Overview

Most AI interfaces treat the body as an input device — fingers on keyboards, eyes on screens, voices in microphones. Embodied AI Interface Design inverts this: the body is the primary interface, and digital systems adapt to its state. This skill draws directly on A-Tech's founder experience with Functional Neurological Disorder (FND) — seizures, hand contracture, walking limits — to create a design framework where physical limitation becomes design insight.

By 2026, embodied AI spans: voice-first agents for hands-free operation, adaptive systems that throttle cognitive load during fatigue episodes, environmental AI that modulates lighting and sound for sensory needs, and digital twins that preserve presence when the body cannot show up.

## When to Use

- Building AI tools for users with neurological, motor, or sensory differences
- Designing voice-first, ambient, or zero-touch interfaces
- Creating adaptive systems that respond to fatigue, pain, or capacity fluctuation
- Developing remote-presence or digital-twin capabilities for human limitation
- Prototyping environmental AI that modulates physical spaces
- NOT for: standard GUI design without embodied dimension, transactional apps where physical state is irrelevant

## Core Process / Workflow

### 1. The Embodiment Spectrum

Map where your product sits on the spectrum of physical integration:

| Level | Body Relationship | Example | Risk |
|---|---|---|---|
| **Disembodied** | Body ignored; screen-only | Traditional SaaS dashboard | Exclusion, fatigue |
| **Accommodated** | Body recognized; static adaptations | Alt-text, screen readers | Partial, one-size |
| **Adaptive** | Body monitored; system responds | Voice dictation, eye tracking | Privacy, paternalism |
| **Embodied** | Body and system co-create | Environmental AI, haptic feedback | Dependency, complexity |
| **Transcendent** | Body limitation overcome by AI | Digital twin presence, predictive assistance | Identity displacement |

**A-Tech Design Principle**: Build at the Adaptive–Embodied level. Never pretend the body does not exist. Never replace the human with simulation.

### 2. Four Design Patterns from Lived Experience

#### Pattern A: Capacity-Aware Throttling
Design systems that detect and respond to fluctuating capacity without shame.

- **FND application**: During seizure prodrome, interface automatically simplifies to one-option voice commands; post-seizure, gradually restores complexity as cognitive tests pass
- **General application**: After-hours coding sessions trigger A-Coder's "gentle mode" — fewer suggestions, longer pauses, comprehension checkpoints
- **Mechanism**: Behavioral proxy detection (error rate spikes, pause duration, command retry patterns) triggers tiered simplification

```yaml
# capacity-tiers.yml
- tier: full
  trigger: baseline performance
  features: [autocomplete, suggestions, multi-panel, realtime-collab]
- tier: reduced
  trigger: error_rate > 2x_baseline OR pause > 30s
  features: [basic-autocomplete, no-suggestions, single-panel]
- tier: minimal
  trigger: error_rate > 5x_baseline OR repeated_failed_commands > 3
  features: [voice-only, one-option-at-a-time, human-escalation]
```

#### Pattern B: Presence Preservation
When the body cannot be present, AI preserves relational continuity.

- **FND application**: During seizure or hospitalization, Open-Oracle digital twin responds to community messages with calibrated tone and known positions; marks responses as "Hamish's twin — he will review on recovery"
- **General application**: Builder's Club members can delegate community participation to their configured agent during illness, travel, or focus periods
- **Guardrail**: Always label delegated presence. Never simulate emotional states the human is not actually experiencing.

#### Pattern C: Environmental Co-Regulation
AI modulates the physical environment to support cognitive and bodily state.

- **FND application**: Smart home integration detects seizure patterns and dims lights, reduces ambient sound, locks doors safely, notifies trusted contacts
- **General application**: A-Coder workspace agent adjusts monitor brightness, notification cadence, and ambient audio based on detected focus depth and fatigue signals
- **Mechanism**: Bidirectional API between AI agent and IoT/environmental controllers with user-defined safety bounds

#### Pattern D: Agency-Preserving Assistance
Help without taking over. The system offers but never imposes.

- **FND application**: Hand contracture day — AI offers voice-to-text as a gentle suggestion, not automatic override; user can decline and type slowly if that maintains sense of autonomy
- **General application**: Be Practical learning platform suggests shorter modules when engagement patterns show fatigue, but always allows user to continue
- **Mechanism**: Explicit consent at each assistance tier; opt-out preserves full functionality at higher friction

### 3. The Accessibility–Privacy Tension

Embodied systems require body data. This creates a fundamental tension:

| Data Type | Accessibility Gain | Privacy Risk | Mitigation |
|---|---|---|---|
| Keystroke dynamics | Fatigue detection | Keystroke biometric deanonymization | Local-only processing; no cloud upload |
| Voice patterns | Emotion/stress inference | Voiceprint identification | On-device inference; aggregate only |
| Eye tracking | Attention state | Gaze pattern inference of intent | Ephemeral data; no storage |
| Environmental sensors | Seizure/autonomic detection | Location and behavior tracking | User-controlled activation; open-source stack |

**A-Tech Policy**: All embodied inference runs locally. No biometric data leaves the device. The open-source stack enables community audit of inference logic.

### 4. Implementation Roadmap

**Phase 1: Behavioral Proxy Detection (Weeks 1–4)**
Use existing inputs (keystroke timing, scroll velocity, command retry rate) to infer capacity state. No new hardware required.

**Phase 2: Optional Sensor Integration (Weeks 5–12)**
Add wearable or environmental sensors for users who opt in. Smartwatch HRV, desktop microphone (local-only voice analysis), ambient light sensors.

**Phase 3: Adaptive Response Layer (Weeks 13–20)**
Build the tiered response system: automatic simplification, explicit assistance offers, environmental co-regulation hooks.

**Phase 4: Digital Presence Configuration (Weeks 21–28)**
Enable users to configure their delegated presence — what the agent can say, how it labels itself, when it hands back to human.

**Phase 5: Community Validation (Ongoing)**
Test with neurodivergent, disabled, and chronically ill users. Iterate on agency-preserving patterns.

## References

- See [references/fnd-design-insights.md](references/fnd-design-insights.md) for detailed lived-experience design notes and community feedback.
- See [references/environmental-ai-protocols.md](references/environmental-ai-protocols.md) for IoT integration specifications and safety bounds.
- See [references/capacity-detection-algorithms.md](references/capacity-detection-algorithms.md) for local-only behavioral proxy detection methods and accuracy benchmarks.
