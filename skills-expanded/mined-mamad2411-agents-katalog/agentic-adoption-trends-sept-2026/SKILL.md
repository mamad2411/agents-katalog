---
name: agentic-adoption-trends-sept-2026
description: Use when tracking AI coding agent adoption market share, advising teams on coding agent tool selection, analyzing Claude Code Codex Copilot Cursor competitive dynamics, or forecasting agentic tooling consolidation for developer platform strategy.
---

# Agentic Adoption Trends: September 2026 Update

**Source:** JetBrains Research, "AI Coding Agents: Adoption Trends" (Aug 2026, Developer Ecosystem Survey 2026 — 10th edition, 15,000+ professional developers, fielded May–Jul 2026) and "How Much Code Do Developers Really Let Agents Write?" (Aug 26 2026, same survey). This is the companion extraction to `agentic-coder-segmentation-2026` (which holds the three-segment code-origin clustering); this skill holds the *tool-level adoption and market-share* layer.

## Adoption Headlines (May–Jul 2026)

- **90% of professional developers use AI coding agents at work at least weekly; 68% daily.**
- **Claude Code: 39% adoption (18% → 39% since Jan 2026); 47% in the US.** Now the market leader, used twice as often as GitHub Copilot. Most-used-tool share 31% (≈80% conversion from usage → primary tool) — the loyalty metric that matters.
- **Codex: 5x growth in 6 months** (3% → 16%); awareness 27% → 65% — the fastest awareness ramp in the sample.
- **GitHub Copilot declined 29% → 21%** but retains the highest awareness (79% mindshare; 86–90% in EU/UK/US). Copilot is losing primary-tool share while remaining the broadest secondary tool.
- **Cursor declined 18% → 12%** (biggest drop in China: 28% → 16%) despite mindshare rising to 75%.
- **OpenCode (open-source): 7% adoption with 42% mindshare** — the highest mindshare-to-adoption ratio of any tool without a corporate backer; the strongest open-source signal in the dataset.
- **Google Antigravity: 6% adoption stable; awareness 29% → 47%.** India stronghold (15% adoption, tied third).
- JetBrains AI: 9% adoption (AI Assistant + Junie).

## Code-Origin Layer (links to the segmentation skill)

~47% of code fully agent-written / ~38% AI-assisted / ~27% manual. Agentic coders ~31% (84% agent-generated), AI-assisted ~47%, manual ~23%. Seniors adopt agentic fastest (~25% of seniors >80% agent-generated). **East Asia 32–35% vs Europe ~16% >80% agent-generated.**

**Tool signature:** Codex users are the most agentic-leaning (42% >80% agent-generated, 37% zero-manual) — interpreted as Codex attracting advanced users seeking better value/quota. Claude Code's mainstream surge means its audience is now broader/less specialized.

**Language split:** Go/JS/TS 54–55% agent-generated; C/C++ least agentic (38% manual); Java/Python middle (48–51%).

## Market-Structure Reading

1. **The IDE-completion era ended.** The market re-sorted from "Copilot in your IDE" to "standalone agentic tools" in under 18 months. Product excellence beats ecosystem lock-in (JetBrains' own framing).
2. **Consolidation is happening at the harness/protocol layer** (ACP lets agents plug into IDEs; JetBrains Central/Air orchestrate multi-agent workflows) — matches the Mozilla harness-layer thesis from this cycle.
3. **Open-source tooling holds a real beachhead:** OpenCode's 42% mindshare at 7% adoption is the signal to watch; it's the category's only tool gaining mindshare without a vendor marketing budget.
4. **Adoption ≠ satisfaction:** Claude Code +58 NPS (Digital Applied Q1) vs Copilot +14 — the loyalty gap explains why Copilot can hold awareness while losing primary share.

## Cross-Links

- `agentic-coder-segmentation-2026` — the three-segment clustering (this skill = tool layer)
- `claude-code`-adjacent content; `codex-agentic-ai-shift-evidence` — Codex diffusion evidence
- `mozilla-open-source-ai-state-2026` — usage/revenue gap; harness-layer thesis
- `sonar-state-of-code-2026`, `review-production-gap-observability-2026` — the downstream verification layer
- `acp-agent-client-protocol` — the integration mechanism enabling multi-agent IDE workflows

## A-Tech Fit

- **Open source:** OpenCode's mindshare anomaly and Codex's value-driven user base are the open-ecosystem story inside an otherwise closed-tool market.
- **Practical:** gives A-Tech clients current market-share evidence for tool-selection recommendations (Claude Code primary for multi-file work; Copilot as secondary completion; Codex for quota-heavy agentic work).
- **Content:** "The AI coding tool market re-sorted in 18 months" is a ready-made hamishfromatech narrative grounded in the 10th edition of the most representative survey in the space.