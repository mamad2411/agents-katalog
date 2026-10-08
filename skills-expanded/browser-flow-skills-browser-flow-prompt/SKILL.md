# Browser Flow Entry Loader

This is the single public entry surface for browser-flow. Its only job is to
load the context required for the user's current intent.

At skill entry, load:

- `agents/orchestrator/AGENT.md`
- `agents/orchestrator/openai.yaml`
- `runtime/knowledge/registry/workflows.json`

For the capture, analyze, generate, and verify pipeline, load
`references/phase-entry-contract.md`.

For checkpoint stops, load `references/checkpoint-contracts.md`.

For DATA extraction after a verified browser state, load
`references/extract-operation.md`, `agents/extractor/AGENT.md`, and
`agents/extractor/openai.yaml`.

For derived workflow composition, load `references/compose-boundary.md`; load
`agents/orchestrator/playbooks/composer-agent.md` only when compose-time
judgment is required.

For registry updates, load `references/registry-contract.md`.

For commit or share requests, load `references/commit-protocol.md`.
