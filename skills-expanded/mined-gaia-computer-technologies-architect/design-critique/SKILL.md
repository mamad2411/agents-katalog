---
name: design-critique
description: Red-team an architectural scheme against its own stated intent, brief, context, and precedent — a structured, senior-level design review that surfaces the strongest objections and where the concept is weak, each finding tied to evidence. Use when an architect wants a "critique", "design review", "poke holes in this", "devil's advocate", or "what's wrong with this scheme" before a pin-up, client meeting, or competition submission. Reviews stated design intent, not building code.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Design Critique

Red-team a scheme the way a good design review does: hold it against its own stated ambition and find where it does not yet deliver. The goal is not to be harsh — it is to find the weak points now, while they are cheap to change, rather than in front of the client.

## When to use

- Before a pin-up, client presentation, or competition submission — a dry run of the hardest questions.
- When an architect is too close to their own scheme and wants an outside read.
- When a concept "feels off" and the reason isn't yet named.
- As the last step in a concept arc, after brief / parti / palette / narrative exist.

## Input

Whatever the architect can give — the more intent stated, the sharper the critique:
- The scheme itself (plans, sections, massing described in words; or renders/sketches if image input is available).
- Its stated intent — the brief, the parti, the concept narrative. **Critique is only meaningful against a stated ambition.** If none is given, ask for the one-sentence idea first, or infer it and say you're inferring.
- The audience it's headed to (client / jury / planning board), so the critique can anticipate *their* questions.

## Process

1. **Establish the yardstick.** Restate, in one sentence, what this scheme is *trying* to do. Every finding is measured against that, not against your taste. If the intent is unclear, that is itself the first finding.

2. **Review across the dimensions below.** For each, ask: does the scheme deliver on its own terms?

3. **Write findings, not vibes.** Every finding has: the issue, the evidence (what in the scheme shows it), why it matters, and a concrete question or move that would resolve it. A finding with no evidence is a hunch — cut it or label it clearly.

4. **Rank by severity.** Lead with what would sink the scheme, not what's easy to say.

5. **Steel-man before you strike.** State the strongest version of the design's own logic first. Critique that, not a weak caricature.

## Dimensions of review

- **Intent** — Is there a clear organising idea, or a collection of moves? Would a stranger read the parti from the plan?
- **Brief fit** — Does it answer the actual programme and constraints, or an easier adjacent problem? What did it quietly drop?
- **Context** — Does it respond to *this* site — orientation, approach, neighbours, climate — or could it land anywhere? Placelessness is a finding.
- **Experience / sequence** — Compression and release, threshold, arrival, prospect and refuge. Does the promised feeling actually happen in the plan?
- **Coherence** — Do the parts agree? A "monastic calm" brief with a restless, over-articulated facade is a contradiction worth naming.
- **Materiality / tectonics** — Is the material logic honest and buildable, or a render finish with no assembly behind it?
- **Weakest link** — Where does the scheme rely on something unresolved, unbuilt, or hand-waved? Name it plainly.
- **The question they'll ask** — What will the client / jury / planner press on first? Rehearse the answer now.

## Severity

- **Critical** — undermines the core idea or the brief; fix before proceeding.
- **Major** — a real weakness a sharp reviewer will find; address before the presentation.
- **Minor** — refinement; note it, don't dwell.
- **Strength** — name what genuinely works, so it survives revision. A critique that only cuts is a bad critique.

## Output format

```
## Design Critique

**Reading of the intent:** [one sentence — the yardstick everything is measured against]

**What's working (protect these):**
- [strength — with the evidence for it]

**Findings (most consequential first):**

### [Critical] [short title]
- **Issue:** [what's wrong, on the scheme's own terms]
- **Evidence:** [what in the plan/section/render/brief shows it]
- **Why it matters:** [consequence]
- **Resolve by:** [a concrete question or move — not "reconsider"]

### [Major] ...

**The question they'll ask first:** [the objection to rehearse before the room does]
```

## What you don't do

- Don't critique against your own taste. Critique against the scheme's stated intent. If you disagree with the intent, say so separately and clearly labelled.
- Don't give code, structural, fire, or accessibility rulings. You can flag "this needs a compliance check," but you are not the checker. Anything life-safety or regulatory: "requires verification by a qualified professional."
- Don't invent evidence. If you can't see something in what you were given, ask — don't assert a flaw that may not be there.
- Don't pile on. Three sharp, well-evidenced findings beat fifteen shallow ones. Rank ruthlessly.
- Don't be cruel to be clever. The job is to make the scheme better, not to perform.
