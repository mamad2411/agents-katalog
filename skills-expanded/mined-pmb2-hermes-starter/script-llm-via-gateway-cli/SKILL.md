---
name: script-llm-via-gateway-cli
description: How standalone scripts (scanners, analyzers, no_agent cron jobs) make LLM calls via the Hermes gateway CLI subprocess instead of managing their own API keys — plus defensive JSON parsing for model output, prompt-length ceiling, and score-based tier normalization.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [llm, scripting, gateway, cron, automation, json-parsing, subprocess]
    triggers:
      - script llm call
      - llm from script
      - gateway cli prompt
      - hermes -z
      - no_agent llm
      - script needs llm
      - api key rotation script
      - parse llm json
    related_skills: [pim-ingestion-pipeline, cron-watchdog, model-provider-routing]
---

# Script LLM Calls via Hermes Gateway CLI

Give standalone scripts (scanners, analyzers, cron `no_agent` jobs) LLM capability without managing API keys in the script. Route calls through the Hermes gateway CLI — the gateway already has working provider routing, model config, and keys, so scripts inherit all of it and survive key rotation/expiry with zero changes.

## The Pattern

```python
import subprocess, sys

HERMES_MAIN = "${USER_HOME}/AppData/Local/hermes/hermes-agent/hermes_cli/main.py"

def call_llm(prompt: str) -> str | None:
    result = subprocess.run(
        [sys.executable, HERMES_MAIN, "-z", prompt],
        capture_output=True, text=True, timeout=90,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None
```

- **Use `sys.executable + hermes_cli/main.py -z`, never bare `hermes`** — on Windows the bare command fails with `[WinError 193] %1 is not a valid Win32 application`.
- Budget **~15–20s per call**; subprocess timeout 60–90s. Fine for cron cadence (hourly, 6h, daily); wrong for interactive loops.

## Why Not Direct API Keys in Scripts

Direct-key scripts break silently: keys expire or get suspended (403), endpoints change, and every script duplicates key-management logic. Concrete case (Jul 2026): two OpenCode Go keys were provisioned to `.env` files and both were already 403 on `https://opencode.ai/zen/go/v1/chat/completions` — the direct-API path was dead on arrival while the gateway kept working through its own configured provider. Scripts routed through the gateway needed no changes.

Keep `.env` key loading (`OPENCODE_API_KEY`, `OPENCODE_GO_API_KEY`, `OPENCODE_GO_API_KEY_*`) as a fallback path only, never the primary.

## Defensive JSON Parsing

LLM responses to "output only JSON" prompts routinely arrive as:

1. A bare JSON **array** — `[{...}, {...}]` (not the `{"findings": [...]}` requested)
2. Wrapped in markdown code fences — ```` ```json [...] ``` ````
3. A single object instead of a list
4. `null` or `{"headline": null, "findings": []}` when the prompt is too long

Parse in this order:

```python
import json, re

def parse_findings(raw: str) -> list[dict]:
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []
    if data is None:
        return []
    if isinstance(data, list):
        return [d for d in data if isinstance(d, dict)]
    if isinstance(data, dict):
        if isinstance(data.get("findings"), list):
            return data["findings"]
        if data.get("headline"):
            return [data]
    return []
```

On a null/empty result, **retry once with a shorter, compacter prompt** before giving up.

## Prompt-Length Ceiling

Embedding >~2000 chars of source content in the prompt materially raises the odds of a null/`findings: []` response. Truncate content excerpts to ~2000 chars. For more coverage, chunk the content and make multiple calls rather than one long call.

## Never Trust the Model's Tier/Score Label

The model will return `"tier": 1` on a 0.15-score finding. Re-derive tier from score after parsing:

```python
score = float(f.get("relevance_score", 0))
f["relevance_score"] = max(0.0, min(1.0, score))
f["tier"] = 1 if score >= 0.40 else 2 if score >= 0.20 else 3
```

Thresholds must match the downstream consumer (e.g. `auto_action_handler.py` uses these same cutoffs).

## When to Use

- Any `no_agent` cron script that needs an LLM pass (scoring, summarization, classification)
- One-off analyzer scripts run from the terminal
- Scanners that enrich findings (e.g. `pim_enhancement_scanner.py`, which uses exactly this pattern in `_call_llm_with_retry()`)

## Pitfalls

- **First call can be slow** — cold provider init adds latency; don't set timeout below 60s.
- **Don't loop tightly** — 15–20s/call means a 100-item loop takes 30+ minutes. Batch items into one prompt where possible.
- **stdout may include non-JSON preamble** — the defensive parser above tolerates it; never `json.loads(stdout)` raw.
