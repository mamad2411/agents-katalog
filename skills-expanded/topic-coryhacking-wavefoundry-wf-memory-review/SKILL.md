---
name: wf-memory-review
description: Review and apply eligible agent-memory consolidation, archival, and purge per the memory lifecycle gates. The Memory review workflow.
---

# Review memories (Wavefoundry skill)

This skill is a thin pointer: the workflow lives in `docs/prompts/memory-review.prompt.md`. Read that document and follow it; do not improvise the steps from this summary.

- Prefer the `memory_reconcile`, `memory_consolidate`, and `memory_purge` MCP tools.
- Gate reminder: consolidation, archival, and purge apply only per the prompt's eligibility gates; nothing is purged on judgment alone.
