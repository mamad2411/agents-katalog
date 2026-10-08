---
name: "ai-cross-platform-token-sync"
description: "Sync caches, compressed tokens, and savings ACROSS ALL 21 AI platforms. 1x work = 21x savings. Share codon tables, block hashes, forever-cache, skill indices. Invoke once per session."
---

# 🔗 AI CROSS-PLATFORM TOKEN SYNC — 21× LEVERAGE
**Leverage: 1 compression/ cache on Platform A → Auto-used by all 20 other platforms**
**Run: ONCE at session START (before any LLM calls)**

## SYNCED RESOURCES (Instant sharing across ALL 21 platforms)
```
SHARED GLOBAL STATE DIR: ~/.agents/shared_state/
├── dna_codon_table.json          # 1800 entry codon table — build once, all platforms decode
├── dna_block_cache_global.json   # Repeated block hashes — seen once = all platforms skip
├── forever_cache_global.jsonl    # SHA256(prompt)→response — any platform cache hit = all benefit
├── skill_index_global.json       # 8,446 skill locations + keyword map — single load
├── tool_result_cache.jsonl       # MCP/tool results (sha256(cmd+args)→output) — run once
├── budget_state.json             # Cross-platform token budget tracking
└── dedup_hash_index.json         # SHA256(paragraph)→turn_id pointer
```

## PLATFORM SYNC HOOKS (Auto-register at init)
```
PLATFORMS SYNCED (21 TOTAL):
.codex .codebuddy .cline .claude .hermes .aider .goose .kiro .qwen .gemini
.orca .continue .copilot .codeium .windsurf .dolphin .mistral .openclaude
.opencode .devin .config/goose

SYNC PROTOCOL — file watcher + atomic writes:
1. EVERY platform writes to its own platform file:
   ~/.agents/shared_state/platform_cache/${PLATFORM_NAME}.jsonl
2. GLOBAL MERGE runs every 30 seconds OR on 10+ new entries:
   - Union all platform caches
   - Dedupe by SHA256 key
   - Write back to global files (atomic rename via .tmp)
3. EVERY platform RELOADS global files:
   - BEFORE: every prompt assembly
   - AFTER: every tool execution
   - Cost: <5ms (files small, cached in RAM)
```

## SPECIFIC SYNC SCENARIOS

### Scenario 1: Codex runs command → Aider/Cline get free cache hit
```
1. Codex runs: `ls ~/.agents/skills-catalog/ | wc -l` → result "8446"
2. Codex writes: tool_result_cache entry [sha256("ls|wc -l"), "8446"]
3. 12s later, Aider needs same info → checks global cache → HIT!
   RESULT: 0 tokens spent on tool, 0 characters in context
   SAVINGS: ~400 tokens + 1.5s exec time × 20 other platforms
```

### Scenario 2: Hermes compresses prompt → all platforms decode same
```
1. Hermes processes 50,000 char doc → DNA compression = 50:1 ratio
2. Block hashes written to dna_block_cache_global.json
3. Next minute, Goose needs same doc → sees hashes already exist → uses pointers
   RESULT: 98% compression without re-encoding + cross-platform consistency
```

### Scenario 3: Cache hit sharing (BIGGEST savings)
```
1. Any platform gets prompt "how to setup lazy_load in hermes config.yaml"
2. Response generated (cost: ~800 tokens) → written to forever_cache_global
3. Next 20 platforms get same/similar prompt (Jaccard ≥0.7) → CACHE HIT
   RESULT: 20 × 800 tokens = 16,000 tokens SAVED
   LEVERAGE FACTOR: 21× (1× cost → 21× benefit)
```

## BUDGET ENFORCEMENT (CROSS-PLATFORM TOKEN CAP)
```
GLOBAL SESSION BUDGET (shared across ALL 21 platforms):
  SOFT CAP: 5000 tokens total (all platforms combined) → warning at 70%
  HARD CAP: 8000 tokens → ALL platforms auto-enter NUCLEAR PRUNE mode
  DAILY CAP: 100,000 tokens → next day reset

BUDGET TRACKER writes EVERY LLM call:
{platform: "hermes", model: "mistral-large", prompt_t: 200, comp_t: 80, ts: 1234567890}

If ANY platform alone uses >40% of remaining budget:
  → auto-escalate to TINY model tier for THAT platform
  → force nuclear pruner MAX aggression
```

## FIRST RUN SETUP
```bash
mkdir -p ~/.agents/shared_state/platform_cache
for p in codex codebuddy cline claude hermes aider goose kiro qwen gemini \
         orca continue copilot codeium windsurf dolphin mistral openclaude \
         opencode devin config_goose; do
  touch ~/.agents/shared_state/platform_cache/${p}.jsonl
done
# Initialize empty global files if missing
for f in dna_codon_table dna_block_cache_global forever_cache_global \
         skill_index_global tool_result_cache budget_state dedup_hash_index; do
  [ -f "~/.agents/shared_state/$f.json" ] || echo "{}" > "~/.agents/shared_state/$f.json"
  [ -f "~/.agents/shared_state/$f.jsonl" ] || : > "~/.agents/shared_state/$f.jsonl"
done
```
