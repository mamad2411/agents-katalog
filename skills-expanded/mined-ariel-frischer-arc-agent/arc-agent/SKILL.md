---
name: arc-agent
description: >
  Use when generating, validating, inspecting, rendering, repairing, or explaining
  arc-agent system design workspaces. Covers staged YAML artifacts, deterministic
  validation, Mermaid/Excalidraw rendering, OpenCode/Codex/Claude agent runners,
  direct structured-output mode, config, troubleshooting, and development commands.
---

# arc-agent

Generate reviewable software architecture workspaces from system design prompts.
Prefer `arc-agent` when the output needs durable files, deterministic validation,
resume/repair behavior, or rendered Markdown/Mermaid diagrams.

## Quick Commands

```bash
arc-agent new "Design a URL shortener like Bitly"
arc-agent new "Design a URL shortener like Bitly" --out designs/bitly
arc-agent inspect designs/bitly
arc-agent validate designs/bitly
arc-agent render designs/bitly --format all
arc-agent init
arc-agent agent doctor
```

Generated workspaces contain:

```text
arc.yaml
01-requirements.yaml
02-entities.yaml
03-api.yaml
04-high-level-design.yaml
05-deep-dives.yaml      # only when --deep-dives is used
06-diagram.yaml
diagram.mmd
DESIGN.md
```

## Generation

Use `arc-agent new` for full staged generation. Without `--out`, the workspace
is `designs/<slug>` based on the prompt.

```bash
arc-agent new "Design a notification system"
arc-agent new "Design a notification system" --deep-dives
arc-agent new "Design a notification system" --render-excalidraw
arc-agent new "Design a notification system" --dry-run --json
```

Default runner is `auto`: it uses OpenCode Go direct mode when a saved API key
and supported model are available, otherwise it falls back to the configured
agent provider.

```bash
arc-agent init
arc-agent new "Design a notification system"
```

Select another provider with `--agent opencode|codex|claude`. Codex uses
`codex exec --json`; Claude uses `claude -p --output-format stream-json
--verbose`. Claude currently defaults to full permissions for non-interactive
artifact writes. Use `--agent-permissions restricted` when that is not desired.

Use direct mode to bypass provider CLI sessions and call OpenCode Go structured
output:

```bash
arc-agent config set opencode_go_api_key ...
arc-agent new "Design a URL shortener like Bitly" --direct
```

Direct mode writes canonical YAML from strict JSON schema responses, then uses
the same local validation, repair, resume, and render flow.

## Validate, Inspect, Render

Validation is deterministic and agent-free. It checks YAML syntax, schemas,
cross-artifact references, manifest stage state, and Mermaid syntax when `mmdc`
is available.

```bash
arc-agent validate designs/bitly
arc-agent validate designs/bitly/03-api.yaml
arc-agent validate designs/bitly/diagram.mmd
arc-agent validate --no-mermaid designs/bitly
arc-agent validate --json designs/bitly
```

Use `inspect` or `status` to summarize workspace state, rendered outputs,
validation failures, resume point, and next action:

```bash
arc-agent inspect designs/bitly
arc-agent status designs/bitly --json
```

Render outputs are derived from validated YAML:

```bash
arc-agent render designs/bitly
arc-agent render designs/bitly --format markdown
arc-agent render designs/bitly --format mermaid
arc-agent render designs/bitly --format svg,png,excalidraw
arc-agent render designs/bitly --format excalidraw,excalidraw-png,excalidraw-svg
```

`all` currently means Markdown plus Mermaid. Optional image formats require
`mmdc`; Excalidraw image export requires `excalirender`.

## Resume and Repair

Rerunning `arc-agent new` against an existing workspace resumes from the first
pending, running, failed, or invalid generated stage.

```bash
arc-agent new "Design a URL shortener like Bitly" --out designs/bitly
arc-agent new "Design a URL shortener like Bitly" --out designs/bitly --from-stage api
arc-agent new "Design a URL shortener like Bitly" --out designs/bitly --restart
```

When repair is exhausted, run `arc-agent validate <workspace>` or validate the
failed artifact directly, fix the reported field/reference/Mermaid issue, then
resume with `--from-stage`.

## Dependencies

Install Mermaid CLI for strict Mermaid validation and SVG/PNG rendering:

```bash
npm install -g @mermaid-js/mermaid-cli
```

Install Excalidraw rendering only when exporting Excalidraw images:

```bash
curl -fsSL https://raw.githubusercontent.com/JonRC/excalirender/main/install.sh | sh
```

Use `arc-agent agent doctor` to check provider and render dependency coverage.

## Library Usage

```go
import "github.com/ariel-frischer/arc-agent/pkg/arcagent"
```

## Config

Default config path: `~/.config/arc-agent/config.yaml`. Override with
`ARC_AGENT_CONFIG` or `--config`.

Important keys: `agent`, `agent_command`, `model`, `repair_model`, `max_steps`,
`max_retries`, `timeout`, `deep_dives`, `output_dir`, `agent_output`,
`agent_permissions`, `agent_read_scope`, `agent_write_scope`,
`agent_context_scope`, `agent_bash`, `agent_web`, `render_formats`,
`excalidraw_theme`, `new_render_excalidraw`.

## Development

```bash
make build          # Build binary
make bin            # Build binary at bin/arc-agent
make install-global # Install globally to GOPATH/bin
make test           # Run tests
make test-v         # Verbose tests
make test-coverage  # Race + coverage
make lint           # Run linters
make format         # Format code
make benchmark      # Evaluate fixed benchmark outputs
```

Keep Cobra command files thin. Put reusable validation, rendering, and artifact
behavior in `pkg/arcagent`; provider process execution in `internal/agent`;
workflow orchestration, prompts, repair, and manifest logic in
`internal/workflow`; and config loading in `internal/config`.
