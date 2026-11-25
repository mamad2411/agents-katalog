---
name: tool-params-extract-and-availability-pattern
description: Tools implement is_available(sources) and extract_params(sources) so the agent can decide at plan time whether to include the tool AND automatically bind its inputs from the detected source dict — no per-tool glue code in the planner.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [tools, extract-params, is-available, planner]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/tools/base.py
imported_at: 2026-04-18T00:00:00Z
---

# Self-Describing Tools: is_available + extract_params

## When to use
Your agent has many tools and many data sources. The planner needs to ask two questions for each (tool, source_dict) pair: "is this tool usable given what I've detected?" and "if yes, what arguments do I pass?". Without this pattern, you end up with giant switch statements in the planner.

## How it works
Every tool subclass declares:
- `is_available(sources) -> bool` — e.g. "grafana is in sources AND has api_key". Default: always True.
- `extract_params(sources) -> dict` — e.g. `{"service_name": sources["grafana"]["service_name"], "time_range_minutes": sources["grafana"]["time_range_minutes"]}`. Default: empty dict.

The planner then filters `all_tools` with `[t for t in all_tools if t.is_available(sources)]` and binds inputs via `t(**t.extract_params(sources))` — no special casing.

## Example
```python
class BaseTool(ABC):
    # metadata ClassVars ...

    def is_available(self, _sources: dict[str, dict]) -> bool:
        """Return True when required data sources are present."""
        return True                                   # default: always available

    def extract_params(self, _sources: dict[str, dict]) -> dict[str, Any]:
        """Extract kwargs to pass to run() from available sources."""
        return {}                                     # default: no params

class GrafanaLogsTool(BaseTool):
    name = "query_grafana_logs"
    # ...

    def is_available(self, sources):
        g = sources.get("grafana")
        return bool(g and g.get("grafana_endpoint") and
                    (g.get("grafana_api_key") or g.get("loki_only")))

    def extract_params(self, sources):
        g = sources["grafana"]
        return {
            "service_name": g["service_name"],
            "endpoint": g["grafana_endpoint"],
            "api_key": g["grafana_api_key"],
            "time_range_minutes": g["time_range_minutes"],
            "pipeline_name": g.get("pipeline_name", ""),
        }
```

## Gotchas
- Keep `is_available` cheap — the planner calls it for every tool × every loop. Pure dict lookups, no network.
- If `extract_params` depends on state beyond `sources`, thread state through — don't reach into module globals.
- For "this tool needs auth BUT I can always run it against a test fixture", respect an injected `_backend` sentinel in `sources` and allow availability.
- Function-based tools get the same treatment via the `@tool(..., is_available=..., extract_params=...)` decorator parameters.
