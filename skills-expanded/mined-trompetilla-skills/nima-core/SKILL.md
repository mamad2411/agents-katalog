---
name: nima-core
description: Biologically-inspired cognitive memory for AI agents. Panksepp affects, Free Energy consolidation, VSA binding, sparse retrieval, temporal prediction, metacognition. Website - https://nima-core.ai
version: 1.1.8
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": ["python3"] },
      },
  }
---

# NIMA Core

Plug-and-play cognitive memory architecture for AI agents.

**Website:** https://nima-core.ai  
**GitHub:** https://github.com/lilubot/nima-core

## Install

```bash
pip install nima-core

# Auto-setup (detects OpenClaw, installs hooks, configures everything)
nima-core
openclaw gateway restart
```

### Manual Hook Install

```bash
openclaw hooks install /path/to/nima-core
openclaw hooks enable nima-bootstrap
openclaw hooks enable nima-recall
openclaw gateway restart
```

## Quick Start

```python
from nima_core import NimaCore

nima = NimaCore(
    name="MyBot",
    important_people={"Alice": 1.5, "Bob": 1.3},  # These people's memories get priority
)
nima.experience("Alice asked about the project", who="Alice", importance=0.7)
results = nima.recall("project")
```

## Smart Consolidation

Configure which people, emotions, and topics matter most:

```python
from nima_core.services.heartbeat import NimaHeartbeat, SmartConsolidation

smart = SmartConsolidation(
    important_people={"Alice": 1.5, "Bob": 1.3},  # Weight multipliers
    emotion_words={"love", "excited", "proud", "worried"},  # Force-consolidate
    importance_markers={"family", "milestone", "decision"},  # Force-consolidate
    noise_patterns=["system exec", "heartbeat_ok"],  # Skip these
)

heartbeat = NimaHeartbeat(nima, message_source=my_source, smart_consolidation=smart)
heartbeat.start_background()
```

Memories from important people get boosted. Emotional content is always kept. Noise is filtered out.

## Cognitive Stack

All V2 components are **enabled by default** (v1.1.0+). No configuration needed.

To disable: `export NIMA_V2_ALL=false`

## API

- `nima.experience(content, who, importance)` — Process through affect → binding → FE pipeline
- `nima.recall(query, top_k)` — Semantic memory search
- `nima.capture(who, what, importance)` — Explicit memory capture (bypasses FE gate)
- `nima.synthesize(insight, domain, sparked_by, importance)` — Lightweight insight capture (280 char max)
- `nima.dream(hours)` — Run consolidation (schema extraction)
- `nima.status()` — System status
- `nima.introspect()` — Metacognitive self-reflection

## Architecture

```
METACOGNITIVE  — Self-model, 4-chunk WM, strange loops
SEMANTIC       — Hyperbolic embeddings, concept hierarchies
EPISODIC       — VSA + Holographic storage, sparse retrieval
CONSOLIDATION  — Free Energy decisions, schema extraction
BINDING        — VSA circular convolution, role-filler composition
AFFECTIVE CORE — Panksepp's 7 affects (SEEKING, RAGE, FEAR, LUST, CARE, PANIC, PLAY)
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `NIMA_DATA_DIR` | `./nima_data` | Memory storage path |
| `NIMA_MODELS_DIR` | `./models` | Model files path |
| `NIMA_V2_ALL` | `true` | Full cognitive stack (affects, binding, FE, etc.) |
| `NIMA_SPARSE_RETRIEVAL` | `true` | Two-stage sparse index |
| `NIMA_PROJECTION` | `true` | 384D → 50KD projection |

## References

- `README.md` — Full documentation with all settings
- `nima_core/config/nima_config.py` — All feature flags
- `.env.example` — Environment variable template
