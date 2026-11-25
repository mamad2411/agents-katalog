---
name: neuroadaptive-attention-engineering
description: Design adaptive interfaces that respond to real-time attention and cognitive state using behavioral signals, EEG, eye-tracking, and predictive processing principles. Use when building high-stakes developer tools, learning platforms, or safety-critical interfaces where cognitive overload leads to errors. NOT for general productivity apps without physiological grounding.
---

# Neuroadaptive Attention Engineering

## Overview
Combine neurophysiological sensing (EEG, eye-tracking, pupillometry) with behavioral proxies to build interfaces that adapt to the user's real-time attentional state. By 2026, research demonstrates sustained attention monitoring predicts task errors 5–12 seconds before they occur — opening the door to preemptive cognitive load reduction and flow-state preservation.

## When to Use
- Building safety-critical systems where cognitive fatigue causes real harm (aviation, medical, infrastructure)
- Designing developer tools for long-duration focused work (4+ hour sessions)
- Creating adaptive learning platforms that calibrate difficulty to real-time capacity
- Developing accessibility tools for ADHD, autism, or traumatic brain injury populations
- NOT for: casual entertainment, general marketing websites, or contexts without informed consent for sensing

## Core Process / Workflow

### 1. Attention State Taxonomy
Define the states your system can detect and respond to:

| State | Physiology | Behavioral Proxies | Design Response |
|---|---|---|---|
| **Focused** | Low theta/beta ratio, stable gaze, steady pupil | Long fixation, consistent typing cadence | Maintain current mode, minimize interruption |
| **Divided** | Elevated beta/gamma, rapid saccades, dilating pupil | Frequent tab-switching, error spikes | Consolidate interface, reduce options |
| **Fatigued** | Rising alpha/theta, slow blink rate, microsleeps | Increasing correction rate, pauses | Force break, lower task complexity |
| **Frustrated** | Elevated skin conductance, erratic gaze, constricted pupil | Aggressive keystrokes, rapid scrolling | Offer assistance, simplify immediately |
| **Bored** | Flat EEG, wandering gaze, stable pupil | Low interaction rate, long inactivity | Increase challenge, add novelty |
| **Flow** | Alpha suppression, smooth pursuit, moderate dilation | Long uninterrupted sequences, time distortion | Preserve at all costs, shield interruptions |

### 2. Sensing Architecture
Layer sensors from invasive to non-invasive based on context and consent:

#### Tier 1: Behavioral Proxies (Default, Zero-Extra-Hardware)
- **Keystroke dynamics** — Inter-key interval variance predicts fatigue
- **Mouse/eye movement patterns** — Saccade speed, fixation duration
- **Error rate trajectory** — Degrading accuracy signals overload
- **Scroll velocity variance** — Increased jitter maps to divided attention
- **Application switch frequency** — Attention residue quantifier

#### Tier 2: Peripheral Physiology (Wearables, Consented)
- **Smartwatch HR/HRV** — Heart rate variability correlates with cognitive load
- **Galvanic skin response** — Skin conductance maps to arousal/frustration
- **Facial EMG (via camera)** — Micro-expressions reveal emotional valence
- **Posture sensors** — Slouching correlates with disengagement

#### Tier 3: Central Physiology (Specialized Equipment, Highly Controlled)
- **EEG (dry-electrode headsets)** — Direct neural activity measurement; alpha suppression marks engagement
- **Eye-tracking (desktop/mobile)** — Pupillometry, blink dynamics, smooth pursuit
- **fNIRS** — Cortical blood flow imaging for workload estimation

### 3. Predictive Processing Interface Loop
Design interfaces that minimize prediction error (surprise) while maintaining optimal challenge:

```
User State Estimate → Predict Next State → Generate Interface → Measure Surprise → Update Model
```

- **Generative user model** — Predict what the user expects to see next
- **Precision weighting** — Trust recent signals more in volatile states; trust baseline more in stable states
- **Surprise budget** — Allocate a fixed "surprise quota" per minute; expensive transitions consume budget
- **Active inference** — Interface suggests actions that resolve uncertainty (e.g., "Did you mean X?")

Implementation example:
```python
class PredictiveInterface:
    def __init__(self):
        self.user_model = GenerativeUserModel()
        self.surprise_budget = 10  # arbitrary units per minute

    def render(self, context, sensor_data):
        state = self.estimate_state(sensor_data)
        predicted_next = self.user_model.predict(context, state)
        candidate_interfaces = self.generate_candidates(context)
        # Select candidate minimizing prediction error within budget
        best = min(candidate_interfaces,
                   key=lambda c: prediction_error(c, predicted_next))
        if surprise_cost(best) > self.surprise_budget.remaining():
            best = fallback_safe_interface()
        return best
```

### 4. Adaptive Intervention Patterns
Trigger interventions based on detected state transitions:

| Transition | Warning Window | Intervention |
|---|---|---|
| Focus → Divided | 5–8 sec | Dim non-primary panels; audio cue for refocus |
| Focus → Fatigued | 10–15 sec | Mandatory micro-break (20–20–20 rule); task simplification |
| Focus → Frustrated | 3–5 sec | Offer "help" button; reduce visible options by 50% |
| Bored → Focus | Immediate | Inject novelty, increase challenge, introduce micro-goal |
| Flow → Any | 15–30 sec | Aggressive interruption shielding; defer all non-critical notifications |

### 5. Ethical and Consent Architecture
Neuroadaptive sensing requires rigorous ethical boundaries:

- **Explicit tiered consent** — Separate consent for behavioral, peripheral, and central sensing
- **On-device processing** — All raw sensor data processed locally; only state labels leave device
- **User override** — Users can declare their state manually, overriding sensor inference
- **No cover manipulation** — System never covertly modifies behavior; all adaptations disclosed
- **Data minimization** — Raw signals deleted after state inference; no long-term storage without opt-in
- **Right to non-sensing** — Plain mode available where all sensing disabled

### 6. DevEx Application: The Flow Guardian
Apply neuroadaptive engineering to developer tools:

- **Pre-flow detection** — When keyboard dynamics suggest rising focus, silence notifications automatically
- **Flow preservation** — Once flow detected (stable cadence + low error rate), block all but emergency interrupts
- **Break optimization** — Detect emerging fatigue before subjective awareness; suggest break when recovery maximizes afternoon productivity
- **Context recovery** — After interruption, restore working memory state via visual breadcrumbs

### 7. Measurement Framework

| Metric | Instrument | Target |
|---|---|---|
| State classification accuracy | Offline labeled dataset | >85% for 4-class (focus/divided/fatigued/flow) |
| Prediction error reduction | A/B vs. non-adaptive | >20% lower task error rate |
| Intervention acceptance rate | User click-through | >60% for suggested breaks |
| False positive rate | User-reported incorrect state | <10% |
| Flow duration extension | Time-tracking, self-report | >25% longer flow episodes |
| Ethical compliance audit | External review | Zero covert manipulation findings |

## References
- See [references/eeg-eye-tracking-integration.md](references/eeg-eye-tracking-integration.md) for 2026 multimodal sensing research and hardware recommendations.
- See [references/predictive-processing-ux-deep-dive.md](references/predictive-processing-ux-deep-dive.md) for extended theoretical treatment of Friston's free-energy principle applied to interface design.
- See `predictive-processing-interface-design` for foundational predictive processing UX patterns.
- See `flow-state-engineering-for-coding-tools` for flow-specific developer experience design.
- See `neurodiversity-ai-inclusive-design` for population-specific neuroadaptive accommodations.
