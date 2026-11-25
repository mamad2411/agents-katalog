---
name: fleet-dashboard
description: Live fleet health view — all agents, Postgres, Ollama, open forks, pending tasks, policy rules.
---

@markdownai v1.0

Call in parallel:
  fleet_status(app_id: heimdallr)
  fleet_agents(app_id: heimdallr)
  fork_list(app_id: heimdallr, status: open)
  agent_task_list(app_id: heimdallr)
  policy_list(app_id: heimdallr, active_only: true)

Report in this format:

## Fleet Dashboard

**Postgres:** up/down — N KB atoms · N tasks
**Ollama:** up/down — models: [list]
**Manifests:** N pass / N fail

**Agents** (by priority group):
  OPERATOR:  willow · ada · steve
  ENGINEER:  heimdallr · hanuman · opus · kart · shiva · ganesha
  WORKER:    [any others from fleet_agents]

**Open forks:**
  FORK-XXXX — title (created_by) [date]
  (none if clean)

**Pending tasks:** N (agent: kart)

**Active policy rules:** N
  [list name + target + action if any]

If postgres=down: stop immediately — everything depends on it.
If manifests failing: flag which ones, don't block.
