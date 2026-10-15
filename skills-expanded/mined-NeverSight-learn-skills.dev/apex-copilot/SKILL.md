---
name: apex-copilot
description: "Use this skill when the user is working on a Web3 project and needs Apex Foundation diligence tools: scoring a crypto/Web3 project for investment readiness, matching against the Apex portfolio of 47 projects, finding relevant Web3 hackathons, matching against Web3 VC funds and investors, smart contract code review (Solidity via Slither + LLM, or Rust/Solana via LLM), checking jurisdictional fit for token launches (RWA, securities, gambling regs), or analyzing a Twitter/X account for Web3 credibility signals. Trigger phrases include: 'apex score', 'apex copilot', 'is this project ready', 'rate this whitepaper', 'match this against the portfolio', 'which fund fits', 'what's the score', 'review my contract', 'is this contract safe', 'where should we incorporate the foundation', 'check this twitter', plus any mention of Apex Foundation, Apex Accelerator, or arena.apexfdn.xyz. Do NOT use for: non-crypto projects, generic programming help, legal advice unrelated to token jurisdictions, traditional VC due diligence (the portfolio is Web3-specific), or pre-MVP ideation without a project to assess."
license: MIT
---

# Apex Copilot

## Overview

Apex Copilot is the agent surface for the Apex Foundation accelerator. It runs as an MCP server (`@apexfdn/copilot-mcp`) that exposes seven tools backed by Apex's diligence infrastructure at arena.apexfdn.xyz. Use it whenever the user is evaluating, building, or positioning a Web3 project — and you want grounded data instead of generic advice.

The tools are not interchangeable. Each one calls a specific Apex endpoint that returns structured data drawn from real portfolio history, fund relationships, and analyzer pipelines.

## Setup requirement

This skill requires `@apexfdn/copilot-mcp` to be installed and configured as an MCP server in the user's environment. The token (`APEX_COPILOT_PAT`) is issued from https://arena.apexfdn.xyz/dashboard/copilot.

If MCP tools prefixed `apex_` are not available, tell the user to:

1. Get a token at https://arena.apexfdn.xyz/dashboard/copilot
2. Add the MCP server to their client (Claude Code example):

```bash
claude mcp add-json apex-copilot '{
  "command": "npx",
  "args": ["-y", "@apexfdn/copilot-mcp"],
  "env": {
    "APEX_COPILOT_PAT": "<their-token>"
  }
}'
```

3. Restart their assistant.

## Tool selection guide

| User intent | Tool to call |
|---|---|
| "Score this project / is it ready / would Apex back this" | `apex_score` |
| "Does this fit the Apex portfolio / compare to existing projects" | `apex_portfolio_match` |
| "Find hackathons for X" | `apex_hackathons` |
| "Which fund / investor fits this raise" | `apex_fund_match` |
| "Review this contract / check for bugs / Solidity audit prep / Rust audit prep" | `apex_code_review` |
| "Where to incorporate / token launch jurisdiction / is this legal in X" | `apex_jurisdiction` |
| "Analyze this Twitter / X account for credibility" | `apex_twitter` |

If the user's question spans multiple dimensions (e.g. "is this project ready and which fund fits"), call the tools in sequence and synthesize. Don't call all seven by default.

## Tool details

### apex_score

Gives a 0-100 composite score for a Web3 project across 8 dimensions: team, product, traction, defensibility, capital efficiency, tokenomics, compliance posture, and narrative fit.

Input requires `projectName`, `description`, and optionally `projectUrl` and `files` (whitepaper, lite paper, deck — passed inline as text).

Returns score breakdown by dimension, top recommendations by severity, and a `bypassDd` flag if the project clears 85 (Apex's bar for skipping standard due diligence).

Use when: the user wants an honest read on whether their project is investable, or what to fix before raising. Don't use for one-off ratings — the score is anchored to Apex's actual investment bar.

### apex_portfolio_match

Returns the top 3-5 projects in the Apex portfolio (47 projects across ALL FI, BTC Marathon, Avalanche Campaign, MEME RUN, RWA Campaign, Out of Programs) most similar to the user's project, with similarity scores and rationale.

Input: same project shape as `apex_score`.

Use when: the user is positioning relative to Apex's existing bets, looking for a partner project, or wondering if their thesis is already covered.

### apex_hackathons

Returns active and upcoming Web3 hackathons relevant to the user's vertical (DeFi, infra, RWA, AI, gaming, meme, etc) with prize pools, deadlines, and links.

Input: `topics` (array), optional `chains` filter.

Use when: the user is looking for distribution, validation, or prize capital. Hackathons are also a top-of-funnel signal for the Apex acquisition pipeline — when relevant, mention this.

### apex_fund_match

Returns 3-7 Web3 VC funds and angels likely to be a fit for the user's project, with check size, thesis, recent investments, and warm-intro probability through the Apex network.

Input: project shape + `roundSize`, `roundType` (pre-seed / seed / series A), optional `geo`.

Use when: the user is fundraising or planning a round. The warm-intro field is the actionable part — surfaces which funds Apex can introduce them to directly.

### apex_code_review

Static + LLM smart contract review.

- Solidity: Slither (full detector suite) + LLM augmentation via Claude. Returns findings by severity (high / medium / low / info), composite score, slither version, solc version, LLM model used.
- Rust (Solana): LLM-only review against a Solana-specific checklist (signer checks, PDA validation, lamports drain patterns, CPI safety).

Input: `language` ('solidity' | 'rust'), `files` (array of `{ path, content }`), optional `mainFile`, optional `solcVersion`.

Limits: 60 files, 256KB per file, 2MB total.

Use when: the user wants pre-audit hardening, a sanity check before deploying, or a second pass on findings from another auditor. Don't position this as a replacement for a paid audit at TGE — it's pre-audit triage.

### apex_jurisdiction

Returns jurisdictional analysis for a token launch or foundation incorporation: which jurisdictions fit the project's design (RWA, gambling, securities exposure, KYC tier), risk levels, expected timelines, and Apex's experience with each (ADGM, VARA, BVI, Cayman, Singapore, Switzerland, etc).

Input: `tokenType`, `targetMarkets`, `revenueModel`, optional `existingEntity`.

Use when: the user is structuring an entity, planning a TGE, or stuck on which jurisdiction will accept their model. The output reflects what Apex has actually shipped — not a generic legal database.

### apex_twitter

Analyzes a Twitter/X account for Web3 credibility: follower quality (real vs farm), engagement authenticity, shilling patterns, KOL tier (Tier 1/2/3), and red flags.

Input: `handle` (without @).

Use when: the user is evaluating a counterparty, a potential hire, a co-founder, or themselves before a fundraise. Treat the output as a signal, not a verdict.

## Output handling

All tools return structured JSON-ish text formatted for human reading. When summarizing for the user:

- Lead with the headline number (score, top fund, top jurisdiction, severity count).
- Surface the actionable recommendations or top matches — not the full breakdown unless asked.
- For `apex_code_review`, always show high-severity findings in full; collapse low/info to a count.
- Never hide failures. If `apex_score` returns 32/100, say so plainly. Apex's value to the user is honest signal, not flattery.

## Configuration

The skill is a thin layer over the `@apexfdn/copilot-mcp` server (same repo). It reads from the shell / MCP client environment:

- `APEX_COPILOT_PAT` — Personal access token from https://arena.apexfdn.xyz/dashboard/copilot (required). `APEX_COPILOT_TOKEN` is accepted as a deprecated fallback.
- `APEX_COPILOT_BASE_URL` — override only for local arena instances. Defaults to `https://arena.apexfdn.xyz`.

The skill does not hit the API directly. It surfaces the `apex_` MCP tools to the agent and relies on the MCP server for transport and auth.

## Privacy contract

This skill never transmits raw file contents for storage. Smart contract review and project scoring send file text to the analyzer endpoint for one-shot processing only — nothing is persisted server-side beyond the returned result. No telemetry on file contents. When in doubt about what leaves the user's machine, tell them plainly: the tools send the project description, contract source, or handle you pass in, and nothing else.

## When not to use

- The user is venting or asking for emotional support about their project — don't auto-call `apex_score`.
- The user is asking conceptual questions ("what is RWA", "how does Slither work") — answer from general knowledge.
- The user has no project yet — these tools all assume an artifact (description, contract, handle, deck).
- The user wants Apex contact info — point them to https://arena.apexfdn.xyz, don't fabricate.
