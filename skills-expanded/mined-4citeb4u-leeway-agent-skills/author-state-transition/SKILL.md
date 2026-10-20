---
name: leeway-author-state-transition
description: Context-conditioned author voice state model for transitions across audience, emotional tone, medium, objective and relationship while preserving stable author traits.
license: MIT
---
# LeeWay Author State Transition

Represent output behavior as a composition of stable profile plus context delta rather than separate caricatures.

VOICE_STATE = STABLE_AUTHOR_CORE + AUDIENCE_DELTA + EMOTIONAL_DELTA + MEDIUM_DELTA + OBJECTIVE_DELTA + RELATIONSHIP_DELTA.

Deltas are evidence-bound and may interact; do not assume linear additivity when samples contradict it. Track transitions and uncertainty. This is a writing behavior model, not a claim about the person's internal psychological state.
