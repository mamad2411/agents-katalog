---
name: outbound-brief
description: Writes or updates outbound-brief.md, the one-page brief every outbound skill reads (what we sell, who buys, off-limits, proof, tone, autopilot), mostly from the Pastel workspace plus a few questions. Use on first run, when the brief is missing, or when the user's positioning, market, or sending rules change.
---

# Outbound brief

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

Pastel already knows a lot about the user's business. Read it first, ask only for what's left.

## Steps

1. **Pull from Pastel:** `pastel_get_workspace_context` (positioning, keywords, competitors, market), `pastel_list_icp_definitions`, `pastel_list_agents` (what their agents already watch), `pastel_list_connected_accounts` (who sends). If the user shares their website, read the homepage and pricing page.
2. **Fill** [`../command-center/shared/outbound-brief.template.md`](../command-center/shared/outbound-brief.template.md). After each line filled from a source, add where it came from: `<!-- from: pastel workspace -->`.
3. **Ask what's left, all at once, five questions at most.** Always confirm these four unless already known: results we can cite publicly, who is off-limits, what we ask for, autopilot on or off.
4. **Save** `outbound-brief.md` in the project root unless the user prefers `.codex/`. Unanswered lines stay `[missing]`.
5. **Compare with Pastel.** If the user's answers contradict an ICP definition or agent in Pastel, list the differences and offer `market-map` to update Pastel.
6. **Check the workspace** with the empty-result check. New users usually arrive during Pastel's first run: tell them it's running and roughly when leads will be ready.

Done when the file is saved, every line is filled or `[missing]`, and autopilot is explicitly on or off.
