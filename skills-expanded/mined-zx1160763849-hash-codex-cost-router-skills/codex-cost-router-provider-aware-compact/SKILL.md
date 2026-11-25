---
name: codex-cost-router-provider-aware-compact
description: Compact-first provider-aware Codex cost router. Use before coding, file edits, project reading, tool calls, debugging, deployment, or high-cost reasoning when model/provider choice matters. It maps manually provided models to L0-L4 tiers, classifies tasks as A-E, warns about provider risk, avoids reading API keys/base_url/local credentials, never auto-fetches model lists, and defaults to concise Compact Route output.
---

# Codex Cost Router Provider-Aware Compact

## Core

v2.1 compact-first cost router for Codex tasks.

Default: evaluate first, do not execute. Route by task complexity, model tier, provider risk, permissions, and token cost.

Never read API Key, base_url, local credentials, provider configs, environment secrets, or model lists. Never request, crawl, or verify models automatically.

Users must manually provide available providers/models, or use GPT-tier fallback.

## Output Modes

Default to Compact Mode.

Use Standard Mode only when the user asks for more detail, the task is multi-file, provider/model info is incomplete, provider is unclear but not high risk, L2/L3 is recommended, or rationale is needed.

Use Full Mode only for high-risk work: database, payment, auth, API Key, user data, deployment, production, unknown proxy, shared API, low-price proxy, unclear model authenticity, L4 recommendation, first use with no model environment, or explicit full analysis request.

Read `references/compact-output-rules.md` when mode choice is unclear.

## Compact Mode Contract

Keep normal output within 8 lines and about 250 Chinese characters.

Compact compresses analysis only. It must not remove the executable next-step prompt.

Route body must include:

- Complexity A-E
- Capability L0-L4
- Recommended model or GPT-tier fallback
- One-line strategy covering reasoning, speed, and permissions
- Token-saving advice
- Safety line
- Next-step instruction

Every output mode must end with:

````md
【下一步执行 Prompt】

```text
...
```
````

The next-step prompt must be directly copyable into Codex and include task goal, scope limits, whether file edits are allowed, whether commands are allowed, whether whole-project scans are allowed, whether dependency installation is allowed, and final output requirements.

If the task is complex or location is unclear, make the next-step prompt read-only analysis first. If the task is high risk, the prompt must forbid file edits, command execution, deployment, database migration, payment/auth changes, and reading real API keys/tokens/cookies/passwords.

## Model Rules

If user provides model list: map models to L0-L4 candidates. Do not claim third-party models equal GPT models.

If user uses official GPT: write `模型环境：官方 GPT，已知`; do not repeat long provider warnings.

If no model list: show one short notice: `为保护 API Key 和本地配置安全，本 Skill 不会自动读取或请求你的模型列表。请手动提供可用模型清单；如果跳过，我将按 GPT 能力等级给出参考。`

GPT fallback:

- L1: GPT-5.4-Mini level
- L2: GPT-5.4 level
- L3: GPT-5.5 medium-high reasoning level
- L4: GPT-5.5 high/ultra-high reasoning level

## Safety Compression

For normal tasks, write only: `安全：不读 key/base_url；无敏感接口风险。`

Expand safety only for API Key, base_url, user data, database, payment, auth, deployment, production, unknown proxy, shared API, low-price proxy, or unclear model authenticity.

## References

Load only when needed:

- `references/compact-output-rules.md`
- `references/model-profile-rules.md`
- `references/model-tier-map.md`
- `references/provider-aware-decision-matrix.md`
- `references/provider-risk-checklist.md`
- `references/task-taxonomy.md`
- `references/output-blueprint.md`
- `references/cost-saving-rules.md`
- `references/risk-checklist.md`
- `references/fallback-strategy.md`
- `references/execution-prompt-templates.md`
