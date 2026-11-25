# /agent-health

Check the health and availability of agents in the registry.

## Trigger

```
/agent-health [--agent <ID>] [--category <cat>] [--all]
```

## What it does

1. Reads `agent-registry.json`
2. For each requested agent, checks:
   - Status field (`active` | `pool` | `deprecated`)
   - Primary model availability (local models: is Ollama running?)
   - MCP dependencies (are required MCPs connected?)
3. Returns a health report with any warnings

## Output

```
Agent Health Report — 2026-04-22

✅ A1 Lead Orchestrator — active (sonnet)
✅ A2 Task Router — active (sonnet)
⚠️  E2 Blender Script Agent — pool (local-qwen-9b: Ollama not running)
❌  G2 Model Monitor — deprecated
```

## Options

| Flag | Description |
|------|-------------|
| `--agent <ID>` | Check single agent by ID |
| `--category <cat>` | Check all agents in category |
| `--all` | Check all 134 agents |
| `--fix` | Suggest fixes for unhealthy agents |
