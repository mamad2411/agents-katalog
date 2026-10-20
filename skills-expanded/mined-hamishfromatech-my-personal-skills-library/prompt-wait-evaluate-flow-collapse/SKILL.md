---
name: prompt-wait-evaluate-flow-collapse
description: Diagnose and defend against the prompt-wait-evaluate loop that collapses flow state in AI-assisted coding. Explains why the interaction pattern itself (not model quality) breaks Csikszentmihalyi's three flow preconditions, the "junk flow" counterfeit, the 39-percentage-point perception gap, and mode-separation protocols to restore deep work. Use when developers report feeling drained despite high output, when designing AI coding workflow policies, when building flow-protection tooling, or when explaining the productivity-experience paradox mechanism to engineering leadership.
---

# Prompt-Wait-Evaluate Flow Collapse

## Overview

The bottleneck in AI-assisted development is no longer authorship — it is the interaction loop itself. Each prompt-response cycle functions as a self-generated interruption that prevents flow state from forming, even when output volume and perceived productivity remain high. This skill provides the mechanism, the measurement framework, and the mode-separation protocol to restore genuine deep work alongside AI assistance.

## When to Use

- Engineers report feeling drained, fragmented, or "not in the zone" despite high commit velocity
- Designing AI coding workflow policies, focus-time protocols, or tool defaults
- Building flow-protection tooling (batch-prompt modes, do-not-disturb windows, focus metrics)
- Explaining the productivity-experience paradox mechanism to engineering leadership
- Diagnosing why a team's output looks great on dashboards but morale and craft satisfaction are eroding
- NOT for arguing against AI tool adoption — the goal is deliberate integration, not rejection

## Core Process / Workflow

### 1. Understand the mechanism — why the loop breaks flow

Csikszentmihalyi's three flow preconditions all collapse simultaneously in the prompt-wait-evaluate loop:

| Flow precondition | In traditional coding | In the prompt-wait-evaluate loop |
|---|---|---|
| **Clear goals at each moment** | You know what the next line should do | You describe high-level intent and wait for a surprise — no moment-to-moment clarity |
| **Immediate feedback** | Type-compile-see in a tight loop | A chunk of output arrives after seconds to minutes of waiting |
| **Challenge matches skill** | Difficulty scales with you as you iterate | Prompting is too easy; evaluating alien output is too hard — difficulty is in the wrong place |

The loop is insidious because it *looks like work* — you are in your IDE, typing, code is appearing — but internally you are context-switching, not building. Every prompt is a handoff; every response is an interruption; every evaluation is a cold start.

### 2. Quantify the hidden cost

- **Perception gap:** Developers predicted AI would make them 24% faster; they believed they were 20% faster after tasks; measured reality was 19% slower — a 39-percentage-point gap that compounds every sprint.
- **Interruption recovery:** Only 1 in 10 interruptions lets a programmer resume coding within a minute (Parnin & Rugaber, 10,000 sessions, 86 programmers). 93% of sessions involved significant navigation to rebuild mental context before editing resumed.
- **Self-generated interruptions:** ~44% of all interruptions are self-generated (Gloria Mark, UC Irvine). The prompt cycle is the most productive-looking form of self-interruption ever invented.
- **Flow state erosion:** In the Vella & Blincoe longitudinal study, the share of engineers rating flow state "worse" nearly tripled (7% → 20%) over six months — the hardest-hit DevEx dimension — while feedback loops improved.
- **Attention span decline:** Average time on a single screen before switching dropped from 2.5 minutes (2004) to 47 seconds.

### 3. Distinguish real flow from "junk flow"

Jeremy Howard (AI Engineer keynote) applied Csikszentmihalyi's own concept of *junk flow* (or *dark flow*) to AI prompting:

- **Real flow:** A genuine challenge stretches your skills and you grow from it. You are inside the problem.
- **Junk flow:** A superficial version that feels like flow at first, then becomes something you are addicted to rather than something that helps you grow. The dopamine is in the anticipation, not the payoff. Casinos manufacture this through an illusion of control.

Prompting an AI can feel like pulling a slot-machine lever — sometimes it nails it, sometimes it hands you nonsense — but you keep going, chasing the next good result. Recognising this distinction is the first defence.

### 4. Apply the mode-separation protocol

Do not keep a chat window open all day. Separate the day into two modes:

**AI-suitable tasks (where the loop is acceptable):**
- Boilerplate, configuration, scaffolding
- Exploratory prototyping
- Writing tests for well-understood behaviour
- Tasks where you would not reach flow anyway

**Deep-work tasks (close the assistant):**
- Designing an architecture
- Debugging a subtle issue
- Implementing anything requiring a complex mental model held in your head
- When you notice your thinking quality degrading with each re-prompt cycle

**Operational rules:**
1. Collect AI-suitable tasks into a dedicated block; handle them in a batch.
2. Keep the rest of the day available for uninterrupted deep work.
3. When prompting quality is getting worse with each cycle, stop, close the assistant, and start typing yourself — not because you are faster, but because the engagement is different.
4. Batch AI interactions rather than interleaving them with focused work.

### 5. Build the flow-protection toolkit

For A-Tech products, the defence is structural, not just behavioural:

- **Batch-prompt mode:** Collect multiple prompts; submit together; review in a single evaluation block rather than a stream of micro-interruptions.
- **Focus-window enforcement:** A configurable do-not-disturb that suppresses inline suggestions during flagged deep-work sessions.
- **Flow-state signal:** Track session-level metrics (longest uninterrupted editing stretch, context-switch count) as leading indicators — not commit volume.
- **Mode indicators:** Make the active mode (AI-assist vs. deep-work) visible to the developer and, optionally, to teammates.

### 6. Address the internal-goods / external-goods trade

Alasdair MacIntyre's distinction (via Nicholas Gruen) frames the deeper loss:

- **External goods** (productivity, output, status): AI is brilliant for these — they hold steady or climb.
- **Internal goods** (flow, mastery, the joy of the craft, the figuring-out): AI is potentially corrosive — it takes the part you loved and hands it to a machine, leaving supervision and accountability.

How a developer feels about AI correlates strongly with which goods they are chasing. Communicate this framing to teams so the trade is named, not hidden.

### 7. A-Tech application matrix

| Product | Application |
|---|---|
| **A-Coder** | Batch-prompt mode; focus-window enforcement; flow-state signal in the wellbeing dashboard; mode indicators that make AI-assist vs. deep-work visible; default to suppressed inline suggestions during flagged sessions |
| **Be Practical** | Mode-separation curriculum module; teach the junk-flow distinction and the 39-point perception gap as a core AI-literacy competency; provide the mode-separation protocol as a learnable workflow |
| **Builder's Club** | Open-source flow-protection MCP tool; community discussion of internal-vs-external goods; shared benchmarks for flow-state signals across AI coding tools |

## References

- See [references/flow-collapse-evidence-base.md](references/flow-collapse-evidence-base.md) for the full research base: Csikszentmihalyi's flow preconditions, the junk-flow concept, Parnin & Rugaber interruption-recovery study, Gloria Mark attention-span research, the 39-percentage-point perception gap, the Vella & Blincoe longitudinal findings, MacIntyre's internal/external goods, and cross-references to adjacent skills.