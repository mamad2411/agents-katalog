---
name: run-macro-workflows
description: Run Opsphere macro_* composite workflows (outage triage, endpoint health, env health) on Team/Enterprise plans. Use when the user wants a structured multi-step investigation in one tool call, or when atomic tools would require many manual steps.
---

# Macro Workflows (`macro_*`)

Macros are **read-only composite tools** on the remote gateway. Each macro runs several atomic checks in sequence and streams **progress** (MCP Streamable HTTP / SSE) before returning a structured report.

**Plans:** Team and Enterprise only. Community tenants get `MACROS_PAID_ONLY` (403) — explain upgrade; do not retry blindly.

**Cursor:** Requires Cursor **2026+** with Streamable HTTP support for progress UI. If `tools/list` has no `macro_*` tools, skip this skill and use subagents or atomic tools.

## Available macros

Check `tools/list` before calling — never invent tool names.

In stable discovery, a visible macro does not prove plan eligibility or module
enablement. Check the active workspace availability, not just the Hub's plan;
respect explicit execution denials. Do not switch workspace to bypass a gate.
Stable-mode workspace changes do not require reconnecting.

| Tool | When to use | Typical args |
|------|-------------|--------------|
| `macro_endpoint_health` | Single hostname/URL: DNS + HTTP + TLS in one run | `hostname` or `url`; optional `port`, `path` |
| `macro_env_health` | Environment health snapshot (errors, deploys, capacity) | `env` (INT/TST/PRE/PRD) |
| `macro_outage_triage` | Site-down / widespread incident with edge + app correlation | `hostname` or `url`; `env`; optional `time_window_hours` |

## When to prefer macros vs subagents

| Situation | Prefer |
|-----------|--------|
| One URL — is it up? DNS + cert? | `macro_endpoint_health` (or `/endpoint-health` subagent) |
| Full incident — many services, deploy correlation | `macro_outage_triage` (or `/outage-triage`) |
| "How is PRE doing?" — env dashboard | `macro_env_health` |
| User on Community / no `macro_*` in list | `/outage-triage`, `/endpoint-health`, or atomic `dns_lookup` + `http_check` |
| User wants step-by-step control in chat | Atomic tools or subagent (not macro) |

Macros **replace long atomic chains** in telemetry — one macro call, not six separate tools for the same triage.

## Flow

1. **Plan gate** — Call `ops_my_usage` if the plan is unknown **and the tool is
   advertised**. In a direct corporate workspace where it is absent, only offer
   macros present in the live `tools/list`; gateway execution policy remains the
   authority. Community → stop with upgrade hint when confirmed.
2. **Catalog** — Confirm the macro exists in `tools/list`.
3. **Clarify** — Ask for missing hostname, environment, or time window (batch 2–3 questions max).
4. **Invoke** — Call the macro with structured arguments. Wait for the final JSON result; progress events are handled by the client.
5. **Report** — Summarize verdict, evidence bullets, and gaps (tools that were skipped). Treat macro output as point-in-time — verify critical facts with live tools if the incident is ongoing.

## Argument hints

- **Hostname:** bare domain (`api.example.com`) or full URL (`https://api.example.com/health`).
- **Environment:** match the user's chip or stated env (INT/TST/PRE/PRD). Community: one env only.
- **Outage window:** default last 1–6 hours unless the user specifies start time.

## Errors

| Signal | Action |
|--------|--------|
| `MACROS_PAID_ONLY` / 403 | Team/Enterprise required — link to pricing |
| Missing credentials for a step | Note in **Gaps**; continue with what the macro returned |
| Timeout / stall | Report partial progress; suggest narrower scope or atomic follow-up |

Do not store secrets. Do not call write/mutate tools from this skill.
