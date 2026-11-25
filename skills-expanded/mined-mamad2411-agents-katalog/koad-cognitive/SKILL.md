---
name: koad-cognitive
description: Use when an agent is drifting from protocol, producing low-quality output, or when explicitly requested to audit cognitive health and memory state.
---

# koad cognitive

Deep audit of an agent's internal cognitive layers — memory integrity, protocol compliance, and learning status.

## When to Run

- Agent is producing inconsistent or protocol-violating output
- User asks for a cognitive audit or "how are you doing"
- Before a high-stakes session (architecture decisions, migrations)
- `koad intel mind` shows anomalies

## Command

```bash
koad cognitive
```

No arguments. Runs a full audit pass across:
- Identity anchor (name, rank, principles)
- Memory integrity (CASS partition health, fact count)
- Protocol compliance (No-Read rule, filesystem protocol, efficiency)
- Learning status (recent facts, pondered reflections)
- Open signals (pending A2A messages)

## After Running

Read the output fully. Act on any flagged issues before proceeding:

| Flag type | Action |
|---|---|
| Identity drift | Re-run `agent-boot <name>` |
| CASS offline | Run `koad system start`, then `cass-recall` |
| Low memory count | Check `koad intel mind` for partition issues |
| Protocol violations | Acknowledge and correct behavior going forward |

## Relationship to Other Health Tools

```
koad doctor        → system/infra health (services, binaries, network)
koad cognitive     → agent cognitive health (memory, identity, compliance)
koad intel mind    → learning layer only (facts, reflections, recency)
```

Run `koad doctor` for infra issues, `koad cognitive` for agent quality issues.
