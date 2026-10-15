---
name: run-sim
description: Run the local competition simulator to test the agent. Use when the user says "run sim", "simulate", "test task", "run simulator", "dry run", "test locally", "preview prompts", "run test".
---

# Run Local Simulator

Run the competition simulator to test the agent against generated prompts.

## Prerequisites

Environment variables must be set:
- `SANDBOX_BASE_URL` — Tripletex sandbox API URL
- `SANDBOX_TOKEN` — Sandbox session token
- `AGENT_URL` — Agent URL (default: `http://localhost:8080`)

## Common Commands

### Single task test
```bash
cd langgraph && SANDBOX_BASE_URL=https://tx-proxy-jwanbnu3pq-lz.a.run.app/v2 SANDBOX_TOKEN=xxx uv run python -m sim --task create_employee --lang no
```

### Dry run (preview prompts without calling agent)
```bash
cd langgraph && SANDBOX_BASE_URL=x SANDBOX_TOKEN=x uv run python -m sim --task create_employee --lang no --dry-run
```

### All Tier 1 tasks (dry run)
```bash
cd langgraph && SANDBOX_BASE_URL=x SANDBOX_TOKEN=x uv run python -m sim --tier 1 --dry-run
```

### Full sweep with JSON output
```bash
cd langgraph && SANDBOX_BASE_URL=xxx SANDBOX_TOKEN=xxx uv run python -m sim --all --output json -o results.json
```

### Test against Cloud Run
```bash
cd langgraph && SANDBOX_BASE_URL=xxx SANDBOX_TOKEN=xxx AGENT_URL=https://tripletex-agent-2fquhrogvq-lz.a.run.app uv run python -m sim --task create_customer --lang no
```

## CLI Flags

| Flag | Description |
|------|-------------|
| `--task TYPE` | Run a specific task type |
| `--tier N` | Run all tasks of a tier (1, 2, or 3) |
| `--all` | Run all registered tasks |
| `--lang CODE` | Language (no, en, de, fr, es, sv, da) |
| `--dry-run` | Generate prompts without calling agent |
| `--output FORMAT` | Output format: table (default) or json |
| `-o FILE` | Write output to file |
| `--seed N` | Random seed for reproducible prompts (default: 42) |
| `-v` | Verbose logging |

## Notes

- 41 prompt generators and 42 verifiers are registered
- Language codes: no, en, de, fr, es, sv, da
- Dry run needs dummy env vars (any non-empty string works)
- The simulator uses `SimTest_{uuid[:8]}` prefix for entity names
