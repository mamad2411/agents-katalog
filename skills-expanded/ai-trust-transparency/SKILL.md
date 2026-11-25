---
name: ai-trust-transparency
description: 'Design explainability interfaces that help users understand AI decisions, build calibrated trust, and verify AI outputs. Use when: AI explainability, XAI UX, confidence indicators, citation design, source attribution, trust signals, AI transparency, why did AI do this.'
---

# AI Trust & Transparency

Design interfaces where users can see into the AI's reasoning, calibrate their trust appropriately, and verify claims independently. The GLASS framework makes AI decision-making visible without overwhelming users.

## Core Principle

Trust is not a boolean. Users should not "trust AI" or "distrust AI" - they should develop **calibrated trust**: high confidence when the AI is reliable, healthy skepticism when it's uncertain. Your job is to give them the signals to calibrate correctly.

---

## The GLASS Framework

| Letter | Principle | Design Question |
|---|---|---|
| **G** | Ground in Sources | Can the user trace every AI claim back to a verifiable source? |
| **L** | Layer Explanations | Can the user get a 5-second answer AND a 5-minute deep dive? |
| **A** | Advertise Limitations | Does the interface proactively tell users what the AI is NOT good at? |
| **S** | Show Confidence | Can the user see how certain the AI is about each output? |
| **S** | Support Override | Can the user correct, override, or reject AI outputs without friction? |

---

## The Trust Calibration Spectrum

Design for the right trust level - not maximum trust.

| Trust Level | User Behavior | Design Goal | When Appropriate |
|---|---|---|---|
| **Over-trust (Automation Bias)** | Accepts all AI outputs without checking | Introduce friction to encourage verification | High-stakes decisions (medical, financial, legal) |
| **Calibrated Trust** | Verifies selectively based on confidence signals | Maintain - this is the target state | Most AI interactions |
| **Under-trust (AI Aversion)** | Rejects AI outputs even when correct | Build trust incrementally through track record | New users, after AI failures |

### Trust Erosion Events (TEEs)

A single trust violation can undo weeks of reliable performance. Design for recovery:

| TEE Type | Example | Recovery Pattern |
|---|---|---|
| **Confident hallucination** | AI states a false fact with no hedging | Immediately acknowledge the error class; show what changed to prevent recurrence |
| **Silent failure** | AI gives an answer but misses a critical constraint | Add constraint-checking signals: "I accounted for X, Y, Z in this answer" |
| **Inconsistency** | AI gives different answers to the same question | Surface version/context differences: "This differs from my earlier answer because..." |
| **Opacity** | User cannot understand why AI made a choice | Retroactive explanation: "I recommended X because of [factors]. Here's what would change if..." |

---

## Confidence Display Patterns

### The Confidence Triad

Every AI output should communicate three dimensions of confidence:

| Dimension | What It Tells the User | Display Pattern |
|---|---|---|
| **Certainty** | How sure is the AI about this specific output? | Color-coded badge (green/amber/red) + percentage if available |
| **Basis** | What evidence supports this output? | Inline citations, source cards, "Based on..." prefix |
| **Scope** | What does this answer cover, and what doesn't it cover? | Explicit boundary statements: "This covers X but does not account for Y" |

### Confidence Display Decision Matrix

| Context | Show Numerical Confidence? | Show Color Badge? | Show Source Links? |
|---|---|---|---|
| Casual information lookup | No - feels clinical | Optional | Yes, inline |
| Professional decision support | Yes - precision matters | Yes | Yes, with expandable detail |
| Creative generation (writing, images) | No - subjectivity makes numbers misleading | No | Show inspiration sources if applicable |
| Code generation | Yes (test pass rate) | Yes | Link to documentation used |
| Medical/legal/financial | Yes - accountability demands it | Yes, conservative (amber default) | Mandatory, with recency indicator |

---

## Citation Architecture

Citations are the single highest-impact trust pattern for LLM-based products.

### Citation Depth Levels

| Level | What Users See | When to Use |
|---|---|---|
| **L0: No citation** | Raw AI output | Only for creative/casual use cases with no factual claims |
| **L1: Source attribution** | "Based on [source name]" | Minimum for any factual claim |
| **L2: Inline citation** | Numbered references linked to specific claims | Professional, research, and decision-support contexts |
| **L3: Quotable evidence** | Direct excerpts from sources with highlighting | High-stakes contexts where users must verify independently |
| **L4: Auditable trace** | Full reasoning chain + every source consulted + sources rejected | Regulated industries, compliance, legal discovery |

### Citation UI Patterns

| Pattern | Implementation | Best For |
|---|---|---|
| **Superscript numbers** | Claim text[1] with footnotes | Long-form responses, research |
| **Inline source chips** | "According to `WHO Guidelines 2025`..." | Conversational interfaces |
| **Expandable evidence cards** | Collapsed by default, expand to show excerpt + link | Decision-support dashboards |
| **Side-panel source viewer** | Click citation, source appears in adjacent panel | Document review, analysis tools |
| **Confidence-colored highlights** | Text segments colored by source reliability | Professional research tools |

---

## Explanation Layering

Different users need different explanation depths at different moments. Design explanations that telescope from simple to deep.

### The 5-Second / 5-Minute / 50-Minute Rule

| Layer | Depth | Content | UI Pattern |
|---|---|---|---|
| **5-second** | Headline | One sentence: what the AI did and its confidence | Always visible - the response itself |
| **5-minute** | Summary | Key factors that influenced the output, top 3 reasons | Expandable section: "Why this answer?" |
| **50-minute** | Audit trail | Full reasoning chain, all sources consulted, alternative answers considered | Link to detailed view or export |

**Anti-pattern:** Dumping all three layers at once. The 50-minute layer should never appear unless explicitly requested.

---

## The "Why?" Menu

Every non-trivial AI output should support a "Why?" interaction:

| "Why?" Question | What to Show |
|---|---|
| "Why this answer?" | Top 3 factors that influenced the output |
| "Why not [alternative]?" | What would need to change for the alternative to be recommended |
| "What are you uncertain about?" | Specific elements with lower confidence + what additional info would help |
| "What did you ignore?" | Factors the AI considered but deprioritized, and why |
| "How would this change if...?" | Sensitivity: what inputs would flip the recommendation |

---

## Anti-Patterns

| Pattern | Why It Fails |
|---|---|
| Showing confidence scores without context | "87% confidence" means nothing without a baseline. Is 87% good or bad for this task? |
| Using green for everything | If all outputs are green-badged, the badge system is meaningless. Users need contrast to calibrate |
| Burying explanations behind 3+ clicks | If users can't reach the "why" in one interaction, they won't bother |
| Making citations look like legal disclaimers | Dense, tiny-font footnotes signal "cover our liability" not "verify this yourself" |
| Explaining the model instead of the decision | Users don't care about transformer architecture. They care about "why THIS recommendation for MY situation" |
| Only explaining when wrong | If explanations only appear after errors, users associate explanation UI with unreliability |

---

## Quick Reference

| Task | Framework Element | Key Deliverable |
|---|---|---|
| Add explainability to AI product | Full GLASS framework | Explanation layer architecture + citation depth map |
| Design confidence indicators | Confidence Triad + Display Matrix | Visual system with color, basis, and scope signals |
| Recover from trust violation | Trust Erosion Events table | Recovery flow with acknowledgment, explanation, and prevention |
| Audit an AI product for transparency | Trust Calibration Spectrum | Assessment of where users fall on the spectrum + design interventions |
| Add citations to LLM outputs | Citation Architecture (L0-L4) | Citation system matched to use case risk level |

## Integration

Works with: `ai-error-resilience` (transparency about failures), `ai-conversation-architect` (confidence in dialogue), `ai-safety-guardrails` (transparency about content filtering), `ai-feedback-loops` (user corrections as trust signals), `ai-ux-eval` (scores the transparency dimension).
