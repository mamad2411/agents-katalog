---
name: recalibrategpt-ai-fatigue-operators-2026
description: Applies RecalibrateGPT (Wani, UIST Adjunct 2026, arXiv:2609.00506, Sept 1 2026) — the first interaction-level framework for conversational AI fatigue, with five cross-turn operators (Anchor, Replay, Delta, Scope, Steer) targeting a four-type fatigue taxonomy — as the pattern skill for designing AI interfaces that combat retype-read-abandon loops. Use when [designing or reviewing LLM chat/conversational UX, diagnosing why users abandon AI sessions, building cross-turn conversation-controls, or writing about AI fatigue and cognitive load]. NOT for [model quality improvement, agentic workflows, or non-conversational AI interfaces].
---

# RecalibrateGPT: Cross-Turn Operators for Conversational AI Fatigue

## Overview
LLM interfaces devolve into a **type → read → retype** loop that produces conversational AI fatigue, cognitive load, and eventual task abandonment. RecalibrateGPT (Wani; UIST Adjunct 2026; two pilot studies, N=12 advanced LLM users) reframes the problem: AI fatigue "is not just a model-quality issue but an interaction-flow cost that interfaces can remove." The system contributes a four-type fatigue taxonomy, five cross-turn operators that act on the full conversation history with a single click, and pilot evidence of workload halved at high usability (NASA-TLX = 2.7; SUS = 86.5).

## When to Use
- Designing or reviewing any multi-turn LLM chat interface
- Diagnosing session abandonment (is it the model, or the interaction flow?)
- Specifying conversation-history controls (what should a UI expose over the transcript?)
- Content on AI fatigue, cognitive load, and why "just write a better prompt" is a UX failure
- NOT for: non-conversational/agentic surfaces; model or prompt-engineering quality; production claims (pilots only)

## The Fatigue Taxonomy (four types, from the formative study)

| Fatigue type | What the user experiences |
|---|---|
| **Retyping** | Re-describing context and constraints the conversation already established |
| **Scanning** | Hunting through long transcripts for the earlier output or decision being revised |
| **Decision paralysis** | Too many open response options; no structured way to compare or commit |
| **Context drift** | The conversation's frame quietly moved; the user's mental model and the transcript diverge |

## The Five Operators (each targets a distinct fatigue type)

| Operator | Action | Fatigue targeted |
|---|---|---|
| **Anchor** | Pin a statement/criterion as the persistent frame | Context drift, retyping |
| **Replay** | Resurface an earlier output into the current turn | Scanning |
| **Delta** | Request an explicit diff from a prior version | Scanning, decision paralysis |
| **Scope** | Bound the next response (length, section, aspect) | Decision paralysis |
| **Steer** | Redirect mid-generation without restarting | Context drift, retyping |

**Key property:** operators act through a structured panel on the *full conversation history* — one click instead of a re-typed prompt. Invoked via an "AssistiveButton" with three palette layouts (Vertical, Arc, Tablet).

## Evidence (pilot scale — treat as directional)
- Formative qualitative study (same 12 advanced users): derived the taxonomy + two design objectives
- Quantitative evaluation: perceived cognitive workload **halved** (NASA-TLX = 2.7) at high usability (SUS = 86.5)
- **Honest limits:** N=12 advanced LLM users, two pilot studies, no longitudinal data, self-report measures; the contribution is the *framework*, not a validated instrument

## The Transferable Framework: Fatigue is a Flow Cost

**Core reframe:** teams treat AI frustration as a model-quality problem (wait for a better model) or a prompting-skills problem (train the user). RecalibrateGPT locates a third cause — *interaction-flow cost* — which the interface owns and can remove. Practical implication: some of your "model isn't good enough" complaints are actually "the transcript is a hostile workspace" complaints, and they are fixable in the UI.

**Design checklist for conversational AI surfaces:**
- [ ] Can the user pin/anchor constraints once instead of restating them? (→ retyping)
- [ ] Can earlier outputs be resurfaced or diffed without scrolling? (→ scanning)
- [ ] Is there a bounded-response affordance (scope) before open-ended generation? (→ decision paralysis)
- [ ] Can the user redirect without abandoning the thread? (→ context drift)
- [ ] Do operators act on history directly, or force re-prompting? (all)

## Integration with the Library's Fatigue/Load Stack
- `ai-fatigue-scale-design` + `ai-review-fatigue-mitigation` cover the *measurement* and *review-workflow* sides; RecalibrateGPT adds the *interaction-operator* layer for conversational surfaces specifically.
- `ai-collaboration-friction-patterns` + `the-80-percent-problem` document the friction; this skill supplies the concrete operator taxonomy to fix it.
- `cognitive-load-reduction-ai-scaffolding` holds the scaffolding theory; the five operators are its chat-native implementation pattern.
- Distinct from `prompt-wait-evaluate-flow-collapse` (which models the prompt-wait rhythm of agent loops) — this targets conversational transcript work, not agentic runs.

## A-Tech Alignment
- **Open source:** published at UIST Adjunct with a framework and taxonomy that any OSS chat UI can implement — operators are UI patterns, not proprietary tech.
- **Privacy:** pure interaction-layer pattern; no additional data collection required (operators act on the local transcript).
- **Financial freedom:** for solo builders — a differentiated chat product feature set (anchor/replay/delta/scope/steer) implementable in weeks on any LLM backend.
- **Practical:** four-type taxonomy + five-operator table + design checklist are immediately usable in design reviews and content ("AI fatigue is an interface bug, not a model limit").

## Related Skills
- `ai-fatigue-scale-design` · `ai-review-fatigue-mitigation` — measurement + review-side fatigue
- `context-engineering` · `context-maxxing-cognitive-agency` — the context-management theory these operators operationalize
- `chain-of-thought-ux-reasoning-transparency` — visibility into model reasoning (process side)
- `verification-load-interface-design` — the verification-cost interface layer