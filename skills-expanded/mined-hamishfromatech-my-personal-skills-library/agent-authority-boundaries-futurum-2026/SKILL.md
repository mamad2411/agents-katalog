---
name: agent-authority-boundaries-futurum-2026
description: Applies Techstrong/Futurum's "The AI Agent Race" special report (Aug 2026; Futurum 2H 2026 Software Lifecycle Engineering survey, n=839) as the AGENT-AUTHORITY-BOUNDARY pattern — enterprises let AI write the change (40.17%) before they let it decide the change goes live (6.20%); 75.21% report ≥1 AI-contributed production incident while only 32.06% have human approval gates; the enterprise decision framework is cost-per-accepted-change, not token price or benchmark share. Use when designing agent adoption roadmaps, autonomy-rollout policies, or evaluating coding-agent vendors. NOT for [model leaderboard comparisons (read the denominator first), benchmark design critique, or per-vendor procurement checklists].
---

# Agent Authority Boundaries: Where Enterprises Stop the Agent

## Overview
Techstrong's "The AI Agent Race" (Alan Shimel, Aug 2026, Futurum data) reframes the coding-agent market from a model race to a systems race: model share ≠ agent share ≠ token share ≠ benchmark leadership ≠ customer outcomes. The load-bearing evidence is the authority gradient from the Futurum 2H 2026 Software Lifecycle Engineering survey (n=839): **AI is used in code generation by 40.17% and code review by 37.66%, but only 13.23% in CI/CD operations and 6.20% in deployment decisions**; individual developer assistance remains the dominant mode (47.20%) while autonomous end-to-end agents stand at 5.84%. Against that adoption curve: **75.21% of software-lifecycle decision-makers self-report at least one AI-contributed production incident** (another 17.52% suspect one), yet only **43.27% mandate human code review, 38.50% AI security scanning, and 32.06% human approval gates** for agent actions. The gap between reported incidents and deployed controls is the report's headline — and its decision framework ("pick the boundary before the brand") is a directly reusable adoption playbook.

## The Evidence Base
- **Four windows, four rankings (read the denominator):** OpenRouter 100T+ tokens (programming ~11% early 2025 → >50%; Claude >60% of programming spend, Google ~15%, OpenAI ~8%); Hugging Face agent activity (~40K Claude Code users, ~49M requests; Codex close behind); JetBrains 15K+ developers (Claude Code 39% adoption, Codex 16%, Copilot 21%, Cursor 12%, OpenCode 7%); Futurum enterprise production models (OpenAI 63.86%, Azure OpenAI 62.09%, Gemini 53.94% — multi-select, NOT coding-agent share).
- **The authority ladder:** assistance 47.20% → supervised agents 18.36% → semi-autonomous 13.59% → autonomous end-to-end 5.84% (15.02% no structured use). Lifecycle adoption falls steeply as consequence rises: generation 40.17% → review 37.66% → testing 28.01% → architecture 26.58% → observability 20.98% → incident response 16.21% → documentation 15.85% → CI/CD 13.23% → security scanning 12.40% → deployment decisions 6.20%.
- **The control gap:** 75.21% report ≥1 AI-contributed production incident (self-reported attribution, not verified causation; 41.60% multiple); among the 778 incident reporters/suspecters: defective AI code 44.34%, security vulnerability 38.69%, out-of-scope agent action 36.25%, sensitive-data exposure 26.86%, supply-chain compromise 19.54%, credential misuse 13.50%. Controls lag: mandatory human code review 43.27%, AI security scanning 38.50%, approval gates 32.06%, pre-promotion scoring 11.68%.
- **The benchmark trap:** OpenAI audited SWE-bench Verified and found material test/problem-design issues in 59.4% of 138 difficult tasks plus training-data contamination evidence, and stopped using it; SWE-Bench Pro (1,865 tasks, 41 repos) shows sharp performance drops on unseen code; Anthropic found a 6-point spread on Terminal-Bench 2.0 from infrastructure resources alone; Hugging Face's CLI study (0.94 vs 0.84 success; up to 6× tokens without a purpose-built CLI) shows tool interface as a first-class variable. A benchmark score is a property of model+harness+tools+environment+task-design.
- **The economics:** agentic token consumption varies up to 30× across eight frontier models on the same task, without buying accuracy; "cost per accepted change" (subscription + inference + compute + tools + human steering/review/rework + failure cost ÷ verified outcomes) is the enterprise metric; "the cheapest token can produce the most expensive pull request."
- **Production patterns:** Coinbase/Cursor (2,400+ developers, agents create 75% of PRs — vendor-published); Shopify River (co-authored 1 of 8 merged PRs on a years-built platform layer); Simplex/Codex (40% fewer design hours, 70% fewer dev hours in its use case). The agent gets the headlines; the surrounding platform decides whether it can ship.

## Core Findings (the authority-boundary pattern)
1. **Adoption tracks blast radius, not capability.** Enterprises will let AI write the change before they let it decide the change goes live; each step toward production multiplies consequence and shrinks adoption.
2. **Autonomy is a set of permissions, not a switch.** Read ≠ write ≠ PR-create ≠ PR-merge ≠ secrets ≠ infrastructure ≠ deploy; the decision tree starts from the job, not the leaderboard.
3. **The trust layer is architectural.** Nonhuman agent identity, least-privilege short-lived credentials, ephemeral constrained environments, deny-by-default network, approved-tools-as-dependencies, branch-not-protected-branch writes, pre-merge scans, risk-tiered approvals, complete audit logs, fast rollback.
4. **Cost per accepted change beats token price.** Agentic token variance (up to 30×) without accuracy gains means pricing comparisons on seat price or token price are category errors; measure total run cost ÷ verified outcomes.
5. **No synthetic market share.** OpenRouter, Hugging Face, JetBrains, Futurum, and customer stories measure different things; combining them into a single share number is the market's favorite mistake.

## When to Use
- Designing an agent-adoption roadmap or autonomy-rollout policy (the four-step decision tree: define work → context → tools → maximum authority, then expand only after reliability is proven inside the previous boundary).
- Evaluating coding-agent vendors for a specific work mode (developer assistance vs supervised delivery vs autonomous background) — the boundary decision precedes the brand decision.
- Building internal evals: run representative tasks with hidden acceptance tests, record completion/retries/human-intervention/defects/rollbacks, and don't let the agent grade itself (Hugging Face found agents self-reporting success when the change didn't exist).

## NOT For
- Model-share or leaderboard claims (the report's core methodological point is that these are different races).
- Benchmark methodology design (use the held benchmark-critique families; this skill holds the enterprise-decision lens).
- Per-vendor procurement scoring without a defined work mode — "there is a leader, but there will not be one horse for every course."

## Core Process / Workflow
1. **Define the work mode first.** Developer assistance / supervised delivery / background-autonomous — the agent class follows the job.
2. **Set the maximum authority before testing.** Name the blast radius (read/write/branch/PR/secrets/infra/prod) and require the agent to fit inside it, not the reverse.
3. **Test the system, not the model.** Evaluate model+harness+tools+environment+task-design on representative internal tasks with independent verification.
4. **Adopt the cost scorecard.** Cost per accepted change = (subscription + inference + compute + tools + steering + review + rework + failure) ÷ verified outcomes; track retries, review load, defect escape, cycle time.
5. **Expand authority only on evidence.** Reliability proven inside the prior boundary is the only license to widen it; the control gap (75% incidents vs 32% approval gates) is the baseline failure mode to design against.

## A-Tech Alignment
- **Open source:** the report elevates open harnesses (OpenHands, Cline, Kilo Code, OpenCode, Aider) to a strategic lane — sovereignty and model portability at the cost of operational discipline; A-Tech's sovereignty positioning maps directly onto the "regulated organizations choose open harnesses" branch.
- **Practical:** the four-window denominator discipline and the cost-per-accepted-change metric are directly reusable in A-Tech's agentic-workflow consulting narrative and content.
- **Trust design:** the boundary framework is the developer-side complement to the payment-layer mandate stack — authority + audit as architecture, not trust.

## Honesty Caveats
- All Futurum figures are proprietary survey results; incident attribution is self-reported and the survey does not establish causation; the source-lock process could not recover the exact "AI-contributed production incident" definition.
- Customer outcomes (Coinbase, Shopify, Simplex) are vendor-published, not controlled comparisons.
- Market-share framings are deliberately non-synthetic; any single-number share read from this evidence is a misuse.
- The report is published by a vendor ecosystem (Techstrong/Futurum) with a DevOps-experience event attached; treat narrative framing accordingly.

## Pairs-with
`devex-accountability-layer-dev-barometer-q3-2026` (the accountability-layer hour ledger), `agentic-verification-observability-loop` (the control-plane build), `agent-payment-record-gap` (the payment-layer identity/record contrast), `vibe-coding-governance-gap-shield` (the governance shield), `the-80-percent-problem` (the invisible-20%), `progressive-disclosure-agent-skills-evidence` (harness design), `outer-loop-harness-framework`, `harness-engineering-ai-agents-2026`.

## References
- Techstrong Research, "The AI Agent Race: At the Top of the Stretch" (Aug 2026; Futurum 2H 2026 SLE survey n=839; source notes F1–F8, P1–P13).
- OpenAI SWE-bench Verified audit (59.4% of 138 tasks with material issues); SWE-Bench Pro (1,865 tasks/41 repos); Anthropic infrastructure-noise analysis; Hugging Face CLI evaluation.
- OpenRouter 100T-token study; Hugging Face agent-traffic analysis; JetBrains 2026 Developer Ecosystem Survey (held by agentic-coder-segmentation).

*Created: 2026-09-17 (Cycle 28, Run 3) — A-Tech Research Division*