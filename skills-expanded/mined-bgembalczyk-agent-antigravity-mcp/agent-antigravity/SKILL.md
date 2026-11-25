---
name: agent-antigravity
description:
  Drive the agent-antigravity MCP server, which gives you a real remote Linux sandbox agent (Google's Gemini Antigravity) with code execution, shell/Python/Node, web search and URL browsing, multimodal input, custom function calling, connecting other MCP servers as sub-tools, a one-call GitHub clone-branch-work-PR workflow, cron-scheduled recurring tasks (Triggers API), reusable named agents (Managed Agents API), and direct sandbox lifecycle control (Environments API: create/list/inspect/delete, download the sandbox filesystem as a .tar, upload files into it). Use this skill whenever the user wants something actually run or executed rather than just written — "run this script", "test this in a sandbox", "have an agent open a PR", "clone this repo and fix X", "schedule this to run every night/hourly/on a cron", "search the web and summarize", "set up a reusable agent with this system prompt", or mentions Antigravity, Gemini's sandbox agent, or any of this server's tool names (create_interaction, create_trigger, create_github_pr_task, create_managed_agent, create_environment, etc.) even in passing. Also use it to look up exact tool parameters, status values, or config shapes (EnvironmentConfig, hooks.json, mcp_server tool entries) before calling any tool in this server.
---

# agent-antigravity MCP server

Delegate real work to this sandbox agent instead of doing it yourself — hand it a
clear, complete, self-contained instruction through one of the tools below, then
poll or continue the same interaction rather than re-prompting from scratch. It
can execute code, browse the web, call functions, and keep sandbox state across
turns; treat it like handing a task to a capable but literal-minded coworker who
needs the full picture up front, not incremental hints.

Before calling anything, confirm `GEMINI_API_KEY` is set (the server raises
`ValueError` otherwise); confirm `GITHUB_TOKEN` too if the task needs
`create_github_pr_task`.

## Tool quick reference

| Tool                                        | Use it to                                                       |
|---------------------------------------------|-----------------------------------------------------------------|
| `create_interaction`                        | Start a new task: run code, search the web, multimodal input    |
| `continue_interaction`                      | Send a follow-up turn in the same sandbox (files persist)       |
| `submit_function_result`                    | Answer a `requires_action` status from a custom `function` tool |
| `get_interaction_status`                    | Poll a single interaction by ID                                 |
| `list_interactions`                         | List cached interactions, newest first                          |
| `cancel_interaction`                        | Stop an in-progress (typically `background=True`) interaction   |
| `delete_interaction`                        | Remove a stored interaction and its local cache entry           |
| `create_github_pr_task`                     | One call: clone repo, branch, do task, push, open PR            |
| `create_trigger`                            | Schedule a recurring interaction on a cron expression           |
| `list_triggers` / `get_trigger`             | Inspect triggers                                                |
| `update_trigger_status`                     | Pause/resume a trigger                                          |
| `delete_trigger`                            | Permanently remove a trigger                                    |
| `run_trigger`                               | Fire a trigger immediately, outside its schedule                |
| `list_trigger_executions`                   | Audit a trigger's run history                                   |
| `create_managed_agent`                      | Register a reusable agent (persona, tools, environment) by ID   |
| `list_managed_agents` / `get_managed_agent` | Inspect registered agents                                       |
| `delete_managed_agent`                      | Remove a registration                                           |
| `create_environment`                        | Provision a standalone sandbox for reuse across interactions    |
| `list_environments` / `get_environment`     | Inspect sandboxes                                               |
| `delete_environment`                        | Terminate a sandbox and free its resources                      |
| `download_environment_files`                | Pull the whole sandbox filesystem as a `.tar`                   |
| `upload_environment_file`                   | Push a local file into a running sandbox                        |

Read the section below for the tool you need — each covers the parameters, the
status values you'll see back, and the things that trip people up.

## Core interaction lifecycle

1.
`create_interaction(prompt, agent=, model=, environment=, tools=, images=, max_total_tokens=, background=, system_instruction=)`
starts a task. Returns JSON with `id`, `status`, `environment_id`, `output_text`,
`steps`. Save the `id` and `environment_id` — you need both to continue the
conversation or check on it later.
    - `status` meanings: `completed` (done, read `output_text`); `requires_action`
      (the agent called a custom `function` tool and is waiting — answer with
      `submit_function_result`); `in_progress` (only for `background=True` — poll,
      don't block); `incomplete` (hit `max_total_tokens` — call `continue_interaction`
      with the same `environment_id` to keep going); `failed`.
    - `background=True` runs async and forces server-side persistence (`store=True`,
      no opt-out) — use it for anything that might take a while, then poll instead
      of waiting synchronously.
2. `continue_interaction(previous_interaction_id, environment_id, prompt=, images=, function_results=)`
   sends a follow-up turn in the *same* sandbox — the filesystem and any files the
   agent wrote in the previous turn are still there. Use this instead of starting a
   fresh `create_interaction` whenever the task builds on prior work.
3. `submit_function_result(previous_interaction_id, environment_id, function_name, call_id, result)`
   is the direct shortcut for the single most common `continue_interaction` case:
   the agent is stuck on `requires_action` waiting for one function's result.
4. `get_interaction_status(interaction_id)` re-fetches a single interaction from the
   live API by ID (cache or not). `list_interactions(page_size=, page_token=)` lists
   the local cache instead — cheaper when you just need an overview, but it won't
   reflect state changes that happened purely server-side.
5. `cancel_interaction(interaction_id)` stops a `background=True` run that's still
   `in_progress`. `delete_interaction(interaction_id)` removes it from the server
   and the local cache — do this for cleanup, not for stopping a running task.

Default `agent` is `antigravity-preview-05-2026`; default `model` is
`gemini-3.6-flash` (alternatives: `gemini-3.5-flash`, `gemini-3.5-flash-lite`).
Not supported: `temperature`/`top_p`/`top_k`/`stop_sequences`/`max_output_tokens`,
structured output, audio/video/document multimodal input (images only).

## GitHub clone → branch → work → PR workflow

`create_github_pr_task(repo_url, task_prompt, base_branch="main", work_branch=, pr_title=, github_token=, model=, agent=)`

This is the single-call path any time the ask is "point the sandbox agent at a
repo and have it open a PR" — don't hand-roll the clone/branch/push/PR steps
through `create_interaction` yourself when this tool already does it in one shot.

- Works on public or private repos. Pass `github_token` (needs `repo` scope) or
  rely on the `GITHUB_TOKEN` environment variable — the tool raises `ValueError`
  up front if neither is available, so check that before assuming it'll work.
- The token is injected through the sandbox's network allowlist header transform,
  never written into the prompt text, so it never shows up in interaction
  transcripts or logs. Never work around this by pasting the token into a custom
  `task_prompt` — that defeats the whole point of the mechanism.
- The agent clones `repo_url`, checks out `base_branch`, creates `work_branch`
  (auto-named `antigravity/task-<hex>` if you don't supply one), performs
  `task_prompt`, commits, pushes, opens the PR via the GitHub REST API, and
  reports the PR URL in `output_text`.
- Returns the same interaction JSON shape as `create_interaction`. The immediate
  response is often still `in_progress` — poll with `get_interaction_status`
  until you actually need the PR URL rather than trusting the first response.
- There's no plan-approval gate before the agent starts pushing. If the user
  wants to review a diff first, tell them this tool doesn't support that pause
  point — they'd need to review the PR after the fact instead.

## Cron scheduling (Triggers API)

Use this whenever the task should repeat on a schedule rather than run once —
nightly maintenance, hourly checks, weekly reports.

-
`create_trigger(schedule, prompt, time_zone=, display_name=, agent=, environment=, max_consecutive_failures=5, execution_timeout_seconds=600)`
— `schedule` is standard 5-field cron syntax (`"0 9 * * *"` = daily at 9am).
`time_zone` is an IANA name (`"America/Argentina/Buenos_Aires"`); omit it and
the schedule runs in UTC.
- `list_triggers(page_size=, page_token=)` / `get_trigger(trigger_id)` — inspect
  what's scheduled.
- `update_trigger_status(trigger_id, status)` with `status` `"active"` or
  `"paused"` — pause instead of deleting when the user wants to temporarily stop
  a recurring task without losing its config.
- `delete_trigger(trigger_id)` — permanent removal.
- `run_trigger(trigger_id)` — fire it once immediately, outside the schedule
  (useful for testing a trigger right after creating it).
- `list_trigger_executions(trigger_id)` — audit history, for "did last night's
  run actually happen" questions.
- Reach for a trigger only when the scheduled work needs the sandbox (code
  execution, web search, file persistence) — a trigger is overkill for something
  that's really just a reminder with no actual task behind it.

## Managed Agents (register once, invoke by ID)

`create_managed_agent(agent_id, base_agent=, model=, system_instruction=, tools=, base_environment=, description=)`
registers a reusable agent configuration — a persona (`system_instruction`),
default `tools`, and a `base_environment` to fork per invocation. Once created,
invoke it exactly like the default agent: `create_interaction(agent=agent_id, prompt=...)`.

Use this instead of repeating the same `system_instruction`/`tools`/environment
setup on every single `create_interaction` call — anytime the same "role" gets
invoked more than once, register it.

- `list_managed_agents(page_size=, page_token=)` / `get_managed_agent(agent_id)` —
  inspect what's registered.
- `delete_managed_agent(agent_id)` — removes the registration only; environments
  and interactions already created under that agent persist independently.
- `agent_id` can't start with a reserved prefix (`antigravity-`, `gemini-`,
  `google-`, etc.) — pick something else if creation fails with a 400.

## Environments (direct sandbox lifecycle)

An environment is the sandbox itself — filesystem, network config, mounted
sources — independent of any one interaction. Reach for these tools when the
sandbox needs to outlive or be shared across multiple interactions, rather than
letting `create_interaction` implicitly fork one per call.

- `create_environment(sources=, network_allowlist=, network_disabled=)`
  provisions a standalone sandbox and returns its `environment_id` — pass that
  ID into `create_interaction`/`continue_interaction`'s `environment=` param to
  reuse it, instead of an inline `EnvironmentConfig` dict (which forks a new one
  per call).
- `list_environments(page_size=, page_token=)` / `get_environment(environment_id)` —
  inspect what's provisioned. Environments persist and are reusable across
  interactions, with roughly a 7-day retention window after going idle.
- `delete_environment(environment_id)` — terminates it and frees its resources.
- `download_environment_files(environment_id, dest_path)` pulls the entire
  sandbox filesystem as a `.tar` to a local path. Use this to actually inspect or
  archive what the agent produced — `output_text` is a summary, not the artifact.
- `upload_environment_file(environment_id, local_path, target_path)` pushes a
  local file into a running sandbox at `target_path` (e.g. a dataset the agent
  needs to work with, or a config file). Use this instead of an inline `EnvironmentConfig`
  source when the environment already exists and you just need to add one file to it.

## Config shapes (pass as plain dicts — no builder tool needed)

- **`mcp_server` tool entry** (inside `create_interaction`'s `tools=` list) connects
  an external MCP server as a sub-tool of the sandbox agent:
  `{"type": "mcp_server", "name": "...", "url": "...", "headers": {...}, "allowed_tools": [...]}`.
  `name` must be lowercase alphanumeric. Only Streamable HTTP is supported — SSE
  remote servers won't work here.
- **`EnvironmentConfig`** (passed as `environment=` to `create_interaction` or
  `create_environment`'s underlying shape):
  `{"type": "remote", "sources": [...], "network": ..., "environment_id": "..."}`.
    - `sources` entries: `"repository"`/`"gcs"` use a `"source"` field (a URL);
      `"inline"` uses `"content"` instead. All types need `"target"` (a subdirectory
      — never `/`).
    - `network` is either `{"allowlist": [{"domain": "...", "transform": {"Authorization": "..."}}]}`
      (allow specific domains and inject headers) or the string `"disabled"` (block
      all outbound traffic). `create_github_pr_task` is the reference example of
      using the allowlist to inject an auth header without ever putting it in the
      prompt — reuse that same pattern for any other authenticated API the sandbox
      needs to call.
- **`hooks.json`** (mounted via an inline source at target `.agents/hooks.json`)
  intercepts sandbox-native tool calls (`code_execution`,
  `read_file`/`write_file`/`list_files`/`delete_file`) before and/or after they
  run: `{"<group>": {"enabled": true, "pre_tool_execution": [{"matcher": "<RE2 regex>",
  "hooks": [{"type": "command"|"http", "command"|"url": "...", "timeout": 10}]}],
  "post_tool_execution": [...]}}`.
    - `pre_tool_execution` hooks can `allow`/`deny` the call; `post_tool_execution`
      hooks run after and can't block anything.
    - Hooks **never** fire for custom `function` tools or `mcp_server` sub-tools —
      only for the sandbox-native tools listed above. Don't reach for `hooks.json`
      to gate a custom function or a remote MCP tool call; it will silently not apply.
    - Unrecognized hook output, a timeout, or a crash defaults to `allow` (fail-safe,
      not fail-closed) — don't rely on a hook alone for anything where silently
      letting the call through would be unacceptable.

## Resources

Read these instead of calling the equivalent tool when you just need to inspect
current state without triggering a fresh action:

`antigravity://interactions/list`, `antigravity://interactions/{id}`,
`antigravity://interactions/{id}/output`, `antigravity://interactions/{id}/steps`,
`antigravity://triggers/list`, `antigravity://agents/list`,
`antigravity://environments/list`.

## Gotchas

- The interaction cache is SQLite-backed (`~/.agent-antigravity/sessions.db` by
  default, overridable via `AGENT_ANTIGRAVITY_SESSIONS_DB`) and survives process
  restarts. `get_interaction_status` always hits the live API by ID regardless of
  what's cached — use it, not `list_interactions`, when you need the current
  authoritative state.
- Every API call tries the `google-genai` SDK first and falls back to direct REST
  on failure (logged at WARNING). REST retries on `429`/`5xx`/transport errors
  with exponential backoff (3 attempts) — set `AGENT_ANTIGRAVITY_LOG_LEVEL=DEBUG`
  if you need to see why a call is slow or failing.
- `stream=True` (real-time step deltas) only exists at the Python SDK level, not
  as an MCP tool option — MCP tool calls are single synchronous request/response,
  so there's nowhere for incremental deltas to surface here.
- For long-running or uncertain-duration work, prefer `background=True` plus
  polling over a single long-blocking `create_interaction` call — it keeps you
  free to do other things between checks instead of tying up the turn.
