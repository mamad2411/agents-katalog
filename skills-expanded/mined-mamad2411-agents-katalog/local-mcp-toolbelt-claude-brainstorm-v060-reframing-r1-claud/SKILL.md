# R1 — Claude (claude-opus-4-7), reframing decision

## 1. Concrete v0.6.0 architecture

**Synthesis E (B + C + partial D)** — keep MCP minimal, weaponize Bash, expose thinking per-tool.

API surface:
```
enqueue-job(tool, args, opts?: { thinking?: 'on'|'off'|'default' })
  → { job_id, result_path, wait_command, est_ms }

# wait_command is a ready-to-paste bash one-liner:
#   "while [ ! -f /path/to/<id>.json ]; do sleep 5; done; cat /path/to/<id>.json"
# Caller (Claude) passes this to its own Bash tool — 10min cap >> any MLX task.

read_job_result(job_id) → result          # MCP-side path, instant once file exists
list_jobs() → [{job_id, status, age_s}]   # optional; small surface
```

Per-tool `thinking` flag is the API for the v0.5.x → v0.6.0 quality lift.
Default per-tool (set in `server.ts` registry, not passed by caller):
- `classify`, `extract`, `transform`, `diff-semantic-index`: **`on`** (reasoning helps)
- `summarize`, `summarize-long`, `summarize-long-chunked`: **`off`** (prose loses 0.5 in eval data)

Trade-off: dual-path (MCP for short / structured-output / cached results; Bash for long thinking-on runs). Caller picks via `wait_command` vs `read_job_result`.

Main risk: Bash tool's 10min cap is an Anthropic product decision; could shrink. Mitigation: monitor; fall back to in-MCP `check_progress` polling if it ever does.

Cost: **S–M**. v0.3.0 job worker is reusable. New: `wait_command` string generation (~5 LOC), per-tool thinking default registry (~30 LOC), env-var override (`OMCP_THINKING_<TOOL>=on|off`).

## 2. Challenge B (bash-wait): brittle or sound?

**Structurally sound, not brittle.** Anthropic ships `Bash` with an explicit 10min cap *because* shell ops are expected to run long (builds, tests, long-poll). Removing that would break vastly more than our use case. The brittleness, if any, is shell-portability of `while [ ! -f ]; do sleep 5; done; cat` — use POSIX-only subset, no `[[` or zsh-isms, and it's safe across `/bin/sh`, `bash`, `zsh`.

## 3. Challenge thinking-everywhere

**Signal, not noise.** Direction is consistent with Qwen3 model card behavior: reasoning models on prose tasks tend to over-generate and split structure, hurting summarization scores. Sample is small but two tasks moved the same way (summarize-long −1.0, classify −0.7 on judgable rows). v0.6.0 should expose per-tool defaults; auto-mode (let model decide) requires more eval data and stays out of scope.

## 4. Prediction

Final v0.6.0 will be **synthesis B + C** (bash-wait + per-tool thinking). A (filesystem + `check_progress`) gets dropped or reduced to a thin fallback — `wait_command` makes a dedicated progress MCP tool redundant for the long-path. The cleaner architecture won't have both.

## Caveat (epistemic humility)

My prior R1 in 2026-05-11's morning brainstorm ranked Copilot's two-tier fast-approx first; the thinking eval data showed that "fast = quality compromise" isn't unanimous and the two-tier framing maps onto "no-think vs think" rather than "small vs big model". I likely have a similar blind spot here — please challenge in R2.
