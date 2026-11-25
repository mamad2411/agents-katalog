---
name: gateway-usage
description: Check Cornell AI Gateway (LiteLLM) key spend and remaining budget from live response headers. Use when asked about API usage, gateway spend, cost, or remaining budget.
---

# Cornell AI Gateway usage check

Use this skill whenever a user asks about their Cornell AI Gateway (LiteLLM, `api.ai.it.cornell.edu`) spend, budget, or remaining usage on their virtual key.

## What this skill does

Run the bundled `scripts/usage.sh`, which:

1. Resolves the gateway key from a 4-source order (env, then macOS Keychain, then `cornell-ai-helper` config.toml, then Cowork plugin mount), so one file works across the Claude Code CLI, a managed Mac, and the Cowork sandbox.
2. Makes one cheap 1-token completion call to capture the live `x-litellm-*` response headers (spend, max budget, per-call cost, gateway version).
3. Attempts `GET /key/info` as a bonus (some keys may have broader access), but expects and handles a 403 gracefully. On the Cornell gateway, normal end-user keys are restricted to `llm_api_routes` only and cannot call `/key/info`, `/user/info`, or `/spend/logs`. Header data is the primary and usually only source.
4. Prints a clean summary: spend to date, max budget, computed remaining budget, this check's own cost, TPM/RPM limits if present, and the standing billing caveats (flat $0.002/request fee, $10/mo free tier is per TEAM not per key, 90-day key expiry, midnight-UTC reset cadence).

## Key-safety rules (do not violate)

The whole point of this skill is that the key stays inside `usage.sh` and never reaches the chat transcript. To keep it that way:

- **Only** invoke the skill by running the bundled script. Let the script resolve the key internally.
- **Never** run your own `curl` with the key inline, **never** `echo`/`grep`/`printf` the raw key value, and **never** pass the key as `ANTHROPIC_AUTH_TOKEN="sk-..." ...` inline in a command. Any of those writes the live credential into the transcript permanently.
- The script already truncates to the last 4 characters (`...XXXX`). Preserve that truncation in everything you show the user. If you ever see a full `sk-` value in output, stop and warn the user their key is exposed and should be rotated.

## How to run it

The exact install root varies (personal `~/.claude/skills/gateway-usage/` or project `.claude/skills/gateway-usage/`), so locate the script relative to whichever root this skill loaded from, then run it:

```bash
for root in "$HOME/.claude/skills/gateway-usage" ".claude/skills/gateway-usage"; do
  [ -f "$root/scripts/usage.sh" ] && SCRIPT="$root/scripts/usage.sh" && break
done
bash "$SCRIPT"
```

Flags:
- `--json`: machine-readable output (use this if you need to reason about the numbers programmatically before summarizing for the user).
- `--debug`: also dumps the raw response headers to stderr (useful for troubleshooting a gateway change; never share this output without redacting the key).

## How to present results

- Lead with **spend**, **max budget**, and **remaining budget** (computed as `max_budget - spend`; the gateway does not emit a dedicated remaining-budget header on this deployment, verified 2026-07-22).
- Always repeat, in your own words, these two caveats (do not omit them):
  - The $10/mo free tier is **per team**, not per key. A low personal spend number doesn't mean the team is still free.
  - Every request costs a flat **$0.002** on top of token cost, including failed/errored requests.
- If TPM/RPM rate-limit headers came back, mention them; if not, say plainly that the key has no rate limit configured (this is normal, not a problem).
- If `/key/info` was blocked (expected 403), do not treat it as an error to the user. Just note that exact budget-reset-date and TPM/RPM limit detail aren't available to end-user keys on this gateway, and if they need that, their team admin can see it in the UI at `https://api.ai.it.cornell.edu/ui` (Virtual Keys, then their key).
- If the script exits 1 (no key found), tell the user how to set `ANTHROPIC_AUTH_TOKEN` or where their key normally lives (Keychain / config.toml).
- If the script exits 2 (gateway call failed), show the exact HTTP status and the gateway's error message verbatim, then the specific hint the script already prints (expired key, budget exceeded, etc). Do not guess beyond what the script reported.
- Never print or log the full key. The script already truncates to the last 4 characters; preserve that truncation in your response.

## Where this runs

This skill reads spend from live `x-litellm-*` response headers, which requires a gateway key on the endpoint plus `curl`. That is true in the CLI and the in-app Code tab, but **not** in the Cowork sandbox.

- **Claude Code CLI (terminal):** full support. Key comes from `$ANTHROPIC_AUTH_TOKEN`, or the Keychain/config fallbacks.
- **Claude Desktop / in-app Code tab on a managed Mac or Windows box:** works. The key is resolved from the macOS Keychain (`cornell-ai-gateway`) or the `cornell-ai-helper` config.toml written by the endpoint-management helper. The script depends only on `curl`, `awk`, `sed`, and `mktemp`; `python3` is not required, and `jq` is optional (used only by `--json`).
- **Managed Cowork (isolated Linux sandbox):** **not supported by this skill.** In the Cornell managed-Cowork model the gateway credential lives server-side in the MCP; the Cowork endpoint holds no gateway key and has no `curl` path to the gateway. A Cowork usage check would need an equivalent **server-side MCP tool** that returns spend, not a client-side header read. Until such a tool exists, direct Cowork users to the admin UI at `https://api.ai.it.cornell.edu/ui`.

## Sandbox note (mktemp)

Some sandboxed shells (including Claude Code's own Bash sandbox) only allow writes under `$TMPDIR` and reject macOS's default `mktemp` path. The script works around this by wrapping `mktemp` to pass `-p "$TMPDIR"` whenever `$TMPDIR` is set, falling back to normal `mktemp` behavior otherwise.

## Notes for whoever maintains this skill

- Header names and the route-restriction behavior were verified live against the production Cornell gateway on 2026-07-22 (LiteLLM version reported: 1.93.0). If Cornell upgrades LiteLLM or changes route permissions, re-verify before trusting this skill's assumptions.
- Confirmed-live headers on this deployment: `x-litellm-key-spend`, `x-litellm-key-max-budget`, `x-litellm-response-cost` (plus `-original`, `-discount-amount`, `-margin-amount`, `-margin-percent`), `x-litellm-call-id`, `x-litellm-model-id`, `x-litellm-model-group`, `x-litellm-version`, `x-litellm-response-duration-ms`, `x-litellm-overhead-duration-ms`, `x-litellm-callback-duration-ms`, `x-litellm-attempted-retries`, `x-litellm-attempted-fallbacks`. Standard OpenAI-style `x-ratelimit-*` headers are documented but only populate when a key/team has TPM/RPM limits set.
- `x-litellm-key-max-budget` is **not** in the current public LiteLLM docs page (`docs.litellm.ai/docs/proxy/response_headers`) but IS returned live by Cornell's deployment. Trust the live header, not the docs gap, but don't assume other undocumented headers exist without testing.
