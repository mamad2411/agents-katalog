---
name: daemon-claimed-task-poll-loop
description: Local daemon polls server for claimed tasks, spawns isolated workdirs, executes the agent backend, streams events, reports completion — with bounded concurrency and heartbeat.
category: agents
version: 1.0.0
tags: [daemon, polling, agents, task-queue, orchestration]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: medium
---

## When to use

- Server-orchestrated jobs that run on untrusted/user machines.
- Each job is long-running (minutes, not milliseconds).
- You want the machine to pull work rather than accept pushes (firewall/NAT friendly).

## Steps

1. Main loop with a bounded semaphore:
   ```go
   sem := make(chan struct{}, cfg.MaxConcurrentTasks) // default 20
   tick := time.NewTicker(cfg.PollInterval)          // default 3s
   for {
       select {
       case <-ctx.Done(): return ctx.Err()
       case <-tick.C:
           tasks, err := d.client.PollClaimedTasks(ctx, d.runtimeIDs())
           if err != nil { logger.Warn("poll failed", "err", err); continue }
           for _, t := range tasks {
               select {
               case sem <- struct{}{}:
                   go func(t Task) {
                       defer func() { <-sem }()
                       d.activeTasks.Add(1); defer d.activeTasks.Add(-1)
                       d.handleTask(ctx, t)
                   }(t)
               default:
                   // at capacity; server will reassign on next poll
               }
           }
       }
   }
   ```
2. `handleTask` creates an isolated per-task workdir and does NOT delete it on exit (reuse on retry):
   ```
   ~/myapp_workspaces/<workspace_id>/<task_short_id>/
     .git-clone/         # cached repo
     codex-home/         # per-task agent config
     ... work files ...
   ```
3. Spawn the agent backend through the unified interface:
   ```go
   backend, err := agent.New(task.Provider, agent.Config{ ExecutablePath: agentPath, Env: mergedEnv })
   session, err := backend.Execute(ctx, task.Prompt, agent.ExecOptions{ Cwd: workdir, Model: task.Model, ... })
   go d.streamMessages(task, session.Messages)   // forward to server as it runs
   result := <-session.Result
   d.client.CompleteTask(task.ID, result)
   ```
4. Parallel goroutines:
   - `heartbeatLoop` sends `{daemon_id, running_tasks}` every 15s.
   - `workspaceSyncLoop` every 30s re-syncs the workspace list (pick up newly-created workspaces without daemon restart).
   - `gcLoop` periodically inspects old per-task workdirs and removes ones whose issues are closed.
   - `serveHealth` on a deterministic per-profile port so external tools can probe liveness.
5. Graceful shutdown:
   - Block new task claims (stop poll loop).
   - Let in-flight tasks finish up to a deadline.
   - Deregister all runtimes server-side.
   - Exit.

## Example

```
[daemon] starting daemon version=v0.1.14 agents=[claude codex] server=https://api.myapp.io
[daemon] registered runtime 7fa81e... (workspace=Engineering, provider=claude)
[daemon] task 492abc claimed, spawning claude in ~/myapp_workspaces/.../492abc
[daemon] task 492abc streaming: tool_use=Read ...
[daemon] task 492abc completed in 4m12s, 38k tokens
[daemon] heartbeat ok (2 workspaces, 5 runtimes, 1 active task)
```

## Caveats

- The poll interval is the floor on task latency; 3s is fine for minutes-long jobs, too long for second-level jobs — for that, use WebSocket or long-poll instead.
- Concurrency limit prevents a user's machine from being DDoSed by the server; enforce it client-side because the server may not know the machine's CPU budget.
- The workspace-sync loop is also where you detect "the user left this workspace" events — deregister the corresponding runtime and drop any in-flight tasks for it.
- Don't auto-delete per-task workdirs on exit; users want to inspect them, and agent retries benefit from cached repo state.
