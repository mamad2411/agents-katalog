---
name: ai-feedback-loops
description: 'Design feedback mechanisms that help AI systems learn from users - thumbs up/down, preference ranking, corrections, and human-in-the-loop escalation. Use when: RLHF UX, user feedback for AI, thumbs up down design, AI correction flow, human in the loop, feedback signal design, AI improvement loops.'
---

# AI Feedback Loops

Design feedback mechanisms that simultaneously improve the AI model AND improve the user's experience of giving feedback. The SIGNAL framework ensures feedback is low-friction, high-quality, and genuinely acted upon.

## Core Principle

Feedback is a **transaction.** Users invest effort (reporting an error, rating an output, explaining what's wrong). If they never see a return on that investment, they stop giving feedback. Design feedback loops that close - where users can see that their input made a difference.

---

## The SIGNAL Framework

| Letter | Principle | Design Question |
|---|---|---|
| **S** | Surface the Moment | Is feedback offered at the exact moment the user has an opinion? |
| **I** | Incentivize Honestly | Does the feedback design encourage genuine assessment, not just positive ratings? |
| **G** | Graduate the Effort | Can users give 1-second feedback OR 1-minute feedback, depending on their willingness? |
| **N** | Narrate the Impact | Can users see how their feedback improved the system? |
| **A** | Aggregate Intelligently | Is individual feedback combined into actionable patterns, not just counted? |
| **L** | Loop the Learning | Does the improved AI behavior visibly reflect the feedback it received? |

---

## The Feedback Pyramid

Design feedback collection in layers - most users will only reach the first layer, and that's fine.

| Layer | Effort | Signal Quality | Collection Rate | Mechanism |
|---|---|---|---|---|
| **L1: Implicit** | Zero effort | Low but high-volume | 100% of users | Usage patterns: regeneration rate, copy rate, session length, abandonment points |
| **L2: Binary** | 1 second | Medium | 15-30% of users | Thumbs up/down, helpful/not helpful |
| **L3: Categorical** | 5 seconds | Medium-High | 5-15% of users | "What was wrong?" dropdown: Inaccurate / Irrelevant / Incomplete / Offensive / Other |
| **L4: Textual** | 30 seconds | High | 2-5% of users | Free-text explanation of what was wrong and what would be better |
| **L5: Comparative** | 60 seconds | Very High | 1-3% of users | Side-by-side preference ranking: "Which response is better? A or B" |

**Design rule:** Never require L3+ feedback to complete a task. Deeper feedback should always be optional and offered after the primary interaction is complete.

---

## Implicit Feedback Signals

These require zero user effort but reveal powerful behavioral data:

| Signal | What It Indicates | Measurement |
|---|---|---|
| **Regeneration** | User rejected the output | Count of "regenerate" clicks per session |
| **Copy/use rate** | User accepted the output | Percentage of outputs that are copied, saved, or acted upon |
| **Edit distance** | User partially accepted | How much the user modified the AI output before using it |
| **Abandonment point** | AI failed to deliver value | Where in the flow users leave |
| **Scroll depth** | Output was too long or too short | How far users scroll before acting |
| **Time-to-next-action** | User needed time to evaluate | Long pause = uncertainty; immediate action = confidence |
| **Return frequency** | Product is valuable | How often users come back after first use |
| **Prompt refinement rate** | AI didn't understand the first time | How often users rephrase their query |

---

## Binary Feedback Design

The thumbs up/down is the most common AI feedback mechanism - and the most commonly botched.

### Thumbs Up/Down Best Practices

| Design Decision | Recommended Approach | Anti-Pattern |
|---|---|---|
| **Placement** | Below every AI response, right-aligned | Hidden in a menu, or only on some responses |
| **Initial state** | Both unselected (neutral) | Pre-selected thumbs up (biases positive) |
| **After thumbs down** | Immediately offer L3 dropdown: "What was wrong?" | Just log the downvote with no follow-up |
| **After thumbs up** | Optional: "What did you like?" (but don't insist) | Pop-up survey that interrupts the flow |
| **Visual feedback** | Button fills/highlights to confirm the vote registered | No visual change (user doesn't know if it worked) |
| **Changeability** | User can change their vote anytime | Vote is locked after submission |

### The Thumbs Down Expansion

When a user clicks thumbs down, expand into a lightweight triage:

```
What was wrong?
[ ] Inaccurate information      [ ] Not what I asked for
[ ] Too long / too short        [ ] Offensive or inappropriate
[ ] Outdated information        [ ] Other: ___________

[Optional] What would a better answer look like?
[_______________________________________________]

[Submit]  [Skip]
```

**Design rule:** "Skip" must be prominent. Forcing explanation creates resentment and low-quality data.

---

## Comparative Feedback (A/B Preference)

The highest-quality feedback signal: showing two AI outputs and asking which is better.

### When to Use Comparative Feedback

| Scenario | Comparative Feedback? | Why |
|---|---|---|
| General chat responses | Occasionally (10-20% of responses) | High-quality signal but adds friction |
| Creative generation (writing, images) | Yes - great fit | Subjective quality is hard to measure otherwise |
| Factual answers | Rarely | Usually one answer is objectively correct - binary feedback is sufficient |
| Code generation | Sometimes | "Which code is cleaner?" is valuable but requires expertise to judge |

### Comparison UI Patterns

| Pattern | How It Works | Best For |
|---|---|---|
| **Side-by-side** | Two responses shown simultaneously | Short responses (< 200 words each) |
| **Sequential with memory** | Show response A, then B, then ask preference | Longer responses where side-by-side is unwieldy |
| **Inline replacement** | "I have an alternative answer. Want to see it?" | Minimal disruption to the main flow |
| **Batch review** | End-of-session: "Help us improve - which answers were best today?" | Users willing to spend 2 minutes helping |

---

## Closing the Feedback Loop

Users who give feedback and never see impact stop giving feedback. Design visible closure.

### Feedback Impact Patterns

| Pattern | Implementation | Example |
|---|---|---|
| **Immediate acknowledgment** | Thank the user and explain what happens next | "Thanks - this helps us improve. We review flagged responses daily." |
| **Aggregate impact** | Show users how feedback from all users improved the system | "Users flagged 500 inaccurate responses last month. 340 were corrected." |
| **Personal impact** | Show the user how THEIR feedback changed behavior | "Based on your feedback, I now handle [specific task] differently." |
| **Release notes** | Tie model improvements to user feedback themes | "v2.3 improvements: Better code generation (informed by user feedback)" |

---

## Human-in-the-Loop Escalation

When AI confidence is low, feedback becomes real-time human decision-making.

### Escalation Triggers

| Trigger | Condition | Escalation Type |
|---|---|---|
| **Confidence below threshold** | Model confidence < 40% on a high-stakes output | Route to human reviewer before showing to user |
| **User reports critical error** | Thumbs down + "Inaccurate" + free-text with urgency signals | Flag for immediate human review |
| **Sensitive content detected** | Output touches medical, legal, financial, or safety topics | Add human verification badge or mandatory disclaimer |
| **Novel situation** | Query is outside the model's training distribution | Transparent handoff: "This is outside my expertise. Let me connect you with..." |
| **Repeated failures** | Same user gives thumbs down 3+ times in a session | Proactive human intervention: "Would you like to speak with a specialist?" |

---

## Anti-Patterns

| Pattern | Why It Fails |
|---|---|
| Feedback widget appears before the user has read the response | Users can't rate what they haven't consumed |
| Only collecting positive feedback (e.g., "Was this helpful? Yes / No" with only "Yes" prominent) | Survivorship bias - you only hear from satisfied users |
| Pop-up NPS survey mid-task | Interrupts flow; generates resentful 0-scores |
| "Thanks for your feedback!" with no evidence of action | Teaches users that feedback is performative, not functional |
| Requiring login to give feedback | Reduces feedback volume by 80%+ |
| Treating all thumbs-down equally | "Inaccurate" and "too long" require completely different responses |

---

## Quick Reference

| Task | Framework Element | Key Deliverable |
|---|---|---|
| Add feedback to AI product | Feedback Pyramid (L1-L5) | Layered feedback system design |
| Improve feedback quality | SIGNAL framework | Audit of current feedback loops + gaps |
| Design thumbs up/down experience | Binary Feedback Best Practices | Thumbs down expansion flow |
| Build RLHF training pipeline UX | Comparative Feedback patterns | A/B preference UI + sampling strategy |
| Close the feedback loop | Feedback Impact Patterns | User-visible impact communication plan |

## Integration

Works with: `ai-error-resilience` (error reports as feedback), `ai-trust-transparency` (feedback builds trust when acted upon), `ai-agent-ux` (rating agent actions), `ai-conversation-architect` (in-conversation feedback moments).
