---
name: tiktok-warmup
description: Warms up TikTok accounts for Flooently + Blaze using Multilogin browser profiles. Use when running warmup sessions, creating new TikTok accounts, managing credentials, or reviewing session design. Triggers on /execute-warmups and any TikTok account management tasks.
license: MIT
metadata:
  author: frahman5
  version: '1.0.0'
---

# TikTok Warmup Skill

Warms up TikTok accounts for Flooently + Blaze using Multilogin browser profiles. Targets Spanish learners across Latin America.

**This is now a semi-manual system.** Faiyam runs `/execute-warmups` (see `prompts/execute-warmups.md`) when ready to warm up. The agent plans today's sessions, runs them in parallel across accounts, and relies on Faiyam for manual debugging (CAPTCHAs, re-logins, weird modals). No background scheduler, no cron — just a slash command.

## Pre-flight — run this immediately on skill load

First, update the skill to the latest version from fstack:

```bash
npx skills update
```

Then run the checks below and report health status for each activity. Do not block — just show the user what's ready and what isn't.

```bash
source .env.cli 2>/dev/null || true

# 1Password — TikTok vault
OP_VAULT_STATUS="❌ OP_SERVICE_ACCOUNT_TOKEN not set"
if [ -n "$OP_SERVICE_ACCOUNT_TOKEN" ]; then
  VAULTS=$(OP_SERVICE_ACCOUNT_TOKEN=$OP_SERVICE_ACCOUNT_TOKEN op vault list --format=json 2>&1)
  if echo "$VAULTS" | python3 -c "import json,sys; names=[v['name'] for v in json.load(sys.stdin)]; assert 'Tiktok' in names" 2>/dev/null; then
    OP_VAULT_STATUS="✅ 1Password Tiktok vault accessible"
  else
    OP_VAULT_STATUS="❌ Tiktok vault not found (wrong OP token, or vault not shared with this service account)"
  fi
fi

# MLX token
MLX_STATUS="❌ MLX_AUTOMATION_TOKEN not set"
[ -n "$MLX_AUTOMATION_TOKEN" ] && MLX_STATUS="✅ MLX_AUTOMATION_TOKEN set"

# AgentMail
AM_STATUS="❌ AGENTMAIL_KEY not set"
[ -n "$AGENTMAIL_KEY" ] && AM_STATUS="✅ AGENTMAIL_KEY set"

# Airtable — token must be present AND resolver must find a matching base
AT_STATUS="❌ AIRTABLE_ACCESS_TOKEN not set"
if [ -n "$AIRTABLE_ACCESS_TOKEN" ]; then
  RESOLVER_OUT=$(python3 .agents/skills/tiktok-warmup/resolve_airtable_schema.py 2>&1)
  if [ $? -eq 0 ]; then
    AT_STATUS="✅ $(echo "$RESOLVER_OUT" | head -1)"
  else
    AT_STATUS="❌ Airtable resolver failed: $(echo "$RESOLVER_OUT" | tail -2 | head -1)"
  fi
fi

echo ""
echo "🔍 Environment Health"
echo ""
echo "  Account Warmup:"
echo "    $MLX_STATUS"
echo "    $OP_VAULT_STATUS"
echo "    $AM_STATUS"
echo "    $AT_STATUS"
echo ""
echo "  Account Creation:"
echo "    $OP_VAULT_STATUS (needs read+write)"
echo "    $AM_STATUS"
echo "    $AT_STATUS"
echo ""
```

Report the output to the user before proceeding. If warmup prerequisites (MLX + OP vault) are missing, tell the user warmup won't work and ask if they want to fix it first.

---

## Reference Files

| File | Purpose |
|------|---------|
| [multiloginRef.md](multiloginRef.md) | **Multilogin X API reference** — auth, workspace IDs, profile IDs, how to start/stop profiles, Playwright connection. |
| [browserWarmupRef.md](browserWarmupRef.md) | **Browser warmup protocol** — humanized Playwright sessions on tiktok.com via Multilogin browser profiles. Preferred approach. |
| [loginRef.md](loginRef.md) | **TikTok login procedure** — do this yourself agentically, never delegate to ensure_login.py. Covers where creds live (1Password Claude-Accessible vault), OTP retrieval (AgentMail), captcha handling, and the visual login-verification checklist. |
| [sessionDesignRef.md](sessionDesignRef.md) | **How to compose the per-account task queue.** Target 50%+ niche-explicit time in early weeks. Recommended task mixes by week, anti-patterns, working example for Sofia. Read this when building a queue for any /execute-warmups run. |
| [accountsRef.md](accountsRef.md) | **Account registry auto-refresh protocol.** Accounts live in Airtable; scripts read from scripts/warmup/accounts.json. The agent refreshes the cache at step 2 of every /execute-warmups run so new/removed accounts propagate automatically with no code edits. |
| [airtableRef.md](airtableRef.md) | Airtable base/table/field IDs - Accounts + Session Log are the two tables we use. |
| [computerUseRef.md](computerUseRef.md) | Mobile cloud phone warmup - computer-use based. Used only for late-stage weeks or special cases. |
| [peekabooRef.md](peekabooRef.md) | Peekaboo CLI fallback - used when request_access fails for cloud phone sessions. |
| [runtimeLearnings.md](runtimeLearnings.md) | Operational learnings from live sessions - **read before every execution**. |
| [accountCreationRef.md](accountCreationRef.md) | How to create TikTok accounts and store credentials in 1Password. |
| [createTiktokRef.md](createTiktokRef.md) | Full interactive protocol for /create-tiktok — step-by-step account creation walkthrough. |
| [adoptAccountRef.md](adoptAccountRef.md) | Walkthrough for integrating a TikTok account created by someone else (e.g. a Fiverr freelancer) — credential takeover, Multilogin setup, Airtable registration, Postiz connection, Search Term generation. |
| [executeWarmupsRef.md](executeWarmupsRef.md) | Full protocol for /execute-warmups — plans and runs warmup sessions across all active accounts. |

## Protocols

- **Run today's warmups (the main thing)**: trigger /execute-warmups. Full protocol in executeWarmupsRef.md.
- **Run a one-off browser warmup session**: read multiloginRef.md + browserWarmupRef.md + runtimeLearnings.md, then invoke scripts/tiktok-warmup-poc.py.
- **Run a mobile warmup session** (rare): read multiloginRef.md + computerUseRef.md + runtimeLearnings.md.
- **Create a new TikTok account**: trigger `/create-tiktok`. Full protocol in createTiktokRef.md.
- **Adopt an externally-created account** (e.g. from Fiverr): read adoptAccountRef.md and walk the user through it step-by-step.
- **Multilogin API operations**: read multiloginRef.md.

## Design philosophy

Target 30-90 min of warmup per account per day, split into 2-4 sessions of 15-30 min each. Rest days in weeks 1-2 are natural (deterministic per account). The Scheduled Sessions Airtable table is deprecated - we log results directly to Session Log.
