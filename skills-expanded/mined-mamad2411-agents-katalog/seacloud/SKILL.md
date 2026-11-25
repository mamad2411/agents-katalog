---
name: seacloud
description: >-
  SeaCloud CLI is a multimodal task execution CLI designed specifically for
  Agents. With one SeaCloud API Key, it provides unified access to LLM, image,
  video, audio, 3D, and other models; supports model search, spec queries, task
  execution, and result tracking; and helps discover and manage professional
  skills for creative workflows through SkillHub. Use when the
  user asks to generate video, image, audio, music, 3D, run a SeaCloud model,
  inspect SeaCloud tasks, find/install agent skills, or automate SeaCloud
  workflows.
version: 0.2.0
allowed-tools: Bash(seacloud:*), Bash(npx seacloud:*), Bash(npx -y @seacloudai/seacloud-cli:*)
---

# seacloud

SeaCloud CLI is a multimodal task execution CLI designed specifically for
Agents. With one SeaCloud API Key, it provides unified access to LLM, image,
video, audio, 3D, and other models; supports model search, spec queries, task
execution, and result tracking; and helps discover and manage professional
skills for creative workflows through SkillHub.

Model execution can use a SeaCloud API key or managed runtime token.
Sandbox and template commands require a SeaCloud login session from
`seacloud auth login`; `seacloud auth set-key <api-key>` is not enough for
sandbox or template operations.
Use `seacloud account balance` to diagnose paid-credit issues before retrying
model generation.

Before running real SeaCloud commands, load the current CLI capabilities:

```bash
seacloud agent describe
```

Use that dynamic output as the source of truth for available commands,
parameters, output modes, authentication requirements, and recovery steps.

For non-interactive sandbox automation, prefer:

```bash
seacloud auth login
seacloud sandbox create base --no-connect --wait --output json --metadata app=agent
seacloud sandbox exec <sandbox_id> "python --version"
seacloud --dry-run sandbox kill <sandbox_id>
seacloud sandbox kill <sandbox_id>
```

Sandbox/template endpoint priority is `--base-url`,
`SEACLOUD_SANDBOX_URL`, `SEACLOUD_BASE_URL`, then
`https://cloud.seaart.ai/api/sandbox/v1`.

For model calls, `seacloud run` accepts text values, remote HTTP(S) URLs, and
local file paths when the model contract field allows that media type:

```bash
seacloud run <model_id> --param image=./input.png --output json
seacloud run <model_id> --param video=./clip.mp4 --output json
seacloud run <model_id> --param audio=./sound.mp3 --output json
```

Local image files under or equal to 10MiB are encoded as base64 first; if
validation or submission rejects base64, the CLI uploads the image and retries
with the returned URL. Local images over 10MiB and up to 100MB upload directly.
Local videos (`.mp4`, `.mov`, `.avi`, `.mkv`) and audio files (`.mp3`, `.wav`,
`.aac`, `.flac`) upload directly and replace the parameter with the returned
URL. Remote HTTP(S) URLs stay unchanged.

When a model call fails, diagnose in this order:

1. Read the command error, stderr, and task ID printed by the CLI.
2. Inspect the task response and logs:

```bash
seacloud task status <task_id> --output json
```

Prefer `error`, `error_type`, `provider_error`, and `logs` when present.
3. If the failure is still unclear, inspect the model contract:

```bash
seacloud models spec <model_id> --output json
```

Use `input_schema`, `required`, field descriptions, `examples`, `protocol`,
`body_mode`, and `endpoints` to verify parameter names, enum values, file URL
requirements, image/video dimensions, object/array shapes, and upstream task
IDs before retrying. Check backend logs or provider snapshots only when task
status and model spec do not explain the failure.

If `model-contracts` returns 404, do not execute fallback curl directly from
the shell. First inspect the API-key protected skill models fallback through
the CLI:

```bash
seacloud models spec <model_id> --output json
seacloud --dry-run run <model_id> --use-skill-model-fallback --param key=value
```

For LLM-only fallback checks, use:

```bash
seacloud --dry-run llm run <model_id> --use-skill-model-fallback --param key=value
```

Only use `--use-reference-curl` after the CLI-managed fallback fails. The CLI
loads the stored API key or managed runtime token and redacts credentials; an
agent must not copy a fallback curl into the shell or construct Authorization
headers manually. If no usable skill model fallback is found, search the
official provider documentation for required parameters, enum values, media
dimensions, formats, and request body shape before any paid call.
