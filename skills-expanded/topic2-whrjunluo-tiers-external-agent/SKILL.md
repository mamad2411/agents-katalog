---
name: external-agent
description: Use when a bounded task needs an external coding-agent CLI or an independent second opinion, including repository research, implementation delegation, and cross-provider review.
---

# External Agent

One unified entry point for handing a bounded task to an external coding-agent CLI.
The **main agent stays the orchestrator and decision-maker**; these agents are
bounded workers whose output is evidence, never the final word.

These are **separate agents** with separate auth, permissions, and behavior — not
different models of one agent. Treat their output as advisory and verify locally.

## Runner (the hands)

Resolve `<plugin-root>` like `dev-workflow`, then:

```bash
python3 <plugin-root>/scripts/external_agent.py \
  --agent <name> --cd "$PWD" --PROMPT "bounded task" \
  [--mode review|delegate] [--format text|json] [--SESSION_ID id] [--context none|git]

python3 <plugin-root>/scripts/external_agent.py \
  --cross-review agy,mimo --cd "$PWD" --context git --format json \
  --PROMPT "review the same frozen artifact"

python3 <plugin-root>/scripts/external_agent.py \
  --cross-review cursor,mimo --review-profile small-fix \
  --cd "$PWD" --context git --format json --PROMPT "review a narrow frozen fix"

python3 <plugin-root>/scripts/external_agent.py \
  --cross-review auto --orchestrator-family openai \
  --review-profile small-fix --progress jsonl \
  --cd "$PWD" --context git --format json --PROMPT "review a narrow frozen fix"
```

- `--mode review` (default): **read-only** posture — independent review / research, no writes.
- `--mode delegate`: **read-write** posture — let the agent implement. **Needs explicit user authorization.**
- `--format text` (default) / `--format json` → `{success, SESSION_ID, agent_messages}`.
- `--SESSION_ID` resumes a prior session (multi-turn); antigravity has no resume.
- `--context git` prepends branch/status/diff to the prompt (for review of current changes).
- `--list` reports installed candidates, provider family, persistent `health_status`, machine-readable `routing_priority`, and `recommended_timeout_seconds`.
- `--cross-review a,b` freezes one prompt/context, computes its SHA-256 and repository fingerprint, and calls every reviewer read-only **in parallel**. Standard profile exits successfully only when at least two known agents from different families return non-empty successful reviews.
- 本 runner 不会自动创建工作流完成门；是否将外部评审设为 `requirements.external_review=true` 由主流程和用户明确选择，未选择时可只使用本地 checklist 收尾。
- `--cross-review auto --orchestrator-family openai` deterministically chooses two installed, healthy, distinct-family reviewers while excluding the orchestrator family. Auto mode also excludes `opencode` while its actual provider family is unknown; use explicit routing only when the operator can verify that provider identity. If fewer than two eligible families exist, it returns structured failure instead of silently weakening the policy.
- `--review-profile small-fix` is explicit opt-in for a workflow-qualified narrow fix. It defaults to 90 seconds per reviewer and stops remaining reviewers after the first valid external success. A one-success report is `success=true`, `quorum=false`, `outcome=degraded`; it is not a full cross-provider quorum.
- `--progress jsonl` (default) writes live lifecycle events to **stderr** while the final text/JSON report remains alone on **stdout** for completion evidence. Use `--progress none` only when a caller does not want live feedback. Events are `cross_review_started`, `review_started`, `review_finished`, `policy_satisfied`, `cross_review_terminated`, and `cross_review_finished`.
- `--fingerprint --cd <repo>` prints the deterministic Git snapshot hash used by the completion gate; workflow state/evidence files are excluded.
- `--timeout N` is an explicit per-agent hard limit. Standard profile uses the provider's persisted recommendation but caps the implicit wait at 600 seconds, then falls back to 600 seconds. An explicit timeout overrides that cap. Small-fix uses 90 seconds when timeout is omitted; health history cannot silently expand that bounded run.
- `--model` only when the user named a model.

## Agent capability matrix (routing)

| agent | family | strong at | default role |
|---|---|---|---|
| `codex` | OpenAI | algorithms, patch diffs, sandbox levels | **execute** |
| `cursor` | multi (GPT/Claude) | repo-aware edits, implementation critique | **execute / review** |
| `grok` | xAI | web search, alternative reasoning | **gather / cross-review** |
| `antigravity` (`agy`) | Google | independent agentic review (Gemini successor) | **gather / review** |
| `mimo` | Xiaomi | China-available, Chinese reasoning | execute / review (fallback) |
| `opencode` | configurable provider | repo-aware execute/review on your own (often free/self-hosted) models | execute / review |
| `kimi` | configurable provider | Kimi Code repo analysis with session resume and structured output | execute / explicit review |
| `gemini` | Google | long context — **legacy: individual tiers disabled, migrate to `antigravity`** | (enterprise only) |

Kimi review is capability-gated: the installed CLI must expose v2 `--agent-file`, and the runner supplies a profile limited to `Read/Grep/Glob`. Kimi is `auto_eligible=false` and never enters automatic cross-review selection because Kimi Code can use configurable providers; explicit review remains available after the operator verifies provider provenance. Delegate mode does not use the read-only profile and still requires explicit write authorization.

> The `gemini` CLI returns `IneligibleTierError` for free / Pro / Ultra accounts since
> the June 2026 migration. Use `antigravity` (`agy`) for Google-family work. The
> `gemini` adapter is kept only for enterprise Code Assist users who still have access.

> ⚠️ **调用返回拒绝/空产出时，优先检查调用方式，而不是归因到具体 agent。**
> 对长 prompt、敏感领域或保真验收要求高的任务，先收敛输入范围、拆分上下文、降低无关敏感表述；
> 若仍返回拒绝/空产出，切换执行路径或换用更适合当前约束的 agent，不要反复重试同一 prompt。

## Routing policy (the brain)

Classify the sub-task, then pick mode + agent:

- **Gather info / research** → `--mode review`. Web/external facts → `grok`; large codebase/doc digest → `antigravity`. Read-only.
- **Execute / implement** → `--mode delegate` (needs user OK). Repo edits → `cursor` or `codex`; pure algorithm → `codex`; own/free/self-hosted models → `opencode`; China-available execution → `mimo`. If a call returns refusal/empty output, adjust the invocation or switch execution path instead of repeating the same prompt. Read-write, scoped to `--cd`.
- **Cross-review** → `--cross-review <a>,<b>`, using **≥2 external CLI agents of different families** in parallel. Prefer installed reviewers with `routing_priority=normal` (normally `grok`, `cursor`, or `mimo`); use `antigravity`/`agy` after healthy candidates when it is marked `slow` or `degraded`, unless the user explicitly names it. Use `codex` as one reviewer only when the main orchestrator is not Codex. Installed binaries are only candidates: failed auth, timeout, empty output, aliases of one agent, or one successful family produce `quorum=false`. `small-fix` may accept that one family only through its explicit degraded policy. A standard `outcome=failed` report can be referenced later by a host-owned platform multi-model fallback, but this runner never weakens external quorum itself. The main agent reconciles every returned result.

Before routing, run `--list` and only pick installed agents. Health persists globally under `$DEV_WORKFLOW_DATA/external-agent-health.json` (default `~/.dev-workflow/`): the first timeout marks the provider `slow` and doubles its recommendation; any current failure streak sets `routing_priority=deprioritized`; two consecutive failures mark it `degraded`. A later success clears the consecutive-failure streak but retains `slow` history. Prefer healthy candidates when equivalent, but never silently skip a named or required provider: report the marker and use its recommendation or an explicit timeout. If the user names an agent, use it; if they just say "external agent", ask which unless context makes it obvious.

Every cross-review report records `review_profile`, `policy`, `outcome`, `created_at`, `finished_at`, total duration, and reviewer lifecycle status/duration. Normal failures use `outcome=failed`; SIGINT/SIGTERM uses `outcome=terminated` with `termination_reason=user_interrupt`. A cancelled, failed, or terminated reviewer is evidence, never a successful opinion. The JSONL stream is observability only: progress events never weaken standard quorum or turn a partial result into success. Waiting updates belong to the orchestrator and should only be emitted when one of these statuses changes; a user stop request terminates the runner, preserves terminated evidence, and stops further review gates rather than leaving work in the background.

## Host-owned platform fallback

`external_agent.py` remains the strict external provider runner. It preserves genuine external failure evidence (`success=false`, `quorum=false`, `outcome=failed`) and never silently launches platform agents or writes `tiers.platform-review/v1`. If the host supports two distinct model IDs and the user has authorized platform subagents, the host may reference that failed report, launch two read-only platform reviewers with distinct roles, adjudicate their structured findings, and validate the resulting platform evidence with `scripts/platform_review_contract.py`.

An external report with `outcome=terminated`, successful external quorum, or an already-successful small-fix degraded policy is not eligible. The host must report the provenance as `external cross-review failed; platform multi-model fallback passed`; it must never call this external quorum.

## Orchestration

```
gather(grok/antigravity, review) → execute(codex/cursor, delegate)
  → --cross-review(2 different-family successes, one artifact hash) → main agent reconciles + verifies
```

## Guardrails

- Read-only external review requires task/workflow authorization to send the scoped artifact; announce before sending repository context with `--context git`. Cross-review children inherit the parent permission mode. `--mode delegate` additionally needs explicit write authorization and stays inside `--cd`.
- Never include secrets, credentials, private keys, `.env` contents, or unrelated files.
- Output is evidence, not authority — verify findings locally; the main agent decides.
- **委派不降级流程**：judging level, comprehension gate, TDD, evidence gates, and final verification stay owned by `dev-workflow`.
- Do not silently fall back to another agent. If auth is missing, ask the user to log that agent in once.
