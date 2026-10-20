---
alwaysApply: true
---

# API credentials live in the repo-root .env — always load it

The repo root contains a gitignored `.env` (template: `.env.example`)
holding, at minimum, `HF_TOKEN`, `OPENAI_API_KEY`, and
`ANTHROPIC_API_KEY`. Any code that talks to a third-party API —
HuggingFace Hub (model/dataset downloads), OpenAI, Anthropic, anything
else — must load it BEFORE the first API touch:

```python
from dotenv import load_dotenv
load_dotenv(REPO_ROOT / ".env")   # anchor to the repo root, NOT the cwd
```

Concretely:

- **Anchor the path to the repo root** (e.g.
  `Path(__file__).resolve().parent.parent / ".env"`), never to the
  working directory — scripts get run from anywhere. Follow the existing
  examples: `agent/config.py`, `training/external_data.py`,
  `scripts/dump_db.py`.
- **Most code gets this for free** by importing `agent.config` (it loads
  `.env` at import time). The trap is STANDALONE scripts that
  deliberately import nothing from the repo (bug reproducers, probes):
  they must load `.env` themselves. Unauthenticated HF downloads
  (rate-limited, slower, fails on gated repos) caused by a forgotten
  load are a recurring, avoidable annoyance.
- **Dual-use scripts** (meant to also run outside this repo, e.g.
  reproducers attached to upstream bug reports) may guard the import
  with `try: ... except ImportError: pass` plus a comment — running
  unauthenticated outside the repo is the correct fallback, and the
  library's own warning makes it visible.
- **Library pickup is automatic once the env var is set**:
  transformers/huggingface_hub read `HF_TOKEN` from the environment; no
  `token=` plumbing needed unless the call site already has it.
- **Never print, log, or commit token values**; `.env` stays gitignored.
  When showing `.env` contents in output, redact values.
