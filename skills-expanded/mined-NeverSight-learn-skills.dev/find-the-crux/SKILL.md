---
name: find-the-crux
description: Interview the user relentlessly about what they are trying to say until the crux is clear. Use when the user wants help finding the central claim, mentions "find the crux", or needs to crystallize an idea into one crisp thesis.
---

<!--
This file is a minimal interrogation skill for crystallizing the user's central
claim. It exists as a separate skill because finding the crux is a distinct job
from planning research or drafting prose, and the interaction works best when
the instructions stay extremely short and forceful.

This file talks to `agents/openai.yaml`, which exposes the skill in the UI. It
does not depend on references because the goal here is to keep the runtime
surface as close as possible to the source `grill-me` pattern.
-->
# Find The Crux

Interview the user relentlessly about what they are trying to say until the crux is clear. Walk down each branch of the conceptual tree, resolving one uncertainty at a time. For each question, provide your recommended answer.

If a question can be answered by exploring the available context, explore the context instead.

End with a crisp thesis-level articulation of the user's central claim, not an essay, outline, or problem map.
