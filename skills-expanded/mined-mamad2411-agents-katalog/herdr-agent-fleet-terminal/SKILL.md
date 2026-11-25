---
name: herdr-agent-fleet-terminal
description: Applies Herdr (Can Celik, Sept 2026) — an open-source Rust terminal multiplexer purpose-built for AI coding agents, classifying sessions into working/blocked/done/idle/unknown states — the reference artifact for the "attention queue" UX pattern when supervising fleets of background coding agents. Use when [designing dashboards or CLIs for supervising parallel agents, choosing a multiplexer for multi-agent terminal workflows, evaluating agent-state detection approaches (hooks/plugins/output analysis), or comparing tmux vs agent-native runtimes]. NOT for [orchestrating agent task graphs (see multi-agent-orchestration-health-metrics), agent payment rails, or harness token-efficiency optimization (see nvidia-sol-pi-harness-self-optimization)].
---

# Herdr: The Terminal as an Attention Queue for Agent Fleets

## Overview
Herdr (Can Celik, open-sourced March 2026; Rust, Apache-2.0) is the first terminal multiplexer purpose-built for AI coding agents. Classic tmux answers "are the panes alive?" Herdr answers the question agent supervision actually raises: **which of my agents is waiting for me, right now?** Sessions are classified into five states — `working`, `blocked`, `done`, `idle`, `unknown` — and surfaced in a sidebar so human attention goes where it is scarce, not wherever a pane happens to be. The pattern generalizes: any product supervising parallel agents is building an attention queue, not a process manager.

## When to Use
- Designing dashboards/CLIs for supervising parallel coding agents across projects, repos, or machines
- Choosing between tmux (mature, general-purpose) and agent-native runtimes (state classification, notifications)
- Evaluating how a tool detects agent states (hooks/plugins vs terminal-output analysis)
- Sizing the one-person OSS funding pattern (36K stars in 4 months → $6M seed)

## Core Process / Workflow
1. **Define the attention queue, not the pane list.** Classify sessions into states that map to human action: working (no action needed), blocked (human input required — the queue), done (review ready), idle, unknown. The sidebar surfaces `blocked` first.
2. **Detect states three ways and accept the imperfection.** Hooks/plugins (exact, requires tool integration), output analysis (approximate, works with any agent), or explicit session IDs (resumable handoff). Herdr supports all three; production systems should prefer explicit signals where the agent tool exposes them.
3. **Persist sessions, not immortality.** Client-disconnect and network failure must not kill agent processes (PTY server/client architecture; restore matrix restores layout, directories, focus, and native agent session IDs). Do not claim server-restart survival — that is out of scope by design.
4. **Federate machines into one status surface.** Multi-machine mode (Sept 7, 2026) aggregates local + SSH-connected servers into one shared agent list: the selected machine shows the terminal, others keep updating status. The supervision plane is one surface; the execution plane stays distributed.
5. **Handle SSH as transport, not replacement.** OpenSSH does auth and host-key verification; remote mode is a client-server hop, not a custom protocol.
6. **Gate the plugin surface.** Herdr's own honesty: the plugin marketplace is uncurated — plugins/hooks/socket API can read terminal contents and secrets. Require review before production use (the pattern every agent-runtime marketplace must adopt).

## Key Evidence
- Scale: 36,000+ GitHub stars, 780K downloads, 1,000+ community plugins in ~4 months (launched March 2026).
- Funding: **$6M seed led by Bessemer Venture Partners (announced ~Sept 10, 2026)** with Y Combinator and e2vc; angel investors include Shopify CEO Tobi Lütke and Cloudflare CTO Dane Knecht. Solo founder Can Celik (Ankara); hiring planned for Rust/terminal/AI-agent talent.
- Ecosystem: Omarchy (DHH's distribution) integrated Herdr as the default agent multiplexer in v4 "Quattro" (with tmux), and DHH contributed window-title, pane-resize, and tab-shift patches — consumer + contributor in one.
- Architecture: client-server multiplexer (PTYs on Unix, ConPTY on Windows); workspaces/tabs/panes; states via hooks/plugins/output analysis; shared agent list across local + SSH servers; Unix Domain Socket / Named Pipe API for automation; Windows limitations (client-only serving since 0.8.2, no Windows server).
- Honest boundaries (from the project's own docs): optional terminal-history storage is disabled by default because it can contain credentials/tokens/prompts; "permanent" sessions are not immortal — server restart terminates processes, and the restore matrix recovers layout/state, not processes.
- Context: this is the agent-runtime layer on top of the existing agent market (JetBrains: 90% weekly adoption, Claude Code 39%); it monetizes *attention management*, not model inference.

## Pairs-with
- `progressive-disclosure-agent-skills-evidence` (harness-layer context: the flat index + agent attention)
- `nvidia-sol-pi-harness-self-optimization` (token efficiency layer above this)
- `agentic-adoption-trends-sept-2026` (the adoption data behind the fleet-supervision workload)
- `sonar-state-of-code-2026` (the verification load the fleet generates)
- `developer-experience-flow-state` (flow/attention theory this operationalizes)
- `aws-pizza-bot-agent-inbox` (the email-inbox sibling pattern for ambient agents)
- `gander-open-voice-agent-architecture` (the voice-lane sibling)

## A-Tech Alignment
- **Open source:** Rust + Apache-2.0; a one-person OSS project that monetizes via VC (not a paywalled core) — the solo OSS funding proof point for the "financial freedom" thesis.
- **Privacy:** terminal-history storage off by default; plugin/hook surfaces can read terminal contents — surface the trust boundary explicitly.
- **Financial freedom:** 36K stars → $6M seed in 4 months is the strongest recent datapoint for solo OSS maintainers turning mindshare into salary-scale funding without closing the core.
- **Practical:** five-state classification + three detection mechanisms is a one-afternoon pattern to adopt in any agent dashboard or CLI.

## Honesty Caveats
- Young project (0.1 → 0.9 in five months); the plugin marketplace is auto-populated, not curated — untrusted entries carry terminal-content access risk.
- Windows support is partial (client-side only); tmux remains the sober choice for simple, known-content sessions.
- Funding is seed-stage; no revenue yet — mindshare-to-revenue conversion is the open question.
- The "1,000+ plugins" figure is a community count, not curated marketplace listings.

*Sources: Herdr GitHub/announcement; heise online (Sept 2026); Lookonchain (Sept 13, 2026); Fundz (Sept 10, 2026); Omarchy v4 release notes; GitHub Sponsors profile (Can Celik).*