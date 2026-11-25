---
name: dual-pathway-habit-regulation-model
description: Apply the dual regulatory model of habitual behavior — RSC-projecting ACC neurons govern decision-making strategy (goal-directed vs habitual), while CS-projecting LOFC neurons govern execution level (frequency/duration). Use when designing habit formation or habit-breaking interventions, distinguishing strategy shift from execution maintenance, building products that need to change WHAT users decide vs HOW OFTEN they act, or translating neurocircuit mechanisms into behavioral design. NOT for general habit tips, atomic habits frameworks, or habit formation advice without the dual-pathway neural distinction.
---

# Dual-Pathway Habit Regulation Model

## The Central Discovery

Habitual behavior has **two dissociable mechanistic dimensions**, controlled by plasticity in distinct cortical pathways:

1. **Decision-making strategy** (goal-directed ↔ habitual): controlled by synaptic potentiation in **RSC-projecting ACC neurons** (anterior cingulate cortex → retrosplenial cortex)
2. **Execution level** (frequency/duration of behavior): controlled by synaptic potentiation in **CS-projecting LOFC neurons** (lateral orbitofrontal cortex → central striatum)

These are **orthogonal**. You can shift someone from goal-directed to habitual strategy WITHOUT changing how often they act. You can change how often they act WITHOUT shifting their strategy. Each requires targeting a different circuit.

## Why This Matters for Design

Most habit-formation advice conflates the two. "Make it a habit" can mean:
- (a) Shift the *decision* from effortful deliberation to automatic (strategy axis — ACC→RSC)
- (b) Increase the *frequency/duration* of the behavior (execution axis — LOFC→CS)

These are different interventions with different mechanisms. Getting them backwards explains why many habit products fail: they target frequency when the user's bottleneck is strategic deliberation, or target automation when the user's bottleneck is consistency.

## The Mechanism (Asaoka et al., Nature Communications 2026)

### Experimental Paradigm
Mice trained sequentially:
1. **CRF** (continuous reinforcement) — every lever press rewarded (3 days)
2. **VR** (variable ratio) — reward after average 10, then 20 presses (6 days) → goal-directed behavior established
3. **VI** (variable interval) — reward on first press after average 60s (4 days) → transition to habitual behavior

### The Two Indices
- **Devaluation index**: positive = goal-directed (reduces pressing when reward devalued); ~zero = habitual (insensitive to reward value)
- **Execution index**: normalized change in lever press rate from final VR session to final VI session

### Key Finding
Devaluation index and execution index are **uncorrelated**. Mice could become fully habitual (devaluation ≈ 0) while increasing, maintaining, or decreasing their press rate. The strategy transition and execution level are governed by dissociable mechanisms.

## The Two Circuits

### Circuit 1: ACC → RSC (Strategy)
- **Region**: anterior cingulate cortex, layer 5 pyramidal neurons projecting to retrosplenial cortex
- **Plasticity**: VR training induces LTP (increased AMPA/NMDA ratio)
- **Function**: maintains goal-directed strategy; encodes action-outcome association
- **Transition to habit**: DEPOTENTIATION of ACC→RSC synapses (AMPA/NMDA returns to baseline under VI training)
- **Causal evidence**:
  - Chemogenetic inhibition of ACC → converts goal-directed to habitual (devaluation index drops to ~0)
  - Chemogenetic activation of ACC → reverts habitual back to goal-directed
  - Optogenetic LTP erasure (CFL-SN CALI) in RSC-projecting ACC neurons → facilitates habit formation without affecting acquisition
- **In vivo Ca²⁺ imaging**: RSC-projecting ACC neurons show burst-like activity during rewarded nose pokes; reward-excited cells increase during VR, decrease after VI switching; reward-inhibited cells show the inverse
- **Does NOT correlate with execution index**

### Circuit 2: LOFC → CS (Execution)
- **Region**: lateral orbitofrontal cortex, layer 5 pyramidal neurons projecting to central striatum
- **Plasticity**: VR training induces LTP; PERSISTS in high-execution mice under VI, absent in low-execution mice
- **Function**: maintains execution level during habit formation; encodes cue-outcome associations (Pavlovian) that facilitate operant execution via Pavlovian-instrumental transfer
- **Causal evidence**:
  - Optogenetic LTP erasure (CFL-SN CALI) in CS-projecting LOFC neurons after VI sessions → reduces execution index; lowers proportion of high-execution mice
  - Chemogenetic activation of CS-projecting LOFC → slight increase in lever pressing frequency
  - Does NOT affect devaluation index (no strategy shift)
- **In vivo Ca²⁺ imaging**: CS-projecting LOFC neurons show reward-related activity with slow decay; reward cells' amplitude progressively increases across training stages; at VI stage, reward-related response positively correlates with execution index
- **Does NOT correlate with devaluation index**

## The Dual Regulatory Model

```
                  ┌─────────────────────────┐
                  │  RSC-projecting ACC L5    │
                  │  (strategy circuit)      │
                  │                          │
                  │  LTP = goal-directed     │
                  │  Depotentiation = habit  │
                  └────────────┬─────────────┘
                               │
                               │ orthogonally
                               │ represented
                               ▼
                  ┌─────────────────────────┐
                  │  CS-projecting LOFC L5   │
                  │  (execution circuit)     │
                  │                          │
                  │  LTP persists = high     │
                  │  LTP absent = low        │
                  │  execution               │
                  └───────────────────────────┘
```

## Application: Behavioral Design Implications

### When the bottleneck is STRATEGY (too much deliberation)
**Target the ACC→RSC axis.** The user is goal-directed — they deliberate every time. You want them to shift to automatic.
- **Design lever: reduce action-outcome contingency visibility.** VI schedules work because the link between effort and reward becomes opaque. In product terms: variable reward timing, decoupled effort-reward feedback, contextual cues that trigger behavior independent of immediate outcome.
- **Design lever: context stability.** Habits form when the context is stable (Bouton 2021). Same environment, same cues, same time → the ACC→RSC depotentiates faster.
- **Avoid: making the user deliberate more.** Gamification that highlights effort-reward links (points per action) keeps the user goal-directed. This is why streak counters can backfire for habit formation — they keep the strategy goal-directed.

### When the bottleneck is EXECUTION (behavior is automatic but infrequent)
**Target the LOFC→CS axis.** The user is already habitual (doesn't deliberate) but doesn't do it often enough.
- **Design lever: Pavlovian-instrumental transfer.** LOFC→CS encodes cue-outcome associations. Strengthen the cue-reward link (Pavlovian) to drive the instrumental behavior. Example: a notification that reliably predicts a reward (not contingent on the action) increases execution frequency.
- **Design lever: reward-related activation.** CS-projecting LOFC neurons' reward response correlates with execution. Make the reward salient and temporally linked to the behavior.
- **Avoid: changing the action-outcome contingency.** That targets the ACC→RSC axis, not LOFC→CS. The user is already habitual; shifting the contingency would push them back to goal-directed, which is the opposite of what you want.

### When both need to change
Sequence the intervention:
1. **First**: establish the context and reduce contingency visibility → shift to habitual (ACC→RSC depotentiation)
2. **Then**: strengthen cue-reward Pavlovian associations → increase execution (LOFC→CS LTP persistence)
Doing them in reverse order fails: increasing execution of a goal-directed behavior makes the deliberation more frequent, not less.

## Implications for Habit-Breaking

For maladaptive habits (compulsivity, addiction):
- **To reduce execution without restoring deliberation**: target LOFC→CS (reduce cue-reward Pavlovian strength). This lowers frequency but leaves the behavior habitual — it will still be automatic when it occurs.
- **To restore goal-directed control**: target ACC→RSC (reactivate LTP). This makes the behavior deliberative again — the person can now choose not to do it. Chemogenetic ACC activation reverted habitual to goal-directed in the study.
- **Pathology link**: hyperactivity in OFC-striatum pathway is implicated in compulsive disorders (OCD, addiction). The LOFC→CS execution circuit is the candidate for "abnormally strong habit" severity.

## Key Distinctions for Practitioners

| Question | ACC→RSC (strategy) | LOFC→CS (execution) |
|---|---|---|
| What does it control? | Goal-directed vs habitual decision | Frequency/duration of the behavior |
| What plasticity? | LTP induced by VR, depotentiated by VI | LTP induced by VR, persists or doesn't under VI |
| What does LTP erasure do? | Facilitates habit formation (strategy shift) | Reduces execution level (frequency) |
| What does activation do? | Restores goal-directed control | Slightly increases pressing frequency |
| Correlates with? | Devaluation index (insensitivity to reward value) | Execution index (change in press rate) |
| Encodes? | Action-outcome association | Cue-outcome (Pavlovian) → drives instrumental via PIT |

## A-Tech Value Alignment

| Value | Alignment |
|---|---|
| Open-source AI | The underlying research is published in Nature Communications under CC BY; the dual-pathway model is transparent and auditable |
| Data privacy | The model is mechanism-based, not surveillance-based — it explains behavior through circuit plasticity, not through tracking individual neural data |
| Financial freedom | Correctly diagnosing the bottleneck (strategy vs execution) avoids wasted intervention spend; habit products that target the wrong axis fail silently |
| Practical implementation | The design levers (context stability, contingency opacity, Pavlovian cue-reward) are implementable in software without neural measurement |

## What This Skill Is NOT

- NOT a general "atomic habits" framework (those conflate strategy and execution)
- NOT a habit-tracking recommendation (tracking can keep behavior goal-directed, opposing automation)
- NOT a claim that you can measure ACC→RSC or LOFC→CS in humans (the mechanism is from mice; the design levers are behavioral translations)
- NOT a recommendation to always push users to habitual (goal-directed control is sometimes better — e.g., for high-stakes decisions)

## References

See `references/dual-pathway-evidence-base.md` for the full experimental details, statistical results, Ca²⁺ imaging findings, optogenetic/chemogenetic manipulations, and the pathological implications for compulsive disorders.