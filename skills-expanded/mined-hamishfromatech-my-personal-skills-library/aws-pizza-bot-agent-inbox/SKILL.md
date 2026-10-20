---
name: aws-pizza-bot-agent-inbox
description: Applies AWS's Sept 10, 2026 open-sourcing of Pizza Bot — a community-project desktop app (own GitHub org, no AWS SLA) giving background/scheduled agents an email-style inbox where completed jobs arrive as unread threads and human decisions surface for action, built on DeepAgents/LangGraph with SQLite checkpoints, "the interface assumes you are not watching" as the core design tenet — as the reference implementation for ambient-agent UX. Use when [designing UIs for long-running background agents, evaluating inbox-style agent supervision patterns, building scheduled/autonomous agent products, or comparing agent-harness interfaces]. NOT for [cloud agent marketplaces (see agent-marketplace-builder-economy) or real-time conversational agent UX (see proactive-agent-design-taxonomy)].
---

# AWS Pizza Bot: The Agent Inbox Interface

## Overview
Pizza Bot is the first production-grade, openly available artifact solving the ambient-agent interface problem: chat is the wrong substrate for agents whose work continues while you're away. Its answer is email mechanics — persistent threads, unread state, decision surfacing — running on a self-hostable stack with resumable, checkpointed agent state.

## When to Use
- Designing products where agents run scheduled/autonomous background work
- Choosing between chat-first and inbox-first interaction models for an agent product
- Selecting an open runtime for long-running, pausable agent workflows
- Assessing the "human decision point" surface in agentic systems

## Core Process / Workflow
1. **Adopt the design tenet.** "The interface assumes you are not watching." Design for absence first: pauses that outlast the creating session, notifications worth acting on, and scheduled work that produces threads instead of logs.
2. **Map the inbox mechanics.** Completed jobs → unread threads; items needing human decision → surfaced for action; an Activity panel exposes jobs handed to specialist agents including tool use and progress. Email's asynchronous, interrupt-tolerant semantics map onto agent supervision with no invented UX.
3. **Build the persistence layer.** DeepAgents (LangChain's long-running-task harness) on LangGraph: agent state checkpointed as it works so a run can stop for approval, survive a disconnected client, and resume later without restart. Pizza Bot stores checkpoints, threads, and app data locally in SQLite and ordinary files.
4. **Self-host the server.** Local server by default; run on an always-on host or container so scheduled agents keep working while the laptop is closed and threads are picked up from another device.
5. **Choose the model per deployment.** Pluggable backends: Anthropic, Amazon Bedrock, Google Gemini, OpenAI, OpenRouter, or local models via Ollama — the harness is model-agnostic by construction.
6. **Extend through the two surfaces.** MCP servers (e.g., browser automation via Playwright MCP) and Agent Skills are the extension points; the bundled skill set shows how deterministic "recipes" parameterize agent actions.
7. **Note the product history as a case study.** Started April 2025 as "JoeBot," a side-of-desk CRM-logging script; became an MCP server executing parameterized recipes across internal systems; grew past 30 contributors and 2,000+ internal users; then "an MCP server requires an MCP client, and expecting non-technical users to work out of an IDE or terminal was never going to cut it" — hence the desktop inbox app. Lineage: LangChain's Jan 2025 "ambient agents" concept and its Agent Inbox reference implementation.

## Key Evidence
- Open-sourced Sept 10, 2026 as a standalone community project in its own GitHub org, deliberately separated from AWS ("no AWS support or service-level agreement — entirely self-hosted").
- AWS maintains a separate OSS SDK (Strands Agents) that sample-repo text describes as "a lighter-weight alternative to LangGraph for agents that don't need explicit graph control flow" — Pizza Bot chose LangGraph's explicit persistence/interrupts instead.
- Origin team: Joseph Dolivo (principal technologist, AWS Startups) and Igor Fil.

## Pairs-with
- `agent-experience-ax-devex-evolution`, `proactive-agent-design-taxonomy`, `outer-loop-harness-framework`, `agent-oversight-work-heuristics`, `mcp-code-execution-agent-efficiency`, `supervisory-engineering-work`, `openai-research-acceleration-intern` (supervision cost), `beyond-vibe-agentic-engineering`.

## A-Tech Alignment
- **Open source:** a fully open, self-hostable reference implementation — the strongest available template for privacy-preserving ambient agents (local SQLite, no cloud control plane).
- **Privacy:** data stays on your machine by default; model choice includes fully local inference.
- **Financial freedom:** zero SaaS dependency for the agent-runtime layer; the inbox pattern is buildable by a solo founder.
- **Practical:** copy the mechanics, not the brand — every component (checkpointing, MCP extension, inbox semantics) is documented and open.

## Honesty Caveats
- Community project: no SLA, no AWS support; maintenance continuity is on the community.
- The LangGraph-vs-Strands choice inside an AWS-adjacent project is a signal, not an official AWS product stance.
- Desktop-app packaging (macOS/Windows/Linux) means the UI layer is Electron-style surface area — audit it before untrusted-agent use.

*Source: The New Stack launch coverage (Sept 10, 2026); project LinkedIn post and blog from the co-creators.*