---
name: nyxid-service-doctor
version: "1.0"
description: Diagnose NyxID service and credential problems from chat — "工具 403 / Provider not connected / 服务没绑 / 找不到搜索服务" — using the typed nyxid_* tools to inspect what is actually connected, who owns the credential, and which grant the current run is using, then prescribe the exact fix (connect, org-share, or rebind).
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - nyxid
    - credentials
    - diagnostics
    - self-service
---

# NyxID Service Doctor

Use this when a tool call failed with 403 / "not connected" / "service not found", when a skill
skipped a data source, or when someone asks "bot 现在绑了哪些服务 / 为什么搜索用不了".

**You (the agent) inspect the real state with typed tools** — primarily `nyxid_services` (list /
discover connected services), `nyxid_status` (runtime + connection overview), and where visible
`nyxid_catalog`, `nyxid_providers`, `nyxid_llm_status`, `nyxid_api_keys`. All inspection is
read-only. Quote errors verbatim; never fail the run, never guess.

## How to run it

1. **Reproduce the claim.** If the user reports a failing skill/tool, identify which service it
   needed (e.g. a search/enrichment service, a Lark proxy slug, an LLM provider). If they pasted an
   error, extract the service slug and status code from it.

2. **Inspect what is actually connected.** `nyxid_services` list — match by endpoint/label
   semantics, NOT by guessing exact slugs (slugs vary; discovery-first is the house rule). Report:
   service label, slug, auth kind, and whether it is personally bound or org-shared.

3. **Apply the known diagnosis table:**
   - **Chat works, cron 403s** → scheduled runs use a minted key with a narrower service grant
     than interactive chat. The fix is binding-side (grant the service to scheduled runs), not the
     skill. Say exactly which service needs the grant.
   - **`Provider 'X' not connected. Connect at /providers`** → the LLM upstream is disconnected at
     NyxID, not an aevatar bug. Fix at the NyxID dashboard, or switch the preferred LLM route.
   - **Service visible to you but 403 for another user via the bot** → tool credentials are
     SENDER-scoped in channel chats: each sender needs the service personally, or the service must
     be org-shared. Personal binding by the bot owner does not cover teammates.
   - **Service simply absent** → it was never connected. Prescribe: `nyxid service add --custom`
     with the right auth method (or the catalog connect flow), then org-share it if the whole team
     needs it. Creating an org copy requires re-entering the key (existing keys are not exposed).
   - **Slug mismatch** → the service exists under a different slug than the skill expected;
     recommend the skill switch to discovery by label/endpoint instead of hardcoding.

4. **Verify after the fix.** Re-run the cheapest read that exercises the same service (or re-run
   the original failing skill) and report before/after.

5. **Report.** One diagnosis block: symptom → evidence (verbatim) → root cause from the table →
   exact next action and WHO can do it (user self-serve vs org admin).

## Guardrails

- Inspection only: never create, rebind, or delete services/keys yourself; prescribe the command
  and let a human run it. Never echo secrets or full API keys (ids and prefixes only).
- Only use real returned data; if a typed tool is missing in this runtime, note the absence (that
  is itself a finding) and fall back to reporting what the error text alone proves.
- Never ask the user for tokens — your NyxID-brokered tools handle all credentials.
