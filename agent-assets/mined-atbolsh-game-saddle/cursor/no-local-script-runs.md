# Do not run project scripts locally

The dedicated Python environment for this project (NAMS / `neo4j_agent_memory`,
torch, transformers, Neo4j, etc.) exists **only on remote servers**. There is
no local environment that can run the agent, the notebooks, or any script that
imports from `agent/` or `game/`.

Concretely:

- **Never execute** project scripts, notebooks, or `python -c` snippets that
  import project runtime dependencies on the local machine. They will fail
  with `ModuleNotFoundError` (or worse, run against the wrong environment) and
  the attempt wastes time.
- Verification that IS allowed locally: syntax checks (`ast.parse`), linters,
  JSON validation, and unit-testing pure stdlib logic extracted in isolation
  (e.g. regex matchers).
- When a change needs a real run to verify, say so and hand the user the exact
  command to run on the remote server instead of running anything yourself.
