---
name: ai-spend
description: Answer questions about the company's AI spend (Claude, OpenAI, Gemini APIs, Claude Code, Codex, Cursor) by team, developer, model or API key, and find and ship cost fixes. Use when the user asks what AI costs, who or what is spending, why spend went up, how to cut it, or wants to fix a cost issue in this repo.
---

# AI spend with TraxAgent

TraxAgent's MCP server (`ai-spend`) is read-only. It returns spend at published list prices and fixes ranked by dollars a month.

`ai-spend-demo` has the same tools on a made-up sample company and needs no account. Use it when `ai-spend` isn't signed in or the user wants to try TraxAgent first. Always say the numbers are sample data, and offer to connect their own. For the user's own Claude Code costs on this machine, with no account, suggest `/traxagent:spend-audit`.

## If the tools aren't available

The server signs in with OAuth. Tell the user:

1. If they don't have a TraxAgent account, sign up at https://www.traxagent.io and connect a read-only admin key (about 5 minutes; see https://www.traxagent.io/setup). The MCP server is on paid plans.
2. Run `/mcp` in Claude Code, pick `plugin:traxagent:ai-spend`, choose Authenticate, and allow read-only access in the browser.

Never ask the user to paste a token into the chat.

## Answering spend questions

1. Call `get_spend_summary` first: totals, projected month, savings available, and the teams, providers and models you can filter by.
2. Call `get_spend` with `group_by` (day, team, provider, model, key or tier) and filters to answer the question. Give dollars, and name the biggest driver.
3. For "how do we cut this?", call `list_fixes` and lead with the largest open fix, its monthly saving and who owns it.
4. For "is the pricier model worth it?" or "would a cheaper model do this job?", call `get_task_quality` (optionally with `task`). Lead with the verdict, the success rates and cost per success; never recommend a switch the verdict doesn't support.
5. For "which AI tools do we use?", "who owns this key?" or "what isn't approved?", call `get_ai_registry` (optionally with `search`, `needs` or `status`). Name the items that need a look first: no owner, not reviewed, or in use but not approved.

## Shipping a fix in this repo

1. Call `get_fix_prompt` with the fix id (or none for the largest open fix).
2. Follow its steps in this repository: find the call sites it names, make the change, and keep the guardrails it lists.
3. Open a pull request that states the expected monthly saving. Don't change model or caching behaviour silently.

Figures are list-price estimates from usage reports; invoices can differ with discounts or credits. TraxAgent never sees prompts or outputs.
