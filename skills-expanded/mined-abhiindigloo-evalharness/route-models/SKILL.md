---
name: route-models
description: Generate a cheapest-first model routing setup with fallbacks and quality escalation, from eval-models results or a user-chosen model order. Produces a standalone Python router (escalates when a reply errors or fails format guards), a routing.json, and a LiteLLM proxy config (error-based fallbacks). Use whenever the user wants model routing, fallbacks, failover, escalation to a stronger model, cost-saving cascades, "use the cheap model unless it fails", or a LiteLLM or gateway config across Claude, Gemini, OpenAI, or local models, even if they don't say "routing". Never deploys or applies anything.
metadata:
  author: Indigloo
  homepage: https://github.com/Abhiindigloo/EvalHarness
---

# Generate a cheapest-first routing setup

Use evidence to send each request to the cheapest model that is likely to succeed, and escalate only when a failure can be detected.

## Inputs

- **Preferred**: `results.json` from eval-models. The chain is every candidate that met the threshold with a known cost, ordered by cost per passing call, keeping each model only if it is more reliable than the cheaper ones before it (dominated models are dropped and listed).
- **Otherwise**: an explicit order from the user via `--chain id1,id2`. Without eval evidence, say clearly that the order is an untested assumption and recommend running eval-models first.

## Guards: the part that makes escalation useful

Escalation on quality only works if a bad reply can be detected automatically. Ask what every good reply must look like, then write `guards.json`:

```json
{"checks": [{"type": "json_keys", "keys": ["invoice_number", "total"]},
            {"type": "max_chars", "value": 2000}]}
```

Guards run on every request, so they must be generic (format, required fields, forbidden phrases, length), not the per-example answers used in the eval. Check types match eval-models (`contains`, `not_contains`, `exact`, `regex`, `json_keys`, `max_chars`). Without guards, the router escalates only on errors and empty replies; state that limitation.

## Generate

```
python3 scripts/make_routing.py --results model-eval-results/results.json \
    --guards guards.json --out routing
```

Options: `--chain id1,id2` to set the order explicitly; `--include-unknown-cost` to append passing candidates whose price is unknown; `--pii-policy block|warn|off` (default `warn`) for prompts containing detected personal data or secrets: `block` never sends them, `warn` sends and reports the categories found, `off` skips the check. Recommend `block` unless the user's application already has consent and controls for that data.

Output in `routing/`:

- `routing.json`: chain, settings, guards. Environment variable names only, never key values.
- `router.py` and `mf_core.py`: standalone router using only the Python standard library. Library call `route(prompt, load_routing("routing.json"))` returns the text, the model used, whether it escalated, and every attempt with latency and cost. CLI: `python3 router.py routing.json "prompt"`.
- `litellm.config.yaml`: LiteLLM proxy config with `fallbacks` and `os.environ/` key references.
- `ROUTING.md`: the plan in plain language.

The `modelfinder_generate_routing` MCP tool returns the same routing.json and LiteLLM config without writing files; use the script when the user wants the standalone router copied into their project.

## Explain the two layers honestly

- **LiteLLM fallbacks** trigger on API errors (rate limits, outages, timeouts), not on wrong answers. The config header says so. Tell the user to check the syntax against current LiteLLM documentation before use, because it changes between releases.
- **router.py guards** escalate on detectable quality failures. They cannot catch answers that are well-formed but wrong.

## After generating

Summarize the chain with each model's eval pass rate and cost, the guards, and the known limits. Recommend monitoring escalation rate and cost per accepted request after rollout, and re-running eval-models when models, prices, or prompts change. Do not deploy, start a proxy, change any application's configuration, or claim it is in production.
