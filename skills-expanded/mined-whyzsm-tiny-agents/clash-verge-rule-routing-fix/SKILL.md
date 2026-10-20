---
name: clash-verge-rule-routing-fix
description: Use when the user asks to fix Clash Verge routing on this Mac, especially "直接帮我改一下", "给我个完全的", or "国内地址不走代理，国外的走代理" for OpenAI, Codex provider, Google/Gemini, Yuque, or Linux.do.
argument-hint: "[target-service-or-goal]"
disable-model-invocation: true
user-invocable: false
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Clash Verge rule routing fix

## When to use

Use this when:
1. The task is on the user's macOS home environment with Clash Verge Rev / Mihomo.
2. The user wants a direct routing fix, a complete copyable YAML block, or a targeted change for OpenAI/ChatGPT/Codex provider/Google/Gemini/Yuque/domestic-vs-foreign routing.
3. You need to distinguish bad node behavior from bad rule order.

Do not use this when:
1. The task is not on this Mac or not using the same Clash Verge Rev layout.
2. The user only wants a status check; use `skills/macos-clash-atrust-network-check/SKILL.md` first.
3. The request is really about editing aTrust internals rather than Clash routing.

## Inputs / context to gather

1. Confirm the active proxy port in this session with `scutil --proxy` and/or current evidence. This memory set has seen both `127.0.0.1:7890` and `127.0.0.1:7897`.
2. Identify the exact traffic goal:
   - OpenAI / ChatGPT should use `🔰 选择节点`
   - Codex provider `39.170.58.150:8888` should be `DIRECT`
   - Domestic services like Yuque / WPS / QQ / WeChat / Apple China should be `DIRECT`
   - Google / Gemini should use `🔰 选择节点`
3. Find the persistent profile file(s) under `~/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/profiles/`, especially `Merge.yaml` or the current generated profile such as `r4jYYhuWOj2w.yaml`.
4. Locate runtime evidence:
   - `clash-verge.yaml`
   - `/tmp/verge/verge-mihomo.sock`
   - `logs/service/service_latest.log`

## Procedure

1. Inspect the current rule placement before editing.
   - Read the relevant `profiles/*.yaml` file(s).
   - Check whether explicit direct/proxy rules already exist and whether they are in `prepend` or are being shadowed by a subscription `MATCH`.
2. Decide the minimal rule set needed.
   - For Codex provider, prefer `IP-CIDR,39.170.58.150/32,DIRECT,no-resolve`.
   - For OpenAI/ChatGPT family, include `openai.com`, `chatgpt.com`, `oaistatic.com`, `oaiusercontent.com`, and optionally `chatgpt.livekit.cloud`.
   - For Google/Gemini, include `google.com`, `googleapis.com`, `gstatic.com`, `googleusercontent.com`, `gvt1.com`, `gvt2.com`, `developers.google.com`, `gemini.google.com`.
   - For domestic direct routing, include `yuque.com`, `kdocs.cn`, `wps.cn`, `qq.com`, `weixin.qq.com`, `icloud.com.cn`, and related business domains when relevant.
3. Put explicit routing in `prepend`, not `append`.
   - Keep direct or proxy rules that must beat `MATCH` near the top.
   - Avoid adding a new `append: MATCH` if the subscription already provides a catch-all.
4. Provide the change in the user’s preferred form.
   - If you are editing locally, update the persistent profile file with the minimal validated change set.
   - If the user wants a copyable config, return a complete syntax-safe block rather than a partial snippet.
5. Reload or re-read the runtime config if the environment supports it.
   - Verify the edited rules appear in `clash-verge.yaml`.
   - If node health is in question, inspect `/proxies` through `/tmp/verge/verge-mihomo.sock` and note the current `🔰 选择节点`.
6. Validate with destination-specific checks.
   - `api.openai.com/v1/models` through the proxy should return a fast `401 Unauthorized`.
   - `39.170.58.150:8888` should return `401` quickly and logs should show `match IPCIDR(39.170.58.150/32) using DIRECT`.
   - Yuque should show `match DomainSuffix(yuque.com) using DIRECT` and ideally return `200`.
   - OpenAI/ChatGPT/Google should show `using 🔰 选择节点`.

## Efficiency plan

1. Start with the user’s routing goal and inspect only the one or two profile files that actually feed the current runtime config.
2. Prefer log validation over broad retesting; Mihomo logs answer "which rule won?" faster than repeated curl experiments.
3. Use a small proven rule set first, then expand only if the user names more services.
4. Stop once the logs show the intended rule match and the destination-specific success criterion is met.

## Pitfalls and fixes

- Rules in `append` do nothing
  - Likely cause: the subscription’s existing `MATCH` catches traffic first.
  - Fix: move explicit direct/proxy rules into `prepend`.
- The YAML "保存不了，报错了"
  - Likely cause: incomplete snippet or invalid structure for this profile layout.
  - Fix: return a complete copyable block with minimal validated changes.
- OpenAI still looks broken after the edit
  - Likely cause: you used the wrong success criterion or the wrong port/current profile.
  - Fix: verify the active proxy port, then check for a fast `401` from `api.openai.com/v1/models` and confirm the Mihomo log shows `match DomainSuffix(openai.com) using 🔰 选择节点`.
- Codex provider still feels slow even though the provider IP is reachable
  - Likely cause: the provider endpoint is being sent through the proxy instead of `DIRECT`.
  - Fix: confirm `IP-CIDR,39.170.58.150/32,DIRECT,no-resolve` wins in logs.
- Node problems and rule problems are getting mixed together
  - Likely cause: a healthy port or successful reload is being mistaken for healthy routing.
  - Fix: validate both rule match and node quality; inspect `/proxies` if requests still stall.

## Verification checklist

1. You identified the active proxy port and current profile file before editing.
2. Any must-win routing rules were placed in `prepend`.
3. You preserved the domestic direct / foreign proxy intent when that was the user’s goal.
4. You validated with the right success signal for the target service, not a generic HTTP check.
5. If you claimed the fix persists, you updated the persistent profile file rather than only the runtime config.
