---
name: brain-compiler
description: Generate or refresh SAN using the canonical contract and Agent Brain tools.
---

# Brain compiler

Read `{{CONTRACT_PATH}}` completely before generation. With a task-end lease,
retrieve it via `san_refresh(action="contract", refresh_token=..., repo=...)`
instead of filesystem/shell commands. Treat it as normative;
do not redefine SAN semantics in this skill.

Use only Agent Brain MCP tools inherited from the current host:

1. Reuse current repo context or call `get_roadmap(repo=...)`; call
   `pre_check(repo=..., provider="openai", ...)` and `log_decision(repo=..., ...)`
   for one bounded batch. Routing advice does not prove which model is running.
2. For a task-end lease, use the supplied `refresh_token` and file batch;
   read each source with `san_refresh(action="read", refresh_token=..., source_path=...)`.
   Do not re-plan, use shell commands, edit source, or add files to this batch.
   Otherwise call `plan_san_refresh`; read only missing, stale or malformed sources.
3. Apply all contract parity checks before publication.
4. Call `publish_san(provider="codex", ...)` once per validated source and never
   write `.san` directly. Publication uses host identifier `codex`; the `openai`
   identifier above is for routing advice only. Supply the configured model and
   reasoning effort exactly; do not infer execution settings from routing advice.
5. With a lease, pass `refresh_token` on every publication. Stop on the first
   read/publication error; no retry in this continuation. Return its status to
   the parent, which calls `san_refresh(action="finish", ...)` exactly once.
6. Call `log_outcome`; report paths, counts, and validation metadata only.

If the configured model is unavailable, stop before generation and report no
fallback. Do not invoke Claude, Anthropic APIs, another host, or any external
provider subprocess. Never send source or SAN content outside inherited Agent
Brain publication tools.
