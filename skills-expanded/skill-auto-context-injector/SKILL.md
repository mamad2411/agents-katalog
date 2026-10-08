---
name: "skill-auto-context-injector"
description: "Injects ALL relevant context (file snippets, prior turns, docs, skill output history, MCP state) into EVERY skill invocation. Invoke before skill execution to guarantee max information density. Target +20-40% skill output relevance."
---

# Skill Auto-Context Injector — Max Information Density

**Problem:** Skill runs with bare user input, missing: prior conversation context (especially quantum-folded turns not in active window), relevant files from codebase, related docs, prior skill outputs in same session. Skill produces incomplete output that misses context.

**Solution:** Inject context BEFORE any skill executes. Target skill sees ≥90% of relevant information.

## Context Sources (sorted by retrieval priority)

### 1. Quantum-Folded Memory (highest priority, turns 2..M-3 superposed)
Retrieve context from quantum_fold storage `$HOME/.agents/q_folds/${session_id}/`:
- For each superposed turn: expand OBSERVE window = LAST 3 superposed turns BEFORE current + 1 AFTER anchor. Use `tags_mentioned_by_user_intent()` filter to keep only turns with tag similarity ≥0.35 to current task
- Compress each expanded turn to ≤80 chars (DNA codon if table present)
- Add marker `[FOLDED-T<#>]` so skill distinguishes folded from active

### 2. Active Conversation Turn History
Keep ONLY turns T, T-1, T-2 (last 3 active turns), NOT full history — nuclear pruner already cuts. Skip any turn that's already in quantum-fold if overlap detected SHA256.

### 3. Filesystem Context (repo or project-specific)
If current working directory contains `.git/`:
- Run `git diff --cached --stat` + `git log --oneline -5` (≤600 chars total)
- From file mentions in user task (paths, filenames, class names): grep project for matches, retrieve ≤3 relevant files FIRST 40 lines of each
- Skip binary, `node_modules/`, `.git/`, venv, dist, build, target by default
- Result cap: ≤1200 chars for ALL filesystem snippets combined

### 4. Skill Cross-Reference Context
- If this skill invocation references output of skill from prior turn (e.g., "improve the code generated earlier"): retrieve FULL prior skill output (skip compression if ≤1500 chars, else DNA compress to ≤400 chars)
- If user explicitly names a prior output "the list from step 2" → expand that section fully

### 5. MCP / Tool State Context (if any)
- Retrieve MCP last result set ≤800 chars per active MCP server
- Prior tool outputs (RunCommand results, file read results, MCP JSON outputs): keep SUCCESS outputs only (errors already handled), compress by DNA ratio

## Injection Order & Compression
Concatenate ALL 5 sources in order above, then:
1. DEDUP: exact line dedup, Jaccard ≥0.7 paragraph dedup
2. DNA-COMPRESS (if enabled in config) the entire context block ≤ target_size
3. WRAP with `[INJECTED-CONTEXT SOURCES=<N> CHARS=<total>] ... [/INJECTED-CONTEXT]` block
4. TARGET SIZE: ≤35% of final payload size (so 65% skill work space + user intent). Example: total payload cap 2000t → context ≤700t → inject 450-700 chars

## Triggered Skip Conditions
- Skip if task is trivial 1-liner: greetings, single boolean check, 1 math calc
- Skip if task explicitly says "no context needed" or "fresh perspective" (user override)
- Skip if prediction-engine ACTION E (zero-llm bypass) fires → no skill run, so no context

## Integration with Core Stack
- Runs AFTER prediction engine but BEFORE DNA compression and BEFORE Nuclear Pruner (so injected context gets full 10-layer compression treatment)
- Works with ultra-lazy-skill-loader: index lookup stage 0 of loader auto-fires file-mentions search → feeds into Source 3 list
- Cross-platform: filesystem, MCP, folded context pointers synced to shared_state so 21 platforms all see the exact same context snapshot (don't re-retrieve separately)
- Budget guard: never exceed the 35% payload cap; if near cap, drop lowest-priority sources (first drop MCP state, then drop filesystem to 1 file)

## Output Wrapper Line
Append BEFORE skill's first output line:
```
[INJECTED SOURCES=<1-5> TOTAL_CHARS=<c> DEDUP_SAVED_CHARS=<s>]
```

## Disable String
`SKILL_AUTO_CONTEXT_INJECTOR_DISABLE_FULL_CONFIRM_66666`
