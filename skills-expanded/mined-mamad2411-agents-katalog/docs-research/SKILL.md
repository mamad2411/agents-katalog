---
name: docs-research
description: Answer a documentation question from local sources with traceable claims and explicit limitations.
---

# Documentation research

Use for offline comparisons, configuration questions, or preparing an evidence
summary. This skill does not authorize web access, agent execution, or file edits.

1. Frame the question and find the nearest primary local source before broad
   searching. Capture its path, version, and date where available.
2. Cross-check claims against code or tests if the question is about shipped
   behavior. Do not turn a proposal, README, or upstream doc into native proof.
3. Attribute each consequential claim with a path/section; quote only the
   smallest passage needed. Label observations, documentation, and inference.
4. Surface contradictions rather than choosing the more convenient source.
   State what additional check would resolve them.
5. Return a concise answer, source list, confidence boundary, and next check.
