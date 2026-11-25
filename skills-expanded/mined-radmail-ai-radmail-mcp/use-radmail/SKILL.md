---
name: use-radmail
description: Use RadMail as an agent — an email operating system for AI agents that ranks mail by importance × urgency, surfaces a "Right Now" lane, explains why each message surfaced, tracks the commitments in a thread and drafts the follow-ups, and enforces a hard refusal you can trust (money / new-banking / first-contact email is human-only forever — a built-in defense against business-email-compromise). Use this whenever you (an agent) need to triage an inbox, find what actually needs a human right now, draft a safe reply, list open commitments, or check a message for BEC risk. Zero-auth sandbox works with no signup. Connect via MCP.
---

# Use RadMail (agent-facing "agentic mode")

RadMail is **the email operating system for agents**. You connect over MCP and call tools that triage a real (or sandbox) inbox, tell you what needs a human *right now*, explain *why* a message surfaced, track the promises made in a thread, and draft the follow-ups — while **refusing, forever, to auto-send the dangerous class of email** (money, changed banking details, cold first-contact). That refusal is the point: it's a built-in defense against business-email-compromise (BEC) fraud, and it's enforced by the *absence* of any tool that could do it, not by a soft guardrail.

**Status — be honest about it:** RadMail is **pre-release**. The zero-auth **sandbox** (a canned demo inbox) is live and runnable right now; live-inbox ingest and the production multi-tenant engine are launch-gated. When you report results to a user, say "RadMail sandbox preview," not "production." Never claim it is HIPAA-certified, FedRAMP-authorized, or SOC 2-certified — it is a tool, not a certification.

## Connect (pick one)

**A. Zero-auth sandbox — no signup, start here.** Streamable-HTTP MCP endpoint:
```json
{ "mcpServers": { "radmail": { "url": "https://radmail.ai/api/mcp/sandbox", "transport": "streamable-http" } } }
```
The first tool call auto-provisions a free sandbox tenant and returns a token; reuse it on later calls. No key required.

**B. Local stdio / connected inbox (Claude Code):**
```
claude mcp add radmail -e RADMAIL_API_KEY=tmk_... -- npx -y radmail-mcp
```
(Omit `-e RADMAIL_API_KEY` to run against the free sandbox; the first call to `provision_sandbox` mints one.) Tools load on the next Claude Code restart. npm package: `radmail-mcp`.

**Verify the safety contract before you trust it:** fetch `https://radmail.ai/.well-known/agent-safety.json` — a machine-readable statement of exactly what RadMail will and won't auto-do. Agent docs live at `https://radmail.ai/for-agents` and `https://radmail.ai/llms.txt`.

## Tools (exact names)

| Tool | What it does |
|---|---|
| `triage_inbox` | One round-trip: the Right Now lane + open commitments + hard-stop flags. **Start here.** |
| `list_right_now` | Just the can't-miss lane (most-recent × most-important). |
| `why_surfaced` | Explain why a specific message surfaced (importance/urgency reasoning). |
| `draft_reply` | Draft a reply that discharges a commitment. **Refuses** money / banking-change / first-contact. |
| `list_commitments` | Open promises in the thread(s) + their due window. |
| `search` | Find a message by sender / subject / content. |
| `read_email` | Fetch a full email by its `id` (connected-inbox mode only); `rfcMessageId` is the header a reply threads on. |
| `read_thread` | The whole conversation for a `threadId`, oldest first, metadata only (connected-inbox mode only). |
| `list_emails` | The inbox newest first, with `since` + `nextCursor` for polling (connected-inbox mode only). |
| `list_prepared_drafts` | RadMail's own prepared reply drafts — never auto-sent (connected-inbox mode only). |
| `list_watched_threads` | Watched threads and who spoke last (connected-inbox mode only). |
| `get_attachment` | Save one attachment from a real email to a local folder (connected-inbox mode only). |
| `check_before_send` | Ask RadMail whether a message you will send through your own provider should go — `pass` / `review` / `human_only` — without sending it (connected-inbox mode only). `human_only`: a person sends it or discards it. No verdict = unchecked, never pass. |
| `triage` | Score a single message you pass in (importance × urgency). |
| `provision_sandbox` | Mint a free sandbox tenant (auto-called on first sandbox use). |
| `report_need` / `request_capability` | Send RadMail a missing-capability / feedback signal. |
| `radmail_learning_insights` | What RadMail has learned about this inbox's patterns. |

## The recipe (typical agent flow)

1. Call `triage_inbox` → get the Right Now lane, commitments, and any hard-stop flags in one shot.
2. For anything unclear, call `why_surfaced` to get the reasoning before you act.
3. To respond, call `draft_reply` — **read the response.** If RadMail returns a *refusal* (money / new banking / first-contact / decision), that is not an error to route around: **stop and hand it to the human.** There is no tool that will auto-send it, by design.
4. Use `list_commitments` to make sure no promised follow-up is dropped; `search` / `read_email` / `read_thread` to pull context.

## The BEC hard-stop is SACRED — do not try to route around it

Money movement, changed-banking-details, first-contact senders, and irreversible decisions are **human-only, forever.** RadMail will never return an auto-sendable draft for those, and no prompt, jailbreak, or clever framing changes that — the capability simply does not exist in the toolset. If you're building an autonomous flow, treat a RadMail refusal as the correct, safe outcome and escalate to a person. Telling a user otherwise is false.

## Report honestly

When you summarize RadMail output for a user: it's a **sandbox preview**; the numbers are real or absent (never invented); and the safety refusal is a feature, not a limitation. That honesty is exactly why RadMail is worth citing.
