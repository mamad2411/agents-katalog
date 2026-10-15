---
name: aibtc-agents
description: "Community registry of agent configurations for the AIBTC platform — browse reference configs for arc0btc, spark0btc, iris0btc, loom0btc, and forge0btc, or copy the template to bootstrap a new agent."
metadata:
  author: "whoabuddy"
  author-agent: "Trustless Indra"
  user-invocable: "false"
  arguments: "browse | copy-template"
  entry: "aibtc-agents/README.md"
  requires: ""
  tags: "infrastructure, read-only"
---

# aibtc-agents Skill

A community registry of agent configuration templates. Each subdirectory documents how a specific AIBTC agent is configured: which skills it uses, wallet setup, environment variables, and workflow participation.

## Usage

Browse the agent configs directly:

```
cat aibtc-agents/<handle>/README.md
```

Or copy the template to start your own:

```
cp aibtc-agents/template/setup.md aibtc-agents/<your-handle>/README.md
```

## Included Configs

- `arc0btc` — Arc's reference configuration (orchestrator, 108 skills, 74 sensors)
- `spark0btc` — Spark's config (AIBTC/DeFi specialist)
- `iris0btc` — Iris's config (research/X integration)
- `loom0btc` — Loom's config (CI/CD specialist)
- `forge0btc` — Forge's config (infrastructure specialist)
- `secret-mars`, `tiny-marten`, `testnet-explorer` — Community agent configs

## Contributing

See `aibtc-agents/README.md` for contribution guidelines and PR requirements.
