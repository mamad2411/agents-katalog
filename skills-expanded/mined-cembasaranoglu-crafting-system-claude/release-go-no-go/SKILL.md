---
name: release-go-no-go
description: Render a go/no-go release board from readiness gate evidence. Use when calling a release decision.
---

# release-go-no-go

Aggregate readiness gate outputs. Produce go/no-go verdict per area with linked evidence. Mark blockers explicitly.

Primary prompts:

- `prompts/86_release_go_no_go_board.md`
- `prompts/85_readiness_gate_aggregator.md`
