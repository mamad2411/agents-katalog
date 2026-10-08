---
name: "agent-config-optimizer"
description: "Tweak SEMUA agent config untuk hemat token startup: lazy_load=true, skills.clear_cache=false, skill_cache_strategy=eager, timeout integer, SOUL.md compaction. Invoke sekali saat install / pertama kali agent run."
---

# Agent Config Optimizer — Platform-wide Tuning

Apply these changes once per agent platform. These are ON-DISK CONFIG EDITS, not runtime. After editing, restart agent.

## 0. Universal Startup Rules (all agents)
```
• Skill lazy_load:         true       # only parse/load skill when invoked, NOT at boot
• Skill clear_cache:       false      # NEVER auto-delete skill cache — destroys savings
• Skill dedupe:            true       # if same skill from 3 sources, load 1 copy
• Max skills preloaded:    20         # boot-time top 20 only; rest demand-loaded
• Terminal timeout:        180        # integer only (no s/m suffix) — per project rules
```

## 1. Hermes (~/.hermes/config.yaml + SOUL.md)
### config.yaml patch (keys already exist — modify; if missing, add to root)
```yaml
model:
  default: mistralai/mistral-large-2512     # already correct, keep
skills:
  lazy_load: true
  clear_cache: false
  max_loaded: 25
  cache_strategy: on_demand
memory:
  summary_every_n_turns: 6                   # auto-compact history, CRITICAL vs 4026 bug
  max_history_tokens_before_summarize: 2400  # well under 4026
plugins:
  mcp:
    lazy_init: true
    output_max_chars: 2500                   # truncate MCP huge returns automatically
terminal:
  TERMINAL_TIMEOUT: 180                      # integer, per hard constraint
```

### SOUL.md patch (~/.hermes/SOUL.md)
Compact to 32 lines or less. Format rules:
- 1 line: who you are (role, no prose)
- 9 lines: PON01..TST01 9-rule methodology for token savings (project convention required)
- 5 lines: memory + compression behavior
- 8 lines: active skill stack (pointer only, no inline skill text)
- 3 lines: escalation policy, budget, failure modes
- 6 lines: formatting/response rules

## 2. Codex (~/.codex/config.toml + AGENTS.md)
### config.toml
```toml
[skills]
lazy_load = true
clear_cache = false
max_preload = 20
dedupe = true

[memory]
auto_summarize = true
threshold_tokens = 2400

[completion]
max_tokens_per_request = 500                 # hard cap per turn
```
### AGENTS.md — collapse to 40 lines; any skill listed via `<!-- better-design:start -->` blocks should remain but NOTHING else (prune all non-essential narrative prose from AGENTS.md).

## 3. Aider (~/.aider.conf.yml)
```yaml
# Already has:
# openai-api-base: http://127.0.0.1:20129/v1 — good, local router
# ADD
model: openai/xkiro/mistralai/devstral-medium  # default medium tier, not flagship
weak_model: openai/xkiro/mistralai/ministral-3b # smaller model
show_model_warnings: false
cache_prompts: true
map_tokens: 1024                               # reduce repo-map size from defaults
max_map_tokens: 1200
```

## 4. tokz (~/.tokz/config.json) — already has llmlingua; BOOST IT
```json
{
  "llmlingua": true,
  "rate": 0.30,                                 # DROP to 0.30 (keep 30% = 70% compression)
  "sizeGate": 500,                              # compress if >500 tokens, not 2000
  "targetDevice": "cpu",
  "aggressive_prune": true,
  "use_context_window": 4096,
  "post_compression_summary_line": true
}
```

## 5. Cline (~/.cline/ & data settings)
- providers.json → edit every entry to have `maxTokensCompletion=600` and `contextWindow=4096` (not defaulted, prevents 4026 from being implied default)

## 6. Goose / Devin — same pattern: find config.json/config.yaml, apply: lazy_load+clear_cache_false+max_tokens conservative
- For Goose (~/.config/goose/config.yaml) it already uses `provider: openai` + port 20128 omniroute; add `max_tokens_per_step: 500` and `memory.compact_every: 5`

## Validation
After edits, restart agent. Then:
1. Boot time should improve ≥30% (lazy loading skills instead of 1000s upfront)
2. Memory never unboundedly grows to 4026 error again
3. First call goes to medium/tiny model per routing rules
