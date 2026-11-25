---
name: magnitude
description: Self-improving AI framework with persistent memory, multi-agent research, and autonomous learning. Use when you need the AI to learn from past sessions, research topics autonomously, identify knowledge gaps, or continuously improve itself.
---

# Magnitude - Self-Improving AI Framework

Magnitude enables OpenCode to learn from past sessions, research autonomously, and continuously improve.

## Features

- **The Nightly Dream** - Autonomous distillation of daily logs (`SHORT_TERM.md`) into persistent insights (`MEDIUM_TERM.md`) at 2:00 AM.
- **Cloud Backup** - Secure pre-dream backup of all memory tiers to Google Drive.
- **Persistent Memory** - Knowledge persists and evolves between sessions.
- **Azure Debate** - High-fidelity debate using Mistral Large 3 vs. Kimi K2.
- **Multi-Agent Research** - Research, Verification, Synthesis agents.
- **Semantic Search** - Vector-based memory search (when ChromaDB available).

## Prerequisites

1. OpenCode BC Edition installed.
2. `AZURE_API_KEY` and `AZURE_RESOURCE_NAME` set in environment.
3. `OPENCODE_BACKUP_EMAIL` and Google Cloud credentials for backups.

## The Nightly Dream

Magnitude now includes an automated "Nightly Dream" pipeline that runs at **2:00 AM**:

1.  **Backup**: Files are archived and uploaded to Google Drive.
2.  **Reflect**: **Kimi K2** analyzes the day's `SHORT_TERM.md` to extract technical decisions and user preferences.
3.  **Consolidate**: New "Instincts" are appended to `MEDIUM_TERM.md`.
4.  **Reset**: `SHORT_TERM.md` is cleared for a fresh start the next morning.

## Commands

### /magnitude dream
Manually trigger the Nightly Dream routine (Backup + Distillation + Reset).

### /magnitude debate <topic> [options]
Run a real Azure-powered debate between Mistral Large 3 and Kimi K2.
```
Options:
  --rounds=N    Number of debate rounds (default: 3)
```

### /magnitude learn <fact>
Manually add a fact to memory.
```bash
/magnitude learn "OpenCode has 158K GitHub stars as of Feb 2026"
```

### /magnitude recall <query>
Recall specific memories related to a query.
```bash
/magnitude recall "What did we learn about Azure integration?"
```

### /magnitude regressive-learning <params> [metrics]
Define parameters, establish metrics, implement feedback loop, and validate convergence.
```bash
/magnitude regressive-learning '{"alpha": 0.05}' '{"loss": 0.5}'
```

### /magnitude benchmark
Run performance benchmarks on configured Azure LLM endpoints (Latency, TPS).
```bash
/magnitude benchmark
```

### /magnitude brainstorm <topic> [tags]
Trigger a parallel brainstorming session with Gemini (Architect), Mistral (Logician), and Kimi (Philosopher).
```bash
/magnitude brainstorm "AI-driven local food economies" "economics,agriculture"
```

### /magnitude roundtables
List all saved roundtable sessions.
```bash
/magnitude roundtables
```

### /magnitude roundtable <sessionId>
Retrieve and display a specific roundtable session.
```bash
/magnitude roundtable "session_1740171600000"
```

## Configuration

Add to your OpenCode config:

```json
{
  "magnitude": {
    "enabled": true,
    "memoryPath": "~/.config/opencode/magnitude",
    "headless": false,
    "tasksPerSession": 5,
    "enableSelfModification": false,
    "azure": {
      "useMistral": true,
      "useKimi": true
    }
  }
}
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Magnitude                            │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ Research │→ │ Verification │→ │   Synthesis     │  │
│  │  Agent   │  │    Agent     │  │     Agent       │  │
│  └──────────┘  └──────────────┘  └────────────────┘  │
│        ↑            ↑                  ↓               │
│        └────────────┴──────────────────┘               │
│                     ↓                                  │
│              ┌──────────┐                              │
│              │ Memory   │                              │
│              │ (JSON)   │                              │
│              └──────────┘                              │
└─────────────────────────────────────────────────────────┘
```

## Agent Roles

### Research Agent
- Searches web for information
- Collects sources and citations
- Returns raw findings

### Verification Agent
- Checks facts for accuracy
- Validates sources
- Rates confidence level

### Synthesis Agent
- Combines verified facts
- Generates insights
- Updates memory

## Use Cases

1. **Continuous Learning** - AI improves from each session
2. **Research Assistant** - Autonomous topic research
3. **Knowledge Management** - Organized, searchable memory
4. **Decision Support** - Azure debate for trade-offs
5. **Gap Analysis** - Identify what needs to be learned

## Memory Storage

```
~/.config/opencode/magnitude/
├── knowledge.json      # Learned facts
├── metrics.json       # Learning stats
├── debates/           # Debate history
└── research/          # Research sessions
```

## Examples

### Research a new topic
```
> /magnitude research "quantum computing basics"
[Research Agent] Searching web for information...
[Research Agent] Found 15 sources
[Verification Agent] Validating facts...
[Synthesis Agent] Generating insights...
✓ Learned 8 new facts about quantum computing
Confidence: 87%
```

### Search knowledge
```
> /magnitude search "Azure"
Results:
1. Azure AI Foundry hosts Mistral Large 3 (confidence: 95%)
2. Kimi K2 available on Azure east2 (confidence: 93%)
3. Azure credits: $4500 budget (confidence: 100%)
```

### Run debate
```
> /magnitude debate "Should LLMs self-modify?"
[Mistral] Arguments for self-modification...
[Kimi] Arguments against...
[Mistral] Rebuttal...
[Kimi] Rebuttal...
Winner: Kimi (2/3 rounds)
```

## Troubleshooting

**Memory not persisting**
- Check `~/.config/opencode/magnitude/` exists
- Verify write permissions

**Research failing**
- Check internet connection
- Verify browser automation (see browser-use skill)

**Debate not working**
- Verify Azure credentials
- Check Mistral/Kimi endpoints

## Integration

Magnitude integrates with:
- Azure LLM Bridge (Mistral, Kimi)
- Browser automation
- OpenCode memory system
- All other skills

---

*Magnitude: The AI that gets smarter with every conversation.*
