---
name: domino-modeling-assistant
description: Enable AI-assisted model development (vibe modeling) in Domino. The assistant writes the data-analysis, model and training code and uses the bundled Domino MCP server to run it as Domino Jobs, wait for and read their output, and read, upload and sync files (text or binary) for DFS projects, so work stays reproducible, governed and tracked in Experiment Manager. Use when setting up an AI coding assistant to work with Domino, configuring or troubleshooting the Domino MCP server, or when the user asks to analyze a dataset, train or compare models, or run scripts as Domino Jobs from a coding assistant.
compatibility: Domino 6.3 and Domino Cloud. Inside a Domino Workspace the bundled MCP server calls the platform through DOMINO_API_PROXY with no credentials; outside Domino it needs DOMINO_HOST and DOMINO_TOKEN (a Personal Access Token or service account token).
---

# Modeling assistant

Applies to Domino 6.3 and Domino Cloud.

## Key components

### MCP (Model Context Protocol)

The Domino MCP server bridges the coding assistant and the Domino platform APIs needed for running Jobs (analysis and training scripts run better as Jobs than on the local terminal), waiting for and reading their output, and reading, uploading and syncing files of a Domino File System (DFS) project when it does not use a Git repository.

The server is **bundled with this plugin** (`mcp-servers/domino_mcp_server/`, name `domino_server`) and starts automatically when the plugin is installed from its source repository. Skills-only distributions do not include it.

If the `domino_server` tools (such as `run_domino_job`) are not available in this session, do not pretend to call them. Tell the user, point them at [SETUP.md](./SETUP.md#register-the-server-manually), and meanwhile use the `domino-jobs` and `domino-python-sdk` skills to run work through the Domino REST API.

- **Inside a Domino Workspace:** nothing to configure. The server calls the platform through `DOMINO_API_PROXY` (no `Authorization` header; the proxy adds the user's token) and reads the project from `DOMINO_PROJECT_ID`, `DOMINO_PROJECT_OWNER`, `DOMINO_PROJECT_NAME` and `DOMINO_IS_GIT_BASED`. On hosts that start MCP servers with a stripped environment (Codex), it recovers these variables from its parent process.
- **Outside Domino (laptop, CI):** set `DOMINO_HOST` (the deployment's HTTPS URL) and `DOMINO_TOKEN` (a Personal Access Token or service account token, sent as `Authorization: Bearer`); Domino user and Project environment variables are not readable there, so the host's configuration or the env file holds the laptop's copy. Hosts with plugin settings ask for both at install; the others read the env file `~/.config/domino-mcp-server/.env` (Codex passes the server no other location). Per-host steps: [SETUP.md](./SETUP.md#give-the-url-and-token-to-the-server). Legacy user API keys (`DOMINO_API_KEY`, `X-Domino-Api-Key`) are deprecated and not accepted. See [SETUP.md](./SETUP.md).

Tool failures come back as MCP tool errors whose message says what to fix; relay it to the user instead of retrying blindly.

Docs: https://docs.domino.ai/cloud/platform-capabilities/features/coding-assistants/modeling-assistant (6.3: replace `cloud` with `6.3`).

## Important considerations

Whenever possible run commands as Domino Jobs through the `domino_server` MCP tools rather than on the local terminal.

At the start of every session, call `get_domino_environment_info`. It tells you whether you are inside a Domino Workspace or on a laptop, the project owner, name and id, whether the project is Git-based or DFS, which authentication mode is active, and what is missing. Inside a Workspace everything is auto-detected; you do not need `domino_project_settings.md`. Outside Domino, fall back to `domino_project_settings.md` for the project name, user name, and dfs setting.

Waiting for a Job happens on the server, never in a loop and never with shell `sleep` (hosts block it): start with `run_domino_job(..., wait_seconds=300)`, call `check_domino_job_run_status(run_id, wait_seconds=300)` again while the response says `is_completed` is false, then read the full output with `check_domino_job_run_results` (`log_type="stdErr"` when the status is not `Succeeded`), briefly explain the conclusions, and share any MLflow or experiment run URL (`open_web_browser` outside Domino, a link inside a Workspace). Caps and response fields: [TOOLS.md](./TOOLS.md#waiting-for-a-job).

Pass `hardware_tier` and `environment_id` to `run_domino_job` only when the user asks for a specific tier or environment; both are validated before the Job starts and an unknown value is an error that lists what exists. Omit both for the project defaults.

Assume project data is already in the Domino project and accessible from job runs, under `/mnt/data/` or `/mnt/imported/data/` (Git-based) or `/domino/datasets/` (DFS); confirm the full path by running a job that lists the folder contents recursively. Always create scripts to understand and transform data and run them as jobs; print analytical output as plain-text tables on stdout so job results are easy to check. Do not delete analysis scripts; save summary charts as image files in the project.

Always check whether the local project has uncommitted changes. For Git-based projects, commit and push before running any Domino job, otherwise Domino cannot see the new files; the file tools refuse Git-based projects. For DFS-based projects, sync with the MCP file tools instead of git before running any jobs, preferring `smart_sync_file`, and never force an overwrite without telling the user what will be replaced. Conflict and overwrite rules, text versus binary content: [TOOLS.md](./TOOLS.md#files-text-and-binary-dfs-only).

When training a model, use MLflow instrumentation and assume the tracking server is configured by Domino; do not set a tracking URI.

## MCP server tools

`get_domino_environment_info`, `run_domino_job`, `check_domino_job_run_status`, `check_domino_job_run_results`, `open_web_browser`, `list_domino_project_files`, `download_file_from_domino_project`, `upload_file_to_domino_project`, `sync_local_file_to_domino`, `smart_sync_file`. Signatures, the waiting rules and caps, hardware tier and environment validation, and text versus binary file handling: [TOOLS.md](./TOOLS.md). Routes behind each tool: `mcp-servers/domino_mcp_server/README.md` in the plugin repository.
