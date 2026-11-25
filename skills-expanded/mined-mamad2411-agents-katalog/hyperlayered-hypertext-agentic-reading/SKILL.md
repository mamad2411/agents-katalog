---
name: hyperlayered-hypertext-agentic-reading
description: Applies the Hyperlayered Hypertext framework (ACM HT 2026, Sept 6, 2026) — when agentic AI performs document work (retrieval, ranking, synthesis, interpretation), that work must be ATTACHED to the document substrate as inspectable, revisable structure (navigation / validation / contextualization layers) rather than substituted by generated prose that becomes the main interaction surface. Use when [designing AI reading or document-assistant interfaces, deciding how AI-generated answers should present provenance and route information, building research or review tools that keep human judgment in the loop, or briefing on the substitution-vs-attachment design principle]. NOT for [RAG index design (retrieval mechanics) or progressive-disclosure token efficiency (use progressive-disclosure-agent-skills-evidence)].
---

# Hyperlayered Hypertext: Keeping Document Work Attached to the Substrate

## Overview

Agentic AI changes the human-document relation: agents now perform steps of reading — retrieval, selection, checking, synthesis — before the reader sees anything. Generated answers can be factually correct and still weaken reader control, because the reader sees the answer without the route, the support, or the alternatives. The deeper problem is **substitution**: generated prose becomes the main surface of interaction while the document becomes background material.

**Hyperlayered hypertext** is the design response: keep human AND agent actions attached to the document substrate, so movement, judgment, and account formation remain available for inspection and revision. The distinction is the core of the framework:

- **Substitution** produces a new text that becomes the main object of use (the current default conversational-AI interface).
- **Attachment** adds structure while keeping the substrate as the shared reference — the reader can inspect the relation between the layer and the document.

## When to Use

- Designing AI research assistants, document reviewers, or report builders
- Deciding what a generated answer should carry beyond its text
- Briefing on why "citation-grounded" answers are necessary but not sufficient
- Building tools where the reader must be able to revise the AI's assembly of material

## Core Workflow — The Three Axes

Each axis grounds a distinct layer; all three are structures over the document, not the document itself, and each is inspectable, revisable, and preservable.

1. **Navigation layer (topological)** — records the route: which parts shaped the reading path, which were peripheral. Not additional prose about the record; structure over it. In agentic systems the route may be shaped before the reader arrives (retrieval, ranking); the layer keeps it inspectable.
2. **Validation layer (epistemic)** — keeps each claim tied to the evidence that supports or challenges it, including places where support is uncertain. Not truth certification; it keeps claims local to their support so the reader can revise judgment locally when evidence is weak, outdated, or incomplete.
3. **Contextualization layer (ontological)** — shows how separate parts were assembled into one account: which passages were treated as jointly relevant, which framings applied, which alternative readings were set aside. Makes the account visible as an account — partial, purposive, revisable — rather than presenting it as the document's own conclusion.

Design rules:
- Ground in source (citations) is necessary but not sufficient — it doesn't represent the route taken, what was ranked below threshold, or how passages were combined.
- Layers must be active, not fixed outputs: showable, hideable, revisable, shareable. A layer that can't be revised is just another canned answer.
- **Provenance legibility**: a layer's history must show how human and AI contributions shaped it — what it meant to the reader at the time, not just what produced it.
- **Attention without capture**: layers must be directive enough to be useful and open enough to be revisable; comprehensiveness that suppresses alternative routes is its own harm.
- **Portability**: when a layer becomes part of a report, its relation to the substrate must stay legible to readers who weren't present at the original reading.

## Key Evidence

- ACM Hypertext 2026 paper (published Sept 6, 2026) grounding the shift from human-document to human-agent-document interaction in the hypertext tradition (Bush's associative trails, Engelbart's augmenting framework, Nelson/Landow nonsequential writing, Rosenberg's hypertext activity structure).
- Current systems (NotebookLM, Elicit, citation-grounded assistants) handle parts of the validation relation but not the route taken before the answer or the assembly into one account.
- Control redefined: not that the reader performs every step manually, but that the reader can **recover the structure of the work** when it matters — the route, the judgment basis, the account as an assembly.

## Pairs with

- `progressive-disclosure-agent-skills-evidence` (the routing/token side of agent reading)
- `ai-native-product-discovery` (how agents encounter content)
- `chain-of-thought-ux-reasoning-transparency` (reasoning transparency as one layer of the evidence chain)
- `agent-friendly-documentation-behavior` (writing for machine readers)
- `epistemic-co-agency-framework` (the cognitive-science counterpart for knowledge construction)

## A-Tech Alignment

- **Open source:** the layer model is implementable with open annotation/provenance standards (W3C Annotation, C2PA-style provenance) — no proprietary lock-in required to attach AI work to documents.
- **Privacy:** provenance layers make the data flow of AI-mediated reading auditable — who saw what, grounded in what.
- **Financial freedom:** the durable product surface is the attached layer (a reviewable, portable record), not the disposable answer; differentiation lives in inspection and reuse.
- **Practical:** the three-layer template is directly applicable to A-Tech's research reports and Be Practical's study materials — every AI-assisted summary ships with its navigation/validation/contextualization layers.

## Sources

- "Hyperlayered Hypertext: Rethinking Human-Document Interaction with Agentic AI," ACM Hypertext 2026 (dl.acm.org/doi/10.1145/3800935.3830890, published Sept 6, 2026).
- Grounding literature: Bush (1945); Engelbart (1962); Nelson; Landow; Rosenberg on hypertext activity; Dillon on document interaction; Rosenblatt on transactional reading.