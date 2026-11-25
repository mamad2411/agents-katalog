# ContextBridge MCP — AI Skill

Copy this file into your project root and rename it to match your AI tool:
- Claude Code → `CLAUDE.md`
- Cursor, Codex, Copilot, Windsurf, Gemini CLI, Zed → `AGENTS.md`

Then fill in `## Your Project Stack` at the bottom.

---

## Connection

ContextBridge MCP runs as a single SSE server by default: `http://127.0.0.1:8755/sse`
(stdio transport is also supported for clients that require it, but SSE is recommended
so multiple AI clients can share one running server).

**Before using CB:**
1. Start the server using your OS start script in `context_bridge/setup/`
2. Connect your AI tool to `http://127.0.0.1:8755/sse` — see `docs/HOW_TO_SETUP_MCP.md` for per-tool instructions
3. Open a new chat — CB tools are only available after connecting

If CB tools are unavailable, skip CB, answer directly, and warn: "CB is offline — answer is not grounded in codebase context."

---

## Prompt Tags

CB is NOT called automatically. It only fires when the user includes `>>SEARCH:` in their message.

| Tag | What it does |
|---|---|
| `>>SEARCH: <text>` | Triggers CB. Call `search_context_hybrid()` with this exact text. |
| `>>TASK: <text>` | What to do after CB returns. Answer this using the CB result. |
| No tag | Skip CB entirely. Answer from your own knowledge. |

**Rules:**
- `>>SEARCH:` present → call `search_context_hybrid()` with the exact value, never rephrase or shorten it
- `>>SEARCH:` + `>>TASK:` present → send only the `>>SEARCH:` value to CB, then answer `>>TASK:` using the result
- No tag → skip CB, answer directly

**Example:**
```
>>SEARCH: user login session token validation
>>TASK: why does the session expire too early, trace the full flow
```

---

## Tool Notes

Tool names and descriptions are loaded automatically from the MCP server. Two exceptions the server does not state:
- `analyze_context()` — do NOT call manually. It runs automatically inside `search_context_hybrid()`.
- `find_code_locations()` — only available when `enable_code_locations: true` in config.

`record_outcome(event_id, outcome)` — `outcome` must be one of: `"success"`, `"partial"`, `"failed"`. Optional `failure_reason`: `"none"`, `"bad_ranking"`, `"stale_graph"`, `"missing_graph_data"`, `"unclear_query"`, `"too_few_results"`, `"ai_did_not_use_context"`.

`record_outcome` also accepts two optional numeric fields: `used_suggested_files` (how many of CB's suggested files you actually used) and `extra_files_read` (how many files you read beyond what CB suggested). If you can state these honestly, pass them — they make the dashboard's quality signal more accurate. This is entirely optional and up to you/the user; if the user decides not to have the AI record this, CB evaluates the result using its own retrieval-quality signals instead.

**Outcome reporting rules — very important:**
- Only call `record_outcome()` for real CB misses. Do not log `"success"`.
- Record `"partial"` only when CB missed one or more files or symbols that were actually required to complete the task, and you had to read extra files because of that miss.
- Record `"failed"` only when CB missed the needed area badly enough that you could not complete the task from CB's retrieval.
- Do **not** blame CB for AI over-reading. Extra file reads alone do **not** mean `"partial"` or `"failed"`.
- If the AI ignored good CB results, wandered into unrelated files, or hallucinated the need for extra reading, do not record a CB miss. If you must explain the situation, use `failure_reason: "ai_did_not_use_context"` only together with a real `"partial"` or `"failed"` outcome that was still caused by a CB miss.
- Only populate `missed_files` with files that were genuinely required and absent from CB's suggested result.

**How to fill these in:** take the `top_files` list from CB's response for this `event_id`. Count how many of those exact paths you actually opened, read, or edited while completing the task — that number is `used_suggested_files`. Count any other files you opened that were NOT in that list — that number is `extra_files_read`. Base both counts only on files you genuinely touched this task, never guess or round up.

---

## Tool Sequence

1. `>>SEARCH:` fires `search_context_hybrid()` — always first
2. `find_code_locations()` — if exact file / line / symbol is needed after step 1
3. `get_module_summary()` — if a module needs deeper context before editing
4. `record_outcome(event_id, outcome)` — only after task when there is a real CB miss. Use `"partial"` / `"failed"` only for real CB misses, not for AI over-reading.

---

## Usage Rules

- If the AI/client calls `search_context_hybrid()`, don't just describe the problem in a sentence. Include the module/feature name, the concrete symptom, and any specific terms you already know (field names, status values, button labels) as keywords in the query. "Specific terms" means terms already known from the user, product, or UI — not code names the AI should go discover first. If the first result looks weak, run a second, narrower query with more specific known terms instead of one long vague one.
- Use only the files CB suggests — do not read entire source files
- Do not call CB again unless the first result was clearly about the wrong module
- Do not call `analyze_context()` manually — it runs automatically inside `search_context_hybrid()`
- If `analysis.skipped: true` in the response, use the retrieval results directly — ranked files and symbol hits are still valid
- If `is_stale: true` in the response, the index is outdated — tell the user to re-run the setup script to rebuild it
- If CB misses required files, follow up with `find_code_locations()` or `get_graphify_pack()` for targeted lookup, then record the miss using `record_outcome()`
- Code blocks in results are the source of truth — do not infer method names from file names
- Prefer uncertainty over hallucination
- Do not call `record_outcome()` unless CB actually missed required context
- Do not record `"partial"` or `"failed"` unless CB actually missed required context. Extra reading caused by AI caution or drift does not count against CB.

---

## Your Project Stack
- Backend:
- Frontend:
- Database:
- AI pipeline: ContextBridge (retrieval) → analysis stage → your AI (implementation)
