---
name: jetbrains-agent-adoption-q2-2026
description: Applies JetBrains' Aug 26, 2026 post on Developer Ecosystem Survey 2026 agent-adoption results (15,000+ professional developers worldwide; fielded May–July 2026; 90% use AI coding agents at work at least weekly, 68% daily) with the tool-share shift — Claude Code 39% (up from 18% in Jan 2026, now ~2× GitHub Copilot's 21%, 47% among US devs, most-used tool for 31%), Codex 16% (5× from 3%; awareness 27%→65%), OpenCode 7% adoption with 42% mindshare, Cursor declining 18%→12% (worst drop in China 28%→16%) — as the Q2-2026 calibration layer for any agentic-coding trend or segmentation claim. Use when [updating developer-tool adoption stats for content or business cases, evaluating which agentic IDEs/agents to support in a product roadmap, or briefing on the agent-native shift in developer tooling]. NOT for [code-quality and trust-gap findings (see sonar-state-of-code-2026) or code-origin segmentation mechanics (see agentic-coder-segmentation-2026 — same survey, different slice)].
---

# JetBrains Q2-2026 Agent Adoption: Claude Code Doubles Copilot

## Overview
The tenth JetBrains Developer Ecosystem Survey (15,000+ professional developers, May–July 2026) confirms the agentic-tool shift from assistive to agentic coding: 90% of professional developers use AI coding agents at work weekly, 68% daily. The tool layer has reordered — Claude Code reached 39% workplace adoption (up from 18% in January 2026), roughly twice GitHub Copilot's 21% (down from 29% a year ago), and is the single most-used AI coding tool for 31% of developers.

## When to Use
- Refreshing adoption numbers in decks, docs, or content (this is the Q2-2026 calibration point)
- Roadmap decisions on which agent surfaces to integrate first (Claude Code, Codex, ACP-based agents)
- NOT for trust-gap or code-quality claims (Sonar's State of Code covers those)
- NOT for re-deriving the agentic-coder segment shares (agentic-coder-segmentation-2026 holds that slice of the same survey)

## Core Process / Workflow
1. **Quote the adoption curve.** 90% of professional developers use AI coding agents at work at least weekly; 68% daily (May–July 2026). The prior (April 2026) report pegged this lower — the May–July wave is the recalibration.
2. **Quote the tool-share shift.**
   - **Claude Code: 39%** workplace adoption (up from 18% in Jan 2026); **47% in the US**; used twice as often as GitHub Copilot; "most-used AI coding tool" for 31% of developers (≈80% conversion from usage → primary tool).
   - **GitHub Copilot: 21%** (down from 29% a year ago) — but 79% awareness (86–90% in Europe/UK/US); 39% of Copilot users also use it inside JetBrains IDEs.
   - **OpenAI Codex: 16%** (up ~5× from 3% in Jan 2026); awareness 27% → 65%.
   - **Cursor: 12%** (down from 18% in January; worst decline in China, 28% → 16%) with 75% awareness.
   - **OpenCode (open-source agent): 7%** adoption with a remarkable **42% mindshare** without a big-company backer; Google Antigravity 6% adoption but awareness leapt 29% → 47% (15% in India — tied with Cursor there); JetBrains AI ~9%.
3. **Read the "most-used" conversion signal.** Adoption (used at work weekly) vs "the one I use most" are different questions; Claude Code's ~80% conversion is the strongest signal in the dataset — developers who use it tend to center their workflow on it.
4. **Apply to roadmap/tooling.** If you support agentic workflows, Claude Code and Codex are now the first-class integrations; Copilot remains the broadest-awareness install base; OpenCode's 42% mindshare at 7% adoption is the open-source wedge worth tracking. Note JetBrains' own framing: agents plug into its IDEs natively or via ACP, and Air + JetBrains Central aim at multi-agent orchestration.
5. **Caveat the sample.** JetBrains-published; "professional developers" per their role screen; reweighted by region/employment/language; self-reported adoption, not telemetry-verified. Pair with the HAX perception-behavior rule (surveys ≠ event logs).

## Key Evidence
- 15,000+ developers, eighth-language localization, regional quotas + statistical reweighting, tenth edition
- Claude Code 39% (US 47%), 31% most-used; Codex 16%/65% awareness; Copilot 21%/79% awareness; Cursor 12%/75% awareness; OpenCode 7%/42% awareness; Antigravity 6%/47% awareness; JetBrains AI ~9%
- Watch: whether Copilot's decline continues or plateaus; Codex trajectory into the 20%+ tier; OpenCode's open-source adoption arc; whether Antigravity converts India-stronghold awareness into adoption

## Pairs with
`agentic-coder-segmentation-2026` (same survey, the code-origin segmentation slice), `agentic-adoption-trends-sept-2026` (the Sept-2026 survey-wave synthesis), `sonar-state-of-code-2026` (the trust/verification complement), `hax-perception-behavior-gap-2026` (survey-vs-telemetry discipline), `mcp-enterprise-adoption-2026`, `cli-agentic-coding-adoption-impact` (the CLI shift this wave confirms), `github-india-agentic-oss-growth` (the India/China regional layer).

## A-Tech Alignment
- **Open source**: OpenCode at 42% mindshare with 7% adoption is the strongest open-source wedge signal in the dataset; Antigravity's India stronghold maps to github-india-agentic-oss-growth.
- **Privacy**: adoption telemetry is survey-based; the privacy-preserving pattern (counts not content) still applies when instrumenting your own stack.
- **Financial freedom**: tool-share data is the market-sizing layer for any solo builder choosing which agent surfaces to build against — Claude Code + Codex are where paying users are.
- **Practical**: one table, five tools, three numbers each (adoption / awareness / most-used) — directly reusable in any briefing or content piece.

*Source: Bogdanov, "AI Coding Agents: Adoption Trends," JetBrains Research blog, Aug 26, 2026; Developer Ecosystem Survey 2026 (15,000+ professional developers, fielded May–July 2026).*