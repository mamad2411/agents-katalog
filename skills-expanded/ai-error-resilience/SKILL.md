---
name: ai-error-resilience
description: 'Design graceful failure experiences for AI products - hallucinations, uncertainty, wrong outputs, and edge cases. Use when: AI hallucination UX, error handling for AI, uncertainty design, graceful degradation, AI failure recovery, confidence thresholds, safe fallbacks.'
---

# AI Error Resilience

Design AI products that fail gracefully, communicate uncertainty honestly, and help users recover without losing trust. The RECOVER framework treats AI errors as a design material, not a bug to hide.

## Core Principle

Traditional software has bugs. AI has **probabilistic outputs on a spectrum of correctness.** You cannot design AI UX using binary error/success patterns. Instead, design for a continuum: right, mostly right, partially right, uncertain, wrong, and dangerously wrong.

---

## The RECOVER Framework

| Letter | Phase | Design Question |
|---|---|---|
| **R** | Recognize | Can the system detect when its output may be unreliable? |
| **E** | Express Uncertainty | Does the interface clearly communicate degrees of confidence to the user? |
| **C** | Contain Blast Radius | If the AI is wrong, what's the worst that can happen? How is damage limited? |
| **O** | Offer Alternatives | Does the user get a Plan B when Plan A might be wrong? |
| **V** | Verify Collaboratively | Can the user easily check, correct, or confirm the AI's output? |
| **E** | Evolve from Errors | Does the system learn from this error type to prevent future occurrences? |
| **R** | Restore Confidence | After a failure, how does the product rebuild the user's willingness to try again? |

---

## AI Error Taxonomy

Not all AI errors are created equal. Each type requires a different UX response.

| Error Type | Description | Severity | UX Response Pattern |
|---|---|---|---|
| **Confident hallucination** | AI invents facts and states them as truth | Critical | Citation requirement + verification prompt |
| **Stale knowledge** | AI references outdated information | High | Timestamp + "knowledge cutoff" indicator |
| **Context misread** | AI misinterprets the user's intent or context | Medium | Reflect understanding before answering |
| **Partial answer** | AI addresses some but not all parts of a query | Medium | Checklist showing what was/wasn't addressed |
| **Formatting error** | Content is correct but presented poorly | Low | Easy reformat/regenerate affordance |
| **Refusal overreach** | AI refuses a legitimate request due to overly strict safety filters | Medium | Explain why + offer alternative path |
| **Confidence inversion** | AI is most confident when it's most wrong | Critical | Mandatory human review for high-stakes outputs |

---

## The Error Severity Matrix

Use this matrix to determine the appropriate UX response based on error probability and consequence:

| | Low Consequence | Medium Consequence | High Consequence |
|---|---|---|---|
| **High Probability of Error** | Auto-correct silently + log | Warn before action + suggest alternatives | Block action + require human approval |
| **Medium Probability** | Show confidence indicator | Present with verification prompt | Require explicit confirmation + evidence |
| **Low Probability** | No intervention needed | Subtle confidence signal | Add verification step for critical outputs |

---

## Uncertainty Communication Patterns

### The Hedging Spectrum

From most to least uncertain, calibrate AI language:

| Confidence Level | AI Language Pattern | Visual Signal | Example |
|---|---|---|---|
| **90%+** | Direct statement | Green / no indicator | "The meeting is scheduled for 3pm." |
| **70-90%** | Qualified statement | Amber indicator | "Based on the data available, the meeting appears to be at 3pm." |
| **50-70%** | Explicit uncertainty | Amber + explanation | "I found conflicting information. It may be 3pm, but some sources say 2pm." |
| **30-50%** | Presented as possibilities | Red indicator | "I'm not confident about this. Here are the possibilities I found: [list]" |
| **Below 30%** | Deferred to user/human | Red + escalation | "I don't have enough information to answer reliably. Here's what might help: [resources]" |

**Anti-pattern:** Using the same hedging language for everything ("I think..." prepended to every response). This makes hedging meaningless. Reserve it for genuine uncertainty.

---

## The Hallucination Defense Playbook

### Prevention Layer (Before Output)

| Strategy | How It Works | Implementation |
|---|---|---|
| **Source grounding** | Only make claims traceable to provided sources | RAG architecture with citation requirements |
| **Constraint declarations** | AI states what information it's working from | "Based on the 3 documents you uploaded..." |
| **Confidence gating** | Suppress outputs below confidence threshold | Set per-use-case thresholds (e.g., medical = 90%, casual = 50%) |
| **Scope framing** | AI explicitly states what's in and out of scope | "I can help with X. For Y, you'll need [alternative]." |

### Detection Layer (During Output)

| Strategy | How It Works | Implementation |
|---|---|---|
| **Self-consistency checking** | Generate multiple responses; flag divergence | If 3 generations disagree, show the disagreement to the user |
| **Factual anchoring** | Cross-reference claims against known data | Highlight claims that don't match provided sources |
| **Temporal markers** | Flag information that may be outdated | "This information is from [date]. Verify current status." |

### Recovery Layer (After Error)

| Strategy | How It Works | Implementation |
|---|---|---|
| **One-click correction** | User marks output as wrong with minimal effort | Thumbs down + "What was wrong?" dropdown |
| **Regeneration with guidance** | User can ask AI to try again with a hint | "Try again, but focus on [specific angle]" |
| **Human escalation** | Seamless handoff to human when AI fails | "Let me connect you with someone who can help with this." |
| **Error acknowledgment** | AI explicitly owns the mistake | "You're right - my previous answer was incorrect. Here's the corrected version." |

---

## Safe Fallback Design

Every AI output needs a fallback plan. Design the fallback hierarchy:

| Priority | Fallback Level | What Happens | User Experience |
|---|---|---|---|
| 1 | **Graceful degradation** | AI provides a less detailed but more reliable answer | "I can give you a general answer, but for specifics you'll want to check [source]." |
| 2 | **Transparent limitation** | AI explains what it can't do and why | "I don't have access to real-time data for this. Here's what I know as of [date]." |
| 3 | **Alternative path** | AI suggests another way to accomplish the goal | "I can't do X directly, but here's how you might approach it using Y." |
| 4 | **Human handoff** | AI transfers to a human with full context | "Transferring you to a specialist. I've shared our conversation so you won't need to repeat yourself." |
| 5 | **Graceful exit** | AI acknowledges the dead end respectfully | "I've reached the limit of what I can help with here. Here are some resources that might help: [links]" |

**Anti-pattern:** The cliff-edge fallback - AI works perfectly until it doesn't, then shows a generic "Something went wrong" error with no path forward.

---

## The Blast Radius Audit

For every AI feature, map the blast radius of failure:

| Question | What to Document |
|---|---|
| What's the worst output the AI could produce? | Specific harmful scenarios, not abstract risks |
| Who is harmed if the AI is wrong? | End user, downstream consumers of the output, third parties |
| Is the harm reversible? | Can the user undo, correct, or recover from a bad output? |
| How quickly is the error detectable? | Immediately (user sees it), delayed (downstream impact), or hidden (user doesn't know)? |
| What safeguards exist? | Human review, verification prompts, confidence gates, output constraints |

---

## Anti-Patterns

| Pattern | Why It Fails |
|---|---|
| Hiding uncertainty behind confident language | Creates automation bias; users can't calibrate trust |
| Showing a spinner then delivering a hallucination | Users equate "thinking time" with reliability - longer processing implies more trustworthy answers |
| Generic error messages ("Something went wrong") | Tells the user nothing actionable. Always specify: what failed, why, and what to do next |
| Requiring users to detect AI errors themselves | Users are not QA testers. Build detection into the system |
| Punishing users for reporting errors | If the correction flow is cumbersome, users will stop reporting and start silently distrusting |
| Overcorrecting after one error | Dropping confidence displays to 0 after one mistake makes the system unusable. Recalibrate, don't overreact |

---

## Quick Reference

| Task | Framework Element | Key Deliverable |
|---|---|---|
| Design error handling for AI product | Full RECOVER framework | Error type map + severity matrix + fallback hierarchy |
| Audit AI product for failure risks | Blast Radius Audit | Risk map with harm scenarios and safeguards |
| Design hallucination prevention | Hallucination Defense Playbook | 3-layer defense (prevention, detection, recovery) |
| Calibrate uncertainty language | Hedging Spectrum | Language guidelines matched to confidence levels |
| Design safe fallback flow | Safe Fallback Hierarchy | 5-level fallback chain with user experience specs |

## Integration

Works with: `ai-trust-transparency` (how errors affect trust), `ai-conversation-architect` (error recovery in dialogue), `ai-safety-guardrails` (preventing harmful errors), `ai-feedback-loops` (learning from error reports), `ai-ux-eval` (scores the recoverability dimension).
