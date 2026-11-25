---
name: agentfem-workflow
description: Build, inspect, run, verify, or explain finite-element simulations with an installed AgentFEM runtime through its MCP workflow tools. Use for AgentFEM project work; do not use it as a generic PDE solver or to claim verification that result evidence does not contain.
---

# AgentFEM workflow

Use only the part of the lifecycle the user requested:

1. Reuse known runtime context. If needed, call `describe_system` with the default
   summary; query `topic="materials"` for one capability area or
   `api="fields.displacement"` for an uncertain signature. These focused queries
   do not run doctor or a case. Older runtimes may lack this support: consult
   installed help or explicitly request `full`, not an automatic upgrade.
2. Work only inside the approved project roots. Create a project from the
   nearest official template or inspect the user's existing project.
3. `submit_run` already performs preflight. Use `validate_project` for an explicit
   editing check, not a duplicate before every submission. Resolve addressable
   errors without silently changing physical assumptions.
4. Use `submit_run`, retain its `job_id`, and observe it with
   `get_run_status`. Do not start a duplicate merely because a long solve is
   still running.
5. Read the completed result through `get_result_summary`. Report project path,
   run identity, quantities of interest, and evidence concisely.

Preserve these distinctions:

- Viewing results needs only result/status tools, not creation or another solve.
- Tool failures retain structured error details and the MCP error flag. A reported
  failed simulation status is scientific execution evidence, not permission to retry.

- AgentFEM is the deterministic finite-element engine; the agent interprets,
  orchestrates, and explains.
- `completed` means execution ended successfully. Say `verified` or `validated`
  only when the result's trust evidence says so.
- Treat `case.py` as executable scientific source. Do not run an untrusted
  project without the user's authorization and an appropriate isolation
  boundary.
- Never work around rejected geometry, materials, constraints, MPI limits, or
  path policy by weakening the request without telling the user.
- Keep generated projects and result paths visible so a human can inspect and
  reproduce the work.
