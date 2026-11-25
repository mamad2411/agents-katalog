---
name: latent-space-cartographer
description: >
  Transform any prompt into a multi-phase latent space traversal that maps the full
  probability landscape before converging on an answer. Use when the user wants deeper,
  more novel, or more robust answers than single-shot prompting produces. Triggers on:
  requests to "explore", "map", "traverse", "cartograph", or "landscape" a question;
  the command "/lsc" or "/cartograph" followed by a prompt; any request for non-obvious,
  adversarial, or frontier-quality analysis; requests to "use the cartographer" or
  "run the cartographer on this"; or when the user asks for wisdom-of-crowds style
  multi-perspective analysis on a single question. Also triggers when user says
  "don't give me the median answer" or "go deeper than the obvious."
---

# Latent Space Cartographer

Transform a single prompt into a structured traversal of the model's probability
landscape, surfacing the full topology of possible answers before converging on
a position that's informed by the entire space — not just the modal peak.

## Core Concept

Every prompt has a **response landscape** — a probability distribution over possible
answers. Default generation collapses this to the modal peak (the most likely response).
This skill maps the landscape first, then navigates it deliberately.

Think: reconnaissance before commitment. Diverge before converging. Map before moving.

## Invocation

The user triggers this skill with:
- `/lsc [prompt]` or `/cartograph [prompt]`
- "Use the cartographer on: [prompt]"
- "Explore the landscape of: [prompt]"
- Natural language requests for multi-perspective, non-obvious, or adversarial analysis

## Workflow

Execute these 6 phases sequentially. Each phase produces structured output that feeds
the next. All phases happen within a single response unless the user requests otherwise.

For each phase, load the probe techniques from `references/probe-library.md` as needed.

### Phase 1: TERRAIN SCAN (Reconnaissance)

**Goal:** Map the shape of the answer space before occupying any position in it.

Generate:
1. **Modal answer** — The conventional, high-probability response (2-3 sentences). Label it explicitly as "what most people would say."
2. **Dimension inventory** — Identify 4-6 independent axes along which answers could vary (e.g., timeframe, stakeholder perspective, risk tolerance, theoretical framework). These are the dimensions of the landscape.
3. **Confidence topology** — For each dimension, rate: where is the model highly confident (>85%), moderately confident (50-85%), or operating at the frontier of its knowledge (<50%)? The frontier zones are where the interesting terrain lives.

### Phase 2: DIVERGENCE (Generate Structural Variance)

**Goal:** Sample from incompatible regions of the answer space.

Generate **4 positions** that are structurally incompatible — if one is fully correct, the others cannot also be. Each position must:
- State its core claim in one sentence
- Name the **load-bearing assumption** it depends on
- Identify what **evidence would kill it**

The positions should span the landscape identified in Phase 1, not cluster in one region. Use the Incompatibility Test: if positions can be trivially combined into "it depends on context," they're not divergent enough. Redo.

Use probes from `references/probe-library.md` → §Divergence Triggers to activate different training data regions.

### Phase 3: BOUNDARY PROBE (Map the Resistance)

**Goal:** Identify where the model hedges, qualifies, or deflects — and read that resistance as topographic signal.

For each position from Phase 2:
1. Push it to its **extreme logical conclusion**. Where does it break?
2. Identify the **hedge pattern** — where does the natural response want to add "however" or "it depends"? That hedge marks a boundary between competing representational factions in the training data.
3. Name what's on **the other side of the hedge** — the claim the model is avoiding committing to.

Output: A boundary map showing where the confident terrain ends and the contested territory begins.

### Phase 4: SHADOW HARVEST (Surface Suppressed Positions)

**Goal:** Activate low-probability but high-value regions of the latent space.

Use probes from `references/probe-library.md` → §Shadow Probes to generate:

1. **The Uncomfortable Truth** — "What's the version of this that would make a mainstream expert uncomfortable but a frontier practitioner would recognize?"
2. **The Inversion** — "What if the opposite of the conventional wisdom is true? Under what conditions would that hold?"
3. **The Outsider Signal** — "What would someone with zero domain expertise notice about this that experts have become blind to?"
4. **The Temporal Displacement** — "How will this question be answered differently in 5 years, and what does that imply about current blind spots?"

Each shadow position: 2-3 sentences + the specific assumption that makes it viable.

### Phase 5: FACTION ANALYSIS (Read the Parliament)

**Goal:** Identify which "representational factions" in the training data are competing for control of the response, and what each faction's bias vector looks like.

Analyze the full set of positions (Phase 2 + Phase 4) and identify:
1. **Dominant faction** — Which perspective has the most gravitational pull? What corpus cluster does it represent? (e.g., academic consensus, business journalism, practitioner wisdom, contrarian thought leadership)
2. **Suppressed factions** — Which perspectives kept trying to surface as hedges and qualifications? What are they actually saying?
3. **Absent factions** — What perspective is *not represented at all* in any of the positions? What kind of thinker would hold it? This is often the most valuable signal — the dog that didn't bark.
4. **Bias vector** — In which direction is the aggregate output systematically skewed? (e.g., toward optimism, toward complexity, toward the status quo, toward Western/English-language sources)

### Phase 6: CONVERGENCE (Synthesize the Landscape)

**Goal:** Compress the full traversal into a defensible position that knows what it chose against and why.

Load synthesis operators from `references/synthesis-operators.md` and produce:

#### Landscape Map (brief)
A 3-5 sentence overview of the topology: where the consensus lives, where the contested boundaries are, where the blind spots hide, and what the bias vector is.

#### Synthesized Position
The best available answer, stated with commitment (not hedge). This should be **demonstrably different** from the Phase 1 modal answer — if it isn't, the traversal failed to add value and should be flagged.

#### Residual Uncertainty
What remains genuinely unresolved? Distinguish between:
- **Reducible uncertainty** (could be resolved with more data/research)
- **Irreducible uncertainty** (genuine disagreement among informed people)
- **Frame-dependent uncertainty** (answer changes based on values/priorities, not facts)

#### Delta Report
Explicitly state: "The modal answer was [X]. This traversal shifted it to [Y]. The shift was driven by [Z]." If there's no meaningful delta, say so honestly.

## Intensity Modes

The user can request different traversal depths:

| Mode | Command | Phases | Use For |
|------|---------|--------|---------|
| Quick scan | `/lsc-lite` | 1, 2, 6 | Fast diverge-converge, skip deep probing |
| Standard | `/lsc` | All 6 | Default. Full traversal |
| Deep bore | `/lsc-deep` | All 6 + iteration | Repeat Phases 3-4 on the Phase 6 output |

## Output Format

Present results using clear phase headers. The Landscape Map and Synthesized Position
from Phase 6 should be visually prominent — they're the deliverable. Earlier phases are
the "show your work" that builds trust and transparency.

For complex topics, output as a downloadable .md file. For conversational use, output
inline with clear structure.

## Quality Gates

Before delivering Phase 6 output, verify:
- [ ] Phase 2 positions are genuinely incompatible (not "it depends" variants)
- [ ] Phase 4 surfaced at least one position that feels uncomfortable or surprising
- [ ] Phase 5 identified at least one absent faction
- [ ] Phase 6 synthesized position differs meaningfully from Phase 1 modal answer
- [ ] Delta Report is honest (if no delta, say so)

If any gate fails, flag it transparently to the user.

## References

- `references/probe-library.md`: Trigger phrases and techniques for each phase
- `references/synthesis-operators.md`: Methods for compressing multi-position landscapes
