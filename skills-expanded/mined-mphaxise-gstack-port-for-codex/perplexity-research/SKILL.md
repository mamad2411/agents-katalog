---
name: perplexity-research
description: Run brain-augmented current web research and separate new information from what the brain already knows.
---

# Perplexity Research

Use this skill when the user asks for current research with citations and local brain context.

## Workflow

1. Search the local brain first with `query` or `brain-ops`.
2. Browse current web sources for the claim, entity, or topic.
3. Distinguish:
   - already known
   - newly found
   - conflicting
   - uncertain
4. Cite sources and keep quotes short.
5. Offer to capture the result with `capture` or `article-enrichment` when useful.

## Guardrails

- Browse for current facts.
- Do not use uncited web claims for high-stakes conclusions.
- Make inferences explicit.
