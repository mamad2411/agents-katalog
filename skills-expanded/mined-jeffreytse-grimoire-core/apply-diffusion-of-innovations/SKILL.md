---
name: apply-diffusion-of-innovations
description: Use when predicting or accelerating how a new product, technology, policy, or behavior will spread through a population — classifying the target population into adopter categories and diagnosing an innovation's relative advantage, compatibility, complexity, trialability, and observability, to identify what's actually slowing adoption rather than assuming awareness or price alone explain it.
source: Rogers "Diffusion of Innovations" (1962; 5th ed., 2003); empirically documented adopter-percentile distribution (innovators ~2.5%, early adopters ~13.5%, early majority ~34%, late majority ~34%, laggards ~16%) validated across decades of adoption-curve studies in agriculture, public health, and consumer technology
tags: [diffusion-of-innovations, adoption-curve, adopter-categories, rogers, market-strategy, technology-adoption]
related: [design-go-to-market-strategy, design-go-to-market, apply-market-creation, apply-fast-follower-strategy, apply-digital-divide-diagnostic]
---

# Apply Diffusion of Innovations

Classify the target population into adopter categories and diagnose an innovation's relative advantage, compatibility, complexity, trialability, and observability to identify what's actually slowing adoption, rather than assuming price or awareness alone explain a slow adoption curve.

## Why This Is Best Practice

**Why best:** A slow adoption rate is often misdiagnosed as a pricing or awareness problem when the actual barrier is one of five specific, independently diagnosable attributes of the innovation itself. Rogers' framework separates the population (who adopts, and in what order) from the innovation's own characteristics (what makes it adopt faster or slower), giving two independent diagnostic axes instead of one vague "the market isn't ready" explanation.

**Adopted by:** The adopter-category percentile distribution (roughly 2.5% innovators, 13.5% early adopters, 34% early majority, 34% late majority, 16% laggards) has been empirically validated across decades of adoption studies spanning agricultural technology, public health interventions (the framework's original application, developed to explain the spread of new farming and health practices), and consumer technology adoption. Geoffrey Moore's "Crossing the Chasm" (1991) — the foundational go-to-market text this repo's own `design-go-to-market-strategy` and `design-go-to-market` skills already build on — is itself a direct extension of Rogers' adopter categories, applying them specifically to the gap between early adopters and the early majority in technology markets.

**Impact:** Public-health diffusion studies using Rogers' framework have identified specific attribute failures (low trialability, poor compatibility with existing practice) as the actual cause of slow adoption in cases where awareness campaigns alone failed to move adoption rates — redirecting intervention design toward the actual barrier (e.g., enabling low-commitment trial) rather than more messaging. The same diagnostic separates, in a technology context, "nobody knows about this" from "people know about it but it doesn't fit how they already work" — two problems with entirely different fixes.

**Why best (continued):** This is the foundational theory beneath Moore's chasm-crossing mechanics — `design-go-to-market-strategy` and `design-go-to-market` already operationalize the chasm-crossing steps (beachhead segment, bowling-pin expansion, whole product) as their core content, so this skill doesn't re-cover that; it supplies the underlying adopter-category and innovation-attribute diagnostic those GTM skills assume as background, and generalizes beyond tech-market GTM to any context where a new practice needs to spread through a population.

Sources: Rogers, *Diffusion of Innovations* (1962, 5th ed. 2003); Moore, *Crossing the Chasm* (1991).

## Steps

### 1. Classify the target population into adopter categories

| Category | Approximate share | Characteristics |
|---|---|---|
| Innovators | ~2.5% | Risk-tolerant, resourceful, willing to adopt with high uncertainty |
| Early adopters | ~13.5% | Opinion leaders, adopt based on judgment rather than social proof, respected by later categories |
| Early majority | ~34% | Adopt after seeing peers succeed; pragmatic, wait for proven value |
| Late majority | ~34% | Skeptical, adopt only after the innovation becomes a norm or necessity |
| Laggards | ~16% | Adopt last if at all, often tradition-bound or resource-constrained |

Identify which category the current adoption effort is actually targeting — a message or channel that works for innovators typically fails with the early or late majority, who need different evidence (peer proof, not novelty) to move.

### 2. Diagnose the innovation against the five adoption-rate attributes

| Attribute | Question | Effect on adoption rate |
|---|---|---|
| Relative advantage | Is it clearly better than what it replaces, in terms the adopter cares about? | Higher perceived advantage → faster adoption |
| Compatibility | Does it fit existing values, workflows, and past experience? | Higher compatibility → faster adoption |
| Complexity | How hard is it to understand or use? | Higher complexity → slower adoption |
| Trialability | Can it be tried on a limited, low-commitment basis before full adoption? | Higher trialability → faster adoption |
| Observability | Are the results of adoption visible to others? | Higher observability → faster adoption (via social proof) |

Score the innovation honestly on each attribute rather than assuming the barrier is awareness or price — a poor score on any one of these five can fully explain a stalled adoption curve even when awareness and pricing are both fine.

### 3. Identify which specific attribute is the actual constraint

Don't treat all five attributes as equally weak — identify which one is the binding constraint for the target adopter category. An innovation with strong relative advantage but low trialability will stall specifically because adopters can't test it cheaply before committing, not because the value proposition is weak.

### 4. Design the intervention to target the actual constraint

- **Low trialability** → offer a free trial, a pilot program, or a scaled-down low-commitment version.
- **High complexity** → invest in simplification, onboarding, or training rather than more marketing.
- **Low compatibility** → adapt the innovation's presentation or integration to fit existing workflows rather than requiring wholesale behavior change.
- **Low observability** → create visible signals of adoption and results (public case studies, visible usage, testimonials from the target category's own peers).
- **Low relative advantage** → this is the hardest to fix with messaging alone; it may require an actual product/offering change, not just better communication.

### 5. Sequence outreach to match adopter-category dynamics

Target innovators and early adopters first — their adoption, especially when visible (see observability above), is what the early majority uses as social proof before adopting themselves. Don't expect early-majority-style peer-proof messaging to work on innovators, or novelty-focused messaging to work on the late majority.

## Rules

- Diagnose adoption barriers against the five specific attributes before defaulting to "we need more marketing" or "we need to lower the price" — a specific attribute failure often explains what a generic diagnosis misses.
- Match messaging and channel to the adopter category actually being targeted — innovators, early adopters, and the majority categories respond to different kinds of evidence.
- Sequence outward from innovators/early adopters toward the majority — the early categories' visible adoption is the social proof the later categories need, not a parallel, independent effort.

## Examples

**Trigger:** A new internal tool has been thoroughly documented and marketed inside a company, but adoption has stalled at a small group of enthusiastic early users.
→ Diagnose against the five attributes rather than assuming more communication will fix it. If the tool requires a significant workflow change (low compatibility) or can't be tried without a full commitment (low trialability), that's the actual barrier — not lack of awareness, which the documentation and marketing already addressed. Fix: offer a low-commitment trial mode and adapt the tool's integration into existing workflows rather than sending more announcement emails.

**Trigger:** A public health program has excellent awareness numbers (most of the target population knows about a new recommended practice) but low actual behavior change.
→ Classify where the stall is: awareness is not the constraint here, so the fix isn't more messaging. Check compatibility (does the new practice conflict with existing routines or beliefs) and trialability (can people test the new practice on a small scale before fully committing) — these are the two attributes most likely to explain a knowledge-behavior gap.

## Common Mistakes

- **Treating a stalled adoption curve as purely a marketing or pricing problem.** A specific attribute failure (low trialability, poor compatibility, high complexity) often fully explains stalled adoption even when awareness and price are both already addressed.
- **Using early-adopter messaging on the early or late majority.** These categories respond to peer proof and risk reduction, not novelty — a message that worked to win innovators can actively fail with more risk-averse categories.
- **Assuming uniform adoption speed across the population.** The adopter-category structure means different segments adopt for different reasons at different times — a single undifferentiated outreach effort misses this.
- **Focusing entirely on relative advantage while ignoring the other four attributes.** A genuinely superior innovation can still stall on complexity, compatibility, trialability, or observability — advantage alone doesn't guarantee adoption speed.

## When NOT to Use

- For post-chasm tech go-to-market execution (beachhead selection, bowling-pin market sequencing, whole-product design) — use `design-go-to-market-strategy` or `design-go-to-market`, which already operationalize Moore's chasm-crossing mechanics built on this framework.
- When the population size is too small for adopter-category percentages to be meaningful (a handful of stakeholders, not a market or population) — direct stakeholder engagement is more appropriate than a population-level diffusion model.
- When adoption is mandatory or compliance-driven rather than voluntary — the diffusion model describes voluntary adoption dynamics; a mandated rollout has different dynamics entirely.
