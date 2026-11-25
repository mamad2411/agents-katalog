---
name: pstack-runtime
description: How pstack-t3 skills delegate, pick models, isolate work, schedule, and verify inside T3 Code through the orchestrator V2 tools. Read before running any other pstack skill that spawns workers, picks a model, or schedules work.
---

# pstack-t3 runtime

pstack-t3 runs inside T3 Code. Every provider T3 drives (Claude, Codex, Grok, Cursor, Pi, OpenCode, Muse, ACP agents) gets the same `t3-code` MCP server. This file maps each pstack concept onto those tools, so a skill works the same whatever model runs it.

Tool names may carry a harness prefix, such as `mcp__t3-code__delegate_task` or `mcp__t3_code__delegate_task`. The semantics are the same. If a T3 tool this skill names is not in your tool list, find it with the host's tool search when the host has one, and call it by the name the search returns. When the host has no tool search, call the tool directly. Start with `orchestrator_capabilities`, and do not conclude the tools are missing until a search or a direct call has failed. ACP agents that cannot see the tools use the terminal bridge in [ACP fallback](#acp-fallback).

## On-demand files

| File | Read when |
| --- | --- |
| [roles.md](roles.md) | before resolving seats, weighing seat agreement, writing or validating a roles file, or when `roles.py` prints a note the section does not explain |
| [waiting.md](waiting.md) | before collecting child results or waiting on children |
| [host.md](host.md) | when a thread settles or snoozes, before you install or locate skills, before interpreting `hasPendingChildRuns`, `hasPendingQuestion`, or a `mode: "wait"` return, when a child's question wakes this thread, or for history notes |
| [threads.md](threads.md) | before `t3_thread_configure`, `t3_queue`, `t3_thread_transfer`, `run_scheduled_task_now`, or pausing a finite program's schedule |
| [webhooks.md](webhooks.md) | before creating a webhook schedule, asking for a signing secret, or choosing between a webhook and a polling schedule |
| [secrets.md](secrets.md) | before you ask the user for a secret, or before a shell command needs a token, deploy key, or password |
| [light.md](light.md) | before every spawn in light mode |
| [gate-review.md](gate-review.md) | before reusing a gate verdict |
| [failures.md](failures.md) | on usage limit or after restart |
| [verification.md](verification.md) | before UI or device or CLI verification |
| [delegation.md](delegation.md) | before spawning a child task or writing its brief |
| [modes.md](modes.md) | for the checks every mode keeps |
| [isolation.md](isolation.md) | before isolating a writing child or running a heavy command |
| [watching.md](watching.md) | before linking a PR or waiting on its checks |

## Vocabulary

| pstack says | In T3 |
| --- | --- |
| subagent, worker, delegate, reviewer, runner, judge | A child task created with `delegate_task`, owned by this thread. |
| cloud worker | A child task. T3 children run on this machine, so they can reach local files, browsers, and auth. |
| background, `run_in_background` | `delegate_task` with `mode: "async"`. |
| wait for a worker | A thread with a schedule of its own ends the turn, and its completions wake it. Any other thread keeps a bounded wait with `t3_thread_wait`. Call `task_status` for a result mid-turn. See [waiting.md](waiting.md). |
| cancel a worker | `task_cancel`. |
| model slug, role model | A target `{providerInstanceId, model, options}` from `orchestrator_capabilities`, resolved through roles. See [Roles](#roles). |
| `inherit-parent`, `auto` | `"inherit"`. Omit `target` so the child inherits this thread's provider, model, and options. |
| separate chat, coordinator chat, PR owner thread | A top-level thread from `t3_thread_launch`, only where [Top-level threads](#top-level-threads) allows it. |
| worktree for a worker | A worktree from `delegate_task` with `isolation: "worktree"`, or a `t3_thread_launch` worktree binding for top-level threads. See [Isolation](#isolation). |
| `/loop`, hourly tick, automation, scheduled wakeup | `schedule_task`. See [Scheduling](#scheduling). |
| `scripts/watch-pr`, a poll loop, waiting on CI | `watch_pull_request` on the thread that owns the PR. See [Pull request watching](#pull-request-watching). |
| transcript, chat history, cloud-agent URL | A T3 thread, read with `t3_thread_search` and `t3_thread_read`. |
| control-ui, browser MCP | T3 preview tools: `preview_open`, `preview_snapshot`, `preview_act`, `preview_evaluate`, `preview_recording_start`. `preview_act` takes one `action`: `click`, `type`, `press`, `hover`, `drag`, `select`, `upload`, or `scroll`. `preview_dialog` accepts or dismisses a browser dialog. |
| ask the user (`AskQuestion`) | The host's question tool if it has one, otherwise a short question in the reply. |
| todolist | The host's todo tool if it has one, otherwise a checklist in the work log. |
| PR you opened or now drive | Register it with `link_pull_request`. |
| status page, dashboard, report table, chart | A page published with `html_preview`, then `html_render`, inside a reply already due. See [Visual reports](#visual-reports). |

## Deadlines

A deadline or timebox sets the order of work. It never waives a step. This holds for Autopilot's early red-test-and-PR target, a brigade or Orchestrate timebox, and any "aim for N minutes" in a brief. Start the deliverable the deadline names first, then run every step the playbook prescribes before the next gate, such as `CODE-READY` or the final report. That includes How, Architect, investigation, and the code delegate. The clock is never a `skip:` reason. When the remaining steps cannot fit, stop at a verifiable point and report the steps that remain instead of skipping them. A step that the brief's `Waived by mode:` line names is not a skip, because the mode removed it before the attempt started.

## Delegation

4. A child starts with only its brief. It sees none of this conversation. Put the goal, the exact paths or SHAs, how to verify, and the report shape in the brief. Point at files instead of pasting large context. Write tool steps as plain verbs ("read", "search the repo", "run"), because the child may be a different provider with different tool names. When the role entry `roles.py show` printed for the child's seat has `haikuBrief`, paste its paragraphs unchanged, in order, at the end of the brief, per [Claude Haiku 5.5](#claude-haiku-55). A code-writing child inside a poteto-mode playbook opens with the poteto-agent persona body. Below it, paste unchanged the lines `python3 <pstack-runtime>/scripts/roles.py mode --cwd "$PWD" --playbook <name> --attempt <kind> [--brief-mode <value> | --session-mode light]` prints, per [Modes](#modes). They start with the `Playbook: playbooks/<name>.md` line, such as `Playbook: playbooks/feature.md`, and carry the required `Mode:` line. Write no `Playbook:` line of your own, because a second one fails the check. See [Resolve and carry the mode](#resolve-and-carry-the-mode) for the `Attempt:` and `Waived by mode:` lines. Copy the printed `Mode:` value into `--brief-mode` on the `roles.py show` call that seats the delegate, and pass no other mode flag. Write that brief to a file and run `python3 <pstack-runtime>/scripts/roles.py check-brief <file>` before `delegate_task`. Exit 1 names what is missing. Fix the brief, run the check again, and pass the checked text unchanged. A seat that matches this thread's model, or an edit that looks small, is not a `skip:` reason for the code delegate.

Steps 1 to 3, 5, and 6 live in [delegation.md](delegation.md).

### Permissions

The permission modes live in [delegation.md](delegation.md).

### Failure handling

- A target is rejected: call `orchestrator_capabilities`, then fall back per [Roles](#roles), and say which seat changed and why.
- A child fails or returns nothing usable: proceed with N-1 and record the dropout. Respawn once with a fresh child for a required slice. Never resume a failed child to fix its own work. When the failure carries a provider error, follow the next bullet before that respawn. A failure that reads `Killed: out of memory.` is an out-of-memory kill that T3 reports. Lower the load before you respawn that child. Run fewer children at once, or run builds through the slot in [Local command capacity](#local-command-capacity). Report a second kill as a blocker.
- Check a usage limit only for a failed child that did not return the brief's result. When a failed child's error names a usage limit, follow [failures.md](failures.md#usage-limit) before you respawn it.
- `hasPendingChildRuns` on `task_status` does not mean the child is still running. It reports later turns on the child's thread, even after the task ended, and it does not reopen the task, including a turn you start with `t3_thread_send`. Decide completion by `workState` alone.
- A stalled child (see [Delegation](delegation.md#spawn-and-collect) step 5): first call `t3_pending_request` with `action: "list"` and the child's `childThreadId` as `threadId`. A child with a question that blocks it waits on an answer and is not stalled. Answer it per [Pending requests](#pending-requests), and count its 10 minutes again from the answer. Otherwise read its last items. When its last assistant message holds the result the brief asked for, use that message as the result and call `task_cancel` on the task. When its last item is an approval request that is still waiting, call `task_cancel` and respawn once with no `runtimeMode`. Otherwise call `task_cancel` and respawn once for a required slice.

### Fresh children by default

The fresh-child rule lives in [delegation.md](delegation.md).

## Roles

Roles let one skill run on whatever providers the user has. A role value is a list of seats. Each seat is `"inherit"` or a target.

### Where roles live

Role files and commands live in [roles.md](roles.md#where-roles-live).

### Role names

The role table lives in [roles.md](roles.md#role-names).

### Built-in defaults

The unset-role policy lives in [roles.md](roles.md#built-in-defaults).

### Excluded seats

The exclude rules live in [roles.md](roles.md#excluded-seats).

### Budget

The budget cap lives in [roles.md](roles.md#budget).

### Fallback

The fallback order lives in [roles.md](roles.md#fallback).

### Claude Haiku 5.5

The Haiku brief rule lives in [roles.md](roles.md#claude-haiku-55).

## Modes

pstack-t3 runs each piece of work in `full` or `light` mode. Full mode runs every step as each skill says. Light mode keeps every check that decides whether code lands and cuts the fan-out around it. A skill or playbook that spawns links here. Its light behavior is the row in [light.md](light.md) that names it, and its full behavior is its own text.

### Resolve and carry the mode

`roles.py mode` and `roles.py show` resolve one effective mode. The highest level present wins. The order is the brief, then the session, then the coordinator, then the project file `.pstack/t3-roles.json`, then the user file `roles.json`, then `light`.

- A brief's `Mode:` line is the frozen decision. A child copies that line's bare value into `--brief-mode` on every `roles.py mode` and `roles.py show` call it makes, and passes no other mode flag. It never resolves the mode again.
- The user's words set the session. `$poteto-mode light`, "light mode", or "use light mode" in a request sets this thread to light. "full mode" sets it back. A light session passes `--session-mode light` on every `roles.py` call that has no brief value, except the explicit reflect below.
- With neither, pass no mode flag. The roles files decide. When neither file sets a mode, the default is `light`.
- A user's explicit reflect passes `--session-mode full` on every `roles.py show` call it makes, whatever the session or the roles files say. A call with no mode flag would fall through to a roles file that stores light. The session stays light after it.

Every brief whose child resolves seats or spawns carries the mode. Get the lines from `roles.py mode`, never from memory.

```bash
python3 <pstack-runtime>/scripts/roles.py mode --cwd "$PWD" [--playbook <name> --attempt <kind>] [--brief-mode <value> | --session-mode light]
```

- A code delegate's brief passes `--playbook <name> --attempt <kind>`. `<kind>` is `first` for new work, `fix` after a send-back, and `bounce` after a queue bounce. Paste the printed lines unchanged under the persona body. They start with the `Playbook:` line, so write no `Playbook:` line of your own. The printed lines include `Attempt:`. Under `Mode: light` they also include any `Waived by mode:` line. Under `Mode: full` there is no `Waived by mode:` line, and the brief must not add one. See [Delegation](#delegation) step 4.
- An owner, sub-coordinator, unit worker, visual-parity owner, or landing writer is not a code delegate. Run the command without `--playbook` and `--attempt`, and paste its `Mode:` and `Mode source:` lines into the brief or the `message`. Right after them, paste the seat rule below unchanged. A launched thread has no parent to ask, and a `Mode source: session` line reads like a session of its own without it.

  ```text
  Seat rule. Copy the Mode value above into --brief-mode on every roles.py mode and roles.py show call you make, and pass no other mode flag. Never pass --session-mode. Mode source names where your launcher's decision came from. It does not make this thread a session.
  ```
- A read-only leaf, such as a `how` explainer or a reviewer, gets no `Mode:` line. It resolves no seat.
- A light session with no brief runs the same command with `--playbook <name> --attempt first` for its own playbook. Its `Waived by mode:` line names the steps this thread skips.

Before a light `roles.py show` or `roles.py backup` call, read [roles.md](roles.md#budget).

An explicit budget wins. Pass the live catalog and `--parent` on every light `show` call, per [Roles](#roles), so a configured `inherit` seat of a capped role gets the cap.

Escalation only moves work toward `full`. `roles.py mode` prints `Mode: full` and `Mode source: escalated: <reason>` when a lease covers a pattern in the project's `"escalate"` list, at the second send-back, or when `--escalated` carries a recorded reason. A light thread that finds its design contested does not run `interrogate`. A thread whose brief has a `Mode:` line stops at a verifiable point and reports `Contested: <reason>` under its status. A thread whose mode came from the session or the roles files switches that work to full, announces the escalation, and runs the step full mode prescribes, such as `interrogate`. Nothing moves work from full to light mid-flight.

### Light behavior

Light behavior lives in [light.md](light.md#light-behavior).

### Never cut

- Tests and the build. The worker runs the project's test command and build before every gate review, and the landing queue reruns them.
- The landing queue's checks.
- One review at every head SHA before merge, per [Gate review](#gate-review), cross-family unless its same-family fallback applies.
- A review reads the whole diff against its base on round one. A later round reads the fix diff since the last reviewed SHA, per [Rounds after the first](../brigade/verdict-protocol.md#rounds-after-the-first).
- Owner fences. Leases, `--owner` generations, worktrees, and the pass-at-head gate.
- A fresh worker for every send-back, per [Fresh children by default](#fresh-children-by-default).
- The code delegate, with the persona, the `roles.py mode` lines, and `roles.py check-brief`.
- One executing fresh-child test per changed spawn or coordination behavior.

### Gate review

The gate procedure lives in [light.md](light.md#gate-review).

### Announcement

When light mode applies, say so once, at the start, in two or three short sentences. Name the source from the `Mode source:` line, what this work cuts, and what still runs, as in "Light mode is on, from this session. This change gets one design sketch and no separate comment review. Tests, the build, and review run, with a fallback if only the author's family can run." On an escalation, name the rule, as in "This change runs in full mode because its lease covers `land.py`." A worker's report repeats its brief's `Mode:` and `Waived by mode:` lines under its status. A step that line names is not a deviation. Name the mode again only when it changes.

## Isolation

The isolation rules live in [isolation.md](isolation.md).

## Local command capacity

The slot rules live in [isolation.md](isolation.md#local-command-capacity).

## Top-level threads

Create top-level threads only when the user asked for separate threads or invoked a playbook or skill that names them (Orchestrate, Autopilot-full, Autopilot-stack, brigade). Invoking those is that request. Everything else uses child tasks.

The launch shape and the other fields live in [threads.md](threads.md#top-level-threads).

- Follow a thread with `t3_thread_wait` and read it with `t3_thread_read` (use `afterPosition` to read only what is new). Send follow-ups with `t3_thread_send`, interrupt with `t3_thread_interrupt`.
- A thread launched with `t3_thread_launch` has no parent. Its finished turn does not wake the launcher. A launcher that needs a report names the message the launched thread sends with `t3_thread_send`.
- `create_threads` makes up to 20 threads sharing this checkout. Use it only for read-only fan-out the user wants visible as threads.

### Forks

Forks live in [threads.md](threads.md#forks).

## Scheduling

`schedule_task` creates recurring work in T3's scheduler. It runs even when no turn is active, so it replaces `/loop`, Cursor automations, and hourly ticks.

The other schedule fields live in [threads.md](threads.md#scheduling).

## Local state

The state paths live in [host.md](host.md#local-state).

## Verification surfaces

A project `verify-*` skill beats all of these when one exists.

## Visual reports

The page rules live in [verification.md](verification.md#visual-reports).

## History

The history tools live in [host.md](host.md#history).

## Pull requests

The link rule lives in [watching.md](watching.md#pull-requests).

## Pull request watching

Read [watching.md](watching.md#pull-request-watching) before waiting on a PR with `watch_pull_request`. Call `unwatch_pull_request` when this thread stops driving the PR.

## Pending requests

The pending-request tools live in [host.md](host.md#pending-requests).

## ACP fallback

Some ACP agents accept the injected MCP server but do not expose its tools. When the T3 tools are absent and `T3_ACP_MCP_NODE` is set, call the same tools through the terminal:

```bash
ELECTRON_RUN_AS_NODE=1 "$T3_ACP_MCP_NODE" ${T3_ACP_MCP_ENTRYPOINT:+"$T3_ACP_MCP_ENTRYPOINT"} acp-mcp-call orchestrator_capabilities '{}'
ELECTRON_RUN_AS_NODE=1 "$T3_ACP_MCP_NODE" ${T3_ACP_MCP_ENTRYPOINT:+"$T3_ACP_MCP_ENTRYPOINT"} acp-mcp-call delegate_task '{"task":"...","mode":"async","clientRequestId":"..."}'
```

This is the supported transport, not a shell substitute for delegation.

## Outside T3

If neither the tools nor the ACP bridge exist, you are not running in T3. Use the host's native subagents on inherited models, run panels sequentially if needed, and state that model diversity and scheduling were unavailable.

## Skill locations

Before you write a child brief that needs a specific MCP server, read [Skill locations](host.md#skill-locations).

## Personas

- `agents/poteto-agent.md` is the persona for code-writing delegates inside a poteto-mode playbook. Paste its body at the top of the child's brief, paste the `roles.py mode` lines, and run `roles.py check-brief` per [Delegation](#delegation) step 4.
- `agents/comment-sicko.md` is the persona for the no-comments review. Paste its body at the top of that reviewer's brief.
- Paste the body only, without the frontmatter.
