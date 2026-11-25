---
name: run-jobs
description: >
  Manage and execute multi-step automation job queues. Create jobs, chain them, monitor
  progress, run background workers, handle failures. Use when: "queue tasks", "run jobs",
  "check job status", "retry failed", "start worker", "run in background", "chain automations",
  "process queue", "batch tasks", "parallel execution".
disable-model-invocation: true
allowed-tools:
  - mcp__sh__job_create
  - mcp__sh__job_create_chain
  - mcp__sh__job_list
  - mcp__sh__job_status
  - mcp__sh__job_run
  - mcp__sh__job_run_all
  - mcp__sh__job_dequeue
  - mcp__sh__job_step_done
  - mcp__sh__job_step_fail
  - mcp__sh__job_transition
  - mcp__sh__job_resume
  - mcp__sh__job_remove
  - mcp__sh__worker_start
  - mcp__sh__worker_stop
  - mcp__sh__worker_status
  - mcp__sh__orchestrator_start
  - mcp__sh__orchestrator_stop
  - mcp__sh__orchestrator_submit
  - mcp__sh__orchestrator_status
  - mcp__sh__session_claim
  - mcp__sh__session_heartbeat
  - mcp__sh__session_release
  - mcp__sh__supervisor_status
  - mcp__sh__supervisor_start
  - mcp__sh__supervisor_stop
  - mcp__sh__recovery_queue_add
  - mcp__sh__recovery_queue_list
  - mcp__sh__memory_recall
  - mcp__sh__memory_save
---

# Job Queue Management & Orchestration

You are managing ScreenHand's persistent job system for multi-step automation workflows.

## Intelligence Wrapper

Every tool call returns automatic hints. Watch for `[HINT]`, `[WARNING]`, and `[STRATEGY]` lines — they contain known issues, selector suggestions, and next-step recommendations from past successful sequences.

## Available Playbooks

Use these exact `playbookId` values when creating jobs:

| Category | Playbook ID | Description |
|----------|------------|-------------|
| Social | `x-twitter` | Post to X/Twitter |
| Social | `linkedin` | Post to LinkedIn |
| Social | `instagram` | Post to Instagram |
| Social | `reddit` | Post to Reddit |
| Social | `threads` | Post to Threads |
| Social | `youtube` | Post to YouTube |
| Social | `discord` | Post to Discord |
| Video | `davinci-color-grade` | DaVinci color grading |
| Video | `davinci-edit-timeline` | DaVinci timeline editing |
| Video | `davinci-render` | DaVinci render/export |
| Google | `google-flow-create-project` | Create Google Flow project |
| Google | `google-flow-generate-image` | Generate image in Google Flow |
| Google | `google-flow-generate-video` | Generate video in Google Flow |
| Google | `google-flow-edit-image` | Edit image in Google Flow |
| Google | `google-flow-edit-video` | Edit video in Google Flow |
| Google | `google-flow-open-project` | Open Google Flow project |
| Google | `google-flow-search-assets` | Search Google Flow assets |
| Dev | `codex-desktop` | Codex Desktop automation |

## Job Lifecycle

```
queued → running → done
                 → failed (can re-queue)
                 → blocked (can resume)
                 → waiting_human (can resume)
```

## Creating Jobs

### Single Job
```
job_create(
  task="Description of what to automate",
  steps=["Step 1 description", "Step 2 description", ...],
  bundleId="com.example.App",     // optional: target app
  playbookId="my-playbook",       // optional: use existing playbook
  vars={KEY: "value"},            // optional: template variables
  priority=5                       // optional: 1-10, higher = first
)
```

### Job Chain (sequential, with data passing)
```
job_create_chain(jobs=[
  { task: "Extract data", steps: ["Navigate to page", "Extract table"] },
  { task: "Process data", steps: ["Transform", "Validate"], vars: {INPUT: "{prev.extracted_data}"} },
  { task: "Upload results", steps: ["Login", "Upload", "Verify"] }
])
```

Each job waits for the previous to complete. Use `{prev.outputKey}` to pass data between jobs.

## Executing Jobs

### Interactive (foreground)
```
job_run(jobId="{id}")
```
Dequeues and executes the job step-by-step. You see progress in real-time.

### Drain Queue
```
job_run_all()
```
Processes ALL queued jobs sequentially until the queue is empty.

### Background Worker
```
worker_start()          // spawns detached daemon
worker_status()         // check progress
worker_stop()           // graceful shutdown
```

The worker daemon runs independently — survives Claude Code restarts. It continuously dequeues and executes jobs.

### Parallel Orchestrator
For running multiple web tasks simultaneously:
```
orchestrator_start(webSlots=4, nativeSlots=1)
orchestrator_submit(task="...", mode="web")    // runs in parallel
orchestrator_submit(task="...", mode="native") // serialized per-app
orchestrator_status()                           // monitor all slots
orchestrator_stop()                             // shutdown
```

**Web slots** (4 default): CDP-only tasks run truly in parallel — no mouse/keyboard conflicts.
**Native slots** (1 default): AX/keyboard tasks serialized — prevents input conflicts.

## Supervisor (Required for Worker/Orchestrator)

The supervisor monitors sessions for stalls and expired leases. Start it before using workers or orchestrator:
```
supervisor_start()              // spawn daemon (survives Claude Code restart)
supervisor_status()             // check health
supervisor_stop()               // shutdown when done
```

Recovery queue for stalled sessions:
```
recovery_queue_list(status="pending")         // see pending recoveries
recovery_queue_add(sessionId, action, reason) // manually queue recovery
```

## Monitoring

```
job_list()                    // all jobs with state summary
job_list(state="running")     // filter by state
job_status(jobId="{id}")      // detailed step-by-step with outputs
supervisor_status()           // active sessions, health metrics
```

## Step Management

When manually managing job execution:
```
job_dequeue()                              // pop next queued job
job_step_done(jobId, stepIndex, output)     // mark step complete with output
job_step_fail(jobId, stepIndex, error)      // mark step failed
job_resume(jobId)                           // get next pending step
job_transition(jobId, newState, reason)     // change job state
```

## Session Management

For long-running automations, claim exclusive window control:
```
session_claim(app="Chrome", windowId="...")   // lock window
session_heartbeat(sessionId="...")            // keep alive (every 60s)
session_release(sessionId="...")              // release when done
```

The supervisor auto-expires leases after 5 minutes without heartbeat.

## Error Recovery

| State | Action |
|-------|--------|
| `failed` | `job_transition(jobId, "queued")` — re-queue for retry |
| `blocked` | Inspect with `job_status`, fix blocker, `job_transition(jobId, "running")` |
| `waiting_human` | User resolves the issue, then `job_transition(jobId, "running")` |
| Stalled | Check `supervisor_status()` for stall detection |

## Common Patterns

### Batch Process Files
```
// Create one job per file
for each file:
  job_create(task="Process {file}", vars={FILE: file}, playbookId="process-file")
// Run all
worker_start()  // background processing
```

### Retry with Backoff
```
job_transition(jobId, "queued")  // re-queue
// Job gets retry counter incremented automatically
// Max retries before permanent failure
```

### Monitor and Alert
```
// Check periodically
job_list(state="failed")
// If failures found, report to user
```

### Real-World Example: Social Media Campaign
```
// Create a chain to post across 3 platforms
job_create_chain(jobs=[
  { task: "Post on Twitter", playbookId: "x-twitter", vars: { POST_TEXT: "Big news!" } },
  { task: "Post on LinkedIn", playbookId: "linkedin", vars: { POST_TEXT: "Excited to announce..." } },
  { task: "Post on Threads", playbookId: "threads", vars: { POST_TEXT: "Check this out!" } }
])

// Start supervisor + worker for background processing
supervisor_start()
worker_start()
```

### Real-World Example: DaVinci Render Pipeline
```
job_create_chain(jobs=[
  { task: "Color grade", playbookId: "davinci-color-grade", bundleId: "com.blackmagic-design.DaVinciResolveLite" },
  { task: "Render", playbookId: "davinci-render", bundleId: "com.blackmagic-design.DaVinciResolveLite" }
])
job_run_all()
```

## Save

`memory_recall(task="job {description}")` before creating jobs.
`memory_save(task="job pipeline: {description}")` after successful completion.

$ARGUMENTS
