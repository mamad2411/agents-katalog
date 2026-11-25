---
name: es-source-management
version: 1.0.0
description: Audit connected search sources, guide connecting missing ones, verify authorization, and set the priority order.
author: matrixx0070
tags: [enterprise-search, connectors, sources, configuration, onboarding, coverage]
capabilities: []
---

# Enterprise Search Source Management

## When to use
Reach for this when search coverage feels incomplete, before first real use, or when someone asks "what can you search?" or "why didn't you find X?" You audit connected sources, guide connecting missing ones, and order sources so the highest-signal ones lead.

**Not for:** running an actual search (es-search); planning a query (es-search-strategy); or summarizing activity from already-connected sources (es-digest).

## Method
1. **Inventory** every source category — chat, email, storage, trackers — and mark each connected, available-but-unconnected, or unsupported.
2. **Detect gaps.** *Decision:* if an unconnected source clearly holds relevant content, call it out explicitly — a missing source is the top cause of a false "not found."
3. **Guide connection.** For each source the user wants, give the concrete path: which connector, which scopes/permissions, where in settings. Point to the authorization flow; never request tokens or codes in-session.
4. **Verify authorization.** Confirm each connected source actually returns results with a trivial probe query. *Decision:* if a source authenticates but returns empty, flag it as broken rather than trusting the green checkmark.
5. **Set priority order.** Rank sources by signal density and trust for this user's work, so ranked search and digests weight them correctly.
6. **Note scope and limits** per source — date range, folders, private vs. shared — so results are honestly bounded.

## Example
User asks "why didn't you find the contract?" You inventory: Slack connected, Gmail connected, Drive **unconnected**. That is the gap — the contract lives in Drive. You give the connect path (Settings → Connectors → Google Drive, read-only scope, via the OAuth flow), then probe the two live sources to confirm they return results, and note Slack is limited to public channels.

## Pitfalls
- Searching around an obvious unconnected source and reporting "not found" without naming the gap.
- Trusting a connected badge without a probe — an authorized-but-empty source silently drops coverage.
- Requesting tokens or auth codes in the conversation instead of pointing to the authorization flow.
- Leaving priority order unset, so low-signal sources dilute ranked results and digests.

## Output format
```
Connected (with priority rank):
1. <source> — <scope/limits>
2. ...

Available to connect:
- <source> — connect via <concrete path / connector + scopes>

Unsupported / blocked:
- <source> — <why>

Recommended priority: <ordered list> — <rationale>
Coverage caveats: <known blind spots to expect>
```
