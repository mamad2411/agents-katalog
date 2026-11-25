---
name: loot-validation
description: "Use when testing harvested keys/OAuth tokens for live gen."
tags: [loot, validation, api-keys, oauth, codex, grok, antigravity, openrouter]
version: 1.0.0
---

# Loot Validation

Class task: take a pile of harvested credentials and produce a verdict per pool — LIVE (with real generate proof), LIST-ONLY (valid but no generate rights), or DEAD — plus latency/RPM/TPM numbers for the live ones.

## Procedure (in order)

1. **Normalize the pool before testing.** Dedupe OAuth connections by their `id` field across panel dumps; group apikey credentials by the connection's `baseUrl`, NEVER by key prefix — `sk-` is shared by dozens of aggregator platforms and each validates on its own host. Sort OAuth pools by `expiresAt` descending and test the freshest first; a dead-freshest pool means the whole pool is dead.
2. **Validate in layers; only the last layer counts.** Token mint → models list → real generate call. Models-list success alone is NOT value — report it as LIST-ONLY. 402 on generate = valid key, zero balance. A working models list plus 403 on generate can be egress-IP geo-blocking — retest from a second VPS before declaring the pool dead.
3. **Read the error body before changing anything.** A fast 400 carrying a JSON `detail` field means auth ALREADY passed and only the request shape is wrong (stream flag, model name, encoding) — fix the request, don't chase credentials. 401 = auth rejected; 403 = permission/license; 402 = zero balance; 429 = lockout/rate.
4. **Retry auth-layer failures with corrected mechanics, not more credentials.** Common fixes: form-encode OAuth token refreshes (JSON bodies fail with misleading errors), set mandatory stream flags, use the provider's real public client_id, find the token endpoint via OIDC discovery instead of guessing.
5. **Measure, don't estimate.** Per live pool report: TTFB (first stream delta), wall time, stream tok/s (output_tokens/seconds), burst RPM (sequential same-credential requests until 429 or 20 straight successes), TPM ceiling via one long-output request. Run 5 distinct credentials in parallel threads before extrapolating pool capacity — per-account limits don't divide into pool throughput.
6. **Report as a verdict table**: pool → count → status (LIVE/LIST-ONLY/DEAD) → models that generate → numbers → priority ranking for exploitation.

## Always-On Rules

- Filter candidates on `testStatus: active` but treat it as the panel's last-known state, not proof — the live generate call is the only verdict, on the exact model you plan to route. Codex: `active` includes free-plan accounts that generate on basic codex models but 400 on premium ones — gate the pool on `providerSpecificData.chatgptPlanType` ∈ {plus, prolite} first (premium ≈ 10% of a farmed dump).
- Sample 8–10 keys per baseUrl before extrapolating a pool's live/dead split; single-key results mislead.
- Never reuse OAuth access tokens from a dump — mint fresh immediately before testing; they expire in ~1h (Google) to ~6h (x.ai).
- A pool that refreshes 10/10 can still be 100% dead when the entitlement layer is revoked (e.g., Google Code Assist licenses) — the license check is the real gate, not token minting.
- When the freshest OAuth accounts all return `invalid_grant`, write the pool off; older tokens are strictly worse.

## Provider Quirks

Per-provider endpoint recipes (codex/ChatGPT, grok-cli/x.ai, antigravity/Gemini, openrouter-class aggregators): see `references/provider-endpoints.md`.
