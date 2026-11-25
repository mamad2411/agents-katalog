---
name: deepseek-harness-open-runtime
description: Applies the DeepSeek Harness open-source agent runtime (MIT, 207K stars in two weeks, Claude Code/Codex as plugins) against xAI's Grok Bot subscription as the two opposite philosophies for agent infrastructure — give away the runtime layer vs sell agents as a product. Use when analyzing open-source agent infrastructure strategy, agent runtime vs model competition, or plugin architectures that absorb competitor agents.
---

# DeepSeek Harness: The Open Runtime Play

## Overview
DeepSeek open-sourced a 453,000-line TypeScript agent runtime under MIT on August 13, 2026 — the orchestration layer above the model (reasoning loops, tools, skills, sessions, sandboxes, execution, UI) that closed products like Claude Code used to control. It reached 207,000 GitHub stars in under three weeks and now runs competitor agents (Claude Code, Codex) as swappable plugins. This skill captures the strategic mechanics of "give away the runtime, sell the model" versus "sell the agent as a subscription product."

## When to Use
- Analyzing whether an AI infrastructure layer should be open-sourced or sold
- Evaluating agent runtime/harness competitive dynamics (who owns the orchestration layer)
- Designing plugin architectures that make competitor agents into components
- Content: "DeepSeek gave away the thing everyone else sells — here's why that works"

**NOT for**: open-weight *model* release strategy (use `open-weight-agentic-model-wave-august-2026`), harness maturity assessment (use `harness-maturity-matrix`), or payment protocols (use `agent-economy-payment-protocols`).

## Core Process

### 1. The two philosophies (same trend, opposite answers)
| Aspect | Grok Bot (xAI, Aug 11) | DeepSeek Harness (Aug 13) |
|---|---|---|
| Nature | Always-on agents with their own cloud computer | Open runtime, everything is a plugin |
| Access | Closed, subscription | MIT-licensed, self-hosted |
| Price | $120–$200/seat/month | Free runtime; pay for the model API |
| Model | Grok only | DeepSeek, Claude, GPT, any OpenAI-compatible endpoint |
| Trust | Buy a service, trust the black box | Build the box yourself; read all 453K lines |

Both turn the agent from a feature into a product. DeepSeek's bet: the durable moat is not the agent but the layer that orchestrates agents — so give it away and let the model API (and ecosystem gravity) monetize.

### 2. Why the architecture matters
- **Everything is a plugin** on the Cordis event-bus meta-framework (forked into the repo with 18 patches): models, tools, skills, sessions, sandboxes, filesystems, execution loops, even the GUI are swappable via configuration, not source changes.
- **Append-only session log**: everything the model sees (system prompts, reasoning, tool calls, context injections) is recorded, inspectable, resumable, forkable, replayable — the missing primitive when an agent derails 20 steps into a task.
- **Competitors become components**: since rc.8 (Aug 19), Claude Code and Codex install on demand as Profile Bundles inside the runtime, with non-interactive permission mode and named instances. Per-subagent provider/model/effort selection (alpha.1, Aug 27) enables cheap-model-for-cleanup + strong-model-for-architecture routing decided at runtime.

### 3. Velocity as signal
Seven releases in two weeks (rc.7 → v0.1.2-alpha.3, Aug 17–31): multimodal input, image uploads via Files API with reuse, Windows x64 Python SDK + persistent PowerShell PTY, per-subagent model routing, visible connection status, token/timing readouts, long-session memory reduction, SQLite backend removal. The release cadence — not the launch — is the health indicator for open infrastructure projects.

### 4. The pricing footgun worth tracking honestly
DeepSeek simultaneously moved V4-Pro to peak/off-peak dual pricing (off-peak $0.66/M in, $1.98/M out; peak double; cache hit $0.022/$0.044). Off-peak is still roughly double the previous $0.435/$0.87 flat rate — Reuters calculated increases of 50% to >1,000% by model/token type. The "open everything" play coexists with narrowing price advantage. Also note: the agentic benchmarks (Terminal Bench, DeepSWE) were measured with Harness in minimal mode — they describe model + infrastructure together, not the model alone.

### 5. Production-readiness caveats
Release-candidate/alpha versions, disclosed breaking changes, SQLite backend already removed. Excellent for studying a serious agent runtime and for experimentation; production use means frequent updates and configuration churn. The strategic reading is durable regardless: **the contest moved from the model to the runtime, and for the first time the runtime is open.**

## References
- Pairs with `harness-maturity-matrix` (harness maturity assessment), `open-weight-agentic-model-wave-august-2026` (the model-release counterpart), `open-source-ai-harness-frontier-2026` (harness-layer landscape), `give-away-keep-matrix-oss-ai` (the open/keep decision framework), `plan-limit-cognitive-thirst-trap` (the metered-subscription alternative).
- A-Tech alignment: open source (MIT, self-hostable, 453K readable lines — the runtime layer is the new commons), privacy (self-hosting keeps session logs and credentials local; jurisdiction caution when pointing at non-local APIs), financial freedom (free runtime + metered model = the anti-subscription architecture), practical (plugin-model pattern and append-only session log are copyable design moves).