---
name: "token-zero-waste-hooks"
description: "8 interceptor hooks at EVERY stack layer (MCP, tool, memory, skill, prompt, output) to ELIMINATE token waste at source. Register ONCE at session init."
---

# 🪝 TOKEN ZERO-WASTE HOOKS — 8-LAYER INTERCEPTION
**Intercept at: MCP Server → Tool Executor → Memory → Skill Loader → Prompt Builder → LLM API → Output Renderer → History Persister**
**Register: ONCE at session START. Auto-enabled across ALL platforms.**

---

## HOOK 1/8 — MCP SERVER INTERCEPTOR (OUTPUT ≤ 800 chars MAX)
```
TRIGGER: mcp_server.onResponse()
1. Cap EACH MCP tool output at 800 chars
2. Remove ALL: debug logs, env vars, stack traces, timestamps >1ms precision
3. JSON: Strip all null, empty string, and duplicate keys
4. Arrays >5 items → [first3, "...", last1, "total=N"]
5. NEVER pass raw binary/base64 through → write to /tmp & return path only
ENFORCEMENT: Hard truncate + warning tag if violated: `[TRUNCATED_800C]`
```

## HOOK 2/8 — TOOL EXECUTOR FILTER
```
TRIGGER: tool.run.before() AND tool.run.after()
BEFORE:
  - Delete arguments that match default values (no need to repeat)
  - Collapse file paths: $HOME→~, redundant dir separators
  - Cap command length display at 200 chars (full cmd only in logs, NOT payload)
AFTER:
  - Success: return only `[tool_name][OK] <1-line result>`
  - Fail: return only `[tool_name][FAIL:ERROR_CODE] <1-line cause>` (≤120 chars)
  - NEVER include full stdout/stderr UNLESS explicitly requested via `DEBUG=1` flag
```

## HOOK 3/8 — MEMORY WRITE THROTTLE
```
TRIGGER: memory.save()
1. SKIP saving:
   - Greetings, filler, "ok", "thanks", "got it" turns
   - Turns with NO new info (just acknowledgments)
   - Tool outputs already cached (hash match)
2. COMPRESS before save: JSON-minify + remove whitespace
3. MAX 1 turn saved per 3 user messages. Older turns → auto-prune (not saved)
4. Memory file MAX size: 64KB. If exceeded → flush oldest 50% to cold storage /tmp/mem_cold/
```

## HOOK 4/8 — SKILL LOADER PAGINATION
```
TRIGGER: skill.load(name)
1. LAZY LOAD: Load ONLY lines MATCHING current intent keywords (not entire SKILL.md)
2. SKILL.md sections:
   - Frontmatter: always load (≤200 chars)
   - Description: load if trigger criteria match
   - Code blocks: load ONLY if tool being invoked matches
   - Examples: NEVER load unless user asks "show example"
3. Cache loaded skill fragments by keyword for 24h
4. TOTAL loaded skills per turn: ≤3. Any additional → defer (return "deferred: skill X available on demand")
```

## HOOK 5/8 — PROMPT BUILDER DEDUPLICATOR
```
TRIGGER: prompt.assemble()
1. HASH DEDUP: SHA256 each paragraph. If hash seen before in this session → replace with `[REF:#N]` (pointer to turn N)
2. SYSTEM PROMPT DEDUP: If platform already injects base system → NEVER duplicate agent system rules (cross-check keywords)
3. FILE CONTENT DEDUP: Same file read twice → reference first read hash, not full content again
```

## HOOK 6/8 — LLM API REQUEST THROTTLE
```
TRIGGER: llm.send.before()
1. BATCH CHECK: If 3+ similar requests in <60s → batch into 1 request
2. CACHE FOREVER: SHA256(prompt) → check Redis/local cache. HIT = RETURN CACHED (0 tokens!)
3. MIN TOKENS: Set max_tokens = min(default, estimated_required_tokens + 50 buffer)
4. DEFAULT: max_tokens = 100. Only increase IF: code generation requested OR user said "long answer"
```

## HOOK 7/8 — OUTPUT RENDERER MINIFIER
```
TRIGGER: response.render.before(user_sees)
1. STRIP: All "thinking" tags, internal chain-of-thought (≤10% unless user asks verbose)
2. COLLAPSE: Multi-line bullets → 1 line if <8 words each
3. CAP DEFAULT: 150 words. Cap code blocks to ≤40 lines unless user requested "full code"
4. UNICODE: Replace emoji with ASCII alternatives (saves 2-4 bytes each: 🔥→[FIRE], ✅→[OK])
```

## HOOK 8/8 — HISTORY PERSISTER PRUNER
```
TRIGGER: history.flush()
1. Only persist: turn 0 + last 6 turns. Everything older → flush to cold storage (NOT synced to LLM context)
2. Strip: All tool outputs from persisted turns (keep only tool success/fail 1-liners)
3. Compress: JSON minify + gzip
4. MAX history.json size: 32KB. If exceeded → rollover monthly archive
```

---

## REGISTRATION (ALL PLATFORMS, ONCE PER SESSION)
```bash
# Check if hooks already registered
if [ ! -f ~/.agents/hooks_registered_$$.pid ]; then
  register-hook --layer=mcp --name=output-cap --priority=0
  register-hook --layer=tool --name=result-filter --priority=0
  register-hook --layer=memory --name=save-throttle --priority=0
  register-hook --layer=skill --name=pagination-loader --priority=0
  register-hook --layer=prompt --name=dedup-builder --priority=0
  register-hook --layer=llm --name=request-throttle --priority=0
  register-hook --layer=output --name=renderer-minifier --priority=0
  register-hook --layer=history --name=persist-pruner --priority=0
  touch ~/.agents/hooks_registered_$$.pid
fi
```

## TELEMETRY (OPTIONAL, OFF BY DEFAULT)
Track savings per hook layer to `~/.agents/hook_savings.jsonl`:
```json
{"hook":"mcp_output_cap","saved_chars":85000,"calls":42,"avg_saved":2023}
```
